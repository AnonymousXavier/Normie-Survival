from random import randint
from math import sin, cos, radians

from Core import States
from ECS import Factories
from ECS.Components import EnemyTag, SpacialComponent
from Globals import Settings

def process(world: dict, spatial_grid: dict):
	global spawned_guards 

	spawned_enemies = 0
	for entity_id in world:
		if EnemyTag in world[entity_id]:
			spawned_enemies += 1

	px, py = world[States.PLAYER_ID][SpacialComponent].grid_pos
	angle = radians(randint(0, 359))
	r = Settings.GAME.MAX_DISTANCE_FROM_PLAYER

	ox, oy = cos(angle) * r, sin(angle) * r
	ex, ey = round(px + ox), round(py + oy)

	if spawned_enemies < Settings.GAME.ALLOWABLE_NUMBER_OF_ENEMIES_ON_SCREEN:
		Factories.spawn_enemy(world, spatial_grid, ex, ey)

	print(spawned_enemies)

