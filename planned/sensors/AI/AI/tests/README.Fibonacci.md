# Fibonacci Test Pack (F01–F16)

This folder contains JSON test specs for Fibonacci- and phyllotaxis-related utilities.
The tests are implementation-agnostic: write your functions anywhere, point the runner
at them, and you’ll get pass/fail with a tidy summary.

---

## Folder layout

planned/
sensors/
AI/
AI/
src/
fibonacci.py            # ← implement function signatures here (recommended)
tests/
Fibonacci/
F01_basic_sequence.json
F02_zero_and_one.json
F03_negative_input_guard.json
F04_large_n_exact.json
F05_golden_ratio_convergence.json
F06_gcd_property.json
F07_cassini_identity.json
F08_matrix_representation.json
F09_binet_formula_check.json
F10_golden_angle_degrees.json
F11_phyllotaxis_position_k100.json
F12_sum_identity.json
F13_negative_index_identity.json
F14_pisano_period_mod_10.json
F15_sum_of_squares_identity.json
F16_scale_up_signal.json
README.md
run_tests.py

> You can change where the runner imports your code by editing `IMPLEMENTATION_IMPORT`
> at the top of `run_tests.py`.

---

## Function contracts (expected names & return shapes)

Implement these in `planned/sensors/AI/AI/src/fibonacci.py`:

```python
def fibonacci_sequence_generator_up_to_nth_term(n: int) -> list[int]: ...
def fibonacci_n(n: int) -> int: ...
def ratio_Fn1_over_Fn(n: int) -> float: ...  # typically F(n+1)/F(n)
def gcd_fibonacci(m: int, n: int) -> int: ...
def cassini_check(n: int) -> int: ...  # returns (-1)**n
def fibonacci_n_via_matrix(n: int) -> int: ...
def fibonacci_n_via_binet(n: int) -> int: ...
def phyllotaxis_golden_angle_deg() -> float: ...
def phyllotaxis_polar_coordinates(k: int, scale_c: float = 1.0, normalize_angle: bool = True) -> dict:
    """
    Returns {"radius": float, "angle_rad": float}
    r = c * sqrt(k)
    theta = k * golden_angle (in radians); if normalize_angle, mod 2π
    """
def sum_fibonacci_0_to_n(n: int) -> int: ...
def fibonacci_negative_n(n: int) -> int: ...
def pisano_period(m: int) -> int: ...
def sum_of_squares_0_to_n(n: int) -> int: ...
def fibonacci_n_meta(n: int) -> dict:
    """
    Returns {"digits": int, "bigint_required": bool}
    """
