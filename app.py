import tkinter as tk
from tkinter import *

from crop import CropPage
from select import SelectPage
from rename import RenamePage

class ProcessApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        tk.Tk.title(self,"Poladrone Image Processing Tool")
        tk.Tk.geometry(self,"700x350")

        #appIcon=PhotoImage(self,file='poladroneLogo.ico')
        #tk.Tk.iconbitmap(self,appIcon)


        #menu bar
        my_menu=Menu(self)
        tk.Tk.config(self,menu=my_menu)

        #1st tier menu bar
        tools_menu=Menu(my_menu)
        my_menu.add_cascade(label="Tools",menu=tools_menu)

        #2nd tier menu bar
        tools_menu.add_command(label="Crop",command=lambda:self.show_frame(CropPage))
        tools_menu.add_command(label="Select",command=lambda:self.show_frame(SelectPage))
        tools_menu.add_command(label="Rename",command=lambda:self.show_frame(RenamePage))

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
