from DAKMatrix import Matrix
from math import pi
from samgob import DiceSetParser
from samgob.iterators.control_flow_iterator import ControlFlowIterator

parser : DiceSetParser = DiceSetParser()

while True:
    ui = input('> ')
    print(ui)
    result = parser.compile_langauge(ControlFlowIterator(
        iter(ui.split(" "))
        ))
    print(result)
