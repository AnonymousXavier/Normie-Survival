from ECS.Components import PowerUpComponent, SpacialComponent, RenderComponent
from ECS.Systems import CameraSystem

import pygame

from Globals import Misc

def process(surface: pygame.Surface, world: dict,  camera:dict, visible_entities: list):
	camera_rect: pygame.Rect = camera[SpacialComponent].rect
	cam_boundary = CameraSystem.get_boundary_of(camera)
	
	rendering_data = Misc.get_camera_rendering_data(cam_boundary)
	
	game_entities_rendered_surface = draw_game_entities(world, cam_boundary, camera_rect, visible_entities)
	entities_transformed_surface = pygame.transform.scale(game_entities_rendered_surface, rendering_data["size"])

	surface.blit(entities_transformed_surface, rendering_data["offset"])

def draw_game_entities(world: dict,cam_boundary: dict, camera_rect, visible_entities: list):
	cbw, cbh = cam_boundary["world_size"]
	
	sorted_entities = sorted(
		visible_entities,
		key=lambda obj_id: world[obj_id][RenderComponent].z_index
		)

	render_surface = pygame.Surface((cbw, cbh))
	for obj_id in sorted_entities:

		if SpacialComponent in world[obj_id] and RenderComponent in world[obj_id]:
			obj = world[obj_id]
			obj_rect = obj[SpacialComponent].rect
			render_pos = obj_rect.left - camera_rect.left, obj_rect.top - camera_rect.top

			render_rect = pygame.Rect(render_pos, obj_rect.size)

			if obj[RenderComponent].sprite:
				render_surface.blit(obj[RenderComponent].sprite, render_rect)
			else:
				pygame.draw.rect(render_surface, obj[RenderComponent].color, render_rect)

			if PowerUpComponent in obj:
				print(obj_id)

	return render_surface
