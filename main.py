import os
import pygame
from datetime import datetime as dt
from buttons import *
import math
from tkinter import *
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column
pygame.init()

# ------------------------------------------
os.system('git add .')
os.system('git commit -m "Initial Commit"')
os.system('git push')
# ------------------------------------------

WIDTH = 750
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('Calendar')

actual_year = dt.now().year
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
# DAYS ARE IN THE ORDER OF MONTHS
days_of_month = [31, [28, 29], 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
BLOCK_SIZE = 100
leap_year = 2016
START = []
TEXTS = [[actual_year, [[[['', (_+1+(x*6))] for _ in range(6)] for x in range(7)] for __ in range(12)]]]


engine = create_engine('sqlite:///notes.db', echo = True)

meta = MetaData()

notes = Table(
    'notes', meta,
    Column('id', Integer, primary_key=True),
    Column('text_id', Integer),
    Column('row', Integer),
    Column('col', Integer),
    Column('month_index', Integer),
    Column('year', Integer),
    Column('notes', String)
)

meta.create_all(engine)
conn = engine.connect()


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
        self.selected = False
        for date in TEXTS:
            if date[0] == self.year:
                self.text = date[1][self.month_index][row][col][0]
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x+1, self.y+1, self.block_size-1, self.block_size-1))
        if len(list(self.text)) != 0:
            blit_text(win, 20, 'Note', (0, 0, 0), self.x + self.block_size//2, self.y + self.block_size//2)


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
        self.sel = []
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
    
    def restart_selected(self):
        for i in range(6):
            for j in range(7):
                if self.grid[j][i] != 0:
                    self.grid[j][i].selected = False
    
    def selected(self, row, col, sel):
        if (row, col) != (-1, -1):
            self.restart_selected()
            if len(sel) > 0:
                sel.remove(sel[0])
            sel.append([self.start_x + (row * self.block_size), self.start_y + (col * self.block_size)])
            self.grid[row][col].selected = True


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

def read_notes(year, month_index, row, col):
    r = Tk()
    r.state('zoomed')
    r.title('Read Notes')
    label = Label(r, text='No notes')
    for date in TEXTS:
        if date[0] == year:
            if date[1][month_index][row][col][0] != '':
                label = Label(r, text=date[1][month_index][row][col][0])
    label.pack()
    r.mainloop()

def get_input(entry, year, month_index, row, col, r):
    txt =  entry.get()
    list = []
    list.append(txt)
    for date in TEXTS:
        if date[0] == year:
            date[1][month_index][row][col][0] = list[0]
            ins = notes.insert().values(text_id=date[1][month_index][row][col][1], row=row, col=col, month_index=month_index, year=year, notes=list[0])
            conn.execute(ins)
            r.destroy()

def add_notes(year, month_index, row, col):
    r = Tk()
    r.state('zoomed')
    r.title('Add notes')
    label = Label(r, text='Add Notes')
    label.pack(padx=15, pady=20)
    en = Entry(r)
    en.pack()
    btn = Button(r, text='Add Note', command=lambda :get_input(en, year, month_index, row, col, r))
    if year < dt.now().year:
        btn['state'] = 'disabled'
    btn.pack(padx=10, pady=10)

def clear_notes(year, month_index, row, col, root):
    for date in TEXTS:
        if date[0] == year:
            date[1][month_index][row][col][0] = ''
            s = notes.delete().where(notes.c.text_id == date[1][month_index][row][col][1])
            conn.execute(s)
    root.destroy()

def update_texts(year):
    s = notes.select().where(notes.c.year > year)
    result = conn.execute(s)
    years = []
    for row in result:
        if row.year in years:
            pass
        else:
            years.append(row.year)
    for yearss in years:
        TEXTS.append([yearss, [[[['', (_+1+(x*6))] for _ in range(6)] for x in range(7)] for __ in range(12)]])
    for date in TEXTS:
        s = notes.select().where(notes.c.year == date[0])
        result = conn.execute(s)
        for row in result:
            date[1][row.month_index][row.row][row.col][0] = row.notes
            
def redraw_window(win, width, month_index, year, square, sel, after_click):
    win.fill((255, 255, 255))
    draw_name_month(win, width, months[month_index])
    blit_text(win, 30, f"Year: {str(year)}", (0, 0, 0), 630, 650)
    square.draw(win)

    for row in square.grid:
        for spot in row:
            if spot != 0:
                spot.draw(win)
    
    if len(after_click) == 1:
        if len(sel) > 0:
            blit_text(win, 30, 'Right Click to notes management', (0, 0, 255), 10, 10)
    
    for i in range(len(sel)):
        pygame.draw.rect(win, (0, 0, 255), (sel[i][0], sel[i][1], square.block_size, square.block_size), 2)
    
    square.blit_days(win)

def add_birthday(year, month_index, square):
    # FIX THIS
    for date in TEXTS:
        pass

def main(win, width):
    run = True
    month_index = dt.now().month - 1
    year = dt.now().year
    sel = []
    after_click = []
    mass_selection = []
    update_texts(year)

    while run:
        changed = False
        square = Square(month_index, BLOCK_SIZE, year)
        pos = pygame.mouse.get_pos()

        redraw_window(win, width, month_index, year, square, sel, after_click)

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
                        changed = True
                elif initial_x_b <= clicked_pos[0] <= final_x_b:
                    if initial_y_b <= clicked_pos[1] <= final_y_b:
                        month_index -= 1
                        changed = True
                        START[0] = square.get_start_day_previous_month()
                if not changed:
                    sel.clear()
                    row, col = get_click(clicked_pos, square)
                    square.selected(row, col, sel)
                    for date in TEXTS:
                        if date[0] == year:
                            if (row, col) != (-1, -1):
                                after_click.append(1)
                                if square.grid[row][col].selected:
                                    if pygame.mouse.get_pressed()[2]:
                                        root = Tk()
                                        root.state('zoomed')
                                        root.title('Notes management')
                                        button1 = tkinter_buttons(root, 'Read Notes', 5, 25, lambda:read_notes(year, month_index, row, col))
                                        button1.pack(padx=15, pady=20)
                                        button2 = tkinter_buttons(root, 'Add Notes', 5, 25, lambda:add_notes(year, month_index, row, col))
                                        button2.pack(padx=15, pady=20)
                                        button3 = tkinter_buttons(root, 'Clear Notes', 5, 25, lambda:clear_notes(year, month_index, row, col, root))
                                        button3.pack(padx=15, pady=20)
                                        root.mainloop()
                                        sel.clear()
                                        after_click.clear()
                else:
                    sel.clear()
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    poss = pygame.mouse.get_pos()
                    row, col = get_click(poss, square)
                    mass_selection.append([row, col])
        
        if month_index > 11:
            month_index = 0
            year += 1
            check = []
            for date in TEXTS:
                if date[0] == year:
                    check.append(1)
            if len(check) == 0:
                TEXTS.append([year, [[[['', (_+1+(x*6))] for _ in range(6)] for x in range(7)] for __ in range(12)]])
        elif month_index < 0:
            month_index = 11
            year -= 1
            check = []
            for date in TEXTS:
                if date[0] == year:
                    check.append(1)
            if len(check) == 0:
                TEXTS.append([year, [[[['', (_+1+(x*6))] for _ in range(6)] for x in range(7)] for __ in range(12)]])
        add_birthday(year, month_index, square)
        if len(after_click) == 2:
            after_click.remove(after_click[0])
        
        pygame.display.update()

main(WIN, WIDTH)

