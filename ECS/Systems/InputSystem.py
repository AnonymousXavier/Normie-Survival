import pygame

from ECS.Systems import ClickingSystem
from Core import States
from ECS.Components import PlayerInputTag
from Globals import Enums, Settings

def process(world: dict, global_events: list):
	pressed_keys = pygame.key.get_pressed()
	# Handle Player Movements

	player_id = States.PLAYER_ID
	if States.PLAYER_ID:
		if is_key_pressed(pressed_keys, Settings.CONTROLS.DOWN): 
			global_events.append({"type": Enums.EVENT_TYPES.MOVEMENT_INTENT, "entity_id": player_id, "dx": 0, "dy": 1})
		if is_key_pressed(pressed_keys,Settings.CONTROLS.UP): 
			global_events.append({"type": Enums.EVENT_TYPES.MOVEMENT_INTENT, "entity_id": player_id, "dx": 0, "dy": -1})
		if is_key_pressed(pressed_keys, Settings.CONTROLS.LEFT): 
			global_events.append({"type": Enums.EVENT_TYPES.MOVEMENT_INTENT, "entity_id": player_id, "dx": -1, "dy": 0})
		if is_key_pressed(pressed_keys, Settings.CONTROLS.RIGHT): 
			global_events.append({"type": Enums.EVENT_TYPES.MOVEMENT_INTENT, "entity_id": player_id, "dx": 1, "dy": 0})

	# --- 1. MOUSE TRANSLATION ---
	raw_mx, raw_my = pygame.mouse.get_pos()
	win_w, win_h = pygame.display.get_surface().get_size()
	screen_w, screen_h = Settings.WINDOW.DESKTOP_WIDTH, Settings.WINDOW.DESKTOP_HEIGHT

	# Calculate the scale the RenderingSystem is currently using
	scale = min(win_w / screen_w, win_h / screen_h)

	# Calculate the black bar padding
	scaled_w = int(screen_w * scale)
	scaled_h = int(screen_h * scale)
	offset_x = (win_w - scaled_w) // 2
	offset_y = (win_h - scaled_h) // 2

	# Reverse the math to get the exact logical pixel the mouse is pointing at!
	logical_mx = int((raw_mx - offset_x) / scale)
	logical_my = int((raw_my - offset_y) / scale)

	# Save it globally so UIHoverSystem can check it continuously without needing an event
	States.SCREEN_MOUSE_POS = (logical_mx, logical_my)

    # --- 2. EVENT BROADCASTING ---

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			States.GAME_RUNNING = False
			break
		# WINDOW RESIZING
		elif event.type == pygame.VIDEORESIZE:

			w, h = max(Settings.WINDOW.MIN_WIDTH, event.w), max(Settings.WINDOW.MIN_HEIGHT, event.h)

			Settings.WINDOW.WIDTH = w
			Settings.WINDOW.HEIGHT = h
			Settings.WINDOW.SIZE = (Settings.WINDOW.WIDTH, Settings.WINDOW.HEIGHT)

			Settings.window = pygame.display.set_mode(Settings.WINDOW.SIZE, pygame.RESIZABLE)
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_F11:
				pygame.display.toggle_fullscreen()
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			# Broadcast a clean, translated click event for the ClickingSystem!
			global_events.append({
				"type": Enums.EVENT_TYPES.MOUSE_CLICK,
				"pos": (logical_mx, logical_my)
			})

		ClickingSystem.process(States.world, global_events, event)

def is_key_pressed(pressed_keys, binded_keys: tuple):
	for key in binded_keys:
		if pressed_keys[key]:
			return True
	return False