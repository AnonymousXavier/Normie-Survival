from Core import States
from ECS.Components import SpacialComponent


def process(world: dict, spatial_grid: dict):
    if States.PLAYER_ID not in world:
        return

    player_obj = world[States.PLAYER_ID]
    p_pos = player_obj[SpacialComponent].grid_pos

    if p_pos in spatial_grid:
        for entity_id in list(spatial_grid[p_pos]):
            target_entity = world.get(entity_id)
            pass
