#!/usr/bin/env/ python3
# coding=utf-8

import os
import time
import tkinter as tk
from tkinter import filedialog
import cv2
import PIL.Image, PIL.ImageTk
from tkinter import messagebox


class GUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        w,h = 650, 650
        master.minsize(width=w, height=h)
        master.maxsize(width=w, height=h)
        #TODO: move all buttons into this frame
        buttonFrame = tk.Frame(master, width=w, height=50, borderwidth=5)
        self.pack()

        self.add_button = tk.Button(self, text="add folder", anchor=tk.SE, command=self.add_folder_button)
        self.add_button.pack()

        self.import_from_folder = '/home/mark/Pictures' #filedialog.askdirectory()
        self.extensions = ['.jpg', '.jpeg', '.img', '.png']
        self.photos = []
        self.export_folders_list = [] #list of folders the user can choose between to export the photo to
        self.get_photos()


    def add_folder_button(self):
        # user wants to add a new folder to export to. Check if folder allready exists on drive, else make new folder.
        answer = tk.messagebox.askquestion("new folder", "Do you want to create a new folder? Select 'no' if you want to use an existing folder")
        if answer == "yes":
            dir = filedialog.askdirectory()
        if answer == "no":
            dir = "no"
        print(dir)
        return


    def handle_path(self, file_path):
        #TODO: remove this method

        #img_height, img_width, img_channels = img.shape
        container = tk.Label(root, image=image)
        container.pack()
        print("should not get here")

        # cv2.imshow('image', img)
        # cv2.startWindowThread()
        # #cannot get around using Waitkey, but it's effect is cancelled like this.
        # waitkey = cv2.waitKey(1000)
        # print(waitkey)


        self.handle_img(file_path)
        #cv2.destroyAllWindows()




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
root.title = "Photo Sorter"
app = GUI(master=root)
app.mainloop()
root.destroy()






