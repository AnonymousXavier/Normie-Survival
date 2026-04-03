import pygame
import math


from Core import States
from Globals import Settings, Misc, Enums
from ECS.Components import (EnemyTag, FacingDirectionComponent, HealthComponent, PlayerStatsComponent, PowerUpTag, SpacialComponent, RenderComponent, 
	PlayerInputTag, StalkerComponent, RotationComponent, CooldownComponent, ProjectileComponent, OrbitalComponent,
	CollectorComponent, ExperienceGemComponent)


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
		PlayerStatsComponent: PlayerStatsComponent()
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
	    RenderComponent: RenderComponent(color=Settings.DEBUG.ENEMY_COLOR),
	    EnemyTag: EnemyTag(),
	    HealthComponent: HealthComponent(hp=3) # Enemies now have 3 HP
	}

	world[new_id] = enemy
	Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

	return new_id

def spawn_gem(world: dict, spatial_grid: dict, grid_x: int, grid_y: int):
    x, y = grid_x * Settings.SPRITE.WIDTH, grid_y * Settings.SPRITE.HEIGHT
    new_id = States.NEXT_ENTITY_ID
    States.NEXT_ENTITY_ID += 1

    gem = {
        SpacialComponent: SpacialComponent(
            grid_pos=(grid_x, grid_y),
            rect=pygame.Rect(x + 4, y + 4, 8, 8) # Smaller than a full tile
        ),
        RenderComponent: RenderComponent(color=(0, 255, 255)), # Cyan gem
        ExperienceGemComponent: ExperienceGemComponent(value=1)
    }

    world[new_id] = gem
    Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)


	

def spawn_shotgun(world: dict, spatial_grid: dict, target_id: int, start_angle: float = 0.0, spin_speed: float = 0.0):
    new_id = States.NEXT_ENTITY_ID
    States.NEXT_ENTITY_ID += 1

    # Placeholder sprite logic (gray box with black barrel)
    placeholder_surface = pygame.Surface(Settings.SPRITE.SIZE, pygame.SRCALPHA)
    placeholder_surface.fill((100, 100, 100)) 
    pygame.draw.rect(placeholder_surface, Settings.COLOURS.BLACK, (10, 6, 6, 4)) 

    shotgun = {
        SpacialComponent: SpacialComponent(
            grid_pos=(0, 0),
            rect=pygame.Rect(0, 0, Settings.SPRITE.WIDTH, Settings.SPRITE.HEIGHT)
        ),
        RenderComponent: RenderComponent(
            color=Settings.DEBUG.PLAYER_COLOR, 
            sprite=placeholder_surface, 
            base_sprite=placeholder_surface 
        ),
        # Pass the new dynamic variables here!
        OrbitalComponent: OrbitalComponent(target_id=target_id, radius=2.0, angle=start_angle, spin_speed=spin_speed),
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
        # Inject the dynamic speed and damage here!
        ProjectileComponent: ProjectileComponent(dx=dx, dy=dy, speed=speed, damage=damage)
    }

    world[new_id] = bullet
    Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)
    
    return new_id
