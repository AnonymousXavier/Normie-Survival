import pygame

from Core import States
from ECS import Factories
from ECS.Components import SpacialComponent
from ECS.Systems import DebugRenderingSystem, FlowFieldSystem, InputSystem, RenderingSystem, DebugSystem, MovementSystem
from Globals import Settings

class Main:
	def __init__(self) -> None:
		player_id = Factories.spawn_player(States.world, States.spatial_grid, 0, 0)
		States.camera = Factories.new_camera((0, 0), Settings.CAMERA.SIZE, player_id)


	def draw(self):
		# FlowFieldSystem.draw(self.window)
		Settings.window.fill(Settings.COLOURS.BLACK)
		RenderingSystem.process(
			surface=Settings.window, 
			world=States.world, 
			spatial_grid=States.spatial_grid, 
			camera=States.camera, 
		)

	def handle_debug(self):
		debug = {}
		debug_spatial_grid = {}

		DebugSystem.process(debug, debug_spatial_grid)
		DebugRenderingSystem.process(
			surface=Settings.window,
			debug=debug,
			debug_grid=debug_spatial_grid,
			camera=States.camera
		)

	def update(self):
		events = []

		dt = Settings.WINDOW.CLOCK.tick(Settings.UPDATE.FPS) / 1000

		InputSystem.process(States.world, events)
		MovementSystem.process(States.world, States.spatial_grid, events, dt)
		FlowFieldSystem.flow_field = FlowFieldSystem.create_flow_field(States.world[1][SpacialComponent].grid_pos)

		pygame.display.update()

	def run(self):
		while States.GAME_RUNNING:
			self.update()
			self.draw()
			if Settings.WINDOW.DEBUG:
				self.handle_debug()
			

Main().run()