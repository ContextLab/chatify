import yaml
import markdown

import pathlib


from IPython.core.magic import Magics, magics_class, cell_magic
from IPython.display import display

import ipywidgets as widgets

from .chains import CreateLLMChain
from .widgets import option_widget, button_widget, text_widget, thumbs


@magics_class
class Chatify(Magics):
    def __init__(self, shell=None, **kwargs):
        super().__init__(shell, **kwargs)
        self.cfg = yaml.load(open('../config.yaml'), Loader=yaml.SafeLoader)
        self.llm_chain = CreateLLMChain(self.cfg)

    def _read_prompt_dir(self):
        prompt_files = list(pathlib.Path('../prompts/').glob('*.yaml'))
        prompt_types = {}
        for f in prompt_files:
            prompt_types[f.name.split('.')[0]] = yaml.load(
                open(f), Loader=yaml.SafeLoader
            )
        return prompt_types

    def _create_ui_elements(self):
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

        # Thumbs up and down
        self.thumbs_up = thumbs('fa-thumbs-up')
        self.thumbs_down = thumbs('fa-thumbs-down')

    def _arrange_ui_elements(self, prompt_type):
        # Arrange options and buttons
        hbox = widgets.HBox(
            [
                self.options[prompt_type],
                self.button,
                self.thumbs_up,
                self.thumbs_down,
            ]
        )
        vbox = widgets.VBox([hbox, self.texts[prompt_type]])
        return vbox

    def gpt(self, inputs, prompt):
        # Query the GPT model
        chain = self.llm_chain.create_chain(
            self.cfg['model_config'], prompt_template=prompt
        )
        output = self.llm_chain.execute(chain, inputs['cell'])
        return markdown.markdown(output)

    def update_values(self, *args):
        index = self.tabs.selected_index
        selected_prompt = self.prompt_names[index]
        # Get the prompt
        prompt = self.prompt_types[selected_prompt][self.options[selected_prompt].value]
        self.texts[selected_prompt].value = self.gpt(self.cell_inputs, prompt)

    @cell_magic
    def explain(self, line, cell):
        # Store the inputs for processing
        self.cell_inputs = {'line': line, 'cell': cell}
        self._create_ui_elements()

        # Create tab container
        components = []
        for index in self.prompt_types:
            components.append(self._arrange_ui_elements(index))
        self.tabs = widgets.Tab(children=components)

        # Name the tabs components
        for i, prompt_type in enumerate(self.prompt_types.keys()):
            self.tabs.set_title(i, prompt_type.title())
            self.texts[prompt_type].value = ''

        # Create a tab group
        accordion = widgets.Accordion(children=[self.tabs])
        accordion.set_title(0, 'Chatify ' + u"\U0001F916")
        display(accordion)

        # Button click
        self.button.on_click(self.update_values)
