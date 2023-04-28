import yaml
import markdown

from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
from IPython.display import Markdown, display

import ipywidgets as widgets

from .llms import llm_chains
from .widgets import option_widget, button_widget, text_widget, thumbs


code_prompts = yaml.load(open('../prompts/code.yaml'), Loader=yaml.SafeLoader)
general_prompts = yaml.load(open('../prompts/general.yaml'), Loader=yaml.SafeLoader)
neuro_prompts = yaml.load(open('../prompts/neuro.yaml'), Loader=yaml.SafeLoader)


@magics_class
class Chatify(Magics):
    def __init__(self, shell=None, **kwargs):
        super().__init__(shell, **kwargs)
        self.general_widget = option_widget(general_prompts)
        self.button = button_widget()
        self.text = text_widget()
        self.thumbs_up = thumbs('fa-thumbs-up')
        self.thumbs_down = thumbs('fa-thumbs-down')

    @cell_magic
    def explain(self, line, cell):
        # Store the inputs for processing
        self.cell_inputs = {'line': line, 'cell': cell}

        # Arrange options and buttons
        hbox = widgets.HBox(
            [self.general_widget, self.button, self.thumbs_up, self.thumbs_down]
        )
        vbox = widgets.VBox([hbox, self.text])
        accordion = widgets.Accordion(children=[vbox])
        accordion.set_title(0, 'Chatify')

        # Button click
        self.button.on_click(self.update_values)
        display(accordion)

    def gpt(self, inputs):
        chain = llm_chains.explainchain(general_prompts[self.general_widget.value])
        output = chain(inputs['cell'])
        return markdown.markdown(output['text'])

    def update_values(self, *args):
        self.text.value = self.gpt(self.cell_inputs)
