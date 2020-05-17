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


class FolderButton(tk.Button):
    def __init__(self, master, text, event):
        super(FolderButton, self).__init__(master, text=text, command=event)
        self.master = master
        self.text = text
        self.event = event
        self.Button = tk.Button(master, text=text, anchor=tk.SE, command=event)




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
        self.w, self.h = 700, 700
        self.buttonHeightOffset = 30
        master.minsize(width=self.w, height=self.h)
        master.maxsize(width=self.w, height=self.h)

        self.base_path = self.get_base_path()
        self.home_path = self.base_path + "/Pictures/PhotoSorter"
        self.platform = ""
        self.photo_counter = 0
        self.extensions = ['.jpg', '.jpeg', '.img', '.png']
        self.photos = []
        self.folderButton_list = []  # list of folders the user can choose between to export the photo to

        self.container = tk.Canvas(self, bg="black")
        self.buttonFrame = tk.Frame(master, width=self.w, height=self.buttonHeightOffset)
        self.container.pack()
        self.buttonFrame.pack(side=tk.BOTTOM)
        self.pack()

        self.add_button = None

        self.import_from_folder = ""
        self.importWait = True
        self.startButton = tk.Button(self.container, takefocus=True, text="Click here to select folder",
                                     command=self.get_import_folder)
        self.startButton.pack()


    def get_import_folder(self):
        self.import_from_folder = filedialog.askdirectory(initialdir=self.base_path + "/Pictures")
        self.startButton.destroy()
        self.get_photos()
        self.create_image()
        self.add_button = tk.Button(self.buttonFrame, text="add folder", anchor=tk.SE, command=self.add_folder_button) \
            .pack(side=tk.LEFT)

    def create_image(self):
        #TODO: make it so that images get created and deleted here
        self.container.delete(tk.ALL)
        if self.container.winfo_width() != self.w:
            self.container.configure(height=self.h-self.buttonHeightOffset, width=self.w)
        self.container.create_image(self.w/2, self.h/2, image=self.photos[self.photo_counter])
        print(self.container.winfo_height())

    def get_base_path(self):
        base_path = ""
        user = getpass.getuser()
        if platform.startswith("linux") or platform.startswith("linux2"):
            self.platform = "linux"
            base_path = "/home/" + user
        elif platform.startswith("win32"):
            self.platform = "win32"
            #TODO: can't find where base_path is stored in windows explorer, find it.
            base_path = "/c/Users/" + user
        else:

            raise Exception("cannot find operating system")
        if not os.path.isdir(base_path):  # make sure basepath exists, else make it
            os.makedirs(base_path)
        return base_path

    def folderButton_click(self, folder_path):
        self.photo_counter += 1

        #TODO: make sure image gets moved to location here

        self.create_image()

        return

    def add_folder_button(self):
        # user wants to add a new folder to export to. Check if folder already exists on drive, else make new folder.
        answer = tk.messagebox.askquestion("new folder", "Do you want to create a new folder? \n Select 'no' if you want to use an existing folder")
        folder = ""
        text = ""
        if answer == "yes":
            text = folder = tk.simpledialog.askstring("Folder name", "What would you like your new folder called?")
            try:
                os.mkdir(self.home_path + "/" + folder)
            except FileExistsError:
                tk.messagebox.showwarning('', 'Folder already exists')
                self.add_folder_button()
                return
        elif answer == "no":
            #select folder
            folder = filedialog.askdirectory(initialdir=self.home_path)
            folder_tuple = folder.split('/')
            text = folder_tuple[len(folder_tuple)-1]
        else:
            return

        #text = tk.simpledialog.askstring(title="name", prompt="what is the name of this folder?")
        button = FolderButton(self.buttonFrame, text, lambda: self.folderButton_click(folder))
        if button in self.folderButton_list:
            button.destroy()
            tk.messagebox.showwarning('', 'Folder already exists')
            self.add_folder_button()
            return
        else:
            self.folderButton_list.append(button)
        print(self.folderButton_list)
        button.pack(side=tk.LEFT)
        self.buttonFrame.pack()
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






