import math

import pygame

from core.settings import WIDTH, HEIGHT


class Missile:

    SPEED = 8
    LIFETIME = 2.5
    RADIUS = 6

    # Visual shape — oriented rectangle body with a pointed nose
    LENGTH = 18
    BODY_WIDTH = 6
    NOSE_LENGTH = 6

    COLOR = (255, 140, 60)

    def __init__(self, position, direction, damage, splash_radius):

        self.position = pygame.Vector2(position)
        self.direction = pygame.Vector2(direction).normalize()

        self.damage = damage
        self.splash_radius = splash_radius

        self.age = 0

    def update(self, dt):

        self.position += self.direction * self.SPEED

        self.age += dt

        return self.age < self.LIFETIME

    def draw(self, screen, camera):

        screen_position = self.position - camera

        # Don't bother drawing missiles that are far outside
        # the visible screen.
        if (
            -20 < screen_position.x < WIDTH + 20
            and
            -20 < screen_position.y < HEIGHT + 20
        ):

            angle = math.degrees(
                math.atan2(
                    self.direction.y,
                    self.direction.x,
                )
            )

            half_width = self.BODY_WIDTH / 2

            # Local-space points, nose pointing along +x.
            # Rotated to face the missile's travel direction.
            local_points = [
                pygame.Vector2(-self.LENGTH / 2, -half_width),
                pygame.Vector2(self.LENGTH / 2 - self.NOSE_LENGTH, -half_width),
                pygame.Vector2(self.LENGTH / 2, 0),
                pygame.Vector2(self.LENGTH / 2 - self.NOSE_LENGTH, half_width),
                pygame.Vector2(-self.LENGTH / 2, half_width),
            ]

            points = [
                screen_position + point.rotate(angle)
                for point in local_points
            ]

            pygame.draw.polygon(
                screen,
                self.COLOR,
                points,
            )