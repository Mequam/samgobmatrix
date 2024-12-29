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



commandTree : Command = Command("root")
commandTree.add_sub_command(SamgobSubCommand("samgob"),default=True)

try:
    while True:
        user_input = prompt_session.prompt(prompt,
                                       style=style,
                                       bottom_toolbar="testing123",
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
    print("goodbye!")
    sys.exit(1)



#parser : DiceSetParser = DiceSetParser(numpy_matrix_formating=True)
#
#while True:
#    ui = input('> ')
#    result = parser.compile_langauge(ControlFlowIterator(
#        iter(ui.split(" "))
#        ))
#    print(result)
