import pytest


# Mock rate equation for testing tracking consistency
def simple_decay_model(theta, k=0.08):
    return -k * theta


def run_euler_step(theta, h, k=0.08):
    next_theta = theta + h * simple_decay_model(theta, k)
    return max(0.0, min(100.0, next_theta))  # Truncation envelope clipping


# --- THE TESTS ---


@pytest.mark.parametrize(
    "initial, expected_step_1",
    [
        (35.0, 32.2),  # 35.0 + 1.0 * (-0.08 * 35) = 32.2
        (20.0, 18.4),  # 20.0 + 1.0 * (-0.08 * 20) = 18.4
    ],
)
def test_euler_exact_math_steps(initial, expected_step_1):
    """Parameterization test to cross-verify basic algorithmic progression calculations."""
    assert pytest.approx(run_euler_step(initial, h=1.0)) == expected_step_1


def test_moisture_saturation_clipping():
    """Ensure that the simulation safeguards prevent physical impossibilities

    (e.g.

    dropping below 0%).
    """
    # Force a massive structural drop step that would mathematically hit negative numbers
    depleted_moisture = run_euler_step(theta=2.0, h=10.0, k=0.9)
    assert depleted_moisture >= 0.0