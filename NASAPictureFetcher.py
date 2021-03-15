#!/usr/bin/env python3

# Kameron Hartman
# c0755285
# Assignment 01 Part 02
# 2021-03-17
#
# This program uses the APOD NASA API to fetch NASA pictures and show them in the browser. Alongside this it had additional functionality which enables you to choose between HD and non HD as well as view the description of the image along with its title.
#
# Author Reflection:
# If I were to do this again with less restrictions I would like to render the image within the application as the assignment specifically requested that it be shown in browser.
# From https://apod.nasa.gov/apod/archivepix.html & https://apod.nasa.gov/apod/archivepixFull.html it can be seen that it goes from today through June 16, 1995

# Imports
import urllib.request
import json
import webbrowser
from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
import datetime
from datetime import timedelta

# Defining Astronomy Picture of the Day (APOD)
apod_api_url = 'https://api.nasa.gov/planetary/apod?'
apod_key = 'api_key=' # Generated API key

# Variables to store dates for reference
startDate = datetime.date(1995, 6, 16)# The farthest date from which images can be retrieved.
currentDate = datetime.date.today()# The current date
selectedDate = datetime.date(1995, 6, 16)# A default date which will be assigned when the application is launched.
daysSinceStart = currentDate - startDate# A calculation assigned to the variable to get the days since the image could be retrieved to be used as a limiter for the slider for date retrieval.

window = Tk()# Creates window using tkinter
window.title("NASA Image Fetcher") # Sets title of window
window.resizable(False, False) # Prevents window resizing

lbl = Label(window, text=f"{selectedDate}") # Creates and sets label default text
lbl.grid(column=0, row=0)# Grid geometry manager

chk_state = BooleanVar() # Creates a boolean variable as chk_state
chk_state.set(True) #set check state

chk = Checkbutton(window, text='HD', var=chk_state) # Creates and sets a checkbox for the HD field, the checkbox being linked to the chk_state variable.
chk.grid(column=0, row=3)# Grid geometry manager

infoOutput = scrolledtext.ScrolledText(window,width=50,height=10) # Creates scrolledtext for the output of the image explanation.
infoOutput.grid(column=0,row=2)# Grid geometry manager
infoOutput.config(wrap=WORD)# Makes the words wrap for easy reading.
infoOutput.configure(state ='disabled') # Prevents typing into the scrolled text

def setSelectedDate(daysSelected):
    """

    Sets the selectedDate variable & the label for date to the date selected from the scroll bar using the amount of days to add as input from the base start date specified as the date of the first image on the NASA API.

    Parameters
    ----------

    daysSelected
        The number of days since startDate
    """
    global selectedDate # Enabling access to selectedDate
    selectedDate = startDate + timedelta(days=int(float(daysSelected))) # Adds the input variable to the start date
    lbl.configure(text=f"{selectedDate}") # Sets label text to the selected date


dateSlider = Scale(window, from_=0, to=daysSinceStart.days, orient=HORIZONTAL, command=setSelectedDate)
dateSlider.grid(column=0, row=1)# Grid geometry manager

def loadImageAndInfo():
    """

    Uses the APOD api to get the image requested from the specified date by the date slider.
    This function also sets the title of the window to the title of the image,
    the scrolled text output will be filled with an explanation of the image,
    and the label will show the date, and image title.
    
    """
    # Request from the url combined with the key to attempt to get an object with all the information.
    apod_url_obj = urllib.request.urlopen(f"{apod_api_url}{apod_key}&date={selectedDate}")

    # Read the object and convert it to a string
    read_string = apod_url_obj.read()

    # Decode the string from JSON to python data structure
    decoded_string = json.loads(read_string.decode('utf-8'))

    print(decoded_string) # Debugging, display information
    
    lbl.configure(text=f"{selectedDate} : {decoded_string['title']}") # the label will show the date, and image title.
    window.title(decoded_string['title']) # the title of the window will become the title of the image.
    infoOutput.configure(state ='normal') # enables editing of the scrolledtext
    infoOutput.delete(1.0, END) # wipes scrolledtext
    infoOutput.insert(INSERT, decoded_string['explanation'])# Puts information about the image into the scrolled text.
    infoOutput.configure(state ='disabled')# disables editing of the scrolledtext
    
    if (chk_state.get() == False):# If not HD
        webbrowser.open(decoded_string['url']) # Opens image in browser
    elif (chk_state.get() == True): # If HD 
        webbrowser.open(decoded_string['hdurl']) # Opens HD image in browser

btn = Button(window, text="Open Image", command=loadImageAndInfo) # Creation of the Open Image button, is linked to the loadImageAndInfo function which will execute when clicked.
btn.grid(column=0, row=4)# Grid geometry manager

window.mainloop()
