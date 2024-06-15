import json
import colorsys
from django import template

register = template.Library() 

@register.filter
def hex_to_rgb(hex_color):
    """
    Converts a hexadecimal color code to RGB format.

    Args:
        hex_color (str): The hexadecimal color code to convert.

    Returns:
        tuple: A tuple representing the RGB values of the color.

    Example:
        >>> hex_to_rgb('#FF0000')
        (255, 0, 0)
    """
    hex_color = hex_color.lstrip('#') 
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


@register.filter
def hex_to_hls(hex_color):
    """
    Converts a hexadecimal color code to HLS format.

    Args:
        hex_color (str): The hexadecimal color code to convert.

    Returns:
        tuple: A tuple representing the HLS values of the color.

    Example:
        >>> hex_to_hls('#FF0000')
        (0.0, 0.5, 1.0)
    """
    r, g, b = hex_to_rgb(hex_color) 
    # build the HLS h=0-255, l=0-100%, S=0-100%
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    return f'{round(h*360)}', f'{int(round(l*100))}%', f'{round(s*100)}%'