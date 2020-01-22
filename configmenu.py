"""Interface and commands regarding to the configuration of the app."""

import tkinter as tk
import tkinter.font
import tkinter.colorchooser as ColorChooser
import configparser
import tkfontchooser

def save_cfg(function):
    """Decorator function.
    
    Calls a function that makes changes in the UI and saves the user
    preferences in a .cfg file.

    Arguments:
        function (function): function to be decorated
    """
    def wrapper(self, *args):
        """Inside function of the decorator.

        Arguments:
            self (ConfigMenu): the instance of the class we are running. 
        """
        function(self, *args)
        with open('config.cfg', 'w') as configfile:
            self.config.write(configfile)
    return wrapper


def pick_color(function):
    """Decorator function.
    
    Opens a color selection window and then passes that color as an
    argument to another function.
    """
    def wrapper(self, *args):
        """Inside function of the decorator.
        
        Arguments:
            self (ConfigMenu): the instance of the class we are running.
        """
        x = ColorChooser.askcolor()
        if x == (None, None):
            return
        return function(self, x[1])
    return wrapper

class ConfigMenu:
    """'Config' menu GUI elements and functionalities.
    
    Arguments:
        parent (main.MainApplication): an instance of the app
    """
    def __init__(self, parent):
        """Creates the config menu.
        
        Arguments:
            parent (main.MainApplication): an instance of the app.
        """
        self.parent = parent
    
        self.load_config()
        self.create_gui()
    
    def create_gui(self):
        """Creates the config menu GUI elements."""
        configmenu = tk.Menu(self.parent.menubar, tearoff=False)

        radiobuttons = {'Do not wrap the text': 'none',
                        'Wrap characters': 'char',
                        'Wrap words': 'word'}
        
        for key, value in radiobuttons.items():
            configmenu.add_radiobutton(label=key, variable=self.wrapping,
                                       value=value, command=self.set_wrapping)

        configmenu.add_separator()
        configmenu.add_command(label='Change font...',
                               command=self.change_font)
        configmenu.add_command(label='Change font color...',
                               command=self.set_font_color)
        configmenu.add_separator()
        configmenu.add_command(label='Change background color...',
                               command=self.set_background)

        self.parent.menubar.add_cascade(label='Config', menu=configmenu)    

    def load_config(self):
        """Loads the cfg file and configs the UI accordingly.
        
        If there is not a cfg file, it uses deafault values.
        """
        self.config = configparser.ConfigParser()
        self.config.read('config.cfg')
        
        sections = ['Background', 'Wrapping', 'Font']
        
        for s in sections:
            if self.config.has_section(s) is False:
                self.config.add_section(s)

        self.wrapping = tk.StringVar(value=self.config['Wrapping'].get('wrap', 'none'))

        tkfont = tk.font.Font(
            self.parent.master,
            family=self.config['Font'].get('family', 'Consolas'),
            size=self.config.getint('Font', 'size', fallback=12),
            weight=self.config['Font'].get('weight', 'normal'),
            slant=self.config['Font'].get('slant', 'roman'),
            underline=self.config.getboolean('Font', 'underline', fallback=0),
            overstrike=self.config.getboolean('Font', 'overstrike', fallback=0)
        )

        self.parent.textbox.config(
            bg=self.config['Background'].get('bg', 'white'),
            fg=self.config['Font'].get('color', 'black'), font=tkfont,
            wrap=self.wrapping.get()
        )
    
    @save_cfg
    def set_wrapping(self):
        """Changes the text wrapping."""
        self.parent.textbox.config(wrap=self.wrapping.get())
        self.config['Wrapping']['wrap'] = self.wrapping.get()

    @save_cfg
    def change_font(self):
        font = tkfontchooser.askfont(self.parent.master)
        if font:
            tkfont = tk.font.Font(
                self.parent.master, family=font['family'], size=font['size'],
                weight=font['weight'], slant=font['slant'],
                underline=font['underline'], overstrike=font['overstrike']
            )
            self.parent.textbox.config(font=tkfont)

            for key, value in font.items():
                self.config['Font'][str(key)] = str(value)
    
    @pick_color
    @save_cfg
    def set_font_color(self, color):
        """Changes the font and insert cursor color.
        
        Arguments:
            color (str): hexadecimal color code
        """
        self.parent.textbox.config(fg=color, insertbackground=color)
        self.config['Font']['color'] = color
    
    @pick_color
    @save_cfg
    def set_background(self, color):
        """Changes the text display color.
        
        Arguments:
            color (str): hexadecimal color code.
        """
        self.parent.textbox.config(bg=color)
        self.config['Background']['bg'] = color