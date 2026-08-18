DRONE_CONFIG = {

    # One-time cost (in uncommon parts) to unlock the drone.
    "unlock_cost": 8,

    # Stats at level 1 (right after unlocking).
    "base_damage": 6,
    "damage_multiplier": 1.2,

    "base_fire_interval": 1.2,
    "fire_interval_multiplier": 0.88,

    # Cost (in uncommon parts) to go from level 1 -> 2, 2 -> 3, etc.
    "upgrade_base_cost": 4,
    "upgrade_cost_multiplier": 1.5,

    # Level 0 = locked. Level max_level = fully upgraded.
    "max_level": 5,

    # Fixed, not affected by level.
    "orbit_radius": 55,
    "orbit_speed": 90,
    "detection_range": 500,

}