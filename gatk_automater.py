#Application Root File

#Old imports, will eventually be reorganized
from Tkinter import *
import tkMessageBox
import tkFileDialog as tkfd
import subprocess
from time import sleep
import os


#Class imports for custom modules
from source_files import *   
    
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