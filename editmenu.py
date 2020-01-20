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

        self.create_menu_buttons()
        self.grey_out()
        self.parent.textbox.bind('<<Selection>>', lambda event:self.grey_out())

    def create_menu_buttons(self):
        """Creates the menu buttons for the edit menu."""
        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        
        self.editmenu.add_command(
            label='Undo', accelerator='Ctrl+Z',
            command=lambda: self.parent.textbox.event_generate('<<Undo>>')
        )
        self.editmenu.add_command(
            label='Redo', accelerator='Ctrl+Y',
        command=lambda: self.parent.textbox.event_generate('<<Redo>>')
        )
        self.editmenu.add_separator()
        self.editmenu.add_command(
            label='Cut', accelerator='Ctrl+X',
            command=lambda:self.parent.textbox.event_generate('<<Cut>>')
        )
        self.editmenu.add_command(
            label='Copy', accelerator='Ctrl+C',
            command=lambda:self.parent.textbox.event_generate('<<Copy>>')
        )
        self.editmenu.add_command(
            label='Paste', accelerator='Ctrl+V',
            command=lambda:self.parent.textbox.event_generate('<<Paste>>')
        )
        self.editmenu.add_separator()
        self.editmenu.add_command(
            label='Select all', accelerator='Ctrl+A',
            command=lambda:self.parent.textbox.event_generate('<<SelectAll>>')
        )
        self.editmenu.add_command(
            label='Delete', accelerator='Del',
            command=lambda:self.parent.textbox.event_generate('<<Clear>>')
        )
        
        self.menubar.add_cascade(label='Edit', menu=self.editmenu)

    def grey_out(self):
        """Disables cut, copy, and delete buttons if there is not text selected."""
        entries = [3, 4, 8]
        
        if self.parent.textbox.tag_ranges('sel'):
            state = 'normal'
        else:
            state = 'disabled'
        
        for entry in entries: 
            self.editmenu.entryconfig(entry, state=state)