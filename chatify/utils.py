from typing import Any, List, Mapping, Optional

import random
import urllib

from markdown_it import MarkdownIt
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments import highlight

from langchain.llms.base import LLM


def highlight_code(code, name, attrs):
    """Highlight a block of code"""

    try:
        lexer = get_lexer_by_name(name)
    except:
        lexer = get_lexer_by_name('python')
    formatter = HtmlFormatter(cssclass='codehilite', linenos='table')

    return highlight(code, lexer, formatter)


def get_html(markdown, code_style='default'):
    """Return HTML string rendered from markdown source."""

    md = MarkdownIt(
        "js-default",
        {
            "linkify": True,
            "html": True,
            "typographer": True,
            "highlight": highlight_code,
        },
    )

    formatter = HtmlFormatter(style=code_style, linenos='table')
    css = formatter.get_style_defs()

    return f'<head><style>{css}</style></head>' + md.render(markdown)


class FakeListLLM(LLM):
    """Fake LLM wrapper for testing purposes.

    Attributes
    ----------
    responses : List
        List of responses.
    """

    responses: List

    @property
    def _llm_type(self) -> str:
        """Return type of LLM.

        Returns
        -------
        str
            Type of LLM.
        """
        return "fake-list"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """First try to lookup in queries, else return 'foo' or 'bar'.

        Parameters
        ----------
        prompt : str
            Input prompt.
        stop : List[str], optional
            List of stop tokens, by default None.

        Returns
        -------
        str
            Generated response.
        """
        response = self.responses[random.randint(0, len(self.responses) - 1)]
        return response

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters.

        Returns
        -------
        Mapping[str, Any]
            Identifying parameters.
        """
        return {}


def compress_code(text):
    return '\n'.join(
        [line.strip() for line in text.split('\n') if len(line.strip()) > 0]
    )


def check_dev_config(config):
    # We assume that the dev config has openai api key
    if ('open_ai' in config['model_config']['model']) and (
        'open_ai_key' not in config['model_config']
        or config['model_config']['open_ai_key'] is None
    ):
        raise KeyError('OpenAI API key cannot be empty')


def download_cache_database(config):
    try:
        cache_db_version = config['cache_db_version']
        file_name = f'NMA_2023_v{cache_db_version}.cache'
        url = config['url']
        # print(f'Downloading the \'cache\' file.')

        urllib.request.urlretrieve(url, file_name)
    except FileNotFoundError:
        print(f'{file_name} could not be downloaded from the provided cache URL: {url}')
