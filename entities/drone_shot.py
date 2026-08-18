import pygame

from core.settings import WIDTH, HEIGHT


class DroneShot:

    SPEED = 10
    LIFETIME = 1.2
    RADIUS = 3

    COLOR = (150, 220, 255)

    def __init__(self, position, direction, damage):

        self.position = pygame.Vector2(position)
        self.direction = pygame.Vector2(direction).normalize()

        self.damage = damage

        self.age = 0

    def update(self, dt):

        self.position += self.direction * self.SPEED

        self.age += dt

        return self.age < self.LIFETIME

    def draw(self, screen, camera):

        screen_position = self.position - camera

        # Don't bother drawing shots that are far outside
        # the visible screen.
        if (
            -10 < screen_position.x < WIDTH + 10
            and
            -10 < screen_position.y < HEIGHT + 10
        ):

            pygame.draw.circle(
                screen,
                self.COLOR,
                (
                    int(screen_position.x),
                    int(screen_position.y),
                ),
                self.RADIUS,
            )