import pygame
from collections import namedtuple

interval = 100


def draw_town(surface, lens, size):
    sq_size = [(surface.get_width() - interval * (size[0] + 1)) / size[0],
               (surface.get_height() - interval * (size[1] + 1)) / size[1]]
    for i in range(size[0]):
        for j in range(size[1]):
            rt_color = (30, 67, 120)
            rt = pygame.Rect(((interval + sq_size[0]) * i + interval, (interval + sq_size[1]) * j + interval),
                             (sq_size[0], sq_size[1]))
            pygame.draw.rect(surface, rt_color, rt, 0)
            pygame.display.update()


def make_wave(surface, traffic_lights, lens, size):
    sq_size = [(surface.get_width() - interval * (size[0] + 1)) / size[0],
               (surface.get_height() - interval * (size[1] + 1)) / size[1]]
    Car = namedtuple('Car',
                     ['x',
                      'y',
                      'time_to_next',
                      'direct',
                      'surface'
                      ]
                     )
    s = pygame.Surface((1, 1))
    s.fill((255, 255, 255))
    surface.blit(s, (interval / 2, interval / 2))
    test_car = Car(0, 1, lens[0][1], 1, s)
    cars = list()
    cars.append(test_car)

    while len(cars) > 0:
        for now in cars:
            all_d = sq_size[(now.direct + 1) % 2] + interval
            if now.direct == 0:

                surface.blit(test_car.surface, ())


def visualisation(traffic_lights, lens, size):
    pygame.init()
    window = pygame.display.set_mode((1000, 1000))
    bg_color = (255, 255, 200)
    window.fill(bg_color)
    pygame.display.update()
    draw_town(window, lens, size)
    make_wave(window, traffic_lights, lens, size)
    while 1:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()
