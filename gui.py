from tkinter import *
from tkinter import simpledialog

SUBREDDIT_FILE_NAME = "subreddits.txt"
	
def onBtnAdd():
	input = simpledialog.askstring("Add Subreddit", "Please enter a subreddit", parent=root)
	
	if input == None:
		return
	
	subreddits = listbox.get(0, END)
	for subreddit in subreddits:
		if subreddit == input:
			return
	
	listbox.insert(END, input)
	updateSubreddits()
	return

def onBtnDelete():
	selection = listbox.curselection()[0]
	listbox.delete(selection)
	updateSubreddits()
	return
	
def updateSubreddits():
	subreddits = listbox.get(0, END)
	with open(SUBREDDIT_FILE_NAME, 'w+') as file:
		for subreddit in subreddits:
			file.write(subreddit + "\n")
	return
	
def loadSubreddits():
	subreddits = []
	with open(SUBREDDIT_FILE_NAME, 'r') as file:
		subreddits = file.read().splitlines()
	return subreddits
	
def onBtnDownload():
	print("download")
	return

root = Tk()
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
root.title("Reddit Downloader")

listbox = Listbox(root)
# listbox.bind('<<ListboxSelect>>', onItemSelect)
listbox.pack(pady = 10)

subreddits = loadSubreddits()
for subreddit in subreddits:
	listbox.insert(END, subreddit)
	
buttonFrame = Frame(root)
buttonFrame.pack(pady = 5)
btnAdd = Button(buttonFrame, text="Add", command=onBtnAdd)
btnAdd.pack(padx = 10, side = LEFT)
btnDelete = Button(buttonFrame, text="Delete", command=onBtnDelete)
btnDelete.pack(padx = 10, side = LEFT)
btnDownload = Button(root, text="Download", command=onBtnDownload)
btnDownload.pack(pady = 5, side = BOTTOM)
	
root.mainloop()