from Core import States
from ECS.Components import (
    AOEComponent,
    SpacialComponent,
    EnemyTag,
    CameraShakeComponent,
)
from ECS.Systems import CombatSystem
from Globals import Misc
from Globals.ParticleManager import ParticleManager
from Globals import Settings


def process(world: dict, spatial_grid: dict, dt: float):
    if States.PLAYER_ID not in world:
        return

    player = world[States.PLAYER_ID]
    if AOEComponent not in player:
        return

    aoe = player[AOEComponent]
    aoe.timer += dt

    if aoe.timer >= aoe.cooldown:
        aoe.timer = 0
        p_pos = player[SpacialComponent].grid_pos

        # Grab physical center for the starting point of the lightning
        p_center = player[SpacialComponent].rect.center

        r = int(aoe.radius)

        entities_to_delete = set()
        hit_something = False  # Track if we actually hit anything for screen shake

        # Scan the grid area
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                cell = (p_pos[0] + dx, p_pos[1] + dy)
                if cell in spatial_grid:
                    for e_id in list(spatial_grid[cell]):
                        enemy = world.get(e_id)
                        if enemy and EnemyTag in enemy:
                            # VISUALS: Get physical center of the enemy BEFORE they take damage/die
                            e_center = enemy[SpacialComponent].rect.center

                            # Draw lightning bolt from player to enemy
                            ParticleManager.emit_lightning(p_center, e_center)

                            # Explode sparks directly on the enemy
                            ParticleManager.emit_sparks(e_center[0], e_center[1])

                            hit_something = True

                            # 2. LOGIC: Deal the actual damage
                            CombatSystem.take_damage(
                                world,
                                spatial_grid,
                                e_id,
                                aoe.damage,
                                entities_to_delete,
                            )

        # 3. IMPACT: Trigger Screen Shake ONCE per pulse (if we hit something)
        if hit_something and Settings.GAME_OPTIONS.SCREEN_SHAKE:
            # Assuming you handle camera shake frames in your CameraSystem
            States.camera[CameraShakeComponent].intensity = 2.0

        # Clean up dead enemies killed by the AOE pulse
        for ent_id in entities_to_delete:
            if ent_id in world:
                g_pos = world[ent_id][SpacialComponent].grid_pos
                Misc.remove_entity_from_grid(ent_id, g_pos, spatial_grid)
                del world[ent_id]
