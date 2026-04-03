import pygame

from Core import States
from ECS import Factories
from ECS.Components import SpacialComponent
from ECS.Systems import AINavigationSystem, CollisionSystem, AimingSystem, WeaponSystem,CameraSystem, DebugRenderingSystem, EnemySpawner, FlowFieldSystem, InputSystem, OrbitalSystem, ProjectileSystem, RenderingSystem, DebugSystem, MovementSystem
from Globals import Settings

class Main:
	def __init__(self) -> None:
		States.PLAYER_ID = Factories.spawn_player(States.world, States.spatial_grid, 0, 0)
		States.camera = Factories.new_camera((0, 0), Settings.CAMERA.SIZE, States.PLAYER_ID)

		# Spawn two shotguns, opposite to each other, rotating at 90 degrees per second
		Factories.spawn_shotgun(States.world, States.spatial_grid, States.PLAYER_ID, start_angle=0.0)
		Factories.spawn_shotgun(States.world, States.spatial_grid, States.PLAYER_ID, start_angle=180.0)

	def draw(self):
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
		AimingSystem.process(States.world, States.spatial_grid, States.camera)

		AINavigationSystem.process(States.world, events)

		MovementSystem.process(States.world, States.spatial_grid, events, dt)
		ProjectileSystem.process(States.world, States.spatial_grid, States.camera, dt)
		WeaponSystem.process(States.world, States.spatial_grid, dt)

		# Run collisions after movement but before spawning new things
		CollisionSystem.process(States.world, States.spatial_grid)

		EnemySpawner.process(States.world, States.spatial_grid)
		OrbitalSystem.process(States.world, States.spatial_grid, dt)

		CameraSystem.process(States.world, States.camera, dt)
		FlowFieldSystem.flow_field = FlowFieldSystem.create_flow_field(States.world[States.PLAYER_ID][SpacialComponent].grid_pos)

		pygame.display.update()

	def run(self):
		while States.GAME_RUNNING:
			self.update()
			self.draw()
			if Settings.DEBUG.ENABLED:
				self.handle_debug()
			

Main().run()