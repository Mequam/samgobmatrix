from prompt_toolkit import Application,HTML
from prompt_toolkit.data_structures import Point
from prompt_toolkit.styles import Style
from prompt_toolkit.layout.containers import HSplit,VSplit
from prompt_toolkit.layout import FormattedTextControl,ScrollablePane
from prompt_toolkit.layout.layout import Layout,BufferControl,Buffer,Window
from prompt_toolkit.widgets import TextArea,Box
from prompt_toolkit.key_binding import KeyBindings

def get_text_prompt()->str:
    return "()> "
def get_html_prompt()->HTML:
    return HTML(f"<prompt>{get_text_prompt()}</prompt>")

keybinding = KeyBindings()

prompt_style = Style.from_dict({
        'prompt':'#00BBFF',
        '':'#EEAA00',
        'history':'#333333'
    })

input_widget = TextArea(prompt=get_html_prompt,height=1)

buffer_scroll_position = 0

history_control = FormattedTextControl(show_cursor=True,get_cursor_position=lambda : Point(0,buffer_scroll_position))

history_widget = Window(history_control,style="class:history")

root_container = HSplit([
    history_widget,
    input_widget
    ])

layout = Layout(root_container)


history_control.text = []

@keybinding.add("enter")
def accept_input(event):
    global buffer_scroll_position

    user_input = input_widget.text
    input_widget.text = ""
    
    history_control.text.append(('class:prompt',get_text_prompt()))
    history_control.text.append(('',user_input + "\n"))
    buffer_scroll_position += 1

    #history_control.buffer.cursor_position = len(history_widget.buffer.text)


app = Application(layout=layout,style=prompt_style,key_bindings=keybinding,full_screen=False)

app.layout.focus(input_widget)

app.run()
