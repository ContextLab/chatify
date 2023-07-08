import os

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

from .utils import FakeListLLM


class ModelsFactory:
    """A factory class for creating different models."""

    def __init__(self, *args) -> None:
        """
        Initializes the ModelsFactory instance.

        Parameters
        ----------
        *args : tuple
            Variable-length arguments.

        Returns
        -------
        None
        """

        return None

    def get_model(self, model_config):
        """Returns the initialized model based on the model configuration.

        Parameters
        ----------
        model_config : dict
            Configuration for the desired model.

        Returns
        -------
        model : object
            Initialized model based on the model configuration.

        Raises
        ------
        RuntimeError
            If the specified model is not supported.
        """
        model_ = model_config['model']

        # Collect all the models
        models = {
            'open_ai_model': OpenAIModel(model_config),
            'open_ai_chat_model': OpenAIChatModel(model_config),
            'fake_model': FakeLLMModel(model_config),
            'cached_model': CachedLLMModel(model_config),
        }

        if model_ in models.keys():
            return models[model_].init_model()
        else:
            raise RuntimeError(f"{model_} is not supported yet!")


class BaseLLMModel:
    """Base class for Language Model (LLM) models."""

    def __init__(self, model_config) -> None:
        """Initializes the BaseLLMModel instance.

        Parameters
        ----------
        model_config : dict
            Configuration for the model.

        Returns
        -------
        None
        """
        self.model_config = model_config
        self.llm_model = None

    def init_model(self, *args, **kwargs):
        """Initializes the LLM model (to be implemented by derived classes).

        Parameters
        ----------
        *args : tuple
            Variable-length arguments.
        **kwargs : dict
            Arbitrary keyword arguments.

        Raises
        ------
        NotImplementedError
            If not implemented by derived classes.
        """
        raise NotImplementedError


class OpenAIModel(BaseLLMModel):
    """Class representing an OpenAI Chat Model derived from BaseLLMModel."""

    def __init__(self, model_config) -> None:
        """Initializes the OpenAIChatModel instance.

        Parameters
        ----------
        model_config : dict
            Configuration for the model.

        Returns
        -------
        None
        """
        super().__init__(model_config)

    def init_model(self):
        """Initializes the OpenAI Chat Model.

        Returns
        -------
        llm_model : ChatOpenAI
            Initialized OpenAI Chat Model.
        """

        os.environ["OPENAI_API_KEY"] = self.model_config['open_ai_key']

        llm_model = OpenAI(
            temperature=0.85,
            openai_api_key=self.model_config['open_ai_key'],
            model_name=self.model_config['model_name'],
            presence_penalty=0.1,
            max_tokens=500,
        )
        return llm_model


class OpenAIChatModel(BaseLLMModel):
    """Class representing an OpenAI Chat Model derived from BaseLLMModel."""

    def __init__(self, model_config) -> None:
        """Initializes the OpenAIChatModel instance.

        Parameters
        ----------
        model_config : dict
            Configuration for the model.

        Returns
        -------
        None
        """
        super().__init__(model_config)

    def init_model(self):
        """Initializes the OpenAI Chat Model.

        Returns
        -------
        llm_model : ChatOpenAI
            Initialized OpenAI Chat Model.
        """
        llm_model = ChatOpenAI(
            temperature=0.85,
            openai_api_key=self.model_config['open_ai_key'],
            model_name=self.model_config['model_name'],
            presence_penalty=0.1,
            max_tokens=500,
        )
        return llm_model


class FakeLLMModel(BaseLLMModel):
    def __init__(self, model_config) -> None:
        """Initializes the FakeListLLM instance.

        Parameters
        ----------
        model_config : dict
            Configuration for the model.

        Returns
        -------
        None
        """
        super().__init__(model_config)

    def init_model(self):
        """Initializes the Fake Chat Model.

        Returns
        -------
        llm_model : FakeListLLM
            Initialized Fake Chat Model.
        """
        responses = ['Placeholder text (used for debugging)']
        llm_model = FakeListLLM(responses=responses)
        return llm_model


class CachedLLMModel(BaseLLMModel):
    def __init__(self, model_config) -> None:
        """Initializes the FakeListLLM instance.

        Parameters
        ----------
        model_config : dict
            Configuration for the model.

        Returns
        -------
        None
        """
        super().__init__(model_config)

    def init_model(self):
        """Initializes the Fake Chat Model.

        Returns
        -------
        llm_model : FakeListLLM
            Initialized Fake Chat Model.
        """
        llm_model = FakeListLLM(responses=['This is a cached response'])
        return llm_model
