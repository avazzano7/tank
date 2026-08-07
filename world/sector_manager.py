import pygame

from core.settings import SECTOR_RADIUS


class SectorManager:

    def __init__(self):

        self.current_sector = 1

        self.radius = SECTOR_RADIUS


    def check_sector_completion(self, player_position):

        distance = player_position.length()


        if distance >= self.radius:

            return True


        return False



    def load_next_sector(self):

        self.current_sector += 1


        # Temporary scaling
        self.radius *= 2



    def get_progress(self, player_position):

        distance = player_position.length()


        return distance, self.radius