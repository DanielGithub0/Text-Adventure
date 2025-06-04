import tkinter as tk
from PIL import Image, ImageTk as ImageTK
from tkinter import ttk

"""class tkinterApp:
    def __init__(self, root, height=540, width=960):
        self.root = root
        self.root.geometry(f"{width}x{height}")  # Set the size of the window
        self.root.title("tkinter test window")

        icon = ImageTK.PhotoImage(Image.open("c:/Users/darkd/Documents/GitHub REPOS/Text-Adventure/testing/githubLogo.jpg"))
        self.root.iconphoto(True, icon)

        self.root.config(bg="#001373")

        self.create_widgets()

    def create_widgets(self):
        WelcomeLabel = ttk.Label(self.root, 
                                 text="Welcome to the tkinter test window", 
                                 background="#001373", 
                                 foreground="white", 
                                 font=("Arial", 24),
                                 relief="raised",
                                 padding=20)
        WelcomeLabel.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = tkinterApp(root)
    root.mainloop()  # Place the window on the screen, listen for events and respond to them
    """
class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("Test Application")

        # creating a frame and assigning it to container
        container = tk.Frame(self, height=540, width=960)
        # specifying the region where the frame is packed in root
        container.pack(side="top", fill="both", expand=True)

        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # We will now create a dictionary of frames
        self.frames = {}
        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in (MainPage, SidePage, CompletionScreen):
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Using a method to switch frames
        self.show_frame(MainPage)
            
    def show_frame(self, cont):
        frame = self.frames[cont]
        #raises the current frame to the top
        frame.tkraise()
        
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Main Page", font=("Arial", 24))
        text = tk.Label(self, text="This is the main page of the application. You can navigate to other pages from here.")
        label.pack(pady=10, padx=10)
        text.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Go to Side Page",
                            command=lambda: controller.show_frame(SidePage))
        button2 = ttk.Button(self, text="Go to Completion Screen",
                            command=lambda: controller.show_frame(CompletionScreen))
        button2.pack()
        button.pack()
    
class SidePage(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Side Page", font=("Arial", 24))
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Go to Completion Screen",
                            command=lambda: controller.show_frame(CompletionScreen))
        button.pack()
    
class CompletionScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Completion Screen", font=("Arial", 24))
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Go to Main Page",
                            command=lambda: controller.show_frame(MainPage))
        button.pack()
        
if __name__ == "__main__":
    app = windows()
    app.mainloop()  # Start the application
