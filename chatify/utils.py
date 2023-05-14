from typing import Any, List, Mapping, Optional

import random

from langchain.llms.base import LLM


class FakeListLLM(LLM):
    """Fake LLM wrapper for testing purposes."""

    responses: List
    i: int = 0

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "fake-list"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """First try to lookup in queries, else return 'foo' or 'bar'."""
        response = self.responses[random.randint(0, len(self.responses) - 1)]
        return response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {}
