from ECS.Components import (
    PlayerStatsComponent,
    SpacialComponent,
    RenderComponent,
    HealthComponent,
)
from ECS.Systems import CameraSystem

import pygame

from Globals import Misc
from Globals import Settings
from Globals.Settings import SPRITE


def process(surface: pygame.Surface, world: dict, camera: dict, visible_entities: list):
    camera_rect: pygame.Rect = camera[SpacialComponent].rect
    cam_boundary = CameraSystem.get_boundary_of(camera)

    rendering_data = Misc.get_camera_rendering_data(cam_boundary)

    game_entities_rendered_surface = draw_game_entities(
        world, cam_boundary, camera_rect, visible_entities
    )
    entities_transformed_surface = pygame.transform.scale(
        game_entities_rendered_surface, rendering_data["size"]
    )

    surface.blit(entities_transformed_surface, rendering_data["offset"])


def draw_game_entities(
    world: dict, cam_boundary: dict, camera_rect, visible_entities: list
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

            # 1. DRAW ENTITY SPRITE/RECT
            if obj[RenderComponent].sprite:
                render_surface.blit(obj[RenderComponent].sprite, render_rect)
            else:
                pygame.draw.rect(
                    render_surface, obj[RenderComponent].color, render_rect
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

    return render_surface
