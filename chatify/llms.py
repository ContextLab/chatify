import yaml

from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, LLMMathChain

config = yaml.load(open('../config.yaml'), Loader=yaml.SafeLoader)

# Language model
llm = ChatOpenAI(
    temperature=0.85,
    openai_api_key=config['open_ai_key'],
    model_name=config['model'],
    presence_penalty=0.1,
    max_tokens=500,
)


class CreateLLMChains:
    def __init__(self) -> None:
        return None

    def create_prompt(self, prompt):
        PROMPT = PromptTemplate(
            template=prompt['content'], input_variables=prompt['input_variables']
        )
        return PROMPT

    def mathchain(self, prompt_template):
        chain = LLMMathChain(llm=llm, prompt=self.create_prompt(prompt_template))
        return chain

    def explainchain(self, prompt_template):
        chain = LLMChain(llm=llm, prompt=self.create_prompt(prompt_template))
        return chain
