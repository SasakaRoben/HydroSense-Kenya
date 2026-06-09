import numpy as np
import pytest

# Import your functions here
# from integration_module import trapezoidal_rule, composite_simpsons_rule


# Mock implementations for testing standalone execution
def trapezoidal_rule(y_values, step_size):
    n = len(y_values) - 1
    total_area = y_values[0] + y_values[-1]
    for i in range(1, n):
        total_area += 2 * y_values[i]
    return (step_size / 2.0) * total_area


def composite_simpsons_rule(y_values, step_size):
    n = len(y_values) - 1
    if n % 2 != 0:  # Odd intervals handle tail step with Trapezoidal
        simps_y = y_values[:-1]
        trap_y = y_values[-2:]
        return simpsons_core(simps_y, step_size) + (step_size / 2.0) * (
            trap_y[0] + trap_y[1]
        )
    return simpsons_core(y_values, step_size)


def simpsons_core(y_values, step_size):
    n = len(y_values) - 1
    total_area = y_values[0] + y_values[-1]
    for i in range(1, n):
        if i % 2 == 1:
            total_area += 4 * y_values[i]
        else:
            total_area += 2 * y_values[i]
    return (step_size / 3.0) * total_area


# --- THE TESTS ---


def test_trapezoidal_linear_function():
    """Test Trapezoidal rule on a perfectly linear function f(x) = x from 0 to

    4.

    Integral should equal exactly 8.0.
    """
    y = [0.0, 1.0, 2.0, 3.0, 4.0]
    h = 1.0
    assert pytest.approx(trapezoidal_rule(y, h)) == 8.0


def test_simpsons_even_intervals():
    """Test Simpson's core on a parabola f(x) = x^2 from 0 to 2.

    Integral should equal 8/3 (~2.6667).
    """
    y = [0.0, 1.0, 4.0]  # 2 intervals (even)
    h = 1.0
    assert pytest.approx(composite_simpsons_rule(y, h), rel=1e-4) == 2.66666667


def test_composite_simpsons_odd_intervals():
    """Verify that an odd number of intervals does not throw an error and is

    handled by the composite fallback.
    """
    y = [1.0, 2.0, 1.0, 3.0]  # 3 intervals (odd)
    h = 1.0
    # Expected: Simpson's on [1, 2, 1] -> (1/3)*(1 + 4(2) + 1) = 3.3333
    # plus Trapezoidal on [1, 3] -> (1/2)*(1 + 3) = 2.0. Total = 5.3333
    assert pytest.approx(composite_simpsons_rule(y, h)) == 5.33333333