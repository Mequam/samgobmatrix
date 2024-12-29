from samgob import DiceSetParser
from samgob.iterators.control_flow_iterator import ControlFlowIterator
from DAKCommand import Command

class SamgobSubCommand(Command):
    def __init__(self,name,**kwargs):
        super().__init__(name,**kwargs)


        self.dice_parser = DiceSetParser()

        @self.function_decorator(default=True)
        def parse(*args : str):
            ret_val = self.dice_parser.compile_langauge(ControlFlowIterator(
                iter(args)
                )
            )
            
            print(ret_val)
        
        @self.function_decorator()
        def variables():
            print(self.dice_parser.variable_map)