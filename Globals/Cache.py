from ECS.Loaders import SpriteLoader
from Globals import Enums


class SPRITES:
    class DEBUG:
        ARROWS_SHEET = SpriteLoader.load_animation(
            "Assets\\Sprites\\Debug\\arrow_icos.png", (16, 16)
        )[0]
        ARROWS_SPRITES = {
            Enums.DIRECTIONS.UP: ARROWS_SHEET[0],
            Enums.DIRECTIONS.LEFT: ARROWS_SHEET[1],
            Enums.DIRECTIONS.RIGHT: ARROWS_SHEET[2],
            Enums.DIRECTIONS.DOWN: ARROWS_SHEET[3],
            (0, 0): ARROWS_SHEET[4],
        }

    class PLAYER:
        idle_sprite_sheet = SpriteLoader.load_animation(
            "Assets/Sprites/Player/Idle.png", (16, 16)
        )
        dead_sprite = SpriteLoader.load_sprite("Assets/Sprites/Player/Dead.png")
        IDLE = [
            [idle_sprite_sheet[0][Enums.ANIM_DIRS.DOWN]],
            [idle_sprite_sheet[0][Enums.ANIM_DIRS.UP]],
            [idle_sprite_sheet[0][Enums.ANIM_DIRS.LEFT]],
            [idle_sprite_sheet[0][Enums.ANIM_DIRS.RIGHT]],
        ]
        WALK = SpriteLoader.load_animation(
            "Assets/Sprites/Player/Walk.png", (16, 16), True
        )
        DEAD = [dead_sprite, dead_sprite, dead_sprite, dead_sprite]

    class ENEMY:
        NORMAL_WALK = SpriteLoader.load_animation(
            "Assets/Sprites/Enemy/GreenCyclopsWalk.png", (16, 16), True
        )
        RED_WALK = SpriteLoader.load_animation(
            "Assets/Sprites/Enemy/RedCyclopsWalk.png", (16, 16), True
        )
        boss_walk = SpriteLoader.load_animation(
            "Assets/Sprites/Enemy/BossWalk.png", (50, 50)
        )[0]
        BOSS = [boss_walk, boss_walk, boss_walk, boss_walk]

    class ITEMS:
        GEM = SpriteLoader.load_sprite("Assets/Sprites/Gem.png")

    class WEAPONS:
        SHOTGUN = SpriteLoader.load_sprite("Assets/Sprites/Weapons/shotgun.png")
        SNIPER = SpriteLoader.load_sprite("Assets/Sprites/Weapons/sniper.png")

    class MENU:
        COVER_ART = SpriteLoader.load_sprite(
            "Assets/Sprites/Menu/NinjaAdventure CoverArt.png"
        )
        CONTROLS = SpriteLoader.load_sprite("Assets/Sprites/Menu/Controls.png")
