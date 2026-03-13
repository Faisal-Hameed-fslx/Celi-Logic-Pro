"""
Cel-Logic Pro — Scene Audit Operator
Summarises Cel-Logic state of every mesh in the scene.
"""

import bpy
from ..registry import register_class
from ..core.engine import require_engine
from ..api.materials import has_material_with_suffix
from ..api.modifiers import has_modifier
from ..api.vertex_colors import has_layer
from ..config import (
    SKIN_MAT_SUFFIX, EYE_MAT_SUFFIX, OUTLINE_MAT_NAME,
    OUTLINE_GP_NAME, MOD_SOLIDIFY, ILM_LAYER, BLUSH_LAYER
)


@register_class
class CELLOGIC_OT_scene_audit(bpy.types.Operator):
    """Print a summary of Cel-Logic setup for every mesh"""
    bl_idname = "cellogic.scene_audit"
    bl_label = "Cel-Logic Scene Audit"
    bl_options = {'REGISTER'}

    def execute(self, context):
        if not require_engine(self, context):
            return {'CANCELLED'}

        meshes = [o for o in bpy.data.objects if o.type == 'MESH']
        if not meshes:
            self.report({'INFO'}, "No meshes in scene.")
            return {'FINISHED'}

        lines = ["=== Cel-Logic Scene Audit ==="]
        for obj in sorted(meshes, key=lambda o: o.name):
            flags = []
            if hasattr(obj, 'cl_proxy') and obj.cl_proxy.enabled:
                flags.append("FaceProxy")
            # GP Line Art outline (new system)
            gp_name = f"{obj.name}{OUTLINE_GP_NAME}"
            if bpy.data.objects.get(gp_name):
                flags.append("LineArt")
            # Legacy: outline material on mesh
            for slot in obj.material_slots:
                if slot.material and slot.material.name == OUTLINE_MAT_NAME:
                    flags.append("Outline(legacy)")
                    break
            if has_modifier(obj, MOD_SOLIDIFY):
                flags.append("Solidify(legacy)")
            if has_material_with_suffix(obj, SKIN_MAT_SUFFIX):
                flags.append("Skin")
            if has_material_with_suffix(obj, EYE_MAT_SUFFIX):
                flags.append("Eyes")
            if has_layer(obj, ILM_LAYER):
                flags.append("ILM")
            if has_layer(obj, BLUSH_LAYER):
                flags.append("Blush")
            if hasattr(obj, 'cl_blush') and obj.cl_blush.enabled:
                flags.append("BlushActive")
            if hasattr(obj, 'lightgroup') and obj.lightgroup:
                flags.append(f"LG:{obj.lightgroup}")

            status = ", ".join(flags) if flags else "—"
            lines.append(f"  {obj.name}: {status}")

        report = "\n".join(lines)
        print(report)
        self.report({'INFO'}, f"Audit complete — {len(meshes)} mesh(es). See console.")
        return {'FINISHED'}
