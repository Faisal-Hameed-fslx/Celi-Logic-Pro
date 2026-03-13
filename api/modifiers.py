"""
Cel-Logic Pro — Modifiers API
Modifier creation, reordering, and removal.
Enforces stack order: Lattice → Armature → Data Transfer → Solidify
"""

import bpy
from ..config import MODIFIER_ORDER
from .. import logger


def add_modifier(obj, mod_type, mod_name, **kwargs):
    """Add a modifier if one with mod_name doesn't exist. Returns modifier."""
    if obj is None or obj.type != 'MESH':
        return None
    existing = obj.modifiers.get(mod_name)
    if existing is not None:
        return existing
    mod = obj.modifiers.new(name=mod_name, type=mod_type)
    for key, value in kwargs.items():
        if hasattr(mod, key):
            setattr(mod, key, value)
    logger.debug(f"Added modifier '{mod_name}' ({mod_type}) to '{obj.name}'")
    return mod


def remove_modifier(obj, mod_name):
    """Remove modifier by name. Returns True if removed."""
    if obj is None or obj.type != 'MESH':
        return False
    mod = obj.modifiers.get(mod_name)
    if mod is not None:
        obj.modifiers.remove(mod)
        logger.debug(f"Removed modifier '{mod_name}' from '{obj.name}'")
        return True
    return False


def has_modifier(obj, mod_name):
    """Check if object has a modifier with given name."""
    if obj is None or obj.type != 'MESH':
        return False
    return obj.modifiers.get(mod_name) is not None


def enforce_modifier_order(obj):
    """Sort CelLogic modifiers to match MODIFIER_ORDER. Others stay in place."""
    if obj is None or obj.type != 'MESH' or len(obj.modifiers) == 0:
        return

    cel_mods = [m.name for m in obj.modifiers if m.name in MODIFIER_ORDER]
    cel_mods.sort(key=lambda n: MODIFIER_ORDER.index(n))

    current_idx = 0
    for mod_name in cel_mods:
        mod = obj.modifiers.get(mod_name)
        if mod is None:
            continue
        mod_index = list(obj.modifiers).index(mod)
        while mod_index > current_idx:
            with bpy.context.temp_override(object=obj):
                bpy.ops.object.modifier_move_up(modifier=mod_name)
            mod_index -= 1
        current_idx += 1
