from Core import States
from ECS.Components import (
    ExperienceGemComponent,
    SpacialComponent,
    CollectorComponent,
    PlayerStatsComponent,
    MegaGemTag,
)
from ECS.Builders.VictoryMenuBuilder import VictoryMenuBuilder
from ECS.Builders.LevelUpMenuBuilder import LevelUpMenuBuilder
from Globals import Misc, Settings, Upgrades
from Globals.AudioManager import AudioManager


def process(world: dict, spatial_grid: dict, dt: float):
    if States.PLAYER_ID not in world:
        return

    player = world[States.PLAYER_ID]
    if CollectorComponent not in player or PlayerStatsComponent not in player:
        return

    p_pos = player[SpacialComponent].rect.center
    p_stats = player[PlayerStatsComponent]
    p_range_grid = player[CollectorComponent].range

    # Pre-calculate Squared Distances
    magnet_range_sq = (p_range_grid * Settings.SPRITE.WIDTH) ** 2
    collection_range_sq = 15**2  # 15 pixels squared
    pull_speed = 250

    grid_r = int(p_range_grid) + 1
    p_grid_x, p_grid_y = player[SpacialComponent].grid_pos

    # The Vacuum Cap
    MAX_PULLS_PER_FRAME = 30
    pulls_this_frame = 0

    for dx in range(-grid_r, grid_r + 1):
        for dy in range(-grid_r, grid_r + 1):
            cell = (p_grid_x + dx, p_grid_y + dy)
            if cell not in spatial_grid:
                continue

            # Iterate over a COPY of the list since we also delete gems
            for gem_id in list(spatial_grid[cell]):
                gem = world.get(gem_id)
                if not gem or ExperienceGemComponent not in gem:
                    continue

                g_rect = gem[SpacialComponent].rect
                g_center = g_rect.center

                dist_x = p_pos[0] - g_center[0]
                dist_y = p_pos[1] - g_center[1]

                # Compare Squared Distances (No math.sqrt)
                dist_sq = dist_x**2 + dist_y**2

                if dist_sq < magnet_range_sq:
                    if dist_sq < collection_range_sq:
                        # COLLECT

                        p_stats.xp += gem[ExperienceGemComponent].value
                        AudioManager.play_sfx("gem_pickup")

                        # CHECK FOR THE WIN CONDITION
                        if MegaGemTag in world[gem_id]:
                            States.CURRENT_STATE = "VICTORY"
                            VictoryMenuBuilder.build(world)
                            AudioManager.play_sfx("victory")

                        Misc.remove_entity_from_grid(gem_id, cell, spatial_grid)
                        del world[gem_id]

                        if States.CURRENT_STATE not in ["VICTORY", "GAME_OVER"]:
                            leveled_up_this_frame = False

                            while p_stats.xp >= p_stats.xp_to_next_level:
                                level_up(p_stats)

                            if leveled_up_this_frame:
                                AudioManager.play_sfx("level_up")
                                States.IS_LEVELING_UP = True

                                # Grab the options and build the menu!
                                options = Upgrades.get_random_upgrades(
                                    p_stats.upgrades_owned
                                )
                                LevelUpMenuBuilder.build(options, p_stats.level)
                    else:
                        # MAGNET PULL
                        if pulls_this_frame >= MAX_PULLS_PER_FRAME:
                            continue

                        pulls_this_frame += 1
                        distance = dist_sq**0.5

                        move_x = (dist_x / distance) * pull_speed * dt
                        move_y = (dist_y / distance) * pull_speed * dt

                        g_rect.x += move_x
                        g_rect.y += move_y

                        # Sync grid position
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


def level_up(stats):
    stats.level += 1
    stats.xp -= stats.xp_to_next_level  # Keep rollover XP

    # THE POLYNOMIAL CURVE
    # Base 10, plus a smoothly increasing amount based on their level.
    # Lvl 1->2: 10 XP. Lvl 10->11: ~168 XP. Lvl 30->31: ~830 XP.
    stats.xp_to_next_level = int(10 + (stats.level**1.5) * 5)

    # Get options and build UI
    options = Upgrades.get_random_upgrades(stats.upgrades_owned)
    LevelUpMenuBuilder.build(options, stats.level)

    # Pause the world
    States.IS_LEVELING_UP = True
