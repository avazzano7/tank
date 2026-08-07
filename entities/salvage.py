import math
import random

import pygame

from core.settings import (
    TECHNO_GREEN,
    SALVAGE_MIN_VALUE,
    SALVAGE_MAX_VALUE,
    SALVAGE_MIN_RADIUS,
    SALVAGE_MAX_RADIUS,
)


class Salvage:

    FADE_WARNING_TIME = 3.0

    def __init__(
        self,
        position,
        value,
        pickup_radius=40,
        lifetime=12.0,
    ):

        self.position = pygame.Vector2(position)

        self.value = value

        self.pickup_radius = pickup_radius

        self.lifetime = lifetime

        self.age = 0.0

        # --------------------------------------------------
        # Visual size scales with value
        # --------------------------------------------------

        self.radius = self.get_radius_for_value(
            value
        )

        # --------------------------------------------------
        # Gentle drift
        # --------------------------------------------------

        angle = random.uniform(
            0,
            math.pi * 2
        )

        speed = random.uniform(
            0.1,
            0.4
        )

        self.velocity = pygame.Vector2(
            math.cos(angle),
            math.sin(angle),
        ) * speed

        self.rotation = random.uniform(
            0,
            360
        )

        self.rotation_speed = random.uniform(
            -2,
            2
        )

    # ------------------------------------------------------
    # Radius scaling
    # ------------------------------------------------------

    @staticmethod
    def get_radius_for_value(value):

        value_span = (
            SALVAGE_MAX_VALUE - SALVAGE_MIN_VALUE
        )

        if value_span <= 0:

            return SALVAGE_MIN_RADIUS

        clamped_value = max(
            SALVAGE_MIN_VALUE,
            min(SALVAGE_MAX_VALUE, value),
        )

        t = (
            (clamped_value - SALVAGE_MIN_VALUE)
            / value_span
        )

        radius_span = (
            SALVAGE_MAX_RADIUS - SALVAGE_MIN_RADIUS
        )

        return (
            SALVAGE_MIN_RADIUS
            + radius_span * t
        )

    # ------------------------------------------------------
    # Update
    # ------------------------------------------------------

    def update(self, dt):

        self.position += self.velocity

        self.rotation += self.rotation_speed

        self.age += dt

    def is_expired(self):

        return self.age >= self.lifetime

    def is_fading(self):

        return (
            self.lifetime - self.age
        ) <= self.FADE_WARNING_TIME

    # ------------------------------------------------------
    # Draw
    # ------------------------------------------------------

    def draw(self, screen, camera):

        if self.is_fading():

            flicker_on = (
                int(self.age * 8) % 2 == 0
            )

            if not flicker_on:

                return

        screen_position = (
            self.position - camera
        )

        points = []

        for offset in (0, 90, 180, 270):

            a = math.radians(
                self.rotation + offset
            )

            points.append(
                screen_position
                + pygame.Vector2(
                    math.cos(a),
                    math.sin(a),
                )
                * self.radius
            )

        pygame.draw.polygon(
            screen,
            TECHNO_GREEN,
            points,
            2,
        )