import pygame
from Resources.scripts.Menus import screen #so if display (full/windowed) stays the same
shotgun=True
def gun():
    return 121, "semi-auto", 1, 5, 200, 4
def blit_gun(angle, mainx=295, mainy=215):
    bg = pygame.Surface((100, 100), pygame.SRCALPHA, 32)
    pygame.draw.rect(bg, (0, 0, 0), (55, 6, 31, 39))
    bg = pygame.transform.rotate(bg, angle)
    screen.blit(bg, (mainx - 25, mainy - 25))
    return [(None, (0, 0, 0), (55, 6, 31, 39))]