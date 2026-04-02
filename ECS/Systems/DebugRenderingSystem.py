import pygame
from Globals import Misc
from ECS.Systems import CameraSystem
from ECS.Components import SpacialComponent, RenderComponent

def process(surface: pygame.Surface, debug: dict, debug_grid: dict,  camera:dict):
	cam_boundary = CameraSystem.get_boundary_of(camera)
	
	rendering_data = Misc.get_camera_rendering_data(cam_boundary)

	debug_elements_rendered_surface = draw_debug_elements(debug, debug_grid, camera, cam_boundary)
	debug_transformed_surface =  pygame.transform.scale(debug_elements_rendered_surface, rendering_data["size"])
	surface.blit(debug_transformed_surface, rendering_data["offset"])

def draw_debug_elements(debug: dict, debug_grid: dict, camera: dict, cam_boundary: dict):
	cbw, cbh = cam_boundary["world_size"]
	cam_left, cam_top = cam_boundary["left"], cam_boundary["top"]
	cam_right, cam_bottom = cam_boundary["right"], cam_boundary["bottom"]

	camera_rect: pygame.Rect = camera[SpacialComponent].rect
	render_surface = pygame.Surface((cbw, cbh))

	for iy in range(cam_top, cam_bottom + 1):
		for ix in range(cam_left, cam_right + 1):
			if (ix, iy) in debug_grid:
				for obj_id in debug_grid[(ix, iy)]:
					obj = debug[obj_id]
					obj_rect = obj[SpacialComponent].rect
					render_pos = obj_rect.left - camera_rect.left, obj_rect.top - camera_rect.top

					render_rect = pygame.Rect(render_pos, obj_rect.size)

					if obj[RenderComponent].sprite:
						render_surface.blit(obj[RenderComponent].sprite, render_rect)
					else:
						pygame.draw.rect(render_surface, obj[RenderComponent].color, render_rect)

	return render_surface