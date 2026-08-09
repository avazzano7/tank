import math
import random

import pygame

from entities.asteroid import Asteroid
from entities.bullet import Bullet

from sound_handling.player import hit_sound
from sound_handling.asteroid import asteroid_impact_sound, asteroid_destroy_sound


class AsteroidManager:

    def __init__(
        self,
        player,
        sector_manager,
    ):

        self.player = player

        self.sector_manager = sector_manager

        self.asteroids = []

        self.pending_drops = []

        self.pending_part_drops = []

        # --------------------------------------------------
        # Read current sector configuration
        # --------------------------------------------------

        self.update_sector_configuration()

        # --------------------------------------------------
        # Populate sector
        # --------------------------------------------------

        self.populate()


    # ======================================================
    # SECTOR CONFIGURATION
    # ======================================================

    def update_sector_configuration(self):

        self.sector_radius = (
            self.sector_manager.radius
        )

        self.max_asteroids = (
            self.sector_manager.max_asteroids
        )

        self.size_weights = (
            self.sector_manager
            .asteroid_size_weights
        )

        self.part_drop_chance = (
            self.sector_manager
            .part_drop_chance
        )

        self.part_rarity_weights = (
            self.sector_manager
            .part_rarity_weights
        )

        # Don't spawn directly around the player.
        self.min_spawn_distance = 500

        # Keep asteroids slightly inside the boundary.
        self.edge_margin = 150


    # ======================================================
    # POPULATION
    # ======================================================

    def populate(self):

        attempts = 0

        max_attempts = (
            self.max_asteroids * 10
        )

        while (
            len(self.asteroids)
            < self.max_asteroids
            and attempts < max_attempts
        ):

            asteroid = (
                self.create_random_asteroid()
            )

            if asteroid is not None:

                self.asteroids.append(
                    asteroid
                )

            attempts += 1


    # ======================================================
    # CREATE RANDOM ASTEROID
    # ======================================================

    def create_random_asteroid(self):

        position = (
            self.get_random_position()
        )

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

        max_distance = (
            self.sector_radius
            - self.edge_margin
        )

        if (
            max_distance
            <= self.min_spawn_distance
        ):

            return None


        for _ in range(50):

            angle = random.uniform(
                0,
                math.pi * 2
            )

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

        # Don't spawn directly on player.

        if (
            position.distance_to(
                self.player.position
            )
            < self.min_spawn_distance
        ):

            return False


        # Don't stack asteroids on top of each other.

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
    # DAMAGE ASTEROID
    # ======================================================

    def damage_asteroid(
        self,
        asteroid,
        damage,
    ):

        destroyed = (
            asteroid.take_damage(
                damage
            )
        )


        if not destroyed:

            return

        asteroid_destroy_sound.play()


        # ----------------------------------------------
        # Record salvage drop (guaranteed)
        # ----------------------------------------------

        salvage_value = random.randint(
            asteroid.salvage_min,
            asteroid.salvage_max,
        )

        self.pending_drops.append(
            {
                "position": pygame.Vector2(
                    asteroid.position
                ),
                "value": salvage_value,
            }
        )


        # ----------------------------------------------
        # Record ship part drop (chance-based)
        # ----------------------------------------------

        if random.random() < self.part_drop_chance:

            rarity = random.choices(

                population=list(
                    self.part_rarity_weights.keys()
                ),

                weights=list(
                    self.part_rarity_weights.values()
                ),

                k=1,
            )[0]

            self.pending_part_drops.append(
                {
                    "position": pygame.Vector2(
                        asteroid.position
                    ),
                    "rarity": rarity,
                }
            )


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

                # Give children some of the parent's
                # momentum.

                child.velocity += (
                    asteroid.velocity * 0.5
                )

                self.asteroids.append(
                    child
                )


        # ----------------------------------------------
        # Remove destroyed asteroid
        # ----------------------------------------------

        if asteroid in self.asteroids:

            self.asteroids.remove(
                asteroid
            )


    # ======================================================
    # POP DROPS
    # ======================================================

    def pop_drops(self):

        drops = self.pending_drops

        self.pending_drops = []

        return drops


    def pop_part_drops(self):

        drops = self.pending_part_drops

        self.pending_part_drops = []

        return drops


    # ======================================================
    # BULLET COLLISION
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
                asteroid.radius
                + Bullet.RADIUS
            ):

                self.damage_asteroid(
                    asteroid,
                    10
                )

                asteroid_impact_sound.play()

                return True


        return False


    # ======================================================
    # PLAYER COLLISION
    # ======================================================

    def check_player_collision(
        self,
        player,
    ):

        if not player.is_alive():

            return

        if player.is_invulnerable():

            return


        for asteroid in self.asteroids:

            distance = (
                player.position -
                asteroid.position
            ).length()


            if distance <= (
                asteroid.radius
                + player.radius
            ):

                player.take_damage(
                    asteroid.contact_damage
                )

                hit_sound.play()

                return


    # ======================================================
    # MAINTAIN POPULATION
    # ======================================================

    def maintain_population(self):

        attempts = 0

        while (
            len(self.asteroids)
            < self.max_asteroids
            and attempts < 10
        ):

            asteroid = (
                self.create_random_asteroid()
            )

            if asteroid is not None:

                self.asteroids.append(
                    asteroid
                )

            attempts += 1


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