from pygame import Rect
from ECS.Components import SpacialComponent, StalkerComponent
from Globals import Settings

def process(world: dict, camera: dict, delta: float):
	cam_rect: Rect = camera[SpacialComponent].rect

	targets_id = camera[StalkerComponent].target_id
	targets_rect = world[targets_id][SpacialComponent].rect

	cam_rect.center = targets_rect.center

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
