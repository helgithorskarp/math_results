# Reproduction

From the repository root, using Python 3.11 or later:

```sh
python3 -B hadwiger_nelson_parts159_three_rotations_review1/independent_audit.py
python3 -O -B hadwiger_nelson_parts159_three_rotations_review1/independent_audit.py
python3 -B hadwiger_nelson_parts159_three_rotations_review1/controls.py
python3 -B hadwiger_nelson_parts159_three_rotations/verify.py --check-expected
python3 -O -B hadwiger_nelson_parts159_three_rotations/verify.py --check-expected
python3 -B hadwiger_nelson_parts159_three_rotations/controls.py
```

The independent main audit uses only the Python standard library.  Expected
output is checked internally against `EXPECTED.json`; controls similarly
check `EXPECTED_CONTROLS.json`.

The small secondary symbolic audit requires SymPy 1.14.0:

```sh
python3 -m venv /tmp/parts159-review-sympy
/tmp/parts159-review-sympy/bin/pip install 'sympy==1.14.0'
/tmp/parts159-review-sympy/bin/python -B \
  hadwiger_nelson_parts159_three_rotations_review1/symbolic_audit.py
```

It checks `EXPECTED_SYMBOLIC.json`.  No SAT package is required.  The
independent main audit took about 132 seconds in the recorded environment;
the target verifier took about 77 seconds.  All inputs are small repository
files; no omitted search output or external data download is needed.
