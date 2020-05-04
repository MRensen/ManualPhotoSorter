#!/usr/bin/env/ python3
# coding=utf-8

import os
from tkinter import *
from tkinter import filedialog
import cv2


def handle_img(img_path):

    return


def handle_path(file_path):
    img = cv2.imread(file_path)
    cv2.imshow('image', img)
    while cv2.waitKey(0) != 1:
        handle_img(file_path)
        cv2.destroyAllWindows()


root = Tk()
root.withdraw()
export_from_folder = '/home/mark/Pictures' #filedialog.askdirectory()

extensions = ['.jpg', '.jpeg', '.img', '.png']
files = []
for r, d, f in os.walk(export_from_folder):
    for file in f:
        for ext in extensions:
            if ext in file:
                handle_path(os.path.join(r, file))

for f in files:
    print(f)
print('...................................export_from_folder...................................................')





