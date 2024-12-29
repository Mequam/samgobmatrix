from command import Command

#represents a set of commands
class CommandSet:
    def __init__(self):
        self.commands : dict(Command) = {}
