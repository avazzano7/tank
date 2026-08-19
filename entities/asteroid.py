import math
import random

import pygame


class Asteroid:

    SIZES = {
        "galactal": {
            "radius": 100,
            "health": 50,
            "speed_min": 0.1,
            "speed_max": 0.7,
            "points_min": 15,
            "points_max": 25,
            "contact_damage": 50,
            "salvage_min": 25,
            "salvage_max": 35,
        },
        "large": {
            "radius": 55,
            "health": 30,
            "speed_min": 0.4,
            "speed_max": 1.2,
            "points_min": 9,
            "points_max": 13,
            "contact_damage": 34,
            "salvage_min": 15,
            "salvage_max": 25,
        },

        "medium": {
            "radius": 32,
            "health": 15,
            "speed_min": 0.6,
            "speed_max": 1.8,
            "points_min": 8,
            "points_max": 11,
            "contact_damage": 20,
            "salvage_min": 8,
            "salvage_max": 14,
        },

        "small": {
            "radius": 18,
            "health": 5,
            "speed_min": 0.8,
            "speed_max": 2.5,
            "points_min": 7,
            "points_max": 9,
            "contact_damage": 12,
            "salvage_min": 3,
            "salvage_max": 6,
        },
    }

    SPLIT_MAP = {
        "galactal": "large",
        "large": "medium",
        "medium": "small",
        "small": None,
    }


    def __init__(
        self,
        position,
        size="large",
        seed=None,
    ):

        self.position = pygame.Vector2(
            position
        )

        self.size = size

        data = self.SIZES[size]

        # Use a private random generator when a seed
        # is provided. This makes procedural asteroids
        # deterministic without affecting the rest
        # of the game.
        rng = random.Random(seed)

        self.radius = data["radius"]
        self.health = data["health"]
        self.contact_damage = data["contact_damage"]

        self.salvage_min = data["salvage_min"]
        self.salvage_max = data["salvage_max"]


        # --------------------------------------------------
        # Movement
        # --------------------------------------------------

        angle = rng.uniform(
            0,
            math.pi * 2
        )

        speed = rng.uniform(
            data["speed_min"],
            data["speed_max"]
        )

        self.velocity = pygame.Vector2(
            math.cos(angle),
            math.sin(angle)
        ) * speed


        # --------------------------------------------------
        # Rotation
        # --------------------------------------------------

        self.rotation = rng.uniform(
            0,
            360
        )

        self.rotation_speed = rng.uniform(
            -1.5,
            1.5
        )


        # --------------------------------------------------
        # Shape
        # --------------------------------------------------

        point_count = rng.randint(
            data["points_min"],
            data["points_max"]
        )

        self.points = []

        for i in range(point_count):

            angle = (
                math.pi * 2
                / point_count
                * i
            )

            distance = rng.uniform(
                self.radius * 0.75,
                self.radius
            )

            self.points.append(
                pygame.Vector2(
                    math.cos(angle) * distance,
                    math.sin(angle) * distance,
                )
            )


    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        self.position += self.velocity

        self.rotation += self.rotation_speed


    # ==================================================
    # DAMAGE
    # ==================================================

    def take_damage(
        self,
        amount,
    ):

        self.health -= amount

        return self.health <= 0


    # ==================================================
    # GET SPLIT SIZE
    # ==================================================

    def get_split_size(self):

        return self.SPLIT_MAP[
            self.size
        ]


    # ==================================================
    # DRAW
    # ==================================================

    def draw(
        self,
        screen,
        camera,
    ):

        screen_position = (
            self.position - camera
        )

        rotated_points = []

        for point in self.points:

            rotated = point.rotate(
                self.rotation
            )

            rotated_points.append(
                screen_position + rotated
            )

        pygame.draw.polygon(
            screen,
            (130, 130, 130),
            rotated_points,
            2
        )