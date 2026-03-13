"""
Cel-Logic Pro — Data Migration
Prevents save corruption when addon versions change.
Called during register() to upgrade old project data.
"""

import bpy
from ..config import DATA_VERSION, ADDON_NAME
from .. import logger


def migrate(scene):
    """
    Run version migrations on a scene.
    Reads scene['cellogic_version'] and applies incremental upgrades.
    """
    if scene is None:
        return

    stored = tuple(scene.get("cellogic_version", (0, 0, 0)))

    if stored >= DATA_VERSION:
        return  # Already up to date

    logger.info(f"Migrating scene '{scene.name}' from v{stored} to v{DATA_VERSION}")

    if stored < (1, 0, 0):
        _migrate_to_1_0_0(scene)

    # Future migrations go here:
    # if stored < (1, 1, 0):
    #     _migrate_to_1_1_0(scene)

    scene["cellogic_version"] = list(DATA_VERSION)
    logger.info(f"Migration complete for '{scene.name}'")


def _migrate_to_1_0_0(scene):
    """Initial version — stamp version on scene."""
    logger.debug("Applying v1.0.0 migration (initial stamp)")


def migrate_all_scenes():
    """Run migration on every scene in the file."""
    for scene in bpy.data.scenes:
        try:
            migrate(scene)
        except Exception as e:
            logger.error(f"Migration failed for scene '{scene.name}': {e}")
