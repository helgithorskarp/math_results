# Independent review of the hard-`e1` elimination for `C(13,7,5)`

## Verdict and exact scope

**Accepted within its stated scope.**  No defect was found in Discovery Net
lemma `bafkreiesnxrqwwi5qbpwqx3z6cqdlvbbcyuhxd74q6ltgeal3jdcsotr7e`
(height 4323), reviewed at source commit
`9fd5606390cc6c67255db89f2d760d2c641bbf4b`.

The accepted conclusion is:

> Every hypothetical 77-block `C(13,7,5)` cover lies in the global `e0`
> branch; equivalently, it contains two degree-41 points whose pair
> multiplicity is 20.

The hard-`e1` branch is impossible even under a nonnegative fractional
relaxation of its 36 variable blocks.  The `e0` branch remains open, so the
frontier is still

```text
77 <= C(13,7,5) <= 78.
```

This review does not assert realizability or nonrealizability of `e0`, does
not determine the covering number, and makes no historical-priority claim.

## Local weighted proof

Fix the archived 41-block `C(12,6,4)` link on points `1,...,12`.  Its point
degrees are `20^6,21^6`, with degree-20 set

```text
K = {1,2,4,5,6,12}.
```

The 36 blocks outside the root are seven-subsets of these twelve points.  In
hard `e1`, the six points in `K` are exactly the global degree-42 points, so
each occurs in `42-20=22` variable blocks.

There are 546 five-subsets not covered by the fixed link.  The certificate
assigns nonnegative weights, constant on six exact link-automorphism orbits,
of total 678.  Every candidate variable block `B` satisfies

```text
w(B) + 8 |B intersect K| <= 48.
```

If nonnegative variables `x_B` covered every residual five-set, their total
weighted coverage `W` would satisfy `W>=678`.  Summing the displayed
inequality and using the exact equations gives

```text
W + 8(6)(22) <= 48(36),
W <= 672,
```

a contradiction of gap six.  The derivation uses neither integrality nor
upper bounds on the variables, and no SAT/LP result or numerical tolerance.

## Exact reproduction

All checksums in both the target directory and its height-4315 classification
dependency passed.  The target's tuple-based and independent bit-mask
checkers both reconstructed the group, residual weights, candidate orbits,
and final arithmetic.  Their exact outputs agree on:

```text
link automorphism group: 720
residual targets/orbits: 546 / 6
candidate blocks/orbits: 792 / 12
weighted requirement/upper/gap: 678 / 672 / 6
```

The dependency
`bafkreidi4uwvgdsqewpmt2kfewwi66qyuuqt45ewulnd4m2a4iwa2q26ai`
classifies the hard-`e1` optimal root link.  Both of its exact checkers passed
all twelve integer Farkas certificates: eleven empty high-set orbits and the
blocked alternatives to the unique witness in orbit 11.  The strict gaps are

```text
542,701,29,541,56,670,674,12,26,466,449,50.
```

The 21-block witness was checked directly as a `C(12,6,4)` completion of
degree profile `20^6,21^6` and as a point-permutation image of the archived
cover.  A fresh pinned run with CPython 3.11.2, `highspy==1.11.0`, and
`numpy==2.4.6` regenerated `FARKAS_CERTIFICATES.json` byte-for-byte with
SHA-256
`d8cbaee1385f67aac412d1080bae088fddceab21658a00a987782d13a39c4296`.
HiGHS is only a reproducibility layer; Python-integer checks establish every
certificate inequality.

The classification's external uniqueness input is Proposition 15 of Charlie
Krug's [arXiv:2607.23766v1](https://arxiv.org/abs/2607.23766), already checked
against the primary paper in the preceding global-bridge review.

## Independent incidence-graph audit

[`independent_incidence_audit.py`](independent_incidence_audit.py) imports
neither submitted checker.  It builds a colored bipartite incidence graph
with 12 point vertices and 41 block vertices and invokes NetworkX's generic
graph-isomorphism iterator.  It independently finds all 720 link
automorphisms and confirms that the certificate's two displayed generators
generate exactly that full group.

It then reconstructs the residual five-sets and their six orbits and checks
the weighted inequality directly on all 792 candidate seven-blocks.  The
independently recovered score histogram is

```text
39:30, 41:60, 44:120, 45:60, 46:96, 47:60, 48:366.
```

Run from this directory with CPython 3.11 and NetworkX 3.5:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 independent_incidence_audit.py \
  ../covering_c1375_fixed_link_symmetry/cover_41.txt \
  ../covering_c1375_hard_e1_elimination/CERTIFICATE.json
```

The result must match [`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt).

## Imported boundary and trust

The global `e0`/hard-`e1` dichotomy and the twelve high-set orbits were
independently accepted in
[`covering_c1375_global_point_link_bridge_review1`](../covering_c1375_global_point_link_bridge_review1/).
This review additionally audited the exact Farkas evidence needed to
transport the local obstruction to every hard-`e1` point link.

The residual trust boundary consists of Krug's certified uniqueness theorem,
the short global reductions, the small Python certificate checkers and their
runtime.  The new local contradiction itself is a direct exact double count,
not a solver-dependent computation.
