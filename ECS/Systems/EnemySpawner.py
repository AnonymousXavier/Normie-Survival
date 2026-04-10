from random import randint
from math import sin, cos, radians
from Core import States
from ECS import Factories
from ECS.Components import EnemyTag, SpacialComponent, BossTag, MegaGemTag
from Globals import Settings

spawn_timer = 0.0


def process(world: dict, spatial_grid: dict, dt: float):
    global spawn_timer

    if is_mega_gem_spawned(world):
        return

    spawn_timer += dt

    spawned_enemies = sum(1 for e in world.values() if EnemyTag in e)
    current_cap = (
        States.GAME_TIME / Settings.GAME.EXACT_SECS_MAX_ENEMIES_ARE_ALLOWED_TO_SPAWN
    ) * Settings.GAME.MAX_ENEMIES_SPAWNABLE

    current_cap = min(current_cap, Settings.GAME.MAX_ENEMIES_SPAWNABLE)
    print(current_cap, spawned_enemies)

    # Only spawn if under cap AND timer is ready
    if spawned_enemies < current_cap:
        spawn_enemy(world, spatial_grid)
        spawn_timer = 0.0  # Reset


def get_difficulty_mult():
    minutes = States.GAME_TIME / 60.0

    time_factor = (minutes**1.25) * 0.1

    return 1.0 + time_factor


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


def is_mega_gem_spawned(world: dict) -> bool:
    return any(MegaGemTag in entity for entity in world.values())
