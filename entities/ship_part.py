import math
import random

import pygame

from core.settings import PART_RARITY_COLORS


NAME_POOL = {
    "common": [
        "Scrap Alloy",
        "Circuit Fragment",
        "Broken Coil",
    ],
    "uncommon": [
        "Reinforced Plating",
        "Ion Capacitor",
        "Stabilizer Unit",
    ],
    "rare": [
        "Quantum Core",
        "Voidglass Shard",
        "Overcharged Relay",
    ],
}

RARITY_RADII = {
    "common": 6,
    "uncommon": 8,
    "rare": 11,
}


class ShipPart:

    FADE_WARNING_TIME = 3.0

    def __init__(
        self,
        position,
        rarity,
        pickup_radius=40,
        lifetime=12.0,
        name=None,
    ):

        self.position = pygame.Vector2(position)

        self.rarity = rarity

        self.name = (
            name
            or random.choice(
                NAME_POOL.get(rarity, ["Unknown Component"])
            )
        )

        self.pickup_radius = pickup_radius

        self.lifetime = lifetime

        self.age = 0.0

        self.radius = RARITY_RADII.get(
            rarity,
            6,
        )

        self.color = PART_RARITY_COLORS.get(
            rarity,
            (255, 255, 255),
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

        sides = 6

        points = []

        for i in range(sides):

            a = math.radians(
                self.rotation
                + (360 / sides) * i
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
            self.color,
            points,
            2,
        )