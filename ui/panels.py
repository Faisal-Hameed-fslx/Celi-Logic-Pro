"""
Cel-Logic Pro — UI Panels
ALL panels in one file, registered via @register_class.
"""

import bpy
from ..registry import register_class
from ..config import VALID_ENGINES
from .layouts import draw_section, draw_prop_row, draw_operator_row


# ═══════════════════════════════════════════════════════
# MAIN PANEL
# ═══════════════════════════════════════════════════════

@register_class
class CELLOGIC_PT_main(bpy.types.Panel):
    """Cel-Logic Pro — Main"""
    bl_label = "Cel-Logic Pro"
    bl_idname = "CELLOGIC_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cel-Logic"

    def draw(self, context):
        layout = self.layout
        engine = context.scene.render.engine
        if engine not in VALID_ENGINES:
            layout.label(text="Goo Engine / EEVEE required", icon='ERROR')
            return
        layout.label(text="Goo Engine detected", icon='CHECKMARK')
        obj = context.active_object
        if obj and obj.type == 'MESH':
            layout.label(text=f"Active: {obj.name}", icon='MESH_DATA')
        else:
            layout.label(text="Select a mesh object", icon='INFO')


# ═══════════════════════════════════════════════════════
# MODULE 1 — FACE PROXY
# ═══════════════════════════════════════════════════════

@register_class
class CELLOGIC_PT_face_proxy(bpy.types.Panel):
    """Face Proxy controls"""
    bl_label = "Face Proxy"
    bl_idname = "CELLOGIC_PT_face_proxy"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cel-Logic"
    bl_parent_id = "CELLOGIC_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        props = obj.cl_proxy

        if not props.enabled:
            draw_operator_row(layout, "cellogic.generate_proxy",
                              "Generate Proxy", icon='FACESEL')
        else:
            col = draw_section(layout, "Proxy Settings", icon='FACESEL')
            draw_prop_row(col, props, "scale")
            draw_prop_row(col, props, "x_offset", text="X Offset")
            draw_prop_row(col, props, "y_offset", text="Y Offset")
            draw_prop_row(col, props, "z_offset", text="Z Offset")
            col.separator()
            draw_operator_row(col, "cellogic.toggle_proxy_visibility",
                              "Toggle Visibility")
            col.separator()
            draw_operator_row(col, "cellogic.delete_proxy",
                              "Delete Proxy", icon='TRASH')


# ═══════════════════════════════════════════════════════
# MODULE 2 — OUTLINE
# ═══════════════════════════════════════════════════════

@register_class
class CELLOGIC_PT_outline(bpy.types.Panel):
    """Line Art Outline controls (Goo Engine GP)"""
    bl_label = "Outline"
    bl_idname = "CELLOGIC_PT_outline"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cel-Logic"
    bl_parent_id = "CELLOGIC_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        props = obj.cl_outline

        if not props.enabled:
            draw_operator_row(layout, "cellogic.add_outline",
                              "Add Outline", icon='GREASEPENCIL')
        else:
            col = draw_section(layout, "Line Art Settings", icon='GREASEPENCIL')
            draw_prop_row(col, props, "thickness")
            draw_prop_row(col, props, "opacity", text="Opacity")
            col.separator()
            col.label(text="Edge Types:")
            row = col.row(align=True)
            row.prop(props, "use_contour", text="Contour", toggle=True)
            row.prop(props, "use_crease", text="Crease", toggle=True)
            row = col.row(align=True)
            row.prop(props, "use_edge_mark", text="Edge Mark", toggle=True)
            row.prop(props, "use_intersection", text="Intersect", toggle=True)
            col.separator()
            row = col.row(align=True)
            row.prop(props, "boil_enabled", text="Living Line")
            if props.boil_enabled:
                row.prop(props, "boil_intensity", text="Intensity")
            col.separator()
            draw_operator_row(col, "cellogic.update_outline_thickness", "Update")
            draw_operator_row(col, "cellogic.toggle_boil", "Toggle Boil")
            draw_operator_row(col, "cellogic.rebuild_outline", "Rebuild")
            col.separator()
            draw_operator_row(col, "cellogic.remove_outline",
                              "Remove Outline", icon='TRASH')


# ═══════════════════════════════════════════════════════
# MODULE 3 — SKIN SHADER
# ═══════════════════════════════════════════════════════

@register_class
class CELLOGIC_PT_skin(bpy.types.Panel):
    """Professor Goo Toon Skin Shader controls"""
    bl_label = "Skin Shader"
    bl_idname = "CELLOGIC_PT_skin"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cel-Logic"
    bl_parent_id = "CELLOGIC_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        props = obj.cl_skin

        if not props.enabled:
            draw_operator_row(layout, "cellogic.setup_skin",
                              "Setup Skin Shader", icon='SHADING_RENDERED')
        else:
            # Preset row
            col = draw_section(layout, "Preset", icon='PRESET')
            col.prop(props, "preset", text="")

            # Colours
            col = draw_section(layout, "Colours", icon='SHADING_RENDERED')
            draw_prop_row(col, props, "base_color", text="Lit Color")
            draw_prop_row(col, props, "shadow_tint", text="Shadow Color")
            draw_prop_row(col, props, "tone_threshold", text="Threshold")
            row = col.row(align=True)
            row.operator("cellogic.update_skin_base", text="Update Lit")
            row.operator("cellogic.update_skin_tint", text="Update Shadow")
            draw_operator_row(col, "cellogic.update_skin_threshold", "Update Threshold")

            # Rim
            col = draw_section(layout, "Curvature Rim", icon='LIGHT_SUN')
            draw_prop_row(col, props, "rim_strength", text="Strength")
            draw_prop_row(col, props, "rim_color", text="Color")
            draw_operator_row(col, "cellogic.update_skin_rim", "Update Rim")

            col.separator()
            draw_operator_row(layout, "cellogic.rebuild_skin", "Rebuild")
            draw_operator_row(layout, "cellogic.remove_skin",
                              "Remove Skin", icon='TRASH')


# ═══════════════════════════════════════════════════════
# UNIVERSAL ANIME SHADER (Body / Face / Hair)
# ═══════════════════════════════════════════════════════

@register_class
class CELLOGIC_PT_shader(bpy.types.Panel):
    """Universal Anime Shader — Body / Face / Hair"""
    bl_label = "Anime Shader"
    bl_idname = "CELLOGIC_PT_shader"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cel-Logic"
    bl_parent_id = "CELLOGIC_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        props = obj.cl_shader

        if not props.enabled:
            # Setup row
            col = draw_section(layout, "Shader Source", icon='FILE_SCRIPT')
            col.prop(props, "shader_source", text="")
            col.separator()
            col = draw_section(layout, "Material Type", icon='SHADING_RENDERED')
            col.prop(props, "material_type", text="")
            col.separator()
            draw_operator_row(layout, "cellogic.setup_shader",
                              "Setup Anime Shader", icon='NODE_MATERIAL')
        else:
            mtype = props.material_type
            source = props.shader_source

            # Shader source
            col = draw_section(layout, "Shader Source", icon='FILE_SCRIPT')
            col.prop(props, "shader_source", text="")

            # Material type
            col = draw_section(layout, "Material Type", icon='NODE_MATERIAL')
            col.prop(props, "material_type", text="")

            # Preset
            col = draw_section(layout, "Preset", icon='PRESET')
            col.prop(props, "preset", text="")

            # ── Toon Core ──
            col = draw_section(layout, "Toon Core", icon='SHADING_RENDERED')
            draw_prop_row(col, props, "lit_color", text="Lit Color")
            draw_prop_row(col, props, "shadow_color", text="Shadow Color")
            if source == 'PROCEDURAL':
                draw_prop_row(col, props, "deep_shadow_color", text="Deep Shadow")
                draw_prop_row(col, props, "shadow_threshold", text="Threshold")
                draw_prop_row(col, props, "shadow_feather", text="Feather")
                draw_prop_row(col, props, "shadow_bands", text="Bands")
                if props.shadow_bands >= 3:
                    draw_prop_row(col, props, "second_threshold", text="2nd Thresh")
                    draw_prop_row(col, props, "second_feather", text="2nd Feather")
            row = col.row(align=True)
            row.operator("cellogic.update_shader_colors", text="Update Colors")
            row.operator("cellogic.update_shader_shadow", text="Update Shadow")

            # ── Body/Skin (GooEngineToon) ──
            if source == 'JSON' or mtype == 'BODY':
                col = draw_section(layout, "GooEngineToon Controls", icon='LIGHT_SUN')
                draw_prop_row(col, props, "cast_shadows", text="Cast Shadows")
                draw_prop_row(col, props, "self_shadows", text="Self Shadows")
                draw_prop_row(col, props, "ambient_light", text="Ambient Light")
                if source == 'PROCEDURAL':
                    draw_prop_row(col, props, "shadow_from_min", text="Shadow Min")
                    draw_prop_row(col, props, "shadow_from_max", text="Shadow Max")

            # ── Lighting ──
            if source == 'PROCEDURAL':
                col = draw_section(layout, "Lighting", icon='LIGHT_SUN')
                draw_prop_row(col, props, "use_shader_info", text="Goo ShaderInfo")
                draw_prop_row(col, props, "light_smoothing", text="Smoothing")

            # ── Specular ──
            if source == 'PROCEDURAL' and mtype in ('BODY', 'HAIR'):
                col = draw_section(layout, "Specular", icon='LIGHT_SPOT')
                draw_prop_row(col, props, "spec_threshold", text="Threshold")
                draw_prop_row(col, props, "spec_intensity", text="Intensity")
                draw_prop_row(col, props, "spec_color", text="Color")
                draw_operator_row(col, "cellogic.update_shader_spec",
                                  "Update Specular")

            # ── Face Shadow ──
            if source == 'PROCEDURAL' and mtype == 'FACE':
                col = draw_section(layout, "Face Shadow", icon='FACESEL')
                draw_prop_row(col, props, "face_shadow_strength",
                              text="Strength")
                draw_prop_row(col, props, "face_shadow_softness",
                              text="Softness")
                draw_prop_row(col, props, "face_warm_shadow",
                              text="Warm Shadow")
                draw_prop_row(col, props, "face_cool_shadow",
                              text="Cool Shadow")
                draw_prop_row(col, props, "face_shade_map_strength",
                              text="Shade Map")
                draw_prop_row(col, props, "face_nose_line_power",
                              text="Nose Line")

            # ── Hair Shine ──
            if source == 'PROCEDURAL' and mtype == 'HAIR':
                col = draw_section(layout, "Hair Shine", icon='STRANDS')
                draw_prop_row(col, props, "hair_highlight_strength",
                              text="Highlight")
                draw_prop_row(col, props, "hair_highlight_width",
                              text="Width")
                draw_prop_row(col, props, "hair_highlight_pos",
                              text="Position")
                draw_prop_row(col, props, "hair_highlight_color",
                              text="HL Color")
                draw_prop_row(col, props, "hair_wave_scale",
                              text="Wave Scale")
                col.separator()
                col.label(text="Day/Night Ramps:")
                draw_prop_row(col, props, "hair_day_night", text="Day/Night")
                draw_prop_row(col, props, "hair_warm_shadow",
                              text="Warm Shadow")
                draw_prop_row(col, props, "hair_warm_lit", text="Warm Lit")
                draw_prop_row(col, props, "hair_cool_shadow",
                              text="Cool Shadow")
                draw_prop_row(col, props, "hair_cool_lit", text="Cool Lit")

            # ── Rim Light ──
            col = draw_section(layout, "Rim Light", icon='OUTLINER_OB_LIGHT')
            draw_prop_row(col, props, "rim_strength", text="Strength")
            draw_prop_row(col, props, "rim_thickness", text="Thickness")
            if source == 'JSON':
                draw_prop_row(col, props, "rim_samples", text="Samples")
                draw_prop_row(col, props, "rim_sample_radius", text="Sample Radius")
                draw_prop_row(col, props, "rim_invert", text="Invert")
            else:
                draw_prop_row(col, props, "rim_color", text="Color")
                draw_prop_row(col, props, "rim_scale_x", text="Scale X")
                draw_prop_row(col, props, "rim_scale_y", text="Scale Y")
            draw_operator_row(col, "cellogic.update_shader_rim",
                              "Update Rim")

            # ── Procedural Masks (procedural only) ──
            if source == 'PROCEDURAL':
                col = draw_section(layout, "Procedural Masks", icon='MOD_MASK')
                draw_prop_row(col, props, "curvature_intensity",
                              text="Curvature")
                draw_prop_row(col, props, "ao_strength", text="AO")
                draw_prop_row(col, props, "normal_dir_influence",
                              text="Normal Dir")
                draw_prop_row(col, props, "camera_facing_power",
                              text="Camera Facing")

                col = draw_section(layout, "Mask Manager", icon='TEXTURE')
                draw_prop_row(col, props, "shadow_mask_procedural",
                              text="Shadow Proc")
                draw_prop_row(col, props, "highlight_mask_procedural",
                              text="Highlight Proc")
                draw_prop_row(col, props, "rim_mask_procedural",
                              text="Rim Proc")

            # ── Edge Highlights (procedural only) ──
            if source == 'PROCEDURAL':
                col = draw_section(layout, "Edge Highlights", icon='IPO_LINEAR')
                draw_prop_row(col, props, "edge_strength", text="Strength")
                draw_prop_row(col, props, "edge_threshold", text="Threshold")

            # ── Ucupaint Integration ──
            col = draw_section(layout, "Ucupaint Paint Layers", icon='BRUSH_DATA')
            if not props.use_ucupaint:
                draw_operator_row(col, "cellogic.setup_ucupaint",
                                  "Setup Paint Layers", icon='BRUSH_DATA')
            else:
                col.label(text="Ucupaint active — use ucupaint panel to paint",
                          icon='CHECKMARK')
                draw_operator_row(col, "cellogic.wire_ucupaint_shadow",
                                  "Wire Shadow Channel")
                draw_operator_row(col, "cellogic.remove_ucupaint",
                                  "Remove Paint Layers", icon='TRASH')

            # Rebuild / Remove
            layout.separator()
            draw_operator_row(layout, "cellogic.rebuild_shader",
                              "Rebuild Shader")
            draw_operator_row(layout, "cellogic.remove_shader",
                              "Remove Shader", icon='TRASH')


# ═══════════════════════════════════════════════════════
# MODULE 4 — ANIME EYES
# ═══════════════════════════════════════════════════════

@register_class
class CELLOGIC_PT_eyes(bpy.types.Panel):
    """Anime Eye Shader controls"""
    bl_label = "Anime Eyes"
    bl_idname = "CELLOGIC_PT_eyes"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cel-Logic"
    bl_parent_id = "CELLOGIC_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        props = obj.cl_eyes

        if not props.enabled:
            draw_operator_row(layout, "cellogic.setup_eyes",
                              "Setup Anime Eyes", icon='HIDE_OFF')
        else:
            # Sclera
            col = draw_section(layout, "Sclera (Eye White)", icon='HIDE_OFF')
            draw_prop_row(col, props, "sclera_brightness", text="Brightness")
            draw_prop_row(col, props, "sclera_shadow_influence", text="Shadow Influence")
            draw_prop_row(col, props, "sclera_shadow_tint", text="Shadow Tint")
            draw_operator_row(col, "cellogic.update_eye_sclera", "Update Sclera")

            # Iris
            col = draw_section(layout, "Iris", icon='LIGHT_POINT')
            draw_prop_row(col, props, "iris_color", text="Color")
            draw_prop_row(col, props, "iris_top_shadow", text="Top Shadow")
            draw_prop_row(col, props, "iris_bottom_glow", text="Bottom Glow")
            draw_prop_row(col, props, "iris_inner_ring", text="Inner Ring")
            draw_prop_row(col, props, "iris_outer_ring", text="Outer Ring")
            draw_operator_row(col, "cellogic.update_eye_iris", "Update Iris")

            # Catchlight
            col = draw_section(layout, "Catchlight", icon='LIGHT_SUN')
            draw_prop_row(col, props, "catchlight_size", text="Size")
            draw_prop_row(col, props, "catchlight_offset_x", text="Offset X")
            draw_prop_row(col, props, "catchlight_offset_y", text="Offset Y")
            draw_prop_row(col, props, "catchlight_softness", text="Softness")
            draw_prop_row(col, props, "catchlight_color", text="Color")
            draw_operator_row(col, "cellogic.update_eye_catchlight", "Update Catchlight")

            # Lid Shadow
            col = draw_section(layout, "Lid Shadow", icon='MOD_MASK')
            draw_prop_row(col, props, "lid_shadow_depth", text="Depth")
            draw_prop_row(col, props, "lid_shadow_thickness", text="Thickness")
            draw_operator_row(col, "cellogic.update_eye_lid", "Update Lid Shadow")

            # Emotion
            col = draw_section(layout, "Emotion Boost", icon='HEART')
            draw_prop_row(col, props, "emotion_boost", text="Boost")
            draw_operator_row(col, "cellogic.update_eye_emotion", "Update Emotion")

            layout.separator()
            draw_operator_row(layout, "cellogic.rebuild_eyes", "Rebuild Eyes")
            draw_operator_row(layout, "cellogic.remove_eyes",
                              "Remove Eyes", icon='TRASH')


# ═══════════════════════════════════════════════════════
# MODULE 5 — BLUSH
# ═══════════════════════════════════════════════════════

@register_class
class CELLOGIC_PT_blush(bpy.types.Panel):
    """Cheek Blush Overlay controls"""
    bl_label = "Blush"
    bl_idname = "CELLOGIC_PT_blush"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cel-Logic"
    bl_parent_id = "CELLOGIC_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        props = obj.cl_blush

        if not props.enabled:
            draw_operator_row(layout, "cellogic.add_blush",
                              "Add Blush", icon='HEART')
        else:
            col = draw_section(layout, "Blush Settings", icon='HEART')
            draw_prop_row(col, props, "color", text="Color")
            draw_prop_row(col, props, "opacity", text="Opacity")
            draw_prop_row(col, props, "softness", text="Softness")
            col.separator()
            draw_operator_row(col, "cellogic.update_blush", "Update Blush")
            draw_operator_row(col, "cellogic.rebuild_blush", "Rebuild Blush")
            col.separator()
            draw_operator_row(col, "cellogic.remove_blush",
                              "Remove Blush", icon='TRASH')


# ═══════════════════════════════════════════════════════
# STUBS — Mouth, Animation, Post
# ═══════════════════════════════════════════════════════

@register_class
class CELLOGIC_PT_mouth(bpy.types.Panel):
    """Flat Anime Mouth Shader controls"""
    bl_label = "Mouth"
    bl_idname = "CELLOGIC_PT_mouth"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cel-Logic"
    bl_parent_id = "CELLOGIC_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        props = obj.cl_mouth

        if not props.enabled:
            draw_operator_row(layout, "cellogic.setup_mouth",
                              "Setup Mouth Shader", icon='MESH_TORUS')
        else:
            # Colors
            col = draw_section(layout, "Mouth Colors", icon='MESH_TORUS')
            draw_prop_row(col, props, "interior_color", text="Interior")
            draw_prop_row(col, props, "teeth_color", text="Teeth")
            draw_operator_row(col, "cellogic.update_mouth_colors",
                              "Update Colors")

            # Boundary
            col = draw_section(layout, "Region Split", icon='UV_DATA')
            draw_prop_row(col, props, "teeth_boundary", text="Teeth Boundary")
            draw_operator_row(col, "cellogic.update_mouth_boundary",
                              "Update Boundary")

            # Goo Engine features
            col = draw_section(layout, "Goo Engine", icon='MODIFIER')
            draw_prop_row(col, props, "depth_offset", text="Depth Offset")
            draw_operator_row(col, "cellogic.update_mouth_depth",
                              "Update Depth")
            draw_prop_row(col, props, "shadow_intensity", text="Shadow")
            draw_operator_row(col, "cellogic.update_mouth_shadow",
                              "Update Shadow")

            layout.separator()
            draw_operator_row(layout, "cellogic.rebuild_mouth",
                              "Rebuild Mouth")
            draw_operator_row(layout, "cellogic.remove_mouth",
                              "Remove Mouth", icon='TRASH')


@register_class
class CELLOGIC_PT_animation(bpy.types.Panel):
    """Timing & Animation (Coming Soon)"""
    bl_label = "Animation (Coming Soon)"
    bl_idname = "CELLOGIC_PT_animation"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cel-Logic"
    bl_parent_id = "CELLOGIC_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def draw(self, context):
        self.layout.label(text="Module 7 — Not yet implemented")


@register_class
class CELLOGIC_PT_post(bpy.types.Panel):
    """Post-Processing (Coming Soon)"""
    bl_label = "Post-Processing (Coming Soon)"
    bl_idname = "CELLOGIC_PT_post"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cel-Logic"
    bl_parent_id = "CELLOGIC_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        self.layout.label(text="Coming soon — broadcast post + compositing")


# ═══════════════════════════════════════════════════════
# UTILITIES ROW
# ═══════════════════════════════════════════════════════

@register_class
class CELLOGIC_PT_utilities(bpy.types.Panel):
    """Utilities — reset & audit"""
    bl_label = "Utilities"
    bl_idname = "CELLOGIC_PT_utilities"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cel-Logic"
    bl_parent_id = "CELLOGIC_PT_main"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        draw_operator_row(layout, "cellogic.full_reset",
                          "Full Reset", icon='FILE_REFRESH')
        draw_operator_row(layout, "cellogic.scene_audit",
                          "Scene Audit", icon='INFO')
