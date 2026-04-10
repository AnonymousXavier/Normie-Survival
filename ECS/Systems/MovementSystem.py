from Core import States
from ECS.Components import (
    EnemyTag,
    PlayerInputTag,
    SpacialComponent,
    VelocityComponent,
    FacingDirectionComponent,
    DashComponent,
)
from Globals.ParticleManager import ParticleManager
from Globals import Enums, Settings, Misc

frame = 0


def process(world: dict, spatial_grid: dict, global_event: list, delta: float):
    global frame

    # --- DASH TIMERS & GHOST TRAIL ---
    if States.PLAYER_ID in world and DashComponent in world[States.PLAYER_ID]:
        dash = world[States.PLAYER_ID][DashComponent]
        player_rect = world[States.PLAYER_ID][SpacialComponent].rect

        # 1. Tick down the cooldown
        if dash.cooldown_timer > 0:
            dash.cooldown_timer -= delta
            if dash.cooldown_timer <= 0:
                dash.flash_timer = 0.15

        # 2. Tick down the flash
        if dash.flash_timer > 0:
            dash.flash_timer -= delta

        # 3. Tick down the active dash window & Drop Ghosts!
        if dash.is_dashing:
            dash.timer -= delta

            # Record the current exact pixel coordinate and set Alpha to 255 (Solid)
            dash.ghosts.append([player_rect.x, player_rect.y, 255.0])

            if dash.timer <= 0:
                dash.is_dashing = False

        # 4. Fade out the ghost trail smoothly (Runs constantly so ghosts fade after dash ends)
        for ghost in dash.ghosts[:]:
            ghost[2] -= 800 * delta  # Subtract alpha based on frame time
            if ghost[2] <= 0:
                dash.ghosts.remove(ghost)

    if frame % (Settings.UPDATE.FPS / Settings.UPDATE.INPUT_CHECKS_PER_SEC) == 0:
        for event in global_event:
            if event["type"] == Enums.EVENT_TYPES.MOVEMENT_INTENT:
                obj_id = event["entity_id"]
                if SpacialComponent in world[obj_id]:
                    if VelocityComponent in world[obj_id]:
                        continue
                    obj = world[obj_id]

                    gx, gy = obj[SpacialComponent].grid_pos
                    dx, dy = event["dx"], event["dy"]
                    nx, ny = (gx + dx, gy + dy)

                    tx, ty = nx * Settings.SPRITE.WIDTH, ny * Settings.SPRITE.HEIGHT

                    speed = get_movement_speed(obj)

                    world[obj_id][VelocityComponent] = VelocityComponent(
                        target=(tx, ty),
                        position=world[obj_id][SpacialComponent].rect.topleft,
                        speed=speed,
                    )

                    if dx != 0 or dy != 0:
                        if FacingDirectionComponent in obj:
                            obj[FacingDirectionComponent].dx = dx
                            obj[FacingDirectionComponent].dy = dy

                    move_entity_on_spatial_grid(obj_id, (nx, ny), world, spatial_grid)

    # Interpolate Movements
    objects_done_with_interpolation = []
    for obj_id in world:
        obj = world[obj_id]
        if VelocityComponent in obj and SpacialComponent in obj:
            px, py = obj[VelocityComponent].position
            tx, ty = obj[VelocityComponent].target
            speed = obj[VelocityComponent].speed

            dx, dy = tx - px, ty - py

            if dx == 0 and dy == 0:
                obj[SpacialComponent].rect.topleft = tx, ty
                objects_done_with_interpolation.append(obj_id)

                continue

            obj[VelocityComponent].position = Misc.move_towards(
                (px, py), (tx, ty), speed * delta
            )
            obj[SpacialComponent].rect.topleft = obj[VelocityComponent].position

    for obj_id in objects_done_with_interpolation:
        del world[obj_id][VelocityComponent]

    frame += 1


def move_entity_on_spatial_grid(
    entity_id: int, new_position: tuple, world: dict, spatial_grid: dict
):
    obj = world[entity_id]
    old_pos = obj[SpacialComponent].grid_pos

    Misc.remove_entity_from_grid(entity_id, old_pos, spatial_grid)
    Misc.register_entity_in_grid(entity_id, new_position, spatial_grid)

    obj[SpacialComponent].grid_pos = new_position


def get_movement_speed(obj: dict):
    speed = 0
    dash_mult = 1.0

    # Check if the entity is currently dashing
    if DashComponent in obj and obj[DashComponent].is_dashing:
        dash_mult = obj[DashComponent].multiplier

    if PlayerInputTag in obj:
        speed = Settings.GAME.PLAYER_SPEED * dash_mult
    elif EnemyTag in obj:
        speed = Settings.GAME.ENEMY_SPEED

    return speed * Settings.CELLS.WIDTH
