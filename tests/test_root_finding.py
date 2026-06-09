import pytest


# Sample target function: f(x) = x^2 - 4 -> Root is at x = 2.0
def sample_target_function(x):
    return x**2 - 4.0


def bisection_method(func, a, b, tol=1e-5, max_iter=100):
    if func(a) * func(b) >= 0:
        raise ValueError("Root is not bracketed by signs at bounds a and b.")

    for _ in range(max_iter):
        midpoint = (a + b) / 2.0
        if abs(func(midpoint)) < tol or (b - a) / 2.0 < tol:
            return midpoint

        if func(midpoint) * func(a) < 0:
            b = midpoint
        else:
            a = midpoint
    return (a + b) / 2.0


# --- THE TESTS ---


def test_bisection_successful_convergence():
    """Verify root finding hits true root within designated numerical tolerances."""
    root = bisection_method(sample_target_function, 0.0, 5.0, tol=1e-4)
    assert pytest.approx(root, abs=1e-4) == 2.0


def test_bisection_invalid_bounds_exception():
    """Test that the algorithm safely throws an exception if the root isn't

    bracketed.
    """
    with pytest.raises(ValueError, match="Root is not bracketed"):
        bisection_method(sample_target_function, 3.0, 6.0)