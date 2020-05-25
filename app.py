import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *

from crop import CropPage
from select import SelectPage
from rename import RenamePage

class ProcessApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.title(self,"Poladrone Image Processing Tool")
        tk.Tk.geometry(self,"750x400")
        tk.Tk.minsize(self,750,400)
        #tk.Tk.resizable(self,width=False,height=False)

        #appIcon=PhotoImage(self,file='poladroneLogo.ico')
        tk.Tk.iconbitmap(self,default="images/poladroneLogo.ico")


        #menu bar
        font_menubar=('Helvetica',16,'bold')
        my_menu=Menu(self,font=font_menubar)
        tk.Tk.config(self,menu=my_menu)

        #my_menu.config(background='red')

        my_menu.add_command(label="Crop",command=lambda:self.show_frame(CropPage))
        my_menu.add_command(label="Select",command=lambda:self.show_frame(SelectPage))
        my_menu.add_command(label="Rename",command=lambda:self.show_frame(RenamePage))

        custom_menu=tk.Frame(self)
        #custom_menu.pack(side="top",fill='both',expand=False)

        button_to_crop=Button(custom_menu,text='Crop',command=lambda:self.show_frame(CropPage))
        button_to_select=Button(custom_menu,text='Select',command=lambda:self.show_frame(SelectPage))
        button_to_rename=Button(custom_menu,text='Rename',command=lambda:self.show_frame(RenamePage),anchor='nw')

        #button_to_crop.pack(side='left',padx=10)
        #button_to_select.pack(side='left',padx=10)
        #button_to_rename.pack(side='left',padx=10)

        button_to_crop.grid(sticky=W)
        button_to_select.grid(sticky=N)
        button_to_rename.grid(sticky=E)

        container=tk.Frame(self)
        container.pack(side="top",fill='both',expand=True)

        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames={}
        #for loop for including frames
        for F in (CropPage,SelectPage,RenamePage):
            frame=F(container,self)
            self.frames[F]=frame
            frame.grid(row=0,column=0,sticky="nsew")

        #which frame shows up first
        self.show_frame(CropPage)


    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()


if __name__ == "__main__":
    app=ProcessApp()
    app.mainloop()
