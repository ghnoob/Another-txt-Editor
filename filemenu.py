import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from functools import partial

# decorator
def save_changes(function):
    """Decorator function.
    
    When we want to close a file that has changed without saving it,
    a popup ask us if we want to save our work.
    """
    def wrapper(self):
        if self.parent.path == '':
            path = 'New file'
        else:
            path = self.parent.path
            
        if self.parent.ismodified:
            s = tkinter.messagebox.askyesnocancel(
                title='Unsaved changes',
                message=f'Do you want to save the changes made in\n"{path}"?'
            )
            if s:
                self.save_file()
            elif s is None:
                return
        function(self)
        self.parent.reset()
    return wrapper

class FileMenu:
    def __init__(self, parent, menubar=None):
        self.parent = parent
        self.menubar = menubar

        filemenu = tk.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label='New file', command=self.new_file)
        filemenu.add_command(label='Open file', command=self.open_file)
        filemenu.add_command(label='Save file', command=self.save_file)
        filemenu.add_command(label='Save file as...',command=self.save_file_as)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.exit)
        menubar.add_cascade(label='File', menu=filemenu)

        # if we close the app with the window manager, calls to the
        # app's custom exit method
        self.parent.master.protocol('WM_DELETE_WINDOW', self.exit)

    @save_changes
    def new_file(self):
        """Creates a new text file."""
        self.parent.text = ''
        self.parent.path = ''
        self.parent.textbox.delete(1.0, 'end')
        self.parent.reset()

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
            self.openpath = path
            self.open_file_2()

    @save_changes
    def open_file_2(self):
            # opens the specified file
            self.parent.path = self.openpath
            file_ = open(self.parent.path, 'r')
            self.parent.text = file_.read() # stores the text if the file
            # to the one in the opened file
            file_.close()
            # updates the text display
            self.parent.textbox.delete(1.0, 'end')
            self.parent.textbox.insert(1.0, self.parent.text)

    def save_file(self):
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
            self.parent.reset() # activates key detection
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
            self.parent.reset() # activates key detection
            self.parent.path = path # stores the path of the file
            # stores the text
            self.parent.text = self.parent.textbox.get(1.0, 'end-1c')
            # saves the file
            fichero = open(self.parent.path, 'w')
            fichero.write(self.parent.text)
            fichero.close()

    @save_changes
    def exit(self):
        """Closes the app."""
        self.parent.master.quit()