"""Based on an answer on StackOverflow by Walle Cyril.

https://stackoverflow.com/questions/7402516/tkinter-case-insensitive-bind

In tkinter, key bindings are case insensitive. That means that binding
's' will only work if the user presses the S key with caps lock
deactivated or while pressing shift.

To solve this we have to bind both uppercase and lowercase letters to
the widget, but that makes the code repetitive.

This module attempts to simplyfi the code by binding both uppercase and
lowercase keys in one function.
"""

def bind_(widget, modifier, key, callback):
    """Makes binding a key to a widget a lot easier.

    Binds both uppercase and lowercase keys.
    
    Arguments:
        widget (tkinter): a tkinter widget
        modifier (str): a modifier key - Control, Shift, Alt, etc.
        key (str): a letter key
        callback (function): a function associated with the letter key
    """
    modifier += '-'

    widget.bind(f'<{modifier}{key.lower()}>', callback)
    widget.bind(f'<{modifier}{key.upper()}>', callback)