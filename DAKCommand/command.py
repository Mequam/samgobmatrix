from argparse import ArgumentParser
import inspect

class Command:
    """
    represents a command that the user can run,
    
    can contain subcommands for more complex tree based processing
    """
    def __init__(self,name : str,**kwargs):
        #the name of this command, and also the command used to run it from cli
        self.name : str = name

        #arg parse argument parser used to generate the help page and parse commands in leaf commands
        self.parser : ArgumentParser = ArgumentParser(prog=name,**kwargs)

        #really boring command that does nothing
        self.default_cmd = None

        #this is the function that is called from parse to actually run operations and make
        #do work
        self.runner = lambda x : x
        
        """
        commands are parsed as a tree structure using this dictionary,
        subcommands are stored here and run based on the string passed into them, they
        in turn run commands from there children until we get to a leaf command that will parse the
        arguments outright and return the result
        """
        self.sub_commands : dict = {}
    

    
    def is_sub_command(self)->bool:
        """
        returns true if we are a sub command
        """
        return len(self.sub_commands) == 0

    
    def help_str(self)->str:
        """return the help string for this command"""
        if self.is_sub_command():
            return self.parser.format_help()
        
        #format sub commands to be a new line deliminated list for viewing
        return "valid commands are \n " + \
                "\n".join(str(list(self.sub_commands.keys()))[1:-1].split(","))
    
    def show_help(self)->None:
        print(self.help_str())
    
    def parse_help_information(self,args : [str])->bool:
        """
        simple routine to parse out and display help pages
        returns true if it ran for use in further processing
        """
        cmd = args[0]

        if cmd == 'help':
            if len(args) >= 2 and args[1] in self.sub_commands:
                self.sub_commands[args[1]].parse_help_information(['help'] + args[2:])
            else:
                self.show_help()
            return True
        return False
    

    def call_from_namespace(self,f,namespace)->None:
        """
        calls a given function from an argparse namespace via
        python function magic :)
        """
        spec = inspect.getfullargspec(f)
        var_namespace = vars(namespace)

        standard_args = [ var_namespace[arg] for arg in var_namespace if arg in spec.args]
        if spec.varargs:
            standard_args += var_namespace[spec.varargs]

        keyword_args = {name : var_namespace[name] for name in var_namespace if name in spec.kwonlyargs}
    
        f(*standard_args,**keyword_args)



    def parse(self,args : [str])->None:
        if self.is_sub_command():
            #actually do work
            self.call_from_namespace(self.runner, self.parser.parse_args(args))

            return

        if self.parse_help_information(args):
            #if we parse out help information we do no further
            #processing
            return

        if len(args) > 0:
            if args[0] in self.sub_commands:
                self.sub_commands[args[0]].parse(args[1:])
            elif self.default_cmd:
                self.default_cmd.parse(args)
        else:
            self.default_cmd.parse(args)


    #convinience function to add a sub command to the tree
    def add_sub_command(self,sub_command : 'Command',*,default = False)->None:
        self.sub_commands[sub_command.name] = sub_command
        if default:
            self.default_cmd = sub_command

    def function_decorator(self,*,name : str = None, default : bool = False,dashList : bool = False):
        """
        decorator used to create and add a command as a sub command to this one
        """

        def decorator(f):
            self.add_sub_command(Command.from_function(f),
                                 default=default)

            return f

        return decorator

    @staticmethod
    def from_function(f : callable,*,name : str = None, dashList : bool = False,**kwargs)->"Command":
        """
        takes a function and returns a command object that parses and sends values to the given function
        """
        spec = inspect.getfullargspec(f)

        ret_val = Command(name = name if name else f.__name__ , **kwargs)


        default_arguments = []
        non_default_arguments = []
        
        #seperate out default and non default arguments
        if spec.defaults:
            default_arguments = zip(spec.args[-len( spec.defaults ):],
                                        spec.defaults)
            non_default_arguments = spec.args[:-len(spec.defaults)]
        else:
            non_default_arguments = spec.args

#standard args
        for arg in non_default_arguments:
            ret_val.parser.add_argument(
                                        arg,
                                        type=spec.annotations[arg] if arg in spec.annotations else None
                                        )
#default args
        for arg,default in default_arguments:
            ret_val.parser.add_argument(f'--{arg}',nargs='?',default=default,
                                        type=spec.annotations[arg] if arg in spec.annotations else None
                                        )
#keyword arguments
        for arg in spec.kwonlyargs:
            if arg in spec.kwonlydefaults:
                ret_val.parser.add_argument(f'--{arg}',nargs='?',default=spec.kwonlydefaults[arg],
                                            type=spec.annotations[arg] if arg in spec.annotations else None
                                        )
            else:
                ret_val.parser.add_argument(f'--{arg}',nargs='?',
                                            type=spec.annotations[arg] if arg in spec.annotations else None
                                        )

        if spec.varargs:
            varname = spec.varargs
            if dashList:
                varname = f'--{spec.varargs}'
            ret_val.parser.add_argument(varname,
                                        type=spec.annotations[spec.varargs] if spec.varargs in spec.annotations else list,
                                        nargs="*"
                                        )


        ret_val.runner = f
        return ret_val

if __name__ == '__main__':

    commandTree = Command("commandTree")
    
    @commandTree.function_decorator()
    def test(a,b,c,*args : str,key=None,**kwargs):
        print(f'aaaay {a}')
        print(f'beeeee {b}')
        print(f'seeeee {c}')
        print(args)


        if key:
            print(f"the key is {key}")
        
        print(kwargs)
    
    commandTree.parse(input('()> ').split(' '))
