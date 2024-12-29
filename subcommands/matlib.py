from DAKCommand import Command
from DAKMatrix import Matrix

from samgob import DiceSetParser
from samgob import ControlFlowIterator
from samgob.errors import ParseError

import matplotlib as mpl
import matplotlib.pyplot as plt

class PlotSubCommand(Command):
    def __init__(self,name : str, dice_parser : DiceSetParser):
        super().__init__(name)

        #store a referene to the langauge parser
        self.dice_parser = dice_parser

        @self.function_command(default=True)
        def heatmap(matrix : str):
            """
            takes a matrix string and parses out the samgob expression, storing the result in the tmp variable,
            then graphs and displays that variable
            """
            try:
                self.dice_parser.compile_langauge(ControlFlowIterator(iter(["tmp="+matrix])))
                
                if "tmp" in self.dice_parser.variable_map and isinstance(self.dice_parser.variable_map["tmp"],Matrix):
                    self.display_matrix(self.dice_parser.variable_map["tmp"],matrix)

            except ParseError:
                print("unable to parse matrix to graph, try again")

    def display_matrix(self,matrix : Matrix,title : str = "matrix")->None:
        
        fig, ax = plt.subplots()
        im = ax.imshow(matrix.value)
        
        color_bar = ax.figure.colorbar(im,ax=ax)
        color_bar.ax.set_ylabel("color range",rotation=-90,va="bottom")


        ax.set_title(title)
        fig.tight_layout()
        plt.show()

