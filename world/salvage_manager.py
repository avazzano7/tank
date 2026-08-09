from entities.salvage import Salvage

from core.settings import (
    SALVAGE_PICKUP_RADIUS,
    SALVAGE_LIFETIME,
)

from sound_handling.salvage import salvage_pickup_sound


class SalvageManager:

    def __init__(self):

        self.pickups = []


    # ======================================================
    # SPAWN
    # ======================================================

    def spawn(self, position, value):

        pickup = Salvage(
            position,
            value,
            pickup_radius=SALVAGE_PICKUP_RADIUS,
            lifetime=SALVAGE_LIFETIME,
        )

        self.pickups.append(
            pickup
        )


    def spawn_from_drops(self, drops):

        for drop in drops:

            self.spawn(
                drop["position"],
                drop["value"],
            )


    # ======================================================
    # UPDATE
    # ======================================================

    def update(self, dt):

        for pickup in self.pickups:

            pickup.update(dt)

        self.pickups = [
            pickup
            for pickup in self.pickups
            if not pickup.is_expired()
        ]


    # ======================================================
    # PLAYER COLLISION
    # ======================================================

    def check_player_collision(self, player):

        remaining = []

        for pickup in self.pickups:

            distance = (
                player.position
                - pickup.position
            ).length()

            if distance <= pickup.pickup_radius:

                player.add_credits(
                    pickup.value
                )

                salvage_pickup_sound.play()

            else:

                remaining.append(
                    pickup
                )

        self.pickups = remaining


    # ======================================================
    # DRAW
    # ======================================================

    def draw(self, screen, camera):

        for pickup in self.pickups:

            pickup.draw(
                screen,
                camera
            )