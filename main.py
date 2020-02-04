"""Another txt Editor Copyright 2020 Rodrigo Pietnechuk.

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
along with Another txt Editor.  If not, see <https://www.gnu.org/licenses/>."""

import tkinter as tk
import tkinter.ttk as ttk

from customtext import CustomText
from filemenu import FileMenu
from editmenu import EditMenu
from configmenu import ConfigMenu
from helpmenu import HelpMenu

# UI
class MainApplication:
    """Main window of the app.
    
    Arguments:
        master (tkinter.Tk): root widget of the app.

    Attributes:
        path (str): stores the path of the file we are editing.
        text (str): stores the text of the file we open before editing
        it to compare it to the text after editing.
        ismodified (bool): True if the text file was modified
    """

    def __init__(self, master):
        """Calls methods that create and configure the widgets.
        
        Arguments:
            master (tkinter.Tk): the root widget if the app.

        Attributes:
            path (str): stores the path of the file we are editing.
            text (str): stores the text of the file we open before editing
            it to compare it to the text after editing.
        """
        # arguments
        self.master = master

        # attributes
        self.path = ''
        self.text = ''

        # call methods
        self.create_widgets()
        self.configure_title()

    def configure_title(self, *args):
        """Configures the app title in the window manager.
        
        It shows the app name with the path to the file we are editing
        if there is. Else, it shows 'New file'.
        If the text file is changed, it adds an asterisk (*) to the path.
        """
        if self.path == '':
            path = 'New file'
        else:
            path = self.path
        
        if self.textbox.edit_modified():
            mod = ' *'
        else:
            mod = ''
        
        self.master.title(f"{path}{mod} - Another txt Editor")
    
    def create_widgets(self):
        """Calls the methods that create the widgets of the app."""
        self.create_textbox()
        self.create_statusbar()
        self.create_menu()

    def create_menu(self):
        """Creates the upper menu."""
        self.menubar = tk.Menu(self.master)
        FileMenu(self)
        EditMenu(self)
        ConfigMenu(self)
        HelpMenu(self)

        # add the menu to the root widget
        self.master.config(menu=self.menubar)

    def create_textbox(self):
        """Creates the text display and scroll bars."""
        textframe = tk.Frame()

        self.textbox = CustomText(textframe, pady=5, padx=5, undo=True)

        yscrollbar = tk.Scrollbar(textframe, command=self.textbox.yview)
        # this bar will be added to the grid only if wrapping is inactive
        # see editmenu.EditMenu.set_scrollbar()
        self.xscrollbar = tk.Scrollbar(textframe, orient='horizontal',
                                       command=self.textbox.xview)

        self.textbox.config(yscrollcommand=yscrollbar.set,
                            xscrollcommand=self.xscrollbar.set)
        
        # changes the title when the text is modified
        self.textbox.bind('<<Modified>>', self.on_modification)
        # adds a separator to the undo stack if the user presses space
        self.textbox.bind('<space>', lambda event:self.textbox.edit_separator())

        # updates the status bar
        self.textbox.bind('<<CursorChange>>', lambda event: self.set_ln_col())
        
        # managing geometry
        self.textbox.grid(row=0, column=0, sticky='nsew')
        yscrollbar.grid(row=0, column=1, sticky='ns')
        textframe.grid_rowconfigure(0, weight=1)
        textframe.grid_columnconfigure(0, weight=1)

        textframe.pack(fill='both', expand=1)

        self.textbox.focus_set() # sets the focus

    def create_statusbar(self):
        """Crates a status bar that indicates text cursor position."""
        self.status_frame = ttk.Frame()

        self.line = tk.IntVar(self.master)
        self.column = tk.IntVar(self.master)
        
        ttk.Label(self.status_frame, text='Ln: ').pack(side='left')
        self.lnlabel = ttk.Label(self.status_frame, textvariable=self.line)
        self.lnlabel.pack(side='left')
        ttk.Label(self.status_frame, text='    Col: ').pack(side='left')
        self.collabel = ttk.Label(self.status_frame, textvariable=self.column)
        self.collabel.pack(side='left')

        self.set_ln_col() # updates de bar once is created

    def set_ln_col(self):
        """Updates the status bar values."""
        ln, col = self.textbox.index('insert').split('.')
        self.line.set(ln)
        self.column.set(col)

    def on_modification(self, event):
        """Called when the text display modified flag changes.
        
        If the flag is False, clears the undo stack so the user can't
        undo an action made in a file after opening another.
        Also updates the window title, to show an asterisk if the flag
        is True or not if it is False
        """
        if self.textbox.edit_modified() == 0:
            self.textbox.edit_reset()
        self.configure_title()
    
    def reset(self):
        """Called when a new file is opened.
        
        Sets the flag that that signals that the text was modified to
        False.
        """
        self.textbox.edit_modified(False)

# runs the app
if __name__ == '__main__':
    root = tk.Tk()
    main_app = MainApplication(root)
    root.mainloop()