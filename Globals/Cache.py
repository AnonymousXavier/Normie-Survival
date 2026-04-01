from ECS.Loaders import SpriteLoader
from Globals import Enums

class SPRITES:
	class DEBUG:
		ARROWS_SHEET = SpriteLoader.load_animation("Assets\\Sprites\\Debug\\arrow_icos.png", (16, 16))[0]
		ARROWS_SPRITES = {
			Enums.DIRECTIONS.UP : ARROWS_SHEET[0],
			Enums.DIRECTIONS.LEFT: ARROWS_SHEET[1],
			Enums.DIRECTIONS.RIGHT: ARROWS_SHEET[2],
			Enums.DIRECTIONS.DOWN: ARROWS_SHEET[3],
			(0, 0): ARROWS_SHEET[4],
		}
