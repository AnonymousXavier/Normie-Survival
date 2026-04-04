import pygame
import math

from Core import States
from Globals import Settings, Misc, Cache, Enums
from ECS.Components import (ArsenalComponent, EnemyTag, FacingDirectionComponent, HealthComponent, HitboxComponent, PlayerStatsComponent, PowerUpTag, SpacialComponent, RenderComponent, 
	PlayerInputTag, StalkerComponent, RotationComponent, CooldownComponent, ProjectileComponent, OrbitalComponent,
	CollectorComponent, ExperienceGemComponent, AnimationComponent, WeaponStats)
from ECS.Components import UITag, UIButtonComponent

def new_camera(cams_topleft: tuple, cams_size: tuple, target_id: int):
	return {
		SpacialComponent: SpacialComponent(
			rect=pygame.Rect(cams_topleft, cams_size)),
		StalkerComponent: StalkerComponent(target_id=target_id)
	}

def spawn_player(world: dict, spatial_grid: dict, grid_x: int, grid_y: int):
	x, y = grid_x * Settings.SPRITE.WIDTH, grid_y * Settings.SPRITE.HEIGHT

	new_id = States.NEXT_ENTITY_ID
	States.NEXT_ENTITY_ID += 1

	player = {
		SpacialComponent: SpacialComponent(
			grid_pos= (grid_x, grid_y),
			rect=pygame.Rect(x, y, Settings.SPRITE.WIDTH, Settings.SPRITE.HEIGHT)
		),
		RenderComponent: RenderComponent(color=Settings.DEBUG.PLAYER_COLOR),
		PlayerInputTag: PlayerInputTag(),
		FacingDirectionComponent: FacingDirectionComponent(),
		CollectorComponent: CollectorComponent(),
		PlayerStatsComponent: PlayerStatsComponent(speed=Settings.GAME.PLAYER_SPEED, max_hp=Settings.GAME.DEFAULT_PLAYER_HP),
        HealthComponent: HealthComponent(hp=Settings.GAME.DEFAULT_PLAYER_HP, max_hp=Settings.GAME.DEFAULT_PLAYER_HP),
        ArsenalComponent: ArsenalComponent(
            inventory= {
                "shotgun": WeaponStats(
                    damage=1, 
                    fire_rate=1.0, 
                    projectile_count=3, 
                    spread_angle=15.0
                )
            }
        ),
        HitboxComponent: HitboxComponent(
            width=round(Settings.SPRITE.WIDTH * Settings.GAME.PLAYER_HITBOX_TO_SPRITE_RATIO), 
            height=round(Settings.SPRITE.HEIGHT * Settings.GAME.PLAYER_HITBOX_TO_SPRITE_RATIO)
        ),
        AnimationComponent: AnimationComponent(
            frames={
                Enums.ANIM_STATES.IDLE: Cache.SPRITES.PLAYER.IDLE,
                Enums.ANIM_STATES.WALK: Cache.SPRITES.PLAYER.WALK
            },
            state=Enums.ANIM_STATES.IDLE,
            direction=Enums.ANIM_DIRS.DOWN
        )
	}

	world[new_id] = player
	Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

	return new_id

def spawn_flowfield_arrow(debug: dict, debug_grid: dict, grid_x: int, grid_y: int, sprite: pygame.Surface):
	x, y = grid_x * Settings.SPRITE.WIDTH, grid_y * Settings.SPRITE.HEIGHT

	new_id = States.NEXT_DEBUG_ELEMENT_ID
	States.NEXT_DEBUG_ELEMENT_ID += 1

	arrow = {
		SpacialComponent: SpacialComponent(
			grid_pos= (grid_x, grid_y),
			rect=pygame.Rect(x, y, Settings.SPRITE.WIDTH, Settings.SPRITE.HEIGHT)
		),
		RenderComponent: RenderComponent(color=Settings.COLOURS.BLACK, sprite=sprite)
	}

	debug[new_id] = arrow
	Misc.register_entity_in_grid(new_id, (grid_x, grid_y), debug_grid)
	return new_id

def spawn_enemy(world: dict, spatial_grid: dict, grid_x: int, grid_y: int):
	x, y = grid_x * Settings.SPRITE.WIDTH, grid_y * Settings.SPRITE.HEIGHT

	new_id = States.NEXT_ENTITY_ID
	States.NEXT_ENTITY_ID += 1

	enemy = {
	    SpacialComponent: SpacialComponent(
	        grid_pos= (grid_x, grid_y),
	        rect=pygame.Rect(x, y, Settings.SPRITE.WIDTH, Settings.SPRITE.HEIGHT)
	    ),
        AnimationComponent: AnimationComponent(
            frames={
                Enums.ANIM_STATES.WALK: Cache.SPRITES.ENEMY.WALK
            },
            state=Enums.ANIM_STATES.WALK,
            direction=Enums.ANIM_DIRS.DOWN
        ),
        FacingDirectionComponent: FacingDirectionComponent(dx=0, dy=0),
	    RenderComponent: RenderComponent(color=Settings.DEBUG.ENEMY_COLOR),
	    EnemyTag: EnemyTag(),
	    HealthComponent: HealthComponent(hp=Settings.GAME.DEFAULT_ENEMY_HP, max_hp=Settings.GAME.DEFAULT_ENEMY_HP),
        HitboxComponent: HitboxComponent(
            width=round(Settings.SPRITE.WIDTH * Settings.GAME.ENEMY_HITBOX_TO_SPRITE_RATIO), 
            height=round(Settings.SPRITE.HEIGHT * Settings.GAME.ENEMY_HITBOX_TO_SPRITE_RATIO)
        )
	}

	world[new_id] = enemy
	Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

	return new_id

def spawn_gem(world: dict, spatial_grid: dict, x_float: float, y_float: float, value: int = 1):
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
            rect=pygame.Rect((round(x + w//2), round(y + 4)), (w, h))
        ),

        RenderComponent: RenderComponent(color=(0,0,0), sprite=Cache.SPRITES.ITEMS.GEM),
        ExperienceGemComponent: ExperienceGemComponent(value=value)
    }

    world[new_id] = gem
    # Always register using the integer grid_pos
    Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

def spawn_shotgun(world: dict, spatial_grid: dict, target_id: int, start_angle: float = 0.0, spin_speed: float = 0.0):
    new_id = States.NEXT_ENTITY_ID
    States.NEXT_ENTITY_ID += 1

    shotgun = {
        SpacialComponent: SpacialComponent(
            grid_pos=(0, 0),
            rect=pygame.Rect(0, 0, Settings.SPRITE.WIDTH, Settings.SPRITE.HEIGHT)
        ),
        RenderComponent: RenderComponent(
            color=Settings.DEBUG.PLAYER_COLOR, 
            sprite=Cache.SPRITES.WEAPONS.SHOTGUN, 
            base_sprite=Cache.SPRITES.WEAPONS.SHOTGUN 
        ),
        # Pass the new dynamic variables here!
        OrbitalComponent: OrbitalComponent(target_id=target_id, radius=1.0, angle=start_angle, spin_speed=spin_speed),
        CooldownComponent: CooldownComponent(fire_rate=1.0),
        RotationComponent: RotationComponent(),
        PowerUpTag: PowerUpTag()
    }

    world[new_id] = shotgun
    Misc.register_entity_in_grid(new_id, (0, 0), spatial_grid)

    return new_id

def spawn_bullet(world: dict, spatial_grid: dict, center_x: float, center_y: float, angle_deg: float, speed: float, damage: int):
    angle_rad = math.radians(-angle_deg) 
    
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
            grid_pos=(grid_x, grid_y),
            rect=pygame.Rect(spawn_x, spawn_y, 4, 4) 
        ),
        RenderComponent: RenderComponent(color=(255, 255, 0)), 
        ProjectileComponent: ProjectileComponent(dx=dx, dy=dy, speed=speed, damage=damage)
    }

    world[new_id] = bullet
    Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)
    
    return new_id

def spawn_upgrade_menu(world: dict):
    center_x = Settings.WINDOW.WIDTH // 2
    center_y = Settings.WINDOW.HEIGHT // 2
    
    upgrades = [
        {"text": "+1 Projectile", "action": {"buff": "projectile"}, "y_offset": -60},
        {"text": "+1 Damage", "action": {"buff": "damage"}, "y_offset": 0},
        {"text": "Faster Fire Rate", "action": {"buff": "fire_rate"}, "y_offset": 60}
    ]

    for upg in upgrades:
        new_id = States.NEXT_ENTITY_ID
        States.NEXT_ENTITY_ID += 1
        
        rect = pygame.Rect(0, 0, 250, 40)
        rect.center = (center_x, center_y + upg["y_offset"])

        world[new_id] = {
            UITag: UITag(),
            UIButtonComponent: UIButtonComponent(
                rect=rect, 
                text=upg["text"], 
                action=upg["action"]
            )
        }
