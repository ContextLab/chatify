import yaml
import markdown

import pathlib


from IPython.core.magic import Magics, magics_class, cell_magic
from IPython.display import display

import ipywidgets as widgets

from .llms import llm_chains
from .widgets import option_widget, button_widget, text_widget, thumbs


@magics_class
class Chatify(Magics):
    def __init__(self, shell=None, **kwargs):
        super().__init__(shell, **kwargs)
        # Buttons and prompt types
        self.button = button_widget()
        self.prompt_types = self._read_prompt_dir()
        self.prompt_names = {
            item: key for item, key in enumerate(self.prompt_types.keys())
        }

        # Create different text and options field for each prompt
        self.texts, self.options = {}, {}
        for key, values in self.prompt_types.items():
            self.texts[key] = text_widget()
            self.options[key] = option_widget(values)

    def _read_prompt_dir(self):
        prompt_files = list(pathlib.Path('../prompts/').glob('*.yaml'))
        prompt_types = {}
        for f in prompt_files:
            prompt_types[f.name.split('.')[0]] = yaml.load(
                open(f), Loader=yaml.SafeLoader
            )
        return prompt_types

    def _create_ui_elements(self, prompt_type):
        # Thumbs up and down
        thumbs_up = thumbs('fa-thumbs-up')
        thumbs_down = thumbs('fa-thumbs-down')

        # Arrange options and buttons
        hbox = widgets.HBox(
            [self.options[prompt_type], self.button, thumbs_up, thumbs_down]
        )
        vbox = widgets.VBox([hbox, self.texts[prompt_type]])
        return vbox

    @cell_magic
    def explain(self, line, cell):
        # Store the inputs for processing
        self.cell_inputs = {'line': line, 'cell': cell}

        # Create tab container
        components = []
        for index in self.prompt_types:
            components.append(self._create_ui_elements(index))
        self.tabs = widgets.Tab(children=components)

        # Name the tabs components
        for i, prompt_type in enumerate(self.prompt_types.keys()):
            self.tabs.set_title(i, prompt_type)

        # Create a tab group
        accordion = widgets.Accordion(children=[self.tabs])
        accordion.set_title(0, 'Chatify')
        display(accordion)

        # Button click
        self.button.on_click(self.update_values)

    def gpt(self, inputs, prompt):
        # Query the GPT model
        chain = llm_chains.explainchain(prompt)
        output = chain(inputs['cell'])
        return markdown.markdown(output['text'])

    def update_values(self, *args):
        index = self.tabs.selected_index
        selected_prompt = self.prompt_names[index]
        # Get the prompt
        prompt = self.prompt_types[selected_prompt][self.options[selected_prompt].value]
        self.texts[selected_prompt].value = self.gpt(self.cell_inputs, prompt)
