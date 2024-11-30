
#EVERYTHING IS UNDER APACHE 2.0

#================================Libraries checking part==================================================
try:
    import tkinter
except ImportError as e:
    exit(str(e)+' No tkinter installed! Use "pip install tk" or "python3 -m pip install tk"')

try:
    import PIL
except ImportError as e:
    exit(str(e)+' No pillow installed! Use "pip install pillow" or "python3 -m pip install pillow"')

try:
    import discord
except ImportError as e:
    exit(str(e)+' No discord.py installed! Use "pip install discord.py" or "python3 -m pip install discord.py"')
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

settingsFile = 'settings.json'
localizationFile = 'localization.json'
logoFile = 'logo.png'
readmeFile = 'README.md'
requierementsFile = 'requierements.txt'

files_to_check_1 = { #.json files
    settingsFile,
    localizationFile
}

files_to_check_2 = { #all other files
    logoFile,
    readmeFile,
    requierementsFile
}

max_console_len = 40
class ProgramWindowClass:
    def __init__(self,root):
        self.ConsoleBg = None
        self.ConsoleLabel = None
        self.ConsoleTimings = None
        self.root = root
        self.root.title("Loading")
        self.root.geometry("400x235")
        self.root.resizable(False,False)
        self.root.configure(bg="black")

        s = ttk.Style()
        s.theme_use('clam')

        s.configure("green.Horizontal.TProgressbar", foreground='green', background='green',troughcolor='black',bordercolor='gray13',lightcolor='green',darkcolor='green')
        s.configure("red.Horizontal.TProgressbar", foreground='red', background='red',troughcolor='black',bordercolor='gray13',lightcolor='red',darkcolor='red')

        s.layout('arrowless.Horizontal.TScrollbar',
                     [('Horizontal.Scrollbar.trough',
                       {'children': [('Horizontal.Scrollbar.thumb',
                                      {'expand': '1', 'sticky': 'nswe'})],
                        'sticky': 'WE'})])

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
        self.render_image('logo.png')
        self.LogoImage.grid(row=0, column=1)
        self.StatusLabel = Label(self.root, text='Checking configuration files', font='Arial 16', bg='black', fg='white')
        self.StatusLabel.grid(row=1, column=1)#.place(x=60,y=20)
        self.UnderLabel1 = Label(self.root, text='', font='Arial 8', bg='black', fg='white')
        self.UnderLabel1.place(x=10,y=135)#.grid(row=3, column=0)
        self.UnderLabel2 = Label(self.root, text='', font='Arial 10', bg='black', fg='white')
        self.UnderLabel2.grid(row=3, column=1)#.place(x=80,y=80)
        self.ProgressBar = ttk.Progressbar(self.root, orient="horizontal", length=150, mode="determinate", style="green.Horizontal.TProgressbar")
        self.ProgressBar.grid(row=2, column=1)#.place(x=5,y=40)

        self.ListBox = Listbox(self.root, selectmode='extended', height=3, width=40, bg='black', fg='white',highlightbackground='gray13',font="Consolas 8")
        self.ScrollBar = ttk.Scrollbar(self.root,orient="horizontal",style="arrowless.Horizontal.TScrollbar")#,width=14,bg='black')

        self.VersionLabel = Label(self.root,text='v1.1',font='Arial 6',bg='black',fg='gray29')
        self.VersionLabel.place(x=370,y=215)

        self.ListBox.configure(xscrollcommand=self.ScrollBar.set)
        self.ScrollBar.configure(command=self.ListBox.xview)

    def render_image(self,imgname):
        global img
        img = ImageTk.PhotoImage(Image.open(imgname))
        self.LogoImage.configure(image=img)

    def add_message_to_list(self,message,message_type,display_message_time):
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

    def start_progress(self,w):
        #progress.start()
        global files_to_check_1
        global files_to_check_2
        failed = False
        # time.sleep(1)
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
            dots = 0
            for i in range(1,random.randint(6,12)):
                dots = (dots+1)%3
                self.UnderLabel2['text'] = 'starting bot'+'.'*(dots+1)
                time.sleep(.25)

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

    def control_panel_process(self):
        self.root.geometry("500x600")
        self.root.title("Control panel")
        self.LogoImage.place(x=0,y=0)
        self.StatusLabel.place(x=165,y=13)
        self.StatusLabel.configure(text='Trade Helper Bot')
        self.VersionLabel.place(x=470,y=580)

        self.ProgressBar.grid_forget()
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
        # self.Button1 = Button(self.root,text='button1')
        # self.Button2 = Button(self.root,text='button2')
        # self.Button3 = Button(self.root,text='button3')
        # self.Button4 = Button(self.root,text='button4')
        #
        # self.Button1.grid(row=1,column=0,padx=5)
        # self.Button2.grid(row=2,column=0,padx=5)
        # self.Button3.grid(row=3,column=0,padx=5)
        # self.Button4.grid(row=4,column=0,padx=5)
        #=====================================

        self.ListBox.place(x=249,y=75)
        self.ListBox.configure(height=35,width=41,highlightbackground='gray9')

        #============================================MAIN BOT PROCESS================================================
        global item_count
        global message_count
        item_count = -1
        message_count = 0
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
            localization = load(data)
        time.sleep(0.5)

        has_warnings = False
        has_errors = False
        for lang in localization:
            for group in localization[lang]:
                for element in localization[lang][group]:
                    if localization[lang][group][element] == "":
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

        selected_localization = settings["localization"]
        try:
            localization[selected_localization]
        except:
            self.add_message_to_list(f'no localization called "{selected_localization}" found. "en" will be used instead.',1,False)
            selected_localization = "en"

        intents = discord.Intents.default()
        intents.message_content = True

        client = discord.Client(intents=intents)
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

        @client.event
        async def on_ready():

            self.add_message_to_list('Bot is loaded successfully',3,True)
            self.add_message_to_list('to use bot, type: "{Coin name} {Entry point} {Take profit} {Stop loss}" in one of the allowed channels.',4,False)
            await client.change_presence(status=status,activity=discord.CustomActivity(name=status_message))

        @client.event
        async def on_message(message):
            self.add_message_to_list(f'Got message from "{message.author.name}" in channel "{message.channel.name}"',0,True)
            if access_role in [str(y.id) for y in message.author.roles] and str(message.channel.id) in allowed_channels:
                self.add_message_to_list(f'Message from "{message.author.name}" passed all checks',0,False)
                data = message.content.split()
                if len(data) > 0 and data[0] == f'<@{bot_id}>': #it is a bot id for tagging it in channel
                    data.pop(0)
                    if len(message.attachments) > 0:
                        img = message.attachments[0].url
                    else:
                        img = False
                    for i in range(len(data)):
                        data[i] = data[i].replace('-',' ')
                    if data[0] == data[0].upper():

                        trade = discord.Embed(title=data[0], color=int(colors[0],16))
                        trade.add_field(name=localization[selected_localization]["labels"]["ep"], value=data[1], inline=False)
                        trade.add_field(name=localization[selected_localization]["labels"]["tp"], value=data[2], inline=False)
                        trade.add_field(name=localization[selected_localization]["labels"]["sl"], value=data[3], inline=False)

                        class trade_view(discord.ui.View):
                            def __init__(self):
                                super().__init__(timeout=None)

                            @discord.ui.button(label=localization[selected_localization]["buttons"]["tp1"], custom_id="button-1", style=discord.ButtonStyle.green)
                            async def b1_click(self, button : discord.ui.Button, interaction: discord.Interaction) -> None:
                                trade.color = int(colors[1],16)
                                await interaction.response.edit_message(content=localization[selected_localization]["buttons"]["tp2"], view=None, embed = trade)

                            @discord.ui.button(label=localization[selected_localization]["buttons"]["sl1"], custom_id="button-2", style=discord.ButtonStyle.red)
                            async def b2_click(self, button : discord.ui.Button, interaction: discord.Interaction) -> None:
                                trade.color = int(colors[2],16)
                                await interaction.response.edit_message(content=localization[selected_localization]["buttons"]["sl2"], view=None, embed = trade)

                            @discord.ui.button(label=localization[selected_localization]["buttons"]["er1"], custom_id="button-3", style=discord.ButtonStyle.grey)
                            async def b3_click(self, button : discord.ui.Button, interaction: discord.Interaction) -> None:
                                trade.color = int(colors[3],16)
                                await interaction.response.edit_message(content=localization[selected_localization]["buttons"]["er2"], view=None, embed = trade)

                        if len(message.attachments) > 0:
                            file = await message.attachments[0].to_file()
                            file.filename = 'image.png'
                            await message.channel.send(content = f"<@&{mention_role}>", file = file, embed = trade, view = trade_view())
                        else:
                            await message.channel.send(content = f"<@&{mention_role}>", embed = trade, view = trade_view())

                        await message.delete()


        self.add_message_to_list('Starting loading bot...',0,True)
        try:
            client.run(settings['bot_token'])
        except Exception as e:
            self.add_message_to_list(str(e),2,True)
        self.add_message_to_list('Bot stopped',1,True)
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
    # time.sleep(random.random())
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
programProcess1 = threading.Thread(target=window.start_progress,args={root},daemon=True)
programProcess1.start()
root.mainloop()

#==================================================================================================================

