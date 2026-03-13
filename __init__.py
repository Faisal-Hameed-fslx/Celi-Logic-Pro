"""
Cel-Logic Pro 2.0 — Professional Anime Rendering Toolkit for Goo Engine

Registry-based addon architecture:
    1. Importing system/operator/ui modules triggers @register_class decorators
    2. register() calls registry.register_all() which sorts and registers everything
    3. Property groups are attached via registry.register_properties()
"""

bl_info = {
    "name": "Cel-Logic Pro",
    "author": "Cel-Logic Team",
    "version": (2, 0, 0),
    "blender": (4, 4, 0),
    "location": "View3D > Sidebar > Cel-Logic",
    "description": "Professional anime cel-shading toolkit for Goo Engine",
    "category": "Render",
}

import bpy

# ── Registry must be imported first ──
from . import registry
from . import logger

# ── Core infrastructure ──
from .core import engine          # noqa: F401
from .core import exceptions      # noqa: F401
from .core import validation      # noqa: F401
from .core import data_migration  # noqa: F401
from .core import dependency_graph  # noqa: F401

# ── API layer (no classes to register, just functions) ──
from .api import materials        # noqa: F401
from .api import modifiers        # noqa: F401
from .api import drivers          # noqa: F401
from .api import vertex_colors    # noqa: F401
from .api import scene            # noqa: F401

# ── Systems (importing triggers @register_class for PropertyGroups + Operators) ──
from .systems import face_proxy   # noqa: F401
from .systems import outline      # noqa: F401
from .systems import skin         # noqa: F401
from .systems import shader       # noqa: F401
from .systems import eyes         # noqa: F401
from .systems import blush        # noqa: F401
from .systems import mouth        # noqa: F401
from .systems import animation    # noqa: F401  (stub)
from .systems import post         # noqa: F401  (stub)

# ── Cross-system operators ──
from . import operators           # noqa: F401

# ── UI (panels) ──
from . import ui                  # noqa: F401

# ── Property group classes (imported for PointerProperty binding) ──
from .systems.face_proxy.properties import CL_FaceProxyProps
from .systems.outline.properties import CL_OutlineProps
from .systems.skin.properties import CL_SkinProps
from .systems.eyes.properties import CL_EyeProps
from .systems.blush.properties import CL_BlushProps
from .systems.mouth.properties import CL_MouthProps
from .systems.shader.properties import CL_ShaderProps


# ═══════════════════════════════════════════════════════
# PROPERTY ATTACHMENTS
# ═══════════════════════════════════════════════════════
# Scheduled so the registry handles them at register time.

registry.register_properties(bpy.types.Object, "cl_proxy", CL_FaceProxyProps)
registry.register_properties(bpy.types.Object, "cl_outline", CL_OutlineProps)
registry.register_properties(bpy.types.Object, "cl_skin", CL_SkinProps)
registry.register_properties(bpy.types.Object, "cl_eyes", CL_EyeProps)
registry.register_properties(bpy.types.Object, "cl_blush", CL_BlushProps)
registry.register_properties(bpy.types.Object, "cl_mouth", CL_MouthProps)
registry.register_properties(bpy.types.Object, "cl_shader", CL_ShaderProps)


# ═══════════════════════════════════════════════════════
# REGISTER / UNREGISTER
# ═══════════════════════════════════════════════════════

def register():
    logger.info("Cel-Logic Pro — registering …")
    registry.register_all()

    # Run data migration on all scenes (safe on first install)
    try:
        data_migration.migrate_all_scenes()
    except Exception as e:
        logger.warning(f"Data migration skipped: {e}")

    logger.info("Cel-Logic Pro — registered successfully")


def unregister():
    logger.info("Cel-Logic Pro — unregistering …")
    registry.unregister_all()
    logger.info("Cel-Logic Pro — unregistered")
