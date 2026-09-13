# Reproduction

Run from the root of the complete `helgithorskarp/math_results` checkout.
The package imports the pinned h4105 norm architecture and exact C0 helpers
from other directories in this repository. `SOURCE_PINS.json` also pins the
prior proof statements and finite interfaces used by the homogeneous-pencil
corollary. Source pins are checked automatically; no Discovery Net service or
private data is needed to reproduce the theorem.

Tested environment: CPython 3.11.2, SymPy 1.14.0, python-flint 0.8.0. A fresh
local environment can be prepared with:

```sh
python3 -m venv /tmp/hn-binomial-venv
/tmp/hn-binomial-venv/bin/pip install sympy==1.14.0 python-flint==0.8.0
```

Use that environment's Python for the commands below if the dependencies are
not already installed. The final package needs no SAT solver and no floating
point tolerance.

## Generate and check

```sh
python3 -B hadwiger_nelson_four_power_binomial_pencils/produce.py --jobs 4 --out /tmp/hn-binomial-roots.json
python3 -B hadwiger_nelson_four_power_binomial_pencils/verify.py --jobs 4 --certificate /tmp/hn-binomial-roots.json --check-expected
python3 -O -B hadwiger_nelson_four_power_binomial_pencils/controls.py --certificate /tmp/hn-binomial-roots.json
python3 -O -B hadwiger_nelson_four_power_binomial_pencils/boundaries.py --certificate /tmp/hn-binomial-roots.json
python3 -O -B hadwiger_nelson_four_power_binomial_pencils/fiber_controls.py
python3 -O -B hadwiger_nelson_four_power_binomial_pencils/cache_audit.py --certificate /tmp/hn-binomial-roots.json
python3 -O -B hadwiger_nelson_four_power_binomial_pencils/classification.py
python3 -O -B hadwiger_nelson_four_power_binomial_pencils/corollary.py
python3 -O -B hadwiger_nelson_four_power_binomial_pencils/pins.py
```

The last three commands use only the Python standard library. All checks
must report `PASS`; the separate `EXPECTED_*.json` files pin the corresponding
compact outputs. The first command constructs the full component table;
the verifier checks every pair and every component, not a sample.

The 8,605,469-byte generated table has SHA-256:

```text
b2e970417d8ed72882305a0d64d2c3992e0fa38478b67bcbd1c2d8dd641ff095
```

It is deliberately kept outside the repository. Worker counts between 1 and
8 are supported. Ordered task collection and canonical field encodings make
the output independent of worker scheduling. An interrupted or failed run
is incomplete; a partial log is not a certificate. Preserve a running job
until it completes or report explicitly why it was stopped.

## Independent checks and optional literal distances

The producer solves the transformed equations in u=x+2y. The verifier
computes the original unshifted resultant and square-free fiber cardinalities.
It substitutes every supplied component into the original equations, checks
that the components are distinct, and requires exact coverage of every fiber.
It does not invoke the producer or solve away the nonlinear unshifted fibers.

The physical verifier constructs all 243 digit points, merges exact
coincidences, examines every pair of distinct physical points, and computes
unit norms directly. Its cache only groups formal displacements differing by
an exact Eisenstein-unit rotation. The proof explains why this preserves every
distance decision. To evaluate every squared norm separately, use:

```sh
python3 -B hadwiger_nelson_four_power_binomial_pencils/verify.py --jobs 4 --certificate /tmp/hn-binomial-roots.json --literal-distances --check-expected
```

This produces the same mathematical output and is slower. The published
validation uses the full cached verifier and compares complete literal and
cached edge lists on algebraic and collision fixtures. It does not claim a
full literal replay at all 4,320 parameters. The generic degree-23 fixture
reduced 29,403 norm evaluations to 2,801; measured times were about 14.17 and
1.61 seconds, respectively. These timings are not a promised whole-run speedup.

## Optional historical residual alignment

The intrinsic theorem and its reproduction do not require the old residual
export. `RESIDUAL.json` contains all 162 retained binomial pencils with their
literal h4195 indices. To verify that alignment, regenerate the historical
export following
`hadwiger_nelson_radix_pair_exclusion_propagation/REPRODUCE.md`, then add
`--residual /path/to/residual.json` to the generator or verifier.

The expected canonical residual SHA-256 is
`42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d`;
the file SHA-256 is
`734286535020a4fc4ccbaac44a8a24c4b775d89854de6515c25b45353b93dc4b`.
No h4117/h4175/h4177 allowance is imported or changed.

## Proof premises and validation boundary

`corollary.py` checks the complete entrywise partition of all 279 homogeneous
nonmonomial pencils between this package and the prior three-position and
four-position no-binomial packages. It does not re-prove those two theorems;
their proof sources and independent reviews are cited in `CONTEXT.json`.
The current exact reductions and physical checks remain unformalized, and
independent-author review of this package is outstanding.
