from DAKMatrix import Matrix
from math import pi
from samgob import DiceSetParser
from samgob.iterators.control_flow_iterator import ControlFlowIterator
import sys

from prompt_toolkit import prompt,PromptSession,print_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style

from DAKCommand import Command
from subcommands.samgob import SamgobSubCommand
from subcommands.save import SaveSubCommand
from subcommands.matlib import PlotSubCommand

style = Style.from_dict({
    # User input (default text).
    '':          '#ff6600',
    'placeholder': '#00CCCC',

    # Prompt.
    'prompt': '#884444',
    'completed': '#333333'
})

completed_style = Style.from_dict({
    # User input (default text).
    '':          '#333333',

    # Prompt.
    'prompt': '#333333',
    'completed': '#333333'
})

prompt = [("class:prompt",'()> ')]
placeholder = [('class:placeholder','command or query')]


bindings = KeyBindings()
prompt_session = PromptSession()

@bindings.add('up')
def _(event):
    print("you pressed the up key")

@bindings.add('down')
def _(event):
    print("you pressed the down key")


dice_parser = DiceSetParser()
dice_parser.numpy_matrix_formating = True

commandTree : Command = Command("root")
commandTree.add_sub_command(SamgobSubCommand("samgob",dice_parser=dice_parser),default=True)
commandTree.add_sub_command(PlotSubCommand("plot",dice_parser=dice_parser))
commandTree.add_sub_command(SaveSubCommand("memory", dice_parser=dice_parser))


#add an exit command to leave the tree
@commandTree.function_command()
def exit():
    print("goodbye!")
    sys.exit(1)

def generate_toolbar()->str:
    buffer = ""
    for v in dice_parser.variable_map:
        if isinstance(dice_parser.variable_map[v],Matrix):
            buffer += f'{v}={dice_parser.variable_map[v].samgob_string()} '
        else:
            buffer += f'{v}={dice_parser.variable_map[v]} '

    ret_val = buffer[:100]
    if len(ret_val) != len(buffer):
        ret_val += "..."

    return ret_val

try:
    while True:
        user_input = prompt_session.prompt(prompt,
                                       style=style,
                                       bottom_toolbar=generate_toolbar,
                                       placeholder=placeholder)
        
        #gray out user inputs before computing outputs
        #ansi command to move the cursor up a line
        sys.stdout.write("\033[A")
        sys.stdout.flush()
        if (user_input == ""): 
            user_input = " " * len(placeholder[0][1]) #zero out placeholder input

        print_formatted_text(prompt[0][1] + user_input,style=completed_style)
        
        commandTree.parse(user_input.split(" "))


except KeyboardInterrupt:
    exit()



#parser : DiceSetParser = DiceSetParser(numpy_matrix_formating=True)
#
#while True:
#    ui = input('> ')
#    result = parser.compile_langauge(ControlFlowIterator(
#        iter(ui.split(" "))
#        ))
#    print(result)
