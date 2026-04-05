import pygame
import math

from Core import States
from Globals import Settings, Misc, Cache, Enums
from ECS.Components import (
    ArsenalComponent,
    BossAIComponent,
    BossTag,
    DamageComponent,
    EnemyTag,
    FacingDirectionComponent,
    HealthComponent,
    HitboxComponent,
    PlayerStatsComponent,
    PowerUpTag,
    SpacialComponent,
    RenderComponent,
    PlayerInputTag,
    StalkerComponent,
    RotationComponent,
    CooldownComponent,
    ProjectileComponent,
    OrbitalComponent,
    CollectorComponent,
    ExperienceGemComponent,
    AnimationComponent,
    WeaponStats,
    StrongerEnemyTag,
)


def new_camera(cams_topleft: tuple, cams_size: tuple, target_id: int):
    return {
        SpacialComponent: SpacialComponent(rect=pygame.Rect(cams_topleft, cams_size)),
        StalkerComponent: StalkerComponent(target_id=target_id),
    }


def spawn_player(world: dict, spatial_grid: dict, grid_x: int, grid_y: int):
    x, y = grid_x * Settings.SPRITE.WIDTH, grid_y * Settings.SPRITE.HEIGHT

    new_id = States.NEXT_ENTITY_ID
    States.NEXT_ENTITY_ID += 1

    player = {
        SpacialComponent: SpacialComponent(
            grid_pos=(grid_x, grid_y),
            rect=pygame.Rect(x, y, Settings.SPRITE.WIDTH, Settings.SPRITE.HEIGHT),
        ),
        RenderComponent: RenderComponent(color=Settings.DEBUG.PLAYER_COLOR),
        PlayerInputTag: PlayerInputTag(),
        FacingDirectionComponent: FacingDirectionComponent(),
        CollectorComponent: CollectorComponent(),
        PlayerStatsComponent: PlayerStatsComponent(),
        HealthComponent: HealthComponent(
            hp=Settings.GAME.DEFAULT_PLAYER_HP, max_hp=Settings.GAME.DEFAULT_PLAYER_HP
        ),
        ArsenalComponent: ArsenalComponent(inventory={"shotgun": WeaponStats()}),
        HitboxComponent: HitboxComponent(
            width=round(
                Settings.SPRITE.WIDTH * Settings.GAME.PLAYER_HITBOX_TO_SPRITE_RATIO
            ),
            height=round(
                Settings.SPRITE.HEIGHT * Settings.GAME.PLAYER_HITBOX_TO_SPRITE_RATIO
            ),
        ),
        AnimationComponent: AnimationComponent(
            frames={
                Enums.ANIM_STATES.IDLE: Cache.SPRITES.PLAYER.IDLE,
                Enums.ANIM_STATES.WALK: Cache.SPRITES.PLAYER.WALK,
            },
            state=Enums.ANIM_STATES.IDLE,
            direction=Enums.ANIM_DIRS.DOWN,
        ),
    }

    world[new_id] = player
    Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

    return new_id


def spawn_flowfield_arrow(
    debug: dict, debug_grid: dict, grid_x: int, grid_y: int, sprite: pygame.Surface
):
    x, y = grid_x * Settings.SPRITE.WIDTH, grid_y * Settings.SPRITE.HEIGHT

    new_id = States.NEXT_DEBUG_ELEMENT_ID
    States.NEXT_DEBUG_ELEMENT_ID += 1

    arrow = {
        SpacialComponent: SpacialComponent(
            grid_pos=(grid_x, grid_y),
            rect=pygame.Rect(x, y, Settings.SPRITE.WIDTH, Settings.SPRITE.HEIGHT),
        ),
        RenderComponent: RenderComponent(color=Settings.COLOURS.BLACK, sprite=sprite),
    }

    debug[new_id] = arrow
    Misc.register_entity_in_grid(new_id, (grid_x, grid_y), debug_grid)
    return new_id


def spawn_normal_enemy(
    world: dict, spatial_grid: dict, grid_x: int, grid_y: int, mult: float
):
    x, y = grid_x * Settings.SPRITE.WIDTH, grid_y * Settings.SPRITE.HEIGHT

    new_id = States.NEXT_ENTITY_ID
    States.NEXT_ENTITY_ID += 1

    enemy = {
        SpacialComponent: SpacialComponent(
            grid_pos=(grid_x, grid_y),
            rect=pygame.Rect(x, y, Settings.SPRITE.WIDTH, Settings.SPRITE.HEIGHT),
        ),
        AnimationComponent: AnimationComponent(
            frames={Enums.ANIM_STATES.WALK: Cache.SPRITES.ENEMY.NORMAL_WALK},
            state=Enums.ANIM_STATES.WALK,
            direction=Enums.ANIM_DIRS.DOWN,
        ),
        FacingDirectionComponent: FacingDirectionComponent(dx=0, dy=0),
        RenderComponent: RenderComponent(color=Settings.DEBUG.ENEMY_COLOR),
        EnemyTag: EnemyTag(),
        HealthComponent: HealthComponent(
            hp=int(Settings.GAME.DEFAULT_ENEMY_HP * mult),
            max_hp=int(Settings.GAME.DEFAULT_ENEMY_HP * mult),
        ),
        HitboxComponent: HitboxComponent(
            width=round(
                Settings.SPRITE.WIDTH * Settings.GAME.ENEMY_HITBOX_TO_SPRITE_RATIO
            ),
            height=round(
                Settings.SPRITE.HEIGHT * Settings.GAME.ENEMY_HITBOX_TO_SPRITE_RATIO
            ),
        ),
        DamageComponent: DamageComponent(amount=int(1 * mult)),
    }

    world[new_id] = enemy
    Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

    return new_id


def spawn_stronger_enemy(
    world: dict, spatial_grid: dict, grid_x: int, grid_y: int, mult: float
):
    x, y = grid_x * Settings.SPRITE.WIDTH, grid_y * Settings.SPRITE.HEIGHT

    new_id = States.NEXT_ENTITY_ID
    States.NEXT_ENTITY_ID += 1

    enemy = {
        SpacialComponent: SpacialComponent(
            grid_pos=(grid_x, grid_y),
            rect=pygame.Rect(x, y, Settings.SPRITE.WIDTH, Settings.SPRITE.HEIGHT),
        ),
        AnimationComponent: AnimationComponent(
            frames={Enums.ANIM_STATES.WALK: Cache.SPRITES.ENEMY.RED_WALK},
            state=Enums.ANIM_STATES.WALK,
            direction=Enums.ANIM_DIRS.DOWN,
        ),
        FacingDirectionComponent: FacingDirectionComponent(dx=0, dy=0),
        RenderComponent: RenderComponent(color=Settings.DEBUG.ENEMY_COLOR),
        EnemyTag: EnemyTag(),
        StrongerEnemyTag: StrongerEnemyTag(),
        HealthComponent: HealthComponent(
            hp=int(Settings.GAME.DEFAULT_ENEMY_HP * mult) * 5,
            max_hp=int(Settings.GAME.DEFAULT_ENEMY_HP * mult) * 5,
        ),
        HitboxComponent: HitboxComponent(
            width=round(
                Settings.SPRITE.WIDTH * Settings.GAME.ENEMY_HITBOX_TO_SPRITE_RATIO
            ),
            height=round(
                Settings.SPRITE.HEIGHT * Settings.GAME.ENEMY_HITBOX_TO_SPRITE_RATIO
            ),
        ),
        DamageComponent: DamageComponent(amount=int(1 * mult)),
    }

    world[new_id] = enemy
    Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

    return new_id


def spawn_boss(world, spatial_grid, mult: float):
    new_id = States.NEXT_ENTITY_ID
    States.NEXT_ENTITY_ID += 1
    p_lvl = world[States.PLAYER_ID][PlayerStatsComponent].level

    # Spawn 10 cells away from player
    player_pos = world[States.PLAYER_ID][SpacialComponent].grid_pos
    spawn_x = player_pos[0] + 10
    spawn_y = player_pos[1]

    grid_x, grid_y = player_pos[0] + 15, player_pos[1]

    # Calculate the center of the 16x16 tile
    tile_center_x = (grid_x * Settings.SPRITE.WIDTH) + (Settings.SPRITE.WIDTH // 2)
    tile_center_y = (grid_y * Settings.SPRITE.HEIGHT) + (Settings.SPRITE.HEIGHT // 2)

    boss_w, boss_h = 50, 50
    # Set the rect so its center matches the tile center
    boss_rect = pygame.Rect(0, 0, boss_w, boss_h)
    boss_rect.center = (tile_center_x, tile_center_y)

    boss_hp = int((100 * mult) * (p_lvl**1.2))

    boss = {
        SpacialComponent: SpacialComponent(
            grid_pos=(spawn_x, spawn_y), rect=boss_rect  # Bigger sprite
        ),
        EnemyTag: EnemyTag(),
        BossTag: BossTag(),
        # Bosses need massive HP to resist your Shotgun build
        HealthComponent: HealthComponent(hp=boss_hp, max_hp=boss_hp),
        RenderComponent: RenderComponent(color=(255, 0, 0)),  # Red Menace
        # ... (Add Movement/AI)
        AnimationComponent: AnimationComponent(
            frames={Enums.ANIM_STATES.WALK: Cache.SPRITES.ENEMY.BOSS},
            state=Enums.ANIM_STATES.WALK,
            direction=Enums.ANIM_DIRS.DOWN,
        ),
        FacingDirectionComponent: FacingDirectionComponent(dx=0, dy=0),
        HitboxComponent: HitboxComponent(
            width=round(50 * Settings.GAME.ENEMY_HITBOX_TO_SPRITE_RATIO),
            height=round(50 * Settings.GAME.ENEMY_HITBOX_TO_SPRITE_RATIO),
        ),
        DamageComponent: DamageComponent(amount=int(1 * mult)),
        BossAIComponent: BossAIComponent(),
    }

    world[new_id] = boss
    Misc.register_entity_in_grid(new_id, (spawn_x, spawn_y), spatial_grid)
    print("🚨 BOSS SPAWNED! 🚨")


def spawn_gem(
    world: dict, spatial_grid: dict, x_float: float, y_float: float, value: int = 1
):
    # Calculate precise pixel position
    x = x_float * Settings.SPRITE.WIDTH
    y = y_float * Settings.SPRITE.HEIGHT

    w, h = Settings.GAME.XP_GEM_SIZE
    # Derive the integer grid coordinates for the spatial_grid key
    grid_x = int(x_float)
    grid_y = int(y_float)

    new_id = States.NEXT_ENTITY_ID
    States.NEXT_ENTITY_ID += 1

    gem = {
        SpacialComponent: SpacialComponent(
            grid_pos=(grid_x, grid_y),
            # Use round() here to ensure the Rect is valid for Pygame
            rect=pygame.Rect((round(x + w // 2), round(y + 4)), (w, h)),
        ),
        RenderComponent: RenderComponent(
            color=(0, 0, 0), sprite=Cache.SPRITES.ITEMS.GEM
        ),
        ExperienceGemComponent: ExperienceGemComponent(value=value),
    }

    world[new_id] = gem
    # Always register using the integer grid_pos
    Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)


def spawn_shotgun(
    world: dict,
    spatial_grid: dict,
    target_id: int,
    start_angle: float = 0.0,
    spin_speed: float = 0.0,
    initial_cooldown_offset=0.0,
):
    new_id = States.NEXT_ENTITY_ID
    States.NEXT_ENTITY_ID += 1

    shotgun = {
        SpacialComponent: SpacialComponent(
            grid_pos=(0, 0),
            rect=pygame.Rect(0, 0, Settings.SPRITE.WIDTH, Settings.SPRITE.HEIGHT),
        ),
        RenderComponent: RenderComponent(
            color=Settings.DEBUG.PLAYER_COLOR,
            sprite=Cache.SPRITES.WEAPONS.SHOTGUN,
            base_sprite=Cache.SPRITES.WEAPONS.SHOTGUN,
        ),
        # Pass the new dynamic variables here!
        OrbitalComponent: OrbitalComponent(
            target_id=target_id, radius=1.0, angle=start_angle, spin_speed=spin_speed
        ),
        CooldownComponent: CooldownComponent(
            fire_rate=1.0, time_since_last_shot=initial_cooldown_offset
        ),
        RotationComponent: RotationComponent(),
        PowerUpTag: PowerUpTag(),
    }

    world[new_id] = shotgun
    Misc.register_entity_in_grid(new_id, (0, 0), spatial_grid)

    return new_id


def spawn_bullet(
    world: dict,
    spatial_grid: dict,
    center_x: float,
    center_y: float,
    angle_deg: float,
    speed: float,
    damage: int,
):
    angle_rad = math.radians(-angle_deg)

    grid_speed = speed * Settings.CELLS.WIDTH
    dx = math.cos(angle_rad)
    dy = math.sin(angle_rad)

    barrel_length = Settings.SPRITE.WIDTH // 2
    spawn_x = center_x + (dx * barrel_length)
    spawn_y = center_y + (dy * barrel_length)

    grid_x = int(spawn_x // Settings.SPRITE.WIDTH)
    grid_y = int(spawn_y // Settings.SPRITE.HEIGHT)

    new_id = States.NEXT_ENTITY_ID
    States.NEXT_ENTITY_ID += 1

    bullet = {
        SpacialComponent: SpacialComponent(
            grid_pos=(grid_x, grid_y), rect=pygame.Rect(spawn_x, spawn_y, 4, 4)
        ),
        RenderComponent: RenderComponent(color=(255, 255, 0)),
        ProjectileComponent: ProjectileComponent(
            dx=dx,
            dy=dy,
            speed=grid_speed,
            damage=damage,
            exact_x=float(spawn_x),
            exact_y=float(spawn_y),
        ),
    }

    world[new_id] = bullet
    Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

    return new_id


# ECS/Factories.py


def refresh_player_shotguns(world, spatial_grid, player_id, count):
    # 1. Find and delete current shotguns
    to_delete = [eid for eid, e in world.items() if PowerUpTag in e]
    for eid in to_delete:
        # (existing cleanup logic...)
        pass

    # 2. Calculate Stagger Timing
    # Get the fire rate from the Arsenal component to know the total cycle time
    player = world[player_id]
    sg_stats = player[ArsenalComponent].inventory["shotgun"]
    fire_rate = sg_stats.base_fire_rate

    # The delay between each gun firing
    stagger_interval = fire_rate / count

    # 3. Respawn with orbital spacing AND timing offsets
    spacing = 360 / count
    for i in range(count):
        # Gun i gets a head start on its cooldown
        # Gun 0 starts at 0.0, Gun 1 starts at stagger_interval, etc.
        start_offset = i * stagger_interval

        spawn_shotgun(
            world,
            spatial_grid,
            player_id,
            start_angle=i * spacing,
            initial_cooldown_offset=start_offset,
        )
