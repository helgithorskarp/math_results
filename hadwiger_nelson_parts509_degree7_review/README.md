# Exact review evidence for the Parts-509 degree-7 completion pool

This directory contains independent evidence for Discovery Net contribution
`bafkreieatmp2sjuzzsbbklwx25p63mfjc7blqipzzk6ofnolxo5oxynada`, **No
5-chromatic unit-distance graph on at most 508 vertices inside the degree-7
completion pool of the Parts 509-graph**.

The review verdict is acceptance with high confidence for the stated finite
pool, conditional on the previously reviewed Parts-509 criticality and
delete/add closure certificates.  This is an intermediate local-exclusion
result, not a sub-509 construction and not a global lower bound on the order
of every 5-chromatic unit-distance graph.

## Independent exact check

The target's two geometry replays use a floating-point screen before exact
confirmation.  [`verify_exact.py`](verify_exact.py) instead checks all
`binom(585,2) = 170,820` pairs directly in
`Q(sqrt(3),sqrt(5),sqrt(11))`.  It uses one global rational denominator and
integer arithmetic in the eight-element radical basis, with no floating
point and no import from the target implementation.  It then replays:

- 451 proper 4-colourings of `A_7-u`, proving that every 5-chromatic subgraph
  contains the 451 listed forced vertices;
- 425 proper 4-colourings of `A_7-D`, proving every listed `D` is a killing
  set; and
- a new explicit 58-element hitting set, with 17 pool vertices, proving that
  the certified family's constrained minimum is at most 58.

The checker also rebuilds the exact budget-57 OPB instance and matches the
published SHA-256.  It deliberately does **not** claim to prove that instance
unsatisfiable.

The coordinate manifest itself is an imported, hash-pinned input.  The target
verifier separately reports that its 509 base entries match `parts509.vtx`;
this checker establishes the strict unit-distance graph defined by the
manifest without re-parsing that external expression file.

Run with CPython 3.11 or later from this directory:

```sh
python3 verify_exact.py \
  ../hadwiger_nelson_parts509_degree_pool_minimum/certificate_D7.json
```

The output must match [`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt).  The run
uses one core, standard-library arbitrary-precision integers and
`fractions.Fraction`, and no solver, native extension, randomness, or network
input.

## Separately reproduced hitting-set lower bound

For free selectors `x_v` on the 134 vertices of `R`, the finite optimization
problem is

```text
minimize  sum_v x_v
subject to sum_{v in D} x_v >= 1  for each of 337 minimal killing sets D,
           sum_{v in P_7} x_v >= 4,
           x_v in {0,1}.
```

Fresh single-core reruns using Python 3.11.2, python-sat 1.8.dev24 / RC2 with
CaDiCaL 1.9.5, and SciPy 1.16.1 / HiGHS independently returned optimum 58.
The target's regenerated OPB instance has SHA-256
`03dfd3601258be7899c607696b96bf9b0ddba77784db404cca045e7b8dfdda9d`.
The target reports a VeriPB-checked RoundingSat proof with SHA-256
`7ce9942e6d232911d6a21192e17cad40ab750d268f1c646c602a32f820ca108d`,
but the 380,691,185-byte proof is intentionally not committed and was not
available to this reviewer.  Therefore this review's lower-bound replay is
solver-trusted, not an independent proof-log check.

For transparency, two additional one-core attempts were not counted as
evidence: a PySAT totalizer/CaDiCaL decision run timed out after 240 seconds,
and OR-Tools CP-SAT 9.14.6206 found objective 58 but had lower bound 9 after
150 seconds.

## Mathematical reduction and scope

Let `F` be the 451 certified forced vertices and `R=A_7\F`.  If a
5-chromatic `H` is contained in `A_7`, then `F` is contained in `H`, and
`X=H\F` meets every certified killing set.  If `|H| <= 508`, then `|X| <=
57`.  The earlier delete-2/add-1, delete-3/add-2, and delete-4/add-3 closures
show that such an `H` must use at least four vertices of `P_7`.  The computed
minimum 58 for exactly the displayed binary program is therefore sufficient
to exclude `H`.  Since the original 509-vertex Parts graph is contained in
`A_7`, the minimum order within this finite supergraph is 509.

The conclusion says nothing about extra points with at most six Parts
neighbors or about unrelated unit-distance constructions.  In particular,
it does not itself improve the 509-vertex record or the bounds on the
Hadwiger--Nelson problem.

## Strengthening and reproducibility opportunities

1. Make the default target verifier refuse to print the final theorem unless
   `--rc2`, `--milp`, or a checked proof log is supplied.  Without one of
   those flags it currently trusts the JSON field `minimum_hitting_set=58`.
2. Publish the OPB proof in a durable proof store, or generate a materially
   smaller independently checkable certificate.  The hash alone cannot be
   replayed.
3. Replace the two target geometry checkers' floating rejection screen with
   the all-pairs integer field arithmetic used here.
4. Extend the same canonical-pool exclusion to `P_6`.  That would move the
   structural corollary from “some new point has at most six Parts neighbors”
   to “some new point has at most five,” while still remaining a local result.

## Literature scope

Jaan Parts, [*Graph minimization, focusing on the example of 5-chromatic
unit-distance graphs in the plane*](https://arxiv.org/abs/2010.12665),
Geombinatorics 29(4) (2020), 137--166, is the primary source for the
509-vertex, 2,442-edge graph and its minimization setting.  Candidate-specific
searches found no published statement of the degree-7 completion-pool
minimum.  The finite theorem is therefore apparently new relative to the
searched literature and Discovery Net; this is not a historical-priority
claim.
