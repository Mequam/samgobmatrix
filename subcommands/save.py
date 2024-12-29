from samgob import DiceSetParser
from samgob import ControlFlowIterator
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

        @self.function_command()
        def save(varname : str,*variablelist : str,outnames : list,filepath = "saved_variables.txt"):
            """
            append one or more variables to a file
            """

            print(variablelist)
            print(outnames)
            with open(filepath,'a') as appendFile:
                for variable_name in (varname,) + variablelist:
                    self.save_variable(appendFile,variable_name,variable_name)

        @self.function_command()
        def load(varname : str = '*',*,filepath = 'saved_variables.txt'):
            try:
                with open(filepath,'r') as readFile:
                    if varname == '*':
                        self.load_all(readFile)
            except FileNotFoundError:
                print(f'"{filepath}" does not exist, try saving variables first')

        
        @self.function_command(default=True)
        def show(*,filepath = "saved_variables.txt"):
            try:
                with open(filepath,'r') as readFile:
                    line = readFile.readline()
                    while line:
                        print(line,end="")
                        line = readFile.readline()
            except FileNotFoundError:
                #inteanded behavior is to do nothing
                pass
    
    #loads all variables stored in the given file
    def load_all(self, file : TextIOWrapper):
        line = file.readline()
        while line:
            print(line[:-1])
            self.dice_parser.compile_langauge(ControlFlowIterator(
                    iter([line.strip()])
                ))
            line = file.readline()


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
