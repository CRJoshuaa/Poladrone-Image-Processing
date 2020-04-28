import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
import shutil
import os


class NthValueOutOfRange(Exception):
    def __init__(self,msg):
        super().__init__(msg)


class SelectPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="Select Page")
        label.grid(column=0,row=0)

        global label_cropped_folder
        global label_selected_folder
        global entry_nth_number
        global progress_select
        global label_progress_select

        croppedPath=""
        selectedPath=""

        label_cropped_folder=Label(self,
                                text="Browse Cropped Image Location ",
                                width=75, height=4)
        button_cropped_explorer=ttk.Button(self,
                                    text="Browse",
                                    command=lambda:self.browseFiles(label_cropped_folder))


        label_selected_folder=Label(self,
                                text="Browse Selected Image Location ",
                                width=75, height=4)
        button_selected_explorer=ttk.Button(self,
                                    text="Browse",
                                    command=lambda:self.browseFiles(label_selected_folder))

        label_nth_number=Label(self,text="Nth number")
        entry_nth_number=Entry(self,width=5,borderwidth=2)

        label_progress_select=Label(self,text="Standby",fg='orange')
        progress_select=ttk.Progressbar(self,orient='horizontal',length=100,mode='determinate')

        button_select_execute=ttk.Button(self,text='Select',
                                            command=self.selectFunction)




        label_cropped_folder.grid(sticky=W,column=0,row=1)
        button_cropped_explorer.grid(column=1,row=1)

        label_selected_folder.grid(sticky=W,column=0,row=2)
        button_selected_explorer.grid(column=1,row=2)

        label_nth_number.grid(column=0,row=3)
        entry_nth_number.grid(column=1,row=3)

        label_progress_select.grid(column=0,row=4)
        progress_select.grid(column=0,row=5)

        button_select_execute.grid(column=1,row=6)


    def browseFiles(self,label):
        directory=filedialog.askdirectory(initialdir='/',title="Select a directory")
        if label==label_cropped_folder:
            label.configure(text="Cropped Folder: "+ directory, fg='blue')
            self.croppedPath=directory
            #print("Raw: " + self.path)
        else:
            label.configure(text="Destination Folder: "+ directory, fg='blue')
            self.selectedPath=directory
            #print("Cropped: " + self.outPath)
        label_progress_select.configure(text="Standby",fg='orange')


    def selectFunction(self):
        #try block for cropped image path

        try:
            print(self.croppedPath)
            if (self.croppedPath==""):
                raise Exception("Empty Cropped Directory")

        except AttributeError:
            print("Empty Cropped Directory")
            messagebox.showerror("Select A Directory","Empty Cropped Directory")
            return
        except Exception:
            print("Empty Cropped Directory")
            messagebox.showerror("Select A Directory","Empty Cropped Directory")
            return


        #try block for selected image path
        try:
            print(self.selectedPath)
            if (self.selectedPath==""):
                raise Exception("Empty Cropped Directory")

        except AttributeError:
            print("Empty Selected Directory")
            messagebox.showerror("Select A Directory","Empty Selected Directory")
            return
        except Exception:
            print("Empty Selected Directory")
            messagebox.showerror("Select A Directory","Empty Selected Directory")
            return

        #try block for nth number
        try:
            if(int(entry_nth_number.get())<=1 or int(entry_nth_number.get())>=len(os.listdir(self.croppedPath)) ):
                raise NthValueOutOfRange("Nth Value Out of Range")

        except NthValueOutOfRange:
            messagebox.showerror("Nth Value Input","Nth Value out of range.\nMust be between 2 and length of cropped folder")
            return
        except ValueError:
            messagebox.showerror("Nth Value Input","Fill in Nth Value with a number")
            return

        label_progress_select.configure(text="PROCESSING",fg='red')


        #print(self.croppedPath)
        nthNum=int(entry_nth_number.get())
        list=os.listdir(self.croppedPath)

        progress_select['value']=0
        progress_select['maximum']=len(list)//nthNum

        for i in list[::nthNum]:
            shutil.copy(self.croppedPath+'/'+i,self.selectedPath)
            progress_select['value']+=1
            progress_select.update()

        label_progress_select.configure(text="DONE",fg='green')
