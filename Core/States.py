from ECS import Components


world = {}
spatial_grid = {}

camera = {}

PLAYER_ID = 1
NEXT_ENTITY_ID = 1
NEXT_DEBUG_ELEMENT_ID = 1
PLAYER_ID = 1

GAME_RUNNING = True
IS_LEVELING_UP = False


# The single source of truth for all shotguns
global_shotgun_stats = Components.WeaponStats()