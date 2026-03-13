"""
Cel-Logic Pro — Scene API
Camera utilities, light group management, scene-level operations.
"""

import bpy
import mathutils
from ..config import HERO_LIGHT_GROUP
from .. import logger


# ═══════════════════════════════════════════════════════
# CAMERA
# ═══════════════════════════════════════════════════════

def get_camera(context=None):
    """Get active scene camera, or None."""
    if context is None:
        context = bpy.context
    return context.scene.camera


def camera_distance(obj, context=None):
    """Distance between object and active camera. Falls back to 10.0."""
    cam = get_camera(context)
    if cam is None or obj is None:
        return 10.0
    return (cam.location - obj.location).length


def camera_view_vector(context=None):
    """Camera forward direction (world space). Falls back to -Z."""
    cam = get_camera(context)
    if cam is None:
        return mathutils.Vector((0, 0, -1))
    return -cam.matrix_world.col[2].xyz.normalized()


# ═══════════════════════════════════════════════════════
# LIGHT GROUPS
# ═══════════════════════════════════════════════════════

def ensure_light_group(name=None, view_layer=None):
    """Create HERO_RIG light group if missing. Returns the lightgroup."""
    if name is None:
        name = HERO_LIGHT_GROUP
    if view_layer is None:
        view_layer = bpy.context.view_layer

    for lg in view_layer.lightgroups:
        if lg.name == name:
            return lg

    bpy.ops.scene.view_layer_add_lightgroup(name=name)
    logger.debug(f"Created light group '{name}'")

    for lg in view_layer.lightgroups:
        if lg.name == name:
            return lg
    return None


def assign_light_group(obj, group_name=None):
    """Assign object to a light group."""
    if group_name is None:
        group_name = HERO_LIGHT_GROUP
    if obj is None:
        return False
    obj.lightgroup = group_name
    return True


def ensure_hero_sun(group_name=None):
    """Create or find the CelLogic hero sun light. Returns light object."""
    if group_name is None:
        group_name = HERO_LIGHT_GROUP

    for obj in bpy.data.objects:
        if obj.type == 'LIGHT' and obj.name.startswith("CelLogic_HeroSun"):
            return obj

    bpy.ops.object.light_add(type='SUN', location=(0, 0, 5))
    sun = bpy.context.active_object
    sun.name = "CelLogic_HeroSun"
    sun.lightgroup = group_name
    logger.debug("Created CelLogic_HeroSun")
    return sun
