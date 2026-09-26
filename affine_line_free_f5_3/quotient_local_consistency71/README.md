# A universal obstruction to local quotient lifting tests

**Theorem.** Every integer quotient of total 71 with fiber weights at
most four and quotient line weights at most sixteen admits line-free
lifts of all 30 projection planes whose **full shared-fiber marginal
distributions agree**. The construction also satisfies the no-four-
collinear condition in plane sections of size at most ten.

Thus independent planar feasibility and complete overlap consistency
on the fibers cannot exclude any admissible 71-weight quotient.
The [proof](PROOF.md) identifies the missing requirement: one common
distribution, or one integral assignment, across all projection planes.

The mechanism is constructive: thirteen small planar templates realize
every required fiber profile, and a 100-element affine group makes the
overlap laws uniform. Any two prescribed missing heights in full fibers
also extend inside one plane. Consequently every individual plane
survives a three-hole gauge at noncollinear quotient positions. The
full marginal-consistency claim is **ungauged**; the stronger gauged
relaxation remains open.

The proof also glues any chosen collection of projection planes when
all shared fibers have weight four and each plane has at most two of
them. This includes triangles of planes with three distinct full-fiber
intersections, and identifies which more complicated arrangements need
to be investigated.

This is a method obstruction for the exact 70-versus-71 problem. It
does not construct or exclude a 71-point set. An explicit 72-weight
control has all the local distributions but no global lift, using the
team's separate [upper-bound theorem](../upper_bound71/README.md).

## Replay

Python 3.10+ and a C++20 compiler named `g++` suffice. No optimizer,
Python package, external catalogue, or network access is required.
From the repository root:

```sh
python3 affine_line_free_f5_3/quotient_local_consistency71/verify.py \
  --out /tmp/quotient-local-check --check-expected
python3 -O affine_line_free_f5_3/quotient_local_consistency71/verify.py \
  --out /tmp/quotient-local-optimized --check-expected
python3 affine_line_free_f5_3/quotient_local_consistency71/verify.py \
  --out /tmp/quotient-local-sanitized --sanitize --check-expected
```

Expected status: `UNIVERSAL_QUOTIENT_LOCAL_CONSISTENCY_VERIFIED`.
The verifier constructs and checks all 3,069 ordinary and 903 small-section
profiles, the affine averaging laws, all 775-line coverage incidences,
and the 71- and 72-weight controls. It also rechecks the planar maximum
16. Verification remains active under Python `-O`.

`model.py` exposes `lift_profile`, `height_images`, and `local_family`.
The latter returns compatible local distributions and must not be used
as a global-lift decoder. The controls explicitly show that conditioning
our recipe on the height gauge can destroy marginal consistency.

See [SOURCES.md](SOURCES.md) for dependencies and
[VALIDATION.md](VALIDATION.md) for the author audit. No independent
peer review, new numerical bound, or historical priority is claimed.
