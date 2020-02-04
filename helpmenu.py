"""Interface and commands regarding to viewing info about the app.

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
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import os.path
import webbrowser

class HelpMenu:
    """'Help' menu elements'.
    
    Arguments:
        main (main.MainApplication): an instance of the main class
    """
    def __init__(self, main):
        """Creates the menu buttons.
        
        Arguments:
            main (main.MainApplication): an instance of the main class
        """
        self.main = main
        
        # paths and urls
        issues_url = 'https://github.com/ghnoob/Another-txt-Editor/issues/new'
        readme_path = 'file://' + os.path.abspath('README.html')
        license_url = 'https://www.gnu.org/licenses/gpl-3.0-standalone.html'
        source_url = 'https://github.com/ghnoob/Another-txt-Editor'
        dev_url = 'https://github.com/ghnoob'
        
        # menu buttons
        helpmenu = tk.Menu(self.main.master, tearoff=0)
        helpmenu.add_command(label='About...', command=self.show_about_box)
        helpmenu.add_separator()
        helpmenu.add_command(
            label = 'Report a bug',
            command = lambda: webbrowser.open_new_tab(issues_url)
        )
        helpmenu.add_separator()
        helpmenu.add_command(
            label = 'Open readme file',
            command = lambda: webbrowser.open_new_tab(readme_path)
        )
        helpmenu.add_command(
            label = 'View license',
            command = lambda: webbrowser.open_new_tab(license_url)
        )
        helpmenu.add_separator()
        helpmenu.add_command(
            label = 'View source code',
            command = lambda: webbrowser.open_new_tab(source_url)
        )
        helpmenu.add_command(
            label = "Visit author's GitHub profile",
            command = lambda: webbrowser.open_new_tab(dev_url)
        )
        self.main.menubar.add_cascade(label='Help', menu=helpmenu)

    def show_about_box(self):
        """Shows an about box with copyright info."""
        msgbox.showinfo(title='About', message='''\
Another txt Editor © 2020 Rodrigo Pietnechuk.

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version
3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program.
If not, see <https://www.gnu.org/licenses/>
'''
                        )