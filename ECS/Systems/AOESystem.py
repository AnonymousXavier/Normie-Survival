# ECS/Systems/AOESystem.py
import math
from Core import States
from ECS.Components import AOEComponent, SpacialComponent, EnemyTag
from ECS.Systems import CombatSystem
from Globals import Settings


def process(world: dict, spatial_grid: dict, dt: float):
    # 1. Find the source of the AOE (usually the Player)
    if States.PLAYER_ID not in world:
        return

    player = world[States.PLAYER_ID]
    if AOEComponent not in player:
        return

    aoe = player[AOEComponent]
    p_pos = player[SpacialComponent].rect.center  # Center of the player

    # 2. Handle the Cooldown Timer
    aoe.timer += dt
    if aoe.timer < aoe.cooldown:
        return

    # 3. Trigger the Pulse!
    aoe.timer = 0
    radius_px = aoe.radius * Settings.SPRITE.WIDTH

    # 4. Find enemies in range using the Spatial Grid for efficiency
    grid_r = int(aoe.radius) + 1
    p_grid_x, p_grid_y = player[SpacialComponent].grid_pos

    for dx in range(-grid_r, grid_r + 1):
        for dy in range(-grid_r, grid_r + 1):
            cell = (p_grid_x + dx, p_grid_y + dy)
            if cell in spatial_grid:
                for target_id in list(spatial_grid[cell]):
                    enemy = world.get(target_id)
                    if enemy and EnemyTag in enemy:
                        e_pos = enemy[SpacialComponent].rect.center

                        # Distance Check (Standard Pythagorean)
                        dist = math.sqrt(
                            (p_pos[0] - e_pos[0]) ** 2 + (p_pos[1] - e_pos[1]) ** 2
                        )

                        if dist <= radius_px:
                            # BOOM! Apply the damage through your central system
                            CombatSystem.take_damage(
                                world, spatial_grid, target_id, aoe.damage
                            )
