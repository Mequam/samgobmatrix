from samgob import DiceSetParser
from io import TextIOWrapper
from DAKCommand import Command
from DAKMatrix import Matrix

class SaveSubCommand(Command):
    """
    represents a sub command that saves a variable out to disc
    """
    def __init__(self,name,dice_parser : DiceSetParser,**kwargs):
        super().__init__(name,**kwargs)


        self.dice_parser : DiceSetParser = dice_parser

        @self.function_decorator()
        def save(varname : str,*extras : str,outnames : list,filepath = "saved_variables.txt"):
            """
            append one or more variables to a file
            """

            with open(filepath,'a') as appendFile:
                for variable_name in (varname,) + extras:
                    self.save_variable(appendFile,variable_name,variable_name)
        
        @self.function_decorator(default=True)
        def show(*,filepath = "saved_variables.txt"):
            with open(filepath,'r') as readFile:
                line = readFile.readline()
                while line:
                    print(line,end="")
                    line = readFile.readline()
    
    def save_variable(self,file : TextIOWrapper,in_name,out_name):
        if not in_name in self.dice_parser.variable_map: return

        #sadly we cannot save set variables as of yet
        if not (
                isinstance(self.dice_parser.variable_map[in_name],Matrix) or \
                type(self.dice_parser.variable_map[in_name]) == float
                ):
                        return

        variable = self.dice_parser.variable_map[in_name]
        
        #we are storing a matrix variable
        if isinstance(variable,Matrix):
            file.writelines(f'{out_name}={variable.samgob_string()}\n')
