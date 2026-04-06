from ECS.Components import (
    PlayerStatsComponent,
    SpacialComponent,
    RenderComponent,
    HealthComponent,
    ShieldComponent,
    AOEComponent,
    TrailComponent,
    ExperienceGemComponent,
)
from ECS.Systems import CameraSystem

import pygame
import math

from Globals import Misc
from Globals import Settings
from Globals.Settings import SPRITE

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

    sorted_entities = sorted(
        visible_entities, key=lambda obj_id: world[obj_id][RenderComponent].z_index
    )

    render_surface = pygame.Surface((cbw, cbh))
    for obj_id in sorted_entities:
        obj = world[obj_id]
        if SpacialComponent in obj and RenderComponent in obj:
            obj_rect = obj[SpacialComponent].rect
            render_pos = (
                obj_rect.left - camera_rect.left,
                obj_rect.top - camera_rect.top,
            )
            render_rect = pygame.Rect(render_pos, obj_rect.size)

            # 3. AOE VISUAL (Underlay)
            # If this is the AOE entity itself (Orbital), give it a pulse
            # ECS/Systems/RenderingSystem.py (Inside your AOE block)

            if AOEComponent in obj:
                aoe = obj[AOEComponent]

                # t goes from 0.0 to 1.0 as the cooldown charges
                t = aoe.timer / aoe.cooldown

                # --- 1. THE MATH: Cubic Easing ---
                # Cubing the inverted fraction makes it drop incredibly fast.
                # Try changing ** 3 to ** 5 for an even faster snap!
                factor = (t) ** 3

                # The absolute maximum size of the zone
                max_radius_px = int(aoe.radius * Settings.SPRITE.WIDTH)

                # The actual shrinking radius
                current_radius = int(max_radius_px * factor)

                # --- 2. PERFORMANCE: Static Surface Size ---
                # Always make the surface the max size so the CPU doesn't panic
                aoe_surf = pygame.Surface(
                    (max_radius_px * 2, max_radius_px * 2), pygame.SRCALPHA
                )
                center_pt = (max_radius_px, max_radius_px)

                # --- 3. THE VISUALS ---
                # A. The "Threat Zone" Ghost Ring (Always visible, very faint)
                pygame.draw.circle(
                    aoe_surf, (255, 0, 0, 15), center_pt, max_radius_px, 1
                )

                if current_radius > 0:
                    # Fade out the alpha as it shrinks
                    alpha = int(factor * 150)

                    # B. The Shrinking Core
                    pygame.draw.circle(
                        aoe_surf, (255, 50, 50, alpha), center_pt, current_radius
                    )

                    # C. The "Energy Rim" (A brighter, thicker ring on the edge of the shrinking core)
                    rim_thickness = max(1, current_radius // 4)
                    pygame.draw.circle(
                        aoe_surf,
                        (255, 150, 150, alpha + 50),
                        center_pt,
                        current_radius,
                        rim_thickness,
                    )

                # Blit it perfectly centered on the player
                render_surface.blit(
                    aoe_surf, aoe_surf.get_rect(center=render_rect.center)
                )

            # 1. DRAW ENTITY SPRITE/RECT
            if obj[RenderComponent].sprite:
                render_surface.blit(obj[RenderComponent].sprite, render_rect)
            else:
                pygame.draw.rect(
                    render_surface, obj[RenderComponent].color, render_rect
                )

            # 2. SHIELD VISUAL (Overlay)
            if ShieldComponent in obj:
                s = obj[ShieldComponent]
                if s.active:
                    # Create a transparent surface for the 'bubble'
                    s_size = obj[SpacialComponent].rect.width + 12
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
                        s_size // 2 - 2,
                    )

                    render_surface.blit(
                        shield_surf, shield_surf.get_rect(center=render_rect.center)
                    )

            # 2. DRAW HEALTH BAR (New)
            # We check both HealthComponent (Enemies) and PlayerStatsComponent (Xavier)
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

                # --- 1. HEALTH BAR ---
                pygame.draw.rect(
                    render_surface, (80, 0, 0), (bx, by, bar_w, bar_h)
                )  # Background
                pygame.draw.rect(
                    render_surface, (0, 200, 0), (bx, by, bar_w * hp_perc, bar_h)
                )  # Foreground

                # --- 2. XP BAR (Player Only) ---
                if PlayerStatsComponent in obj:
                    stats = obj[PlayerStatsComponent]
                    xp_perc = max(0, min(1, stats.xp / stats.xp_to_next_level))

                    # Position it 6 pixels above the Health Bar
                    xp_by = by - bar_h

                    # Background (Dark Blue)
                    pygame.draw.rect(
                        render_surface, (20, 20, 0), (bx, xp_by, bar_w, bar_h)
                    )
                    # Foreground (Bright Cyan/XP Color)
                    pygame.draw.rect(
                        render_surface,
                        (255, 200, 0),
                        (bx, xp_by, bar_w * xp_perc, bar_h),
                    )
            # --- XP GEM TRAILS ---
            if TrailComponent in obj and ExperienceGemComponent in obj:
                trail = obj[TrailComponent]
                # 1. Record the current center position
                center_pos = obj[SpacialComponent].rect.center
                trail.history.append(center_pos)

                # 2. Keep the history at the max length
                if len(trail.history) > trail.length:
                    trail.history.pop(0)

                # 3. Draw the "Dart" Trail (Only if it's currently moving fast/vacuuming)
                # We check if history[0] is different from the current pos to ensure it's moving
                if len(trail.history) > 1 and trail.history[0] != center_pos:
                    # Draw from oldest (tail) to newest (head), getting thicker
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

                        # Draw a nice bright cyan/blue line for XP
                        pygame.draw.line(
                            render_surface, (0, 255, 255), cam_start, cam_end, thickness
                        )

            # Hit Flash
            if HealthComponent in obj and obj[HealthComponent].hit_timer > 0:
                # Use the hit-flash surface instead of the regular sprite
                hit_sprite = get_hit_surface(obj[RenderComponent].sprite)
                render_surface.blit(hit_sprite, render_rect)
                # Decrease timer
                obj[HealthComponent].hit_timer -= dt
            else:
                # Draw normal sprite
                # render_surface.blit(obj[RenderComponent].sprite, render_rect)
                pass

    return render_surface


def get_hit_surface(sprite):
    # 1. Create a mask from the sprite (handles transparency perfectly)
    mask = pygame.mask.from_surface(sprite)
    # 2. Convert that mask into a surface
    hit_surf = mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0))
    return hit_surf
