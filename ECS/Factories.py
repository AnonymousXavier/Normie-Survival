import pygame


from Core import States
from Globals import Settings, Misc, Enums
from ECS.Components import (EnemyTag, PowerUpComponent, PowerUpTag, SpacialComponent, RenderComponent, 
	PlayerInputTag, StalkerComponent)


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

	shotgun = {
		SpacialComponent: SpacialComponent(
			grid_pos= (grid_x, grid_y),
			rect=pygame.Rect(x, y, Settings.SPRITE.WIDTH, Settings.SPRITE.HEIGHT)
		),
		RenderComponent: RenderComponent(color=Settings.DEBUG.PLAYER_COLOR),
		PowerUpComponent: PowerUpComponent(_id=Enums.POWERUPS.SHOTGUN),
		PowerUpTag: PowerUpTag()
	}

	world[new_id] = shotgun
	Misc.register_entity_in_grid(new_id, (grid_x, grid_y), spatial_grid)

	return new_id

