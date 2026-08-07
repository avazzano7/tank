import pygame
import math


class Player:

    def __init__(self, x, y):

        # World position
        self.position = pygame.Vector2(x, y)

        # Movement
        self.velocity = pygame.Vector2(0, 0)

        self.angle = -90

        self.rotation_speed = 5
        self.thrust_power = 0.15

        self.max_speed = 8

        # Weapon
        self.bullet_interval = 0.25
        self.bullet_timer = 0.0

    def get_forward_direction(self):

        return pygame.Vector2(
            math.cos(math.radians(self.angle)),
            math.sin(math.radians(self.angle))
        )

    def rotate(self, amount):

        self.angle += amount * self.rotation_speed

    def thrust(self):

        direction = self.get_forward_direction()

        self.velocity += direction * self.thrust_power

    def update(self, dt):

        # Weapon timer
        self.bullet_timer -= dt

        # Limit speed
        if self.velocity.length() > self.max_speed:

            self.velocity.scale_to_length(
                self.max_speed
            )

        # Move
        self.position += self.velocity

        # Space friction
        self.velocity *= 0.98

    def can_fire(self):

        return self.bullet_timer <= 0

    def fire(self):

        self.bullet_timer = self.bullet_interval

    def draw(self, screen, camera):

        screen_position = (
            self.position - camera
        )

        direction = self.get_forward_direction()

        left = pygame.Vector2(
            math.cos(math.radians(self.angle + 140)),
            math.sin(math.radians(self.angle + 140))
        )

        right = pygame.Vector2(
            math.cos(math.radians(self.angle - 140)),
            math.sin(math.radians(self.angle - 140))
        )

        points = [
            screen_position + direction * 25,
            screen_position + left * 15,
            screen_position + right * 15
        ]

        pygame.draw.polygon(
            screen,
            (255, 255, 255),
            points,
            2
        )