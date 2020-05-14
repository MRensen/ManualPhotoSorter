#!/usr/bin/env/ python3
# coding=utf-8

import os
from sys import platform
import time
import tkinter as tk
from tkinter import filedialog
import PIL.Image, PIL.ImageTk
from tkinter import messagebox
from tkinter import simpledialog
import getpass

class FolderButton():
    def __init__(self, master, text, event):
        self.master = master
        self.text = text
        self.event = event
        self.Button = tk.Button(master, text=text, anchor=tk.SE, command=event)

    def pack(self):
        self.Button.pack()


def resize_to_screen(img, masterw, masterh):
    # this function resizes the image to fit the master window
    w = img.width
    h = img.height
    neww = 0
    newh = 0
    ratio = w/h
    if w>h :
        neww = masterw
        newh = round(neww/ratio)
        return img.resize((neww, newh))
    else:
        newh = masterh
        neww = round(newh * ratio)
        return img.resize((neww, newh))





class GUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.w,self.h = 650, 650
        self.buttonHeightOffset = 30
        master.minsize(width=self.w, height=self.h)
        master.maxsize(width=self.w, height=self.h)

        self.base_path = self.get_base_path()
        self.platform = ""
        self.photo_counter = 0
        self.extensions = ['.jpg', '.jpeg', '.img', '.png']
        self.photos = []
        self.folderButton_list = []  # list of folders the user can choose between to export the photo to

        self.container = tk.Canvas(self, width=self.w, height=self.h-self.buttonHeightOffset)
        self.buttonFrame = tk.Frame(master)

        #packs
        self.container.pack()
        self.pack()
        self.buttonFrame.pack()

        self.add_button = tk.Button(self.buttonFrame, text="add folder", anchor=tk.SE, command=self.add_folder_button)
        self.add_button.pack()

        self.import_from_folder = filedialog.askdirectory()

        self.get_photos()
        self.create_image()

    def create_image(self):
        #TODO: make it so that images get created and deleted here
        self.container.create_image(self.w/2, self.h/2, image=self.photos[self.photo_counter])

    def get_base_path(self):
        base_path = ""
        if platform.startswith("linux") or platform.startswith("linux2"):
            self.platform = "linux"
            base_path = "/home/" + getpass.getuser() + "/Pictures/PhotoSorter"
        elif platform.startswith("win32"):
            self.platform = "win32"
            #TODO: can't find where base_path is stored in explorer, find it.
            base_path = "/c/Users/" + getpass.getuser() + "/Pictures/PhotoSorter"
        else:
            #TODO check is this doesn't cause issues
            raise Exception("cannot find operating system")
        if not os.path.isdir(base_path):  # make sure basepath exists, else make it
            os.makedirs(base_path)
        return base_path

    def folderButton_click(self):
        return

    def add_folder_button(self):
        # user wants to add a new folder to export to. Check if folder already exists on drive, else make new folder.
        answer = tk.messagebox.askquestion("new folder", "Do you want to create a new folder? \n Select 'no' if you want to use an existing folder")
        folder = ""
        text = ""
        if answer == "yes":
            #TODO:create new folder
            text = folder = tk.simpledialog.askstring("Folder name", "What would you like your new folder called?")
            try:
                os.mkdir(self.base_path + "/" + folder)
            except FileExistsError:
                tk.messagebox.showwarning('', 'Folder already exists')
                self.add_folder_button()
                return

        if answer == "no":
            #select folder
            folder = filedialog.askdirectory(initialdir=self.base_path)
            folder_tuple = folder.split()
            text = folder_tuple[1]

        self.photo_counter += 1
        self.create_image()

        #text = tk.simpledialog.askstring(title="name", prompt="what is the name of this folder?")
        button = FolderButton(self.buttonFrame, text, self.folderButton_click)
        if button in self.folderButton_list:
            tk.messagebox.showwarning('', 'Folder already exists')
            self.add_folder_button()
            return
        else:
            self.folderButton_list.append(button)
        print(self.folderButton_list)
        button.pack()
        self.buttonFrame.pack()




        print(folder)
        return


    def get_photos(self):
        #get all the photos with extensions in extensions[] from the given folder
        for r, d, f in os.walk(self.import_from_folder):
            for file in f:
                for ext in self.extensions:
                    if ext in file:
                        img = self.create_tk_image_from_path(os.path.join(r, file))


    def create_tk_image_from_path(self, file_path):
        # make the image from file_path TK-ready (tk doesn't read jpg) and load these images into photos[]
        image = PIL.Image.open(file_path)
        print("old: {} + {}".format(image.width, image.height))
        image = resize_to_screen(image, self.w, self.h-self.buttonHeightOffset) #this function resizes the image to fit the master window
        print("new: {} + {}".format(image.width, image.height))
        photoimage = PIL.ImageTk.PhotoImage(image)
        self.photos.append(photoimage)

        return image


root = tk.Tk()
root.title("Photo Sorter")
app = GUI(master=root)
app.mainloop()
root.destroy()






