import pygame

# user settings

TICK = 100
WINDOW_SIZE = (500, 500)
BACKGROUND_COLOR = (255, 255, 255)
SQUARES_COLOR = (135, 210, 0)
INTERVAL = 50

# end of user settings

VERTICAL = 0
HORIZONTAL = 1
SIZE_CAR = 5


class Car:
    bad = False
    x = 0
    y = 0
    cell_x = 0
    cell_y = 0
    time = 0
    direction = VERTICAL
    color = (255, 0, 0)
    rect = pygame.Rect((0, 0), (0, 0))


class Cell:
    x = 0
    y = 0
    rect = pygame.Rect((0, 0), (0, 0))


class Field:
    interval = INTERVAL
    squares_color = SQUARES_COLOR
    car_size = SIZE_CAR

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
        for i in range(len(field[0])):
            if field[0][i] == 0:
                continue
            car = Car()
            car.direction = VERTICAL
            car.time = 0
            car.cell_x = 0
            car.cell_y = i
            car.x = (i // 2) * (self.interval + self.squares_width) + self.squares_width + self.interval // 2
            car.y = 0
            car.size = self.car_size
            car.rect = pygame.Rect((car.x - self.car_size // 2, car.y - self.car_size // 2),
                                   (self.car_size, self.car_size))
            pygame.draw.rect(pygame.display.get_surface(), car.color, car.rect)
            pygame.display.flip()
            self.cars.append(car)

        for i in range(len(field)):
            if field[i][0] == 0:
                continue
            car = Car()
            car.direction = HORIZONTAL
            car.time = 0
            car.cell_x = i
            car.cell_y = 0
            car.x = 0
            car.y = (i // 2) * (self.interval + self.squares_height) + self.squares_height + self.interval // 2
            car.rect = pygame.Rect((car.x - self.car_size // 2, car.y - self.car_size // 2),
                                   (self.car_size, self.car_size))
            car.size = self.car_size
            pygame.draw.rect(pygame.display.get_surface(), car.color, car.rect)
            pygame.display.flip()
            self.cars.append(car)
        check = True
        time = 0
        waiting_time = 0
        while check:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit("Goodbye")
            if pygame.time.get_ticks() % TICK != 0:
                continue
            count_bad = 0
            for c in self.cars:
                c.time += 1
                if c.direction == HORIZONTAL:
                    if c.cell_x % 2 == 1:
                        if time % traffic_lights[(c.cell_x + 1) // 2][c.cell_y // 2][HORIZONTAL][1] > \
                                traffic_lights[(c.cell_x + 1) // 2][c.cell_y // 2][HORIZONTAL][0]:
                            waiting_time += 1
                        else:
                            c.x = (c.cell_x - 1) * (self.interval + self.squares_width) + \
                                  self.squares_width * c.time // field[c.cell_x][c.cell_y]
                            c.rect = pygame.Rect((c.x, c.y), (self.car_size, self.car_size))
                            pygame.draw.rect(pygame.display.get_surface(), c.color, c.rect)
                            pygame.display.update(c.rect)
                    else:
                        c.x = (c.cell_x - 1) * self.interval + c.cell_x * self.squares_width + \
                              self.interval * c.time // field[c.cell_x][c.cell_y]
                        c.rect = pygame.Rect((c.x, c.y), (self.car_size, self.car_size))
                        pygame.draw.rect(pygame.display.get_surface(), c.color, c.rect)
                        pygame.display.update(c.rect)
                else:
                    if c.cell_y % 2 == 1:
                        if time % traffic_lights[c.cell_x // 2][(c.cell_y + 1) // 2][VERTICAL][1] > \
                                traffic_lights[c.cell_x // 2][(c.cell_y + 1) // 2][VERTICAL][0]:
                            waiting_time += 1
                        else:
                            c.y = (c.cell_y - 1) * (self.interval + self.squares_height) + \
                                  self.squares_height * c.time // field[c.cell_x][c.cell_y]
                            c.rect = pygame.Rect((c.x, c.y), (self.car_size, self.car_size))
                            pygame.draw.rect(pygame.display.get_surface(), c.color, c.rect)
                            pygame.display.update(c.rect)
                    else:
                        c.y = (c.cell_y - 1) * self.interval + c.cell_y * self.squares_height + \
                              self.interval * c.time // field[c.cell_x][c.cell_y]
                        c.rect = pygame.Rect((c.x, c.y), (self.car_size, self.car_size))
                        pygame.draw.rect(pygame.display.get_surface(), c.color, c.rect)
                        pygame.display.update(c.rect)
                if c.cell_x < (len(field) - 1) and c.cell_y < (len(field[0]) - 1):
                    if c.time >= field[c.cell_x][c.cell_y]:
                        if c.direction == HORIZONTAL:
                            c.cell_y += 1
                        else:
                            c.cell_x += 1
                        c.time = 0
                else:
                    count_bad += 1
            if count_bad == len(self.cars):
                check = False
            time += 1

    def __init__(self, field, traffic_lights):

        self.cars = list()
        self.field_coords = list()
        self.count_of_squares_y = (len(field) + 1) // 2
        self.count_of_squares_x = (len(field[0]) + 1) // 2

        pygame.init()
        pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.get_surface().fill(BACKGROUND_COLOR)

        self.squares_width = (pygame.display.get_surface().get_size()[0] - (
                self.count_of_squares_x - 1) * self.interval) // self.count_of_squares_x
        self.squares_height = (pygame.display.get_surface().get_size()[1] - (
                self.count_of_squares_y - 1) * self.interval) // self.count_of_squares_y
        self.visualisation(field, traffic_lights)
        print(111111111111111111111111111111111111111)
        while 1:
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit("Goodbye")
