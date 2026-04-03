from ECS.Components import ExperienceGemComponent, SpacialComponent, CollectorComponent, PlayerStatsComponent
from Globals import Misc

def process(world: dict, spatial_grid: dict):
    for obj in list(world.values()):
        if CollectorComponent in obj and PlayerStatsComponent in obj:
            p_pos = obj[SpacialComponent].grid_pos
            p_stats = obj[PlayerStatsComponent]
            p_range = obj[CollectorComponent].range
            
            # Check neighbors based on collector range
            r = int(p_range)
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    cell = (p_pos[0] + dx, p_pos[1] + dy)
                    
                    if cell in spatial_grid:
                        # Use a copy of the list because we might delete gems while iterating
                        for entity_id in list(spatial_grid[cell]):
                            if ExperienceGemComponent in world.get(entity_id, {}):
                                # Add XP
                                p_stats.xp += world[entity_id][ExperienceGemComponent].value
                                
                                # Remove Gem
                                Misc.remove_entity_from_grid(entity_id, cell, spatial_grid)
                                del world[entity_id]
                                
                                # Trigger Level Up check
                                if p_stats.xp >= p_stats.xp_to_next_level:
                                    level_up(p_stats)

def level_up(stats):
    stats.level += 1
    stats.xp = 0
    stats.xp_to_next_level = int(stats.xp_to_next_level * 1.5)
    print(f"LEVEL UP! Reached Level {stats.level}")
    # This is where you'll eventually trigger the UI to buff States.global_shotgun_stats