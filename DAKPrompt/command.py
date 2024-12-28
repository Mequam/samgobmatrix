from argparse import ArgumentParser
import inspect

class Command:
    """
    represents a command that the user can run
    """
    def __init__(self,**kwargs):
        self.parser = ArgumentParser(**kwargs)
        self.sub_commands : dict = {}
    
    def is_sub_command()->bool:
        return len(self.sub_commands) == 0


    @staticmethod
    def from_function(f : callable,*,dashList = False,**kwargs)->"Command":
        """
        takes a function and returns a command object that parses and sends values to the given function
        """
        spec = inspect.getfullargspec(f)

        print(spec)
        
        ret_val = Command(prog=f.__name__,**kwargs)


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
            if arg in spec.annotations:
                print(spec.annotations[arg])
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

        return ret_val

if __name__ == '__main__':
    def test(*args : str):
        print(args)
    
    c = Command.from_function(test)
    x = c.parser.parse_args(input('test ').split(' '))
    print(x)




