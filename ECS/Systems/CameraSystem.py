from pygame import Rect, math
from ECS.Components import SpacialComponent, StalkerComponent
from Globals import Misc, Settings

def process(world: dict, camera: dict, delta: float):
	cam_rect: Rect = camera[SpacialComponent].rect

	targets_id = camera[StalkerComponent].target_id
	targets_rect = world[targets_id][SpacialComponent].rect

	boundary = get_boundary_of(camera)
	cw, ch = boundary["world_size"]

	cam_rect.center = Misc.interpolate_towards(cam_rect.center, targets_rect.center, delta * 2)

	cam_rect.centerx = math.clamp(cam_rect.centerx, cw // 2, Settings.MAP.COLS - cw // 2)
	cam_rect.centery = math.clamp(cam_rect.centery, ch // 2, Settings.MAP.ROWS - ch // 2)

def get_boundary_of(camera: dict):
	cam_rect: Rect = camera[SpacialComponent].rect
	sprite_width, sprite_height = Settings.SPRITE.SIZE

	gtop = cam_rect.top // sprite_height
	gleft = cam_rect.left // sprite_width
	gbottom = cam_rect.bottom // sprite_height
	gright = cam_rect.right // sprite_width

	return {
		"top": round(gtop), 
		"bottom": round(gbottom), 
		"left": round(gleft), 
		"right": round(gright), 
		"world_size": (round(cam_rect.right - cam_rect.left), round(cam_rect.bottom - cam_rect.top))
	}
