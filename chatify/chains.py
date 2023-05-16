import time

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, LLMMathChain

from .llm_models import ModelsFactory
from .cache import LLMCacher


class CreateLLMChain:
    def __init__(self, config) -> None:
        # Parameters
        self.chain_config = config['chain_config']
        self.llm_model = None
        self.cache = config['cache']

        # Models, Cache and chains
        self.llm_models_factory = ModelsFactory()
        self.cacher = LLMCacher(config)
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
        if self.llm_model is None:
            # Setup the LLM model
            self.llm_model = self.llm_models_factory.get_model(model_config)

            if self.cache:
                self.llm_model = self.cacher.cache_llm(self.llm_model)

        # Setup the chain
        try:
            chain_type = self.chain_config['chain_type']
        except KeyError:
            chain_type = 'default'
        chain = self.chain_factory[chain_type](
            llm=self.llm_model, prompt=self.create_prompt(prompt_template)
        )
        return chain

    def execute(self, chain, inputs, *args, **kwargs):
        if self.cache:
            inputs = chain.prompt.format(text=inputs)
            output = chain.llm(inputs, cache_obj=self.cacher.llm_cache)
        else:
            output = chain(inputs)['text']

        return output
