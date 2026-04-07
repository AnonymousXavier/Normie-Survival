import pygame

pygame.init()


class WINDOW:
    DESKTOP_WIDTH, DESKTOP_HEIGHT = pygame.display.get_desktop_sizes()[0]

    MIN_WIDTH = 500
    MIN_HEIGHT = 500

    WIDTH = 500
    HEIGHT = 500
    SIZE = WIDTH, HEIGHT

    CLOCK = pygame.Clock()


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
    PLAYER_SPEED = 5  # Cells per secs
    ENEMY_SPEED = 2

    PLAYER_HITBOX_TO_SPRITE_RATIO = 0.375
    ENEMY_HITBOX_TO_SPRITE_RATIO = 0.75

    FIELD_OF_VIEW_IN_PERCENT = 0.8  # Renderable Region Isze compared to window size

    ALLOWABLE_NUMBER_OF_ENEMIES_ON_SCREEN = 100
    MAX_DISTANCE_FROM_PLAYER = 25

    DEFAULT_PLAYER_HP = 10
    DEFAULT_ENEMY_HP = 3

    XP_GEM_SIZE = (4, 4)
    TIME_ELAPSED_TO_ENEMIES_RATIO = 5  # Increase by n every min

    BOSS_SPAWN_TIME_DELAY = 600  # secs
    BOSS_STRENGTH_MULTIPLIER = 100
    STRONGER_ENEMIES_MULTIPLIER = 5
    PLAYER_LEVEL_TO_ENEMY_HEALTH_EXPONENT = 0
    PLAYER_LEVEL_TO_BOSS_HEALTH_EXPONENT = 1.25

    BOSS_SPAWN_DISTANCE_FROM_PLAYER = 10

    SHIELD_RADIUS = 12


class GAME_OPTIONS:
    SOUND = False


class COLOURS:
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    BROWN = (100, 100, 0)
    YELLOW = (255, 255, 0)
    GOLD = (255, 215, 0)


class DEBUG:
    ENABLED = False
    PLAYER_COLOR = COLOURS.BLUE
    ENEMY_COLOR = COLOURS.GREEN
    HITBOX_COLOR = COLOURS.RED
    BOSS_COLOR = COLOURS.RED
    WEAPON_COLOR = COLOURS.BROWN
    BULLET_COLOR = COLOURS.YELLOW


class CAMERA:
    ZOOM = WINDOW.HEIGHT / (
        CELLS.HEIGHT * GAME.MAX_DISTANCE_FROM_PLAYER * GAME.FIELD_OF_VIEW_IN_PERCENT
    )
    WIDTH = WINDOW.WIDTH / ZOOM
    HEIGHT = WINDOW.HEIGHT / ZOOM

    SIZE = WIDTH, HEIGHT

    @classmethod
    def update(cls):
        pass


class CONTROLS:
    UP = (pygame.K_w, pygame.K_UP)
    DOWN = (pygame.K_s, pygame.K_DOWN)
    LEFT = (pygame.K_a, pygame.K_LEFT)
    RIGHT = (pygame.K_d, pygame.K_RIGHT)


window = pygame.display.set_mode(WINDOW.SIZE, pygame.RESIZABLE)
