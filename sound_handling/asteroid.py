import pygame

# Load sound files (and set volume)
asteroid_destroy_sound = pygame.mixer.Sound("assets/sounds/asteroid/destroy.wav")
asteroid_destroy_sound.set_volume(0.5)

asteroid_impact_sound = pygame.mixer.Sound("assets/sounds/asteroid/impact.wav")
asteroid_impact_sound.set_volume(0.9)