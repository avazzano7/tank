import pygame
import math

from core.settings import (
    PLAYER_MAX_HEALTH,
    PLAYER_COLLISION_RADIUS,
    PLAYER_INVULNERABILITY_DURATION,
)


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

        # Health / collision
        self.max_health = PLAYER_MAX_HEALTH
        self.health = self.max_health

        self.radius = PLAYER_COLLISION_RADIUS

        self.invulnerable_timer = 0.0

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

        # Invulnerability timer
        if self.invulnerable_timer > 0:

            self.invulnerable_timer -= dt

            if self.invulnerable_timer < 0:

                self.invulnerable_timer = 0

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

    # ------------------------------------------------------
    # Health
    # ------------------------------------------------------

    def is_invulnerable(self):

        return self.invulnerable_timer > 0

    def take_damage(self, amount):

        if self.is_invulnerable():

            return False

        self.health -= amount

        if self.health < 0:

            self.health = 0

        self.invulnerable_timer = (
            PLAYER_INVULNERABILITY_DURATION
        )

        return self.health <= 0

    def is_alive(self):

        return self.health > 0

    def reset_health(self):

        self.health = self.max_health

        self.invulnerable_timer = 0.0

    def draw(self, screen, camera):

        # Flicker while invulnerable
        if self.is_invulnerable():

            flicker_on = (
                int(self.invulnerable_timer * 10) % 2 == 0
            )

            if not flicker_on:

                return

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