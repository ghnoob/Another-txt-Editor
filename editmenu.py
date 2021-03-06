"""Interface and commands regarding to edit the text.

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

class EditMenu:
    """'Edit' menu graphic elements and functionalities.
    
    Arguments:
        main (main.MainApplication): an instance of the main class
    """
    def __init__(self, main):
        """Adds the edit menu to the menu bar.
        
        Arguments:
            main (main.MainApplication): an instance of the main class
        """
        self.main = main

        self.create_menu_buttons()
        self.grey_out()
        self.main.textbox.bind('<<Selection>>', lambda event:self.grey_out())

    def create_menu_buttons(self):
        """Creates the menu buttons for the edit menu."""
        self.editmenu = tk.Menu(self.main.menubar, tearoff=0)
        
        self.editmenu.add_command(
            label='Undo', accelerator='Ctrl+Z',
            command=lambda: self.main.textbox.event_generate('<<Undo>>')
        )
        self.editmenu.add_command(
            label='Redo', accelerator='Ctrl+Y',
        command=lambda: self.main.textbox.event_generate('<<Redo>>')
        )
        self.editmenu.add_separator()
        self.editmenu.add_command(
            label='Cut', accelerator='Ctrl+X',
            command=lambda:self.main.textbox.event_generate('<<Cut>>')
        )
        self.editmenu.add_command(
            label='Copy', accelerator='Ctrl+C',
            command=lambda:self.main.textbox.event_generate('<<Copy>>')
        )
        self.editmenu.add_command(
            label='Paste', accelerator='Ctrl+V',
            command=lambda:self.main.textbox.event_generate('<<Paste>>')
        )
        self.editmenu.add_separator()
        self.editmenu.add_command(
            label='Select all', accelerator='Ctrl+A',
            command=lambda:self.main.textbox.event_generate('<<SelectAll>>')
        )
        self.editmenu.add_command(
            label='Delete', accelerator='Del',
            command=lambda:self.main.textbox.event_generate('<<Clear>>')
        )
        
        self.main.menubar.add_cascade(label='Edit', menu=self.editmenu)

        # contextual menu
        self.main.textbox.bind(
            '<Button-3>',
            lambda event: self.editmenu.post(event.x_root, event.y_root)
        )
        self.main.textbox.bind(
            '<App>', lambda event: self.editmenu.post(
                self.main.master.winfo_rootx(), self.main.master.winfo_rooty()
            )
        )

    def grey_out(self):
        """Disables cut, copy, and delete buttons if there is not text selected."""
        entries = [3, 4, 8]
        
        if self.main.textbox.tag_ranges('sel'):
            state = 'normal'
        else:
            state = 'disabled'
        
        for entry in entries: 
            self.editmenu.entryconfig(entry, state=state)