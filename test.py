import unittest
from main import LEFT_BOTTOM_CORNER, RIGHT_TOP_CORNER, MAP_WIDTH, MAP_HEIGHT, coordinates_to_pixels

class MyTestCase(unittest.TestCase):
    def test_something(self):
        result = coordinates_to_pixels(LEFT_BOTTOM_CORNER)
        self.assertEqual(result, (0, 0))

        result = coordinates_to_pixels(RIGHT_TOP_CORNER)

        self.assertAlmostEqual(result[0], MAP_WIDTH)
        self.assertAlmostEqual(result[1], MAP_HEIGHT)

if __name__ == '__main__':
    unittest.main()
