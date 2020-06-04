import pygame
from tkinter import messagebox
import threading

# user settings

FPS = 60
WINDOW_SIZE = (1000, 1000)
BACKGROUND_COLOR = (255, 255, 255)
SQUARES_COLOR = (29, 35, 91)
INTERVAL = 50
CAR_COLOR = (0, 255, 0)

# end of user settings

# system constants

TIME_INTERVAL = 1000 // FPS
VERTICAL = 0
HORIZONTAL = 1
SIZE_CAR = 10
RED = (255, 0, 0)
GREEN = (0, 255, 0)


# end of system constants

class Car:
    def __init__(self, x=0, y=0, cell_x=0, cell_y=0, direction=VERTICAL):
        self.is_road_ended = False
        self.is_waiting = False
        self.current_time = 0
        self.x = x
        self.y = y
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.direction = direction
        self.drawing_rect = pygame.Rect((self.x, self.y), (SIZE_CAR, SIZE_CAR))

    def redraw(self):
        self.drawing_rect.left = self.x
        self.drawing_rect.top = self.y

    def move(self, x, y):
        self.x = x
        self.y = y
        self.redraw()


class Cell:
    def __init__(self, x: int = 0, y: int = 0, width: int = 100, height: int = 100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.drawing_rect = pygame.Rect((self.x, self.y), (width, height))


class Field:

    def create_town(self):
        for i in range(self.count_of_squares_x):
            self.field_coords.append(list())
            for j in range(self.count_of_squares_y):
                x = i * (INTERVAL + self.squares_width)
                y = j * (INTERVAL + self.squares_height)
                cell = Cell(x, y, self.squares_width, self.squares_height)
                pygame.draw.rect(self.window, SQUARES_COLOR, cell.drawing_rect)
                pygame.display.flip()
                self.field_coords[i].append(cell)

    def redraw_town(self):
        for i in self.field_coords:
            for j in i:
                pygame.draw.rect(self.window, SQUARES_COLOR, j.drawing_rect)

    def set_start_positions(self):
        for i in range(len(self.field[0])):
            if self.field[0][i] == 0:
                continue
            x = (i // 2) * (INTERVAL + self.squares_width) + self.squares_width + INTERVAL // 2 - SIZE_CAR // 2
            y = 0 - SIZE_CAR // 2
            car = Car(x, y, 0, i, VERTICAL)
            pygame.draw.rect(self.window, GREEN, car.drawing_rect)
            pygame.display.flip()
            self.cars.append(car)
        for i in range(len(self.field)):
            if self.field[i][0] == 0:
                continue
            x = 0 - SIZE_CAR // 2
            y = (i // 2) * (INTERVAL + self.squares_height) + self.squares_height + INTERVAL // 2 - SIZE_CAR // 2
            car = Car(x, y, i, 0, HORIZONTAL)

            pygame.draw.rect(self.window, GREEN, car.drawing_rect)
            pygame.display.flip()
            self.cars.append(car)

    def cell_coord_to_traffic_index(self, value: int):
        return (value - 1) // 2

    def can_go_on_the_crossroad(self, car: Car):
        x = self.cell_coord_to_traffic_index(car.cell_x)
        y = self.cell_coord_to_traffic_index(car.cell_y)
        sum_time = self.traffic_lights[x][y][car.direction][1] + self.traffic_lights[x][y][car.direction][2]
        if car.current_time > 0 or self.traffic_lights[y][x][car.direction][0] > self.time:
            return True
        if ((self.time - self.traffic_lights[x][y][car.direction][0]) % sum_time) > \
                self.traffic_lights[x][y][car.direction][1]:
            return False
        else:
            return True

    def is_on_the_crossroad(self, car: Car):
        if car.cell_x % 2 == 0 or car.cell_y % 2 == 0:
            return False
        else:
            return True

    def move_car(self, car: Car):
        new_x: int = car.x
        new_y: int = car.y
        if car.cell_y % 2 == 0 or car.cell_x % 2 == 0:
            if car.direction == HORIZONTAL:
                new_x = (car.cell_y // 2) * (INTERVAL + self.squares_width) + \
                        (self.squares_width * car.current_time) // self.field[car.cell_x][car.cell_y]
            else:
                new_y = (car.cell_x // 2) * (INTERVAL + self.squares_height) + \
                        (self.squares_height * car.current_time) // self.field[car.cell_x][car.cell_y]
        else:
            if car.direction == HORIZONTAL:
                new_x = ((car.cell_y + 1) // 2) * self.squares_width + ((car.cell_y - 1) // 2) * INTERVAL + \
                        (INTERVAL * car.current_time) // self.field[car.cell_x][car.cell_y]
            else:
                new_y = ((car.cell_x + 1) // 2) * self.squares_height + ((car.cell_x - 1) // 2) * INTERVAL + \
                        (INTERVAL * car.current_time) // self.field[car.cell_x][car.cell_y]
        car.move(new_x, new_y)
        if car.current_time >= self.field[car.cell_x][car.cell_y]:
            if car.direction == VERTICAL:
                car.cell_x += 1
            else:
                car.cell_y += 1
            car.current_time = 0

    def can_go(self, car: Car):
        if (car.cell_x > (len(self.field) - 1)) or (car.cell_y > (len(self.field[0]) - 1)):
            return False
        else:
            return True

    def step(self):
        for car in self.cars:
            if self.can_go(car):
                if self.is_on_the_crossroad(car):
                    if self.can_go_on_the_crossroad(car):
                        car.current_time += 1
                        self.move_car(car)
                    else:
                        self.waiting_time += 1
                else:
                    car.current_time += 1
                    self.move_car(car)
            for others in self.cars:
                if car.drawing_rect.colliderect(others.drawing_rect) and car != others:
                    self.collision = True
                    return True
        self.window.fill(BACKGROUND_COLOR)
        self.redraw_town()
        for car in self.cars:
            pygame.draw.rect(self.window, CAR_COLOR, car.drawing_rect)
        pygame.display.flip()
        self.time += 1
        return False

    def end(self):
        for car in self.cars:
            if (car.cell_x <= (len(self.field) - 1)) and (car.cell_y <= (len(self.field[0]) - 1)):
                return False
        else:
            return True

    def cycle_of_steps(self):
        interval = threading.Event()
        interval.set()
        while self.stop.is_set():
            while interval.is_set():
                collision: bool = self.step()
                interval.wait(TIME_INTERVAL)
                if self.end() or collision:
                    self.stop.clear()
                    interval.clear()

    def visualisation(self):
        self.create_town()
        self.set_start_positions()
        self.stop.set()

        steps = threading.Thread(target=self.cycle_of_steps, daemon=True)
        steps.start()

        while steps.is_alive():
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit()

        if not self.collision:
            messagebox.showinfo("Your wasting time",
                                "All your wasting time is {:.2f} s!".format(self.waiting_time / FPS))
        else:
            messagebox.showerror("Error", "You have a collision!")

    def __init__(self, field, traffic_lights):

        self.stop = threading.Event()
        self.waiting_time = 0
        self.time = 0
        self.cars = list()
        self.field_coords = list()
        self.collision = False
        self.count_of_squares_y = (len(field) + 1) // 2
        self.count_of_squares_x = (len(field[0]) + 1) // 2
        self.field = field
        self.traffic_lights = [[[[l * FPS for l in k] for k in j] for j in i] for i in traffic_lights]

        pygame.init()
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        self.window.fill(BACKGROUND_COLOR)

        self.squares_width = (self.window.get_size()[0] -
                              (self.count_of_squares_x - 1) * INTERVAL) // self.count_of_squares_x
        self.squares_height = (self.window.get_size()[1] -
                               (self.count_of_squares_y - 1) * INTERVAL) // self.count_of_squares_y
