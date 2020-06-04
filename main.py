from visualisation import Field
from tkinter import Tk


def main():
    root = Tk()
    root.withdraw()
    lens = [[0, 200, 0, 100, 0, 100, 0],
            [500, 100, 100, 100, 100, 100, 100],
            [0, 100, 0, 100, 0, 100, 0],
            [1000, 100, 100, 100, 100, 100, 100],
            [0, 100, 0, 100, 0, 100, 0]]
    traffic_lights = [[[[2, 1, 3], [2, 1, 3]], [[0, 1, 3], [0, 1, 3]], [[0, 1, 3], [0, 1, 3]]],
                      [[[0, 1, 3], [0, 1, 3]], [[0, 1, 3], [0, 1, 3]], [[0, 1, 3], [0, 1, 3]]],
                      [[[0, 1, 3], [0, 1, 3]], [[0, 1, 3], [0, 1, 3]], [[0, 1, 3], [0, 1, 3]]]]
    field = Field(field=lens, traffic_lights=traffic_lights)
    field.visualisation()


if __name__ == '__main__':
    main()
