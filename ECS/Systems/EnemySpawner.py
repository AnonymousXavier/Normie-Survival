from random import randint

from Core import States
from ECS import Factories
from ECS.Components import SpacialComponent
from Globals import Settings

spawned_guards = 0

def process(world: dict, spatial_grid: dict):
	global spawned_guards 

	px, py = world[States.PLAYER_ID][SpacialComponent].grid_pos
	ox, oy = randint(-1 * Settings.GAME.MAX_DISTANCE_FROM_PLAYER, Settings.GAME.MAX_DISTANCE_FROM_PLAYER + 1), randint(-1 * Settings.GAME.MAX_DISTANCE_FROM_PLAYER, Settings.GAME.MAX_DISTANCE_FROM_PLAYER + 1)
	ex, ey = px + ox, py + oy

	if spawned_guards < Settings.GAME.ALLOWABLE_NUMBER_OF_ENEMIES:
		Factories.spawn_enemy(world, spatial_grid, ex, ey)

		spawned_guards += 1