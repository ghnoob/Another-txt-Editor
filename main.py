import tkinter as tk
import tkinter.scrolledtext
from filemenu import FileMenu
from editmenu import EditMenu

# globals
app_name = 'Another text editor'

# UI
class MainApplication:
    """Main window of the app.
    
    Parameters:
        master (tkinter,Tk): root widget of the app.

    Attributes:
        path (str): stores the path of the file we are editing.
        text (str): stores the text of the file we open before editing
        it to compare it to the text after editing.
        ismodified (bool): True if the text file was modified
    """

    def __init__(self, master):
        """Calls methods that create and configure the widgets.
        
        Parameters:
            master (tkinter.Tk): the root widget if the app.

        Attributes:
            path (str): stores the path of the file we are editing.
            text (str): stores the text of the file we open before editing
            it to compare it to the text after editing.
            ismodified (bool): True if the text file was modified
        """
        # arguments
        self.master = master

        # attributes
        self.path = ''
        self.text = ''
        self.ismodified = False

        # call methods
        self.configure_widgets()
        self.create_widgets()

    def configure_widgets(self):
        """General configuration of the widgets."""
        self.configure_title()

    def configure_title(self):
        """Configures the app title in the window manager.
        
        It shows the app name with the path to the file we are editing
        if there is. Else, it shows 'New file'.
        If the text file is changed, it adds an asterisk (*) to the path.
        """
        if self.path == '':
            path = 'New file'
        else:
            path = self.path
        
        if self.ismodified:
            mod = ' *'
        else:
            mod = ''
        
        self.master.title(f"{path}{mod} - {app_name}")
    
    def create_widgets(self):
        """Calls the methods that create the widgets of the app."""
        self.create_menu()
        self.create_textbox()

    def create_menu(self):
        """Creates the upper menu."""
        menubar = tk.Menu(self.master)
        FileMenu(self, menubar)
        EditMenu(self, menubar)

        # add the menu to the root widget
        self.master.config(menu=menubar)

    def create_textbox(self):
        """Creates the text display"""
        
        self.textbox = tk.scrolledtext.ScrolledText(
            self.master, font=('Consolas', 12), pady=5, padx=5
        )

        # detects if the text was modified
        self.textbox.bind('<<Modified>>', self.on_modification)
        
        self.textbox.pack(fill='both', expand=1)

    # events
    def on_modification(self, event):
        """Called if the contents of the text widget are modified.

        Sets a flag that signals that the text was modified to True and
        adds an asterisk (*) to thr file name in the window title to
        notify that to the user. 
        """
        self.ismodified = True
        self.configure_title() # updates the title

    def reset(self):    
        """Called when a new file is opened.
        
        Sets the flag that that signals that the text was modified to
        False and deleted the asterisk (*) in the window title if there
        is one, to notify the user that the text is unchanged.
        """
        self.ismodified = False
        self.configure_title()

# runs the app
if __name__ == '__main__':
    root = tk.Tk()
    main_app = MainApplication(root)
    root.mainloop()