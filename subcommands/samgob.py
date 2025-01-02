from samgob import DiceSetParser
from samgob.errors import ParseError
from samgob.iterators.control_flow_iterator import ControlFlowIterator
from DAKCommand import Command

class SamgobSubCommand(Command):
    def __init__(self,name,dice_parser,**kwargs):
        super().__init__(name,**kwargs)


        self.dice_parser = dice_parser

        @self.function_command(raw=True,default=True)
        def parse(args : [str]):
            try:
                
                ret_val = self.dice_parser.compile_langauge(ControlFlowIterator(
                    iter(args)
                    )
                )
                print(ret_val)
            except ParseError:
                print(f"unrecognized query or command, try help to get more information")
            
        
        @self.function_command()
        def variables():
            print("variables")
            print(len("variables")*'-')
            for key in self.dice_parser.variable_map:
                print(f"{key}:{str(self.dice_parser.variable_map[key])}")
            print(len("variables")*'-')
