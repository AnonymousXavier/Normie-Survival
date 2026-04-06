import math
import pygame
from Core import States  # <-- ADD THIS TO IMPORTS
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
    # --- 1. THE ANCHOR FIX ---
    player = world.get(States.PLAYER_ID)
    if not player or SpacialComponent not in player:
        return

    px = player[SpacialComponent].rect.centerx
    py = player[SpacialComponent].rect.centery

    cam_boundary = CameraSystem.get_boundary_of(camera)
    visible_ids = Misc.get_entities_on_screen(spatial_grid, cam_boundary)

    for obj_id in list(world.keys()):
        obj = world[obj_id]
        if PowerUpTag in obj and RotationComponent in obj and RenderComponent in obj:
            target_enemy_id = None
            closest_dist_sq = float("inf")

            # Find closest enemy using the PLAYER'S position (px, py), not the gun's!
            for v_id in visible_ids:
                if EnemyTag in world[v_id] and SpacialComponent in world[v_id]:
                    ex = world[v_id][SpacialComponent].rect.centerx
                    ey = world[v_id][SpacialComponent].rect.centery

                    dx = ex - px
                    dy = ey - py
                    dist_sq = (dx * dx) + (dy * dy)

                    if dist_sq < closest_dist_sq:
                        closest_dist_sq = dist_sq
                        target_enemy_id = v_id

            if target_enemy_id:
                obj[WeaponComponent].has_target = True
                ex = world[target_enemy_id][SpacialComponent].rect.centerx
                ey = world[target_enemy_id][SpacialComponent].rect.centery

                # Calculate aim from the PLAYER to the ENEMY
                aim_dx = ex - px
                aim_dy = ey - py

                # 1. Get the actual target angle
                target_angle_deg = math.degrees(math.atan2(-aim_dy, aim_dx))
                current_angle = obj[RotationComponent].angle

                # 2. SMOOTH INTERPOLATION
                diff = (target_angle_deg - current_angle + 180) % 360 - 180
                smoothed_angle = current_angle + (diff * 0.15)

                # 3. DIRECTIONAL ORBITING
                if OrbitalComponent in obj:
                    obj[OrbitalComponent].angle = (
                        -smoothed_angle + obj[OrbitalComponent].offset_angle
                    )

                # 4. RENDERING
                if abs(diff) > 0.5:
                    obj[RotationComponent].angle = smoothed_angle
                    base_sprite = obj[RenderComponent].base_sprite
                    if base_sprite:
                        if abs(smoothed_angle) > 90:
                            working_sprite = pygame.transform.flip(
                                base_sprite, False, True
                            )
                        else:
                            working_sprite = base_sprite

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
