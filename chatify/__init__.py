"""Top-level package for chatify."""

__author__ = """Contextual Dynamics Laboratory"""
__email__ = 'contextualdynamics@gmail.com'
__version__ = '0.1.1'

from .main import Chatify
from .llm_models import FakeLLMModel, CachedLLMModel, OpenAIModel, OpenAIChatModel, HuggingFaceModel, ModelsFactory, BaseLLMModel

def load_ipython_extension(ipython):
    ipython.register_magics(Chatify)
