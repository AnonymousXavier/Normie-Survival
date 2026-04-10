import pygame

pygame.init()


class WINDOW:
    DESKTOP_WIDTH, DESKTOP_HEIGHT = pygame.display.get_desktop_sizes()[0]

    MIN_WIDTH = 500
    MIN_HEIGHT = 500

    WIDTH = 500
    HEIGHT = 500
    SIZE = WIDTH, HEIGHT

    TITLE = "NORMIE SURVIVAL"


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
    UI_UPDATES_PER_SEC = 1
    FIELD_UPDATES_PER_SEC = 1
    FPS = 60


class GAME:
    PLAYER_SPEED = 5  # Cells per secs
    ENEMY_SPEED = 2

    PLAYER_HITBOX_TO_SPRITE_RATIO = 0.375
    ENEMY_HITBOX_TO_SPRITE_RATIO = 0.75

    MAX_ENEMIES_SPAWNABLE = 250
    EXACT_SECS_MAX_ENEMIES_ARE_ALLOWED_TO_SPAWN = 800
    MAX_DISTANCE_FROM_PLAYER = 12

    DEFAULT_PLAYER_HP = 10
    DEFAULT_ENEMY_HP = 3

    XP_GEM_SIZE = (4, 4)
    TIME_ELAPSED_TO_ENEMIES_RATIO = 1  # Increase by n every min

    BOSS_SPAWN_TIME_DELAY = 210  # secs
    BOSS_STRENGTH_MULTIPLIER = 100
    STRONGER_ENEMIES_MULTIPLIER = 5
    PLAYER_LEVEL_TO_ENEMY_HEALTH_EXPONENT = 0

    BOSS_SPAWN_DISTANCE_FROM_PLAYER = 12

    SHIELD_RADIUS = 12

    GAME_DELAY_ON_PLAYER_HIT = 0
    GAME_DELAY_ON_BOSS_KILLED = 0
    GAME_DELAY_ON_BOSS_HIT = 0


class UPGRADES_MAX_LEVELS:
    WEAPON = 40
    DEFENSE = 30
    QOL = 15
    PASSIVES = 30


class GAME_OPTIONS:
    SOUND = True
    MUSIC = True
    SCREEN_SHAKE = True


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
    CELLS_IN_VIEW = 18
    ZOOM = WINDOW.HEIGHT / (CELLS.HEIGHT * CELLS_IN_VIEW)
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
    DASH = (pygame.K_SPACE, pygame.K_LSHIFT)


window = pygame.display.set_mode(WINDOW.SIZE, pygame.RESIZABLE)
pygame.display.set_caption(WINDOW.TITLE.capitalize())


class COMPONENTS_BASE_VALUES:
    class PICKUP:
        distance = 3.0

    class DASH:
        cooldown = 10
        duration = 0.2
