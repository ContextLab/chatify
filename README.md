# Chatify
[![DOI](https://zenodo.org/badge/627651845.svg)](https://zenodo.org/badge/latestdoi/627651845)

<img src="https://raw.githubusercontent.com/ContextLab/chatify/main/docs/images/greeting.png" alt="greeting" width="400"/>

Chatify is a python package that enables ipython magic commands to Jupyter notebooks that provide LLM-driven enhancements to markdown and code cells.  This package is currently in the *alpha* stage: expect broken things, crashes, bad (wrong, misleading) answers, and other serious issues.  That said, we think Chatify is pretty neat even in this early form, and we're excited about its future!

# Background

This tool was originally created to supplement the [Neuromatch Academy](https://compneuro.neuromatch.io/tutorials/intro.html) materials.  A "Chatify-enhanced" version of the Neuromatch computational neuroscience course may be found [here](https://contextlab.github.io/course-content/tutorials/intro.html), and an enhanced version of the deep learning course may be found [here](https://contextlab.github.io/course-content-dl/tutorials/intro.html).

## Installing and enabling Chatify

To install and enable chatify in any Jupyter (iPython) notebook, add the following two cells to the top of your notebook (and run them):

```python
%pip install davos
import davos
davos.config.suppress_stdout = True
```

```python
smuggle chatify
%load_ext chatify
```

No further setup is required.  To interact with Chatify about any code in the notebook, simply insert the `%%explain` magic command at the top of the code cell and then run it (shift + enter) to access the Chatify interface.  To disable Chatify and run the code block as usual, just delete the `%%explain` command and re-run the cell (e.g., by pressing shift + enter again).

### Why those two cells?

The first cell installs and enables the [Davos](https://github.com/ContextLab/davos) library, which is used to safely manage Python dependencies in Jupyter notebooks. Importing Davos provides access to the `smuggle` keyword.  The `smuggle` keyword is like a safer and more robust version of `import`; if the requested package isn't available in the current environment, it will be automatically installed and imported. Importantly, any newly installed packages are automatically isolated in a virtual environment.  This prevents Chatify or its dependencies from interfering with other packages that might be installed on your system.

The `smuggle` statement in the second cell is what actually installs, configures, and imports Chatify, and the `%load_ext` line loads and enables the Chatify extension (accessed by adding the `%%explain` magic command to the top of any code cell in the notebook).

If you don't care about protecting your runtime environment from potential side effects of installing Chatify (note: this is **not recommended** and may **break other aspects of your setup**!), you can replace those two cells above with the following:

```python
!pip install -qqq chatify
import chatify
%load_ext chatify
```

Note: the quiet (`-qqq`) flags are optional, but including them will avoid cluttering up your notebook with installation-related messages.  It's probably fine to use this "direct/unsafe install" method if you're running Chatify in a Colab notebook, inside of a container, or in a dedicated virtual environment, but you shouldn't install the unsafe version of Chatify locally. GPU-friendly libraries are notoriously finicky, and since Chatify will mess with some of those libraries it's reasonably likely that your other GPU libraries will stop working correctly if you don't isolate Chatify's effects on your system.

### I like to live on the wild side-- give me the bleeding edge version! 

Psst...if you really want to see our lack of quality control on full display, we can tell you the secret password 🤫. Step this way...that's right. Don't mind those animals, pay no attention...🐯🦁🦎...🦌🐘🐬🦕...to install Chatify directly from GitHub (**even though this is not recommended!!**), with no safety checks or guarantees whatsoever, you can add and run this cell to the top of your notebook:

```python
!pip install -qqq chatify git+https://github.com/ContextLab/chatify.git
import chatify
%load_ext chatify
```

You should really only do this in a fully protected (containerized, virtual)
environment or on Colab, since it could break other stuff on your system. Don't
say we didn't warn you!

## Customizing Chatify

Chatify is designed to work by default in the free tiers of [Colaboratory](https://colab.research.google.com/) and [Kaggle](https://www.kaggle.com/code) notebooks, and to operate without requiring any additional costs or setup beyond installing and enabling Chatify itself. There's some server magic that happens behind the scenes to make that happen.  In addition to Colaboratory and Kaggle notebooks, Chatify also supports a variety of other systems and setups, including running locally or on other cloud-based systems (e.g., if you don't want our servers to see what you're doing 🕵️).  For setups with additional resources, it is possible to switch to better-performing or lower-cost models.  Chatify works in CPU-only environments, but it is GPU-friendly (for both CUDA-enabled and Metal-enabled systems).  We support any text-generation model on [Hugging Face](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending), Meta's [Llama 2](https://ai.meta.com/resources/models-and-libraries/llama-downloads/) models, and OpenAI's [ChatGPT](https://chat.openai.com/) models (e.g., ChatGPT-3.5 and ChatGPT-4).  Models that run on Hugging Face or OpenAI's servers require either a [Hugging Face API key](https://huggingface.co/docs/api-inference/quicktour#get-your-api-token) or an [OpenAI API key](https://platform.openai.com/signup), respectively.

Once you have your API key(s), if needed, create a `config.yaml` file in the directory where you launch your notebook.  For the OpenAI configuration, replace `<OPANAI API KEY>` with your actual OpenAI API key (with no quotes) and then create a `config.yaml` file with the following contents:

### OpenAI configuration

If you have an OpenAI API key, adding this config.yaml file to your local directory (after adding your API key) will substantially improve your experience by generating higher quality responses:

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
  model_name: gpt-4
  max_tokens: 2500

chain_config:
  chain_type: default

prompts_config:
  prompts_to_use: [tutor, tester, inventer, experimenter]
```

### Llama 2 configuration

If you're running your notebook on a well-resourced machine, you can use this config file to get good performance for free, and without using our servers!  The 7B and 13B variants of llama 2 both run on the free tier of Google Colaboratory and Kaggle, but the 13B is substantially slower (therefore we recommend the 7B variant if you're using Colaboratory or Kaggle notebooks). Note that using this configuration requires installing the "HuggingFace" dependencies (`pip install chatify[hf]`).

```yaml
cache_config:
  cache: False
  caching_strategy: exact  # alternative: similarity
  cache_db_version: 0.1
  url: <URL> # ignore this

feedback: False

model_config:
  model: llama_model
  model_name: TheBloke/Llama-2-70B-Chat-GGML  # can also replace "70B" with either "7B" or "13B" on this line and the next
  weights_fname: llama-2-70b-chat.ggmlv3.q5_1.bin
  max_tokens: 2500
  n_gpu_layers: 40
  n_batch: 512

chain_config:
  chain_type: default

prompts_config:
  prompts_to_use: [tutor, tester, inventer, experimenter]
```

### Hugging Face configuration (local)

If you're running your notebook on a well-resourced machine, you can use this config file to get good performance for free, and without using our servers! For most models this will require lots of RAM. It's a nice way to explore a wide variety of models.  Note that using this configuration requires installing the "HuggingFace" dependencies (`pip install chatify[hf]`).

```yaml
cache_config:
  cache: False
  caching_strategy: exact  # alternative: similarity
  cache_db_version: 0.1
  url: <URL> # ignore this

feedback: False

model_config:
  model: huggingface_model
  model_name: TheBloke/Llama-2-70B-Chat-GGML  # replace with any text-generation model on Hugging Face!
  max_tokens: 2500
  n_gpu_layers: 40
  n_batch: 512

chain_config:
  chain_type: default

prompts_config:
  prompts_to_use: [tutor, tester, inventer, experimenter]
```

After saving your `config.yaml` file, follow the "[**Installing and enabling Chatify**](README.md#installing-and-enabling-chatify)" instructions.


# What do I do if I have questions or problems?

We'd love to hear from you 🤩!  If you're using Chatify as part of one of the NMA courses, please consider filling out our [feedback survey](https://forms.gle/V9ZGssyukjmFR9bk7) to help us improve and/or better understand the experience. For more general problems, please submit an [issue](https://github.com/ContextLab/chatify/issues). And for other questions, comments, concerns, etc., just send us an [email](contextualdynamics@gmail.com).


# I want to help!

Yay-- welcome 🎉!  This is a *very* new project (in the "alpha" phase) and we're looking for all the help we can get!  If you're new around here and want to explore/contribute, here's how:

1. [Fork](https://github.com/ContextLab/chatify/fork) this repository so that you can work with your own "copy" of the code base
2. Take a look at our [Project Board](https://github.com/orgs/ContextLab/projects/3) and/or the list of open [issues](https://github.com/ContextLab/chatify/issues) to get a sense of the current project status, todo list, etc.
3. Feel free to add your own issues/tasks, comment on existing issues, etc.

## Current priorities and suggested tasks to start with

In general, we've broken down tasks into ["coding" tasks](https://github.com/ContextLab/chatify/labels/coding%20required) (which require some amount of coding, likely in Python) and ["non-coding" tasks](https://github.com/ContextLab/chatify/labels/non-coding) (which do *not* require coding).

If you have questions, ideas, etc., also please check out the [discussion board](https://github.com/ContextLab/chatify/discussions)!
