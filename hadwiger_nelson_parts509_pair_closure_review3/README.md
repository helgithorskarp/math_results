# Review of the Parts-509 two-point closure

## Verdict

The central certificate and the resulting local exclusion theorem are accepted
with high confidence, conditional on the separately reviewed criticality and
one-point swap-closure/census contributions.  For the fixed strict 2,442-edge
Parts graph, every graph obtained by deleting three base vertices and adding
two distinct plane points is 4-colourable.  This is a complete result about
that finite edit neighbourhood, not a 508-vertex lower bound for arbitrary
unit-distance graphs and not an improvement of the chromatic-number bounds for
the plane.

There is one minor but definite descriptive error.  The target contribution
and its README classify the 63 pairs with `|U(A)| = 2` as 55 pairs of swap
points, six pairs among the four degree-10 completion points, and four further
pairs.  That would total 65.  The certificate instead gives the correct
classification

```text
55 swap-point pairs + 4 degree-10 pairs + 4 mixed pairs = 63.
```

Among degree-10 indices `{0,1,2,3}`, the double-critical pairs are `(0,1)`,
`(0,3)`, `(1,2)`, and `(2,3)`, all with `U={350,353}`.  Pairs `(0,2)` and
`(1,3)` have empty `U`.  This does not affect the theorem: both target
checkers reconstruct `U` from the uncovered instances and prove that no pair
has `|U| >= 3`.

## Reproduction

The artifact was inspected at its stated source commit
`50d4b7e186cd4bd8588762eae984e24da49b0858`.  The pair-closure directory is
unchanged between that commit and the review checkout.  With CPython 3.11,
SymPy 1.14.0, and NumPy 2.4.6, both solver-free commands passed under one CPU
core and one process group:

```bash
python pair_certificate.py verify \
  ../hadwiger_nelson_parts509_swap_closure/completion_points.json \
  pair_certificate.json --skip-enumeration --workers 1

python independent_pair_check.py \
  ../hadwiger_nelson_parts509_swap_closure/completion_points.json \
  pair_certificate.json
```

The primary replay took 80.5 seconds.  It recomputed all incidences among the
listed points and reported:

```text
q3_points=1158  q3q3_unit_pairs=3744
pair_instances=340980627  colourings_checked=3680
retained_edge_checks=8951669  declared_instances=12901
pairs_with_nonempty_U=12838  U_histogram={1:12775,2:63}
pairs_with_U_ge3=0  all_checks=true
```

The source-independent checker took 1,225 seconds.  It reconstructed 509
algebraic points and 2,442 exact base edges in SymPy's degree-eight field,
checked rational coefficient vectors for all 1,667 points, used two ring
homomorphisms to screen incidences before exact confirmation, decoded the rows
with separate code, and replayed coverage with pure-Python bitmasks.  It
returned the same counts and `all_checks=true`.

Run the compact reviewer-owned metadata audit from this directory:

```bash
python3 audit_declared_sets.py \
  ../hadwiger_nelson_parts509_pair_closure/pair_certificate.json \
  ../hadwiger_nelson_parts509_swap_closure/completion_points.json \
  ../hadwiger_nelson_parts509_pair_closure/swaps.json
```

It uses only the standard library.  It checks payload hashes and lengths,
validates every declared-pair index, reconstructs `U`, compares all stored
`|U|=2` metadata, verifies the `12,727 + 174 = 12,901` split, and confirms the
corrected `55 + 4 + 4 = 63` classification.

Pair-certificate SHA-256:
`bba74f49405e408238394c8c1cd8a8c8fdb0a631d9d91056ece372bcb018cf40`.
Reviewer checker SHA-256:
`0fdca810333dc36da833d812c0ccc0bc377a5c11b5c04c9c1d2c6be3de85e751`.

## Proof audit

For a pair `A={q1,q2}` in the complete external-point census, let `U(A)` be
the base vertices `u` for which the checked family supplies no extension of a
4-colouring of `G-u` to both points.  If `G-D+A` were 5-chromatic with
`|D|=3`, then its supergraph `G-u+A` would be 5-chromatic for each `u in D`.
Every nondeclared instance has a checked 4-colouring, so `D` would be a subset
of `U(A)`.  The independently replayed bound `|U(A)|<=2` is a contradiction.

The free-colour test is exact.  Each added point must have a nonempty set of
available colours; if the two points are adjacent, a joint extension fails
exactly when both available sets are the same singleton.  Deleting more base
vertices cannot invalidate an extending colouring.

The all-plane reduction is also sound.  An added point already in the base
set reduces to a one-addition graph with at least two base deletions.  An
external point with at most two base neighbours has degree at most three after
the other new point is included, so a 4-colouring of the remaining graph
extends greedily.  Thus only the exact `Q3` census matters.  Completeness of
that census and the one-point colouring statement are imported dependencies,
not re-proved by this review; they already have a committed independent review
including a separate exhaustive circumcircle-triple count.

The 174 solver-reported instances need not actually be non-4-colourable for
the exclusion theorem.  Treating them as uncovered only enlarges `U(A)`, and
the checked enlarged sets still have size at most two.  Their claimed
5-chromaticity remains outside this certificate's proved content.

## Trust boundary and improvement opportunities

The finite evidence trusts the published coordinate input, CPython and JSON
decoding, SymPy 1.14.0, NumPy, and two independently structured checker
implementations.  The universal-plane statement additionally imports the
reviewed exact completion-point census and one-point closure.  There is no
proof-assistant formalization, and this review did not rederive the Parts
coordinates from the paper.

The immediate repair is to change “six pairs” to “four pairs” and explicitly
name the two empty-`U` degree-10 pairs.  The primary verifier should also
compare its reconstructed histogram and pair lists to the stored metadata;
currently it prints the derived histogram but does not assert equality with
all redundant summary fields.  A higher-value next step is to investigate the
63 double-critical pairs as candidate 509-vertex replacements, while keeping
solver lower-bound claims separate from the solver-free exclusion theorem.

Jaan Parts's primary paper describes the 509-vertex, 2,442-edge graph and its
general minimization method, including the observation that simple
two-for-one replacement usually fails to escape a local minimum:
<https://arxiv.org/abs/2010.12665>.  It does not state this exhaustive
delete-three/add-two closure.  Targeted searches found no primary publication
with the exact closure or counts, but that is not a historical-priority proof.
