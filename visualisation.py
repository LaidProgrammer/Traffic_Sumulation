import pygame
from collections import namedtuple


class Car:
    x = 0
    y = 0
    cell_x = 0
    cell_y = 0
    time = 0


class Cell:
    x = 0
    y = 0
    rect = pygame.Rect((0, 0), (0, 0))


class Field:
    interval = 50
    squares_color = (135, 210, 0)

    def create_town(self, field):
        for i in range(self.count_of_squares_y):
            self.field_coords.append(list())
            for j in range(self.count_of_squares_x):
                cell = Cell()
                cell.x = i * (self.interval + self.squares_width)
                cell.y = j * (self.interval + self.squares_height)
                cell.rect = pygame.Rect((cell.x, cell.y), (self.squares_width, self.squares_height))
                pygame.draw.rect(pygame.display.get_surface(), self.squares_color, cell.rect)
                pygame.display.flip()
                self.field_coords[i].append(cell)

    def visualisation(self, field, traffic_lights):
        self.create_town(field)

    def __init__(self, field, traffic_lights):

        self.field_coords = list()
        self.count_of_squares_y = (len(field) + 1) // 2
        self.count_of_squares_x = (len(field[0]) + 1) // 2

        pygame.init()
        pygame.display.set_mode((1000, 1000))
        pygame.display.get_surface().fill((255, 255, 255))

        self.squares_width = (pygame.display.get_surface().get_size()[0] - (
                self.count_of_squares_x - 1) * self.interval) // self.count_of_squares_x
        self.squares_height = (pygame.display.get_surface().get_size()[1] - (
                self.count_of_squares_y - 1) * self.interval) // self.count_of_squares_y
        self.visualisation(field, traffic_lights)
        while 1:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit("Goodbye")
