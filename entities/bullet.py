import pygame

from core.settings import WIDTH, HEIGHT


class Bullet:

    SPEED = 12
    LIFETIME = 1.5
    RADIUS = 3

    def __init__(self, position, direction):

        self.position = pygame.Vector2(position)
        self.direction = pygame.Vector2(direction).normalize()

        self.age = 0

    def update(self, dt):

        self.position += self.direction * self.SPEED

        self.age += dt

        return self.age < self.LIFETIME

    def draw(self, screen, camera):

        screen_position = self.position - camera

        # Don't bother drawing bullets that are far outside
        # the visible screen.
        if (
            -10 < screen_position.x < WIDTH + 10
            and
            -10 < screen_position.y < HEIGHT + 10
        ):

            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (
                    int(screen_position.x),
                    int(screen_position.y),
                ),
                self.RADIUS,
            )