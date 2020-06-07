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
import _pickle as pickle


class FolderButton(tk.Button):
    def __init__(self, master, text, path):
        self.master = master
        self.path = path
        self.textvar = tk.StringVar()
        self.textvar.set(text)
        super(FolderButton, self).__init__(master, textvariable=self.textvar, command=self.callback)

    def settext(self, str):
        self.textvar.set(str)

    def gettext(self):
        return self.textvar.get()

    def setpath(self, str):
        self.path = str

    def getpath(self):
        return self.path

    def callback(self):
        app.folderButton_click(self)

    def save(self):
        text = self.gettext()
        return text, self.path

    def change(self, text=None, path=None):
        if text:
            self.settext(text)
        if path:
            self.setpath(path)

    def delete(self):
        self.destroy()




def resize_to_screen(img, masterw, masterh):
    # this function resizes the image to fit the master window
    w = img.width
    h = img.height
    neww = 0
    newh = 0
    ratio = w/h
    if w <= masterw or h <= masterh:
        return img
    elif w>h :
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
        if not os.path.isdir(self.home_path):  # make sure home_path exists, else make it
            os.makedirs(self.home_path)
        self.platform = ""  # stores whether user is using linux or windows
        self.photo_counter = 0  # this is mainly just the index for walking through the photos array
        self.extensions = ['.jpg', '.jpeg', '.img', '.png']
        self.photos = [] # array of tuples (photo, photo_path)
        self.folderButton_list = []  # list of folders the user can choose between to export the photo to


        # instantiate widgets
        self.container = tk.Canvas(self)
        self.buttonFrame = tk.Frame(master, width=self.w, height=self.buttonHeightOffset)
        self.container.pack()
        self.buttonFrame.pack(side=tk.BOTTOM)
        self.pack()

        self.add_button = None

        self.import_from_folder = "" # this is where the path to the folder is stored that the user wants to sort the photos from
        self.startButton = tk.Button(self.container, height=int(self.h/2), width=int(self.w/2), takefocus=True, text="Click here to begin",
                                     command=self.get_import_folder)  # one time use (may change out button for a clickable background or something)
        self.startButton.pack()




    def get_import_folder(self):
        # opens a dialog for the user to select import_from_folder.
        if not self.import_from_folder:
            self.import_from_folder = filedialog.askdirectory(initialdir=self.base_path + "/Pictures")
        if self.import_from_folder:
            self.startButton.destroy()
        else:
            return

        # final step in initiation process
        self.get_photos()
        self.create_image()
        self.addButton()

    def addButton(self):
        # adds the add button
        self.add_button = tk.Button(self.buttonFrame, text="add folder", anchor=tk.SE, command=self.add_folder_button) \
            .pack(side=tk.LEFT)

    def create_image(self):
        # first, clears container (a.k.a canvas)
        # than, sets preps canvas for image load and loads image into canvas
        self.container.delete(tk.ALL)
        if self.container.winfo_width() != self.w:
            self.container.configure(height=self.h-self.buttonHeightOffset, width=self.w)
        print(self.photos)
        self.container.create_image(self.w/2, self.h/2, image=self.photos[self.photo_counter][0])
        print(self.container.winfo_height())

    def get_base_path(self):
        # fetches the user's home folder and stores the user's OS type
        # also, creates homefolder for this application (if it doesn't already exist)
        base_path = ""
        user = getpass.getuser()
        if platform.startswith("linux") or platform.startswith("linux2"):
            self.platform = "linux"
            base_path = "/home/" + user
        elif platform.startswith("win32"):
            self.platform = "win32"
            base_path = "/Users/" + user
            print(base_path)
        else:

            raise Exception("cannot find operating system")
        return base_path

    def folderButton_click(self, button):
        # this is basically the callback for any folderButton clicked.
        # increments photo_counter, moves image to folderButton's path and loads new image into container
        old_path = self.photos[self.photo_counter][1]
        new_path = button.path + "/" + os.path.basename(old_path)
        print(new_path)
        os.rename(old_path, new_path)

        self.photo_counter += 1
        try:
            self.create_image()
        except IndexError:
            tk.messagebox.showinfo("finished", "the selected folder has no more images to sort")


        return

    def buttonFrame_update(self):
        self.buttonFrame.pack()

    def add_folder_button(self):
        text = ""
        folder = ""

        answer = tk.messagebox.askquestion("Do you want to create a new folder?",
                                           "Select 'yes' if you want to create a new folder \n Select 'no' if you want to use an existing folder")
        folder = ""
        text = ""
        if answer == "yes":
            # create new folder
            text = tk.simpledialog.askstring("Folder name", "How do you want to name your folder?")
            try:
                folder = self.home_path + "/" + text
                os.mkdir(folder)
            except FileExistsError:
                tk.messagebox.showwarning('', 'Folder already exists')
                self.add_folder_button()
                return
        elif answer == "no":
            # select existing folder
            folder = filedialog.askdirectory(initialdir=self.home_path)
            folder_tuple = folder.split('/')
            text = folder_tuple[len(folder_tuple) - 1]
            for button in self.folderButton_list:
                if button.gettext() == text:
                    tk.messagebox.showwarning('', 'Folder already exists')
                    return self.add_folder_button()
        else:
            # this is where the user cancels the dialog
            return

        if not text or not folder:
            return

        button = FolderButton(self.buttonFrame, text, folder)  # this is THE button

        self.folderButton_list.append(button)
        button.pack(side=tk.LEFT)
        self.buttonFrame.pack()
        return


    def get_photos(self):
        #get all the photos with extensions in extensions[] from the given folder
        for r, d, f in os.walk(self.import_from_folder):
            print("dirpath: {} \n"
                  "dirname: {} \n \n".format(r,d))
            for file in f:
                for ext in self.extensions:
                    if ext in file:
                        img = self.create_tk_image_from_path(os.path.join(r, file))
            break


    def create_tk_image_from_path(self, file_path):
        # make the image from file_path TK-ready (tk doesn't read jpg) and load these images into photos[]
        if file_path in [tup1[1] for tup1 in self.photos]:
            print("File_path already exists: {}".format(file_path))
       # print("w:{} + h:{} + offset:{} + path:{}".format(self.w, self.h, self.buttonHeightOffset, file_path))
        image = PIL.Image.open(file_path)
       # print("old: {} + {}".format(image.width, image.height))
        image = resize_to_screen(image, self.w, self.h-self.buttonHeightOffset) #this function resizes the image to fit the window
       # print("new: {} + {}".format(image.width, image.height))
        photoimage = PIL.ImageTk.PhotoImage(image)
        self.photos.append((photoimage, file_path))

        return image

    def save(self):
        # saves the state of the app to 'config.dict' as stated in menubar.save
        print("saving....")
        photos = []
        folderButton_list = []
        for photo in self.photos:
            photos.append(photo[1])
        for button in self.folderButton_list:
            button_tuple = button.save()
            folderButton_list.append(button_tuple)

        dump = {"photos": photos,
                #"photo_counter": self.photo_counter,
                "folderButton_list": folderButton_list,
                "platform": self.platform,
                "base_path": self.base_path,
                "home_path": self.home_path,
                "importFolder": self.import_from_folder,
                "buttonHeightOffset": self.buttonHeightOffset,
                "w": self.w,
                "h": self.h
                }
        print("saved")
        return dump

    def load(self, dump):
        # loads the state of the app from 'config.dict' as stated in menubar.load
        print("loading....")
        #self.photo_counter = dump.get("photo_counter") #maybe not use this now that images don't load when they've been moved
        self.platform = dump.get("platform")
        self.base_path = dump.get("base_path")
        self.home_path = dump.get("home_path")
        self.import_from_folder = dump.get("importFolder")
        self.buttonHeightOffset = dump.get("buttonHeightOffset")
        self.w = dump.get("w")
        self.h = dump.get("h")
        for path in dump.get("photos"):
            try:
                self.create_tk_image_from_path(path)
            except FileNotFoundError:
                print("File not found: [{}]\n".format(path))
        if not self.add_button:
            self.addButton()
        for tup in dump.get("folderButton_list"):
            button = FolderButton(self.buttonFrame, tup[0], tup[1])
            for folderbutton in self.folderButton_list:
                if folderbutton.gettext() == button.gettext() and folderbutton.path == button.getpath():
                    button.destroy()
                    tk.messagebox.showwarning('', 'Folder already exists')
                    return

            if os.path.exists(button.path):
                self.folderButton_list.append(button)
                print(self.folderButton_list)
                button.pack(side=tk.LEFT)
            else:
                button.destroy()
                tk.messagebox.showwarning('', 'Folder \'{}\' doesn\'t exist'.format(button.gettext()))
        self.buttonFrame.pack()

        # continuation of initialization process
        if self.startButton.winfo_exists() > 0:
            self.startButton.destroy()
        self.create_image()

        print("loaded")

    def selected_folder_button(self):
        pass


class MenuBar(tk.Menu):

    def __init__(self, master, app):
        super(MenuBar, self).__init__(master=master)
        self.app = app
        self.add_menu()
        self.intvar = tk.IntVar()
        self.intvar.set(len(app.folderButton_list))
        self.buttonchangemenu = None
        self.trace_id = 0
        pass

    def add_menu(self):
        filemenu = tk.Menu(self, tearoff=0)
        filemenu.add_command(label="Exit", command=self.exit)
        filemenu.add_command(label="Save", command=self.save)
        filemenu.add_command(label="Load", command=self.load)
        self.add_cascade(label="File", menu=filemenu)

        buttonmenu = tk.Menu(self, tearoff=0)
        buttonmenu.add_command(label="add button", command=app.add_folder_button)
        buttonmenu.add_command(label="delete button", command=self.delete_button)
        buttonmenu.add_command(label="rename button", command=self.rename_button)
        self.add_cascade(label="Buttons", menu=buttonmenu)

        #TODO: resize window and resize images, option: pass

    def delete_button(self):
        self.buttonchange(self.delete_button_helper)

    def delete_button_helper(self, *args):
        app.folderButton_list[self.intvar.get()].delete()
        app.buttonFrame_update()
        self.buttonchangemenu.destroy()


    def buttonchange(self, func):
        if self.trace_id:
            self.intvar.trace_vdelete('w', self.trace_id)
        self.buttonchangemenu = tk.Toplevel(root)
        for idx, button in enumerate(app.folderButton_list):
            print("{} idx = {}".format(idx, button.gettext()))
            tk.Radiobutton(master=self.buttonchangemenu, text=button.gettext(),
                           variable=self.intvar, value=idx, indicatoron=0).pack()
            print(idx)
            self.intvar.set(idx+1)
        tk.Button(master=self.buttonchangemenu, text="Done", bg='red', bd=10,
                  command=self.buttonchangemenu.destroy) \
            .pack(side=tk.TOP)

        self.trace_id = self.intvar.trace('w', func)

    def rename_button(self):
        self.buttonchange(self.change_selected_button)


    def change_selected_button(self, *args):
        button = app.folderButton_list[self.intvar.get()]
        text = tk.simpledialog.askstring("Folder name", "How do you want to rename your folder?")
        if not text:
            return
        else:
            #TODO: changes direcotry name, but not the shown name of the button in the tk window
            folder = app.home_path + "/" + text
            os.rename(button.path, folder)
            button.change(text=text, path=folder)
            button.pack()
            app.buttonFrame_update()
            self.buttonchangemenu.destroy()






    def exit(self):
        ans = messagebox.askyesno("Quit", "Do you want to save before quitting?")
        if ans:
            self.save()
        root.destroy()

    def save(self):
        dump = app.save()
        try:
            with open('config.dict', 'wb') as config_dict:
                pickle.dump(dump, config_dict)
        except FileNotFoundError:
            print("filenotfound-----------------------------------")
        except TypeError:
            print("typeError-------------------------")
            print(dump)
        if not config_dict.closed:
            config_dict.close()

    def load(self):
        with open('config.dict', 'rb') as config_dict:
            dump = pickle.load(config_dict)
            app.load(dump)
        config_dict.close()

def on_closing():
    menubar.exit()

root = tk.Tk()
root.title("Photo Sorter")
app = GUI(master=root)
menubar = MenuBar(root, app)
root.config(menu=menubar)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
root.destroy()









