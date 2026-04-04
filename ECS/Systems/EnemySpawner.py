from random import randint
from math import sin, cos, radians
from Core import States
from ECS import Factories
from ECS.Components import EnemyTag, SpacialComponent
from Globals import Settings

def process(world: dict, spatial_grid: dict):
    # Count existing enemies
    spawned_enemies = sum(1 for e in world.values() if EnemyTag in e)

    # Every 60 seconds, increase the allowed cap by n
    current_cap = Settings.GAME.ALLOWABLE_NUMBER_OF_ENEMIES_ON_SCREEN + (int(States.GAME_TIME // 60) * Settings.GAME.TIME_ELAPSED_TO_ENEMIES_RATIO)
    
    # Increase spawn frequency (one check per frame can be too fast, maybe logic here)
    if spawned_enemies < current_cap:
        spawn_at_edge(world, spatial_grid)

def spawn_at_edge(world: dict, spatial_grid: dict):
    px, py = world[States.PLAYER_ID][SpacialComponent].grid_pos
    angle = radians(randint(0, 359))
    r = Settings.GAME.MAX_DISTANCE_FROM_PLAYER

    ox, oy = cos(angle) * r, sin(angle) * r
    ex, ey = round(px + ox), round(py + oy)

    Factories.spawn_enemy(world, spatial_grid, ex, ey)