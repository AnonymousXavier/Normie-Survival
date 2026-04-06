import pygame
import math

from Core import States
from Globals import Settings, Misc, Cache, Enums
from ECS.Components import (
    ArsenalComponent,
    BossAIComponent,
    BossTag,
    CameraShakeComponent,
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
    TrailComponent,
    WeaponComponent,
    WeaponStats,
    StrongerEnemyTag,
)


def new_camera(cams_topleft: tuple, cams_size: tuple, target_id: int):
    return {
        SpacialComponent: SpacialComponent(rect=pygame.Rect(cams_topleft, cams_size)),
        StalkerComponent: StalkerComponent(target_id=target_id),
        CameraShakeComponent: CameraShakeComponent(intensity=0.0),
    }


def spawn_player(
    world: dict, spatial_grid: dict, grid_x: int, grid_y: int, primary_weapon: str
):
    x, y = grid_x * Settings.SPRITE.WIDTH, grid_y * Settings.SPRITE.HEIGHT

    new_id = States.NEXT_ENTITY_ID
    States.NEXT_ENTITY_ID += 1

    if primary_weapon == "sniper":
        starting_stats = WeaponStats(
            base_damage=15,
            base_fire_rate=2.5,
            projectile_count=1,
            spread_angle=0.0,
            speed=50.0,  # Fast bullet
            pierce=2,  # Starts with pierce!
        )
    else:  # Default to Shotgun
        starting_stats = WeaponStats(
            base_damage=1,
            base_fire_rate=1.0,
            projectile_count=3,
            spread_angle=15.0,
            speed=35.0,
            pierce=1,
        )

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
        ArsenalComponent: ArsenalComponent(
            inventory={primary_weapon: starting_stats}, primary_weapon=primary_weapon
        ),
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

    # --- LEVEL SCALING ---
    p_lvl = world[States.PLAYER_ID][PlayerStatsComponent].level
    hp_scale = p_lvl**Settings.GAME.PLAYER_LEVEL_TO_BOSS_HEALTH_EXPONENT
    final_hp = int(Settings.GAME.DEFAULT_ENEMY_HP * mult) * hp_scale

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
            hp=(final_hp),
            max_hp=final_hp,
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

    # --- LEVEL SCALING ---
    p_lvl = world[States.PLAYER_ID][PlayerStatsComponent].level
    hp_scale = p_lvl**Settings.GAME.PLAYER_LEVEL_TO_BOSS_HEALTH_EXPONENT
    final_hp = int(Settings.GAME.DEFAULT_ENEMY_HP * mult) * hp_scale

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
            hp=int(final_hp) * Settings.GAME.STRONGER_ENEMIES_MULTIPLIER,
            max_hp=int(final_hp) * Settings.GAME.STRONGER_ENEMIES_MULTIPLIER,
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

    boss_hp = int(
        (Settings.GAME.BOSS_STRENGTH_MULTIPLIER * mult)
        * (p_lvl**Settings.GAME.PLAYER_LEVEL_TO_BOSS_HEALTH_EXPONENT)
    )

    boss = {
        SpacialComponent: SpacialComponent(
            grid_pos=(spawn_x, spawn_y), rect=boss_rect  # Bigger sprite
        ),
        EnemyTag: EnemyTag(),
        BossTag: BossTag(),
        # Bosses need massive HP to resist your Shotgun build
        HealthComponent: HealthComponent(hp=boss_hp, max_hp=boss_hp),
        RenderComponent: RenderComponent(color=(255, 0, 0)),  # Red Menace
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
        TrailComponent: TrailComponent(length=6),
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
            rect=pygame.Rect((0, 0), (Cache.SPRITES.WEAPONS.SHOTGUN.get_size())),
        ),
        RenderComponent: RenderComponent(
            color=Settings.DEBUG.PLAYER_COLOR,
            sprite=Cache.SPRITES.WEAPONS.SHOTGUN,
            base_sprite=Cache.SPRITES.WEAPONS.SHOTGUN,
        ),
        # Pass the new dynamic variables here!
        OrbitalComponent: OrbitalComponent(
            target_id=target_id,
            radius=1.0,
            angle=start_angle,
            spin_speed=spin_speed,
            offset_angle=start_angle,
        ),
        CooldownComponent: CooldownComponent(
            fire_rate=1.0, time_since_last_shot=initial_cooldown_offset
        ),
        RotationComponent: RotationComponent(),
        PowerUpTag: PowerUpTag(),
        WeaponComponent: WeaponComponent(weapon_type="shotgun"),
    }

    world[new_id] = shotgun
    Misc.register_entity_in_grid(new_id, (0, 0), spatial_grid)

    return new_id


def spawn_sniper(
    world: dict,
    spatial_grid: dict,
    target_id: int,
    start_angle: float = 0.0,
    initial_cooldown_offset=0.0,
):
    new_id = States.NEXT_ENTITY_ID
    States.NEXT_ENTITY_ID += 1

    sniper = {
        SpacialComponent: SpacialComponent(
            grid_pos=(0, 0),
            rect=pygame.Rect((0, 0), (Cache.SPRITES.WEAPONS.SNIPER.get_size())),
        ),
        RenderComponent: RenderComponent(
            color=(255, 0, 0),
            sprite=Cache.SPRITES.WEAPONS.SNIPER,
            base_sprite=Cache.SPRITES.WEAPONS.SNIPER,
        ),
        OrbitalComponent: OrbitalComponent(
            target_id=target_id,
            radius=1.0,
            angle=start_angle,
            spin_speed=0.0,
            offset_angle=start_angle,
        ),
        CooldownComponent: CooldownComponent(
            fire_rate=2.0, time_since_last_shot=initial_cooldown_offset
        ),
        RotationComponent: RotationComponent(),
        WeaponComponent: WeaponComponent(weapon_type="sniper"),
        PowerUpTag: PowerUpTag(),
    }
    world[new_id] = sniper
    Misc.register_entity_in_grid(new_id, (0, 0), spatial_grid)


def refresh_weapon(world, spatial_grid, player_id, weapon_type, count):
    # 1. Delete all physical entities of THIS specific weapon type
    to_delete = [
        eid
        for eid, e in world.items()
        if PowerUpTag in e
        and WeaponComponent in e
        and e[WeaponComponent].weapon_type == weapon_type
    ]
    for eid in to_delete:
        Misc.remove_entity_from_grid(
            eid, world[eid][SpacialComponent].grid_pos, spatial_grid
        )
        del world[eid]

    # 2. Respawn with stagger
    player = world[player_id]
    w_stats = player[ArsenalComponent].inventory[weapon_type]
    stagger_interval = w_stats.base_fire_rate / count
    spacing = 360 / count

    for i in range(count):
        start_offset = i * stagger_interval
        if weapon_type == "shotgun":
            spawn_shotgun(
                world,
                spatial_grid,
                player_id,
                start_angle=i * spacing,
                initial_cooldown_offset=start_offset,
            )
        elif weapon_type == "sniper":
            spawn_sniper(
                world,
                spatial_grid,
                player_id,
                start_angle=(i * spacing) + 45,
                initial_cooldown_offset=start_offset,
            )


def spawn_bullet(
    world: dict,
    spatial_grid: dict,
    center_x: float,
    center_y: float,
    angle_deg: float,
    speed: float,
    damage: int,
    pierce: int = 1,
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
            pierce=pierce,
        ),
    }

    world[new_id] = bullet
    Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

    return new_id
