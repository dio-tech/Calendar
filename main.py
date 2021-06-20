import os
import pygame
from datetime import datetime as dt
from buttons import *
pygame.init()

# ------------------------------------------
os.system('git add .')
os.system('git commit -m "Initial Commit"')
os.system('git push')
# ------------------------------------------

WIDTH = 750
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('Calendar')

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
# DAYS ARE IN THE ORDER OF MONTHS
days_of_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
BLOCK_SIZE = 100


class Square:
    def __init__(self, month_index, block_size):
        self.block_size = block_size
        self.start_x = 30
        self.start_y = 140
        self.month_index = month_index
        self.month = months[self.month_index]
        self.days = days_of_month[self.month_index]
    
    def draw(self, win):
        # NEED TO MAKE IT START IN THE RIGHT DAY OF THE WEEK
        week = ['S', 'M', 'T', 'W', 'T', 'F', 'S']
        self.blit_days(win)
        for i in range(len(week)):
            draw_names_of_weekend(win, week[i], self.start_x + (i*self.block_size) + self.block_size//2-10)
            for j in range(self.days//len(week)):
                pygame.draw.rect(win, (255, 0, 0), (self.start_x + (i*self.block_size), self.start_y + (j*self.block_size),
                            self.block_size, self.block_size), 2)
                for left in range(self.days%len(week)):
                    pygame.draw.rect(win, (255, 0, 0), (self.start_x + (left*self.block_size),
                            self.start_y + ((self.days//len(week))*self.block_size), self.block_size, self.block_size), 2)
    
    def blit_days(self, win):
        j = self.start_y+5
        counter = 0
        for i in range(self.days):
            x = self.start_x+10 + (counter*self.block_size)
            if x > 720:
                j += self.block_size
                counter = 0
            x = self.start_x+10 + (counter*self.block_size)
            blit_text(win, 40, str(int(i+1)), (0, 0, 0), x, j)
            counter += 1

def blit_text(win, size, txt, color, x, y):
    font = pygame.font.SysFont('comicsans', size)
    text = font.render(txt, True, color)
    win.blit(text, (x, y))

def draw_name_month(win, width, txt):
    font = pygame.font.SysFont('comicsans', 80)
    text = font.render(txt, True, (0, 0, 0))
    win.blit(text, (width//2 - text.get_width()//2, 30))

def draw_names_of_weekend(win, txt, x):
    font = pygame.font.SysFont('comicsans', 50)
    text = font.render(txt, True, (0, 0, 0))
    win.blit(text, (x, 100))

def redraw_window(win, width, month_index, year):
    win.fill((255, 255, 255))
    draw_name_month(win, width, months[month_index])
    blit_text(win, 30, f"Year: {str(year)}", (0, 0, 0), 630, 650)

def main(win, width):
    run = True
    month_index = dt.now().month - 1
    year = dt.now().year

    while run:
        square = Square(month_index, BLOCK_SIZE)
        pos = pygame.mouse.get_pos()

        redraw_window(win, width, month_index, year)
        square.draw(win)

        # BUTTONS
        initial_x_f, final_x_f, initial_y_f, final_y_f = forward_button(win, pos, width)
        initial_x_b, final_x_b, initial_y_b, final_y_b = back_button(win, pos, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_pos = pygame.mouse.get_pos()
                if initial_x_f <= clicked_pos[0] <= final_x_f:
                    if initial_y_f <= clicked_pos[1] <= final_y_f:
                        month_index += 1
                if initial_x_b <= clicked_pos[0] <= final_x_b:
                    if initial_y_b <= clicked_pos[1] <= final_y_b:
                        month_index -= 1
        
        if month_index > 11:
            month_index = 0
            year += 1
        elif month_index < 0:
            month_index = 11
            year -= 1
        
        pygame.display.update()

main(WIN, WIDTH)

