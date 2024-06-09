import customtkinter
import os
import random
import mimetypes
from pygame import mixer
import threading as thr
import colorsys
import time
import configparser
from discord.ext.tasks import loop
import discord
import discord.ext
from discord import app_commands
from datetime import datetime
from flask import Flask, Response
import pyaudio

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


customtkinter.set_appearance_mode("dark")
config = configparser.ConfigParser()
usetextbox = False




import sounddevice

#p = pyaudio.PyAudio()

#for i in range(p.get_device_count()):
#    print(p.get_device_info_by_index(i).get('name'))

config = configparser.ConfigParser()


"""
try:
    config.read('config.ini')
    audiodevice = config["Device"]["AudioDevice"]
    print(audiodevice)
except:
    config['Device'] = {'AudioDevice': str(sounddevice.query_devices(kind='output')["name"])}


    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    
    audiodevice = config["Device"]["AudioDevice"]
"""

def readconfignwrite(header, item, fallback):
    try:
        config.read('config.ini')
        print("Read config " + str(header) + ", " + str(item) + " and got " + str(config[header][item]))
        return config[header][item]
    except:
        config[header] = {item: fallback}

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        print(str(header) + ", " + str(item) + " changed to " + str(fallback))
    
    return config[header][item]

def writeconfig(header, item, input):
    settingschanged()
    config[header] = {item: input}

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print(str(header) + ", " + str(item) + " changed to " + str(input))



try:
    readqueuetype = int(readconfignwrite("STYLE", "Queuetype", 2))
    if readqueuetype == 1:
        usetextbox = True
    else:
        usetextbox = False
except:
    print("Could not read queue type!")

try:
    AudioPort = int(readconfignwrite("PORT", "Audioport", 5959))
except:
    print("Could not read audio port!")

#os.startfile('audioserver.py')

#-------------------------------------------------------

app = customtkinter.CTk()
screenx = 600 #round(app.winfo_screenwidth()/2)
screeny = 600 #round(app.winfo_screenheight()/1.3)
#print(str(screenx) + "x" + str(screeny))
app.geometry(str(screenx) + "x" + str(screeny))
app.iconbitmap("icon.ico")
app.title("PyWebRadio")
#app.resizable(width=True, height=True)


tabview = customtkinter.CTkTabview(master=app)
tabview.pack()

tabview.add("Queue")  
tabview.add("Settings")
tabview.add("Station")
tabview.add("Stream")
tabview.add("Bot")
tabview.set("Queue")  

customtkinter.set_widget_scaling(1)
customtkinter.set_window_scaling(1)



label = customtkinter.CTkLabel(text="Queue", fg_color="transparent", master=tabview.tab("Queue"), font=("Arial",20))
label.pack()

label = customtkinter.CTkLabel(text="Settings", fg_color="transparent", master=tabview.tab("Settings"), font=("Arial",20))
label.place(anchor=customtkinter.N, relx=0.5)

label = customtkinter.CTkLabel(text="Station", fg_color="transparent", master=tabview.tab("Station"), font=("Arial",20))
label.place(anchor=customtkinter.N, relx=0.5)

label = customtkinter.CTkLabel(text="Stream", fg_color="transparent", master=tabview.tab("Stream"), font=("Arial",20))
label.place(anchor=customtkinter.N, relx=0.5)

label = customtkinter.CTkLabel(text="Bot", fg_color="transparent", master=tabview.tab("Bot"), font=("Arial",20))
label.place(anchor=customtkinter.N, relx=0.5)
#label.pack()



if usetextbox:
    textbox = customtkinter.CTkTextbox(master=tabview.tab("Queue"), width=screenx, height=(int(screeny/1.6)))
    textbox.pack()
else:
    queueframe = customtkinter.CTkScrollableFrame(master=tabview.tab("Queue"), width=screenx, height=(int(screeny/1.6)), fg_color="#1D1E1E")
    queueframe.pack()

nowplaying = customtkinter.CTkLabel(text="Now playing", fg_color="transparent", master=tabview.tab("Queue"), font=("Arial",12))
nowplaying.pack(anchor=customtkinter.NW)

def skipsong():
    playaudio()

def reverseskip():
    bumpgetindex(-2)
    playaudio()

def gotofunc():
    try:
        global masterindex
        global masterlist
        if int(gotoentry.get()) >= 0 and int(gotoentry.get()) <= len(masterlist) - 1:
            masterindex = int(gotoentry.get()) - 1
            playaudio()
        else:
            print("Number out of range")
            err = thr.Thread(target=displayerror, args=("Number out of range", 2))
            err.daemon = True
            err.start()
    except:
        print("Invalid number")
        err = thr.Thread(target=displayerror, args=("Invalid number", 2))
        err.daemon = True
        err.start()


reverse = customtkinter.CTkButton(master=tabview.tab("Queue"), text="⏪", command=reverseskip, width=32)
reverse.pack(side=customtkinter.LEFT, anchor=customtkinter.NW)

skip = customtkinter.CTkButton(master=tabview.tab("Queue"), text="⏩", command=skipsong, width=32)
skip.pack(side=customtkinter.LEFT, anchor=customtkinter.NW)

gotoentry = customtkinter.CTkEntry(master=tabview.tab("Queue"), width=30)
gotoentry.pack(side=customtkinter.RIGHT, anchor=customtkinter.NE)
goto = customtkinter.CTkButton(master=tabview.tab("Queue"), text="GOTO", command=gotofunc, width=32)
goto.pack(side=customtkinter.RIGHT, anchor=customtkinter.NE)


#------------------SETTINGS------------------

def changequeue():
    writeconfig("STYLE", "Queuetype", queuetype.get())
    

def settingschanged():
    changesettings.configure(text="Settings changed, please restart the program")

queuetype = customtkinter.IntVar(value=0)
radiobutton_1 = customtkinter.CTkRadioButton(master=tabview.tab("Settings"), text="Text ",
                                             command=changequeue, variable= queuetype, value=1, width=0, height=0)
radiobutton_2 = customtkinter.CTkRadioButton(master=tabview.tab("Settings"), text="Button ",
                                             command=changequeue, variable= queuetype, value=2, width=0, height=0)
radiobutton_1.place(anchor=customtkinter.E, rely=0, relx= 1, y=60, x=-20)
radiobutton_2.place(anchor=customtkinter.E, rely=0, relx= 1, y=60, x=-90)

label = customtkinter.CTkLabel(text="Queue style ", fg_color="transparent", master=tabview.tab("Settings"), font = ("Arial", 16))
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=60, x=20)
longtext = "Display the queue using a button-based or a text-based system. Use text-based if you're experiencing performance issues with a large amount of audio files (>100, including jingles)"
label = customtkinter.CTkLabel(text=longtext, wraplength=screenx-20, justify="left", fg_color="transparent", master=tabview.tab("Settings"), font=("Arial", 12), text_color="gray70")
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=87, x=20)

def switch_event():
    writeconfig("BUILD", "Jingles", int(switch.get() == 'True'))
    
    if switch.get() == 'True':
        jingleslider.configure(state="normal", progress_color="steelblue1", button_color="#1F6AA5")
    else:
        jingleslider.configure(state="disabled", progress_color="gray60", button_color="gray70")



switch_var = customtkinter.StringVar(value="on")
switch = customtkinter.CTkSwitch(master=tabview.tab("Settings"), text="", command=switch_event,
                                 variable=switch_var, onvalue="True", offvalue="False", width=0)
switch.place(anchor=customtkinter.E, rely=0, relx= 1, y=140, x=-20)

label = customtkinter.CTkLabel(text="Jingles ", fg_color="transparent", master=tabview.tab("Settings"), font = ("Arial", 16))
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=140, x=20)
longtext = 'Adds a random audio file from the Jingles directory every few songs. The frequency is determined by "jingle frequency"'
label = customtkinter.CTkLabel(text=longtext, wraplength=screenx-20, justify="left", fg_color="transparent", master=tabview.tab("Settings"), font=("Arial", 12), text_color="gray70")
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=167, x=20)

def changejinglefreq(value):
    jingleslider.set(round(value))
    jinglefreq.configure(text=round(value))
    if round(value) != changejinglefreq.newvalue:
        changejinglefreq.newvalue = round(value)
        writeconfig("JINGLE", "Jinglefreq", round(value))


jinglefreq = customtkinter.CTkLabel(text="10", justify="right", fg_color="transparent", master=tabview.tab("Settings"), font=("Arial", 12))
jinglefreq.place(anchor=customtkinter.E, rely=0, relx= 1, y=220, x=-145)
jingleslider = customtkinter.CTkSlider(master=tabview.tab("Settings"), from_=1, to=10, progress_color="steelblue1", command=changejinglefreq, width=120)
jingleslider.place(anchor=customtkinter.E, rely=0, relx= 1, y=220, x=-20)
changejinglefreq.newvalue = 0
label = customtkinter.CTkLabel(text="Jingle frequency ", fg_color="transparent", master=tabview.tab("Settings"), font = ("Arial", 16))
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=220, x=20)
longtext = 'Determines how many songs there should be between each jingle.'
label = customtkinter.CTkLabel(text=longtext, wraplength=screenx-20, justify="left", fg_color="transparent", master=tabview.tab("Settings"), font=("Arial", 12), text_color="gray70")
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=247, x=20)


def changeend():
    writeconfig("END", "Doend", int(endswitch.get() == 'True'))
    


endswitch_var = customtkinter.StringVar(value="off")
endswitch = customtkinter.CTkSwitch(master=tabview.tab("Settings"), text="", command=changeend,
                                 variable=endswitch_var, onvalue="True", offvalue="False", width=0)
endswitch.place(anchor=customtkinter.E, rely=0, relx= 1, y=290, x=-20)

label = customtkinter.CTkLabel(text="Ending track(s)", fg_color="transparent", master=tabview.tab("Settings"), font = ("Arial", 16))
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=290, x=20)
longtext = 'Adds any audio files found in the "End" folder to the end of the queue.\nNOTE: These tracks will NOT be shuffled'
label = customtkinter.CTkLabel(text=longtext, wraplength=screenx-20, justify="left", fg_color="transparent", master=tabview.tab("Settings"), font=("Arial", 12), text_color="gray70")
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=317, x=20)



# ----------Station Settings--------------

nameEntry = customtkinter.CTkEntry(master=tabview.tab("Station"), placeholder_text="Station name")
nameEntry.place(anchor=customtkinter.E, rely=0, relx= 1, y=60, x=-20)
label = customtkinter.CTkLabel(text="Station Name", fg_color="transparent", master=tabview.tab("Station"), font = ("Arial", 16))
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=60, x=20)

def savestation():
    writeconfig("NAME", "stationname", nameEntry.get())
    settingschanged()

savebutton =  customtkinter.CTkButton(tabview.tab("Station"), text="Save", command=savestation)
savebutton.place(anchor=customtkinter.SW, rely=1, relx= 0, y=0, x=0)

# ----------Stream Settings----------------

def changeStream():
    writeconfig("STREAM", "enabled", int(streamswitch.get() == 'True'))

streamswitch_var = customtkinter.StringVar(value="on")
streamswitch = customtkinter.CTkSwitch(master=tabview.tab("Stream"), text="", command=changeStream,
                                 variable=streamswitch_var, onvalue="True", offvalue="False", width=0)
streamswitch.place(anchor=customtkinter.E, rely=0, relx= 1, y=60, x=-20)

label = customtkinter.CTkLabel(text="Audio Stream", fg_color="transparent", master=tabview.tab("Stream"), font = ("Arial", 16))
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=60, x=20)
longtext = 'Stream the station audio at the audio server port'
label = customtkinter.CTkLabel(text=longtext, wraplength=screenx-20, justify="left", fg_color="transparent", master=tabview.tab("Stream"), font=("Arial", 12), text_color="gray70")
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=87, x=20)

def audioserversettings():
    dialog = customtkinter.CTkInputDialog(text="Audio server port:", title="Input Port")
    pinput = dialog.get_input()
    if pinput is not None:
        if pinput.isnumeric():
            if int(pinput) >= 0 and int(pinput) <= 65535:
                writeconfig("PORT", "audioport", int(pinput))
            else:
                err = thr.Thread(target=displayerror, args=("Port must be between 0 and 65535", 4))
                err.daemon = True
                err.start()
        else: 
            err = thr.Thread(target=displayerror, args=("Port must be numeric", 3))
            err.daemon = True
            err.start()
    

portentry = customtkinter.CTkButton(tabview.tab("Stream"), text="Set Server Port", command=audioserversettings)
portentry.place(anchor=customtkinter.E, rely=0, relx= 1, y=140, x=-20)
label = customtkinter.CTkLabel(text="Audio server port (0-65535)", fg_color="transparent", master=tabview.tab("Stream"), font = ("Arial", 16))
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=140, x=20)
longtext = 'Currently ' + str(AudioPort)
label = customtkinter.CTkLabel(text=longtext, wraplength=screenx-20, justify="left", fg_color="transparent", master=tabview.tab("Stream"), font=("Arial", 12), text_color="gray70")
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=167, x=20)





#-------------Bot Settings----------------

def changeBot():
    writeconfig("BOT", "enabled", int(botswitch.get() == 'True'))

botswitch_var = customtkinter.StringVar(value="off")
botswitch = customtkinter.CTkSwitch(master=tabview.tab("Bot"), text="", command=changeBot,
                                 variable=botswitch_var, onvalue="True", offvalue="False", width=0)
botswitch.place(anchor=customtkinter.E, rely=0, relx= 1, y=60, x=-20)

label = customtkinter.CTkLabel(text="Discord Bot", fg_color="transparent", master=tabview.tab("Bot"), font = ("Arial", 16))
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=60, x=20)
longtext = 'Enable or disable Discord bot integration'
label = customtkinter.CTkLabel(text=longtext, wraplength=screenx-20, justify="left", fg_color="transparent", master=tabview.tab("Bot"), font=("Arial", 12), text_color="gray70")
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=87, x=20)


npchentry = customtkinter.CTkEntry(master=tabview.tab("Bot"), placeholder_text="Channel ID")
npchentry.place(anchor=customtkinter.E, rely=0, relx= 1, y=140, x=-20)

label = customtkinter.CTkLabel(text='"Now Playing" Channel', fg_color="transparent", master=tabview.tab("Bot"), font = ("Arial", 16))
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=140, x=20)
longtext = 'The bot will send a message that displays what song is currently playing in the channel with this ID\nSet to 0 to not send any messages'
label = customtkinter.CTkLabel(text=longtext, wraplength=screenx-20, justify="left", fg_color="transparent", master=tabview.tab("Bot"), font=("Arial", 12), text_color="gray70")
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=167, x=20)

vcchentry = customtkinter.CTkEntry(master=tabview.tab("Bot"), placeholder_text="Voice ID")
vcchentry.place(anchor=customtkinter.E, rely=0, relx= 1, y=220, x=-20)

label = customtkinter.CTkLabel(text='Voice Channel', fg_color="transparent", master=tabview.tab("Bot"), font = ("Arial", 16))
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=220, x=20)
longtext = 'The channel ID the bot will connect and play music to\nSet to 0 to not play music in voice'
label = customtkinter.CTkLabel(text=longtext, wraplength=screenx-20, justify="left", fg_color="transparent", master=tabview.tab("Bot"), font=("Arial", 12), text_color="gray70")
label.place(anchor=customtkinter.W, rely=0, relx= 0, y=247, x=20)


def savebots():
    npinput = npchentry.get()
    if npinput is not None:
        if npinput.isnumeric():
            writeconfig("CHANNEL", "Nowplaychannel", int(npinput))
        else: 
            err = thr.Thread(target=displayerror, args=("Channel IDs must be numeric", 3))
            err.daemon = True
            err.start()
    else: writeconfig("CHANNEL", "Nowplaychannel", 0)

    vcinput = vcchentry.get()
    if vcinput is not None:
        if vcinput.isnumeric():
            writeconfig("VC", "VoiceChannel", int(vcinput))
        else: 
            err = thr.Thread(target=displayerror, args=("Channel IDs must be numeric", 3))
            err.daemon = True
            err.start()
    else: writeconfig("VC", "VoiceChannel", 0)


    settingschanged()

savebotsb =  customtkinter.CTkButton(tabview.tab("Bot"), text="Save", command=savebots)
savebotsb.place(anchor=customtkinter.SW, rely=1, relx= 0, y=0, x=0)
#------------------------------------------


try:
    stationName = str(readconfignwrite("NAME", "stationname", "My Station"))
    nameEntry.insert(0, stationName)
    app.title(stationName)
except:
    print("Could not read station name!")

try:
    npChannel = int(readconfignwrite("CHANNEL", "Nowplaychannel", 0))
    npchentry.insert(0, npChannel)
except:
    print("Could not read now playing channel ID!")

try:
    voiceChannel = int(readconfignwrite("VC", "VoiceChannel", 0))
    vcchentry.insert(0, voiceChannel)
except:
    print("Could not read voice channel ID!")

try:
    doend = bool(int(readconfignwrite("END", "Doend", 0)))
    if doend:
        endswitch.select()
    else:
        endswitch.deselect()
except:
    print("Could not read ending track setting!")


try:
    if readqueuetype == 1:
        radiobutton_1.select()
    else:
        radiobutton_2.select()
except:
    print("Invalid queue type! Was it read/stored incorrectly?")

try:
    jinglefrequency = int(readconfignwrite("JINGLE", "Jinglefreq", 2))
    jingleslider.set(jinglefrequency)
    jinglefreq.configure(text=jingleslider.get())
except:
    print("Could not read jingle frequency!")


try:
    dojingles = bool(int(readconfignwrite("BUILD", "jingles", 0)))
    if dojingles:
        switch.select()
        jingleslider.configure(state="normal", progress_color="steelblue1", button_color="#1F6AA5")
    else:
        switch.deselect()
        jingleslider.configure(state="disabled", progress_color="gray60", button_color="gray70")
        
except:
    print("Could not read queue type!")


try:
    botEnabled = bool(int(readconfignwrite("BOT", "enabled", 0)))
    if botEnabled:
        botswitch.select()
    else:
        botswitch.deselect()
except:
    print("Could not check if bot should be enabled!")


try:
    streamEnabled = bool(int(readconfignwrite("STREAM", "enabled", 1)))
    if streamEnabled:
        streamswitch.select()
    else:
        streamswitch.deselect()
except:
    print("Could not check if stream should be enabled!")

#-------------------------------------------------------

error = customtkinter.CTkLabel(app, text="", fg_color="transparent", text_color="red", font=("Arial",12))
error.pack(anchor=customtkinter.S, side=customtkinter.BOTTOM)

changesettings = customtkinter.CTkLabel(app, text="", fg_color="transparent", font=("Arial",12), justify ="center")
changesettings.place(anchor=customtkinter.S, rely=1, relx= 0.5, y=0, x=0)


tabview.configure(width=screenx, height=int(screeny-30))

#-------------------------------------------------------


music_path = "Music"
jingle_path = "Jingles"
end_path = "End"
masterlist = []
masterindex = 0
currentplay = ""
initialized =  False
buttons = []




def displayerror(text, hold):
    print(text)
    error.configure(text=str(text))
    time.sleep(hold)
    error.configure(text="")

def bumpgetindex(bump):
    global masterindex
    masterindex += bump
    if masterindex < -1:
        masterindex = -1
    return masterindex + bump

def list_audio_file_in_folder(folder_path):
    audio_files = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type and mime_type.startswith("audio/"):
                audio_files.append(str(file_path))
    return audio_files

def reshuffle():
    global masterindex
    global masterlist
    masterlist = []
    masterindex = 0
    jingles = list_audio_file_in_folder(jingle_path)
    prev = -1
    for index, file_name in enumerate(random.sample(os.listdir(music_path), len(os.listdir(music_path)))):
        file_path = os.path.join(music_path, file_name)
        if os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type and mime_type.startswith("audio/"):
                masterlist.append(file_path)
                if dojingles:
                    if (index - prev) >= jinglefrequency :
                        prev = index
                        randjing = random.choice(jingles)
                        masterlist.append(randjing)
    if doend:
        for file_name in os.listdir(end_path):
            file_path = os.path.join(end_path, file_name)
            if os.path.isfile(file_path):
                mime_type, _ = mimetypes.guess_type(file_path)
                if mime_type and mime_type.startswith("audio/"):
                    masterlist.append(file_path)
    


reshuffle()

def buildlist():

    if usetextbox:

        try:
            textbox.configure(state="normal")
            textbox.delete("0.0", "end")
            for index, item in enumerate(masterlist):
                if index == masterindex:
                    prefix = "--->      " + str(index) + ". "
                else:
                    prefix = '' + str(index) + ". "

                if "Jingles" in item:
                    textbox.insert("end", prefix + 'JINGLE' + "\n")
                else:
                    textbox.insert("end", prefix + str(os.path.splitext(item)[0]).replace("Music\\", '').replace("End\\", '') + "\n")       #"end", prefix + str(re.sub(r'\B([A-Z])', r' \1', str(os.path.splitext(item)[0]).replace('music_', '')).replace("_", " ").replace("Music\\", '').replace("End\\", '')) + "\n")
            textbox.configure(state="disabled")
        except: 
            print("Error building queue text, retrying...")
            displayerror("Error building queue text, retrying...", 4)
            buildlist()
    else:
        try:
            global buttons
            if buildlist.destroy:
                buildlist.destroy = False
                for index, button in enumerate(buttons):
                    setbutton(index)
            if buildlist.built == False:
                buildlist.built = True
                
                for index, item in enumerate(masterlist):
                    
                    if "Jingles" in item:
                        color = "gray18"
                        hovercolor = "gray28"
                    else:
                        color = "gray24"
                        hovercolor = "gray30"

                    buttons.append(customtkinter.CTkButton(master=queueframe, text=formatname(index, True), command=lambda i=index: gotoandplay(i), width=screenx, anchor=customtkinter.W, corner_radius=0, fg_color=color, hover_color=hovercolor))

                    buttons[index].pack(anchor=customtkinter.W)
                    setbutton.previousbutton = buttons[0]
                    setbutton.previousindex = 0
                    """
                    thisbutton = customtkinter.CTkButton(master=queueframe, text=formatname(index), command=lambda i=index: gotoandplay(i), width=32)
                    thisbutton.pack()
                    buttons.append(thisbutton)
                    """
                        
                        #textbox.insert("end", prefix + str(re.sub(r'\B([A-Z])', r' \1', str(os.path.splitext(item)[0]).replace('music_', '')).replace("_", " ").replace("Music\\", '')) + "\n")

            
        except:
            print("Error building queue, retrying...")
            displayerror("Error building queue, retrying...", 4)
            buildlist()
buildlist.built = False
buildlist.destroy = False

def formatname(index, arrow):
    global masterindex
    if arrow:
        if index == masterindex:
            prefix = "" + str(index) + ". "
        else:
            prefix = '' + str(index) + ". "
    else:
        prefix = ""

    if "Jingles" in masterlist[index]:
        return prefix + 'JINGLE'
    else:
        return prefix + str(str(os.path.splitext(masterlist[index])[0]).replace("Music\\", '').replace("End\\", ''))                #str(re.sub(r'\B([A-Z])', r' \1', str(os.path.splitext(masterlist[index])[0]).replace('music_', '')).replace("_", " ").replace("Music\\", '').replace("End\\", ''))

def setbutton(index):
    global buttons
    global masterlist


    if "Jingles" in masterlist[setbutton.previousindex]:
        color = "gray18"
    else:
        color = "gray24"

    setbutton.previousbutton.configure(text=str(formatname(setbutton.previousindex, True)), state="normal", fg_color=color)
    buttons[index].configure(text=str(formatname(index, True)), state="disabled", fg_color="gray40")
    setbutton.previousbutton = buttons[index]
    setbutton.previousindex = index
    

def gotoandplay(index):
        global masterindex
        masterindex = int(index) - 1
        playaudio()


mixer.init()

if not usetextbox:
    buildlist()

def QueryTrack():
    global currentplay
    global masterlist
    global masterindex
    query = []
    
    if currentplay != "JINGLE":
        query.append("Now playing:")
        query.append(currentplay)
    else:
        query.append("Intermission")
        query.append(stationName)
    
    
    query.append(round(mixer.Sound(masterlist[masterindex]).get_length() - (mixer.music.get_pos()/1000))+2)
    return query


def playaudio():
        global usetextbox
        global masterindex
        global currentplay
        try:
            if masterindex >= len(masterlist):
                buildlist.destroy = True
                reshuffle()
                buildlist()
                print('Reshuffled queue')
            if mixer.get_init:
                if masterindex == 0:
                    reverse.configure(state="disabled")
                else:
                    reverse.configure(state="normal")
                if masterindex >= len(masterlist) - 1:
                    skip.configure(state="disabled")
                else:
                    skip.configure(state="normal")
                

                mixer.music.load(masterlist[masterindex])
                mixer.music.play()
                currentplay = formatname(masterindex, False)
                if usetextbox:
                    buildlist()
                else:
                    setbutton(masterindex)
                if "Jingles" in masterlist[masterindex]:
                    nowplaying.configure(text="JINGLE")
                else:
                    nowplaying.configure(text=str(str(os.path.splitext(masterlist[masterindex])[0]).replace("Music\\", '').replace("End\\", '')))             #str(re.sub(r'\B([A-Z])', r' \1', str(os.path.splitext(masterlist[masterindex])[0]).replace('music_', '')).replace("_", " ").replace("Music\\", '').replace("End\\", ''))

        except: 
            print("Error playing audio, retrying...")
            displayerror("Error playing audio, retrying...", 4)
            if usetextbox:
                buildlist()
            else:
                setbutton(masterindex)
            

def startloop():
    global initialized
    time.sleep(0.2)
    if not initialized:
        t = thr.Thread(target=songloop)
        t.daemon = True
        t.start()
        c = thr.Thread(target=colorRotate)
        c.daemon = True
        c.start()

def songloop():
    global masterindex
    global initialized
    while True:
        try:
            if not mixer.music.get_busy():
                if not initialized:
                    initialized = True
                    playaudio()
                else:
                    bumpgetindex(1)
                    playaudio()
        except:
            print("Error in main loop")
            displayerror("Error in main loop", 4)
            break

def colorRotate():
        while True:
            try:
                for i in range(100):
                    hue = i / float(100)
                    rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.8)
                    hex_code = '#{:02x}{:02x}{:02x}'.format(
                    int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
                    nowplaying.configure(text_color=hex_code)
                    if not usetextbox:
                        buttons[masterindex].configure(text_color_disabled=hex_code)
                    time.sleep(0.1)
            except:
                print("Error in color loop")
                displayerror("Error in color loop", 4)
                break


temp = thr.Thread(target=startloop)
temp.daemon = True
temp.start()

def DiscordBot():
    global currentplay
    global mysong
    global masterlist
    global masterindex


    mysong = ''
    @client.event
    async def on_ready():
        print(f'Connected! {client.user}')
        if  npChannel != 0:
            invalid = False
            try:
                channel = client.get_channel(npChannel)
            except:
                print("Error getting now playing channel! Is the ID invalid?")
                invalid = True
            try:
                msgfile = open('lastmsg','r')
                message_id = msgfile.read()
            except:
                msgfile = open("lastmsg", 'w+')
                message_id = msgfile.read()
            try:
                lastmsg = await channel.fetch_message(message_id)
            except:
                print("Couldn't find message from file")
            try:     
                await lastmsg.delete()
            except:
                print("Could not delete message")
        await sendsong.start()

    @loop(seconds=1)
    async def sendsong():
        global mysong
        global vc
        global message
        invalid = False
        try:
            channel = client.get_channel(npChannel)
        except:
            print("Error getting now playing channel! Is the ID invalid?")
            invalid = True
        
        if mysong != currentplay:
                mysong = currentplay
                
                if voiceChannel != 0:
                    channel_id = voiceChannel
                    invalid = False
                    try:
                        voice_channel = client.get_channel(channel_id)  
                        voice = discord.utils.get(client.voice_clients, guild=voice_channel.guild)
                    except:
                        print("Error getting now voice channel! Is the ID invalid?")
                        invalid = True
                    if not invalid:
                        
                        if voice == None: 
                            try:
                                vc = await voice_channel.connect()
                                await voice_channel.guild.change_voice_state(channel=voice_channel, self_mute=False, self_deaf=True)
                            except:
                                print("Error joining voice")
                        if vc.is_playing:
                            try:
                                vc.pause()
                            except:
                                print("Error stopping voice music")
                    
                        try:
                            vc.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=masterlist[masterindex]))
                        except:
                            err = thr.Thread(target=displayerror, args=("Could not play music in voice. Ensure ffmpeg.exe is located in the root directory next to the program executable.", 10))
                            err.daemon = True
                            err.start()
                if currentplay != 'JINGLE':
                    formatted = currentplay
                    hue = random.randint(0, 100) / float(100)
                    rgb = colorsys.hsv_to_rgb(hue, 1.0, 0.8)
                    if  npChannel != 0 and not invalid:
                        MessageEmbed = discord.Embed(
                                            title="Now playing", 
                                            description="## " + formatted,
                                            color= discord.Color.from_rgb(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)))
                        MessageEmbed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))


                        try: await message.edit(embed=MessageEmbed)

                        except: 
                            message = await channel.send(embed=MessageEmbed)
                            file = open("lastmsg", 'w+')
                            file.write(str(message.id))
                    
                    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=formatted))
                else:
                    if  npChannel != 0 and not invalid:
                        MessageEmbed = discord.Embed(
                                            title="Intermission", 
                                            description="## " + stationName,
                                            color= 0x000000
                                            )
                        MessageEmbed.set_footer(text=datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

                        try: await message.edit(embed=MessageEmbed)

                        except: 
                            message = await channel.send(embed=MessageEmbed)
                            file = open("lastmsg", 'w+')
                            file.write(str(message.id))

                    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=stationName))

    

    try:
        t = open("token.txt", "r")
        
    except:
        t = open("token.txt", "a+")
        print('Place Discord bot token in token.txt')
        displayerror("Place Discord bot token in token.txt", 5)
    

    client.run(str(t.read()))

if botEnabled:
    bot = thr.Thread(target=DiscordBot)
    bot.daemon = True
    bot.start()


def AudioServer():
    deviceindex = sounddevice.query_devices(kind="input")["index"]
    global currentplay
    global AudioPort

    app = Flask(__name__)

    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    
    audio1 = pyaudio.PyAudio()
    
    def genHeader(sampleRate, bitsPerSample, channels):
        datasize = 2000*10**6
        o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
        o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
        o += bytes("WAVE",'ascii')                                              # (4byte) File type
        o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
        o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
        o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
        o += (channels).to_bytes(2,'little')                                    # (2byte)
        o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
        o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
        o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
        o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
        o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
        o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
        return o

    @app.route('/audio')
    def audio():
        def sound():

            CHUNK = 1024
            sampleRate = 44100
            bitsPerSample = 16
            channels = 2
            wav_header = genHeader(sampleRate, bitsPerSample, channels)

            stream = audio1.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,input_device_index=deviceindex,
                            frames_per_buffer=CHUNK)
            first_run = True
            while True:
                if first_run:
                    data = wav_header + stream.read(CHUNK)
                    first_run = False
                else:
                    data = stream.read(CHUNK)
                yield(data)

        return Response(sound(), mimetype="audio/wav")

    @app.route('/playing')
    def getplay():
        return QueryTrack()

    if __name__ == "__main__":
        from waitress import serve
        serve(app, host='0.0.0.0',port=AudioPort)

if streamEnabled:
    AudSr = thr.Thread(target=AudioServer)
    AudSr.daemon = True
    AudSr.start()




app.mainloop()





