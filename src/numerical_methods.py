import sys

def bisection_method(f, a, b, tol=1e-6, max_iter=100):
    if f(a) * f(b) >= 0:
        return None, 0, "Failed: Same signs at bounds"
    
    iterations = 0
    for _ in range(max_iter):
        iterations += 1
        c = (a + b) / 2.0
        f_c = f(c)
        
        if abs(f_c) < tol or (b - a) / 2.0 < tol:
            return c, iterations, "Converged"
            
        if f(a) * f_c < 0:
            b = c
        else:
            a = c
    return (a + b) / 2.0, iterations, "Max Iterations Reached"


def newton_raphson_method(f, df, x0, tol=1e-6, max_iter=100):
    x = x0
    iterations = 0
    for _ in range(max_iter):
        iterations += 1
        df_x = df(x)
        
        if abs(df_x) < 1e-12:
            return x, iterations, "Failed: Derivative near zero"
            
        x_next = x - (f(x) / df_x)
        
        if abs(x_next - x) < tol or abs(f(x_next)) < tol:
            return x_next, iterations, "Converged"
            
        x = x_next
    return x, iterations, "Max Iterations Reached"


def secant_method(f, x0, x1, tol=1e-6, max_iter=100):
    iterations = 0
    for _ in range(max_iter):
        iterations += 1
        f_x0, f_x1 = f(x0), f(x1)
        
        if abs(f_x1 - f_x0) < 1e-12:
            return x1, iterations, "Failed: Denominator near zero"
            
        x_next = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
        
        if abs(x_next - x1) < tol or abs(f(x_next)) < tol:
            return x_next, iterations, "Converged"
            
        x0, x1 = x1, x_next
    return x1, iterations, "Max Iterations Reached"


# Run Simulation and Log Results

# Target Function: f(x) = x^3 - x - 2
def f(x): return x**3 - x - 2
def df(x): return 3*x**2 - 1

# Execute each method
root_b, iter_b, status_b = bisection_method(f, a=1.0, b=2.0)
root_n, iter_n, status_n = newton_raphson_method(f, df, x0=1.0)
root_s, iter_s, status_s = secant_method(f, x0=1.0, x1=2.0)

# Calculate final residual errors |f(root)|
err_b = abs(f(root_b)) if root_b is not None else float('nan')
err_n = abs(f(root_n)) if root_n is not None else float('nan')
err_s = abs(f(root_s)) if root_s is not None else float('nan')


# Comparison Report
print(f"{'METHOD COMPARISON REPORT (f(x) = x^3 - x - 2)':^72}")
print(f"{'Method':<20}{'Iterations':<12}{'Final Root':<15}{'Final Error |f(x)|':<20}{'Status':<10}")

print(f"{'Bisection':<20}{iter_b:<12}{root_b:<15.6f}{err_b:<20.6e}{status_b:<10}")
print(f"{'Newton-Raphson':<20}{iter_n:<12}{root_n:<15.6f}{err_n:<20.6e}{status_n:<10}")
print(f"{'Secant':<20}{iter_s:<12}{root_s:<15.6f}{err_s:<20.6e}{status_s:<10}")