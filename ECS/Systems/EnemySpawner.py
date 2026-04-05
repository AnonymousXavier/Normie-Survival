from random import randint
from math import sin, cos, radians
from Core import States
from ECS import Factories
from ECS.Components import EnemyTag, SpacialComponent, BossTag
from Globals import Settings

spawn_timer = 0.0
SPAWN_DELAY = 0.2  # Only allow one spawn every 0.2 seconds


def process(world: dict, spatial_grid: dict, dt: float):
    global spawn_timer
    spawn_timer += dt

    spawned_enemies = sum(1 for e in world.values() if EnemyTag in e)
    current_cap = Settings.GAME.ALLOWABLE_NUMBER_OF_ENEMIES_ON_SCREEN + (
        int(States.GAME_TIME // 60) * Settings.GAME.TIME_ELAPSED_TO_ENEMIES_RATIO
    )

    # Only spawn if under cap AND timer is ready
    if spawned_enemies < current_cap and spawn_timer >= SPAWN_DELAY:
        spawn_enemy(world, spatial_grid)
        spawn_timer = 0.0  # Reset


def get_difficulty_mult():
    # Time factor: +0.1 every minute
    time_factor = States.GAME_TIME / 60.0 * 0.1
    # Kill factor: +0.05 every 50 kills
    kill_factor = (States.KILLS_COUNT // 50) * 0.05

    return 1.0 + time_factor + kill_factor


def spawn_enemy(world, spatial_grid):
    mult = get_difficulty_mult()

    px, py = world[States.PLAYER_ID][SpacialComponent].grid_pos
    angle = radians(randint(0, 359))
    r = Settings.GAME.MAX_DISTANCE_FROM_PLAYER

    ox, oy = cos(angle) * r, sin(angle) * r
    ex, ey = round(px + ox), round(py + oy)

    if not is_boss_alive(world):
        Factories.spawn_normal_enemy(world, spatial_grid, ex, ey, mult)
    else:
        Factories.spawn_stronger_enemy(world, spatial_grid, ex, ey, mult)


def is_boss_alive(world: dict) -> bool:
    # Efficiently check if any entity has the BossTag
    return any(BossTag in entity for entity in world.values())
