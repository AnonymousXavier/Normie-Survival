from ECS.Components import SpacialComponent, VelocityComponent
from Globals import Enums, Settings, Misc

frame = 0

def process(world: dict, spatial_grid: dict, global_event: list, delta: float):
    global frame

    if frame % (Settings.UPDATE.FPS / Settings.UPDATE.INPUT_CHECKS_PER_SEC) == 0:
        for event in global_event:
            if event["type"] == Enums.EVENT_TYPES.MOVEMENT_INTENT:
                obj_id = event["entity_id"] 
                if SpacialComponent in world[obj_id]:
                    obj = world[obj_id]

                    gx, gy = obj[SpacialComponent].grid_pos
                    dx, dy = event["dx"], event["dy"]
                    nx, ny = (gx + dx, gy + dy)

                    tx, ty = nx * Settings.SPRITE.WIDTH, ny * Settings.SPRITE.HEIGHT
                    world[obj_id][VelocityComponent] = VelocityComponent(target=(tx, ty), position=world[obj_id][SpacialComponent].rect.topleft, speed=Settings.GAME.PLAYER_SPEED)

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

            obj[VelocityComponent].position = Misc.move_towards((px, py), (tx, ty), speed * delta)
            obj[SpacialComponent].rect.topleft = obj[VelocityComponent].position  

    for obj_id in objects_done_with_interpolation:
        del world[obj_id][VelocityComponent]

    frame += 1

def move_entity_on_spatial_grid(entity_id: int, new_position: tuple, world:dict, spatial_grid: dict):
    obj = world[entity_id]
    old_pos = obj[SpacialComponent].grid_pos

    Misc.remove_entity_from_grid(entity_id, old_pos, spatial_grid)
    Misc.register_entity_in_grid(entity_id, new_position, spatial_grid)

    obj[SpacialComponent].grid_pos = new_position

