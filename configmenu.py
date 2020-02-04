"""Interface and commands regarding to the configuration of the app.

This file is part of Another txt Editor.

Another txt Editor is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Another txt Editor is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Another txt Editor.  If not, see <https://www.gnu.org/licenses/>.
"""

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
        main (main.MainApplication): an instance of the main class
    """
    def __init__(self, main):
        """Creates the config menu.
        
        Arguments:
            main (main.MainApplication): an instance of the main class.
        """
        self.main = main
    
        self.load_config()
        self.create_gui()
    
    def create_gui(self):
        """Creates the config menu GUI elements."""
        configmenu = tk.Menu(self.main.menubar, tearoff=False)

        configmenu.add_checkbutton(
            label='Show status bar', variable=self.show_status_bar,
            command=self.set_statusbar
        )
        configmenu.add_separator()

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

        self.main.menubar.add_cascade(label='Config', menu=configmenu)    

    def load_config(self):
        """Loads the cfg file and configs the UI accordingly.
        
        If there is not a cfg file, it uses deafault values.
        """
        self.config = configparser.ConfigParser()
        self.config.read('config.cfg')
        
        sections = ['Background', 'View', 'Font']
        
        for s in sections:
            if self.config.has_section(s) is False:
                self.config.add_section(s)

        self.show_status_bar = tk.BooleanVar(
            self.main.master, value=self.config.getboolean(
                'View', 'show_status_bar', fallback=1
            )
        )
        self.wrapping = tk.StringVar(value=self.config['View'].get('wrap', 'none'))

        tkfont = tk.font.Font(
            self.main.master,
            family=self.config['Font'].get('family', 'Consolas'),
            size=self.config.getint('Font', 'size', fallback=12),
            weight=self.config['Font'].get('weight', 'normal'),
            slant=self.config['Font'].get('slant', 'roman'),
            underline=self.config.getboolean('Font', 'underline', fallback=0),
            overstrike=self.config.getboolean('Font', 'overstrike', fallback=0)
        )

        self.main.textbox.config(
            bg=self.config['Background'].get('bg', 'white'),
            fg=self.config['Font'].get('color', 'black'),
            insertbackground=self.config['Font'].get('color', 'black'),
            font=tkfont, wrap=self.wrapping.get()
        )

        self.set_scrollbar()
        self.set_statusbar()

    def set_scrollbar(self):
        """Controls the horizontal scrollbar of the text display.
        
        It hides the scrollbar if the text wrapping is activated and
        shows it if wrapping is not activated.
        """
        if self.wrapping.get() == 'none':
            self.main.xscrollbar.grid(row=1, column=0, sticky='ew')
        else:
            self.main.xscrollbar.grid_forget()

    @save_cfg
    def set_statusbar(self):
        """Shows the statusbar if the option to show it is on.
        
        Else, it hides it.
        """
        self.config['View']['show_status_bar'] = str(self.show_status_bar.get())
        
        if self.show_status_bar.get():
            self.main.status_frame.pack(fill='x')
        else:
            self.main.status_frame.pack_forget()
    
    @save_cfg
    def set_wrapping(self):
        """Changes the text wrapping."""
        self.main.textbox.config(wrap=self.wrapping.get())
        self.config['View']['wrap'] = self.wrapping.get()
        self.set_scrollbar()

    @save_cfg
    def change_font(self):
        font = tkfontchooser.askfont(self.main.master)
        if font:
            tkfont = tk.font.Font(
                self.main.master, family=font['family'], size=font['size'],
                weight=font['weight'], slant=font['slant'],
                underline=font['underline'], overstrike=font['overstrike']
            )
            self.main.textbox.config(font=tkfont)

            for key, value in font.items():
                self.config['Font'][str(key)] = str(value)
    
    @pick_color
    @save_cfg
    def set_font_color(self, color):
        """Changes the font and insert cursor color.
        
        Arguments:
            color (str): hexadecimal color code
        """
        self.main.textbox.config(fg=color, insertbackground=color)
        self.config['Font']['color'] = color
    
    @pick_color
    @save_cfg
    def set_background(self, color):
        """Changes the text display color.
        
        Arguments:
            color (str): hexadecimal color code.
        """
        self.main.textbox.config(bg=color)
        self.config['Background']['bg'] = color