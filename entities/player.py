import pygame
import math

from core.settings import (
    PLAYER_MAX_HEALTH,
    PLAYER_COLLISION_RADIUS,
    PLAYER_INVULNERABILITY_DURATION,
)

from sound_handling.player import fire_sound, thrust_sound

from core.upgrades_config import UPGRADE_TRACKS


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

        self.bullet_damage = 10

        # Health / collision
        self.max_health = PLAYER_MAX_HEALTH
        self.health = self.max_health

        self.radius = PLAYER_COLLISION_RADIUS

        self.invulnerable_timer = 0.0

        # Progression
        self.credits = 0

        self.parts = []

        self.upgrade_levels = {
            key: 0
            for key in UPGRADE_TRACKS
        }

        self.thrust_channel = pygame.mixer.Channel(0)

    def get_forward_direction(self):

        return pygame.Vector2(
            math.cos(math.radians(self.angle)),
            math.sin(math.radians(self.angle))
        )

    def rotate(self, amount):

        self.angle += amount * self.rotation_speed

    def thrust(self):

        if not self.thrust_channel.get_busy():
            self.thrust_channel.play(thrust_sound, loops=-1)

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
        fire_sound.play()
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

    # ------------------------------------------------------
    # Progression
    # ------------------------------------------------------

    def add_credits(self, amount):

        self.credits += amount

    def add_part(self, part_data):

        self.parts.append(part_data)


    # ------------------------------------------------------
    # Upgrades
    # ------------------------------------------------------

    def get_upgrade_summary(self):

        summary = []

        for key, track in UPGRADE_TRACKS.items():

            level = self.upgrade_levels[key]

            max_level = track["max_level"]

            maxed = level >= max_level

            cost = (
                None
                if maxed
                else self._get_upgrade_cost(key, level)
            )

            summary.append(
                {
                    "key": key,
                    "label": track["label"],
                    "level": level,
                    "max_level": max_level,
                    "cost": cost,
                    "maxed": maxed,
                }
            )

        return summary

    def _get_upgrade_value(self, track_key, level):

        track = UPGRADE_TRACKS[track_key]

        return (
            track["base_value"]
            * (track["value_multiplier"] ** level)
        )

    def _get_upgrade_cost(self, track_key, level):

        track = UPGRADE_TRACKS[track_key]

        return round(
            track["base_cost"]
            * (track["cost_multiplier"] ** level)
        )

    def purchase_upgrade(self, track_key):

        track = UPGRADE_TRACKS.get(track_key)

        if track is None:

            return False

        level = self.upgrade_levels[track_key]

        if level >= track["max_level"]:

            # Already maxed out.
            return False

        cost = self._get_upgrade_cost(
            track_key,
            level
        )

        if self.credits < cost:

            return False

        self.credits -= cost

        # Value at the level we're upgrading INTO.
        value = self._get_upgrade_value(
            track_key,
            level + 1
        )

        if track_key == "fire_rate":

            self.bullet_interval = value

        elif track_key == "bullet_damage":

            self.bullet_damage = round(value)

        elif track_key == "max_health":

            increase = value - self.max_health

            self.max_health = round(value)

            self.health += increase

        self.upgrade_levels[track_key] += 1

        return True

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