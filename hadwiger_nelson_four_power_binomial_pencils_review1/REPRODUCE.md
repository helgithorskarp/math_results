# Reproduction

Run from the root of a complete `helgithorskarp/math_results` checkout.
Tested versions are CPython 3.11.2, SymPy 1.14.0, and python-flint 0.8.0.

```sh
python3 -m venv /tmp/hn-binomial-review-venv
/tmp/hn-binomial-review-venv/bin/pip install sympy==1.14.0 python-flint==0.8.0
```

Regenerate and verify the uncommitted target table:

```sh
/tmp/hn-binomial-review-venv/bin/python -B hadwiger_nelson_four_power_binomial_pencils/produce.py \
  --jobs 8 --out /tmp/hn-binomial-roots.json
/tmp/hn-binomial-review-venv/bin/python -B hadwiger_nelson_four_power_binomial_pencils/verify.py \
  --jobs 8 --certificate /tmp/hn-binomial-roots.json --check-expected
```

Run the independent reverse-projection and physical audit:

```sh
/tmp/hn-binomial-review-venv/bin/python -B \
  hadwiger_nelson_four_power_binomial_pencils_review1/independent_audit.py \
  --pencils hadwiger_nelson_four_power_binomial_pencils/PENCILS.json \
  --certificate /tmp/hn-binomial-roots.json --jobs 8 --check-expected

/tmp/hn-binomial-review-venv/bin/python -B \
  hadwiger_nelson_four_power_binomial_pencils_review1/independent_controls.py \
  --certificate /tmp/hn-binomial-roots.json --check-expected
```

Run all compact target controls:

```sh
/tmp/hn-binomial-review-venv/bin/python -O -B hadwiger_nelson_four_power_binomial_pencils/controls.py --certificate /tmp/hn-binomial-roots.json
/tmp/hn-binomial-review-venv/bin/python -O -B hadwiger_nelson_four_power_binomial_pencils/boundaries.py --certificate /tmp/hn-binomial-roots.json
/tmp/hn-binomial-review-venv/bin/python -O -B hadwiger_nelson_four_power_binomial_pencils/cache_audit.py --certificate /tmp/hn-binomial-roots.json
/tmp/hn-binomial-review-venv/bin/python -O -B hadwiger_nelson_four_power_binomial_pencils/fiber_controls.py
/tmp/hn-binomial-review-venv/bin/python -O -B hadwiger_nelson_four_power_binomial_pencils/classification.py
/tmp/hn-binomial-review-venv/bin/python -O -B hadwiger_nelson_four_power_binomial_pencils/corollary.py
/tmp/hn-binomial-review-venv/bin/python -O -B hadwiger_nelson_four_power_binomial_pencils/pins.py
```

The full optional target `--literal-distances` run was not needed for this
review.  The independent checker instead derives raw norm equations from the
definition, partitions all 29,403 label pairs into 2,801 exact unit-rotation
classes, and expands every class after collision quotienting.  Target controls
also compare literal and cached edge lists on a high-degree injective fixture
and four collision fixtures.
