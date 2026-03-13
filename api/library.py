"""
Cel-Logic Pro — Shader Library Loader
Appends pre-built node groups from the Emily Rig blend file.
Falls back to the bundled shader_library.blend for non-Goo groups.
"""

import os
import bpy
from .. import logger

_LIBRARY_FILE = "shader_library.blend"

# Groups that contain Goo Engine custom nodes and must be loaded
# from a full blend file (not a stripped library)
_GOO_GROUPS = {
    "EMILY_Shader", "EMILY_SunBody_Group", "EMILY_SunFace_Group",
    "DillonEeveeToonShader.001", "RimLight", "Hair_Highlights",
    "LightFX.001", "Shadow Caster", "Position Distance",
    "Geometry Nodes", "Geometry Nodes.001",
}


def get_library_path():
    """Return absolute path to the bundled shader_library.blend."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(os.path.dirname(here), "resources", _LIBRARY_FILE)


def _find_emily_blend():
    """Find the Emily Rig blend file.

    Search order:
    1. Addon root folder (next to __init__.py)
    2. EMILY_BLEND_PATH from config (user-configurable)
    3. Parent of addon folder (workspace root)
    """
    from ..config import EMILY_BLEND_PATH

    _EMILY_NAME = "_Emily_Rig_Master_GE.blend"

    # Addon root directory (cel_logic_pro/)
    addon_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    candidates = [
        os.path.join(addon_root, _EMILY_NAME),              # inside addon folder
        EMILY_BLEND_PATH,                                     # config path
        os.path.join(os.path.dirname(addon_root), _EMILY_NAME),  # parent folder
    ]
    for p in candidates:
        if p and os.path.isfile(p):
            return p
    return None


def _load_from_blend(filepath, names):
    """Append node groups from a blend file, skipping already-loaded ones."""
    missing = [n for n in names if n not in bpy.data.node_groups]
    if not missing:
        return

    if not os.path.isfile(filepath):
        logger.warning(f"Blend file not found: {filepath}")
        return

    with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
        available = set(data_from.node_groups)
        to_load = [n for n in missing if n in available]
        data_to.node_groups = to_load

    loaded = [n for n in missing if n in bpy.data.node_groups]
    if loaded:
        logger.debug(f"Loaded node groups from {os.path.basename(filepath)}: {loaded}")

    return [n for n in missing if n not in bpy.data.node_groups]


def ensure_node_groups(names):
    """Append any missing node groups, trying Emily blend first for Goo groups.

    Blender's libraries.load silently drops node groups containing custom
    node types (ShaderInfo, Curvature, etc.) unless the source file was
    saved with Goo Engine and the current session has those types registered.
    The Emily Rig blend file preserves these properly.
    """
    missing = [n for n in names if n not in bpy.data.node_groups]
    if not missing:
        return

    # Try Emily blend for Goo-dependent groups
    goo_needed = [n for n in missing if n in _GOO_GROUPS]
    non_goo_needed = [n for n in missing if n not in _GOO_GROUPS]

    emily_path = _find_emily_blend()
    if emily_path and goo_needed:
        still_missing = _load_from_blend(emily_path, goo_needed)
        if still_missing:
            logger.warning(f"Could not load from Emily: {still_missing}")

    # Try library blend for remaining
    lib_path = get_library_path()
    all_remaining = [n for n in names if n not in bpy.data.node_groups]
    if all_remaining:
        still_missing = _load_from_blend(lib_path, all_remaining)
        if still_missing:
            # Final attempt: try Emily blend for everything
            if emily_path:
                _load_from_blend(emily_path, still_missing)

    final_missing = [n for n in names if n not in bpy.data.node_groups]
    if final_missing:
        logger.warning(f"Node groups not found: {final_missing}")


def copy_node_group(name, new_name):
    """Create a deep copy of a node group, including nested sub-groups.

    Returns the copied group, or None if the source doesn't exist.
    Sub-groups referenced inside are also copied to avoid shared mutations.
    """
    ensure_node_groups([name])
    base = bpy.data.node_groups.get(name)
    if base is None:
        return None

    grp = base.copy()
    grp.name = new_name

    # Deep-copy nested groups so per-material edits don't bleed
    for node in grp.nodes:
        if node.type == 'GROUP' and node.node_tree:
            sub = node.node_tree.copy()
            sub.name = f"{new_name}__{node.node_tree.name}"
            node.node_tree = sub

    return grp


def cleanup_node_groups(prefix):
    """Remove all node groups whose name starts with *prefix*.

    Used when a material is deleted to free per-material copies.
    """
    to_remove = [ng for ng in bpy.data.node_groups if ng.name.startswith(prefix)]
    for ng in to_remove:
        bpy.data.node_groups.remove(ng)
