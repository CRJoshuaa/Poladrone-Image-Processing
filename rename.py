import os

import tkinter as tk
from tkinter import *
from tkinter import messagebox


class RenamePage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        global label_rename_folder
        global entry_image_set_name
        global progress_rename
        global label_progress_rename

        font_page_title=('Helvetica',16,'bold')
        font_label=("Verdana",10)

        renameImagePath=""
        imageSetName=""

        label=tk.Label(self,text="Rename Page",font=font_page_title)


        label_rename_folder = Label(self,
                                    text = "Selected Image Directory",
                                    width=55, height=4,
                                    font=font_label,
                                    wraplength=500,
                                    justify='left',
                                    anchor=W,
                                    fg='grey')
        button_rename_explorer = ttk.Button(self,
                                text = "Browse",
                                command = self.browseFiles)

        label_image_set_name=Label(self,text='Image Set Name: ',font=font_label)
        entry_image_set_name=ttk.Entry(self,width=40)

        label_progress_rename=Label(self,text="Standby",fg='orange')
        progress_rename=ttk.Progressbar(self,orient='horizontal',length=100,mode='determinate')


        button_rename_execute=ttk.Button(self,text="Rename", command=self.renameFunction)


        label.grid(column=0,row=0)

        label_rename_folder.grid(column = 1, row = 1,columnspan=10)
        button_rename_explorer.grid(column = 12, row = 1)

        label_image_set_name.grid(column = 1, row = 2)
        entry_image_set_name.grid(column=2, row=2)

        label_progress_rename.grid(column=1,row=3)
        progress_rename.grid(column=1,row=4)


        button_rename_execute.grid(column=10,row=5)




    def browseFiles(self):
        self.renameImagePath = filedialog.askdirectory(initialdir = "/",
                                              title = "Select a File")
        try:
            if not any(fname.endswith('.JPG') for fname in os.listdir(self.renameImagePath)):
                raise Exception("Directory has no .jpeg files")

        except Exception:
            messagebox.showerror("Select A Directory","JPG files(s) not found")
            return


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
            if not(filename.endswith('.JPG')):
                progress_rename['value']+=1
                progress_rename.update()
                continue
            dst=self.imageSetName+str("_"+'{:0>4}'.format(count))+".JPG"
            src=self.renameImagePath+'/'+filename
            dst=self.renameImagePath+'/'+dst

            os.rename(src,dst)

            progress_rename['value']+=1
            progress_rename.update()

        label_progress_rename.configure(text='DONE',fg='green')
