"""
Cel-Logic Pro — Full Reset / Cleanup Operator
Removes ALL Cel-Logic data from the active object in one click.
"""

import bpy
from ..registry import register_class
from ..core.engine import require_engine
from ..api.materials import remove_materials_by_suffix, remove_material_by_name
from ..api.modifiers import remove_modifier
from ..api.drivers import remove_all_drivers
from ..config import (
    SKIN_MAT_SUFFIX, EYE_MAT_SUFFIX, MOUTH_MAT_SUFFIX,
    OUTLINE_MAT_NAME, OUTLINE_GP_NAME, MOD_SOLIDIFY,
    ILM_LAYER, BLUSH_LAYER, MOD_DATA_TRANSFER,
)
from .. import logger


@register_class
class CELLOGIC_OT_full_reset(bpy.types.Operator):
    """Remove ALL Cel-Logic materials, modifiers, drivers, and vertex colours"""
    bl_idname = "cellogic.full_reset"
    bl_label = "Full Cel-Logic Reset"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH' and context.mode == 'OBJECT'

    def execute(self, context):
        if not require_engine(self, context):
            return {'CANCELLED'}

        obj = context.active_object

        # — Materials —
        removed = 0
        for suffix in (SKIN_MAT_SUFFIX, EYE_MAT_SUFFIX, MOUTH_MAT_SUFFIX):
            removed += remove_materials_by_suffix(obj, suffix)
        # Outline uses exact name, not suffix
        if remove_material_by_name(obj, OUTLINE_MAT_NAME):
            removed += 1

        # — Modifiers (legacy Solidify + DataTransfer) —
        remove_modifier(obj, MOD_SOLIDIFY)
        remove_modifier(obj, MOD_DATA_TRANSFER)

        # — GP Outline object —
        gp_name = f"{obj.name}{OUTLINE_GP_NAME}"
        gp_obj = bpy.data.objects.get(gp_name)
        if gp_obj:
            gp_data = gp_obj.data
            bpy.data.objects.remove(gp_obj, do_unlink=True)
            if gp_data and gp_data.users == 0:
                bpy.data.grease_pencils_v3.remove(gp_data)

        # — Drivers —
        remove_all_drivers(obj)

        # — Vertex colour layers —
        mesh = obj.data
        if hasattr(mesh, 'color_attributes'):
            for layer_name in (ILM_LAYER, BLUSH_LAYER):
                layer = mesh.color_attributes.get(layer_name)
                if layer:
                    mesh.color_attributes.remove(layer)
        elif hasattr(mesh, 'vertex_colors'):
            for layer_name in (ILM_LAYER, BLUSH_LAYER):
                layer = mesh.vertex_colors.get(layer_name)
                if layer:
                    mesh.vertex_colors.remove(layer)

        # — Reset property groups —
        for attr in ('cl_proxy', 'cl_outline', 'cl_skin', 'cl_eyes', 'cl_blush', 'cl_mouth'):
            pg = getattr(obj, attr, None)
            if pg and hasattr(pg, 'enabled'):
                pg.enabled = False

        # — Face proxy child —
        proxy_name = getattr(obj, 'cl_proxy', None)
        if proxy_name:
            pn = getattr(proxy_name, 'proxy_name', '')
            child = bpy.data.objects.get(pn)
            if child:
                bpy.data.objects.remove(child, do_unlink=True)

        # — Light group —
        obj.lightgroup = ""

        logger.info(f"Full reset on '{obj.name}': {removed} material(s) removed")
        self.report({'INFO'}, f"All Cel-Logic data removed from '{obj.name}'")
        return {'FINISHED'}
