from ECS.Components import (
    MegaGemTag,
    PlayerStatsComponent,
    SpacialComponent,
    RenderComponent,
    HealthComponent,
    ShieldComponent,
    TrailComponent,
    ExperienceGemComponent,
    DashComponent,
    BossTag,
)
from ECS.Systems import CameraSystem

import pygame
import math

from Globals import Misc
from Globals import Settings
from Globals.ParticleManager import ParticleManager

DEBUG_FONT = pygame.font.SysFont("Arial", 12)


def process(
    surface: pygame.Surface,
    world: dict,
    camera: dict,
    visible_entities: list,
    dt: float,
):
    camera_rect: pygame.Rect = camera[SpacialComponent].rect
    cam_boundary = CameraSystem.get_boundary_of(camera)

    rendering_data = Misc.get_camera_rendering_data(cam_boundary)

    game_entities_rendered_surface = draw_game_entities(
        world, cam_boundary, camera_rect, visible_entities, dt
    )
    entities_transformed_surface = pygame.transform.scale(
        game_entities_rendered_surface, rendering_data["size"]
    )

    surface.blit(entities_transformed_surface, rendering_data["offset"])


def draw_game_entities(
    world: dict, cam_boundary: dict, camera_rect, visible_entities: list, dt: float
):
    cbw, cbh = cam_boundary["world_size"]
    render_surface = pygame.Surface((cbw, cbh))
    render_surface.fill((10, 10, 14))  # Moody background

    # 1. DRAW THE GRID
    tile_size = Settings.SPRITE.WIDTH * 2
    grid_color = (25, 25, 35)
    offset_x = -(camera_rect.left % tile_size)
    offset_y = -(camera_rect.top % tile_size)
    for x in range(int(offset_x), cbw, tile_size):
        pygame.draw.line(render_surface, grid_color, (x, 0), (x, cbh), 2)
    for y in range(int(offset_y), cbh, tile_size):
        pygame.draw.line(render_surface, grid_color, (0, y), (cbw, y), 2)

    # Pre-sort entities once for the actors pass
    sorted_entities = sorted(
        visible_entities, key=lambda obj_id: world[obj_id][RenderComponent].z_index
    )

    # ==========================================
    # PASS 1: THE FLOOR (Shadows and Auras)
    # ==========================================
    for obj_id in visible_entities:  # No sorting needed for the floor
        obj = world[obj_id]
        if SpacialComponent in obj:
            obj_rect = obj[SpacialComponent].rect
            render_pos = (
                obj_rect.left - camera_rect.left,
                obj_rect.top - camera_rect.top,
            )

            # --- THE DROP SHADOW ---
            if (
                HealthComponent in obj
                or PlayerStatsComponent in obj
                or ExperienceGemComponent in obj
            ):
                shadow_w = int(obj_rect.width * 0.7)
                shadow_h = int(obj_rect.width * 0.3)
                shadow_x = render_pos[0] + (obj_rect.width - shadow_w) // 2
                shadow_y = render_pos[1] + obj_rect.height - (shadow_h // 2)

                # Optimized Shadow: Using draw instead of creating surfaces per-frame
                pygame.draw.ellipse(
                    render_surface, (5, 5, 8), (shadow_x, shadow_y, shadow_w, shadow_h)
                )

            # --- THE MEGA GEM AURA ---
            if ExperienceGemComponent in obj and MegaGemTag in obj:
                pulse = abs(math.sin(pygame.time.get_ticks() * 0.005))
                aura_radius = int(obj_rect.width * (1.2 + pulse * 0.8))
                aura_surf = pygame.Surface(
                    (aura_radius * 2, aura_radius * 2), pygame.SRCALPHA
                )
                pygame.draw.circle(
                    aura_surf,
                    (255, 215, 0, 80 + int(pulse * 50)),
                    (aura_radius, aura_radius),
                    aura_radius,
                )
                render_surface.blit(
                    aura_surf,
                    aura_surf.get_rect(
                        center=(
                            render_pos[0] + obj_rect.width // 2,
                            render_pos[1] + obj_rect.height // 2,
                        )
                    ),
                )

            # --- DASH GHOST TRAIL ---
            if (
                DashComponent in obj
                and RenderComponent in obj
                and obj[RenderComponent].sprite
            ):
                dash = obj[DashComponent]
                if dash.ghosts:
                    # Create the solid Cyan silhouette once
                    ghost_sprite = get_hit_surface(obj[RenderComponent].sprite)
                    ghost_sprite.fill(
                        (0, 255, 255, 255), special_flags=pygame.BLEND_RGBA_MULT
                    )

                    for ghost in dash.ghosts:
                        ghost_x, ghost_y, alpha = ghost
                        # Translate world pixel coords to camera coords
                        render_ghost_x = ghost_x - camera_rect.left
                        render_ghost_y = ghost_y - camera_rect.top

                        # Apply the fading transparency and draw onto the floor layer
                        temp_sprite = ghost_sprite.copy()
                        temp_sprite.set_alpha(int(alpha))
                        render_surface.blit(
                            temp_sprite, (render_ghost_x, render_ghost_y)
                        )

    # ==========================================
    # PASS 2: THE ACTORS (Sprites, Shields, UI)
    # ==========================================
    for obj_id in sorted_entities:
        obj = world[obj_id]
        if SpacialComponent in obj and RenderComponent in obj:
            obj_rect = obj[SpacialComponent].rect
            render_pos = (
                obj_rect.left - camera_rect.left,
                obj_rect.top - camera_rect.top,
            )
            render_rect = pygame.Rect(render_pos, obj_rect.size)

            # --- DRAW SPRITE ---
            if obj[RenderComponent].sprite:
                working_sprite = obj[RenderComponent].sprite

                # Boss/MegaGem Scaling
                if MegaGemTag in obj or BossTag in obj:
                    working_sprite = working_sprite.copy()
                    if MegaGemTag in obj:
                        working_sprite.fill(
                            (255, 200, 0, 255), special_flags=pygame.BLEND_RGBA_MULT
                        )

                    new_size = (int(obj_rect.width * 1.5), int(obj_rect.height * 1.5))
                    working_sprite = pygame.transform.scale(working_sprite, new_size)
                    render_rect = working_sprite.get_rect(center=render_rect.center)

                render_surface.blit(working_sprite, render_rect)
            else:
                pygame.draw.rect(
                    render_surface, obj[RenderComponent].color, render_rect
                )

            # ==========================================
            # OVERLAYS (Shields, HP, Trails, Flashes)
            # ==========================================

            # SHIELD VISUAL
            if ShieldComponent in obj:
                s = obj[ShieldComponent]
                if s.active:
                    # Create a transparent surface for the 'bubble'
                    s_size = (
                        obj[SpacialComponent].rect.width + Settings.GAME.SHIELD_RADIUS
                    )
                    shield_surf = pygame.Surface((s_size, s_size), pygame.SRCALPHA)

                    # Pulsing Alpha based on time
                    alpha = 100 + int(math.sin(pygame.time.get_ticks() * 0.01) * 30)
                    color = (0, 150, 255, alpha)  # Transparent Blue

                    pygame.draw.circle(
                        shield_surf, color, (s_size // 2, s_size // 2), s_size // 2, 2
                    )
                    # Draw the 'glow'
                    pygame.draw.circle(
                        shield_surf,
                        (0, 150, 255, 40),
                        (s_size // 2, s_size // 2),
                        s_size // 2 - 1,
                    )

                    render_surface.blit(
                        shield_surf, shield_surf.get_rect(center=render_rect.center)
                    )

            # DRAW HEALTH BAR
            hp_data = None
            if PlayerStatsComponent in obj:
                hp_data = (
                    obj[PlayerStatsComponent].current_hp,
                    obj[PlayerStatsComponent].final_max_hp,
                )
            elif HealthComponent in obj:
                hp_data = (obj[HealthComponent].hp, obj[HealthComponent].max_hp)

            if hp_data:
                curr, m_hp = hp_data
                hp_perc = max(0, min(1, curr / m_hp))

                bar_w = obj_rect.width
                bar_h = Settings.SPRITE.HEIGHT // 6
                bx, by = render_pos[0], render_pos[1] - bar_h

                # HEALTH BAR
                pygame.draw.rect(
                    render_surface, (80, 0, 0), (bx, by, bar_w, bar_h)
                )  # Background
                pygame.draw.rect(
                    render_surface, (0, 200, 0), (bx, by, bar_w * hp_perc, bar_h)
                )  # Foreground

                # --- PLAYER SPECIFIC BARS (HP -> XP -> DASH) ---
                if PlayerStatsComponent in obj:
                    stats = obj[PlayerStatsComponent]

                    # 1. XP BAR
                    xp_perc = max(0, min(1, stats.xp / stats.xp_to_next_level))
                    xp_by = by - bar_h
                    pygame.draw.rect(
                        render_surface, (20, 20, 0), (bx, xp_by, bar_w, bar_h)
                    )
                    pygame.draw.rect(
                        render_surface,
                        (255, 200, 0),
                        (bx, xp_by, bar_w * xp_perc, bar_h),
                    )

                    # 2. DASH BAR
                    if DashComponent in obj:
                        dash = obj[DashComponent]
                        dash_by = xp_by - bar_h

                        # Calculate progress (0.0 to 1.0)
                        dash_perc = 1.0 - (dash.cooldown_timer / dash.cooldown)

                        # Background
                        pygame.draw.rect(
                            render_surface, (0, 30, 40), (bx, dash_by, bar_w, bar_h)
                        )

                        # Foreground (Cyan)
                        bar_color = (0, 255, 255)

                        # --- THE FLASH LOGIC ---
                        if dash.cooldown_timer <= 0:
                            # Pulse white when ready
                            pulse = abs(math.sin(pygame.time.get_ticks() * 0.01))
                            if pulse > 0.5:
                                bar_color = (200, 255, 255)  # Light glow

                        pygame.draw.rect(
                            render_surface,
                            bar_color,
                            (bx, dash_by, bar_w * dash_perc, bar_h),
                        )

            # XP GEM TRAILS
            if TrailComponent in obj and ExperienceGemComponent in obj:
                trail = obj[TrailComponent]
                # Record the current center position
                center_pos = obj[SpacialComponent].rect.center
                trail.history.append(center_pos)

                # Keep the history at the max length
                if len(trail.history) > trail.length:
                    trail.history.pop(0)

                # Draw the Trail (Only if it's currently being vacummed)
                if len(trail.history) > 1 and trail.history[0] != center_pos:
                    # Draw from oldest to newest
                    for i in range(len(trail.history) - 1):
                        start_pt = trail.history[i]
                        end_pt = trail.history[i + 1]

                        # Offset points by camera
                        cam_start = (
                            start_pt[0] - camera_rect.x,
                            start_pt[1] - camera_rect.y,
                        )
                        cam_end = (end_pt[0] - camera_rect.x, end_pt[1] - camera_rect.y)

                        # Tail is 1px, gets thicker as it approaches the gem
                        thickness = max(1, i)

                        # Draw a nice bright line for XP
                        pygame.draw.line(
                            render_surface, (0, 255, 255), cam_start, cam_end, thickness
                        )

            # Hit Flash
            if HealthComponent in obj and obj[HealthComponent].hit_timer > 0:
                if obj[RenderComponent].sprite:
                    hit_sprite = get_hit_surface(obj[RenderComponent].sprite)

                    # NEW: Scale the flash to match the render_rect!
                    if BossTag in obj or MegaGemTag in obj:
                        hit_sprite = pygame.transform.scale(
                            hit_sprite, render_rect.size
                        )

                    render_surface.blit(hit_sprite, render_rect)
                else:
                    pygame.draw.rect(render_surface, (255, 255, 255), render_rect)

                obj[HealthComponent].hit_timer -= dt

    ParticleManager.update_and_draw(
        render_surface,
        dt,
        # Ensure these are PIXEL offsets!
        cam_x=cam_boundary["left"] * Settings.CELLS.WIDTH,
        cam_y=cam_boundary["top"] * Settings.CELLS.HEIGHT,
    )

    return render_surface


def get_hit_surface(sprite):
    # Create a mask from the sprite
    mask = pygame.mask.from_surface(sprite)
    # Convert that mask into a surface
    hit_surf = mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0))
    return hit_surf
