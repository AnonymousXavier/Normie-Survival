import pygame
from Globals import Misc, Settings
from ECS.Systems import CameraSystem
from ECS.Components import SpacialComponent, RenderComponent, HitboxComponent


def process(
    surface: pygame.Surface,
    debug: dict,
    debug_grid: dict,
    camera: dict,
    real_world: dict = None,
):
    cam_boundary = CameraSystem.get_boundary_of(camera)
    rendering_data = Misc.get_camera_rendering_data(cam_boundary)
    camera_rect = camera[SpacialComponent].rect

    master_debug_surf = pygame.Surface(cam_boundary["world_size"], pygame.SRCALPHA)

    # Draw Hitboxes onto the master surface
    if real_world:
        for obj in real_world.values():
            if HitboxComponent in obj and SpacialComponent in obj:
                h_rect = obj[HitboxComponent].rect

                # Relative to camera
                render_pos = (
                    h_rect.left - camera_rect.left,
                    h_rect.top - camera_rect.top,
                )
                render_rect = pygame.Rect(render_pos, h_rect.size)

                pygame.draw.rect(
                    master_debug_surf, Settings.DEBUG.HITBOX_COLOR, render_rect, 2
                )

    draw_debug_elements(master_debug_surf, debug, debug_grid, camera, cam_boundary)

    transformed_debug = pygame.transform.scale(
        master_debug_surf, rendering_data["size"]
    )
    surface.blit(transformed_debug, rendering_data["offset"])


def draw_debug_elements(
    render_surface: pygame.Surface,
    debug: dict,
    debug_grid: dict,
    camera: dict,
    cam_boundary: dict,
):
    cam_left, cam_top = cam_boundary["left"], cam_boundary["top"]
    cam_right, cam_bottom = cam_boundary["right"], cam_boundary["bottom"]
    camera_rect: pygame.Rect = camera[SpacialComponent].rect

    for iy in range(cam_top, cam_bottom + 1):
        for ix in range(cam_left, cam_right + 1):
            if (ix, iy) in debug_grid:
                for obj_id in debug_grid[(ix, iy)]:
                    obj = debug[obj_id]
                    obj_rect = obj[SpacialComponent].rect
                    render_pos = (
                        obj_rect.left - camera_rect.left,
                        obj_rect.top - camera_rect.top,
                    )
                    render_rect = pygame.Rect(render_pos, obj_rect.size)

                    if obj[RenderComponent].sprite:
                        render_surface.blit(obj[RenderComponent].sprite, render_rect)
                    else:
                        pygame.draw.rect(
                            render_surface, obj[RenderComponent].color, render_rect
                        )
