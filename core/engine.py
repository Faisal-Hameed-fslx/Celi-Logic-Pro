"""
Cel-Logic Pro — Engine Detection
Goo Engine 4.4 only. Standard Blender / Cycles NOT supported.
"""

import bpy
from ..config import VALID_ENGINES, ENGINE_DISPLAY_NAME, ADDON_NAME, COLOR_MGMT_VIEW_TRANSFORM
from .exceptions import EngineMismatchError
from .. import logger


def is_valid_engine(context=None):
    """
    Check if the current render engine is a valid EEVEE variant.
    Returns True during restricted context (addon install).
    """
    try:
        if context is None:
            context = bpy.context
        scene = getattr(context, 'scene', None)
        if scene is None:
            return True  # Restricted context — assume valid
        return scene.render.engine in VALID_ENGINES
    except (AttributeError, RuntimeError):
        return True  # Restricted context fallback


def get_current_engine(context=None):
    """Return the current render engine ID string, or 'UNKNOWN' on failure."""
    try:
        if context is None:
            context = bpy.context
        scene = getattr(context, 'scene', None)
        if scene is None:
            return "RESTRICTED_CONTEXT"
        return scene.render.engine
    except (AttributeError, RuntimeError):
        return "UNKNOWN"


def require_engine(operator, context):
    """
    Gate for operator.execute(). Returns True if engine is valid.

    Usage:
        if not require_engine(self, context):
            return {'CANCELLED'}
    """
    if is_valid_engine(context):
        return True

    current = get_current_engine(context)
    msg = (
        f"{ADDON_NAME} requires {ENGINE_DISPLAY_NAME}. "
        f"Current engine: {current}"
    )
    operator.report({'ERROR'}, msg)
    logger.warning(msg)
    return False


def assert_engine(context=None):
    """
    Raise EngineMismatchError if engine is invalid.
    For use in API functions that are not operators.
    """
    if not is_valid_engine(context):
        current = get_current_engine(context)
        raise EngineMismatchError(
            f"Requires {ENGINE_DISPLAY_NAME}, got: {current}"
        )


def ensure_goo_color_management(scene=None):
    """Set colour management to Standard for vibrant anime look.

    Called automatically when setting up skin shader.
    """
    if scene is None:
        try:
            scene = bpy.context.scene
        except (AttributeError, RuntimeError):
            return
    try:
        cm = scene.view_settings
        cm.view_transform = COLOR_MGMT_VIEW_TRANSFORM
        cm.look = "None"
        cm.exposure = 0.0
        cm.gamma = 1.0
        logger.debug(f"Color management set to {COLOR_MGMT_VIEW_TRANSFORM}")
    except Exception as e:
        logger.warning(f"Could not set color management: {e}")
