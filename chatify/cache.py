from gptcache.adapter.langchain_models import LangChainLLMs
from gptcache import Cache
from gptcache.processor.pre import get_prompt


from gptcache.manager import get_data_manager, CacheBase, VectorBase


from gptcache.embedding import Onnx
from gptcache.embedding.string import to_embeddings as string_embedding


from gptcache.similarity_evaluation.distance import SearchDistanceEvaluation
from gptcache.similarity_evaluation.exact_match import ExactMatchEvaluation

from .utils import download_cache_database


class LLMCacher:
    """A class for caching and managing LLM (Language Model) instances."""

    def __init__(self, config):
        """Initializes a new LLMCacher instance.

        Parameters:
        -----------
        config : dict
            A dictionary containing configuration parameters.
        """
        self.cache_config = config['cache_config']
        self.llm_cache = None
        self._download_qa_database()

    def _download_qa_database(self):
        cache_db_version = self.cache_config['cache_db_version']
        self.db_file = f'NMA_2023_v{cache_db_version}.cache'

        if self.cache_config['url'] is not None:
            download_cache_database(self.cache_config)

    def cache_llm(self, llm, *args, **kwargs):
        """Caches the LLM using the specified caching strategy.

        Parameters
        ----------
        llm : LLM
            The LLM (Language Model) to be cached.
        *args : positional arguments
            Additional positional arguments.
        **kwargs : keyword arguments
            Additional keyword arguments.

        Returns
        -------
        llm : LangChainLLMs
            The LangChainLLMs instance after caching the LLM.
        """
        self.llm_cache = Cache()
        self.llm_cache.set_openai_key()

        if self.cache_config['caching_strategy'] == 'similarity':
            onnx = Onnx()
            cache_base = CacheBase(self.db_file)
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
            data_manager = get_data_manager(data_path=self.db_file)
            self.llm_cache.init(
                pre_embedding_func=get_prompt,
                data_manager=data_manager,
                similarity_evaluation=ExactMatchEvaluation(),
            )
        llm = LangChainLLMs(llm=llm)
        return llm
