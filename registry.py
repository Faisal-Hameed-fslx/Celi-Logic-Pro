"""
Cel-Logic Pro — Central Registry
Deterministic class registration with automatic priority ordering.

Usage:
    from .registry import register_class

    @register_class
    class MY_OT_operator(bpy.types.Operator):
        ...

Registration order is handled automatically:
    PropertyGroups → Operators → Panels
"""

import bpy

_CLASSES = []
_PROPERTY_ATTACHMENTS = []


def register_class(cls):
    """Decorator: schedule a bpy class for registration."""
    _CLASSES.append(cls)
    return cls


def register_properties(blender_type, attr_name, prop_group):
    """Schedule a PointerProperty attachment for register time."""
    _PROPERTY_ATTACHMENTS.append((blender_type, attr_name, prop_group))


def _sort_classes():
    """Sort classes: PropertyGroups → Operators/Other → Panels."""
    props = []
    operators = []
    panels = []
    others = []

    for cls in _CLASSES:
        if issubclass(cls, bpy.types.PropertyGroup):
            props.append(cls)
        elif issubclass(cls, bpy.types.Panel):
            panels.append(cls)
        elif issubclass(cls, bpy.types.Operator):
            operators.append(cls)
        else:
            others.append(cls)

    return props + operators + others + panels


def register_all():
    """Register all collected classes and attach properties."""
    from . import logger

    ordered = _sort_classes()
    for cls in ordered:
        try:
            bpy.utils.register_class(cls)
        except Exception as e:
            logger.error(f"Failed to register {cls.__name__}: {e}")

    for blender_type, attr_name, prop_group in _PROPERTY_ATTACHMENTS:
        try:
            setattr(blender_type, attr_name, bpy.props.PointerProperty(type=prop_group))
        except Exception as e:
            logger.error(f"Failed to attach {attr_name}: {e}")

    logger.info(f"Registered {len(ordered)} classes, {len(_PROPERTY_ATTACHMENTS)} properties")


def unregister_all():
    """Unregister all classes and detach properties in reverse order."""
    from . import logger

    for blender_type, attr_name, _ in reversed(_PROPERTY_ATTACHMENTS):
        try:
            delattr(blender_type, attr_name)
        except Exception:
            pass

    ordered = _sort_classes()
    for cls in reversed(ordered):
        try:
            bpy.utils.unregister_class(cls)
        except Exception as e:
            logger.error(f"Failed to unregister {cls.__name__}: {e}")

    logger.info("Unregistered all classes")
