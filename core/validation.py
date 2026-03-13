"""
Cel-Logic Pro — Validation Helpers
Pre-flight checks for operators. Fail early, fail clearly.
"""

from .exceptions import MissingObjectError


def require_mesh(context, operator=None):
    """Validate active object is a mesh. Returns the object or raises."""
    obj = context.active_object
    if obj is None:
        msg = "No active object selected"
        if operator:
            operator.report({'ERROR'}, msg)
        raise MissingObjectError(msg)
    if obj.type != 'MESH':
        msg = f"'{obj.name}' is not a mesh (type: {obj.type})"
        if operator:
            operator.report({'ERROR'}, msg)
        raise MissingObjectError(msg)
    return obj


def require_object_mode(context, operator=None):
    """Validate we are in Object mode."""
    if context.mode != 'OBJECT':
        msg = "Switch to Object mode first"
        if operator:
            operator.report({'ERROR'}, msg)
        return False
    return True


def require_camera(context, operator=None):
    """Validate an active camera exists. Returns camera or None."""
    camera = context.scene.camera
    if camera is None:
        msg = "No active camera in scene"
        if operator:
            operator.report({'WARNING'}, msg)
        return None
    return camera
