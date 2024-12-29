from command import Command

class Prompt:
    """
    this class represents a command prompt that the user can type into and add information too
    you can overload 
    """
    def __init__(self):
        self.commands : [Command] = []

    def command(**kwargs): #creates and registers a command from a function
        def decorator(f):
            pass


