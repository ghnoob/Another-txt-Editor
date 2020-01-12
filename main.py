import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext
import tkinter.filedialog
import tkinter.messagebox

# globals
app_name = 'Another text editor'

# decorator
def save_changes(function):
    """Decorator function.
    
    When we want to close a file that has changed without saving it,
    a popup ask us if we want to save our work.
    """
    def wrapper(self):
        if self.path == '':
            path = 'New file'
        else:
            path = self.path
            
        if self.ismodified:
            s = tk.messagebox.askyesnocancel(
                title='Unsaved changes',
                message=f'Do you want to save the changes made in\n"{path}"?'
            )
            if s:
                self.save()
            elif s is None:
                return
        function(self)
        self.reset()
    return wrapper


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

        # if we close the app with the window manager, calls to the
        # app's custom exit method
        self.master.protocol('WM_DELETE_WINDOW', self.exit)

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

        # file menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='New file', command=self.new_file)
        filemenu.add_command(label='Open file', command=self.open_file)
        filemenu.add_command(label='Save file', command=self.save_file)
        filemenu.add_command(label='Save file as...',command=self.save_file_as)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.exit)
        menubar.add_cascade(label='File', menu=filemenu)

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
        
        self.textbox.pack(fill='both', expand=1)

    # file menu functions   
    @save_changes
    def new_file(self):
        """Creates a new text file."""
        self.text = '' # clears the text display 
        self.path = '' # resets the path
        self.textbox.delete(1.0, 'end')

    def open_file(self):
        """Opens the selected text file.

        If we were working with other text file, and we didn't save it,
        the program ask us to save the file."""
        # opens the save window
        path = tk.filedialog.askopenfilename(
            title='Open file', filetypes=(
                ('Plain text file', '*.txt'),
            )
        )

        # this runs only if the user didn't press 'cancel'
        if path != '':
            self.path = path
            self.open_file_2()

    @save_changes
    def open_file_2(self):
            # opens the specified file
            file_ = open(self.path, 'r')
            self.text = file_.read() # stores the text if the file
            # to the one in the opened file
            file_.close()
            # updates the text display
            self.textbox.delete(1.0, 'end')
            self.textbox.insert(1.0, self.text)

    def save_file(self):
        """Saves the file if there is a specified location for it.
        
        If there is not, it calls the method save_file_as(), that ask
        the user for a localtion to save the file.
        """
        if self.path != '':
            # stores the test
            self.text = self.textbox.get(1.0, 'end-1c')
            # saves the file
            file_ = open(self.path, 'w')
            file_.write(self.text)
            file_.close()
            self.reset() # activates key detection
        else:
            self.save_file_as()

    def save_file_as(self):
        """Saves the file in a path specified by the user."""
        path = tk.filedialog.asksaveasfilename(
            title='Save file as',
            filetypes=( ('Plain text file', '*.txt'),),
            defaultextension='*.txt', initialfile='New text file'       
        )
        # runs only if we don't press 'cancel'
        if path != '':
            self.path = path # stores the path of the file
            # stores the text
            self.text = self.textbox.get(1.0, 'end-1c')
            # saves the file
            fichero = open(self.path, 'w')
            fichero.write(self.text)
            fichero.close()
            self.reset() # activates key detection

    @save_changes
    def exit(self):
        """Closes the app."""
        self.master.quit()

    # events
    def detect_text_changes(self, event):
        """Detects if the text has changed.
        
        When the key detection is on, it is called when we press a key.    
        When it detects that the text has changes, deactivates key
        detection.  
        """
        # compares the text before and after the key press
        if self.text != self.textbox.get(1.0,'end'):
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

# runs the app
if __name__ == '__main__':
    root = tk.Tk()
    main_app = MainApplication(root)
    root.mainloop()