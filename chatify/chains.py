import time

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, LLMMathChain

from .llm_models import ModelsFactory
from .cache import LLMCacher


class CreateLLMChain:
    def __init__(self, config) -> None:
        self.chain_config = config['chain_config']
        self.llm_models_factory = ModelsFactory()
        self._setup_chain_factory()
        return None

    def _setup_chain_factory(self):
        self.chain_factory = {'math': LLMMathChain, 'default': LLMChain}

    def create_prompt(self, prompt):
        PROMPT = PromptTemplate(
            template=prompt['content'], input_variables=prompt['input_variables']
        )
        return PROMPT

    def create_chain(self, model_config, prompt_template):
        # Setup the LLM model
        llm_model = self.llm_models_factory.get_model(model_config)

        # Setup the chain
        try:
            chain_type = self.chain_config['chain_type']
        except KeyError:
            chain_type = 'default'
        chain = self.chain_factory[chain_type](
            llm=llm_model, prompt=self.create_prompt(prompt_template)
        )
        return chain

    def execute(self, chain, inputs, *args, **kwargs):
        output = chain(inputs)
        return output
