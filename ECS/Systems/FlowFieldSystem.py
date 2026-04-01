from collections import deque
import pygame
from Globals import Cache, Settings

flow_field = {}

def create_flow_field(target_pos):
	direction_field = {}

	queue = deque()
	queue.append(target_pos)

	direction_field[target_pos] = 0, 0

	while queue:
		px, py = queue.popleft() # Get First Point

		for neighbour in _get_cell_neighbours((px, py)):
			if neighbour not in direction_field:

				nx, ny = neighbour
				dx, dy = px - nx, py - ny

				direction_field[neighbour] = dx, dy
				queue.append(neighbour)

	return direction_field

def _get_cell_neighbours(pos: tuple):
		px, py = pos
		directions = [(-1, 0), (0, 1), (0, -1), (1, 0)]
		neighbours = []

		w, h = Settings.MAP.SIZE

		for dx, dy in directions:
			nx, ny = px + dx, py + dy
			if 0 <= nx < w and 0 <= ny < h:
				neighbours.append((nx, ny))

		return neighbours

def draw(surface: pygame.Surface):
	cw, ch = Settings.CELLS.SIZE

	for xi, yi in flow_field:
		x = xi * cw
		y = yi * ch

		col = (100, 100, 100)
		if flow_field[(xi, yi)] == 0:
			col = (150, 125, 125)

		icon_surface = Cache.SPRITES.DEBUG.ARROWS_SPRITES[flow_field[(xi, yi)]]

		rect = pygame.Rect(x, y, cw, ch)
		icon_rect = icon_surface.get_rect(center = rect.center)
		pygame.draw.rect(surface, col, rect)
		surface.blit(icon_surface, icon_rect)
