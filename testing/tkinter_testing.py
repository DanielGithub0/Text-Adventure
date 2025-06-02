import tkinter as tk #import the tkinter module
from PIL import Image, ImageTk as ImageTK #import the PIL module for image handling

window = tk.Tk() #initialise the window
window.geometry("960x540") #set the size of the window
window.title("tkinter test window") #set the title of the window

icon = ImageTK .PhotoImage(Image.open("c:/Users/darkd/Documents/GitHub REPOS/Text-Adventure/testing/githubLogo.jpg")) #load the icon image
window.iconphoto(True, icon) #set the icon of the window

window.config(bg = "#001373")

WelcomeLabel = tk.Label(window, 
                     text="Welcome to the tkinter test window", 
                     bg="#001373", 
                     fg="white", 
                     font=("Arial", 24),
                     relief="raised",
                     bd=8,
                     padx=20,
                     pady=20) #create a label with the text "Welcome to the tkinter test window"
WelcomeLabel.pack()

window.mainloop() #place the window on the screen, listen for events and respond to them

