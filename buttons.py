import pygame
pygame.init()

def forward_button(win, pos, width):
    font = pygame.font.SysFont('comicsans', 100)
    if width//2 + 160 <= pos[0] <= width//2 + 160 + 120:
        if 685 <= pos[1] <= 685 + 50:
            pygame.draw.rect(win, (255, 0, 0), (width//2 + 160, 685, 120, 50))
    text = font.render('>', True, (0, 0, 0))
    win.blit(text, (width//2 + 200, 670))
    return width//2 + 160, width//2 + 160 + 120, 685, 685 + 50

def back_button(win, pos, width):
    font = pygame.font.SysFont('comicsans', 100)
    text = font.render('<', True, (0, 0, 0))
    if width//2 - 160 - 80 <= pos[0] <= width//2 - 160 - 80 + 120:
        if 685 <= pos[1] <= 685 + 50:
            pygame.draw.rect(win, (255, 0, 0), (width//2 - 160 - 80, 685, 120, 50))
    win.blit(text, (width//2 - 200, 670))
    return width//2 - 160 - 80, width//2 - 160 - 80 + 120, 685, 685 + 50