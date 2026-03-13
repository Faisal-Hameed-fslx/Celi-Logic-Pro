"""
Cel-Logic Pro — Dependency Graph
Tracks which systems are active and their relationships.
Prevents orphaned data and ensures clean teardown order.
"""

from .. import logger

# System dependency map: system → list of systems it depends on
DEPENDENCIES = {
    "face_proxy": [],
    "outline": [],
    "skin": [],
    "eyes": [],
    "blush": ["skin"],      # Blush injects into skin material
    "mouth": [],
    "animation": [],
    "perspective": [],
    "post": [],
}


def get_active_systems(obj):
    """Return list of active system names on an object."""
    active = []
    if hasattr(obj, 'cl_proxy') and obj.cl_proxy.enabled:
        active.append("face_proxy")
    if hasattr(obj, 'cl_outline') and obj.cl_outline.enabled:
        active.append("outline")
    if hasattr(obj, 'cl_skin') and obj.cl_skin.enabled:
        active.append("skin")
    if hasattr(obj, 'cl_eyes') and obj.cl_eyes.enabled:
        active.append("eyes")
    if hasattr(obj, 'cl_blush') and obj.cl_blush.enabled:
        active.append("blush")
    return active


def check_dependencies(system_name, obj):
    """
    Check if all dependencies for a system are met.
    Returns (ok, missing_list).
    """
    deps = DEPENDENCIES.get(system_name, [])
    active = get_active_systems(obj)
    missing = [d for d in deps if d not in active]
    return (len(missing) == 0, missing)


def get_teardown_order(systems):
    """
    Return the safe order to remove systems (dependents first).
    """
    # Reverse topological sort
    order = []
    remaining = set(systems)
    while remaining:
        # Find systems with no active dependents
        batch = []
        for s in remaining:
            dependents = [
                other for other in remaining
                if s in DEPENDENCIES.get(other, [])
            ]
            if not dependents:
                batch.append(s)
        if not batch:
            # Circular dependency — just dump remaining
            logger.warning(f"Circular dependency detected: {remaining}")
            order.extend(remaining)
            break
        order.extend(batch)
        remaining -= set(batch)
    return order
