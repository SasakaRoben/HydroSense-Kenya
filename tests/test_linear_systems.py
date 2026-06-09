import numpy as np
import pytest
import scipy.linalg as la


def test_solver_mathematical_validity():
    """Verifies both solvers yield matching solutions and back-multiply

    perfectly to vector b.
    """
    A = np.array([[2.0, -1.0, 0.0], [-1.0, 2.0, -1.0], [0.0, -1.0, 2.0]])
    b = np.array([4.0, 2.0, 5.0])

    # Direct solve
    x_direct = np.linalg.solve(A, b)

    # LU solve
    lu, piv = la.lu_factor(A)
    x_lu = la.lu_solve((lu, piv), b)

    # Cross-method validation
    assert np.allclose(x_direct, x_lu)

    # Mathematical identity check (Ax - b = 0)
    assert np.allclose(np.dot(A, x_direct), b)


def test_singular_matrix_handling():
    """Ensure our system catches invalid physical topologies (e.g., zero

    rows).
    """
    invalid_A = np.array([[0.0, 0.0, 0.0], [-1.0, 2.0, -1.0], [0.0, -1.0, 2.0]])
    b = np.array([4.0, 2.0, 5.0])

    with pytest.raises(np.linalg.LinAlgError):
        np.linalg.solve(invalid_A, b)