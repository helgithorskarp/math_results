# Unrestricted three-branch point-link factorization for `good43`

This directory gives an exact, catalog-free construction theorem for the
open `R(5,5)` endpoint.  If a 43-vertex coloring with no monochromatic `K_5`
exists, then after exchanging colors and choosing a minimum-degree root it is
in exactly one of three link branches:

```text
root red degree       link sizes       cross-matrix variables
18                    18 + 24                 432
19                    19 + 23                 437
20                    20 + 22                 440
```

Conversely, satisfying any branch's link conditions and all its active
width-four/width-six cross clauses reconstructs a literal physical `good43`.
This covers every unrestricted candidate: no automorphism, regularity,
catalog, or preselected carrier is assumed.

The companion event-core lemma supplies global feedback.  If a certified
unsatisfiable collection of cross clauses has internal activation support
`P`, then one sound master clause excludes every link assignment extending
`P`.  This is the route from conditional cross proofs back into the complete
three-branch problem.  See [PROOF.md](PROOF.md) for the exact statement and
its cardinality caveat.

This is endpoint-facing reduction, not endpoint movement: the package does
**not** contain a `good43`, a branch exclusion, or a new Ramsey bound.

## Reproduce the checks

Only CPython 3.11 or later and the standard library are required.

```bash
make check
```

The check performs:

* exhaustive factorization identities for all 33,867 labeled graph words of
  orders one through six and every one of their 202,013 rooted views;
* the same controls with Python assertions disabled;
* exact comparison of the three target branches with
  [expected_target.json](expected_target.json);
* two physical audits of the bundled good42 calibration, one of which imports
  no factorization code and directly scans all 850,668 five-subsets; and
* SHA-256 verification of every immutable source and fixture.

The bundled [calibration_good42.hex](calibration_good42.hex) is only a positive
fixture for the construction interface.  It has 427 red edges, red-degree
range 19--22, zero monochromatic five-sets, and 59,934 active cross clauses at
root zero.  It is not a 43-vertex target graph and carries no priority claim.

Individual entry points are:

```bash
python3 -B factorization.py --target-spec
python3 -B factorization.py --n 42 --root 0 \
  --hex "$(tr -d '\n' < calibration_good42.hex)"
python3 -B verify_physical.py
```

The hexadecimal convention lists lexicographic edge bits `(0,1),(0,2),...`
in the low-to-high bit order of each successive hexadecimal digit.

## What is exact and what remains

There are 903 physical edge coordinates.  Fixing the root colors leaves 861
free variables, divided into 421--429 internal link variables and 432--440
cross variables.  The outer link CNFs have 53,998--64,758 clauses.  Once a
link is fixed, its cross clauses are exactly all remaining possible
monochromatic `K_5` obstructions, so a satisfying cross matrix is independently
checkable as a physical graph.

The next falsifiable endpoint milestone is to run a proof-producing outer/
inner solver over all three branches, use only checked event cores for learned
master clauses, and either output a physically verified `good43` or close a
whole branch with replayable certificates.  Solver timeouts, defect records,
and isolated fixed-link failures do not count.

## Literature and relationship to prior work

The sole non-elementary input is McKay and Radziszowski's classical
[`R(4,5)=25`](https://doi.org/10.1002/jgt.3190190304), used to force every
red degree into 18--24.  The current global context is Angeltveit and McKay's
[`R(5,5)<=46`](https://arxiv.org/abs/2409.15709).

This package generalizes the repository's earlier
[`21+21` doubly-exact cross normal form](../ramsey_r55_doubly_exact_cross_normal_form),
which applies only after a catalog-dependent hard-branch theorem.  Here the
sparse-color/minimum-root choice supplies an exhaustive `18/19/20` split for
the unrestricted problem.  Repository and Discovery Net overlap were checked
at the pass boundary; novelty is asserted only relative to those searched
records, not the historical literature.
