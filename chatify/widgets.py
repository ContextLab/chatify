import ipywidgets as widgets
import IPython


def option_widget(config):
    keys = list(config.keys())
    options = widgets.Dropdown(
        options=keys,
        value=keys[0],
        description='Options:',
    )
    return options


def button_widget():
    button = widgets.Button(
        description='Explain',
        disabled=False,
        button_style='',
        tooltip='Chatify',
        icon='fa-comments',
    )
    return button


def thumbs(icon='fa-thumbs-up'):
    button = widgets.Button(
        description='',
        disabled=False,
        button_style='',
        icon=icon,
    )
    return button


def text_widget():
    text = widgets.HTMLMath(
        value='', placeholder='', description='', style=dict(font_size='14px')
    )
    return text
