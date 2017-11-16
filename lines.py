# -*- coding: utf-8 -*-
import pygame
import colorsys
from random import randint
from math import sqrt

size = [1280, 720]
total_lines = 300
save_frames_to_png = False  # So I can post it as a GIF on http://mgz.me


def main():
    pygame.init()
    pygame.display.set_caption('Lines')

    screen_surface = pygame.display.set_mode((size[0], size[1]))
    surface_background = pygame.Surface((size[0], size[1]))
    surface_background.fill((3, 6, 12))

    pygame.font.init()

    draw_line = DrawLine()
    lines = []

    for line in range(total_lines - 1):
        lines.append(draw_line.compose_line())

    running = True
    frame = 0
    while running:

        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                draw_line.randomize_positions()
        if not running:
            break

        if pygame.mouse.get_focused():
            if pygame.mouse.get_pressed()[0]:  # Left Button: add lines while follow mouse cursor
                mouse_position = pygame.mouse.get_pos()
                lines.append(draw_line.compose_line(current_x=mouse_position[0], current_y=mouse_position[1]))
                if len(lines) < total_lines:
                    lines.append(draw_line.compose_line())
            elif pygame.mouse.get_pressed()[1]:  # Middle Button: just move on events capture
                pygame.event.wait()
                lines.append(draw_line.compose_line())
            elif pygame.mouse.get_pressed()[2]:  # Right Button: del lines
                try:
                    del lines[0]
                except IndexError:
                    pass
            else:
                lines.append(draw_line.compose_line())
        else:
            lines.append(draw_line.compose_line())

        my_font = pygame.font.SysFont('Arial', 13)
        _n_lines = "line" if len(lines) == 1 else "lines"
        text_surface = my_font.render("{0} {1}".format(len(lines), _n_lines), False, (255, 255, 255))
        draw_scene(screen_surface, surface_background, text_surface, lines)

        try:
            del lines[0]
        except IndexError:
            pass

        frame += 1
        pygame.display.flip()
        if save_frames_to_png:
            pygame.image.save(screen_surface, "{num:{fill}{width}}.png".format(num=frame, fill='0', width=4))
        pygame.time.wait(8)


def draw_scene(surface, background, text_surface, lines_list):
    surface.blit(background, (0, 0))
    try:
        for _line in lines_list:
            pygame.draw.line(surface, _line.color, _line.start_pos, _line.end_pos, _line.width)
            pygame.draw.circle(surface, _line.color, _line.start_pos, 3)
            pygame.draw.circle(surface, _line.color, _line.end_pos, 3)
    except KeyError:
        pass
    surface.blit(text_surface, (10, 10))


def random_pos(x):
    return randint(1, x - 1)


def random_start_positions():
    x = size[0]
    y = size[1]
    return (random_pos(x), random_pos(y)), (random_pos(x), random_pos(y))


class Line(object):

    def __init__(self, start_pos, end_pos, color, width):
        object.__init__(self)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.width = width


class DrawLine:

    def __init__(self):

        self.start = random_start_positions()

        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

        self.increment_x1 = 1
        self.increment_y1 = 2
        self.increment_x2 = 3
        self.increment_y2 = 4

    def next_positions(self):

        if not self.x1 and not self.y1 and not self.x2 and not self.y2:
            self.x1 = self.start[0][0] + self.increment_x1
            self.y1 = self.start[0][1] + self.increment_y1
            self.x2 = self.start[1][0] + self.increment_x2
            self.y2 = self.start[1][1] + self.increment_y2

        if self.x1 <= 5 or self.x1 >= size[0] - 5:
            self.increment_x1 *= -1
        if self.y1 <= 5 or self.y1 >= size[1] - 5:
            self.increment_y1 *= -1
        if self.x2 <= 5 or self.x2 >= size[0] - 5:
            self.increment_x2 *= -1
        if self.y2 <= 5 or self.y2 >= size[1] - 5:
            self.increment_y2 *= -1

        self.x1 += self.increment_x1
        self.y1 += self.increment_y1
        self.x2 += self.increment_x2
        self.y2 += self.increment_y2

        return (self.x1, self.y1), (self.x2, self.y2)

    def randomize_positions(self):
        (self.x1, self.y1), (self.x2, self.y2) = random_start_positions()

    def cycle_color(self):
        (r, g, b) = colorsys.hls_to_rgb(float(self.x1) / size[0], 0.6, 1.0)
        return int(255 * r), int(255 * g), int(255 * b)

    def check_if_p1_is_closer(self, x, y):
        _point_1_distance = sqrt((self.x1 - x) ** 2 + (self.y1 - y) ** 2)
        _point_2_distance = sqrt((self.x2 - x) ** 2 + (self.y2 - y) ** 2)

        return True if _point_1_distance < _point_2_distance else False

    def compose_line(self, current_x=False, current_y=False):

        next_positions = self.next_positions()
        width = 1

        start_position, end_position = next_positions[0], next_positions[1]
        if current_x and current_y:
            if self.check_if_p1_is_closer(current_x, current_y):
                self.x1 = current_x
                self.y1 = current_y
            else:
                self.x2 = current_x
                self.y2 = current_y

        return Line(start_position, end_position, self.cycle_color(), width)


if __name__ == "__main__":
    main()
