from tkinter import ttk
import tkinter as tk

THEMES = {
    'light': {
        'primary': '#1976D2',
        'secondary': '#424242',
        'success': '#43A047',
        'warning': '#FFA000',
        'error': '#D32F2F',
        'background': '#FFFFFF',
        'surface': '#F5F5F5',
        'text': '#212121',
        'text_secondary': '#757575',
        'button_text': '#000000',  # White text for buttons
        'button_hover': '#1565C0'  # Darker blue for hover
    },
    'dark': {
        'primary': '#90CAF9',
        'secondary': '#B0BEC5',
        'success': '#81C784',
        'warning': '#FFB74D',
        'error': '#E57373',
        'background': '#303030',
        'surface': '#424242',
        'text': '#FFFFFF',
        'text_secondary': '#B0BEC5',
        'button_text': '#000000',  # Black text for buttons
        'button_hover': '#82B1FF'  # Lighter blue for hover
    },
    'ocean': {
        'primary': '#006064',      # Deep cyan
        'secondary': '#00838F',    # Dark cyan
        'success': '#00695C',      # Dark teal
        'warning': '#FF8F00',      # Dark amber
        'error': '#D32F2F',        # Red
        'background': '#E0F7FA',   # Light cyan
        'surface': '#B2EBF2',      # Lighter cyan
        'text': '#006064',         # Deep cyan
        'text_secondary': '#00838F',
        'button_text': '#000000',  # White text for buttons
        'button_hover': '#00838F'  # Darker cyan for hover
    },
    'nature': {
        'primary': '#2E7D32',      # Dark green
        'secondary': '#388E3C',    # Green
        'success': '#1B5E20',      # Darker green
        'warning': '#F57F17',      # Dark yellow
        'error': '#C62828',        # Dark red
        'background': '#F1F8E9',   # Light green
        'surface': '#DCEDC8',      # Lighter green
        'text': '#33691E',         # Darker green
        'text_secondary': '#558B2F',
        'button_text': '#000000',  # White text for buttons
        'button_hover': '#388E3C'  # Lighter green for hover
    },
    'sunset': {
        'primary': '#D84315',      # Deep orange
        'secondary': '#FF5722',    # Orange
        'success': '#FF7043',      # Light orange
        'warning': '#FFB300',      # Amber
        'error': '#D32F2F',        # Red
        'background': '#FBE9E7',   # Light orange
        'surface': '#FFCCBC',      # Lighter orange
        'text': '#BF360C',         # Dark orange
        'text_secondary': '#D84315',
        'button_text': '#000000',  # White text for buttons
        'button_hover': '#FF5722'  # Orange for hover
    }
}

class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style(root)

    def apply_theme(self, theme_name='light'):
        if theme_name not in THEMES:
            theme_name = 'light'
        
        colors = THEMES[theme_name]
        
        # Configure basic styles
        self.style.configure('.',
            background=colors['background'],
            foreground=colors['text'],
            font=('Segoe UI', 10)
        )

        # Button styles with explicit text colors
        button_styles = {
            'TButton': colors['primary'],
            'Primary.TButton': colors['primary'],
            'Secondary.TButton': colors['secondary'],
            'Success.TButton': colors['success']
        }

        # Apply button styles
        for style_name, color in button_styles.items():
            self.style.configure(style_name,
                background=color,
                foreground=colors['button_text'],
                font=('Segoe UI', 10, 'bold'),
                padding=(10, 5)
            )
            
            # Add hover effect
            self.style.map(style_name,
                background=[('active', colors['button_hover'])],
                foreground=[('active', colors['button_text'])]
            )

        # Configure labels with theme colors
        self.style.configure('TLabel',
            background=colors['background'],
            foreground=colors['text'],
            font=('Segoe UI', 10)
        )

        self.style.configure('Header.TLabel',
            background=colors['background'],
            foreground=colors['primary'],
            font=('Segoe UI', 14, 'bold')
        )

        # Configure Treeview colors
        self.style.configure('Treeview',
            background=colors['surface'],
            fieldbackground=colors['surface'],
            foreground=colors['text'],
            font=('Segoe UI', 10)
        )

        self.style.configure('Treeview.Heading',
            background=colors['primary'],
            foreground=colors['button_text'],
            font=('Segoe UI', 10, 'bold')
        )

        # Configure Frames
        self.style.configure('TFrame',
            background=colors['background']
        )

        self.style.configure('TLabelframe',
            background=colors['background']
        )

        self.style.configure('TLabelframe.Label',
            background=colors['background'],
            foreground=colors['text'],
            font=('Segoe UI', 10, 'bold')
        )

        # Update root window
        self.root.configure(bg=colors['background'])

        # Update text widgets
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Text):
                widget.configure(
                    background=colors['surface'],
                    foreground=colors['text'],
                    font=('Segoe UI', 10),
                    insertbackground=colors['text']  # Cursor color
                )

        return self.style, colors

def apply_style(root):
    theme_manager = ThemeManager(root)
    return theme_manager.apply_theme()
