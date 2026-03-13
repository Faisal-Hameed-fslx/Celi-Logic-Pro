"""
Cel-Logic Pro — Drivers API
Centralized driver creation for animation, noise, and camera compensation.
"""

import bpy
from .. import logger


def add_noise_driver(obj, prop_path, intensity=0.5, prop_index=-1):
    """Add sin-based pseudo-random noise driver."""
    fcurve = obj.driver_add(prop_path, prop_index)
    if fcurve is None:
        return None
    d = fcurve.driver
    d.type = 'SCRIPTED'

    var = d.variables.new()
    var.name = "frame"
    var.type = 'SINGLE_PROP'
    var.targets[0].id_type = 'SCENE'
    var.targets[0].id = bpy.context.scene
    var.targets[0].data_path = "frame_current"

    d.expression = f"{intensity} * sin(frame * 12.345 + 67.89) * sin(frame * 3.456)"
    logger.debug(f"Added noise driver on '{obj.name}'.{prop_path}")
    return fcurve


def add_camera_distance_driver(obj, prop_path, fallback=1.0, prop_index=-1):
    """Add driver that scales property by camera distance."""
    camera = bpy.context.scene.camera
    if camera is None:
        return None

    fcurve = obj.driver_add(prop_path, prop_index)
    if fcurve is None:
        return None
    d = fcurve.driver
    d.type = 'SCRIPTED'

    var = d.variables.new()
    var.name = "cam_dist"
    var.type = 'LOC_DIFF'
    var.targets[0].id = obj
    var.targets[1].id = camera

    d.expression = f"{fallback} * (cam_dist / 10.0)"
    return fcurve


def add_frame_step(fcurve, step=2):
    """Add stepped interpolation modifier to an f-curve."""
    if fcurve is None:
        return
    mod = fcurve.modifiers.new(type='STEPPED')
    mod.frame_step = step
    mod.use_frame_start = False
    mod.use_frame_end = False


def remove_driver(obj, prop_path, index=-1):
    """Safely remove a driver from a property path."""
    try:
        obj.driver_remove(prop_path, index)
        return True
    except Exception:
        return False


def remove_all_drivers(obj):
    """Remove all drivers from an object."""
    if obj is None or not hasattr(obj, 'animation_data') or obj.animation_data is None:
        return
    for driver in list(obj.animation_data.drivers):
        try:
            obj.driver_remove(driver.data_path, driver.array_index)
        except Exception:
            pass
