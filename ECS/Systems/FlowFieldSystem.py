from collections import deque
from ECS import Factories
from Globals import Cache, Settings

flow_field = {}

def create_flow_field(target_pos):
	max_radius=Settings.GAME.MAX_DISTANCE_FROM_PLAYER

	direction_field = {}
	queue = deque()
	queue.append(target_pos)
	direction_field[target_pos] = 0, 0

	while queue:
		px, py = queue.popleft() 
		
		# Stop calculating if we've gone too far from the player
		if abs(px - target_pos[0]) > max_radius or abs(py - target_pos[1]) > max_radius:
			continue

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
	
	for dx, dy in directions:
		neighbours.append((px + dx, py + dy))

	return neighbours

def store_arrows_in_degub(debug: dict, debug_grid: dict):
	for xi, yi in flow_field:
		icon_surface = Cache.SPRITES.DEBUG.ARROWS_SPRITES[flow_field[(xi, yi)]]
		Factories.spawn_flowfield_arrow(debug, debug_grid, xi, yi, icon_surface)
