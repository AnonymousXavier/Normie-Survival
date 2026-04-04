from Core import States
from ECS.Components import SpacialComponent
from Globals import Misc

# NOTE: Removed CollectorComponent and ExperienceGemComponent. 
# This system is now strictly for stepping on non-XP items (like health potions later).

def process(world: dict, spatial_grid: dict):
    if States.PLAYER_ID not in world:
        return
        
    player_obj = world[States.PLAYER_ID]
    p_pos = player_obj[SpacialComponent].grid_pos
        
    if p_pos in spatial_grid:
        for entity_id in list(spatial_grid[p_pos]):
            target_entity = world.get(entity_id)
            
            
            # Future Logic: If target_entity has HealthPotionComponent, GoldComponent, etc.
            # Do NOT check for ExperienceGemComponent here anymore!
            
            pass