#GATK Main Application  Class File

from Tkinter import *
import tkMessageBox
import tkFileDialog as tkfd
import subprocess
from time import sleep
import os

#modules
from gatk_bwa_popups import *

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
      
      self.out_dir_label = Label(self, text='Output Directory')
      self.out_dir_label.grid(row = 6, column = 0, sticky = W)
      
      self.out_dir_path = Text(self, width = 65, height = 1, background='white')
      self.out_dir_path.grid(row = 7, column = 0, sticky = W)
      self.out_dir_path.config(state = DISABLED)
      
      self.out_dir_button = Button(self, text='Browse', command = lambda:self.file_select('3'))
      self.out_dir_button.grid(row = 7, column = 1, sticky = W, padx = 10, pady = 10)
      
      self.run_button = Button(self, text='Begin Processing', command = self.run)
      self.run_button.grid(row = 8, column = 0, columnspan = 3, pady = 10)
   
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
	file_name = tkfd.askdirectory(parent=self, title='Select BWA Aligner directory')
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
	file_name = tkfd.askdirectory(parent=self, title='Select Picard Tools directory')
	self.picard_directory_path.insert(INSERT, file_name)
	self.picard_directory_path.config(state = DISABLED)
	
	with open('paths.txt', 'r') as file:
	  lines = file.readlines()
	lines[1] = file_name + '\n'
	with open('paths.txt', 'w') as file:
	  file.writelines(lines)
			 
      elif file_type=='2':
	#this is samtools_directory
	self.samtools_directory_path.config(state = NORMAL)
	self.samtools_directory_path.delete(1.0, END)
	file_name = tkfd.askdirectory(parent=self, title='Select SamTools directory')
	self.samtools_directory_path.insert(INSERT, file_name)
	self.samtools_directory_path.config(state = DISABLED)
	
	with open('paths.txt', 'r') as file:
	  lines = file.readlines()
	lines[2] = file_name + '\n'
	with open('paths.txt', 'w') as file:
	  file.writelines(lines)
	  
      else:
	#this is the output directoyr
	self.out_dir_path.config(state = NORMAL)
	self.out_dir_path.delete(1.0, END)
	file_name = tkfd.askdirectory(parent=self, title='Select output directory')
	self.out_dir_path.insert(INSERT, file_name)
	self.out_dir_path.config(state = DISABLED)
	
   def run(self):
     #runs the tools
     
     if (self.bwa_directory_path.get(1.0,END).rstrip('\n') == '' or self.picard_directory_path.get(1.0,END).rstrip('\n') == '' or self.samtools_directory_path.get(1.0,END).rstrip('\n') == '' or self.out_dir_path.get(1.0,END).rstrip('\n') == ''):
       tkMessageBox.showerror('Process Error', 'The tools directories are not entered, aborting...')
       return
     
     bwa_prompt = BWAPopup1(self)
     index_name = None
     bwa_path = None
     out_directory = self.out_dir_path.get(1.0, END).rstrip('\n')
     self.wait_window(bwa_prompt)
     
     sleep(0.25)
     
     if (bwa_prompt.getExitCode() == 0):
	tkMessageBox.showerror('Process Error', 'Fields were not filled out correctly, aborting...')
	return
     else:
        bwa_path = self.bwa_directory_path.get(1.0, END).rstrip('\n')
        index_name = bwa_prompt.getFileNameInput()
        fasta_path = bwa_prompt.getPathInput()
        
	p = subprocess.Popen([bwa_path + '/bwa', 'index', '-a', 'bwtsw', '-p', out_directory + '/' + index_name, fasta_path])
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
	
	sam_file = file(out_directory + '/' + sam_out + '.sam', 'w') 
	
	if bwa_prompt2.useP():
	   p = subprocess.Popen([bwa_path + '/bwa', 'mem', '-t', cores, '-p', '-v', '1', index_name, fastq], stdout=sam_file)
	   p.wait()
	else:
	   p = subprocess.Popen([bwa_path + '/bwa', 'mem', '-t', cores, '-v', '1', index_name, fastq], stdout=sam_file)
	   p.wait() 
	   
	sam_file.close()