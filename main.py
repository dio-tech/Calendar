import os
import pygame
from datetime import datetime as dt
from buttons import *
import math
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
days_of_month = [31, [28, 29], 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
BLOCK_SIZE = 100
leap_year = 2016
START = []
TEXTS = [[2021, [[['' for _ in range(6)] for x in range(7)] for __ in range(12)]]]


class Spot:
    def __init__(self, row, col, block_size, month_index, year):
        self.row = row
        self.col = col
        self.block_size = block_size
        self.start_x = 30
        self.start_y = 140
        self.x = self.start_x + (self.row * self.block_size)
        self.y = self.start_y + (self.col * self.block_size)
        self.color = (255, 255, 255)
        self.year = year
        self.month_index = month_index
        for date in TEXTS:
            if date[0] == self.year:
                self.text = date[1][self.month_index][row][col]
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x+1, self.y+1, self.block_size-1, self.block_size-1))
        if type(self.text) != list:
            blit_text(win, 20, str(self.text), (0, 0, 0), self.x + self.block_size//2, self.y + self.block_size//2)
        # ITS GOING TO BE A TEXT


class Square:
    def __init__(self, month_index, block_size, year):
        self.year = year
        self.block_size = block_size
        self.start_x = 30
        self.start_y = 140
        self.month_index = month_index
        self.month = months[self.month_index]
        if self.month_index == 1:
            if (leap_year - self.year)%4 == 0:
                self.days = days_of_month[self.month_index][1]
            else:
                self.days = days_of_month[self.month_index][0]
        else:
            self.days = days_of_month[self.month_index]
        self.week = ['S', 'M', 'T', 'W', 'T', 'F', 'S']
        self.end_first_x = self.start_x + (len(self.week) * self.block_size)
        self.end_first_y = self.start_y + ((self.days//len(self.week)) * self.block_size)
        if self.days%len(self.week) != 0:
            self.end_final_y = self.end_first_y + self.block_size
        else:
            self.end_final_y = self.end_first_y
        self.end_final_x = self.start_x + ((self.days%len(self.week)) * self.block_size)
        self.start_day_month = self.get_starting_day()
        self.final_day_month = self.get_final_month_day_week()
        self.grid = self.get_grid()
        self.num_of_last_rows = math.ceil((self.days - (14+len(self.week)-self.start_day_month))/len(self.week))
        self.num_of_rest = (self.days - (14+len(self.week)-self.start_day_month))%len(self.week)
    # PROBLEMS IN GETTING THE DAYS
    
    def get_starting_day(self):
        if len(START) == 0:
            if dt.today().weekday != 6:
                day = dt.today().weekday()+1
            else:
                day = 0
            for _ in range(1, dt.now().day):
                day -= 1
                if day == -1:
                    day = 6
            START.append(day)
        return START[0]
    
    def get_final_month_day_week(self):
        day = self.start_day_month
        for _ in range(self.days):
            day += 1
            if day > len(self.week)-1:
                day = 0
        return day
    
    def get_start_day_previous_month(self):
        day_previous_month = self.start_day_month
        if self.month_index-1 == 1:
            if (leap_year - self.year)%4 == 0:
                for _ in range(days_of_month[self.month_index-1][1]):
                    day_previous_month -= 1
                    if day_previous_month == -1:
                        day_previous_month = 6
            else:
                for _ in range(days_of_month[self.month_index-1][0]):
                    day_previous_month -= 1
                    if day_previous_month == -1:
                        day_previous_month = 6
        else:
            for _ in range(days_of_month[self.month_index-1]):
                day_previous_month -= 1
                if day_previous_month == -1:
                    day_previous_month = 6
        return day_previous_month

    
    def get_grid(self):
        grid = [[0 for _ in range(6)] for x in range(7)]
        # FIRST LINE
        counter = self.start_day_month
        for _ in range(len(self.week) - self.start_day_month):
            spot = Spot(counter, 0, self.block_size, self.month_index, self.year)
            grid[counter][0] = spot
            counter += 1
        # SECOND AND THIRD LINES
        for i in range(len(self.week)):
            for j in range(1, 3):
                spot = Spot(i, j, self.block_size, self.month_index, self.year)
                grid[i][j] = spot
        # THE REST
        difference = self.days - (14+(len(self.week)-self.start_day_month))
        module = difference%len(self.week)
        if module <= 0:
            for i in range(len(self.week)):
                for j in range(3, 3+math.ceil((difference-module)/len(self.week))):
                    spot = Spot(i, j, self.block_size, self.month_index, self.year)
                    grid[i][j] = spot
        if module > 0:
            for i in range(len(self.week)):
                for j in range(3, 3 + (difference//(len(self.week)))):
                    spot = Spot(i, j, self.block_size, self.month_index, self.year)
                    grid[i][j] = spot
            for i in range(module):
                for j in range(3 + (difference//(len(self.week))), 3 + (difference//(len(self.week))) + 1):
                    spot = Spot(i, j, self.block_size, self.month_index, self.year)
                    grid[i][j] = spot
        
        return grid
    
    def draw(self, win):
        for i in range(len(self.week)):
            draw_names_of_weekend(win, self.week[i], self.start_x + (i*self.block_size) + self.block_size//2-10)
        # DRAW CERTAIN SQUARES
        for i in range(7):
            for j in range(2):
                pygame.draw.rect(win, (255, 0, 0), (self.start_x + (i*self.block_size), self.start_y + (j*self.block_size) + self.block_size,
                        self.block_size, self.block_size), 2)
        # DRAW_UNCERTAIN_SQUARES
        for i in range(len(self.week) - self.start_day_month):
            pygame.draw.rect(win, (255, 0, 0), (self.start_x + (self.start_day_month*self.block_size) + (i*self.block_size), self.start_y,
                    self.block_size, self.block_size), 2)
        y = self.start_y + (3*self.block_size)
        counter = 0
        for _ in range(self.days-(14+(len(self.week) - self.start_day_month))):
            if self.start_x + (counter * self.block_size) > 720:
                y += self.block_size
                counter = 0
            pygame.draw.rect(win, (255, 0, 0), (self.start_x + (counter*self.block_size), y, self.block_size, self.block_size), 2)
            counter += 1
    
    def blit_days(self, win):
        j = self.start_y+5
        counter = 0
        day = 1
        # FIRST LINE
        for _ in range(len(self.week) - self.start_day_month):
            x = self.start_x + (self.start_day_month*self.block_size) + (counter*self.block_size) + 10
            blit_text(win, 40, str(day), (0, 0, 0), x, j)
            day += 1
            counter += 1
        counter = 0
        j = self.start_y + self.block_size + 5
        # SECOND AND THIRD LINES
        for _ in range(14):
            x = self.start_x + (counter*self.block_size) + 10
            if x > 720:
                j += self.block_size
                counter = 0
            x = self.start_x + (counter*self.block_size) + 10
            blit_text(win, 40, str(day), (0, 0, 0), x, j)
            day += 1
            counter += 1
        counter = 0
        j = self.start_y + (3*self.block_size)+5
        
        # THE REST
        for _ in range(self.days - day+1):
            x = self.start_x + (counter*self.block_size) + 10
            if x > 720:
                j += self.block_size
                counter = 0
            x = self.start_x + (counter*self.block_size) + 10
            blit_text(win, 40, str(day), (0, 0, 0), x, j)
            day += 1
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

def get_click(pos, square):
    if square.start_x <= pos[0] <= square.end_first_x:
        if square.start_y <= pos[1] <= square.end_final_y + square.block_size:
            div_x = pos[0] - square.start_x
            div_y = pos[1] - square.start_y
            row = div_x // square.block_size
            col = div_y // square.block_size
    
            if square.grid[row][col] != 0:
                return row, col
    
    return -1, -1

def redraw_window(win, width, month_index, year, square):
    win.fill((255, 255, 255))
    draw_name_month(win, width, months[month_index])
    blit_text(win, 30, f"Year: {str(year)}", (0, 0, 0), 630, 650)
    square.draw(win)

    for row in square.grid:
        for spot in row:
            if spot != 0:
                spot.draw(win)
    
    square.blit_days(win)

def add_birthday():
    # CORRECT THIS
    for date in TEXTS:
        date[1][2][3][3] = 'My Birthday'

def main(win, width):
    run = True
    month_index = dt.now().month - 1
    year = dt.now().year

    while run:
        add_birthday()
        square = Square(month_index, BLOCK_SIZE, year)
        pos = pygame.mouse.get_pos()

        redraw_window(win, width, month_index, year, square)

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
                        START[0] = square.final_day_month
                elif initial_x_b <= clicked_pos[0] <= final_x_b:
                    if initial_y_b <= clicked_pos[1] <= final_y_b:
                        month_index -= 1
                        START[0] = square.get_start_day_previous_month()
                else:
                    row, col = get_click(clicked_pos, square)
                    for date in TEXTS:
                        if date[0] == year:
                            date[1][month_index][row][col] = 'This is the way'
        
        if month_index > 11:
            month_index = 0
            year += 1
            check = []
            for date in TEXTS:
                if date[0] == year:
                    check.append(1)
            if len(check) == 0:
                TEXTS.append([year, [[['' for _ in range(6)] for x in range(7)] for __ in range(12)]])
        elif month_index < 0:
            month_index = 11
            year -= 1
            check = []
            for date in TEXTS:
                if date[0] == year:
                    check.append(1)
            if len(check) == 0:
                TEXTS.append([year, [[['' for _ in range(6)] for x in range(7)] for __ in range(12)]])
        
        pygame.display.update()

main(WIN, WIDTH)

