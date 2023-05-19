import os

from gptcache.adapter.langchain_models import LangChainLLMs
from gptcache import Cache
from gptcache.processor.pre import get_prompt

from langchain import SQLDatabase, SQLDatabaseChain

from gptcache.processor.pre import get_prompt
from gptcache.manager import get_data_manager, CacheBase, VectorBase
from gptcache.embedding import Onnx
from gptcache.similarity_evaluation.distance import SearchDistanceEvaluation


class LLMCacher:
    """A class for caching and managing LLM (Language Model) instances."""

    def __init__(self, config):
        """Initializes a new LLMCacher instance.

        Parameters:
        -----------
        config : dict
            A dictionary containing configuration parameters.
        """
        self.config = config
        self.llm_cache = None

    def cache_llm(self, llm, *args, **kwargs):
        """Caches the LLM using the specified caching strategy.

        Parameters:
        -----------
        llm : LLM
            The LLM (Language Model) to be cached.
        *args : positional arguments
            Additional positional arguments.
        **kwargs : keyword arguments
            Additional keyword arguments.

        Returns:
        --------
        llm : LangChainLLMs
            The LangChainLLMs instance after caching the LLM.
        """
        self.llm_cache = Cache()
        self.llm_cache.set_openai_key()

        if self.config['caching_strategy'] == 'similarity':
            onnx = Onnx()
            cache_base = CacheBase('sqlite')
            vector_base = VectorBase('faiss', dimension=onnx.dimension)
            data_manager = get_data_manager(
                cache_base, vector_base, max_size=10, clean_size=2
            )
            self.llm_cache.init(
                pre_embedding_func=get_prompt,
                embedding_func=onnx.to_embeddings,
                data_manager=data_manager,
                similarity_evaluation=SearchDistanceEvaluation(),
            )
        else:
            # Exact caching
            self.llm_cache.init(
                pre_embedding_func=get_prompt,
            )
        llm = LangChainLLMs(llm=llm)
        return llm
