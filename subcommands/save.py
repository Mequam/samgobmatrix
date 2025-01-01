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
            variables = None
            with open(filepath,'r') as readFile:
                variables = self.read_queries(readFile)
            
            if not variables:
                print("unable to detect query file!")

            for variable_name in (varname,) + variablelist:
                print(variable_name)
                encoding = self.encode_variable(variable_name)
                if encoding:
                    variables[variable_name] = encoding

            with open(filepath,'w') as writeFile:
                self.store_queries(variables, writeFile)

        @self.function_command()
        def load(varname : str = '*',*,filepath = 'saved_variables.txt'):
            try:
                with open(filepath,'r') as readFile:
                    if varname == '*': #load all queries
                        self.load_all_queries(readFile)
                    else: #load a specific query
                        self.load_query(varname, readFile)

            except FileNotFoundError:
                print(f'"{filepath}" does not exist, try saving variables first')

        
        @self.function_command(default=True)
        def show(*,filepath = "saved_variables.txt"):
            try:
                with open(filepath,'r') as readFile:
                    print(self.read_queries(readFile))
            except FileNotFoundError:
                #inteanded behavior is to do nothing
                pass

    def load_query(self,varname : str, readFile : TextIOWrapper)->None:
        queries = self.read_queries(readFile)
        if varname in queries:
            self.dice_parser.compile_langauge(ControlFlowIterator(
                iter([f'{varname}={queries[varname]}'])
                ))

    #loads all variables stored in the given file
    def load_all_queries(self, file : TextIOWrapper):
        line = file.readline()
        while line:
            print(line[:-1])
            self.dice_parser.compile_langauge(ControlFlowIterator(
                    iter([line.strip()])
                ))
            line = file.readline()

    def store_queries(self, queries : dict, writeFile : TextIOWrapper)->None:
        for query in queries:
            writeFile.write(f'{query}={queries[query]}')


    def read_queries(self, file : TextIOWrapper)->dict:
        """reads in every entry of a text file into memory for convinent editing"""
        lines = file.readlines()
        return { key:value for (key,value) in [line.split("=") for line in lines]}

    def encode_variable(self,in_name)->str:
        if not in_name in self.dice_parser.variable_map: return None

        #sadly we cannot save set variables as of yet
        if not (
                isinstance(self.dice_parser.variable_map[in_name],Matrix) or \
                type(self.dice_parser.variable_map[in_name]) == float or \
                type(self.dice_parser.variable_map[in_name]) == int
                ):
                        return None

        variable = self.dice_parser.variable_map[in_name]

        #we are storing a matrix variable
        if isinstance(variable,Matrix):
            return (f'{variable.samgob_string()}\n')
        else: #float variable
            return (f'{variable}\n')

