from Core import States
from ECS.Components import SpacialComponent, ExperienceGemComponent, PlayerStatsComponent
from Globals import Misc

def process(world: dict, spatial_grid: dict):
    player = world[States.PLAYER_ID]
    player_grid_pos = player[SpacialComponent].grid_pos
    player_stats = player.get(PlayerStatsComponent)

    if not player_stats:
        return

    # 2. Check the player's current cell in the spatial grid
    if player_grid_pos in spatial_grid:
        # We use a copy of the list to avoid "dictionary size changed during iteration" errors
        for entity_id in list(spatial_grid[player_grid_pos]):
            entity_components = world.get(entity_id)
            
            if entity_components and ExperienceGemComponent in entity_components:
                # Gaining the XP
                gem_value = entity_components[ExperienceGemComponent].value
                player_stats.xp += gem_value
                
                # Cleanup: Remove from grid and world
                Misc.remove_entity_from_grid(entity_id, player_grid_pos, spatial_grid)
                del world[entity_id]
                
                print(f"XP Gained: {gem_value} | Total: {player_stats.xp}/{player_stats.xp_to_next_level}")