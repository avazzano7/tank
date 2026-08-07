import pygame

from world.sector_config import SECTOR_CONFIGS


class SectorManager:

    def __init__(self):

        self.current_sector = 1

        self.config = None

        self.load_sector(
            self.current_sector
        )


    # ==================================================
    # LOAD SECTOR
    # ==================================================

    def load_sector(self, sector_number):

        if sector_number not in SECTOR_CONFIGS:

            raise ValueError(
                f"Sector {sector_number} "
                f"does not exist."
            )

        self.current_sector = sector_number

        self.config = SECTOR_CONFIGS[
            sector_number
        ]


    # ==================================================
    # LOAD NEXT SECTOR
    # ==================================================

    def load_next_sector(self):

        next_sector = (
            self.current_sector + 1
        )

        self.load_sector(
            next_sector
        )


    # ==================================================
    # CONFIGURATION
    # ==================================================

    def get_config(self):

        return self.config


    # ==================================================
    # COMMON PROPERTIES
    # ==================================================

    @property
    def name(self):

        return self.config["name"]


    @property
    def radius(self):

        return self.config["radius"]


    @property
    def outpost_count(self):

        return self.config["outpost_count"]


    @property
    def max_asteroids(self):

        return self.config["max_asteroids"]


    @property
    def asteroid_size_weights(self):

        return self.config[
            "asteroid_size_weights"
        ]


    @property
    def enemy_types(self):

        return self.config[
            "enemy_types"
        ]


    @property
    def enemy_spawn_rate(self):

        return self.config[
            "enemy_spawn_rate"
        ]


    @property
    def boss(self):

        return self.config["boss"]


    # ==================================================
    # SECTOR COMPLETION
    # ==================================================

    def check_sector_completion(
        self,
        player_position
    ):

        distance = (
            pygame.Vector2(
                player_position
            ).length()
        )

        return distance >= self.radius


    # ==================================================
    # PROGRESS
    # ==================================================

    def get_progress(
        self,
        player_position
    ):

        distance = pygame.Vector2(
            player_position
        ).length()

        return (
            distance,
            self.radius
        )