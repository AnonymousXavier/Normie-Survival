import pygame


from Core import States
from Globals import Settings, Misc, Enums
from ECS.Components import (EnemyTag, PowerUpComponent, PowerUpTag, SpacialComponent, RenderComponent, 
	PlayerInputTag, StalkerComponent, RotationComponent)


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
	}

	world[new_id] = enemy
	Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

	return new_id

def spawn_shotgun(world: dict, spatial_grid: dict, grid_x: int, grid_y: int):
	x, y = grid_x * Settings.SPRITE.WIDTH, grid_y * Settings.SPRITE.HEIGHT

	new_id = States.NEXT_ENTITY_ID
	States.NEXT_ENTITY_ID += 1

	# Create a temporary surface with a "barrel" drawn on it so we can see where it aims
	placeholder_surface = pygame.Surface(Settings.SPRITE.SIZE, pygame.SRCALPHA)
	placeholder_surface.fill((100, 100, 100)) # Gray gun body
	pygame.draw.rect(placeholder_surface, Settings.COLOURS.BLACK, (10, 6, 6, 4)) # Black barrel pointing right (0 degrees)

	shotgun = {
		SpacialComponent: SpacialComponent(
			grid_pos=(grid_x, grid_y),
			rect=pygame.Rect(x, y, Settings.SPRITE.WIDTH, Settings.SPRITE.HEIGHT)
		),
		RenderComponent: RenderComponent(
			color=Settings.DEBUG.PLAYER_COLOR, 
			sprite=placeholder_surface, 
			base_sprite=placeholder_surface
		),
		PowerUpComponent: PowerUpComponent(_id=Enums.POWERUPS.SHOTGUN),
		PowerUpTag: PowerUpTag(),
		RotationComponent: RotationComponent() 
	}

	world[new_id] = shotgun
	Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

	return new_id

