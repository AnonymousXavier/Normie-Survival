from Core import States
from ECS.Components import ExperienceGemComponent, SpacialComponent, CollectorComponent, PlayerStatsComponent
from ECS.Builders.LevelUpMenuBuilder import LevelUpMenuBuilder
from Globals import Misc, Upgrades

def process(world: dict, spatial_grid: dict):    
    if States.PLAYER_ID not in world:
        return
        
    player_obj = world[States.PLAYER_ID]
    
    # Safety check for required components
    if CollectorComponent in player_obj and PlayerStatsComponent in player_obj:
        p_pos = player_obj[SpacialComponent].grid_pos
        p_stats = player_obj[PlayerStatsComponent]
        p_range = player_obj[CollectorComponent].range
        
        r = int(p_range)
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                cell = (p_pos[0] + dx, p_pos[1] + dy)
                
                if cell in spatial_grid:
                    for entity_id in list(spatial_grid[cell]):
                        target_entity = world.get(entity_id)
                        if target_entity and ExperienceGemComponent in target_entity:
                            # Add XP
                            p_stats.xp += target_entity[ExperienceGemComponent].value
                            print(f"XP: {p_stats.xp} / {p_stats.xp_to_next_level}")
                            
                            # Cleanup
                            Misc.remove_entity_from_grid(entity_id, cell, spatial_grid)
                            del world[entity_id]
                            
                            # Level check
                            if p_stats.xp >= p_stats.xp_to_next_level:
                                level_up(p_stats, world)

def level_up(stats, world):
    # 1. Standard Level Up Logic
    stats.level += 1
    stats.xp = 0 # Or keep the remainder if you're fancy
    stats.xp_to_next_level = int(stats.xp_to_next_level * 1.5)

    print(f"LEVEL UP! Reached Level {stats.level}")
    
    # 2. Get the Options
    options = Upgrades.get_random_upgrades(stats.upgrades_owned)
    
    # 3. Build the UI using our dynamic builder!
    LevelUpMenuBuilder.build(options)
    
    # 4. Pause the world so the menu can be interacted with
    States.IS_LEVELING_UP = True