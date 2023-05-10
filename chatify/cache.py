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
    def __init__(self) -> None:
        return None

    def cache_llm(self, llm, *args, **kwargs):
        onnx = Onnx()
        cache_base = CacheBase('sqlite')
        vector_base = VectorBase('faiss', dimension=onnx.dimension)
        data_manager = get_data_manager(
            cache_base, vector_base, max_size=10, clean_size=2
        )

        self.llm_cache = Cache()
        self.llm_cache.init(
            pre_embedding_func=get_prompt,
        )
        llm = LangChainLLMs(llm=llm)
        return llm
