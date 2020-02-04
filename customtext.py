"""Code by Bryan Oakley on StackOverflow
https://stackoverflow.com/questions/23571407/how-to-i-have-the-call-back-in-tkinter-when-i-change-the-current-insert-position
"""
import tkinter as tk

class CustomText(tk.Text):
    """A custom text widget.

    Raises an event when text or text cursor position change. Ideal for
    making a status bar.
    """
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "delete") or 
            args[0:3] == ("mark", "set", "insert")):
            self.event_generate("<<CursorChange>>", when="tail")

        return result