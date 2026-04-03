import math
import pygame
from ECS.Components import SpacialComponent, RenderComponent, RotationComponent, PowerUpTag, EnemyTag
from ECS.Systems import CameraSystem
from Globals import Misc

def process(world: dict, spatial_grid: dict, camera: dict):
    # Grab everything on screen
    cam_boundary = CameraSystem.get_boundary_of(camera)
    visible_ids = Misc.get_entities_on_screen(spatial_grid, cam_boundary)
    
    for obj_id in list(world.keys()):
        obj = world[obj_id]
        if PowerUpTag in obj and RotationComponent in obj and RenderComponent in obj:
            
            # Get the weapons position
            gx = obj[SpacialComponent].rect.centerx
            gy = obj[SpacialComponent].rect.centery
            
            target_enemy_id = None
            closest_dist_sq = float('inf')

            # Find closest enemy
            for v_id in visible_ids:
                if EnemyTag in world[v_id] and SpacialComponent in world[v_id]:
                    ex = world[v_id][SpacialComponent].rect.centerx
                    ey = world[v_id][SpacialComponent].rect.centery
                    
                    dx = ex - gx
                    dy = ey - gy
                    dist_sq = (dx * dx) + (dy * dy) 
                    
                    if dist_sq < closest_dist_sq:
                        closest_dist_sq = dist_sq
                        target_enemy_id = v_id

            # Only rotate if we actually found a target
            if target_enemy_id:
                ex = world[target_enemy_id][SpacialComponent].rect.centerx
                ey = world[target_enemy_id][SpacialComponent].rect.centery
                
                aim_dx = ex - gx
                aim_dy = ey - gy
                
                angle_rad = math.atan2(-aim_dy, aim_dx)
                angle_deg = math.degrees(angle_rad)

                current_angle = obj[RotationComponent].angle
                
                # Only re-render if the angle shifted enough to save CPU
                if abs(current_angle - angle_deg) > 2.0:
                    obj[RotationComponent].angle = angle_deg
                    
                    base_sprite = obj[RenderComponent].base_sprite
                    if base_sprite:
                        rotated_sprite = pygame.transform.rotate(base_sprite, angle_deg)
                        new_rect = rotated_sprite.get_rect(center=obj[SpacialComponent].rect.center)
                        obj[SpacialComponent].rect.size = new_rect.size
                        obj[RenderComponent].sprite = rotated_sprite