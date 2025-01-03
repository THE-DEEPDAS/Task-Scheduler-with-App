import tkinter as tk
from tkinter import ttk
from .style import apply_style

class TutorialPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.style, self.colors = apply_style(self)
        self.create_tutorial_content()

    def create_tutorial_content(self):
        # Main container with padding
        main_container = ttk.Frame(self, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header section
        header = ttk.Label(
            main_container,
            text="Welcome to the Tutorial",
            style="Header.TLabel"
        )
        header.pack(pady=(0, 20))

        # Buttons section
        self.create_button_section(main_container)
        
        # Labels section
        self.create_label_section(main_container)
        
        # Cards section
        self.create_card_section(main_container)

    def create_button_section(self, parent):
        # Buttons showcase
        button_frame = ttk.LabelFrame(
            parent,
            text="Button Styles",
            padding="10"
        )
        button_frame.pack(fill=tk.X, pady=(0, 20))

        # Primary button
        ttk.Label(
            button_frame,
            text="Primary Button:",
            style="Body.TLabel"
        ).pack(anchor=tk.W)
        ttk.Button(
            button_frame,
            text="Primary Action",
            style="Primary.TButton"
        ).pack(pady=(5, 10))

        # Secondary button
        ttk.Label(
            button_frame,
            text="Secondary Button:",
            style="Body.TLabel"
        ).pack(anchor=tk.W)
        ttk.Button(
            button_frame,
            text="Secondary Action",
            style="Secondary.TButton"
        ).pack(pady=(5, 10))

        # Success button
        ttk.Label(
            button_frame,
            text="Success Button:",
            style="Body.TLabel"
        ).pack(anchor=tk.W)
        ttk.Button(
            button_frame,
            text="Success Action",
            style="Success.TButton"
        ).pack(pady=(5, 10))

    def create_label_section(self, parent):
        # Labels showcase
        label_frame = ttk.LabelFrame(
            parent,
            text="Label Styles",
            padding="10"
        )
        label_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(
            label_frame,
            text="Header Label Example",
            style="Header.TLabel"
        ).pack(anchor=tk.W, pady=5)

        ttk.Label(
            label_frame,
            text="Body Label Example - This is how regular text appears",
            style="Body.TLabel"
        ).pack(anchor=tk.W, pady=5)

    def create_card_section(self, parent):
        # Cards showcase
        card_frame = ttk.LabelFrame(
            parent,
            text="Card Examples",
            padding="10"
        )
        card_frame.pack(fill=tk.X)

        # Example card
        card = ttk.Frame(
            card_frame,
            style="Card.TFrame",
            padding="10"
        )
        card.pack(fill=tk.X, pady=10)

        ttk.Label(
            card,
            text="Card Title",
            style="Header.TLabel"
        ).pack(anchor=tk.W)

        ttk.Label(
            card,
            text="This is an example of how content looks inside a card component.",
            style="Body.TLabel"
        ).pack(anchor=tk.W, pady=(5, 0))

        ttk.Button(
            card,
            text="Card Action",
            style="Primary.TButton"
        ).pack(pady=(10, 0))
