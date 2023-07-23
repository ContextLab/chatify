# Chatify 🤖
[![DOI](https://zenodo.org/badge/627651845.svg)](https://zenodo.org/badge/latestdoi/627651845)

Chatify is a python package that enables ipython magic commands to Jupyter notebooks that provide LLM-driven enhancements to markdown and code cells.  This package is currently in the *alpha* stage: expect broken things, crashes, bad (wrong, misleading) answers, and other serious issues.  That said, we think Chatify is pretty neat even in this early form, and we're excited about its future!

![Image credit: DALL-E-2; prompt: robotic tutor helping a human student learn to program, science fiction, detailed rendering, futuristic, exquisite detail, graphic artist](https://github.com/ContextLab/chatify/assets/9030494/e3b928e1-f683-44a5-af1e-5c51e3f0e541)


# Background

This tool was originally created to supplement the [Neuromatch Academy](https://compneuro.neuromatch.io/tutorials/intro.html) materials.  To reign in costs in this initial version and enable support for the widest audience, we use [the smallest (7B parameter) variant of Meta's Llama 2 model](https://huggingface.co/meta-llama/Llama-2-7b) as the default model.  A "Chatify-enhanced" version of the Neuromatch computational neuroscience course may be found [here](https://contextlab.github.io/course-content/tutorials/intro.html), and an enhanced version of the deep learning course may be found [here](https://contextlab.github.io/course-content-dl/tutorials/intro.html).

## Installing and enabling Chatify

To install and enable chatify in any Jupyter (iPython) notebook, add the following two cells to the top of your notebook (and run them):

```python
%pip install davos
import davos
davos.config.suppress_stdout = True
```

```python
smuggle chatify   # pip: git+https://github.com/ContextLab/chatify.git
%load_ext chatify
```

No further setup is required.  To interact with Chatify about any code in the notebook, simply insert the `%%explain` magic command at the top of the code cell and then run it (shift + enter) to access the Chatify interface.  To disable Chatify and run the code block as usual, just delete the `%%explain` command and re-run the cell (e.g., by pressing shift + enter again).

## Customizing Chatify

Chatify is designed to work by default in the free tiers of [Colaboratory](https://colab.research.google.com/) and [Kaggle](https://www.kaggle.com/code) notebooks, and to operate without requiring any additional costs or setup beyond installing and enabling Chatify itself.

Chatify is designed to work on a variety of systems and setups, including the "free" tiers on Google Colaboratory and Kaggle.  For setups with additional resources, it is possible to switch to better-performing models.  Chatify works on CPU-only environments, but is GPU-friendly (for both CUDA-enabled and Metal-enabled systems).  We support any text-generation model on [Hugging Face](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending), Meta's [Llama 2](https://ai.meta.com/resources/models-and-libraries/llama-downloads/) models, and OpenAI's [ChatGPT](https://chat.openai.com/) models (both ChatGPT-3.5 and ChatGPT-4).  Models that run on Hugging Face or OpenAI's servers require either a [Hugging Face API key](https://huggingface.co/docs/api-inference/quicktour#get-your-api-token) or an [OpenAI API key](https://platform.openai.com/signup), respectively.

Once you have your API key(s), if needed, create a `config.yaml` file in the directory where you launch your notebook.  For the OpenAI configuration, replace `<OPANAI API KEY>` with your actual OpenAI API key (with no quotes) and then create a `config.yaml` file with the following contents:

### OpenAI configuration

```yaml
cache_config:
  cache: False
  caching_strategy: exact  # alternative: similarity
  cache_db_version: 0.1
  url: <URL> # ignore this

feedback: False

model_config:
  open_ai_key: <OPENAI API KEY>
  model: open_ai_model
  model_name: gpt-4  # alternative: for debugging consider using gpt-3.5-turbo (cheaper and faster, but lower-quality responses)
  max_tokens: 1024

chain_config:
  chain_type: default

prompts_config:
  prompts_to_use: [tutor, tester, inventer, experimenter]
```

### Hugging Face configuration (local)

```yaml
cache_config:
  cache: False
  caching_strategy: exact  # alternative: similarity
  cache_db_version: 0.1
  url: <URL> # ignore this

feedback: False

model_config:
  open_ai_key: <OPENAI API KEY>
  model: huggingface_model
  model_name: TheBloke/Llama-2-70B-Chat-GGML  # replace with any text-generation model
  max_tokens: 1024
  n_gpu_layers: 40
  n_batch: 512

chain_config:
  chain_type: default

prompts_config:
  prompts_to_use: [tutor, tester, inventer, experimenter]
```

### Llama 2 configuration

```yaml
cache_config:
  cache: False
  caching_strategy: exact  # alternative: similarity
  cache_db_version: 0.1
  url: <URL> # ignore this

feedback: False

model_config:
  open_ai_key: <OPENAI API KEY>
  model: llama_model
  model_name: TheBloke/Llama-2-70B-Chat-GGML  # can replace "70B" with either "7B" or "13B" in this line and the next
  weights_fname: llama-2-70b-chat.ggmlv3.q5_1.bin
  max_tokens: 1024
  n_gpu_layers: 40
  n_batch: 512

chain_config:
  chain_type: default

prompts_config:
  prompts_to_use: [tutor, tester, inventer, experimenter]
```

After saving your `config.yaml` file, follow the "[**Installing and enabling Chatify**](README.md#installing-and-enabling-chatify)" instructions.


# What do I do if I have questions or problems?

We'd love to hear from you!  Please consider filling out our [feedback survey](https://forms.gle/V9ZGssyukjmFR9bk7) or submitting an [issue](https://github.com/ContextLab/chatify/issues).


# I want to help!

Yay-- welcome 🎉!  This is a new project (in the "concept" phase) and we're looking for all the help we can get!  If you're new around here and want to explore/contribute, here's how:

1. [Fork](https://github.com/ContextLab/chatify/fork) this repository so that you can work with your own "copy" of the code base
2. Take a look at our [Project Board](https://github.com/orgs/ContextLab/projects/3) and/or the list of open [issues](https://github.com/ContextLab/chatify/issues) to get a sense of the current project status, todo list, etc.
3. Feel free to add your own issues/tasks, comment on existing issues, etc.

## Current priorities and suggested tasks to start with

In general, we've broken down tasks into ["coding" tasks](https://github.com/ContextLab/chatify/labels/coding%20required) (which require some amount of coding, likely in Python) and ["non-coding" tasks](https://github.com/ContextLab/chatify/labels/non-coding) (which do *not* require coding).

If you have questions, ideas, etc., also please check out the [discussion board](https://github.com/ContextLab/chatify/discussions)!
