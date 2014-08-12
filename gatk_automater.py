from Tkinter import *
import tkMessageBox
import tkFileDialog as tkfd
import subprocess
from time import sleep
import os

class AppGATK(Frame):
   
   def __init__(self, parent, *args, **kwargs):
      Frame.__init__(self, parent)
      self.bwa_directory_label = Label(self, text='BWA Aligner Directory')
      self.bwa_directory_label.grid(row=0, column=0, sticky = W)
      
      self.bwa_directory_path = Text(self, width = 65, height = 1, background='white')
      self.bwa_directory_path.grid(row=1, column=0, sticky = W)
      
      self.bwa_directory_button = Button(self, text='Browse', command = lambda:self.file_select('0'))
      self.bwa_directory_button.grid(row=1, column=1, sticky = W, padx = 10, pady = 10)
        
      self.picard_directory_label = Label(self, text='Picard Tools Directory')
      self.picard_directory_label.grid(row=2, column=0, sticky = W)
      
      self.picard_directory_path = Text(self, width = 65, height = 1, background='white')
      self.picard_directory_path.grid(row=3, column=0, sticky = W)
      
      self.picard_directory_button = Button(self, text='Browse', command = lambda:self.file_select('1'))
      self.picard_directory_button.grid(row=3, column=1, sticky = W, padx = 10, pady = 10)
      
      self.samtools_directory_label = Label(self, text='SamTools Directory')
      self.samtools_directory_label.grid(row=4, column=0, sticky = W)
      
      self.samtools_directory_path = Text(self, width = 65, height = 1, background='white')
      self.samtools_directory_path.grid(row=5, column=0, sticky = W)
      
      self.samtools_directory_button = Button(self, text='Browse', command = lambda:self.file_select('2'))
      self.samtools_directory_button.grid(row=5, column=1, sticky = W, padx = 10, pady = 10)
      
      self.run_button = Button(self, text='Begin Processing', command = self.run)
      self.run_button.grid(row = 5, column = 2, sticky = W)
   
   def read_saved_paths(self, path_file):
      self.bwa_directory_path.config(state = NORMAL)
      self.bwa_directory_path.delete(1.0, END)
      self.bwa_directory_path.insert(INSERT, path_file.readline())
      self.bwa_directory_path.config(state = DISABLED)
      
      self.picard_directory_path.config(state = NORMAL)
      self.picard_directory_path.delete(1.0, END)
      self.picard_directory_path.insert(INSERT, path_file.readline())
      self.picard_directory_path.config(state = DISABLED)
      
      self.samtools_directory_path.config(state = NORMAL)
      self.samtools_directory_path.delete(1.0, END)
      self.samtools_directory_path.insert(INSERT, path_file.readline())
      self.samtools_directory_path.config(state = DISABLED)
    
   def file_select(self, file_type):
      #file_type is internal, uses string ints (goes in order of layout in __init__
      if file_type == '0':
	#this is bwa_directory
	self.bwa_directory_path.config(state = NORMAL)
	self.bwa_directory_path.delete(1.0, END)
	file_name = tkfd.askdirectory(parent=root, title='Select BWA Aligner directory')
	self.bwa_directory_path.insert(INSERT, file_name)
	self.bwa_directory_path.config(state = DISABLED)
	
	with open('paths.txt', 'r') as file:
	  lines = file.readlines()
	lines[0] = file_name + '\n'
	with open('paths.txt', 'w') as file:
	  file.writelines(lines)
	
      elif file_type=='1':
	#this is picard_directory
	self.picard_directory_path.config(state = NORMAL)
	self.picard_directory_path.delete(1.0, END)
	file_name = tkfd.askdirectory(parent=root, title='Select Picard Tools directory')
	self.picard_directory_path.insert(INSERT, file_name)
	self.picard_directory_path.config(state = DISABLED)
	
	with open('paths.txt', 'r') as file:
	  lines = file.readlines()
	lines[1] = file_name + '\n'
	with open('paths.txt', 'w') as file:
	  file.writelines(lines)
			 
      else:
	#this is samtools_directory
	self.samtools_directory_path.config(state = NORMAL)
	self.samtools_directory_path.delete(1.0, END)
	file_name = tkfd.askdirectory(parent=root, title='Select SamTools directory')
	self.samtools_directory_path.insert(INSERT, file_name)
	self.picard_directory_path.config(state = DISABLED)
	
	with open('paths.txt', 'r') as file:
	  lines = file.readlines()
	lines[2] = file_name + '\n'
	with open('paths.txt', 'w') as file:
	  file.writelines(lines)
	
   def run(self):
     #runs the tools
     
     if (self.bwa_directory_path.get(1.0,END).rstrip('\n') == '' or self.picard_directory_path.get(1.0,END).rstrip('\n') == '' or self.samtools_directory_path.get(1.0,END).rstrip('\n') == ''):
       tkMessageBox.showerror('Process Error', 'The tools directories are not entered, aborting...')
       return
     
     bwa_prompt = BWAPopup1(self)
     index_name = None
     bwa_path = None
     self.wait_window(bwa_prompt)
     
     sleep(0.25)
     
     if (bwa_prompt.getExitCode() == 0):
	tkMessageBox.showerror('Process Error', 'Fields were not filled out correctly, aborting...')
	return
     else:
        bwa_path = self.bwa_directory_path.get(1.0, END).rstrip('\n')
        index_name = bwa_prompt.getFileNameInput()
        fasta_path = bwa_prompt.getPathInput()
        
	p = subprocess.Popen([bwa_path + '/bwa', 'index', '-a', 'bwtsw', '-p', index_name, fasta_path])
	p.wait()
    
     bwa_prompt2 = BWAPopup2(self, index_name)
     self.wait_window(bwa_prompt2)
     
     sleep(0.25)
     
     if (bwa_prompt2.getExitCode() == 0):
	tkMessageBox.showerror('Process Error', 'Fields were not filled out correctly, aborting...')
	return
     else:
	cores = bwa_prompt2.getCores()
	fastq = bwa_prompt2.getFastq()
	sam_out = bwa_prompt2.getSAM()
	
	sam_file = file(sam_out + '.sam', 'w') 
	
	if bwa_prompt2.useP():
	   p = subprocess.Popen([bwa_path + '/bwa', 'mem', '-t', cores, '-p', '-v', '1', index_name, fastq], stdout=sam_file)
	   p.wait()
	else:
	   p = subprocess.Popen([bwa_path + '/bwa', 'mem', '-t', cores, '-v', '1', index_name, fastq], stdout=sam_file)
	   p.wait() 
	   
	sam_file.close()
     
class BWAPopup1(Toplevel):
    def __init__(self, parent):
	Toplevel.__init__(self, parent)
	self.label = Label(self, text='Name index file')
	self.label.grid(row = 0, column = 0, sticky = W)
	self.text_entry = Text(self, width=30, height=1, background='white')
	self.text_entry.grid(row = 1, column = 0, sticky = W)
	
	self.label2 = Label(self, text='Browse fasta file')
	self.label2.grid(row = 2, column = 0, sticky = W)
	self.file_path = Text(self, width=30, height=1, background='white')
	self.file_path.grid(row = 3, column = 0, sticky = W)
	self.file_path.config(state = DISABLED)
		     
	self.browse = Button(self, text='Browse', command=self.browse)
	self.browse.grid(row = 3, column = 1, sticky = W)
	
	self.button_ok = Button(self, text='Ok', command = self.confirm)
	self.button_ok.grid(row = 4, column = 0, sticky = W)
	self.button_cancel = Button(self, text='Cancel', command = self.cancel)
	self.button_cancel.grid(row = 4, column = 0, sticky = E)
	
	self.exit_code = 0
    
    def browse(self):
	self.file_path.config(state = NORMAL)
	self.file_path.delete(1.0, END)
	file_name = tkfd.askopenfilename(filetypes = [('fasta files','.fasta')])
	self.file_path.insert(INSERT, file_name)
	self.file_path.config(state = DISABLED)
    
    def cancel(self):
      self.exit_code = 0
      self.destroy()
      
    def confirm(self):
      self.exit_code = 1
      
      if (self.text_entry.get(1.0, END).rstrip('\n') == ''):
	self.exit_code = 0
      
      if (self.file_path.get(1.0, END).rstrip('\n') == ''):
	self.exit_code = 0
      
      self.index_name = self.text_entry.get(1.0, END).rstrip('\n')
      self.fasta_path = self.file_path.get(1.0, END).rstrip('\n')
      
      self.destroy()
    
    def getExitCode(self):
	return self.exit_code
    
    def getFileNameInput(self):
	if (self.exit_code == 0):
	    return None
	else:
	  return self.index_name
	
    def getPathInput(self):
      if (self.exit_code == 0):
	  return None
      else:
	 return self.fasta_path
	
class BWAPopup2(Toplevel):
    
    def __init__(self, parent, index_file):
      Toplevel.__init__(self, parent)
      self.index_file = index_file
      self.use_p = False
      self.label1 = Label(self, text='Name the output SAM file')
      self.label1.grid(row = 0, column = 0, sticky = W)
      self.sam_entry = Text(self, width = 32, height = 1, background='white')
      self.sam_entry.grid(row = 1, column = 0, sticky = W)
      self.label2 = Label(self, text='Enter number of cores (between 1 and 8):')
      self.label2.grid(row = 0, column = 2, sticky = W)
      self.core_entry = Text(self, width = 4, height = 1, background='white')
      self.core_entry.grid(row = 0, column = 3, sticky = W)
      self.p_check = Checkbutton(self, text = ' Interleaved Reads?', variable=self.use_p)
      self.p_check.grid(row = 1, column = 2, sticky = W)
      self.label3 = Label(self, text='Select your fastq file')
      self.label3.grid(row = 2, column = 0, sticky = W)
      self.fastq_path = Text(self, width = 32, height = 1, background = 'white')
      self.fastq_path.grid(row = 3, column = 0, sticky = W)
      self.fastq_path.config(state = DISABLED)
      self.fastq_browse = Button(self, text = 'Browse', command = self.browse)
      self.fastq_browse.grid(row = 3,column = 1, sticky = W)
      
      self.confirm_button = Button(self, text = 'Confirm', command = self.confirm)
      self.confirm_button.grid(row = 4, column = 2, sticky = E)
      self.cancel_button = Button(self, text = 'Cancel', command = self.cancel)
      self.cancel_button.grid(row = 4, column = 3, sticky = W)
      
      self.exit_code = 0
      
    def browse(self):
      self.fastq_path.config(state = NORMAL)
      self.fastq_path.delete(1.0, END)
      file_name = tkfd.askopenfilename(filetypes = [('fastq files','.fastq')])
      self.fastq_path.insert(INSERT, file_name)
      self.fastq_path.config(state = DISABLED)
      
    
    def confirm(self):
	self.exit_code = 1
	self.sam_entry_text = ''
	self.fastq_path_text = ''
	self.core_num = ''
	
	if (self.sam_entry.get(1.0, END).rstrip('\n') == ''):
	    self.exit_code = 0
	else:
	    self.sam_entry_text = self.sam_entry.get(1.0, END).rstrip('\n')
	    
	if (self.fastq_path.get(1.0, END).rstrip('\n') == ''):
	    self.exit_code = 0
	else:
	    self.fastq_path_text = self.fastq_path.get(1.0, END).rstrip('\n')
	    
	try:
	    self.core_num = self.core_entry.get(1.0, END).rstrip('\n')
	    int_core = int(self.core_num)
	    if (int_core < 1 or int_core > 8):
		exit_code = 0
	except:
	  exit_code = 0
	  
	self.destroy()
	
    def cancel(self):
	self.destroy()
	
    def getExitCode(self):
	return self.exit_code
      
    def getSAM(self):
	return self.sam_entry_text
      
    def getFastq(self):
	return self.fastq_path_text
      
    def getCores(self):
	return self.core_num
      
    def useP(self):
	return self.use_p      
    
    
root = Tk()
root.title('GATK Processor')

app = AppGATK(root)
app.pack()

if not os.path.isfile('paths.txt'):
  mk_file = file('paths.txt', 'w')
  mk_file.writelines(['PATH HERE\n', 'PATH HERE\n', 'PATH HERE\n'])
  mk_file.close()
  
paths = file('paths.txt','r+')

app.read_saved_paths(paths)

root.mainloop()