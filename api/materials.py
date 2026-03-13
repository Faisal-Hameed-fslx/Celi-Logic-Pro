"""
Cel-Logic Pro — Materials API
All material creation, assignment, and node tree manipulation goes through here.
"""

import bpy
from ..core.exceptions import MaterialError
from .. import logger


# ═══════════════════════════════════════════════════════
# MATERIAL CRUD
# ═══════════════════════════════════════════════════════

def create_material(name):
    """Create or retrieve a material. Always has use_nodes=True."""
    mat = bpy.data.materials.get(name)
    if mat is not None:
        return mat
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    logger.debug(f"Created material '{name}'")
    return mat


def assign_material(obj, mat, slot_index=None):
    """Assign material to object. Appends if slot_index is None."""
    if obj is None or mat is None:
        return False
    if slot_index is not None and slot_index < len(obj.material_slots):
        obj.material_slots[slot_index].material = mat
    else:
        obj.data.materials.append(mat)
    return True


def find_material_by_suffix(obj, suffix):
    """Find first material on obj whose name ends with suffix."""
    if obj is None:
        return None
    for slot in obj.material_slots:
        if slot.material and slot.material.name.endswith(suffix):
            return slot.material
    return None


def has_material_with_suffix(obj, suffix):
    """Check if object has any material ending with suffix."""
    return find_material_by_suffix(obj, suffix) is not None


def remove_materials_by_suffix(obj, suffix):
    """Remove all materials from object whose name ends with suffix."""
    if obj is None or not hasattr(obj.data, 'materials'):
        return 0
    removed = 0
    indices = []
    for i, mat in enumerate(obj.data.materials):
        if mat and mat.name.endswith(suffix):
            indices.append(i)
    for i in reversed(indices):
        obj.data.materials.pop(index=i)
        removed += 1
    if removed:
        logger.debug(f"Removed {removed} material(s) with suffix '{suffix}' from '{obj.name}'")
    return removed


def remove_material_by_name(obj, mat_name):
    """Remove a specific material by exact name from object slots.
    Uses direct data API (no bpy.ops) for Blender 4.x compatibility."""
    if obj is None or not hasattr(obj.data, 'materials'):
        return False
    for i in range(len(obj.data.materials) - 1, -1, -1):
        mat = obj.data.materials[i]
        if mat and mat.name == mat_name:
            obj.data.materials.pop(index=i)
            logger.debug(f"Removed material '{mat_name}' from '{obj.name}'")
            return True
    return False


# ═══════════════════════════════════════════════════════
# NODE TREE HELPERS
# ═══════════════════════════════════════════════════════

def clear_node_tree(mat):
    """Remove all nodes from material's node tree."""
    if mat is None or not mat.use_nodes:
        return
    for node in list(mat.node_tree.nodes):
        mat.node_tree.nodes.remove(node)


def get_or_create_node(node_tree, node_type, name=None, location=(0, 0)):
    """Get existing node by name or create new one."""
    if name and name in node_tree.nodes:
        return node_tree.nodes[name]
    node = node_tree.nodes.new(type=node_type)
    if name:
        node.name = name
        node.label = name
    node.location = location
    return node


def safe_link(node_tree, from_socket, to_socket):
    """Safely create a link between two sockets."""
    try:
        node_tree.links.new(from_socket, to_socket)
        return True
    except Exception as e:
        logger.warning(f"Failed to link {from_socket} → {to_socket}: {e}")
        return False
