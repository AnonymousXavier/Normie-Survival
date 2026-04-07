from ECS.Components import ProjectileComponent, SpacialComponent
from ECS.Systems import CameraSystem
from Globals import Misc, Settings


def process(world: dict, spatial_grid: dict, camera: dict, delta: float):
    cam_boundary = CameraSystem.get_boundary_of(camera)

    allowable_distance = 2
    left_bound = cam_boundary["left"] - allowable_distance
    right_bound = cam_boundary["right"] + allowable_distance
    top_bound = cam_boundary["top"] - allowable_distance
    bottom_bound = cam_boundary["bottom"] + allowable_distance

    bullets_to_delete = []

    for obj_id in world:
        if ProjectileComponent in world[obj_id] and SpacialComponent in world[obj_id]:
            obj = world[obj_id]

            # Move the bullet
            proj = obj[ProjectileComponent]
            space = obj[SpacialComponent]

            # Add the movement to the TRUE float trackers
            proj.exact_x += proj.dx * proj.speed * delta
            proj.exact_y += proj.dy * proj.speed * delta

            # Snap the Pygame integer rect to the exact floats
            space.rect.centerx = round(proj.exact_x)
            space.rect.centery = round(proj.exact_y)

            # Update Grid
            old_pos = obj[SpacialComponent].grid_pos
            new_pos = (
                obj[SpacialComponent].rect.x // Settings.SPRITE.WIDTH,
                obj[SpacialComponent].rect.y // Settings.SPRITE.HEIGHT,
            )

            if old_pos != new_pos:
                Misc.remove_entity_from_grid(obj_id, old_pos, spatial_grid)
                Misc.register_entity_in_grid(obj_id, new_pos, spatial_grid)
                obj[SpacialComponent].grid_pos = new_pos

            if not (
                left_bound <= new_pos[0] <= right_bound
                and top_bound <= new_pos[1] <= bottom_bound
            ):
                bullets_to_delete.append(obj_id)

    # delete off-screen bullets
    for obj_id in bullets_to_delete:
        grid_pos = world[obj_id][SpacialComponent].grid_pos
        Misc.remove_entity_from_grid(obj_id, grid_pos, spatial_grid)
        del world[obj_id]
