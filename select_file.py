from tkinter import filedialog
from tkinter import *
import os

def select_file(ext):

	filetypes = ((ext + " files","*"+ext),("all files","*.*"))

	root = Tk()
	root.withdraw()

	dir_i = os.getcwd()
	filename =  filedialog.askopenfilename(initialdir=dir_i,title="Select file",
		filetypes=filetypes)

	root.destroy()

	return filename