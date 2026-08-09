WIDTH = 800
HEIGHT = 600

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# -----------------------------
# HUD Theme — Techno Green
# -----------------------------

TECHNO_GREEN = (57, 255, 140)
TECHNO_GREEN_DIM = (30, 140, 90)
TECHNO_GREEN_DARK = (10, 35, 25)

# -----------------------------
# Sector Generation
# -----------------------------

SECTOR_RADIUS = 10000

OUTPOST_COUNT = 8

# Used later when we start scaling difficulty
SECTOR_RADIUS_MULTIPLIER = 2.0

# -----------------------------
# Player
# -----------------------------

PLAYER_MAX_HEALTH = 100

# Used for asteroid/player collision detection
PLAYER_COLLISION_RADIUS = 16

# Seconds of invulnerability after taking a hit
PLAYER_INVULNERABILITY_DURATION = 1.5

# -----------------------------
# Salvage
# -----------------------------

# How close the player must get to auto-collect a pickup
SALVAGE_PICKUP_RADIUS = 40

# Seconds before an uncollected pickup disappears
SALVAGE_LIFETIME = 12.0

# Value range used to scale pickup visual size
SALVAGE_MIN_VALUE = 3
SALVAGE_MAX_VALUE = 25

SALVAGE_MIN_RADIUS = 4
SALVAGE_MAX_RADIUS = 12

# -----------------------------
# Docking
# -----------------------------

# Distance from a hub within which the player can dock
HUB_DOCKING_RANGE = 150