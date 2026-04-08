import random
from pygame import Rect
from ECS.Components import SpacialComponent, StalkerComponent, CameraShakeComponent
from Globals import Settings


def process(world: dict, camera: dict, delta: float):
    cam_rect: Rect = camera[SpacialComponent].rect

    targets_id = camera[StalkerComponent].target_id
    targets_rect = world[targets_id][SpacialComponent].rect

    # Start with the smooth tracking position
    base_x = targets_rect.centerx
    base_y = targets_rect.centery

    # CAMERA SHAKE
    if Settings.GAME_OPTIONS.SCREEN_SHAKE:
        if CameraShakeComponent in camera:
            shake = camera[CameraShakeComponent]
            if shake.intensity > 0:
                # Generate a violent, random integer offset
                offset_x = random.randint(-int(shake.intensity), int(shake.intensity))
                offset_y = random.randint(-int(shake.intensity), int(shake.intensity))

                base_x += offset_x
                base_y += offset_y

                # Lose 150 intensity per second
                shake.intensity -= 150.0 * delta
                if shake.intensity < 0:
                    shake.intensity = 0.0

    # Apply final position
    cam_rect.center = (base_x, base_y)


def get_boundary_of(camera: dict):
    cam_rect: Rect = camera[SpacialComponent].rect
    sprite_width, sprite_height = Settings.SPRITE.SIZE

    gtop = cam_rect.top // sprite_height
    gleft = cam_rect.left // sprite_width
    gbottom = cam_rect.bottom // sprite_height
    gright = cam_rect.right // sprite_width

    return {
        "top": round(gtop),
        "bottom": round(gbottom),
        "left": round(gleft),
        "right": round(gright),
        "world_size": (
            round(cam_rect.right - cam_rect.left),
            round(cam_rect.bottom - cam_rect.top),
        ),
    }
