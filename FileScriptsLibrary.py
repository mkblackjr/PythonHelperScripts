from tkinter import *
from tkinter.filedialog import askopenfilename

def openFile(initial_dir):
	filepath = askopenfilename(initialdir = initial_dir,
								filetypes =(("Text File", "*.txt"),("All Files","*.*")),
								title = "Choose a file.")

	while not filepath:
		print("There was an error selecting the file. Please try again.\n")
		filepath = askopenfilename(initialdir = initial_dir,
								filetypes =(("Text File", "*.txt"),("All Files","*.*")),
								title = "Choose a file.")

	return filepath