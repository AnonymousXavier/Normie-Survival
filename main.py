import pygame

from ECS.Systems import FlowFieldSystem
from Globals import Settings

class Main:
	def __init__(self) -> None:
		self.running = True
		self.window = pygame.display.set_mode(Settings.WINDOW.SIZE)

		w, h = Settings.MAP.SIZE
		hw, hh = w // 2, h // 2
		FlowFieldSystem.flow_field = FlowFieldSystem.create_flow_field((hw, hh))

	def draw(self):
		FlowFieldSystem.draw(self.window)

	def input(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

	def update(self):
		self.input()

		mx, my = pygame.mouse.get_pos()
		mxi, myi = mx // Settings.CELLS.WIDTH, my // Settings.CELLS.HEIGHT

		FlowFieldSystem.flow_field = FlowFieldSystem.create_flow_field((mxi, myi))
		pygame.display.update()

	def run(self):
		while self.running:
			self.update()
			self.draw()

Main().run()