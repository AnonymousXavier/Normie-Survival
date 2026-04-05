from Core import States
from ECS.Components import (
    ExperienceGemComponent,
    SpacialComponent,
    CollectorComponent,
    PlayerStatsComponent,
)
from ECS.Systems import UISystem
from ECS.Builders.LevelUpMenuBuilder import LevelUpMenuBuilder
from Globals import Misc


# ECS/Systems/CollectionSystem.py
import math
from Globals import Settings


def process(world: dict, spatial_grid: dict, dt: float):
    if States.PLAYER_ID not in world:
        return

    player = world[States.PLAYER_ID]
    p_pos = player[SpacialComponent].rect.center  # Use pixel center for smooth math
    p_stats = player[PlayerStatsComponent]
    p_range_grid = player[CollectorComponent].range

    # Convert grid range to pixels for the magnet check
    magnet_range = p_range_grid * Settings.SPRITE.WIDTH
    collection_range = 10  # Pixels (nearly touching)
    pull_speed = 400  # Pixels per second

    # We still use the spatial grid to find nearby gems efficiently
    grid_r = int(p_range_grid) + 1
    p_grid_x, p_grid_y = player[SpacialComponent].grid_pos

    for dx in range(-grid_r, grid_r + 1):
        for dy in range(-grid_r, grid_r + 1):
            cell = (p_grid_x + dx, p_grid_y + dy)
            if cell not in spatial_grid:
                continue

            for gem_id in list(spatial_grid[cell]):
                gem = world.get(gem_id)
                if not gem or ExperienceGemComponent not in gem:
                    continue

                g_rect = gem[SpacialComponent].rect
                g_center = g_rect.center

                # Calculate distance
                dist_x = p_pos[0] - g_center[0]
                dist_y = p_pos[1] - g_center[1]
                distance = math.sqrt(dist_x**2 + dist_y**2)

                if distance < magnet_range:
                    if distance < collection_range:
                        # --- PHASE 2: COLLECT ---
                        p_stats.xp += gem[ExperienceGemComponent].value
                        Misc.remove_entity_from_grid(gem_id, cell, spatial_grid)
                        del world[gem_id]

                        if p_stats.xp >= p_stats.xp_to_next_level:
                            level_up(p_stats, world)
                    else:
                        # --- PHASE 1: MAGNET PULL ---
                        # Move gem toward player
                        move_x = (dist_x / distance) * pull_speed * dt
                        move_y = (dist_y / distance) * pull_speed * dt

                        # Update precise pixel position
                        g_rect.x += move_x
                        g_rect.y += move_y

                        # Sync grid position if it crosses cell boundaries
                        new_grid_pos = (
                            int(g_rect.x // Settings.SPRITE.WIDTH),
                            int(g_rect.y // Settings.SPRITE.HEIGHT),
                        )
                        if new_grid_pos != cell:
                            Misc.remove_entity_from_grid(gem_id, cell, spatial_grid)
                            Misc.register_entity_in_grid(
                                gem_id, new_grid_pos, spatial_grid
                            )
                            gem[SpacialComponent].grid_pos = new_grid_pos


def level_up(p_stats, world):
    # 1. Increment Level
    p_stats.level += 1
    p_stats.xp -= p_stats.xp_to_next_level
    p_stats.xp_to_next_level = int(p_stats.xp_to_next_level * 1.4)

    # 2. Generate the NEW formatted options
    player_entity = world[States.PLAYER_ID]
    options = UISystem.get_level_up_options(
        player_entity
    )  # Now returns 'title' and 'reward'

    # 3. Build Menu (No more KeyError)
    LevelUpMenuBuilder.build(options)

    # 4. Pause Game
    States.IS_LEVELING_UP = True
    print(f"✨ LEVEL {p_stats.level} REACHED!")
