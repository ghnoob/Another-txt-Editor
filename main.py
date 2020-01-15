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

        # detects key presses inside the text display and calls a method
        # that checks if the text has changed.
        self.textbox.bind('<Key>', self.detect_text_changes)
        self.textbox.bind('<KeyRelease>', self.detect_text_changes)
        
        self.textbox.pack(fill='both', expand=1)

    # events
    def detect_text_changes(self, event):
        """Detects if the text has changed.
        
        When the key detection is on, it is called when we press a key.    
        When it detects that the text has changes, deactivates key
        detection.  
        """
        # compares the text before and after the key press
        if self.text != self.textbox.get(1.0,'end-1c'):
            self.ismodified = True
            self.configure_title() # updates the title
            self.textbox.unbind(self.detect_text_changes)
            # deactivates key detection

    def reset(self):    
        """Resets the variable that controls if the text was modified,
        the title of the app in the window manager and activtes the
        key detection."""
        self.ismodified = False
        self.configure_title()
        self.textbox.bind('<Key>', self.detect_text_changes)
        self.textbox.bind('<KeyRelease>', self.detect_text_changes)

# runs the app
if __name__ == '__main__':
    root = tk.Tk()
    main_app = MainApplication(root)
    root.mainloop()