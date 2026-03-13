"""
Cel-Logic Pro — Vertex Colors API
Manages vertex color layers for ILM shadow painting and blush masking.
"""

import bpy
from ..config import ILM_LAYER, BLUSH_LAYER
from .. import logger


def ensure_layer(obj, layer_name=None):
    """Ensure a vertex color layer exists. Creates if missing. Returns layer."""
    if layer_name is None:
        layer_name = ILM_LAYER
    if obj is None or obj.type != 'MESH':
        return None

    mesh = obj.data

    # Blender 3.2+ / Goo Engine
    if hasattr(mesh, 'color_attributes'):
        layer = mesh.color_attributes.get(layer_name)
        if layer is None:
            layer = mesh.color_attributes.new(
                name=layer_name, type='FLOAT_COLOR', domain='CORNER'
            )
            logger.debug(f"Created color attribute '{layer_name}' on '{obj.name}'")
        return layer

    # Legacy fallback
    if hasattr(mesh, 'vertex_colors'):
        layer = mesh.vertex_colors.get(layer_name)
        if layer is None:
            layer = mesh.vertex_colors.new(name=layer_name)
        return layer

    return None


def has_layer(obj, layer_name):
    """Check if object has a vertex color layer."""
    if obj is None or obj.type != 'MESH':
        return False
    mesh = obj.data
    if hasattr(mesh, 'color_attributes'):
        return mesh.color_attributes.get(layer_name) is not None
    if hasattr(mesh, 'vertex_colors'):
        return mesh.vertex_colors.get(layer_name) is not None
    return False


def fill_channel(obj, layer_name, channel='R', value=0.5):
    """Fill a specific channel to a uniform value. channel: R/G/B/A."""
    if obj is None or obj.type != 'MESH':
        return False

    mesh = obj.data
    layer = None
    if hasattr(mesh, 'color_attributes'):
        layer = mesh.color_attributes.get(layer_name)
    elif hasattr(mesh, 'vertex_colors'):
        layer = mesh.vertex_colors.get(layer_name)
    if layer is None:
        return False

    ch_map = {'R': 0, 'G': 1, 'B': 2, 'A': 3}
    ch_idx = ch_map.get(channel.upper(), 0)

    for color_data in layer.data:
        c = list(color_data.color)
        c[ch_idx] = value
        color_data.color = c

    return True
