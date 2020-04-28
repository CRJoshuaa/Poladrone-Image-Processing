import os

import tkinter as tk
from tkinter import *
from tkinter import messagebox


class RenamePage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="Rename Page")
        label.grid(column=0,row=0)

        global label_rename_folder
        global entry_image_set_name
        global progress_rename
        global label_progress_rename

        renameImagePath=""
        imageSetName=""

        # Create a File Explorer label
        label_rename_folder = Label(self,
                                    text = "Browse Selected Images",
                                    width = 75, height = 4)
        button_rename_explorer = ttk.Button(self,
                                text = "Browse Files",
                                command = self.browseFiles)

        label_image_set_name=Label(self,text='Image Set Name')
        entry_image_set_name=Entry(self,width=40,borderwidth=2)

        label_progress_rename=Label(self,text="Standby",fg='orange')
        progress_rename=ttk.Progressbar(self,orient='horizontal',length=100,mode='determinate')


        button_rename_execute=ttk.Button(self,text="Rename", command=self.renameFunction)




        label_rename_folder.grid(column = 0, row = 1)
        button_rename_explorer.grid(column = 1, row = 1)

        label_image_set_name.grid(column = 0, row = 2)
        entry_image_set_name.grid(column=1, row=2)

        label_progress_rename.grid(column=0,row=3)
        progress_rename.grid(column=0,row=4)


        button_rename_execute.grid(column=1,row=5)




    def browseFiles(self):
        self.renameImagePath = filedialog.askdirectory(initialdir = "/",
                                              title = "Select a File")

        label_rename_folder.configure(text="File Opened: "+self.renameImagePath,fg='blue')
        label_progress_rename.configure(text='Standby',fg='orange')

    def renameFunction(self):
        #progress bar section config

        try:
            print(self.renameImagePath)
            if (self.renameImagePath==""):
                raise Exception("Empty Image Directory")

        except AttributeError:
            print("Empty Image Directory")
            messagebox.showerror("Select A Directory","Empty Image Directory")
            return;
        except Exception:
            print("Empty Image Directory")
            messagebox.showerror("Select A Directory","Empty Image Directory")
            return;




        label_progress_rename.configure(text='PROCESSING',fg='red')
        progress_rename['value']=0
        progress_rename['maximum']=len(os.listdir(self.renameImagePath))


        if (entry_image_set_name.get()==""):
            self.imageSetName="default"
        else:
            self.imageSetName=entry_image_set_name.get().replace(' ',"_")


        for count,filename in enumerate(os.listdir(self.renameImagePath)):
            dst=self.imageSetName+str("_"+'{:0>4}'.format(count))+".jpg"
            src=self.renameImagePath+'/'+filename
            dst=self.renameImagePath+'/'+dst

            os.rename(src,dst)

            progress_rename['value']+=1
            progress_rename.update()

        label_progress_rename.configure(text='DONE',fg='green')
