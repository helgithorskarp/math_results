# A universal obstruction after fixing the height gauge

Every admissible 71-weight quotient has compatible full-fiber planar
marginals **even after the three-hole gauge is fixed**. In fact the
local laws can all avoid any prescribed transverse affine plane, fixing
every weight-four fiber's hole on that plane. Small sections of size at
most ten still contain no four collinear points.

These local laws cannot glue: a genuine line-free set avoiding a plane
has at most **64** points. The [proof](PROOF.md) constructs the laws
uniformly for every quotient, using a cyclic hole construction and
fourteen small templates. It needs no solver or catalogue.

This closes the height-gauge gap in the [previous obstruction](../quotient_local_consistency71/README.md).
It gives **no new bound on the original extremal problem**, whose value
remains 70 or 71. Adding other plane constraints rejects the displayed
certificate; feasibility of that larger model is not asserted.

## Exact replay

Python 3.10+ and a C++20 compiler named `g++` suffice. From the repository:

```sh
python3 affine_line_free_f5_3/gauged_quotient_obstruction71/verify.py \
  --out /tmp/gauged-quotient-check --check-expected
python3 -O affine_line_free_f5_3/gauged_quotient_obstruction71/verify.py \
  --out /tmp/gauged-quotient-optimized --check-expected
python3 affine_line_free_f5_3/gauged_quotient_obstruction71/verify.py \
  --out /tmp/gauged-quotient-sanitized --sanitize --check-expected
```

Expected status: `UNIVERSAL_GAUGED_MARGINAL_OBSTRUCTION_VERIFIED`.
The audit checks all 3,972 full profile distributions, including their
exact subset marginals and every thinning outcome; all 101 top small
profiles; all 775 spatial lines; and the 64-point sharpness control.
It independently replays all 1,081,575 planar 17-subsets.

`model.family71(weights)` returns local probability distributions.
They are explicitly **not** a global witness decoder. Every one of
these returned families has been constructed to be globally unglueable.

See [SOURCES.md](SOURCES.md) for dependencies and [VALIDATION.md](VALIDATION.md)
for the audit scope. Compact exact expected results and template data
are included. No optimizer, Python package or network is needed to replay.
