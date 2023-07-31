#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
from glob import glob

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['gptcache', 'langchain', 'openai', 'markdown', 'ipywidgets', 'requests', 'markdown-it-py[linkify,plugins]', 'pygments']
extras = ['transformers', 'torch>=2.0', 'tensorflow>=2.0', 'flax', 'einops', 'accelerate', 'xformers', 'bitsandbytes', 'sentencepiece', 'llama-cpp-python']

test_requirements = [
    'pytest>=3',
]

setup(
    author="NeuroMatch",
    author_email='nma@neuromatch.io',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A python package that adds a magic command to Jupyter notebooks to enable LLM interactions with code cells.",
    install_requires=requirements,
    extras_require={
        'hf': extras,
    },
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='chatify',
    name='chatify',
    packages=find_packages(include=['chatify', 'chatify.*']),
    test_suite='tests',
    tests_require=test_requirements,
    package_data={'': ['**/*.yaml']},
    url='https://github.com/ContextLab/chatify',
    version='0.2.0',
    zip_safe=False,
)
