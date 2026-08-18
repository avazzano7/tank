import random

import pygame

from entities.enemy import Enemy
from entities.bullet import Bullet
from entities.missile import Missile


class EnemyManager:

    # ==================================================
    # INITIALIZATION
    # ==================================================

    def __init__(
        self,
        player,
        sector_manager,
    ):

        self.player = player

        self.sector_manager = (
            sector_manager
        )

        self.enemies = []

        # --------------------------------------------------
        # Sector configuration
        # --------------------------------------------------

        self.update_sector_configuration()

        # --------------------------------------------------
        # Spawn timer
        # --------------------------------------------------

        self.spawn_timer = 0.0

        # Spawn enemies away from the player.
        self.min_spawn_distance = 1200

        # Keep enemies inside the sector boundary.
        self.edge_margin = 300


    # ==================================================
    # SECTOR CONFIGURATION
    # ==================================================

    def update_sector_configuration(self):

        self.sector_radius = (
            self.sector_manager.radius
        )

        self.enemy_types = (
            self.sector_manager.enemy_types
        )

        self.enemy_spawn_rate = (
            self.sector_manager.enemy_spawn_rate
        )


    # ==================================================
    # UPDATE
    # ==================================================

    def update(
        self,
        dt,
    ):

        # ----------------------------------------------
        # Spawn timer
        # ----------------------------------------------

        if self.enemy_spawn_rate > 0:

            self.spawn_timer += dt

            if (
                self.spawn_timer
                >= self.enemy_spawn_rate
            ):

                self.spawn_timer = 0.0

                self.spawn_enemy()

        # ----------------------------------------------
        # Update enemies
        # ----------------------------------------------

        for enemy in self.enemies:

            enemy.update(
                dt,
                self.player
            )

        # ----------------------------------------------
        # Remove dead enemies
        # ----------------------------------------------

        self.enemies = [
            enemy
            for enemy in self.enemies
            if enemy.is_alive()
        ]


    # ==================================================
    # SPAWN ENEMY
    # ==================================================

    def spawn_enemy(self):

        if not self.enemy_types:

            return None

        position = (
            self.get_random_spawn_position()
        )

        if position is None:

            return None

        enemy_type = random.choices(
            population=list(
                self.enemy_types.keys()
            ),
            weights=list(
                self.enemy_types.values()
            ),
            k=1,
        )[0]

        enemy = Enemy(
            position,
            enemy_type,
        )

        self.enemies.append(
            enemy
        )

        return enemy


    # ==================================================
    # RANDOM SPAWN POSITION
    # ==================================================

    def get_random_spawn_position(self):

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

            x = random.uniform(
                -max_distance,
                max_distance
            )

            y = random.uniform(
                -max_distance,
                max_distance
            )

            position = pygame.Vector2(
                x,
                y
            )

            # Must be inside the circular sector.
            if (
                position.length_squared()
                > max_distance ** 2
            ):

                continue

            # Must be sufficiently far from player.
            if (
                position.distance_to(
                    self.player.position
                )
                < self.min_spawn_distance
            ):

                continue

            return position

        return None


    # ==================================================
    # PLAYER COLLISION
    # ==================================================

    def check_player_collision(
        self,
        player,
    ):

        for enemy in self.enemies:

            distance = (
                player.position
                - enemy.position
            ).length()

            if distance <= (
                player.radius
                + enemy.radius
            ):

                player.take_damage(
                    enemy.contact_damage
                )

                # Destroy enemy after collision.
                enemy.health = 0

                return True

        return False


    # ==================================================
    # BULLET COLLISION
    # ==================================================

    def check_bullet_collision(
        self,
        bullet,
    ):

        for enemy in self.enemies:

            distance = (
                bullet.position
                - enemy.position
            ).length()

            if distance <= (
                enemy.radius
                + Bullet.RADIUS
            ):

                destroyed = (
                    enemy.take_damage(
                        self.player.bullet_damage
                    )
                )

                return True

        return False


    # ==================================================
    # MISSILE COLLISION
    # ==================================================

    def check_missile_collision(
        self,
        missile,
    ):

        hit = False

        affected = []

        for enemy in self.enemies:

            distance = (
                missile.position
                - enemy.position
            ).length()

            if distance <= (
                missile.splash_radius
                + enemy.radius
            ):

                affected.append(
                    enemy
                )

                hit = True

        for enemy in affected:

            enemy.take_damage(
                missile.damage
            )

        return hit


    # ==================================================
    # DRAW
    # ==================================================

    def draw(
        self,
        screen,
        camera,
    ):

        for enemy in self.enemies:

            enemy.draw(
                screen,
                camera
            )