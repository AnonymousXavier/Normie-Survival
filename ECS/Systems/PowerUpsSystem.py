import pygame
from math import radians, sin, cos

from Core import States
from ECS import Factories
from ECS.Components import SpacialComponent
from Globals import Enums, Settings, Misc


powerups = {
	Enums.POWERUPS.SHOTGUN: {"ids": [], "radius": 2, "offset": -90} # Grid Distance
}

def process(world: dict, spatial_grid: dict):
	for power_type in powerups:
		for i, powerup_id in enumerate(powerups[power_type]["ids"]):
			update_powerup_positions(world, spatial_grid, power_type, powerup_id, i)

def update_powerup_positions(world: dict, spatial_grid: dict, power_type: int, powerup_id: int, i: int):
	player_rect: pygame.Rect = world[States.PLAYER_ID][SpacialComponent].rect
	sw, sh = Settings.SPRITE.SIZE
	angle_increment = 360 / len(powerups[power_type]["ids"])

	r = powerups[power_type]["radius"] * sw
	angle = angle_increment * i + powerups[power_type]["offset"]
	powerup_rect: pygame.Rect = world[powerup_id][SpacialComponent].rect

	old_pos = world[States.PLAYER_ID][SpacialComponent].grid_pos
	x, y = cos(radians(angle)) * r, sin(radians(angle)) * r

	powerup_rect.center = player_rect.centerx + x, player_rect.centery + y
	new_pos = powerup_rect.centerx // sw, powerup_rect.centery // sh

	Misc.remove_entity_from_grid(powerup_id, old_pos, spatial_grid)
	Misc.register_entity_in_grid(powerup_id, new_pos, spatial_grid)

def add_powerup(powerup_id: int, world: dict, spatial_grid: dict):
	match powerup_id:
		case Enums.POWERUPS.SHOTGUN:
			_id = Factories.spawn_shotgun(world, spatial_grid, 0, 0)
			powerups[Enums.POWERUPS.SHOTGUN]["ids"].append(_id)

