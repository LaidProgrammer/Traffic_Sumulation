import unittest

from visualisation import Field, Car, Cell, VERTICAL, FPS, INTERVAL


class CarTest(unittest.TestCase):
    def setUp(self):
        self.test_car = Car(1, 2, 3, 4, VERTICAL)

    def test_Car_creation(self):
        self.assertEqual(self.test_car.x, 1)
        self.assertEqual(self.test_car.y, 2)
        self.assertEqual(self.test_car.cell_x, 3)
        self.assertEqual(self.test_car.cell_y, 4)
        self.assertEqual(self.test_car.direction, VERTICAL)

    def test_Car_redraw(self):
        self.test_car.x = -1
        self.test_car.y = -2
        self.test_car.redraw()
        self.assertEqual(self.test_car.drawing_rect.top, self.test_car.y)
        self.assertEqual(self.test_car.drawing_rect.left, self.test_car.x)

    def test_Car_move(self):
        self.test_car.move(5, 6)
        self.assertEqual(self.test_car.x, 5)
        self.assertEqual(self.test_car.y, 6)


class CellTest(unittest.TestCase):
    def setUp(self):
        self.test_cell = Cell(1, 2, 3, 4)

    def test_Cell_creation(self):
        self.assertEqual(self.test_cell.x, 1)
        self.assertEqual(self.test_cell.y, 2)
        self.assertEqual(self.test_cell.width, 3)
        self.assertEqual(self.test_cell.height, 4)


class FieldTest(unittest.TestCase):
    def setUp(self):
        self.lens = [[0, 100, 0],
                     [100, 50, 100],
                     [0, 100, 0]]
        self.traffic_lights = [[[[0, 1, 3],
                                 [0, 1, 3]]]]
        self.test_field = Field(field=self.lens, traffic_lights=self.traffic_lights)

    def test_Field_creation(self):
        self.assertEqual(self.test_field.traffic_lights,
                         [[[[l * FPS for l in k] for k in j] for j in i] for i in self.traffic_lights])
        self.assertEqual(self.test_field.field, self.lens)
        self.assertEqual(self.test_field.count_of_squares_x, (len(self.lens[0]) + 1) // 2)
        self.assertEqual(self.test_field.count_of_squares_y, (len(self.lens) + 1) // 2)
        self.assertEqual(self.test_field.squares_width,
                         (self.test_field.window.get_size()[0] -
                          (self.test_field.count_of_squares_x - 1) * INTERVAL) // self.test_field.count_of_squares_x)
        self.assertEqual(self.test_field.squares_height,
                         (self.test_field.window.get_size()[1] -
                          (self.test_field.count_of_squares_y - 1) * INTERVAL) // self.test_field.count_of_squares_y)

    def test_Field_can_go(self):
        test_car = Car(cell_x=2, cell_y=3)
        self.assertFalse(self.test_field.can_go(test_car))
        test_car.cell_y = 2
        self.assertTrue(self.test_field.can_go(test_car))

    def test_Field_cell_coord_to_traffic_index(self):
        self.assertEqual(self.test_field.cell_coord_to_traffic_index(1), 0)
        self.assertEqual(self.test_field.cell_coord_to_traffic_index(11), 5)

    def test_Field_can_go_on_the_crossroad(self):
        test_car = Car(cell_x=1, cell_y=1)
        self.assertTrue(self.test_field.can_go_on_the_crossroad(test_car))
        self.test_field.time = self.traffic_lights[0][0][0][1] * FPS + 1
        self.assertFalse(self.test_field.can_go_on_the_crossroad(test_car))

    def test_Field_is_on_the_crossroad(self):
        test_car = Car(cell_x=0, cell_y=1)
        self.assertFalse(self.test_field.is_on_the_crossroad(test_car))
        test_car.cell_x = 1
        self.assertTrue(self.test_field.is_on_the_crossroad(test_car))

    def test_Field_end(self):
        test_car = Car(cell_x=0, cell_y=0)
        self.test_field.cars.append(test_car)
        self.assertFalse(self.test_field.end())
        test_car.cell_x = 3
        self.assertTrue(self.test_field.end())


if __name__ == '__main__':
    unittest.main()
