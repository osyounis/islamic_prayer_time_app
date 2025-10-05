"""
بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ

This module contains tests used to make sure that the math module doesn't have
any errors.


Author: Omar Younis
Date: 28/09/2025 [dd/mm/yyyy format]

"""
import os
import sys
import math
import unittest

# Shows file where to look to import packages.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import utils.math_utils as mu
from utils.math_utils import _degree_to_radians, _radians_to_degree


class TestDegreeToRadianConversion(unittest.TestCase):
    """
    Unit tests for testing the conversions between degrees to radians.
    """

    def test_180_degrees_to_pi(self) -> None:
        """Tests to see if we get pi when we convert 180 degrees to radians.
        """
        self.assertAlmostEqual(_degree_to_radians(180.0), math.pi)

    def test_zero_degrees_to_zero(self) -> None:
        """Makes sure zero degrees give us 0 radians.
        """
        self.assertAlmostEqual(_degree_to_radians(0.0), 0.0)

    def test_90_degrees_to_half_pi(self) -> None:
        """Tests 90 degrees gives us pi/2 radians.
        """
        self.assertAlmostEqual(_degree_to_radians(90.0), math.pi / 2)

    def test_45_degrees_to_quarter_pi(self) -> None:
        """Tests to see that 45 degrees gives us pi/4 radians.
        """
        self.assertAlmostEqual(_degree_to_radians(45.0), math.pi / 4)

    def test_negative_degrees(self) -> None:
        """Makes sure we get the right conversion even with negative numbers.
        -180 gives us -pi.
        """
        self.assertAlmostEqual(_degree_to_radians(-180.0), -math.pi)

    def test_random_degree_value(self) -> None:
        """Tests a unique angle to see if the radians convert properly.
        10 degrees and the value was retrieved from a Texas Instruments TI-84
        Graphing Calculator.
        """
        self.assertAlmostEqual(_degree_to_radians(10), 0.1745329)


class TestRadiansToDegreeConversion(unittest.TestCase):
    """
    Unit tests for testing the conversions between radians to degrees.
    """

    def test_pi_to_180_degrees(self) -> None:
        """Tests pi converts to 180 degrees.
        """
        self.assertAlmostEqual(_radians_to_degree(math.pi), 180.0)

    def test_zero_to_zero_degrees(self) -> None:
        """Tests that zero radians converts to zero degrees.
        """
        self.assertAlmostEqual(_radians_to_degree(0.0), 0.0)

    def test_half_pi_to_90_degrees(self) -> None:
        """Tests that pi/2 rads converts to 90 degrees.
        """
        self.assertAlmostEqual(_radians_to_degree(math.pi / 2), 90.0)

    def test_quarter_pi_to_45_degrees(self) -> None:
        """Tests the pi/4 rads converts to 45 degrees.
        """
        self.assertAlmostEqual(_radians_to_degree(math.pi / 4), 45.0)

    def test_negative_radian(self) -> None:
        """Tests that -pi/4 rads converts to -45 degrees.
        """
        self.assertAlmostEqual(_radians_to_degree(-math.pi / 4), -45.0)

    def test_random_radian_value(self) -> None:
        """Tests a unique rad number to see if the degrees convert properly.
        0.1745329 is 10 degrees. This value was retrieved from a Texas
        Instruments TI-84 Graphing Calculator.
        """
        self.assertAlmostEqual(_radians_to_degree(0.1745329), 10.0, places=4)


class TestTrigFunctions(unittest.TestCase):
    """
    Unit tests for testing the cot(x) and acot(x) functions.
    """
    def test_45_degrees(self):
        """Test the cot(x) function. dcot() = cos() / sin(). The other method is
        to do 1 / tan(). This test compares both approaches.
        """
        self.assertAlmostEqual(mu.dcot(45.0), (1 / math.tan(math.pi / 4)))

    def test_zero_raises(self):
        """cot(0) should be undefined [dividing by zero]. This test makes sure
        an error is raised when this is attempted, specifically a divide by zero
        error.
        """
        with self.assertRaises(ZeroDivisionError):
            mu.dcot(0)

    def test_negative_angle(self):
        """Tests to make sure negative angles give the correct conversion in
        radians.
        """
        self.assertAlmostEqual(mu.dcot(-45.0), (1 / math.tan(-math.pi / 4)))

    def test_inverse_relationship(self):
        """Previous tests confirm that cot(x) is working properly if they all
        pass. This test assumes that doct(x) is correct and that dacot(x) is
        working. By passing one function into the other, we should end up with
        the original angle. If so then dacot(x) is correct.
        """
        angle = 45.0    # Angle to test with.
        self.assertAlmostEqual(mu.dacot(mu.dcot(angle)), angle)

    def test_zero_is_90_degrees(self) -> None:
        """acot(0) should be 90 degrees.
        """
        self.assertEqual(mu.dacot(0), 90.0)

    def test_quadrant_1(self) -> None:
        """acot(x > 0) should give an angle in Quadrant 1 (0° - 90°).
        """
        result = mu.dacot(1)    # cot(45 degrees) = 1
        self.assertTrue(0 < result < 90)
        self.assertAlmostEqual(result, 45.0)

    def test_quadrant_2(self) -> None:
        """acot(x < 0) should give an angle in Quadrant 2 (90° - 180°).
        """
        result = mu.dacot(-1)
        self.assertTrue(90 < result < 180)
        self.assertAlmostEqual(result, 90 + 45)


if __name__ == '__main__':
    unittest.main()
