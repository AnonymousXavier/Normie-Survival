import pygame

pygame.display.init()

def load_sprite(file_path: str):
	return pygame.image.load(file_path)

def load_animation(file_path: str, goal_sprite_dimension: tuple, vertical=False):
	sprite_sheet = load_sprite(file_path)

	full_w, full_h = sprite_sheet.size
	w, h = goal_sprite_dimension

	cols, rows = full_w // w, full_h // h

	frames = []
	for yi in range(rows):
		row = []
		for xi in range(cols):
			frame = pygame.Surface((w, h), pygame.SRCALPHA)
			x = xi * w
			y = yi * h

			frame.blit(sprite_sheet, (0, 0), pygame.Rect(x, y, w, h))
			row.append(frame)

		frames.append(row)

	transposed_frames = [] 
	if vertical:
		for yi in range(rows):
			row = []
			for xi in range(cols):
				row.append(frames[xi][yi])
			transposed_frames.append(row)

		return transposed_frames
	return frames

