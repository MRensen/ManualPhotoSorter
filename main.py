#!/usr/bin/env/ python3
# coding=utf-8

import os
import time
import tkinter as tk
from tkinter import filedialog
import cv2
import PIL.Image, PIL.ImageTk
from tkinter import messagebox
from tkinter import simpledialog

class FolderButton():
    def __init__(self, master, text, event):
        self.master = master
        self.text = text
        self.event = event
        self.Button = tk.Button(master, text=text, anchor=tk.SE, command=event)



class GUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        w,h = 650, 650
        master.minsize(width=w, height=h)
        master.maxsize(width=w, height=h)

        self.photo_counter = 0
        self.extensions = ['.jpg', '.jpeg', '.img', '.png']
        self.photos = []
        self.folderButton_list = []  # list of folders the user can choose between to export the photo to

        self.container = tk.Canvas(self, width=650, height=620)
        self.buttonFrame = tk.Frame(master)

        #packs
        self.container.pack()
        self.pack()
        self.buttonFrame.pack()

        self.add_button = tk.Button(self.buttonFrame, text="add folder", anchor=tk.SE, command=self.add_folder_button)
        self.add_button.pack()

        self.import_from_folder = '/home/mark/Pictures' #filedialog.askdirectory()

        self.get_photos()

        self.container.create_image(20, 20, anchor=tk.CENTER, image=self.photos[self.photo_counter])

    def folderButton_click(self):
        return

    def add_folder_button(self):
        # user wants to add a new folder to export to. Check if folder allready exists on drive, else make new folder.
        answer = tk.messagebox.askquestion("new folder", "Do you want to create a new folder? Select 'no' if you want to use an existing folder")
        folder = ""
        if answer == "yes":
            #TODO:create new folder
            folder = True
        if answer == "no":
            #select folder
            folder = filedialog.askdirectory()
        text = tk.simpledialog.askstring(title="name", prompt="what is the name of this folder?")
        button = FolderButton(self.buttonFrame, text, self.folderButton_click)
        if folder in self.folderButton_list:
            tk.messagebox.showwarning('', 'Folder already exists')
            self.add_folder_button()
            return
        else:
            self.folderButton_list.append(button)




        print(folder)
        return


    def get_photos(self):
        #get all the photos with extensions in extensions[] from the given folder
        for r, d, f in os.walk(self.import_from_folder):
            for file in f:
                for ext in self.extensions:
                    if ext in file:
                        img = self.create_tk_image_from_path(os.path.join(r, file))
                        self.photos.append(img)

    def create_tk_image_from_path(self, file_path):
        # make the image from file_path TK-ready (tk doesn't read jpg) and load these images into photos[]
        img = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2RGB)
        image = PIL.ImageTk.PhotoImage(PIL.Image.fromarray(img))
        return image


root = tk.Tk()
root.title("Photo Sorter")
app = GUI(master=root)
app.mainloop()
root.destroy()






