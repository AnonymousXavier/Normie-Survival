import pygame
import math

from ECS.Components import SpacialComponent, RenderComponent, RotationComponent, PowerUpTag
from ECS.Systems import CameraSystem
from Globals import Misc

def process(world: dict, camera: dict):
	mx, my = pygame.mouse.get_pos()
	
	cam_rect = camera[SpacialComponent].rect
	cam_boundary = CameraSystem.get_boundary_of(camera)
	render_data = Misc.get_camera_rendering_data(cam_boundary)
	
	scale = render_data["size"][0] / cam_boundary["world_size"][0]
	ox, oy = render_data["offset"]
	
	# Convert Screen Space -> World Space
	world_mx = ((mx - ox) / scale) + cam_rect.left
	world_my = ((my - oy) / scale) + cam_rect.top
	
	# Process Aiming
	for obj_id in world:
		obj = world[obj_id]
		if PowerUpTag in obj and RotationComponent in obj and RenderComponent in obj:
			center_x = obj[SpacialComponent].rect.centerx
			center_y = obj[SpacialComponent].rect.centery
			
			dx = world_mx - center_x
			dy = world_my - center_y
			
			angle_rad = math.atan2(-dy, dx) 
			angle_deg = math.degrees(angle_rad)
			
			current_angle = obj[RotationComponent].angle
			
			# Only rotate if angle changed by > 2 degrees
			if abs(current_angle - angle_deg) > 2.0:
				obj[RotationComponent].angle = angle_deg
				
				base_sprite = obj[RenderComponent].base_sprite
				if base_sprite:
					rotated_sprite = pygame.transform.rotate(base_sprite, angle_deg)
					
					# Rotating changes the image size. Re-center it!
					new_rect = rotated_sprite.get_rect(center=obj[SpacialComponent].rect.center)
					obj[SpacialComponent].rect.size = new_rect.size
					
					obj[RenderComponent].sprite = rotated_sprite