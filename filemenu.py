"""Interface and commands regarding to mofication of the text files."""

import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog

# decorator
def save_changes(function):
    """Asks the user to save their unsaved changes in a text document."""
    def wrapper(self, *args):
        if self.parent.path == '':
            path = 'New file'
        else:
            path = self.parent.path
            
        if self.parent.textbox.edit_modified():
            s = tkinter.messagebox.askyesnocancel(
                title='Unsaved changes',
                message=f'Do you want to save the changes made in\n"{path}"?'
            )
            if s:
                self.save_file()
            # if the user press cancel stops the rest of the execution
            elif s is None:
                return
        function(self)
        self.parent.textbox.edit_modified(False)
    return wrapper

class FileMenu:
    """File menu elements and functions.
    
    Arguments:
        parent (main.MainApplication): an instance of the app
        menubar: (tk.Menu): the app's menubar
    """
    def __init__(self, parent, menubar=None):
        """Calls methods that create the menu buttons and binds key
        shorcuts to them.
        
        Arguments:
            parent (main.MainApplication): an instance of the app
            menubar: (tk.Menu): the app's menubar
        """
        self.parent = parent
        self.menubar = menubar
        self.create_ui()
        self.key_shortcuts()

    def create_ui(self):
        """Creates the file menu buttons."""
        filemenu = tk.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label='New file',
                             accelerator='Ctrl+N', command=self.new_file)
        filemenu.add_command(label='Open file...',
                             accelerator='Ctrl+O', command=self.open_file)
        filemenu.add_command(label='Save file',
                             accelerator='Ctrl+S', command=self.save_file)
        filemenu.add_command(label='Save file as...',
                             accelerator='Ctrl+Shift+S', command=self.save_file_as)
        filemenu.add_separator()
        filemenu.add_command(label='Exit',
                             accelerator='Alt+F4', command=self.exit)
        self.menubar.add_cascade(label='File', menu=filemenu)

    def key_shortcuts(self):
        """Adds key bindings to the file menu buttons."""
        self.parent.master.bind('<Control-n>', self.new_file)
        self.parent.master.bind('<Control-N>', self.new_file)
        self.parent.master.bind('<Control-o>', self.open_file)
        self.parent.master.bind('<Control-O>', self.open_file)
        self.parent.master.bind('<Control-s>', self.save_file)
        self.parent.master.bind('<Control-S>', self.save_file)
        self.parent.master.bind('<Control-Shift-s>', self.save_file_as)
        self.parent.master.bind('<Control-Shift-S>', self.save_file_as)
        self.parent.master.bind('<Alt-F4>', self.exit)
        # if we close the app with the window manager, calls to the
        # app's custom exit method
        self.parent.master.protocol('WM_DELETE_WINDOW', self.exit)

    # menu commands
    @save_changes
    def new_file(self):
        """Creates a new text file."""
        self.parent.text = ''
        self.parent.path = ''
        self.parent.textbox.delete(1.0, 'end')

    def open_file(self, *args):
        """Asks the user to a file location, to open that file."""
        # opens the save window
        path = tk.filedialog.askopenfilename(
            title='Open file...', filetypes=(
                ('Plain text file', '*.txt'),
            )
        )

        # this runs only if the user didn't press 'cancel'
        if path != '':
            self.openpath = path
            self.open_file_2()

    @save_changes
    def open_file_2(self):
        """Opens the selected file."""
        self.parent.path = self.openpath
        file_ = open(self.parent.path, 'r')
        self.parent.text = file_.read() # stores the text of the file
        file_.close()
        # updates the text display
        self.parent.textbox.delete(1.0, 'end')
        self.parent.textbox.insert(1.0, self.parent.text)

    def save_file(self, *args):
        """Saves the file if there is a specified location for it.
        
        If there is not, it calls the method save_file_as(), that ask
        the user for a localtion to save the file.
        """
        if self.parent.path != '':
            # stores the test
            self.parent.text = self.parent.textbox.get(1.0, 'end-1c')
            # saves the file
            file_ = open(self.parent.path, 'w')
            file_.write(self.parent.text)
            file_.close()
            self.parent.textbox.edit_modified(False)
        else:
            self.save_file_as()

    def save_file_as(self, *args):
        """Saves the file in a path specified by the user."""
        path = tk.filedialog.asksaveasfilename(
            title='Save file as...',
            filetypes=( ('Plain text file', '*.txt'),),
            defaultextension='*.txt', initialfile='New text file'       
        )
        # runs only if we don't press 'cancel'
        if path != '':
            self.parent.path = path # stores the path of the file
            # stores the text
            self.parent.text = self.parent.textbox.get(1.0, 'end-1c')
            # saves the file
            file_ = open(self.parent.path, 'w')
            file_.write(self.parent.text)
            file_.close()
            self.parent.textbox.edit_modified(False)

    @save_changes
    def exit(self):
        """Closes the app."""
        self.parent.master.quit()