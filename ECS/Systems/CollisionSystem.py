from ECS.Components import ProjectileComponent, SpacialComponent, EnemyTag, HealthComponent
from Globals import Misc

def process(world: dict, spatial_grid: dict):
    entities_to_delete = set()

    # Find all projectiles
    for proj_id in list(world.keys()):
        if ProjectileComponent in world[proj_id] and SpacialComponent in world[proj_id]:
            proj_rect = world[proj_id][SpacialComponent].rect
            grid_pos = world[proj_id][SpacialComponent].grid_pos
            
            # Check the current and neighboring grid cells for enemies
            neighbor_cells = [
                (grid_pos[0] + dx, grid_pos[1] + dy)
                for dx in [-1, 0, 1] for dy in [-1, 0, 1]
            ]

            for cell in neighbor_cells:
                if cell in spatial_grid:
                    for target_id in spatial_grid[cell]:
                        # 3. Collision logic
                        if EnemyTag in world[target_id] and HealthComponent in world[target_id]:
                            enemy_rect = world[target_id][SpacialComponent].rect
                            
                            if proj_rect.colliderect(enemy_rect):
                                # Apply damage
                                world[target_id][HealthComponent].hp -= world[proj_id][ProjectileComponent].damage
                                
                                # Mark bullet for removal
                                entities_to_delete.add(proj_id)
                                
                                # Mark enemy if dead
                                if world[target_id][HealthComponent].hp <= 0:
                                    entities_to_delete.add(target_id)

    # Clean up entities
    for ent_id in entities_to_delete:
        if ent_id in world:
            g_pos = world[ent_id][SpacialComponent].grid_pos
            Misc.remove_entity_from_grid(ent_id, g_pos, spatial_grid)
            del world[ent_id]