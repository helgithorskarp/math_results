# Two explicit hole traps for Schur-six support exchanges

No complete six-colouring of `[1,537]` or new numerical Schur bound is
claimed. The four supplied words are proper **partial** colourings, each
with one unfilled point. Zero means unfilled. Having 536 assigned points
is not a colouring of the interval `[1,536]`.

This construction checkpoint identifies an exact limitation of a natural
move that changes the support of colour 6. This is a follow-up construction
route to the [reviewed mixing result](../../schur_s6_three_way_mixing/README.md).
It allows the current sixth class to split among all six colours; that
older theorem concerns the different, printed536 baseline. The move
does produce large, valid trades, but neither of the two specific inputs
below can be completed in one such move.

## The operation and exact claim

Fix a partial word `w`. A **support exchange** produces `v` as follows:

* An old point of colour `c` in 1, ..., 5 may retain `c`, become6, or become
  the new hole.
* An old point of colour 6 may receive any of 1, ..., 6, or become the hole.
* The old hole must receive one of 1, ..., 6.
* At most one new hole is allowed, and every fully assigned equation
  `x+y=z` must have more than one colour, including when `x=y`.

Every position is independent. There is no equality imposed on translated
positions, no prescribed sixth support, and no symmetry restriction.

The following two statements have independently checked DRAT proofs:

| Fixed input | Old hole | Every admissible support exchange has its hole at |
| --- | ---: | ---: |
| [`initial.txt`](initial.txt) |322|161|
| [`traded.txt`](traded.txt) |161|322|

In particular neither input admits a full 537-colouring by this operation.
Both statements are attained: `initial_exchange.txt` and
`traded_exchange.txt` give literal positive witnesses for the indicated
hole positions. These are two fixed-input statements. They do not prove
that every iterated exchange stays in this pair of hole positions, or
exclude exchanges that allow other old classes to split among several
new colours.

## Construction data

The initial word comes from the five-colour 160-word in the earlier
[interval-tail trade data](../schur6_interval_tail_trades/data.json).
Repeat that word modulo 161 outside colour 6 support
`[78,154] union [460,537]`, with 161 and 322 initially unfilled. Give 161
colour 6 and restore 81,82,83 to their periodic colours. This leaves just
322 unfilled. The source five-word is not modularly sum-free: its one
unordered nonzero-output modular defect is 95+95=29 modulo 161, hidden
by the reserved intervals. Literal verification is supplied here, so
the present claims do not depend on trusting that construction argument.

Eight successive solver-found support exchanges preserved a single hole.
The fifth produced `traded.txt`, whose hole is 161. Colouring that point 6
creates exactly

```
161 + 161 = 322
161 + 322 = 483
```

and no other monochromatic equation. Removing 322 instead gives the
positive witness `traded_exchange.txt`. The traded word has only 43 points
of colour 6 and changes many other positions; it is not merely the original
three-point support adjustment. These near words are search inputs, not
lower-bound certificates. No historical novelty is claimed for periodic
lifting or support exchanges.

`trade.py` provides the exact search operator, phase hints, seeds and
literal acceptance gate. To reproduce the bounded walk in the pinned
environment, from this directory:

```
python3 -B trade.py --input initial.txt --out /tmp/schur-star-walk --seconds 90 --budget 3000 --steps 24 --size 6 --family star --mobile --seed 171701
```

The recorded run accepted 8 partial words, with holes alternating 161,322,
then returned UNKNOWN at its next query. Its best direct filling had the
two defects displayed above. Solver UNKNOWN is not an exclusion. Replaying
a bounded search can depend on environment and timing; the explicit word
and its exact checks are the evidence for the positive statements.

## Encoding, certificates and independent checks

`certify.py` has one Boolean variable for each allowed `(position,state)`.
Exactly-one clauses select its state. A negative clause forbids each
monochromatic Schur equation for each colour available at every involved
point; doubled variables are collapsed. Pairwise negative clauses permit
at most one zero. Finally the purported unique new hole is forbidden.
Thus a satisfying assignment would be precisely a counterexample to the
corresponding fixed-input statement, including a possible full colouring.
All clauses are necessary and sufficient for the stated operation.

The encoder performs an independent endpoint-order clause comparison.
The separate standard-library `verify.py` imports neither generator nor
solver. It verifies all four words against all 72092 unordered equations
(268 doublings), checks both positive exchanges and the two explicit
defects, and can independently reconstruct each entire CNF multiset.

| Input | Variables | Clauses | Generated proof bytes |
| --- | ---: | ---: | ---: |
| initial |2226|241820|1957840|
| traded |1786|223802|330772|

Python 3.11.2, `python-sat==1.9.dev15`, its Glucose3 solver with proof
logging, and DRAT-trim source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` were used. Both independent
checker runs returned `s VERIFIED`; neither proof used a RAT step in
its retained core. CNF/proof hashes and checker provenance are in
`expected.json`. Generated CNFs and proof traces remain outside git;
the source regenerates them. Assertions must be enabled.

```
python3 -B verify.py
mkdir -p /tmp/schur-star-proof
python3 -B certify.py --input initial.txt --exclude-hole 161 --out /tmp/schur-star-proof/initial
python3 -B certify.py --input traded.txt --exclude-hole 322 --out /tmp/schur-star-proof/traded
python3 -B verify.py --cnfs /tmp/schur-star-proof
/path/to/drat-trim /tmp/schur-star-proof/initial.cnf /tmp/schur-star-proof/initial.drat
/path/to/drat-trim /tmp/schur-star-proof/traded.cnf /tmp/schur-star-proof/traded.drat
```

A fresh `certify.py` record marks `independently_proof_checked=false`:
that flag is deliberate until the separate checker has run. A bare
UNSAT status is not the certificate. The trust boundary consists of the
specified point operation, the independently audited CNFs, the checked
proof traces and literal word checks. No external peer review of this
new checkpoint is claimed.

## Consequence for the construction search

Moving the reserved sixth class and mixing it among all six colours was
useful, but one such exchange cannot repair either saved state. Trials
that also let one of the other five current classes receive arbitrary
colours remained UNKNOWN; they are not covered by these certificates.
That is a concrete wider trade direction. The
[2026 shifted-template paper](https://arxiv.org/abs/2607.15034) still uses
the [published lower bound 536](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).
This checkpoint does not change it.
