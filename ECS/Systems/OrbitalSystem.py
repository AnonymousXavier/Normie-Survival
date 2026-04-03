import math
from ECS.Components import OrbitalComponent, SpacialComponent
from Globals import Settings, Misc

def process(world: dict, spatial_grid: dict, delta: float):
    # Used list to avoid dictionary size errors when the world dict changes
    for obj_id in list(world.keys()):
        if OrbitalComponent in world[obj_id] and SpacialComponent in world[obj_id]:
            obj = world[obj_id]
            orbital = obj[OrbitalComponent]
            
            if orbital.target_id not in world or SpacialComponent not in world[orbital.target_id]:
                continue
                
            target_rect = world[orbital.target_id][SpacialComponent].rect
            
            if orbital.spin_speed != 0:
                orbital.angle += orbital.spin_speed * delta
                orbital.angle %= 360
                
            # The Geometry
            angle_rad = math.radians(orbital.angle)
            pixel_radius = orbital.radius * Settings.SPRITE.WIDTH
            
            offset_x = math.cos(angle_rad) * pixel_radius
            offset_y = math.sin(angle_rad) * pixel_radius
            
            # Apply the position relative to the target's exact center
            new_cx = target_rect.centerx + offset_x
            new_cy = target_rect.centery + offset_y
            
            spacial = obj[SpacialComponent]
            spacial.rect.center = (round(new_cx), round(new_cy))
            
            # Update Spatial Grid
            old_grid = spacial.grid_pos
            new_grid = (spacial.rect.x // Settings.SPRITE.WIDTH, 
                        spacial.rect.y // Settings.SPRITE.HEIGHT)
            
            if old_grid != new_grid:
                Misc.remove_entity_from_grid(obj_id, old_grid, spatial_grid)
                Misc.register_entity_in_grid(obj_id, new_grid, spatial_grid)
                spacial.grid_pos = new_grid