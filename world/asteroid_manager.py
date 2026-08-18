import random

import pygame

from entities.asteroid import Asteroid
from entities.bullet import Bullet
from entities.missile import Missile

from sound_handling.player import hit_sound
from sound_handling.asteroid import (
    asteroid_impact_sound,
    asteroid_destroy_sound,
)


class AsteroidManager:

    # --------------------------------------------------
    # Procedural generation settings
    # --------------------------------------------------

    CHUNK_SIZE = 2000

    ACTIVE_CHUNK_RADIUS = 1

    ASTEROIDS_PER_CHUNK = 80


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

        # Chunks that have already been generated.
        self.generated_chunks = set()

        # Procedural asteroids destroyed by the player.
        self.destroyed_asteroids = set()

        # Spatial grid for collision detection.
        self.collision_grid = {}

        self.update_sector_configuration()


    # ==================================================
    # SECTOR CONFIGURATION
    # ==================================================

    def update_sector_configuration(self):

        self.sector_radius = (
            self.sector_manager.radius
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

        self.collision_grid_cell_size = 220


    # ==================================================
    # CHUNKS
    # ==================================================

    def get_chunk(
        self,
        position,
    ):

        return (
            int(
                position.x
                // self.CHUNK_SIZE
            ),
            int(
                position.y
                // self.CHUNK_SIZE
            ),
        )


    def get_chunk_seed(
        self,
        chunk,
    ):

        x, y = chunk

        # Unique but deterministic seed for this chunk.
        return (
            self.sector_manager.current_sector * 1000003
            + x * 73856093
            + y * 19349663
        )


    # ==================================================
    # GENERATE CHUNK
    # ==================================================

    def generate_chunk(
        self,
        chunk,
    ):

        if chunk in self.generated_chunks:

            return

        self.generated_chunks.add(
            chunk
        )

        rng = random.Random(
            self.get_chunk_seed(chunk)
        )

        chunk_x, chunk_y = chunk

        start_x = (
            chunk_x * self.CHUNK_SIZE
        )

        start_y = (
            chunk_y * self.CHUNK_SIZE
        )

        for index in range(
            self.ASTEROIDS_PER_CHUNK
        ):

            x = rng.uniform(
                start_x,
                start_x + self.CHUNK_SIZE
            )

            y = rng.uniform(
                start_y,
                start_y + self.CHUNK_SIZE
            )

            position = pygame.Vector2(
                x,
                y
            )

            # Don't generate outside the circular sector.
            if (
                position.length_squared()
                > self.sector_radius ** 2
            ):

                continue

            size = rng.choices(
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

            asteroid_id = (
                chunk,
                index
            )

            if asteroid_id in (
                self.destroyed_asteroids
            ):

                continue

            asteroid_seed = (
                self.get_chunk_seed(chunk)
                + index
            )

            asteroid = Asteroid(
                position,
                size,
                asteroid_seed,
            )

            asteroid.procedural_id = (
                asteroid_id
            )

            self.asteroids.append(
                asteroid
            )


    # ==================================================
    # LOAD NEARBY CHUNKS
    # ==================================================

    def load_nearby_chunks(self):

        player_chunk = self.get_chunk(
            self.player.position
        )

        needed_chunks = set()

        for x in range(
            player_chunk[0]
            - self.ACTIVE_CHUNK_RADIUS,

            player_chunk[0]
            + self.ACTIVE_CHUNK_RADIUS
            + 1,
        ):

            for y in range(
                player_chunk[1]
                - self.ACTIVE_CHUNK_RADIUS,

                player_chunk[1]
                + self.ACTIVE_CHUNK_RADIUS
                + 1,
            ):

                chunk = (
                    x,
                    y
                )

                needed_chunks.add(
                    chunk
                )

                self.generate_chunk(
                    chunk
                )

        # Remove asteroids from chunks that are now
        # too far away.
        self.asteroids = [
            asteroid
            for asteroid in self.asteroids
            if (
                asteroid.procedural_id is None
                if hasattr(
                    asteroid,
                    "procedural_id"
                )
                else False
            )
            or self.is_chunk_active(
                asteroid.procedural_id[0],
                needed_chunks
            )
        ]


    def is_chunk_active(
        self,
        chunk,
        active_chunks,
    ):

        return chunk in active_chunks


    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        self.load_nearby_chunks()

        for asteroid in self.asteroids:
            asteroid.update()

        self._rebuild_collision_grid()


    # ==================================================
    # SPATIAL GRID
    # ==================================================

    def _grid_key(
        self,
        position,
    ):

        return (
            int(
                position.x
                // self.collision_grid_cell_size
            ),
            int(
                position.y
                // self.collision_grid_cell_size
            ),
        )


    def _rebuild_collision_grid(self):

        grid = {}

        for asteroid in self.asteroids:

            key = self._grid_key(
                asteroid.position
            )

            grid.setdefault(
                key,
                []
            ).append(
                asteroid
            )

        self.collision_grid = grid


    def _add_to_collision_grid(
        self,
        asteroid,
    ):

        key = self._grid_key(
            asteroid.position
        )

        self.collision_grid.setdefault(
            key,
            []
        ).append(
            asteroid
        )


    def _remove_from_collision_grid(
        self,
        asteroid,
    ):

        key = self._grid_key(
            asteroid.position
        )

        bucket = self.collision_grid.get(
            key
        )

        if (
            bucket is not None
            and asteroid in bucket
        ):

            bucket.remove(
                asteroid
            )


    def _nearby_asteroids(
        self,
        position,
    ):

        cell_x, cell_y = (
            self._grid_key(position)
        )

        nearby = []

        for dx in (-1, 0, 1):

            for dy in (-1, 0, 1):

                nearby.extend(
                    self.collision_grid.get(
                        (
                            cell_x + dx,
                            cell_y + dy,
                        ),
                        [],
                    )
                )

        return nearby


    # ==================================================
    # DAMAGE ASTEROID
    # ==================================================

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
        # Salvage
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
        # Part drop
        # ----------------------------------------------

        if (
            random.random()
            < self.part_drop_chance
        ):

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
        # Remember procedural destruction
        # ----------------------------------------------

        if hasattr(
            asteroid,
            "procedural_id"
        ):

            self.destroyed_asteroids.add(
                asteroid.procedural_id
            )


        # ----------------------------------------------
        # Split
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

                child.velocity += (
                    asteroid.velocity * 0.5
                )

                child.procedural_id = None

                self.asteroids.append(
                    child
                )

                self._add_to_collision_grid(
                    child
                )


        # ----------------------------------------------
        # Remove destroyed asteroid
        # ----------------------------------------------

        if asteroid in self.asteroids:

            self.asteroids.remove(
                asteroid
            )

        self._remove_from_collision_grid(
            asteroid
        )


    # ==================================================
    # POP DROPS
    # ==================================================

    def pop_drops(self):

        drops = self.pending_drops

        self.pending_drops = []

        return drops


    def pop_part_drops(self):

        drops = self.pending_part_drops

        self.pending_part_drops = []

        return drops


    # ==================================================
    # BULLET COLLISION
    # ==================================================

    def check_bullet_collision(
        self,
        bullet,
    ):

        for asteroid in self._nearby_asteroids(
            bullet.position
        ):

            distance = (
                bullet.position
                - asteroid.position
            ).length()

            if distance <= (
                asteroid.radius
                + Bullet.RADIUS
            ):

                self.damage_asteroid(
                    asteroid,
                    self.player.bullet_damage
                )

                asteroid_impact_sound.play()

                return True

        return False


    # ==================================================
    # DRONE SHOT COLLISION
    # ==================================================

    def check_drone_shot_collision(
        self,
        shot,
    ):

        for asteroid in self._nearby_asteroids(
            shot.position
        ):

            distance = (
                shot.position
                - asteroid.position
            ).length()

            if distance <= (
                asteroid.radius
                + shot.RADIUS
            ):

                self.damage_asteroid(
                    asteroid,
                    shot.damage
                )

                asteroid_impact_sound.play()

                return True

        return False


    # ==================================================
    # MISSILE COLLISION
    # ==================================================

    def check_missile_collision(
        self,
        missile,
    ):

        for asteroid in self._nearby_asteroids(
            missile.position
        ):

            distance = (
                missile.position
                - asteroid.position
            ).length()

            if distance <= (
                asteroid.radius
                + Missile.RADIUS
            ):

                self.apply_splash_damage(
                    missile.position,
                    missile.damage,
                    missile.splash_radius,
                )

                return True

        return False


    def apply_splash_damage(
        self,
        position,
        damage,
        splash_radius,
    ):

        affected = [
            asteroid
            for asteroid in self._nearby_asteroids(
                position
            )
            if (
                asteroid.position
                - position
            ).length()
            <= (
                splash_radius
                + asteroid.radius
            )
        ]

        for asteroid in affected:

            if asteroid not in self.asteroids:

                continue

            self.damage_asteroid(
                asteroid,
                damage,
            )

            asteroid_impact_sound.play()


    # ==================================================
    # PLAYER COLLISION
    # ==================================================

    def check_player_collision(
        self,
        player,
    ):

        if not player.is_alive():

            return

        if player.is_invulnerable():

            return

        for asteroid in self._nearby_asteroids(
            player.position
        ):

            distance = (
                player.position
                - asteroid.position
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


    # ==================================================
    # DRAW
    # ==================================================

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