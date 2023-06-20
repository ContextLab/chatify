import ipywidgets as widgets
import IPython


def option_widget(config):
    """Create an options dropdown widget based on the given configuration.

    Parameters
    ----------
    config : dict
        Configuration for the options.

    Returns
    -------
    options : widgets.Dropdown
        Dropdown widget containing the options.
    """
    keys = list(config.keys())
    options = widgets.Dropdown(
        options=keys,
        value=keys[0],
        description='Options:',
    )
    return options


def button_widget():
    """Create a button widget.

    Returns
    -------
    button : widgets.Button
        Button widget.
    """
    button = widgets.Button(
        description='Explain',
        disabled=False,
        button_style='',
        tooltip='Get',
        icon='fa-comments',
    )
    return button


def thumbs(icon='fa-thumbs-up'):
    """Create a thumbs-up button widget.

    Parameters
    ----------
    icon : str, optional
        Icon class for the button, by default 'fa-thumbs-up'.

    Returns
    -------
    button : widgets.Button
        Thumbs-up button widget.
    """
    button = widgets.Button(
        description='',
        disabled=False,
        button_style='',
        icon=icon,
        layout=widgets.Layout(width='5%'),
    )
    return button


def text_widget():
    """Create a text widget.

    Returns
    -------
    text : widgets.HTMLMath
        HTMLMath widget for displaying text.
    """
    text = widgets.HTMLMath(
        value='', placeholder='', description='', style=dict(font_size='14px')
    )
    return text
