import pygame

from Core import States
from ECS import Factories
from ECS.Components import SpacialComponent
from ECS.Systems import AINavigationSystem, CameraSystem, DebugRenderingSystem, EnemySpawner, FlowFieldSystem, InputSystem, RenderingSystem, DebugSystem, MovementSystem
from Globals import Settings

class Main:
	def __init__(self) -> None:
		States.PLAYER_ID = Factories.spawn_player(States.world, States.spatial_grid, 0, 0)
		States.camera = Factories.new_camera((0, 0), Settings.CAMERA.SIZE, States.PLAYER_ID)


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
		AINavigationSystem.process(States.world, events)
		MovementSystem.process(States.world, States.spatial_grid, events, dt)
		EnemySpawner.process(States.world, States.spatial_grid)

		CameraSystem.process(States.world, States.camera, dt)
		FlowFieldSystem.flow_field = FlowFieldSystem.create_flow_field(States.world[States.PLAYER_ID][SpacialComponent].grid_pos)

		pygame.display.update()

	def run(self):
		while States.GAME_RUNNING:
			self.update()
			self.draw()
			if Settings.WINDOW.DEBUG:
				self.handle_debug()
			

Main().run()