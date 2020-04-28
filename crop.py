import os
import cv2
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


class ValueOutOfRange(Exception):
    def __init__(self,msg):
        super().__init__(msg)

class CropPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="Crop Page")
        label.grid(sticky='n')

        global label_raw_folder
        global label_cropped_folder
        global label_progress_bar
        global progress_bar
        global entry_crop_length
        global entry_crop_width

        global dimensionLock


        path=""
        outPath=""
        dimensionLock=BooleanVar()


        label_raw_folder=Label(self,
                                text="Browse Raw Image Location ",
                                width=75, height=4)
        button_raw_explorer=ttk.Button(self,
                                    text="Browse",
                                    command=lambda:self.browseFiles(label_raw_folder))


        label_cropped_folder=Label(self,
                                text="Browse Croppped Image Location ",
                                width=75, height=4)
        button_cropped_explorer=ttk.Button(self,
                                    text="Browse",
                                    command=lambda:self.browseFiles(label_cropped_folder))

        check_dimension_lock=Checkbutton(self,text="Square Crop",variable=dimensionLock)

        label_cropped_length=Label(self,text="Cropped Length")
        entry_crop_length=Entry(self,width=5,borderwidth=2)

        label_cropped_width=Label(self,text="Cropped Width")
        entry_crop_width=Entry(self,width=5,borderwidth=2)


        label_progress_bar=Label(self,
                                text="Standby",
                                fg="orange")
        progress_bar=ttk.Progressbar(self,orient='horizontal',length=100,mode='determinate')



        button_crop_execute=ttk.Button(self,
                                    text="EXECUTE",
                                    command=self.cropFunction)


        label_raw_folder.grid(sticky=W,column=0,row=1)
        button_raw_explorer.grid(column=1,row=1)

        label_cropped_folder.grid(sticky=W,column=0,row=2)
        button_cropped_explorer.grid(column=1,row=2)

        check_dimension_lock.grid(sticky="nsew",column=0,row=3)
        check_dimension_lock.deselect()

        label_cropped_length.grid(column=0,row=4)
        entry_crop_length.grid(column=1,row=4,sticky=W)

        label_cropped_width.grid(column=0,row=5)
        entry_crop_width.grid(column=1,row=5,sticky=W)

        label_progress_bar.grid(column=0,row=6)
        progress_bar.grid(column=0,row=7)

        button_crop_execute.grid(column=1,row=10)


    def browseFiles(self,label):
        directory=filedialog.askdirectory(initialdir='/',title="Select a directory")
        if label==label_raw_folder:
            label.configure(text="RAW Folder: "+ directory, fg='blue')
            self.path=directory

        else:
            label.configure(text="Cropped Folder: "+ directory, fg='blue')
            self.outPath=directory


        label_progress_bar.configure(text="Standby",fg='orange')

        if (directory==""):
            label.configure(text="No Folder Selected "+ directory, fg='red')
            raise Exception("Empty directory")


    def cropFunction(self):
        #try block for RAW path
        try:
            print(self.path)
            if (self.path==""):
                raise Exception("Empty Raw Directory")

        except AttributeError:
            print("Empty RAW Directory")
            messagebox.showerror("Select A Directory","Empty RAW Directory")
            return;

        except Exception:
            print("Empty RAW Directory")
            messagebox.showerror("Select A Directory","Empty RAW Directory")
            return;

        #try block for cropped path
        try:
            print(self.outPath)
            if (self.outPath==""):
                raise Exception("Empty Cropped Directory")
        except AttributeError:
            print("Empty Cropped directory")
            messagebox.showerror("Select A Directory","Empty Cropped Directory")
            return;

        except Exception:
            print("Empty RAW Directory")
            messagebox.showerror("Select A Directory","Empty RAW Directory")
            return;
        #try block for crop dimension inputs

        try:
            if(int(entry_crop_length.get())>5000 or int(entry_crop_length.get())<0):
                raise ValueOutOfRange("Value is out of range")
            if(int(entry_crop_width.get())>3000 or int(entry_crop_width.get())<0):
                raise ValueOutOfRange("Value is out of range")

        except ValueOutOfRange:
            messagebox.showerror("Dimension Input","Values out of range")
            return;
        except ValueError:
            messagebox.showerror("Dimension Input","Dimesions must be integers")
            return;
            #cropLength=500
            #cropWidth=500

        #default crop dimensions
        cropLength=500
        cropWidth=500

        #tset progress label to processing
        label_progress_bar.configure(text="PROCESSING ",
                                        fg='red')

        #checking for empty values
        if(dimensionLock.get()):
            if(entry_crop_length.get()==""):
                print("Using default values for square crop")

            else:
                print("square crop")
                cropLength=int(entry_crop_length.get())//2
                cropWidth=int(entry_crop_length.get())//2

        else:
            if(entry_crop_width.get()=="" or entry_crop_length.get()=="" ):
                print("Using default vals for rectangle crop")
            else:
                print("rectangle crop")
                cropLength=int(entry_crop_length.get())//2
                cropWidth=int(entry_crop_width.get())//2


        #initializing progress bar
        progress_bar['value']=0
        progress_bar['maximum']=len(os.listdir(self.path))

        # iterate through the names of contents of the folder
        for image_path in os.listdir(self.path):


            # create the full input path and read the file
            input_path = os.path.join(self.path, image_path)

            # for loading color image
            img_to_crop = cv2.imread(input_path)
            height, width, channels = img_to_crop.shape

            '''
            # for loading grayscale image
            img_to_crop = cv2.imread(input_path, 0)
            height, width = img_to_crop.shape
            '''
            # new position for square image cropping to size
            upper_left = (int((width / 2) - cropWidth), int((height / 2) - cropLength))
            bottom_right = (int((width / 2) + cropWidth), int((height / 2) + cropLength))

            '''
            # new position for square image cropping
            upper_left = (int((width - height) / 2), 0)
            bottom_right = (int((width + height) / 2), height)
            '''

            # crop the image
            img_crop = img_to_crop[upper_left[1]:bottom_right[1], upper_left[0]:bottom_right[0]]

            # create full output path & save the file to disk
            fullpath = os.path.join(self.outPath, 'crop_'+image_path)
            cv2.imwrite(fullpath, img_crop)

            #update progress_bar
            progress_bar['value']+=1
            progress_bar.update()


        label_progress_bar.configure(text="DONE! ",fg='green')
