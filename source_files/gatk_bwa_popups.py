#BWA popup classes

from Tkinter import *
import tkMessageBox
import tkFileDialog as tkfd
import subprocess
from time import sleep
import os

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