import pygame
import os
from Identify_Num.constants import *
from Identify_Num.cell import Cell
from Identify_Num.ml.identifier import get_num
from tkinter import Tk
from tkinter import messagebox
import torch

Tk().withdraw()


# Window Management
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screen_width//2-WIDTH//2, screen_height//2-WIDTH//2)
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Identify Num, By: Arjun Sahlot")


def adjust_res(res):
    vals = sorted([int(i) for i in range(1, res*2)], key=lambda x: abs(res - x))
    for val in vals:
        if WIDTH % val == 0:
            return val


def draw_window(win, canvas):
    win.fill(WHITE)
    for row in canvas:
        for cell in row:
            cell.draw(win)


def create_canvas(res):
    canvas = []
    width = WIDTH//res
    for i in range(res):
        canvas.append([])
        for j in range(res):
            canvas[i].append(Cell(i, j, width))

    return canvas


def get_vals(canvas):
    values = []

    for i in range(len(canvas)):
        values.append([])
        for j in range(len(canvas)):
            values[i].append(canvas[i][j].value)

    return torch.tensor(values)


def main(win, width):
    clock = pygame.time.Clock()
    res = adjust_res(RESOLUTION)
    canvas = create_canvas(res)
    pygame.mouse.set_visible(False)
    radius = 30
    
    run = True
    while run:
        clock.tick(FPS)
        draw_window(win, canvas)
        pygame.draw.circle(win, BLACK, pygame.mouse.get_pos(), radius, 3)

        if pygame.mouse.get_pressed()[0]:
            for row in canvas:
                for cell in row:
                    cell.fill(radius, *pygame.mouse.get_pos())

        if pygame.mouse.get_pressed()[2]:
            for row in canvas:
                for cell in row:
                    cell.erase(radius, *pygame.mouse.get_pos())

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                # exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    radius -= 3
                    radius = max(radius, 5)
                if event.button == 5:
                    radius += 3
                    radius = min(radius, 600)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    messagebox.showinfo("Prediction", f"The computer predicted {get_num(get_vals(canvas))}")

        try:
            pygame.display.update()
        except pygame.error:
            pass


main(WINDOW, WIDTH)
