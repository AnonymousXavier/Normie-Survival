from Globals import Settings

def register_entity_in_grid(entity_id: int, pos: tuple, spatial_grid: dict):
	if pos not in spatial_grid:
		spatial_grid[pos] = [entity_id]
	else:
		spatial_grid[pos].append(entity_id)

def remove_entity_from_grid(entity_id: int, pos: tuple, spatial_grid: dict):
	if pos in spatial_grid:
		if entity_id in spatial_grid[pos]:
			spatial_grid[pos].remove(entity_id)
			if spatial_grid[pos] == []:
				del spatial_grid[pos]
			return True

def interpolate_towards(position: tuple, target_position, speed: float):
	tx, ty = target_position
	px, py = position

	return lerp(px, tx, speed), lerp(py, ty, speed)

def move_towards(position: tuple, target_position: tuple, speed: float):
	px, py = position
	tx, ty = target_position
	dx, dy = round(tx - px), round(ty - py)

	nx, ny = px + dx * speed, py + dy * speed

	if dx == 0:
		nx = tx
	if dy == 0:
		ny = ty

	return nx, ny


def lerp(start: float, end: float, speed: float):
	if abs(speed) > abs(round(end - start)): 
		return end
	return start + round(end - start) * speed

def get_entities_on_screen(world: dict, spatial_grid: dict, cam_boundary: dict):
	
	cam_left, cam_top = cam_boundary["left"], cam_boundary["top"]
	cam_right, cam_bottom = cam_boundary["right"], cam_boundary["bottom"]

	visible_renderable_entities = []
	for iy in range(cam_top, cam_bottom + 1):
		for ix in range(cam_left, cam_right + 1):
			if (ix, iy) in spatial_grid:
				for obj_id in spatial_grid[(ix, iy)]:
					visible_renderable_entities.append(obj_id)

	return visible_renderable_entities

def clamp(value, min_value, max_value):
	if value > max_value:
		return min_value
	if value < min_value:
		return max_value
	return value

def get_camera_rendering_data(cam_boundary: dict):
	cbw, cbh = cam_boundary["world_size"]

	# FOR WINDOW RESIZ-ING
	scale_x = Settings.WINDOW.WIDTH / cbw
	scale_y = Settings.WINDOW.HEIGHT / cbh
	scale = min(scale_x, scale_y) 
	
	w = int(cbw * scale)
	h = int(cbh * scale)

	ox = (Settings.WINDOW.WIDTH - w) // 2
	oy = (Settings.WINDOW.HEIGHT - h) // 2

	return {"size": (w, h), "offset": (ox, oy)}


