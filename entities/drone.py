import math

import pygame


class Drone:

    RADIUS = 8

    COLOR = (100, 200, 255)

    def __init__(self, orbit_radius, orbit_speed):

        self.orbit_angle = 0.0

        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed

        self.position = pygame.Vector2(0, 0)

        self.fire_timer = 0.0

    # ------------------------------------------------------
    # Orbit
    # ------------------------------------------------------

    def update_orbit(self, player_position, dt):

        self.orbit_angle += self.orbit_speed * dt

        angle_rad = math.radians(
            self.orbit_angle
        )

        offset = pygame.Vector2(
            math.cos(angle_rad),
            math.sin(angle_rad),
        ) * self.orbit_radius

        self.position = (
            pygame.Vector2(player_position)
            + offset
        )

    # ------------------------------------------------------
    # Firing
    # ------------------------------------------------------

    def tick_fire_timer(self, dt):

        self.fire_timer -= dt

    def can_fire(self):

        return self.fire_timer <= 0

    def reset_fire_timer(self, interval):

        self.fire_timer = interval

    # ------------------------------------------------------
    # Draw
    # ------------------------------------------------------

    def draw(self, screen, camera):

        screen_position = (
            self.position - camera
        )

        points = [
            screen_position + pygame.Vector2(0, -self.RADIUS),
            screen_position + pygame.Vector2(self.RADIUS, 0),
            screen_position + pygame.Vector2(0, self.RADIUS),
            screen_position + pygame.Vector2(-self.RADIUS, 0),
        ]

        pygame.draw.polygon(
            screen,
            self.COLOR,
            points,
            2,
        )