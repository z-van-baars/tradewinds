import pygame

pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
pygame.init()

click = pygame.mixer.Sound('sound/click.wav')
chime = pygame.mixer.Sound('sound/chime.wav')
