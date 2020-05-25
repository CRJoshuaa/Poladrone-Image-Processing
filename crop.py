import os
import cv2
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

#exception class for out of range values
class ValueOutOfRange(Exception):
    def __init__(self,msg):
        super().__init__(msg)

class CropPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        #tk.Frame.config(self,bg='blue')


        global label_raw_folder
        global label_cropped_folder
        global label_progress_bar
        global progress_bar
        global entry_crop_length
        global label_cropped_width
        global entry_crop_width

        global dimensionLock

        font_page_title=('Helvetica',16,'bold')
        font_label=("Verdana",10)

        #style_button=ttk.Style()
        #style_button.configure('TButton',background='#FD3A41',foreground='white')

        path=""
        outPath=""
        dimensionLock=BooleanVar()

        label_crop_page=Label(self,
                                text="Crop Page",
                                font=font_page_title,
                                justify=CENTER,
                                anchor=N)

        label_raw_folder=Label(self,
                                text="Raw Image Directory ",
                                width=55, height=4,
                                font=font_label,
                                wraplength=500,
                                justify='left',
                                anchor=W,
                                fg='grey')

        button_raw_explorer=ttk.Button(self,
                                        text="Browse",
                                        command=lambda:self.browseFiles(label_raw_folder))


        label_cropped_folder=Label(self,
                                    text="Cropped Image Directory ",
                                    width=55, height=4,
                                    font=font_label,
                                    wraplength=500,
                                    justify=LEFT,
                                    anchor=W,
                                    fg='grey')

        button_cropped_explorer=ttk.Button(self,
                                            text="Browse",
                                            #background="blue",
                                            command=lambda:self.browseFiles(label_cropped_folder))

        check_dimension_lock=Checkbutton(self,
                                            text="Square Crop",
                                            font=font_label,
                                            variable=dimensionLock,
                                            command=self.checkLabel)

        label_cropped_length=Label(self,
                                    text="Crop Length: ",
                                    font=font_label,
                                    justify=LEFT,
                                    anchor=W)
        entry_crop_length=ttk.Entry(self,width=5)

        label_cropped_width=Label(self,
                                    text="Crop Width: ",
                                    font=font_label,
                                    justify=LEFT,
                                    anchor=W)
        entry_crop_width=ttk.Entry(self,width=5)


        label_progress_bar=Label(self,
                                text="Standby",
                                fg="orange")
        progress_bar=ttk.Progressbar(self,orient='horizontal',length=100,mode='determinate')



        button_crop_execute=ttk.Button(self,
                                    text="Crop",
                                    command=self.cropFunction)

        label_crop_page.grid(sticky='n')

        label_raw_folder.grid(sticky=W,column=1,row=1,columnspan=10)
        button_raw_explorer.grid(column=12,row=1)

        label_cropped_folder.grid(sticky=W,column=1,row=2,columnspan=10)
        button_cropped_explorer.grid(column=12,row=2)

        check_dimension_lock.grid(sticky=W,column=2,row=3,columnspan=5)
        check_dimension_lock.deselect()

        label_cropped_length.grid(sticky=W,column=2,row=4)
        entry_crop_length.grid(column=3,row=4,sticky=W)

        label_cropped_width.grid(column=2,row=5,sticky=W)
        entry_crop_width.grid(column=3,row=5,sticky=W)

        label_progress_bar.grid(column=2,row=6)
        progress_bar.grid(column=2,row=7)

        button_crop_execute.grid(column=10,row=10)

    #check if square crop is selecetd
    def checkLabel(self):
        if(dimensionLock.get()):
            label_cropped_width.config(state='disable')
            entry_crop_width.config(state='disable')
        else:
            label_cropped_width.config(state='active')
            entry_crop_width.config(state='normal')

    #file browser
    def browseFiles(self,label):
        directory=filedialog.askdirectory(initialdir='/',title="Select a directory")
        if label==label_raw_folder:
            #try block for RAW folder with no jpeg
            try:
                if not any(fname.endswith('.JPG') for fname in os.listdir(directory)):
                    label.configure(text="No Folder Selected "+ directory, fg='red')
                    raise Exception("Directory has no .JPG files")

            except Exception:
                messagebox.showerror("Select A Directory","JPG files(s) not found")
                return

            label.configure(text="RAW Folder: "+ directory, fg='blue')
            self.path=directory

        else:
            label.configure(text="Cropped Folder: "+ directory, fg='blue')
            self.outPath=directory


        label_progress_bar.configure(text="Standby",fg='orange')
        progress_bar['value']=0

        if (directory==""):
            label.configure(text="No Folder Selected ", fg='red')
            #raise Exception("Empty directory")

    #cropping function
    def cropFunction(self):
        #default crop dimensions
        cropLength=500
        cropWidth=500

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
            if (self.outPath==""):
                raise Exception("Empty Cropped Directory")
        except AttributeError:
            messagebox.showerror("Select A Directory","Empty Cropped Directory")
            return;

        except Exception:
            messagebox.showerror("Select A Directory","Empty Cropped Directory")
            return;

        #try block for crop dimension inputs
        try:
            if(dimensionLock.get()):
                if(entry_crop_length.get()==""):
                    defaultVal=messagebox.askquestion("Dimension Input","Use default crop values?\nLength: 500\nWidth: 500")
                    if defaultVal=="yes":
                        pass
                    else:
                        label_progress_bar.configure(text="Standby",fg='orange')
                        progress_bar['value']=0
                        return
                else:
                    if(int(entry_crop_length.get())>3000 or int(entry_crop_length.get())<0):
                        raise ValueOutOfRange("Value is out of range")
                    else:
                        print("square crop")
                        cropLength=int(entry_crop_length.get())//2
                        cropWidth=int(entry_crop_length.get())//2

            else:
                if(entry_crop_width.get()=="" or entry_crop_length.get()=="" ):
                    defaultVal=messagebox.askquestion("Dimension Input","Use default crop values?\nLength: 500\nWidth: 500")
                    if defaultVal=="yes":
                        pass
                    else:
                        label_progress_bar.configure(text="Standby",fg='orange')
                        progress_bar['value']=0
                        return

                else:
                    if(int(entry_crop_length.get())>5000 or int(entry_crop_length.get())<0):
                        raise ValueOutOfRange("Value is out of range")
                    elif(int(entry_crop_width.get())>3000 or int(entry_crop_width.get())<0):
                        raise ValueOutOfRange("Value is out of range")
                    else:
                        print("rectangle crop")
                        cropLength=int(entry_crop_length.get())//2
                        cropWidth=int(entry_crop_width.get())//2

        except ValueOutOfRange:
            messagebox.showerror("Dimension Input","Values out of range")
            return

        #set progress label to processing
        label_progress_bar.configure(text="PROCESSING ",
                                        fg='red')

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
