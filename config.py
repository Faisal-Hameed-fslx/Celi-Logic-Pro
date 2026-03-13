"""
Cel-Logic Pro — Configuration
Central location for ALL constants, defaults, and magic numbers.
No hardcoded values anywhere else in the codebase.
"""

import math

# ═══════════════════════════════════════════════════════
# ADDON IDENTITY
# ═══════════════════════════════════════════════════════
ADDON_NAME = "Cel-Logic Pro"
ADDON_VERSION = (1, 0, 0)
DATA_VERSION = (1, 0, 0)

# ═══════════════════════════════════════════════════════
# ENGINE DETECTION
# Goo Engine 4.4 only (Blender EEVEE fork)
# Standard Blender / Cycles NOT supported
# ═══════════════════════════════════════════════════════
VALID_ENGINES = {'BLENDER_EEVEE'}
ENGINE_DISPLAY_NAME = "Goo Engine"

# Color Management — must be Standard for vibrant anime colours
COLOR_MGMT_VIEW_TRANSFORM = "Standard"

# ═══════════════════════════════════════════════════════
# MODIFIER NAMES & ORDER
# ═══════════════════════════════════════════════════════
MOD_LATTICE = "CelLogic_Lattice"
MOD_ARMATURE = "CelLogic_Armature"
MOD_DATA_TRANSFER = "CelLogic_DataTransfer"
MOD_SOLIDIFY = "CelLogic_Solidify"

MODIFIER_ORDER = [
    MOD_LATTICE,
    MOD_ARMATURE,
    MOD_DATA_TRANSFER,
    MOD_SOLIDIFY,
]

# ═══════════════════════════════════════════════════════
# MODULE 1: FACE PROXY
# ═══════════════════════════════════════════════════════
PROXY_SUFFIX = "_CelLogic_Proxy"
PROXY_SEGMENTS = 32
PROXY_RINGS = 16
AUTO_SMOOTH_ANGLE = math.pi  # 180°

# ═══════════════════════════════════════════════════════
# MODULE 2: OUTLINE
# ═══════════════════════════════════════════════════════
OUTLINE_GP_NAME = "CelLogic_OutlineGP"      # Grease Pencil object name suffix
OUTLINE_LINEART_MOD = "CelLogic_LineArt"    # LINEART modifier name
OUTLINE_LAYER = "Outline"                    # GP layer name
OUTLINE_MAT_NAME = "CelLogic_Outline"        # GP stroke material

DEFAULTS_OUTLINE = {
    "thickness": 25,
    "thickness_min": 1,
    "thickness_max": 100,
    "opacity": 1.0,
    "color": (0.0, 0.0, 0.0, 1.0),
    "use_contour": True,
    "use_crease": True,
    "use_edge_mark": True,
    "use_intersection": True,
}

# ═══════════════════════════════════════════════════════
# MODULE 3: SKIN SHADER (Professor Goo Method)
# ═══════════════════════════════════════════════════════
SKIN_MAT_SUFFIX = "_CelLogic_Skin"
HERO_LIGHT_GROUP = "HERO_RIG"
ILM_LAYER = "CelLogic_ILM"

DEFAULTS_SKIN = {
    "base_color": (0.9, 0.75, 0.65, 1.0),       # lit side colour
    "shadow_tint": (0.15, 0.08, 0.25, 1.0),     # shadow side colour
    "highlight_power": 1.0,
    "rim_strength": 0.5,
    "rim_color": (1.0, 0.6, 0.5, 1.0),
    "tone_threshold": 0.45,                       # hard cut position (0-1)
}

# Built-in skin presets
SKIN_PRESETS = {
    "Default Skin": {
        "base_color": (0.9, 0.75, 0.65, 1.0),
        "shadow_tint": (0.15, 0.08, 0.25, 1.0),
        "rim_color": (1.0, 0.6, 0.5, 1.0),
        "rim_strength": 0.5,
        "tone_threshold": 0.45,
    },
    "Cool Porcelain": {
        "base_color": (0.95, 0.92, 0.90, 1.0),
        "shadow_tint": (0.4, 0.35, 0.55, 1.0),
        "rim_color": (0.8, 0.85, 1.0, 1.0),
        "rim_strength": 0.7,
        "tone_threshold": 0.5,
    },
    "Warm Tan": {
        "base_color": (0.72, 0.52, 0.38, 1.0),
        "shadow_tint": (0.2, 0.08, 0.06, 1.0),
        "rim_color": (1.0, 0.5, 0.3, 1.0),
        "rim_strength": 0.4,
        "tone_threshold": 0.4,
    },
    "Soft (Fur/Snow)": {
        "base_color": (0.95, 0.93, 0.90, 1.0),
        "shadow_tint": (0.7, 0.65, 0.72, 1.0),
        "rim_color": (0.9, 0.92, 1.0, 1.0),
        "rim_strength": 0.3,
        "tone_threshold": 0.55,
    },
    "Hard Metal": {
        "base_color": (0.7, 0.72, 0.75, 1.0),
        "shadow_tint": (0.08, 0.08, 0.12, 1.0),
        "rim_color": (0.8, 0.85, 1.0, 1.0),
        "rim_strength": 0.8,
        "tone_threshold": 0.35,
    },
}

# ═══════════════════════════════════════════════════════
# MODULE 4: EYE SYSTEM
# ═══════════════════════════════════════════════════════
EYE_MAT_SUFFIX = "_CelLogic_Eye"

DEFAULTS_EYE = {
    "sclera_brightness": 0.95,
    "sclera_shadow_influence": 0.3,
    "sclera_shadow_tint": (0.7, 0.75, 0.9, 1.0),
    "iris_color": (0.2, 0.4, 0.8, 1.0),
    "iris_top_shadow": 0.6,
    "iris_bottom_glow": 0.4,
    "iris_inner_ring": 0.3,
    "iris_outer_ring": 0.2,
    "catchlight_size": 0.15,
    "catchlight_offset_x": 0.1,
    "catchlight_offset_y": 0.15,
    "catchlight_softness": 0.1,
    "catchlight_color": (1.0, 1.0, 1.0, 1.0),
    "lid_shadow_depth": 0.3,
    "lid_shadow_thickness": 0.2,
    "emotion_boost": 0.0,
}

# ═══════════════════════════════════════════════════════
# MODULE 5: BLUSH
# ═══════════════════════════════════════════════════════
BLUSH_LAYER = "CelLogic_Blush"

DEFAULTS_BLUSH = {
    "color": (1.0, 0.4, 0.5, 1.0),
    "opacity": 0.3,
    "softness": 0.5,
}

# ═══════════════════════════════════════════════════════
# MODULE 6: MOUTH
# ═══════════════════════════════════════════════════════
MOUTH_MAT_SUFFIX = "_CelLogic_Mouth"

DEFAULTS_MOUTH = {
    "interior_color": (0.08, 0.02, 0.02, 1.0),
    "teeth_color": (0.9, 0.88, 0.85, 1.0),
    "teeth_boundary": 0.35,
    "depth_offset": 0.002,
    "shadow_intensity": 0.15,
}

# ═══════════════════════════════════════════════════════
# MODULE 7: TIMING
# ═══════════════════════════════════════════════════════
TIMING_ONES = 1
TIMING_TWOS = 2
TIMING_THREES = 3
TIMING_FOURS = 4
DEFAULT_LAG_FRAMES = 2

# ═══════════════════════════════════════════════════════
# MODULE 8: PERSPECTIVE
# ═══════════════════════════════════════════════════════
LATTICE_SUFFIX = "_CelLogic_HeadLattice"
SHOULDER_SUFFIX = "_CelLogic_ShoulderLattice"
DEFAULT_CHEAT_START = 30.0
DEFAULT_CHEAT_END = 90.0

# ═══════════════════════════════════════════════════════
# MODULE 9: POST-PROCESS
# ═══════════════════════════════════════════════════════
POST_GROUP_NAME = "CelLogic_PostStack"

DEFAULTS_POST = {
    "grain": 0.03,
    "posterize": 128,
    "chromatic": 0.5,
    "vignette": 0.05,
}

# ═══════════════════════════════════════════════════════
# AAA ANIME SHADER SYSTEM (v3 — Modular Architecture)
# 9-module pipeline: Input → Masks → Manager → Lighting
#   → Toon → Face/Hair → Effects → Compositor
# ═══════════════════════════════════════════════════════
SHADER_BODY_SUFFIX = "_CelLogic_Body"
SHADER_FACE_SUFFIX = "_CelLogic_Face"
SHADER_HAIR_SUFFIX = "_CelLogic_Hair"
EMILY_BLEND_PATH = r"D:\Celi Logic\cel_logic_pro\_Emily_Rig_Master_GE.blend"

DEFAULTS_SHADER = {
    # ── Shader Source ──
    "shader_source":      "JSON",         # JSON = from shader.json, PROCEDURAL = builder.py

    # ── Ucupaint ──
    "use_ucupaint":       False,          # enable ucupaint painting layers
    "ucupaint_shadow":    False,          # wire shadow channel to ucupaint too

    # ── Toon Core ──
    "lit_color":          (1.0, 1.0, 1.0, 1.0),
    "shadow_color":       (0.75, 0.70, 0.85, 1.0),
    "deep_shadow_color":  (0.35, 0.25, 0.45, 1.0),
    "shadow_threshold":   0.45,       # lit ↔ mid boundary (face/hair)
    "shadow_feather":     0.02,       # edge softness (face/hair)
    "second_threshold":   0.20,       # mid ↔ deep boundary
    "second_feather":     0.02,
    "shadow_bands":       2,          # 2 = two-tone, 3 = three-tone

    # ── Body/Skin (GooEngineToon architecture) ──
    "shadow_from_min":    0.125,      # MapRange cel threshold low
    "shadow_from_max":    0.15,       # MapRange cel threshold high
    "cast_shadows":       1.0,        # cast shadow toggle (0=off, 1=on)
    "self_shadows":       1.0,        # self shadow toggle
    "ambient_light":      0.0,        # ambient lighting blend

    # ── Lighting Interpreter (face/hair fallback) ──
    "light_smoothing":    0.05,       # threshold smoothing width
    "use_shader_info":    True,       # use Goo ShaderInfo if available

    # ── Specular ──
    "spec_threshold":     0.90,
    "spec_intensity":     0.5,
    "spec_color":         (1.0, 1.0, 1.0, 1.0),

    # ── Rim Light (Curvature-based) ──
    "rim_strength":       1.0,        # RimFac (1.0 matches GooEngineToon)
    "rim_thickness":      10.0,       # matches GooEngineToon
    "rim_samples":        4.0,        # matches GooEngineToon
    "rim_sample_radius":  0.2,        # matches GooEngineToon
    "rim_color":          (1.0, 1.0, 1.0, 1.0),
    "rim_scale_x":        4.0,
    "rim_scale_y":        0.0,
    "rim_invert":         0.0,        # rim inversion (0=normal, 1=inverted)

    # ── Edge Highlights ──
    "edge_strength":      0.0,
    "edge_threshold":     0.5,

    # ── Procedural Masks ──
    "curvature_intensity": 1.0,
    "ao_strength":         0.5,
    "normal_dir_influence": 0.5,
    "camera_facing_power": 2.0,

    # ── Mask Manager defaults ──
    "shadow_mask_procedural": 1.0,    # 1=full procedural, 0=full painted
    "highlight_mask_procedural": 1.0,
    "rim_mask_procedural":    1.0,

    # ── Face-specific ──
    "face_shadow_strength":    0.8,
    "face_shadow_softness":    0.3,
    "face_warm_shadow":        (0.85, 0.75, 0.80, 1.0),
    "face_cool_shadow":        (0.70, 0.70, 0.85, 1.0),
    "face_shade_map_strength": 0.0,
    "face_nose_line_power":    0.5,

    # ── Hair-specific ──
    "hair_highlight_strength": 0.6,
    "hair_highlight_width":    4.9,
    "hair_highlight_pos":      7.6,
    "hair_highlight_density":  -0.1,
    "hair_highlight_color":    (0.46, 0.24, 0.63, 1.0),
    "hair_wave_scale":         3.0,
    "hair_wave_distortion":    23.0,
    "hair_day_night":          0.0,
    "hair_warm_ramp_shadow":   (0.6, 0.4, 0.35, 1.0),
    "hair_warm_ramp_lit":      (1.0, 0.95, 0.9, 1.0),
    "hair_cool_ramp_shadow":   (0.3, 0.3, 0.5, 1.0),
    "hair_cool_ramp_lit":      (0.9, 0.9, 1.0, 1.0),
}

SHADER_PRESETS = {
    "Default": {
        "lit_color": (1.0, 1.0, 1.0, 1.0),
        "shadow_color": (0.75, 0.7, 0.85, 1.0),
        "deep_shadow_color": (0.35, 0.25, 0.45, 1.0),
        "rim_color": (1.0, 1.0, 1.0, 1.0),
        "rim_strength": 0.25,
        "shadow_threshold": 0.45,
    },
    "Warm Skin": {
        "lit_color": (0.991, 0.839, 0.831, 1.0),
        "shadow_color": (0.672, 0.376, 0.429, 1.0),
        "deep_shadow_color": (0.35, 0.18, 0.25, 1.0),
        "rim_color": (1.0, 0.889, 0.829, 1.0),
        "rim_strength": 0.3,
        "shadow_threshold": 0.45,
    },
    "Cool Porcelain": {
        "lit_color": (0.95, 0.92, 0.90, 1.0),
        "shadow_color": (0.4, 0.35, 0.55, 1.0),
        "deep_shadow_color": (0.2, 0.15, 0.3, 1.0),
        "rim_color": (0.8, 0.85, 1.0, 1.0),
        "rim_strength": 0.5,
        "shadow_threshold": 0.5,
    },
    "Hard Metal": {
        "lit_color": (0.7, 0.72, 0.75, 1.0),
        "shadow_color": (0.25, 0.25, 0.30, 1.0),
        "deep_shadow_color": (0.08, 0.08, 0.12, 1.0),
        "rim_color": (0.8, 0.85, 1.0, 1.0),
        "rim_strength": 0.8,
        "shadow_threshold": 0.4,
    },
    "Emily Skin": {
        "lit_color": (0.991, 0.839, 0.831, 1.0),
        "shadow_color": (0.672, 0.376, 0.429, 1.0),
        "deep_shadow_color": (0.35, 0.18, 0.22, 1.0),
        "rim_color": (1.0, 0.889, 0.829, 1.0),
        "rim_strength": 0.3,
        "shadow_threshold": 0.45,
    },
    "Emily Suit": {
        "lit_color": (0.676, 0.763, 0.823, 1.0),
        "shadow_color": (0.328, 0.429, 0.558, 1.0),
        "deep_shadow_color": (0.15, 0.2, 0.35, 1.0),
        "rim_color": (1.0, 0.889, 0.829, 1.0),
        "rim_strength": 0.2,
        "shadow_threshold": 0.45,
    },
    "Emily Dark": {
        "lit_color": (0.255, 0.315, 0.485, 1.0),
        "shadow_color": (0.098, 0.075, 0.175, 1.0),
        "deep_shadow_color": (0.04, 0.03, 0.08, 1.0),
        "rim_color": (0.8, 0.85, 1.0, 1.0),
        "rim_strength": 0.15,
        "shadow_threshold": 0.4,
    },
    "Emily Pink": {
        "lit_color": (0.761, 0.337, 0.645, 1.0),
        "shadow_color": (0.448, 0.129, 0.360, 1.0),
        "deep_shadow_color": (0.22, 0.06, 0.18, 1.0),
        "rim_color": (1.0, 0.889, 0.829, 1.0),
        "rim_strength": 0.25,
        "shadow_threshold": 0.45,
    },
    "Anime Hair Dark": {
        "lit_color": (0.117, 0.109, 0.112, 1.0),
        "shadow_color": (0.046, 0.046, 0.059, 1.0),
        "deep_shadow_color": (0.02, 0.02, 0.03, 1.0),
        "rim_color": (0.5, 0.5, 0.6, 1.0),
        "rim_strength": 0.2,
        "shadow_threshold": 0.45,
    },
}
