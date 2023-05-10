import yaml

from langchain.chat_models import ChatOpenAI
from langchain.llms.fake import FakeListLLM


class ModelsFactory:
    def __init__(self, *args) -> None:
        return None

    def get_model(self, model_config):
        model_ = model_config['model']

        # Collect all the models
        models = {
            'open_ai_model': OpenAIChatModel(model_config),
            'fake_model': FakeLLMModel(model_config),
        }

        if model_ in models.keys():
            return models[model_].init_model()
        else:
            raise RuntimeError(f"{model_} is not supported yet!")


class BaseLLMModel:
    def __init__(self, model_config) -> None:
        self.model_config = model_config
        self.llm_model = None

    def init_model(self, *args, **kwargs):
        raise NotImplementedError


class OpenAIChatModel(BaseLLMModel):
    def __init__(self, model_config) -> None:
        super().__init__(model_config)

    def init_model(self):
        llm_model = ChatOpenAI(
            temperature=0.85,
            openai_api_key=self.model_config['open_ai_key'],
            model_name=self.model_config['model'],
            presence_penalty=0.1,
            max_tokens=500,
        )
        return llm_model


class FakeLLMModel(BaseLLMModel):
    def __init__(self, model_config) -> None:
        super().__init__(model_config)

    def init_model(self):
        responses = [
            "Action: Python REPL\nAction Input: print(2 + 2)",
            "Final Answer: 4",
        ]
        llm_model = FakeListLLM(responses=responses)
        return llm_model
