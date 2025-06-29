import tkinter as tk
from tkinter import messagebox
import json
import os

class DarkTheme:
    # Dark color scheme
    BACKGROUND = "#2d2d2d"
    FOREGROUND = "#e0e0e0"
    ACCENT = "#3a7ebf"
    ENTRY_BG = "#3d3d3d"
    LISTBOX_BG = "#3d3d3d"
    LISTBOX_FG = "#e0e0e0"
    SELECTION = "#4a4a4a"
    BUTTON_ACTIVE = "#1f5b9e"
    WARNING = "#bf3a3a"

class LightTheme:
    # Light color scheme
    BACKGROUND = "#f0f0f0"
    FOREGROUND = "#333333"
    ACCENT = "#007bff"
    ENTRY_BG = "#ffffff"
    LISTBOX_BG = "#ffffff"
    LISTBOX_FG = "#333333"
    SELECTION = "#d0d0d0"
    BUTTON_ACTIVE = "#0056b3"
    WARNING = "#ff4d4d"s
    
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Peroxide To Do")
        self.root.geometry("480x420")
        self.theme = DarkTheme()
         
        self.theme = {DarkTheme, LightTheme}
        # Configure root window background
        self.root.configure(bg=self.theme.BACKGROUND)
        
        # Task list and data file
        self.tasks = []
        self.data_file = "todo_data.json"
        
        # Load existing tasks
        self.load_tasks()
        
        # Create container frame for all frames
        self.container = tk.Frame(self.root, bg=self.theme.BACKGROUND)
        self.container.pack(fill="both", expand=True)
        
        # Dictionary to hold all frames
        self.frames = {MenuFrame, TodoFrame, AboutFrame}
        
        # Create all frames
        for F in (MenuFrame, TodoFrame, AboutFrame):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Show the menu frame first
        self.show_frame(TodoFrame)
        
        # Bind window closing event to save tasks
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
        # Special setup for TodoFrame when shown
        if cont == TodoFrame:
            frame.update_listbox()
            

    
    def add_task(self, task_text):
        if task_text:
            self.tasks.append({"text": task_text, "completed": False})
            if TodoFrame in self.frames:
                self.frames[TodoFrame].update_listbox()
    
    def delete_task(self, index):
        try:
            del self.tasks[index]
            self.frames[TodoFrame].update_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")
    
    def clear_tasks(self):
        self.tasks = []
        self.frames[TodoFrame].update_listbox()
    
    def mark_complete(self, index):
        try:
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]
            self.frames[TodoFrame].update_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to mark.")
    
    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.tasks = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.tasks = []
    
    def save_tasks(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.tasks, f)
    
    def on_closing(self):
        self.save_tasks()
        self.root.destroy()

class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=controller.theme.BACKGROUND)
        self.controller = controller
        
        label = tk.Label(
            self, 
            text="Main Menu", 
            font=('Arial', 18), 
            bg=controller.theme.BACKGROUND,
            fg=controller.theme.FOREGROUND
        )
        label.pack(pady=20)
        
        # Button styling
        button_options = {
            'bg': controller.theme.ACCENT,
            'fg': controller.theme.FOREGROUND,
            'activebackground': controller.theme.BUTTON_ACTIVE,
            'activeforeground': controller.theme.FOREGROUND,
            'width': 20,
            'height': 2,
            'borderwidth': 0,
            'highlightthickness': 0
        }
        
        todo_btn = tk.Button(
            self, 
            text="To-Do List", 
            command=lambda: controller.show_frame(TodoFrame),
            **button_options
        )
        todo_btn.pack(pady=10)
        
        about_btn = tk.Button(
            self, 
            text="About", 
            command=lambda: controller.show_frame(AboutFrame),
            **button_options
        )
        about_btn.pack(pady=10)
        
        quit_btn = tk.Button(
            self, 
            text="Quit", 
            command=controller.on_closing,
            **button_options
        )
        quit_btn.pack(pady=10)

class TodoFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=controller.theme.BACKGROUND)
        self.controller = controller
        
        # Navigation frame
        nav_frame = tk.Frame(self, bg=controller.theme.BACKGROUND)
        nav_frame.pack(fill="x", pady=5)
        
        # Navigation button styling
        nav_button_options = {
            'bg': controller.theme.ACCENT,
            'fg': controller.theme.FOREGROUND,
            'activebackground': controller.theme.BUTTON_ACTIVE,
            'activeforeground': controller.theme.FOREGROUND,
            'borderwidth': 0,
            'highlightthickness': 0
        }
        
        menu_btn = tk.Button(
            nav_frame, 
            text="Menu", 
            command=lambda: controller.show_frame(MenuFrame),
            **nav_button_options
        )
        menu_btn.pack(side="left", padx=5)
        
        about_btn = tk.Button(
            nav_frame, 
            text="About", 
            command=lambda: controller.show_frame(AboutFrame),
            **nav_button_options
        )
        about_btn.pack(side="left", padx=5)
        
        # Task entry frame
        entry_frame = tk.Frame(self, bg=controller.theme.BACKGROUND)
        entry_frame.pack(pady=10)
        
        self.task_entry = tk.Entry(
            entry_frame, 
            width=30, 
            font=('Arial', 12),
            bg=controller.theme.ENTRY_BG,
            fg=controller.theme.FOREGROUND,
            insertbackground=controller.theme.FOREGROUND,
            borderwidth=0,
            highlightthickness=0
        )
        self.task_entry.pack(side="left", padx=5)
        self.task_entry.bind("<Return>", lambda event: self.add_task_handler())
        
        add_button = tk.Button(
            entry_frame, 
            text="Add Task", 
            command=self.add_task_handler,
            **nav_button_options
        )
        add_button.pack(side="left")
        
        # Task list frame
        list_frame = tk.Frame(self, bg=controller.theme.BACKGROUND)
        list_frame.pack(pady=10, fill="both", expand=True)
        
        self.task_listbox = tk.Listbox(
            list_frame, 
            width=50, 
            height=15, 
            font=('Arial', 12),
            selectmode=tk.SINGLE,
            bg=controller.theme.LISTBOX_BG,
            fg=controller.theme.LISTBOX_FG,
            selectbackground=controller.theme.SELECTION,
            selectforeground=controller.theme.FOREGROUND,
            borderwidth=0,
            highlightthickness=0
        )
        self.task_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(
            list_frame,
            bg=controller.theme.BACKGROUND,
            troughcolor=controller.theme.BACKGROUND,
            activebackground=controller.theme.ACCENT
        )
        scrollbar.pack(side="right", fill="y")
        
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Button frame
        button_frame = tk.Frame(self, bg=controller.theme.BACKGROUND)
        button_frame.pack(pady=10)
        
        # Action button styling
        action_button_options = {
            'bg': controller.theme.ACCENT,
            'fg': controller.theme.FOREGROUND,
            'activebackground': controller.theme.BUTTON_ACTIVE,
            'activeforeground': controller.theme.FOREGROUND,
            'borderwidth': 0,
            'highlightthickness': 0
        }
        
        delete_button = tk.Button(
            button_frame, 
            text="Delete Selected", 
            command=self.delete_task_handler,
            **action_button_options
        )
        delete_button.pack(side="left", padx=5)
        
        clear_button = tk.Button(
            button_frame, 
            text="Clear All", 
            command=self.clear_tasks_handler,
            **action_button_options
        )
        clear_button.pack(side="left", padx=5)
        
        complete_button = tk.Button(
            button_frame,
            text="Mark Complete",
            command=self.mark_complete_handler,
            **action_button_options
        )
        complete_button.pack(side="left", padx=5)
    
    def add_task_handler(self):
        task = self.task_entry.get()
        if task:
            self.controller.add_task(task)
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")
    
    def delete_task_handler(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.controller.delete_task(selected_index)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")
    
    def clear_tasks_handler(self):
        self.controller.clear_tasks()
    
    def mark_complete_handler(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.controller.mark_complete(selected_index)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to mark.")
    
    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.controller.tasks:
            prefix = "[✓] " if task["completed"] else "[ ] "
            self.task_listbox.insert(tk.END, prefix + task["text"])

class AboutFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=controller.theme.BACKGROUND)
        self.controller = controller
        
        # Navigation frame
        nav_frame = tk.Frame(self, bg=controller.theme.BACKGROUND)
        nav_frame.pack(fill="x", pady=5)
        
        # Navigation button styling
        nav_button_options = {
            'bg': controller.theme.ACCENT,
            'fg': controller.theme.FOREGROUND,
            'activebackground': controller.theme.BUTTON_ACTIVE,
            'activeforeground': controller.theme.FOREGROUND,
            'borderwidth': 0,
            'highlightthickness': 0
        }
        
        menu_btn = tk.Button(
            nav_frame, 
            text="Menu", 
            command=lambda: controller.show_frame(MenuFrame),
            **nav_button_options
        )
        menu_btn.pack(side="left", padx=5)
        
        todo_btn = tk.Button(
            nav_frame, 
            text="To-Do List", 
            command=lambda: controller.show_frame(TodoFrame),
            **nav_button_options
        )
        todo_btn.pack(side="left", padx=5)
        
        # About content
        content_frame = tk.Frame(self, bg=controller.theme.BACKGROUND)
        content_frame.pack(pady=20)
        
        about_label = tk.Label(
            content_frame, 
            text="Peroxide To Do\n\nVersion 0.1.2\n\nCreated by P4ndA",
            font=('Arial', 14),
            justify="center",
            bg=controller.theme.BACKGROUND,
            fg=controller.theme.FOREGROUND
        )
        about_label.pack()

class SettingsFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=controller.theme.BACKGROUND)
        self.controller = controller
        
        nav_frame = tk.Frame(self, bg=controller.theme.BACKGROUND)
        nav_frame.pack(fill="x", pady=5)
        
        nav_button_options = {
            'bg': controller.theme.ACCENT,
            'fg': controller.theme.FOREGROUND,
            'activebackground': controller.theme.BUTTON_ACTIVE,
            'activeforeground': controller.theme.FOREGROUND,
            'borderwidth': 0,
            'highlightthickness': 0
        }
        
        label = tk.Label(
            self, 
            text="Settings", 
            font=('Arial', 18), 
            bg=controller.theme.BACKGROUND,
            fg=controller.theme.FOREGROUND
        )
        label.pack(pady=20)
        
        # Add settings options here in the future
        # For now, just a placeholder
        
        theme_btn = tk.Button(
            self,
            nav_frame, 
            text="Change Theme", 
            command=lambda: controller.show_frame(MenuFrame),
            **nav_button_options
        )
        
        placeholder_label = tk.Label(
            self, 
            text="Settings will be available soon.",
            bg=controller.theme.BACKGROUND,
            fg=controller.theme.FOREGROUND
        )
        placeholder_label.pack(pady=10)
        
        
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()