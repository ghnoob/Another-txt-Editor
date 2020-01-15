"""Interface and commands regarding to edit the text."""

import tkinter as tk

class EditMenu:
    """The 'Edit' menu on the menu bar.
    
    Parameters:
        parent (main.MainApplication): an instance of the app
        menubar (tkinter.Menu): app's menubar
    """
    def __init__(self, parent, menubar):
        """Adds the edit menu to the menu bar.
        
        Parameters:
            parent (main.MainApplication): an instance of the app
            menubar (tkinter.Menu): app's menubar
        """
        self.parent = parent
        self.menubar = menubar

        editmenu = tk.Menu(self.menubar, tearoff=0)
        
        editmenu.add_command(
            label='Cut',
            command=lambda:self.parent.textbox.event_generate('<<Cut>>')
        )
        editmenu.add_command(
            label='Copy',
            command=lambda:self.parent.textbox.event_generate('<<Copy>>')
        )
        editmenu.add_command(
            label='Paste',
            command=lambda:self.parent.textbox.event_generate('<<Paste>>')
        )
        editmenu.add_separator()
        editmenu.add_command(
            label='Select all',
            command=lambda:self.parent.textbox.event_generate('<<SelectAll>>')
        )
        editmenu.add_command(
            label='Delete',
            command=lambda:self.parent.textbox.event_generate('<<Clear>>')
        )
        
        menubar.add_cascade(label='Edit', menu=editmenu)