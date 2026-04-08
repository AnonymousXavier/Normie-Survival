import pygame
import random


class ParticleManager:
    # Each particle: [x, y, vx, vy, lifetime, max_lifetime, color, size]
    particles = []
    lightning_bolts = []

    @classmethod
    def emit_sparks(cls, x, y, color=(255, 200, 50), count=8):
        """Fires a burst of particles from a specific point"""
        for _ in range(count):
            vx = random.uniform(-200, 200)
            vy = random.uniform(-200, 200)
            lifetime = random.uniform(0.15, 0.4)
            size = random.randint(2, 5)
            cls.particles.append([x, y, vx, vy, lifetime, lifetime, color, size])

    @classmethod
    def emit_lightning(cls, start_pos, end_pos):
        """Generates a jagged line path and stores it to flash on screen."""
        points = [start_pos]
        segments = random.randint(4, 7)  # How many "kinks" in the lightning
        variance = 15  # How far the lightning strays from a straight line

        # Calculate the mathematical step size between player and enemy
        dx = (end_pos[0] - start_pos[0]) / segments
        dy = (end_pos[1] - start_pos[1]) / segments

        for i in range(1, segments):
            # Move along the line, but add wild perpendicular jitter
            px = start_pos[0] + (dx * i) + random.uniform(-variance, variance)
            py = start_pos[1] + (dy * i) + random.uniform(-variance, variance)
            points.append((px, py))

        points.append(end_pos)

        # Store the bolt. It will live for exactly 5 frames to give a satisfying "flash/fade"
        cls.lightning_bolts.append(
            {
                "points": points,
                "life": 5,  # Current frame life
                "max_life": 5,  # Used to calculate the fade out
            }
        )

    @classmethod
    def update_and_draw(cls, window, dt, cam_x=0, cam_y=0):
        """Updates physics and draws directly to the screen"""
        if not cls.particles:
            return

        alive_particles = []
        for p in cls.particles:
            p[4] -= dt  # Decrease lifetime
            if p[4] > 0:
                # Apply velocity
                p[0] += p[2] * dt
                p[1] += p[3] * dt

                # Dynamic sizing (shrinks as it dies)
                current_size = max(1, int(p[7] * (p[4] / p[5])))

                # Apply camera offset if in gameplay, else draw absolute
                px = int(p[0] - cam_x)
                py = int(p[1] - cam_y)

                pygame.draw.rect(window, p[6], (px, py, current_size, current_size))
                alive_particles.append(p)

            cls.particles = alive_particles

        for bolt in cls.lightning_bolts[:]:
            bolt["life"] -= 1
            if bolt["life"] <= 0:
                cls.lightning_bolts.remove(bolt)
                continue

            # Calculate intensity: Starts at 255 (bright), fades to 0
            intensity = int((bolt["life"] / bolt["max_life"]) * 255)

            # Bright Cyan looks the most electric against dark backgrounds
            color = (intensity, 255, 255)

            # Draw the jagged segments
            points = bolt["points"]
            for i in range(len(points) - 1):
                # Apply your camera offset to keep it locked in the physical world!
                p1 = (points[i][0] - cam_x, points[i][1] - cam_y)
                p2 = (
                    points[i + 1][0] - cam_x,
                    points[i + 1][1] - cam_y,
                )

                # Line gets physically thinner as it fades
                pygame.draw.line(window, color, p1, p2, width=max(1, bolt["life"]))

    @classmethod
    def clear(cls):
        cls.particles.clear()
