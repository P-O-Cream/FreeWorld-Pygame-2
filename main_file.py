# Copyright [C] 2023 P.O Cream(浅),LinLinand all contributors
# All right Reserved

#     Distributed under GPL license
#     See copy at https://opensource.org/licenses/GPL-3.0
# FreeWorld Pygame 2.0 is the rebuild version of FreeWorld
# It is based on Pygame and Tkinter

import time                    
import atexit
import os
import sys
import random
import base64
import json
import re
import socket
import requests
import pygame
import tkinter as tk
from PIL import*

class ChooseInterface(object):
    def __init__(self):
        self.name = "ChooseInterface"
        self.windows = tk.Tk()
        self.windows.title("FreeWorld Pygame 2 游戏选项")
        self.windows.geometry("1000x746+0+0")
        self.ChooseInterface_photo = tk.PhotoImage(file="FreeWorld LOGO.png")
        self.ChooseInterface_image = tk.Label(self.windows, image=self.ChooseInterface_photo)
        self.ChooseInterface_image.grid(row=0,column=0)
        self.windows.iconphoto(True,tk.PhotoImage(file='FreeWorld icon.png'))
        
        self.begin_button = tk.Button(self.windows,text="开始冒险吧",height=2,width=13,font=("44"),command=self.begin_button_command)
        self.update_button = tk.Button(self.windows,text="游戏更新内容",height=2,width=13,font=("18"),command=self.update_button_command)
        self.begin_button.grid(row=0,column=0)
        self.update_button.grid(row=1,column=0)

    def begin_button_command(self):
        ...
    
    def update_button_command(self):
        ...
        
    def tk_run(self):self.windows.mainloop()
    
_ChooseInterface = ChooseInterface()
_ChooseInterface.tk_run()
