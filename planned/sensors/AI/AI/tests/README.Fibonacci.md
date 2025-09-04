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


if off tweak:

---

### `run_tests.py`
```python
#!/usr/bin/env python3
"""
Lightweight JSON test runner for the Fibonacci test pack.

Usage:
  python3 run_tests.py
  python3 run_tests.py --impl planned.sensors.AI.AI.src.fibonacci
"""
from __future__ import annotations

import argparse
import importlib
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

# --- Configure where to import the implementation from by default ---
IMPLEMENTATION_IMPORT = "planned.sensors.AI.AI.src.fibonacci"

# --- Paths ---
THIS_DIR = Path(__file__).parent
DEFAULT_TEST_GLOB = "F*.json"

# --- Utilities ---

def approx_equal(a: Any, b: Any, tol: float) -> bool:
    """Numeric approximate equality with absolute tolerance."""
    try:
        return abs(float(a) - float(b)) <= tol
    except Exception:
        return False

def approx_equal_dict(a: dict, b: dict, tol: dict[str, float]) -> bool:
    """Dict equality with per-field tolerances."""
    for k in b.keys():
        if k not in a:
            return False
        if isinstance(b[k], (int, float)):
            t = tol.get(k, 0.0)
            if not approx_equal(a[k], b[k], t):
                return False
        else:
            if a[k] != b[k]:
                return False
    return True

def format_ok(msg: str) -> str:
    return f"\033[92m✔ {msg}\033[0m"

def format_fail(msg: str) -> str:
    return f"\033[91m✘ {msg}\033[0m"

@dataclass
class TestResult:
    id: str
    name: str
    passed: bool
    message: str

# --- Core runner ---

def load_impl(module_path: str):
    try:
        return importlib.import_module(module_path)
    except ModuleNotFoundError as e:
        print(format_fail(f"Could not import implementation module '{module_path}': {e}"))
        sys.exit(1)

def run_json_test(impl, spec_path: Path) -> TestResult:
    spec = json.loads(spec_path.read_text())
    test_id = spec.get("id", spec_path.stem)
    name = spec.get("name", spec_path.stem)
    func_name = spec["function"]
    expected_error = spec.get("expected_error")

    # Resolve function
    try:
        func: Callable = getattr(impl, func_name)
    except AttributeError:
        return TestResult(test_id, name, False, f"Function '{func_name}' not found in implementation.")

    # Build calls
    try:
        if "cases" in spec:
            # Multiple inputs / outputs
            for case in spec["cases"]:
                kwargs = case if isinstance(case, dict) else {}
                n = kwargs.get("n")
                try:
                    out = func(**{k: v for k, v in kwargs.items() if k != "expected"})
                except Exception as e:
                    return TestResult(test_id, name, False, f"Case n={n}: unexpected exception: {e}")
                exp = kwargs["expected"]
                if out != exp:
                    return TestResult(test_id, name, False, f"Case n={n}: expected {exp}, got {out}")
            return TestResult(test_id, name, True, "All cases passed.")

        # Single call
        kwargs = spec.get("input", {})
        if expected_error:
            try:
                _ = func(**kwargs)
            except Exception as e:
                if type(e).__name__ == expected_error:
                    return TestResult(test_id, name, True, f"Raised {expected_error} as expected.")
                return TestResult(test_id, name, False, f"Raised {type(e).__name__}, expected {expected_error}.")
            return TestResult(test_id, name, False, f"Expected error {expected_error}, but call succeeded.")

        out = func(**kwargs) if kwargs else func()

        # Expected shapes
        if "expected_meta" in spec:
            # Dict with meta properties (e.g., digits, bigint_required)
            exp_meta = spec["expected_meta"]
            # Allow extra keys in output; assert at least the expected ones
            for k, v in exp_meta.items():
                if k not in out:
                    return TestResult(test_id, name, False, f"Missing meta field '{k}' in output.")
                if out[k] != v:
                    return TestResult(test_id, name, False, f"Meta '{k}': expected {v}, got {out[k]}")
            return TestResult(test_id, name, True, "Meta matched.")

        if "expected" in spec:
            exp = spec["expected"]
            tol = spec.get("tolerance")

            # Numeric with scalar tolerance
            if isinstance(exp, (int, float)) and isinstance(tol, (int, float)):
                if approx_equal(out, exp, float(tol)):
                    return TestResult(test_id, name, True, "Within tolerance.")
                return TestResult(test_id, name, False, f"Expected {exp}±{tol}, got {out}")

            # Dict with per-field tolerances
            if isinstance(exp, dict) and isinstance(tol, dict):
                if isinstance(out, dict) and approx_equal_dict(out, exp, tol):
                    return TestResult(test_id, name, True, "Fields within tolerance.")
                return TestResult(test_id, name, False, f"Expected (with per-field tol) {exp}, got {out}")

            # Exact match (lists, ints, dicts, etc.)
            if out == exp:
                return TestResult(test_id, name, True, "Exact match.")
            return TestResult(test_id, name, False, f"Expected {exp}, got {out}")

        return TestResult(test_id, name, True, "No 'expected' given; nothing to assert.")
    except Exception as e:
        return TestResult(test_id, name, False, f"Runner error: {e}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--impl",
        default=IMPLEMENTATION_IMPORT,
        help="Python module path to the implementation (default: %(default)s)",
    )
    ap.add_argument(
        "--glob",
        default=DEFAULT_TEST_GLOB,
        help=f"Glob for selecting test JSONs in this folder (default: {DEFAULT_TEST_GLOB})",
    )
    args = ap.parse_args()

    impl = load_impl(args.impl)

    test_files = sorted(THIS_DIR.glob(args.glob))
    if not test_files:
        print(format_fail(f"No tests found matching pattern '{args.glob}' in {THIS_DIR}"))
        sys.exit(1)

    results: list[TestResult] = []
    for p in test_files:
        res = run_json_test(impl, p)
        results.append(res)
        icon = "OK" if res.passed else "FAIL"
        print((format_ok if res.passed else format_fail)(f"{p.name}: {res.message}"))

    passed = sum(r.passed for r in results)
    total = len(results)
    print("\n" + ("=" * 48))
    if passed == total:
        print(format_ok(f"ALL TESTS PASSED ({passed}/{total})"))
        code = 0
    else:
        print(format_fail(f"{passed}/{total} tests passed"))
        # Print a short failure summary
        for r in results:
            if not r.passed:
                print(format_fail(f"- {r.id} {r.name}: {r.message}"))
        code = 2
    print("=" * 48 + "\n")
    sys.exit(code)

if __name__ == "__main__":
    main()

