import math
import random

import pygame

from entities.asteroid import Asteroid


class AsteroidManager:

    def __init__(
        self,
        player,
        sector_radius,
    ):

        self.player = player
        self.sector_radius = sector_radius

        self.asteroids = []

        # --------------------------------------------------
        # Sector Asteroid Configuration
        # --------------------------------------------------

        self.max_asteroids = 30

        self.min_spawn_distance = 500

        self.edge_margin = 150

        # Probability of each initial asteroid size
        self.size_weights = {
            "large": 0.60,
            "medium": 0.30,
            "small": 0.10,
        }

        # --------------------------------------------------
        # Initial Population
        # --------------------------------------------------

        self.populate()


    # ======================================================
    # POPULATION
    # ======================================================

    def populate(self):

        while len(self.asteroids) < self.max_asteroids:

            asteroid = self.create_random_asteroid()

            if asteroid is not None:

                self.asteroids.append(
                    asteroid
                )


    # ======================================================
    # CREATE ASTEROID
    # ======================================================

    def create_random_asteroid(self):

        position = self.get_random_position()

        if position is None:

            return None


        size = random.choices(
            population=[
                "large",
                "medium",
                "small",
            ],
            weights=[
                self.size_weights["large"],
                self.size_weights["medium"],
                self.size_weights["small"],
            ],
            k=1,
        )[0]


        return Asteroid(
            position,
            size
        )


    # ======================================================
    # RANDOM POSITION
    # ======================================================

    def get_random_position(self):

        for _ in range(50):

            angle = random.uniform(
                0,
                math.pi * 2
            )

            # Leave room around the outer edge.
            max_distance = (
                self.sector_radius
                - self.edge_margin
            )

            if max_distance <= self.min_spawn_distance:

                return None


            distance = random.uniform(
                self.min_spawn_distance,
                max_distance
            )


            position = (
                pygame.Vector2(
                    math.cos(angle),
                    math.sin(angle)
                )
                * distance
            )


            # Make sure the asteroid isn't too close
            # to another asteroid.
            if self.is_position_clear(
                position
            ):

                return position


        return None


    # ======================================================
    # POSITION VALIDATION
    # ======================================================

    def is_position_clear(
        self,
        position,
        minimum_distance=150,
    ):

        # Don't spawn too close to the player.
        if (
            position.distance_to(
                self.player.position
            )
            < self.min_spawn_distance
        ):

            return False


        # Don't overlap another asteroid.
        for asteroid in self.asteroids:

            if (
                position.distance_to(
                    asteroid.position
                )
                < minimum_distance
            ):

                return False


        return True


    # ======================================================
    # UPDATE
    # ======================================================

    def update(self):

        for asteroid in self.asteroids:

            asteroid.update()


    # ======================================================
    # DAMAGE
    # ======================================================

    def damage_asteroid(
        self,
        asteroid,
        damage,
    ):

        destroyed = asteroid.take_damage(
            damage
        )


        if not destroyed:

            return


        # ----------------------------------------------
        # Split asteroid
        # ----------------------------------------------

        split_size = (
            asteroid.get_split_size()
        )


        if split_size is not None:

            for _ in range(2):

                child = Asteroid(
                    asteroid.position,
                    split_size
                )

                # Give the children some of the parent's
                # momentum.
                child.velocity += (
                    asteroid.velocity * 0.5
                )

                self.asteroids.append(
                    child
                )


        # Remove destroyed asteroid.

        if asteroid in self.asteroids:

            self.asteroids.remove(
                asteroid
            )


    # ======================================================
    # BULLET COLLISIONS
    # ======================================================

    def check_bullet_collision(
        self,
        bullet,
    ):

        for asteroid in self.asteroids:

            distance = (
                bullet.position -
                asteroid.position
            ).length()


            if distance <= (
                asteroid.radius +
                bullet.RADIUS
            ):

                self.damage_asteroid(
                    asteroid,
                    10
                )

                return True


        return False


    # ======================================================
    # MAINTAIN POPULATION
    # ======================================================

    def maintain_population(self):

        while len(self.asteroids) < self.max_asteroids:

            asteroid = self.create_random_asteroid()

            if asteroid is not None:

                self.asteroids.append(
                    asteroid
                )

            else:

                break


    # ======================================================
    # DRAW
    # ======================================================

    def draw(
        self,
        screen,
        camera,
    ):

        for asteroid in self.asteroids:

            asteroid.draw(
                screen,
                camera
            )