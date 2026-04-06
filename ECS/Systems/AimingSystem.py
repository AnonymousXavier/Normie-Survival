import math
import pygame
from ECS.Components import (
    SpacialComponent,
    RenderComponent,
    RotationComponent,
    PowerUpTag,
    EnemyTag,
    OrbitalComponent,
    WeaponComponent,
)
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
            closest_dist_sq = float("inf")

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
                obj[WeaponComponent].has_target = True
                ex = world[target_enemy_id][SpacialComponent].rect.centerx
                ey = world[target_enemy_id][SpacialComponent].rect.centery

                aim_dx = ex - gx
                aim_dy = ey - gy

                # 1. Get the actual target angle
                target_angle_deg = math.degrees(math.atan2(-aim_dy, aim_dx))
                current_angle = obj[RotationComponent].angle

                # 2. SMOOTH INTERPOLATION (LERP)
                # Find the shortest distance between current and target angle (-180 to +180)
                diff = (target_angle_deg - current_angle + 180) % 360 - 180

                # Move 15% of the way to the target this frame (Increase to snap faster, decrease to turn slower)
                smoothed_angle = current_angle + (diff * 0.15)

                # 3. DIRECTIONAL ORBITING
                if OrbitalComponent in obj:
                    # Invert the smoothed angle for the position to fix Pygame's upside-down Y axis!
                    obj[OrbitalComponent].angle = (
                        -smoothed_angle + obj[OrbitalComponent].offset_angle
                    )

                # 4. RENDERING (Only re-render if it moved enough to save CPU on micro-jitters)
                if abs(diff) > 0.5:
                    obj[RotationComponent].angle = smoothed_angle

                    base_sprite = obj[RenderComponent].base_sprite
                    if base_sprite:
                        # --- THE FLIP FIX ---
                        if abs(smoothed_angle) > 90:
                            working_sprite = pygame.transform.flip(
                                base_sprite, False, True
                            )
                        else:
                            working_sprite = base_sprite

                        # --- ROTOZOOM ---
                        rotated_sprite = pygame.transform.rotozoom(
                            working_sprite, smoothed_angle, 1.0
                        )
                        new_rect = rotated_sprite.get_rect(
                            center=obj[SpacialComponent].rect.center
                        )
                        obj[SpacialComponent].rect.size = new_rect.size
                        obj[RenderComponent].sprite = rotated_sprite
            else:
                obj[WeaponComponent].has_target = False
