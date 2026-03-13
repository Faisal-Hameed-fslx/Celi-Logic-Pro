"""
Cel-Logic Pro — Goo Engine Node Reference
Complete socket definitions for all 11 Goo Engine custom shader nodes.
Probed from Goo Engine 4.4.3 (blender 4.4 fork).

Usage:
    from ..core.goo_nodes import GOO_NODES, has_goo_node
    info = GOO_NODES['ShaderInfo']
    # info['type'] → 'ShaderNodeShaderInfo'
    # info['inputs'] → {'WorldPosition': 0, 'Normal': 1}
    # info['outputs'] → {'Diffuse Shading': 0, 'Cast Shadows': 1, ...}
"""

# ═══════════════════════════════════════════════════════
# NODE DEFINITIONS
# Indexed by friendly key, each entry has:
#   type       — bl_idname used in nodes.new(type=...)
#   label      — Default label shown in Blender UI
#   inputs     — dict{socket_name: index}
#   outputs    — dict{socket_name: index}
#   enums      — dict{prop_name: [(id, label), ...]}  (if any)
# ═══════════════════════════════════════════════════════

GOO_NODES = {

    # ─── Core Toon Shading ───────────────────────────
    'ShaderInfo': {
        'type': 'ShaderNodeShaderInfo',
        'label': 'Shader Info',
        'inputs': {
            'WorldPosition': 0,   # VECTOR
            'Normal': 1,          # VECTOR
        },
        'outputs': {
            'Diffuse Shading': 0,       # COLOR (RGBA)
            'Cast Shadows': 1,          # FLOAT  (0=lit, 1=shadow)
            'Self Shadows': 2,          # FLOAT
            'Ambient Lighting': 3,      # COLOR (RGBA)
            'Half-lambert factor': 4,   # FLOAT  (0→1 shading ramp)
        },
    },

    # ─── Screen‑Space Compositing ────────────────────
    'ScreenspaceInfo': {
        'type': 'ShaderNodeScreenspaceInfo',
        'label': 'Screenspace Info',
        'inputs': {
            'View Position': 0,   # VECTOR
        },
        'outputs': {
            'Scene Color': 0,     # COLOR (RGBA)
            'Scene Depth': 1,     # FLOAT
        },
    },

    # ─── Edge / Rim Detection ────────────────────────
    'Curvature': {
        'type': 'ShaderNodeCurvature',
        'label': 'Curvature',
        'inputs': {
            'Samples': 0,         # FLOAT
            'Sample Radius': 1,   # FLOAT
            'Thickness': 2,       # FLOAT
            'Scale': 3,           # VECTOR
        },
        'outputs': {
            'Scene Curvature': 0,  # FLOAT
            'Scene Rim': 1,        # FLOAT
        },
    },

    # ─── Light Info ──────────────────────────────────
    'LightInfo': {
        'type': 'ShaderNodeLightInfo',
        'label': 'Light Info',
        'inputs': {},
        'outputs': {
            'Light Color': 0,        # COLOR (RGBA)
            'Light Power': 1,        # FLOAT
            'Perceptual Power': 2,   # FLOAT
        },
    },

    # ─── Depth Override ──────────────────────────────
    'SetDepth': {
        'type': 'ShaderNodeSetDepth',
        'label': 'Set Depth',
        'inputs': {
            'Shader': 0,       # SHADER
            'View Depth': 1,   # FLOAT
        },
        'outputs': {
            'Shader': 0,       # SHADER
        },
    },

    # ─── SDF Shapes ──────────────────────────────────
    'SdfPrimitive': {
        'type': 'ShaderNodeSdfPrimitive',
        'label': 'Sdf Primitive',
        'inputs': {
            'Vector': 0,       # VECTOR
            'Size': 1,         # FLOAT
            'Radius': 2,       # FLOAT
            'Value1': 3,       # FLOAT
            'Value2': 4,
            'Value3': 5,
            'Value4': 6,
            'Point_0': 7,      # VECTOR (4X Point sockets)
            'Point_1': 8,
            'Point_2': 9,
            'Point_3': 10,
            'Angle': 11,       # FLOAT (angle)
            'Roundness': 12,   # FLOAT (factor)
            'Linewidth': 13,   # FLOAT
        },
        'outputs': {
            'Distance': 0,     # FLOAT
        },
        'enums': {
            'mode': [
                'SPHERE_3D', 'BOX_3D', 'TORUS_3D', 'CONE_3D',
                'POINT_CONE_3D', 'CYLINDER_3D', 'POINT_CYLINDER_3D',
                'CAPSULE_3D', 'OCTAHEDRON_3D', 'HEX_PRISM_3D',
                'HEX_PRISM_INCIRCLE_3D', 'PLANE_3D', 'SOLID_ANGLE_3D',
                'PYRAMID_3D', 'DISC_3D', 'CIRCLE_3D',
                # 2D primitives
                'CIRCLE_2D', 'RECTANGLE_2D', 'ELLIPSE_2D', 'TRIANGLE_2D',
                'PENTAGON_2D', 'HEXAGON_2D', 'ISOSCELES_2D', 'TRAPEZOID_2D',
                'RHOMBUS_2D', 'STAR_2D', 'HEART_2D', 'PIE_2D', 'ARC_2D',
                'MOON_2D', 'VESICA_2D', 'CROSS_2D', 'ROUNDX_2D',
                'HORSESHOE_2D', 'ROUND_JOINT_2D', 'FLAT_JOINT_2D',
                'LINE_2D', 'CORNER_2D', 'BEZIER_2D', 'POINT_TRIANGLE_2D',
                'QUAD_2D', 'PARABOLA_2D', 'PARABOLA_SEGMENT_2D', 'CAPSULE_2D',
            ],
        },
    },

    # ─── SDF Operators ───────────────────────────────
    'SdfOp': {
        'type': 'ShaderNodeSdfOp',
        'label': 'Sdf Operator',
        'inputs': {
            'Distance_A': 0,   # FLOAT
            'Distance_B': 1,   # FLOAT
            'Value_A': 2,      # FLOAT
            'Value_B': 3,      # FLOAT
            'Count': 4,        # INT
        },
        'outputs': {
            'Distance': 0,     # FLOAT
        },
        'enums': {
            'operation': [
                'DILATE', 'ONION', 'ANNULAR', 'MASK', 'FLATTEN',
                'INVERT', 'PULSE', 'BLEND', 'EXCLUSION', 'DIVIDE',
                'PIPE', 'ENGRAVE', 'GROOVE', 'TONGUE',
                'UNION', 'UNION_SMOOTH', 'UNION_ROUND', 'UNION_COLUMNS',
                'UNION_STAIRS', 'UNION_CHAMFER',
                'INTERSECT', 'INTERSECT_SMOOTH', 'INTERSECT_ROUND',
                'INTERSECT_COLUMNS', 'INTERSECT_STAIRS', 'INTERSECT_CHAMFER',
                'DIFF', 'DIFF_SMOOTH', 'DIFF_ROUND',
                'DIFF_COLUMNS', 'DIFF_STAIRS', 'DIFF_CHAMFER',
            ],
        },
    },

    # ─── SDF Vector Operations ───────────────────────
    'SdfVectorOp': {
        'type': 'ShaderNodeSdfVectorOp',
        'label': 'Sdf Vector Operator',
        'inputs': {
            'Vector1': 0,
            'Vector2': 1,
            'Vector3': 2,
            'Scale': 3,
            'Value1': 4,
            'Value2': 5,
            'Angle': 6,
            'Count1': 7,
            'Count2': 8,
        },
        'outputs': {
            'Vector': 0,
            'Position': 1,
            'Value': 2,
        },
        'enums': {
            'operation': [
                'VEC_REFLECT', 'VEC_MIRROR', 'VEC_POLAR',
                'VEC_REPEAT_INF', 'VEC_REPEAT_INF_MIRROR',
                'VEC_REPEAT_FINITE', 'OCTANT', 'VEC_SWIZZLE',
                'VEC_ROTATE', 'VEC_SPIN', 'VEC_EXTRUDE', 'VEC_TWIST',
                'VEC_SWIRL', 'VEC_PINCH_INFLATE', 'VEC_RADIAL_SHEAR',
                'VEC_BEND', 'UV_ROTATE', 'UV_SCALE', 'UV_GRID',
                'UV_RAND_ROTATE', 'UV_RAND_FLIP', 'TILESET',
                'MAP_11', 'MAP_05', 'MAP_UV',
            ],
            'axis': [
                'XYZ_AXIS', 'XZY_AXIS', 'YXZ_AXIS',
                'YZX_AXIS', 'ZXY_AXIS', 'ZYX_AXIS',
            ],
        },
    },

    # ─── SDF Noise ───────────────────────────────────
    'SdfNoise': {
        'type': 'ShaderNodeSdfNoise',
        'label': 'Sdf Noise',
        'inputs': {
            'Position': 0,
            'Distance': 1,
            'Detail': 2,
            'Roughness': 3,
            'Detail Inflation': 4,
            'Detail Blend': 5,
        },
        'outputs': {
            'Distance': 0,
        },
    },

    # ─── Effects ─────────────────────────────────────
    'Twirl': {
        'type': 'ShaderNodeTwirl',
        'label': 'Twirl',
        'inputs': {
            'Vector': 0,
            'Center': 1,
            'Amount': 2,
        },
        'outputs': {
            'Vector': 0,
        },
    },

    'WaterRipples': {
        'type': 'ShaderNodeWaterRipples',
        'label': 'Water Ripples',
        'inputs': {
            'Vector': 0,
            'Time': 1,
            'Mode': 2,
            'Scale': 3,
            'Intensity': 4,
            'Speed': 5,
            'Detail': 6,
            'Bias': 7,
        },
        'outputs': {
            'Distorted Vector': 0,
            'Mask': 1,
        },
        'enums': {
            'mode': ['DROPS', 'RIPPLES', 'FLOW', 'CAUSTIC'],
        },
    },
}


# ═══════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════

def has_goo_node(node_key):
    """Check if a Goo Engine node key is defined."""
    return node_key in GOO_NODES


def goo_type(node_key):
    """Return the bl_idname for a Goo Engine node. Raises KeyError if unknown."""
    return GOO_NODES[node_key]['type']


def goo_output(node_key, output_name):
    """Return the output socket index for a named output."""
    return GOO_NODES[node_key]['outputs'][output_name]


def goo_input(node_key, input_name):
    """Return the input socket index for a named input."""
    return GOO_NODES[node_key]['inputs'][input_name]


def try_create_goo_node(node_tree, node_key, name=None, location=(0, 0)):
    """Try to create a Goo Engine node. Returns (node, True) on success,
    or (None, False) if the node type doesn't exist in this build."""
    info = GOO_NODES.get(node_key)
    if info is None:
        return None, False
    try:
        node = node_tree.nodes.new(type=info['type'])
        if name:
            node.name = name
            node.label = name
        node.location = location
        return node, True
    except Exception:
        return None, False
