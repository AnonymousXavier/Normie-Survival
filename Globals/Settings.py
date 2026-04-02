import pygame

class WINDOW:
	MIN_WIDTH = 500
	MIN_HEIGHT = 500
	
	WIDTH = 500
	HEIGHT = 500
	SIZE = WIDTH, HEIGHT

	DEBUG = True
	CLOCK = pygame.Clock()

class MAP:
	ROWS = 20
	COLS = 20
	SIZE = ROWS, COLS

class SPRITE:
	WIDTH = 16
	HEIGHT = 16
	SIZE = WIDTH, HEIGHT

class CELLS:
	WIDTH = SPRITE.WIDTH
	HEIGHT = SPRITE.HEIGHT
	SIZE = WIDTH, HEIGHT

class UPDATE:
	INPUT_CHECKS_PER_SEC = 15
	FPS = 60

class GAME:
	PLAYER_SPEED = 8

class COLOURS:
	BLACK = (0, 0, 0)
	RED = (255, 0, 0)

class DEBUG:
	PLAYER_COLOR = COLOURS.RED

class CAMERA:
	ZOOM = 2 
	WIDTH = WINDOW.WIDTH / ZOOM
	HEIGHT = WINDOW.HEIGHT / ZOOM

	SIZE = WIDTH, HEIGHT

class CONTROLS:
	UP = (pygame.K_w, pygame.K_UP)
	DOWN = (pygame.K_s, pygame.K_DOWN)
	LEFT = (pygame.K_a, pygame.K_LEFT)
	RIGHT = (pygame.K_d, pygame.K_RIGHT)

window = pygame.display.set_mode(WINDOW.SIZE, pygame.RESIZABLE)