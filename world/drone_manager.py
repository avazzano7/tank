from entities.drone import Drone
from entities.drone_shot import DroneShot

from core.drone_config import DRONE_CONFIG


class DroneManager:

    def __init__(self):

        self.drone = None

        self.shots = []


    # ======================================================
    # SYNC WITH PLAYER PROGRESSION
    # ======================================================

    def sync_with_player(self, player):

        if (
            player.has_drone()
            and self.drone is None
        ):

            self.drone = Drone(
                DRONE_CONFIG["orbit_radius"],
                DRONE_CONFIG["orbit_speed"],
            )


    # ======================================================
    # UPDATE
    # ======================================================

    def update(self, dt, player, asteroids):

        self.sync_with_player(player)

        if self.drone is None:

            return

        self.drone.update_orbit(
            player.position,
            dt,
        )

        self.drone.tick_fire_timer(dt)

        if not self.drone.can_fire():

            return

        target = self._find_nearest_asteroid(
            asteroids
        )

        if target is None:

            return

        direction = (
            target.position - self.drone.position
        )

        if direction.length_squared() == 0:

            return

        direction = direction.normalize()

        stats = player.get_drone_stats()

        self.shots.append(
            DroneShot(
                self.drone.position,
                direction,
                stats["damage"],
            )
        )

        self.drone.reset_fire_timer(
            stats["fire_interval"]
        )


    def _find_nearest_asteroid(self, asteroids):

        nearest = None

        nearest_distance = (
            DRONE_CONFIG["detection_range"]
        )

        for asteroid in asteroids:

            distance = (
                asteroid.position - self.drone.position
            ).length()

            if distance <= nearest_distance:

                nearest = asteroid

                nearest_distance = distance

        return nearest


    # ======================================================
    # DRAW
    # ======================================================

    def draw(self, screen, camera):

        if self.drone is not None:

            self.drone.draw(
                screen,
                camera
            )

        for shot in self.shots:

            shot.draw(
                screen,
                camera
            )