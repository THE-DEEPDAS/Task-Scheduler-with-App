from tkinter import ttk

def apply_style(root):
    style = ttk.Style()
    
    # Configure common styles
    style.configure("TButton",
                   padding=6,
                   relief="flat",
                   background="#2196f3",
                   foreground="black")
    
    style.configure("TLabel",
                   padding=5,
                   font=("Helvetica", 10))
    
    style.configure("TEntry",
                   padding=5)
    
    # Configure frame styles
    style.configure("TFrame",
                   background="white")
    
    return style
