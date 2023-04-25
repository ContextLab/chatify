import yaml

from IPython.core.magic import Magics, magics_class, line_magic, cell_magic

from IPython.display import Markdown, display

from .llms import llm_chains


code_prompts = yaml.load(open('../prompts/code.yaml'), Loader=yaml.SafeLoader)
general_prompts = yaml.load(open('../prompts/general.yaml'), Loader=yaml.SafeLoader)
neuro_prompts = yaml.load(open('../prompts/neuro.yaml'), Loader=yaml.SafeLoader)


@magics_class
class Chatify(Magics):
    @cell_magic
    def eli5(self, line, cell):
        chain = llm_chains.explainchain(general_prompts['basic'])
        output = chain(cell)
        display(Markdown(output['text']))
