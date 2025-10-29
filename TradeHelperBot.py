from discord import Interaction
from discord._types import ClientT

#EVERYTHING IS UNDER APACHE 2.0

#================================Libraries checking part==================================================
not_installed_libs = []
installs = []
try:
    import tkinter
except Exception as e:
    not_installed_libs.append('tkinter')
    installs.append('"pip install tk" or "python3 -m pip install tk"')

try:
    import PIL
except Exception as e:
    not_installed_libs.append('pillow')
    installs.append('"pip install pillow" or "python3 -m pip install pillow"')

try:
    import discord
    from discord import app_commands
except Exception as e:
    not_installed_libs.append('discord.py')
    installs.append('"pip install discord.py" or "python3 -m pip install discord.py"')

try:
    import asyncio
except Exception as e:
    not_installed_libs.append('asyncio')
    installs.append('"pip install asyncio" or "python3 -m pip install asyncio"')

try:
    import ccxt
except Exception as e:
    not_installed_libs.append('ccxt')
    installs.append('"pip install ccxt" or "python3 -m pip install ccxt"')

try:
    from matplotlib import pyplot as plt
except Exception as e:
    not_installed_libs.append('matplotlib')
    installs.append('"pip install matplotlib" or "python3 -m pip install matplotlib"')

try:
    import mplfinance as mpf
except Exception as e:
    not_installed_libs.append('mplfinance')
    installs.append('"pip install mplfinance" or "python3 -m pip install mplfinance"')

try:
    import pandas as pd
except Exception as e:
    not_installed_libs.append('pandas')
    installs.append('"pip install pandas" or "python3 -m pip install pandas"')

if len(not_installed_libs) > 0:
    for i in range(len(not_installed_libs)):
        lib = not_installed_libs[i]
        solution = installs[i]
        raise ModuleNotFoundError(f'{lib} is not installed! Type {solution} in command line (Win+R => cmd)')

isTweenInstalled = True
try:
    import tween
    from pytweening import easeInOutSine
except ImportError as e:
    isTweenInstalled = False
#=========================================================================================================

import tkinter
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk

from datetime import datetime
from json import load
import time
import threading
import random
import platform
import os
import io
import numpy as np
from typing import Optional
import sys, os

def resource_path(relative_path):
    """Get the absolute path to a resource, works for .py and PyInstaller .exe"""
    if getattr(sys, "_MEIPASS", False):
        # PyInstaller has unpacked files here
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

settingsFile = 'settings.json'
localizationFile = resource_path('localization.json')
logoFile = resource_path('logo.png')
readmeFile = 'README.md'
requirementsFile = resource_path('requirements.txt')

files_to_check_1 = { #.json files
    settingsFile,
    localizationFile
}

files_to_check_2 = { #all other files
    logoFile,
    readmeFile,
    requirementsFile
}

# if os.path.exists("markets_linear_BTCUSDT.json"):
#     os.remove("markets_linear_BTCUSDT.json")
# save_file = open("markets_linear_BTCUSDT.json","x")
# save_file.writelines(str(ohlcv))
# save_file.close()

# print(bybitins.fetchTicker('ETHUSDT',[]))

max_console_len = 40

def fig2img(fig):
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    plotimg = Image.open(buf)
    return plotimg

class ProgramWindowClass:
    disabledrag = False
    lang: str = "en"
    localization = []

    def __init__(self,root):
        self.BotStatus = "Offline"
        self.BotObj = None
        self.BotMessages = {}
        self.TransparencySlider = None
        self.TransparencySliderValue = None
        self.ControlsLabel = None
        self.ControlsLabelBg = None
        self.ControlsBg = None
        self.ConsoleBg = None
        self.ConsoleLabel = None
        self.ConsoleTimings = None
        self.root = root
        self.root.title("Loading")
        self.root.geometry("400x235")
        self.root.resizable(False,False)
        self.root.configure(bg="black")
        self.root.attributes('-alpha',1)
        self.root.wm_attributes('-transparentcolor', '#111111')

        # self.root.overrideredirect(True)
        self.root.iconbitmap(resource_path("logo.ico"))

        self.root._offsetx = 0
        self.root._offsety = 0
        self.root._window_x = 980
        self.root._window_y = 500
        self.root._window_w = 400
        self.root._window_h = 235
        self.root.geometry('{w}x{h}+{x}+{y}'.format(w=self.root._window_w,h=self.root._window_h,x=self.root._window_x,y=self.root._window_y))
        self.root.bind('<Button-1>',self.clickwin)
        self.root.bind('<B1-Motion>',self.dragwin)
        self.root.bind("<ButtonRelease-1>",self.buttonreleased)

        global item_count
        global message_count
        item_count = -1
        message_count = 0

        s = ttk.Style()
        s.theme_use('clam')

        s.configure("green.Horizontal.TProgressbar", foreground='green', background='green',troughcolor='black',bordercolor='gray13',lightcolor='green',darkcolor='green')
        s.configure("red.Horizontal.TProgressbar", foreground='red', background='red',troughcolor='black',bordercolor='gray13',lightcolor='red',darkcolor='red')

        s.layout('arrowless.Horizontal.TScrollbar',
                     [('Horizontal.Scrollbar.trough',
                       {'children': [('Horizontal.Scrollbar.thumb',
                                      {'expand': '1', 'sticky': 'nswe'})],
                        'sticky': 'WE'})])

        s.configure("black.Horizontal.TScale", gripcount = 0,
                    background="gray17", darkcolor="gray13", lightcolor="gray19",
                    troughcolor="black", bordercolor="black", arrowcolor="black",
                    arrowsize=16,foreground='black')
        s.configure("arrowless.Horizontal.TScrollbar", gripcount=0,
                        background="gray17", darkcolor="gray13", lightcolor="gray19",
                        troughcolor="black", bordercolor="black", arrowcolor="black",
                    arrowsize=16,foreground='black')

        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=0)

        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(4, weight=1)
        self.root.rowconfigure(5, weight=1)
        self.root.rowconfigure(6, weight=1)

        self.LogoImage = Label(self.root,bg='black')
        self.render_image(self.LogoImage,resource_path('logo.png'))
        self.LogoImage.grid(row=0, column=1)

        self.ExitButton = Button(self.root,bg='black',highlightbackground='black',bd=0,command=self.exit_program)
        self.render_image(self.ExitButton,resource_path('x.png'),True)
        self.ExitButton.place(x=365,y=5)

        self.StatusLabel = Label(self.root, text='Checking configuration files', font='Arial 16', bg='black', fg='white')
        self.StatusLabel.grid(row=1, column=1)#.place(x=60,y=20)
        self.UnderLabel1 = Label(self.root, text='', font='Arial 8', bg='black', fg='white')
        self.UnderLabel1.place(x=10,y=135)#.grid(row=3, column=0)
        self.UnderLabel2 = Label(self.root, text='', font='Arial 10', bg='black', fg='white')
        self.UnderLabel2.grid(row=3, column=1)#.place(x=80,y=80)
        self.ProgressBar = ttk.Progressbar(self.root, orient="horizontal", length=150, mode="determinate", style="green.Horizontal.TProgressbar")
        self.ProgressBar.grid(row=2, column=1)#.place(x=5,y=40)

        self.ListBox = Listbox(self.root, selectmode='extended', height=3, width=40, bg='#000000', fg='white',highlightbackground='gray13',font="Consolas 8")
        self.ScrollBar = ttk.Scrollbar(self.root,orient="horizontal",style="arrowless.Horizontal.TScrollbar")#,width=14,bg='black')

        self.VersionLabel = Label(self.root,text='v1.2.1',font='Arial 6',bg='black',fg='gray29')
        self.VersionLabel.place(x=350,y=215)

        self.ListBox.configure(xscrollcommand=self.ScrollBar.set)
        self.ScrollBar.configure(command=self.ListBox.xview)

    def dragwin(self,event):
        if self.disabledrag: return
        delta_x = self.root.winfo_pointerx() - self.root._offsetx
        delta_y = self.root.winfo_pointery() - self.root._offsety
        x = self.root._window_x + delta_x
        y = self.root._window_y + delta_y
        self.root.geometry("+{x}+{y}".format(x=x, y=y))
        self.root._offsetx = self.root.winfo_pointerx()
        self.root._offsety = self.root.winfo_pointery()
        self.root._window_x = x
        self.root._window_y = y

    def clickwin(self,event):
        self.root._offsetx = self.root.winfo_pointerx()
        self.root._offsety = self.root.winfo_pointery()

    def buttonreleased(self,event):
        if self.disabledrag: self.disabledrag = False

    def change_transparency(self,value=100):
        self.disabledrag = True
        value = float(value)
        if value < 0 or value > 100:
            return
        self.TransparencySliderValue.configure(text=f'Transparency: {int(value)}%')
        self.root.attributes('-alpha',value/100)

    def render_image(self,where,imgname=resource_path('logo.png'),shitcode=False):
        if shitcode:
            global img2
            img2 = ImageTk.PhotoImage(Image.open(imgname))
            where.configure(image=img2)
        else:
            global img
            img = ImageTk.PhotoImage(Image.open(imgname))
            where.configure(image=img)

    def add_message_to_list(self,message='',message_type=0,display_message_time=False):
        global item_count
        global message_count
        message_count += 1
        message = message.lower()

        splits = len(message)//max_console_len + (len(message)%max_console_len > 0)
        added_time = False
        for i in range(0,splits):

            #print(message[i*max_console_len:(i+1)*max_console_len],len(message[i*max_console_len:(i+1)*max_console_len]))
            item_count += 1

            if display_message_time and not added_time and message_type != 4:
                added_time = True
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                self.ConsoleTimings.insert(item_count,current_time)
            elif message_type == 4 and not added_time:
                added_time = True
                self.ConsoleTimings.insert(item_count,"INFO:")
            elif message_type == 5 and not added_time:
                added_time = True
                self.ConsoleTimings.insert(item_count,"END:")
            else:
                self.ConsoleTimings.insert(item_count,"")

            self.ListBox.insert(item_count,message[i*max_console_len:(i+1)*max_console_len])
            if message_type == 0:
                self.ConsoleTimings.itemconfig(item_count,{'fg':'white'})
                self.ListBox.itemconfig(item_count,{'fg':'white'})
            elif message_type == 1:
                self.ConsoleTimings.itemconfig(item_count,{'fg':'orange'})
                self.ListBox.itemconfig(item_count,{'fg':'orange'})
            elif message_type == 2:
                self.ConsoleTimings.itemconfig(item_count,{'fg':'black','bg':'red'})
                self.ListBox.itemconfig(item_count,{'fg':'black','bg':'red'})
            elif message_type == 3:
                self.ConsoleTimings.itemconfig(item_count,{'fg':'lime'})
                self.ListBox.itemconfig(item_count,{'fg':'lime'})
            elif message_type == 4:
                self.ConsoleTimings.itemconfig(item_count,{'fg':'aqua'})
                self.ListBox.itemconfig(item_count,{'fg':'aqua'})
            elif message_type == 5:
                self.ConsoleTimings.itemconfig(item_count,{'fg':'black','bg':'white'})
                self.ListBox.itemconfig(item_count,{'fg':'black','bg':'white'})

    def exit_program(self,custom_message = None):
        exit_message = 'Exiting in 10 seconds...'

        if self.BotStatus == "Working":
            #await self.BotObj.close()
            if len(self.BotMessages) > 0:
                self.add_message_to_list(f"Bot had {len(self.BotMessages)} active messages. They won't work after bot restart.",1)

        if custom_message:
            exit_message = str(custom_message)
        self.add_message_to_list(exit_message,5,True)

        def exit_func():
            time.sleep(10)
            root.destroy()

        exiting = threading.Thread(target=exit_func,daemon=True)
        exiting.run()
        return True

    def underlabel_dots_anim(self):
        dots = 0
        for i in range(1,random.randint(10,20)):
            dots = (dots+1)%3
            self.UnderLabel2['text'] = 'starting bot'+'.'*(dots+1)
            time.sleep(.25)

    def start_progress(self):
        #progress.start()
        global files_to_check_1
        global files_to_check_2
        failed = False
        time.sleep(1)
        progress_per_file = 100/(len(files_to_check_1)+len(files_to_check_2))
        for file in files_to_check_1:
            status,message,solution = confCheck(file,1)
            if not status:
                self.StatusLabel['text'] = 'Failed'
                self.ListBox.insert('active',message)
                #self.UnderLabel1.configure(text="Possible solution:",bg="black", borderwidth=1, relief="groove")
                self.UnderLabel2['text'] = solution
                self.ProgressBar.configure(mode="indeterminate",style="red.Horizontal.TProgressbar",value=0)
                self.ProgressBar.start()

                self.ListBox.grid(row=5,column=1)
                self.ScrollBar.place(x=78,y=155,width=244)#.grid(row=4, column=1, sticky=NS)

                failed = True
            elif not failed:
                self.ProgressBar['value'] += progress_per_file
        for file in files_to_check_2:
            status,message,solution = confCheck(file,2)
            if not status:
                self.StatusLabel['text'] = 'Failed'
                self.ListBox.insert('active',message)
                #self.UnderLabel1.configure(text="Possible solution:",bg="black", borderwidth=1, relief="groove")
                self.UnderLabel2['text'] = solution
                self.ProgressBar.configure(mode="indeterminate",style="red.Horizontal.TProgressbar")
                self.ProgressBar.start()

                self.ListBox.grid(row=5,column=1)
                self.ScrollBar.place(x=78,y=155,width=244)#.grid(row=4, column=1, sticky=NS)

                failed = True
            elif not failed:
                self.ProgressBar['value'] += progress_per_file
        if not failed:
            self.StatusLabel['text'] = 'Everything is good!'
            self.ProgressBar.configure(mode="indeterminate")
            self.ProgressBar.start()

            dotsanim = threading.Thread(target=self.underlabel_dots_anim,daemon=True)
            dotsanim.start()
            self.control_panel_process()

    def onMouseWheel(self,event):
        listboxes = [self.ListBox,self.ConsoleTimings]
        """
        Convert mousewheel motion to scrollbar motion.
        """
        if (event.num == 4):    # Linux encodes wheel as 'buttons' 4 and 5
            delta = -1
        elif (event.num == 5):
            delta = 1
        else:                   # Windows & OSX
            delta = int(-event.delta/120)
        for lb in listboxes:
            lb.yview("scroll", delta, "units")
        return "break"

    def getLT(self,text):
        for category,cdata in self.localization[self.lang].items():
            for name,value in cdata.items():
                if name == text:
                    return value
        for category,cdata in self.localization["en"].items():
            for name,value in cdata.items():
                if name == text:
                    return value
        return "{No text found for '"+text+"'}"

    def control_panel_process(self):
        self.BotStatus = "Prepairing"
        window_size = [400,235]
        logo_pos = [180,10]
        exit_pos = [365,5]
        version_pos = [350,215]

        self.StatusLabel.grid_forget()
        self.ProgressBar.grid_forget()
        time.sleep(1)

        if isTweenInstalled:
            tween1 = tween.to(window_size,0,500,.25,"easeInOutSine")
            tween2 = tween.to(window_size,1,600,.25,"easeInOutSine")
            logotween1 = tween.to(logo_pos,0,0,.5,"easeOutSine")
            logotween2 = tween.to(logo_pos,1,0,.5,"easeOutSine")
            exittween1 = tween.to(exit_pos,0,465,.25,"easeInOutSine")
            versiontween1 = tween.to(version_pos,0,450,.25,"easeInOutSine")
            versiontween2 = tween.to(version_pos,1,580,.25,"easeInOutSine")
            for var in range(0,50):
                tween.update(.01)
                self.root.geometry(str(int(window_size[0]))+"x"+str(int(window_size[1])))
                self.LogoImage.place(x=logo_pos[0],y=logo_pos[1])
                self.ExitButton.place(x=exit_pos[0],y=exit_pos[1])
                self.VersionLabel.place(x=version_pos[0],y=version_pos[1])
                time.sleep(.01)

            # for var in range(0,50):
            #     tween.update(.01)
            #     time.sleep(.01)
            time.sleep(.25)

        self.root.geometry("500x600")
        self.root.title("Control panel")
        self.LogoImage.place(x=0,y=0)
        self.StatusLabel.place(x=165,y=13)
        self.ExitButton.place(x=465,y=5)
        self.StatusLabel.configure(text='Trade Helper Bot')
        self.VersionLabel.place(x=450,y=580)

        self.UnderLabel2.grid_forget()

        self.ConsoleBg = Canvas(self.root,height=17,width=295,bg='gray9',highlightbackground='gray9')
        self.ConsoleBg.place(x=200,y=55)
        self.ConsoleLabel = Label(self.root,text='CONSOLE',font='Arial 9',bg='gray9',fg='white')
        self.ConsoleLabel.place(x=310,y=55)

        self.ConsoleTimings = Listbox(self.root, selectmode='extended', height=35, width=8, bg='black', fg='white',highlightbackground='gray9',font="Consolas 8")
        self.ConsoleTimings.place(x=199,y=75)

        self.ConsoleTimings.bind("<MouseWheel>", self.onMouseWheel)
        self.ConsoleTimings.bind("<Button-4>", self.onMouseWheel)
        self.ConsoleTimings.bind("<Button-5>", self.onMouseWheel)
        self.ListBox.bind("<MouseWheel>", self.onMouseWheel)
        self.ListBox.bind("<Button-4>", self.onMouseWheel)
        self.ListBox.bind("<Button-5>", self.onMouseWheel)


        #WIP
        self.ControlsBg = Canvas(self.root,height=510,width=196,bg='black',highlightbackground='gray9')
        self.ControlsBg.place(x=0,y=55)
        self.ControlsBg.create_text(97, 20, text = "WIP", angle = -90, anchor = "w",font='Helvetica 200 bold', fill='gray2')
        self.ControlsLabelBg = Canvas(self.root,height=17,width=196,bg='gray9',highlightbackground='gray9')
        self.ControlsLabelBg.place(x=0,y=55)
        self.ControlsLabel = Label(self.root,text='CONTROLS',font='Arial 9',bg='gray9',fg='white')
        self.ControlsLabel.place(x=70,y=55)
        #================BUTTONS==============
        self.TransparencySliderValue = Label(self.root,text='Transparency: 100%',font='Helvetica 10',bg='black',fg='white')
        self.TransparencySlider = ttk.Scale(self.root, from_=5, to=100, value=100,command = self.change_transparency,length=150,style='black.Horizontal.TScale')
        # self.Button1 = Button(self.root,text='button1')
        # self.Button2 = Button(self.root,text='button2')
        # self.Button3 = Button(self.root,text='button3')
        # self.Button4 = Button(self.root,text='button4')
        #
        self.TransparencySliderValue.place(x=10,y=85)
        self.TransparencySlider.place(x=10,y=110)
        # self.Button1.grid(row=1,column=0,padx=5)
        # self.Button2.grid(row=2,column=0,padx=5)
        # self.Button3.grid(row=3,column=0,padx=5)
        # self.Button4.grid(row=4,column=0,padx=5)
        #=====================================

        self.ListBox.place(x=249,y=75)
        self.ListBox.configure(height=35,width=41,highlightbackground='gray9')

        #============================================MAIN BOT PROCESS================================================

        if not isTweenInstalled:
            self.add_message_to_list('No tween installed! Use "pip install tween" or "python3 -m pip install tween"',1)

        global item_count
        global message_count

        self.add_message_to_list(f'reading {settingsFile}...',0,True)
        with open(settingsFile, encoding="utf8") as data:
            settings = load(data)
        time.sleep(0.2)
        has_warnings = False
        has_errors = False
        for i in settings:
            time.sleep(0.1)
            if settings[i] == "" and i != 'status_message' and i != 'bot_token':
                self.add_message_to_list(f'{settingsFile} has empty field "{i}". Continuing can cause errors',1,False)
                has_warnings = True
            if i == 'allowed_channels_id':
                has_something = False
                for j in settings[i]:
                    if j != "": has_something = True
                if not has_something:
                    self.add_message_to_list(f'{settingsFile} has no allowed channels assigned at "{i}". Bot will not respond to any message.',1,False)
                    has_warnings = True
            if settings[i] == "" and i == 'bot_token':
                self.add_message_to_list(f'{settingsFile} has no bot token at "{i}".',2,False)
                has_errors = True
        if not has_warnings and not has_errors:
            self.add_message_to_list(f'done reading file: {settingsFile}',3,True)
        elif not has_errors:
            self.add_message_to_list(f'done reading file: {settingsFile}',1,True)
        else:
            self.add_message_to_list(f'done reading file: {settingsFile}',2,True)





        self.add_message_to_list(f'reading {localizationFile}...',0,True)
        with open(localizationFile, encoding="utf8") as data:
            self.localization = load(data)
        time.sleep(0.5)


        self.lang = settings["localization"]
        try:
            self.localization[self.lang]
        except:
            self.add_message_to_list(f'no localization called "{self.lang}" found. "en" will be used instead.',1,False)
            self.lang = "en"


        has_warnings = False
        has_errors = False
        for group in self.localization[self.lang]:
            for element in self.localization[self.lang][group]:
                if self.localization[self.lang][group][element] == "":
                    time.sleep(0.1)
                    has_warnings = True
                    self.add_message_to_list(f'{localizationFile} has empty field at "{lang}"/"{group}"/"{element}". Continuing can cause errors',1,False)

        if not has_warnings and not has_errors:
            self.add_message_to_list(f'done reading file: {localizationFile}',3,True)
        elif not has_errors:
            self.add_message_to_list(f'done reading file: {localizationFile}',1,False)
        else:
            self.add_message_to_list(f'done reading file: {localizationFile}',2,False)
            #localization.json has error :(

        self.add_message_to_list(f'getting info from {settingsFile}...',0,True)
        def status_check(status):
            if status == 0:
                return discord.Status.offline
            if status == 1:
                return discord.Status.online
            if status == 2:
                return discord.Status.dnd
            if status == 3:
                return discord.Status.idle
            return discord.Status.online


        intents = discord.Intents.default()
        intents.message_content = True

        client = None
        tree = None
        try:
            client = discord.Client(intents=intents)
            tree = app_commands.CommandTree(client)
        except Exception as e:
            self.add_message_to_list(str(e),2,True)
            if platform.python_version() == '3.12.4':       #<=========================================================TEMP WORKAROUND
                self.add_message_to_list('Possible solution: use python3.10 instead',4,False)
            self.exit_program()

        self.BotObj = client

        bot_id = settings["bot_id"]
        access_role = settings["access_role"]
        mention_role = settings["mention_role"]
        allowed_channels = settings["allowed_channels_id"]
        colors = [
            settings["colors"]["active_deal"],
            settings["colors"]["good_deal"],
            settings["colors"]["bad_deal"],
            settings["colors"]["nothing_deal"]
        ]
        status_message = settings["status_message"]
        status = status_check(settings["status"])
        self.add_message_to_list(f'done retrieving info from: {settingsFile}',3,True)


        def ohlcv2df(values):
            candles = []
            candles = pd.DataFrame(data=values)
            candles.rename(columns = { 0 : 'Start Date',
                                       1 : 'Open',
                                       2 : 'High',
                                       3 : 'Low',
                                       4 :'Close',
                                       }, inplace = True)
            candles['Start Date'] = pd.to_datetime(candles['Start Date'], unit='ms')
            candles = candles.astype({'Open': 'float'})
            candles = candles.astype({'High': 'float'})
            candles = candles.astype({'Low': 'float'})
            candles = candles.astype({'Close': 'float'})
            candles = candles.set_index('Start Date', inplace=False)
            return candles

        def values2plot(values):
            mc = mpf.make_marketcolors(up='#2fd91e', down='#ed2f1a', inherit=True)
            s = mpf.make_mpf_style(base_mpl_style=['bmh', 'dark_background'], marketcolors=mc, y_on_right=True)
            coin_plot, axlist = mpf.plot(values,
                                         figratio=(16, 6),
                                         type="candle",
                                         style=s,
                                         tight_layout=True,
                                         datetime_format='%H:%M',
                                         ylabel="Price ($)",
                                         returnfig=True)
            return axlist, coin_plot

        def create_plot(coin: str,timeframe: str,plot_range: int):
            bybitInstance = ccxt.bybit()
            try:
                ohlcv = bybitInstance.fetch_ohlcv(coin,timeframe,limit=max(min(plot_range,10),1000))
            except Exception as e:
                self.add_message_to_list(str(e),2,True)
                return False,False

            if not len(ohlcv):
                self.add_message_to_list(f"Something went wrong and plot values haven't been received. for {message.author.name} with coin {data[0]}", 1,True)

            values = ohlcv2df(ohlcv[-plot_range:-1])

            axlist, coin_plot = values2plot(values)
            #axlist[0].set_title(f"{data[0]} - {timeframe}", fontsize=20, style='italic', fontfamily='Consolas' )

            return axlist,coin_plot

        #============================PREPARATIONS============================================
        bot_messages = {} #This list is for situations, when bot goes offline
        #============================PREPARATIONS============================================

        #============================DISCORD BOT CLASSES=====================================

        class zoomPlotModal(discord.ui.Modal,title = f"Type zoom level:"):
            def __init__(self,plot_range):
                super().__init__(timeout=None)
                self.plot_range = plot_range
            input_zoom = discord.ui.TextInput(label = "Zoom level:", style = discord.TextStyle.short, placeholder = "from 10 to 1000", default = "", required=True) #str(self.plot_range)
            async def on_submit(self, interaction: Interaction[ClientT], /) -> None:
                user_input = self.input_zoom.value
                try:
                    user_input = max(min(int(user_input),1000),10)
                except:
                    user_input = self.plot_range

                self.on_submit_interaction = interaction #unused
                self.on_submit_input = user_input
                await interaction.response.send_message(content=f"Scaling graph to {user_input}", delete_after = 5)
                self.stop()

        class trade_view(discord.ui.View):

            def __init__(self,data,timeframe,embed,plot_range,bot_message,getLT):
                super().__init__(timeout=None)
                self.data = data
                self.timeframe = timeframe
                self.embed = embed
                self.plot_range = plot_range
                self.bot_message = bot_message
                self.getLT = getLT

            @discord.ui.button(label=self.getLT("tp1"), custom_id="button-1", style=discord.ButtonStyle.green)
            async def b1_click(self, button : discord.ui.Button, interaction: discord.Interaction) -> None:
                self.embed.color = int(colors[1],16)
                bot_messages[self.bot_message.id] = None
                await self.bot_message.edit(content=self.getLT("tp2"), view=None, embed = self.embed)

            @discord.ui.button(label=self.getLT("sl1"), custom_id="button-2", style=discord.ButtonStyle.red)
            async def b2_click(self, button : discord.ui.Button, interaction: discord.Interaction) -> None:
                self.embed.color = int(colors[2],16)
                bot_messages[self.bot_message.id] = None
                await self.bot_message.edit(content=self.getLT("sl2"), view=None, embed = self.embed)

            @discord.ui.button(label=self.getLT("er1"), custom_id="button-3", style=discord.ButtonStyle.grey)
            async def b3_click(self, button : discord.ui.Button, interaction: discord.Interaction) -> None:
                self.embed.color = int(colors[3],16)
                bot_messages[self.bot_message.id] = None
                await self.bot_message.edit(content=self.getLT("er2"), view=None, embed = self.embed)


            @discord.ui.button(label=self.getLT("setZoom"), custom_id="button-4", style=discord.ButtonStyle.primary)
            async def b4_click(self, interaction: discord.Interaction, button : discord.ui.Button) -> None:
                setZoomModal = zoomPlotModal(self.plot_range)
                await interaction.response.send_modal(setZoomModal)
                response = await setZoomModal.wait()
                #await setZoomModal.on_submit_interaction.response.send_message(content=f"Updating graph scale to {user_input}")
                user_input = setZoomModal.on_submit_input
                #plot_range = max(min(plot_range-10,10),1000)
                axlist, coin_plot = create_plot(self.data[0],self.timeframe,user_input)
                if axlist:
                    coin_plot.savefig(f'plots/{self.data[0]}plot.png', bbox_inches='tight')
                    message = await setZoomModal.on_submit_interaction.channel.send(content = f"<@&{mention_role}>", file = discord.File(f'plots/{self.data[0]}plot.png'), embed = self.embed, view = None)
                else:
                    message = await setZoomModal.on_submit_interaction.channel.send(content = f"<@&{mention_role}>", embed = self.embed, view = None)

                message_view = trade_view(self.data,self.timeframe,self.embed,self.plot_range,message,self.getLT)
                await message.edit(view = message_view)
                bot_messages[str(message.id)] = message
                bot_messages[str(self.bot_message.id)] = None
                await self.bot_message.delete()
                self.stop()


            # @discord.ui.button(label=self.getLT("zoomOut"), custom_id="button-5", style=discord.ButtonStyle.primary)
            # async def b5_click(self, button : discord.ui.Button, interaction: discord.Interaction) -> None:
            #     plot_range = max(min(plot_range+10,10),1000)
            #     axlist, coin_plot = await create_plot(data[0],timeframe,plot_range)
            #     await interaction.response.edit_message(file= discord.File(f'plots/{data[0]}plot.png'), view=None, embed = trade)

        #============================DISCORD BOT CLASSES=====================================

        #============================DISCORD BOT COMMANDS=====================================
        @tree.command(
            name=self.getLT("dc"),
            description=self.getLT("dc_desc"),
            guild=None #discord.Object(id=677524157793304579),
        )
        @app_commands.describe(pair_name = self.getLT("pn_desc"),entry_point = self.getLT("ep_desc"),take_profit = self.getLT("tp_desc"),stop_loss = self.getLT("sl_desc"))
        async def deal_command(interaction: discord.Interaction, pair_name: str, entry_point: Optional[str], take_profit: Optional[str], stop_loss: Optional[str]):

            await interaction.response.send_message(content=f"Creating deal in {pair_name}...", delete_after = 5)

            data = [pair_name.upper()]
            not_provided = []
            if entry_point:
                data.append(entry_point)
            else:
                data.append(None)
                not_provided.append(self.getLT("ep"))
            if take_profit:
                data.append(take_profit)
            else:
                data.append(None)
                not_provided.append(self.getLT("tp"))
            if stop_loss:
                data.append(stop_loss)
            else:
                data.append(None)
                not_provided.append(self.getLT("sl"))

            #============================================TRADING STOCK GENERATION TESTING===============================================
            timeframe = '15m'
            plot_range = 100
            axlist,coin_plot = create_plot(data[0],timeframe, plot_range)
            #============================================TRADING STOCK GENERATION TESTING===============================================
            trade = discord.Embed(title=data[0], color=int(colors[0],16))

            if data[1]:
                trade.add_field(name=self.getLT("ep"), value=data[1], inline=False)
            if data[2]:
                trade.add_field(name=self.getLT("tp"), value=data[2], inline=False)
            if data[3]:
                trade.add_field(name=self.getLT("sl"), value=data[3], inline=False)
            if len(not_provided) > 0:
                trade.add_field(name=self.getLT("not_provided"), value=" ".join(not_provided),inline=False)

            if axlist:
                coin_plot.savefig(f'plots/{data[0]}plot.png', bbox_inches='tight')
                bot_message = await interaction.channel.send(content = f"<@&{mention_role}>", file = discord.File(f'plots/{data[0]}plot.png'), embed = trade, view = None)
            else:
                bot_message = await interaction.channel.send(content = f"<@&{mention_role}>", embed = trade, view = None)


            message_view = trade_view(data,timeframe,trade,plot_range,bot_message,self.getLT)
            await bot_message.edit(view = message_view)
            bot_messages[str(bot_message.id)] = bot_message


        #============================DISCORD BOT COMMANDS=====================================

        @client.event
        async def on_ready():
            self.add_message_to_list('Bot is loaded successfully',3,True)
            self.add_message_to_list('to use bot, type: "{Coin name} {Entry point} {Take profit} {Stop loss}" in one of the allowed channels.',4,False)
            self.BotStatus = "Working"
            await tree.sync(guild=None)#discord.Object(id=677524157793304579))
            await client.change_presence(status=status,activity=discord.CustomActivity(name=status_message))

        @client.event
        async def on_message(message):
            if str(message.author.id) == str(bot_id):
                self.add_message_to_list(f'{message.author.name} sent a message',0,True)
            else:
                self.add_message_to_list(f'Got message from "{message.author.name}" in channel "{message.channel.name}"',0,True)
            if access_role in [str(y.id) for y in message.author.roles] and str(message.channel.id) in allowed_channels:
                data = message.content.split()
                if len(data) > 1 and data[0] == f'<@{bot_id}>': #it is a bot id for tagging it in channel
                    data.pop(0)
                    if len(message.attachments) > 0:
                        img = message.attachments[0].url
                    else:
                        img = False
                    for i in range(len(data)):
                        data[i] = data[i].replace('-',' ')
                    if data[0] == data[0].upper():

                        self.add_message_to_list(f'Message from "{message.author.name}" passed all checks',0,False)
                        #============================================TRADING STOCK GENERATION TESTING===============================================
                        timeframe = '15m'
                        plot_range = 100
                        axlist,coin_plot = create_plot(data[0],timeframe, plot_range)
                        #============================================TRADING STOCK GENERATION TESTING===============================================

                        trade = discord.Embed(title=data[0], color=int(colors[0],16))
                        if len(data) > 1:
                            trade.add_field(name=self.getLT("ep"), value=data[1], inline=False)
                        else:
                            trade.add_field(name=self.getLT("not_provided"), value="`"+self.getLT("ep")+"\n"+self.getLT("tp")+"\n"+self.getLT("sl")+"`")
                        if len(data) > 2:
                            trade.add_field(name=self.getLT("tp"), value=data[2], inline=False)
                        else:
                            trade.add_field(name=self.getLT("not_provided"), value="`"+self.getLT("tp")+"\n"+self.getLT("sl")+"`")
                        if len(data) > 3:
                            trade.add_field(name=self.getLT("sl"), value=data[3], inline=False)
                        else:
                            trade.add_field(name=self.getLT("not_provided"), value="`"+self.getLT("sl")+"`")

                        bot_message = None
                        if len(message.attachments) > 0:
                            file = await message.attachments[0].to_file()
                            file.filename = 'image.png'
                            bot_message = await message.channel.send(content = f"<@&{mention_role}>", file = file, embed = trade, view = trade_view(data,timeframe,trade,plot_range,self.getLT))
                        else:
                            if axlist:
                                coin_plot.savefig(f'plots/{data[0]}plot.png', bbox_inches='tight')
                                bot_message = await message.channel.send(content = f"<@&{mention_role}>", file = discord.File(f'plots/{data[0]}plot.png'), embed = trade, view = None)
                            else:
                                bot_message = await message.channel.send(content = f"<@&{mention_role}>", embed = trade, view = None)
                            message_view = trade_view(data,timeframe,trade,plot_range,bot_message,self.getLT)
                            await bot_message.edit(view = message_view)
                            #bot_message.delete()
                        bot_messages[str(bot_message.id)] = bot_message
                        await message.delete()

        self.add_message_to_list('Starting loading bot...',0,True)
        self.BotStatus = "Starting"
        try:
            client.run(settings['bot_token'])
        except Exception as e:
            self.add_message_to_list(str(e),2,True)
        self.BotMessages = bot_messages
        self.add_message_to_list('Bot stopped',0,True)
        self.exit_program()
    #============================================================================================================

def check(f):
    try:
        open(f, encoding="utf8")
    except:
        return False
    else:
        return True
def check2(f):
    try:
        load(open(f, encoding="utf8"))
    except Exception as e:
        return False,e
    else:
        return True, True
def confCheck(filename,fileType):
    time.sleep(random.random())
    if not check(filename):
        return False,f"{filename} wasn't found.","Consider adding file to script folder/renaming file to '{filename}'."
    if fileType == 2:
        return True,"",""
    status,result = check2(filename)
    if not status:
        return False,f"{filename}: "+str(result),"Try to redownload file from github"#f"Error. {filename} file is broken.","Change settings file and restart program"
    return True,f"{filename} is OK.",""

root = tkinter.Tk()
window = ProgramWindowClass(root)
programProcess1 = threading.Thread(target=window.start_progress,daemon=True)
programProcess1.start()
root.mainloop()

#==================================================================================================================