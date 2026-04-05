from Globals import Misc
from ECS.Components import ProjectileComponent, SpacialComponent, EnemyTag
from ECS.Systems import CombatSystem


def process(world: dict, spatial_grid: dict):
    entities_to_delete = set()

    for proj_id in list(world.keys()):
        if proj_id not in world:
            continue

        if ProjectileComponent in world[proj_id] and SpacialComponent in world[proj_id]:
            proj_rect = world[proj_id][SpacialComponent].rect
            grid_pos = world[proj_id][SpacialComponent].grid_pos

            neighbor_cells = [
                (grid_pos[0] + dx, grid_pos[1] + dy)
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
            ]

            for cell in neighbor_cells:
                if cell in spatial_grid:
                    for target_id in list(spatial_grid[cell]):
                        if EnemyTag in world[target_id]:
                            enemy_rect = world[target_id][SpacialComponent].rect

                            if proj_rect.colliderect(enemy_rect):
                                # Call centralized logic!
                                damage = world[proj_id][ProjectileComponent].damage
                                CombatSystem.take_damage(
                                    world,
                                    spatial_grid,
                                    target_id,
                                    damage,
                                    entities_to_delete,
                                )

                                # Projectile always dies on hit
                                entities_to_delete.add(proj_id)
                                break  # Breaks the target_id loop

                    # FIX: If the bullet hit something, stop checking the other cells!
                    if proj_id in entities_to_delete:
                        break

    # Cleanup
    # (Keep your existing cleanup loop here...)

    # Clean up entities
    for ent_id in entities_to_delete:
        if ent_id in world:
            g_pos = world[ent_id][SpacialComponent].grid_pos
            Misc.remove_entity_from_grid(ent_id, g_pos, spatial_grid)
            del world[ent_id]
