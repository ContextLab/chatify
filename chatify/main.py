import pathlib

import ipywidgets as widgets
import yaml
from IPython.core.magic import Magics, cell_magic, magics_class
from IPython.display import display

from .chains import CreateLLMChain
from .utils import check_dev_config, get_html
from .widgets import button_widget, loading_widget, option_widget, text_widget, thumbs


@magics_class
class Chatify(Magics):
    """A class for interactive chat functionality.

    Examples
    --------

    .. code-block:: python

        chat = Chatify()
        chat.explain('prompt', 'input')
    """

    def __init__(self, shell=None, **kwargs):
        super().__init__(shell, **kwargs)
        try:
            # If we find the config file we assume that user is a dev
            self.cfg = yaml.load(open("./config.yaml"), Loader=yaml.SafeLoader)
            print("config.yaml file found; using custom configuration.")
            # Check dev config file
            check_dev_config(self.cfg)

        except FileNotFoundError:
            # If we don't find the config.yaml the user is an end-point user
            # TODO: Fix a bug where the default_config.yaml file is not found
            # dirname = pathlib.Path(__file__).parent.resolve()
            # self.cfg = yaml.load(
            #     open(pathlib.Path(str(dirname) + "/default_config.yaml")),
            #     Loader=yaml.SafeLoader,
            # )
            # NOTE: As of now, the config is hard-coded as a temporary fix
            self.cfg = {
                "cache_config": {
                    "cache": False,
                    "caching_strategy": "exact",
                    "cache_db_version": 0.1,
                    "url": None,
                },
                "feedback": False,
                "model_config": {
                    "model": "proxy",
                    "proxy_url": "https://chatify.experiments.kordinglab.com/prompt/",
                },
                "chain_config": {"chain_type": "proxy"},
                "prompts_config": {
                    "prompts_to_use": ["tutor", "tester", "inventer", "experimenter"]
                },
            }

        self.prompts_config = self.cfg["prompts_config"]

        self.llm_chain = CreateLLMChain(self.cfg)
        self.tabs = None

    def _read_prompt_dir(self):
        """Reads prompt files from the dirname + '/prompts/' directory.

        Returns
        -------
        prompt_types : dict
            A dictionary mapping prompt types to their corresponding YAML contents.
        """
        dirname = pathlib.Path(__file__).parent.resolve()
        prompt_files = list(pathlib.Path(str(dirname) + "/prompts/").glob("*.yaml"))
        prompt_types = {}
        for f in self.prompts_config["prompts_to_use"]:
            for prompt_file in prompt_files:
                if f == prompt_file.name.split(".")[0]:
                    prompt_types[f] = yaml.load(
                        open(prompt_file), Loader=yaml.SafeLoader
                    )
        return prompt_types

    def _create_ui_elements(self):
        """Creates UI elements like buttons, prompt types, texts, and options."""
        # Buttons and prompt types
        self.execute_button = button_widget()
        self.loading = loading_widget()
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
        self.thumbs_up = thumbs("\U0001F44D")
        self.thumbs_down = thumbs("\U0001F44E")

    def _arrange_ui_elements(self, prompt_type):
        """Arranges UI elements based on the selected prompt type.

        Parameters
        ----------
        prompt_type : str
            The selected prompt type.

        Returns
        -------
        vbox : object
            A VBox container holding the arranged UI elements.
        """
        # Arrange options and buttons
        if self.cfg["feedback"]:
            elements = [
                self.options[prompt_type],
                self.execute_button,
                self.thumbs_up,
                self.thumbs_down,
            ]

        else:
            elements = [self.options[prompt_type], self.execute_button, self.loading]
        hbox = widgets.HBox(elements)
        vbox = widgets.VBox([hbox, self.texts[prompt_type]])
        return vbox

    def _cache(self, input_string, prompt):
        chain = self.llm_chain.create_chain(
            self.cfg["model_config"], prompt_template=prompt
        )
        output = self.llm_chain.execute(chain, input_string)
        return output

    def gpt(self, inputs, prompt):
        """Queries the GPT model and returns the output in markdown format.

        Parameters
        ----------
        inputs : dict
            The input dictionary containing line and cell values.
        prompt : str
            The prompt for querying the GPT model.

        Returns
        -------
        output : str
            The GPT model output in markdown format.
        """
        # TODO: Should we create the chain every time? Only prompt is changing not the model
        chain = self.llm_chain.create_chain(
            self.cfg["model_config"], prompt_template=prompt
        )
        output = self.llm_chain.execute(chain, inputs["cell"])

        return get_html(output)

    def update_values(self, *args, **kwargs):
        """Updates the values of UI elements based on the selected options.

        Parameters
        ----------
        *args
            Variable-length argument list.
        """
        self.loading.width = 30
        index = self.tabs.selected_index
        selected_prompt = self.prompt_names[index]
        # Get the prompt
        self.prompt = self.prompt_types[selected_prompt][
            self.options[selected_prompt].value
        ]
        self.texts[selected_prompt].value = self.gpt(self.cell_inputs, self.prompt)
        self.response = self.texts[selected_prompt].value
        self.loading.width = 0

    def record(self, *args):
        try:
            data = {
                "prompt": self.prompt,
                "response": self.response,
                "thumbs_up": self.thumbs_up.get_state(),
                "thumbs_down": self.thumbs_down.get_state(),
            }
        except AttributeError:
            data = {
                "prompt": None,
                "response": None,
                "thumbs_up": self.thumbs_up.get_state(),
                "thumbs_down": self.thumbs_down.get_state(),
            }
        # TODO: Implement data recording logic

    @cell_magic
    def explain(self, line, cell):
        """Executes the cell magic command 'explain' to display interactive chat UI.

        Parameters
        ----------
        line : str
            The command line arguments.
        cell : str
            The input cell contents.
        """
        # Store the inputs for processing
        self.cell_inputs = {"line": line, "cell": cell}
        self._create_ui_elements()

        # Create tab container
        components = []
        for index in self.prompt_types:
            components.append(self._arrange_ui_elements(index))
        self.tabs = widgets.Tab(children=components)

        # Name the tabs components
        for i, prompt_type in enumerate(self.prompt_types.keys()):
            self.tabs.set_title(i, "Robo-" + prompt_type.lower())
            self.texts[prompt_type].value = ""

        # Create a tab group
        accordion = widgets.Accordion(children=[self.tabs])
        accordion.set_title(0, "🤖💬")
        accordion.layout.collapsed = False

        display(accordion)

        # Button click
        self.execute_button.on_click(self.update_values)

        # Thumbs up and down
        self.thumbs_down.on_click(self.record)
        self.thumbs_up.on_click(self.record)
