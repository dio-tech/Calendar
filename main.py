import os
import pygame

# ------------------------------------------
os.system('git add .')
os.system('git commit -m "Initial Commit"')
os.system('git push')
# ------------------------------------------

WIDTH = 750, 750
WIN = pygame.display.set_mode((WIDTH, WIDTH))

def main(win, width):
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

main(WIN, WIDTH)

