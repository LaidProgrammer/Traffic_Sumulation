from visualisation import Field


lens = [[0, 100, 0, 100, 0, 100, 0],
        [100, 100, 100, 100, 100, 100, 100],
        [0, 100, 0, 100, 0, 100, 0],
        [100, 100, 100, 100, 100, 100, 100],
        [0, 100, 0, 100, 0, 100, 0]]
traffic_lights = [[[[1, 3], [1, 3]], [[1, 3], [1, 3]], [[1, 3], [1, 3]], [[1, 3], [1, 3]]],
                  [[[1, 3], [1, 3]], [[1, 3], [1, 3]], [[1, 3], [1, 3]], [[1, 3], [1, 3]]],
                  [[[1, 3], [1, 3]], [[1, 3], [1, 3]], [[1, 3], [1, 3]], [[1, 3], [1, 3]]],
                  [[[1, 3], [1, 3]], [[1, 3], [1, 3]], [[1, 3], [1, 3]], [[1, 3], [1, 3]]]]

if __name__ == '__main__':
    field = Field(field=lens, traffic_lights=traffic_lights)
