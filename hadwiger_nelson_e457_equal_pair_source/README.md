# A 457-point physical equal-pair source

## Exact result

There is an explicit strict plane unit-distance graph `E457` with **457
distinct points and 2,329 complete unit edges**.  It is four-colourable, but
in every proper four-colouring its marked vertices `O,V` have the same colour.
Their Euclidean distance is `8/3`.

This improves the 477-point equal-pair source inside the earlier E477
construction by 20 vertices.  It is not claimed vertex-minimal, and it is not
a five-chromatic graph or progress below the 509-point record by itself.

The standard two-half spindle still has the raw lower bound

```text
2*457-1 = 913,
```

so this source does not reopen the closed E477 marked-pair spindle family.
Its construction value is a different one-half composition: any physical
connector on at most 53 points, sharing `O,V` and forcing them different in
four colours, would have total order at most `457+53-2=508` before additional
collisions.  No such connector is supplied here.

## Exact physical graph

The rows in `core.json` use the inherited E477 coordinate convention

```text
(a,b,c,d) = ((a*sqrt(3)+b*sqrt(11))/36,
             (c+d*sqrt(33))/36).
```

The checker proves tuple distinctness and expands the squared distance of all
`C(457,2)=104,196` point pairs.  For a difference row `(a,b,c,d)`, the squared
distance is

```text
(3*a*a + 11*b*b + c*c + 33*d*d
 + 2*(a*b+c*d)*sqrt(33))/1296.
```

Thus unit distance is the exact pair of integer conditions

```text
3*a*a + 11*b*b + c*c + 33*d*d = 1296,
a*b + c*d = 0.
```

No inherited-edge assumption or numerical tolerance enters the 2,329-edge
reconstruction.  The listed 457-colour word is then checked on every edge and
has `colour(O)=colour(V)`.

## Four-colour impossibility certificate

The contrary query fixes `colour(O)=0`, `colour(V)=1`; colour permutation makes
this complete for unequal marked colours.  The canonical direct encoding has
1,828 variables and 12,517 clauses: exactly one of four colours per vertex,
four inequality clauses per unit edge, and the two pins.

Glucose 4.2 generated a DRUP proof.  `drat-trim` removed unused lemmas and
verified the retained ASCII DRAT proof; the xz-compressed trace is committed as
`state.drat.xz`.  The final trace has 131,322 retained lemmas, all RUP (zero RAT
lemmas), and used 10,363,903 resolution steps in the trimming replay.  The
canonical CNF is `state.cnf`.

A separate deterministic C++ exhaustive search is included.  It visits
1,348,142 nodes and 674,115 conflicts before rejecting the unequal pins.  This
duplicates the decision with a different proof mechanism; it is not an
independent-author review.

## Reproduction

CPython 3.11 or later and a C++17 compiler reconstruct the graph and replay the
small exhaustive checker:

```sh
g++ -std=c++17 -O3 -Wall -Wextra -pedantic \
  hadwiger_nelson_e457_equal_pair_source/colour_check.cpp \
  -o /tmp/e457-colour-check
python3 -B hadwiger_nelson_e457_equal_pair_source/build.py \
  --out /tmp/e457-state.cnf
cmp hadwiger_nelson_e457_equal_pair_source/state.cnf /tmp/e457-state.cnf
python3 -B hadwiger_nelson_e457_equal_pair_source/verify.py \
  --checker /tmp/e457-colour-check
python3 -B hadwiger_nelson_e457_equal_pair_source/controls.py
sha256sum -c hadwiger_nelson_e457_equal_pair_source/SHA256SUMS
```

For proof-trace replay, build `drat-trim` from upstream commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` (the generation run used the
repository copy from this commit) and run:

```sh
python3 -B hadwiger_nelson_e457_equal_pair_source/verify.py \
  --checker /tmp/e457-colour-check --drat-trim /path/to/drat-trim
```

The verifier decompresses the trace to a temporary directory and requires the
proof checker to return success.  The trace was also converted to LRAT and
accepted by upstream `lrat-check`; that larger intermediate is not committed.

## Construction history and boundary

Starting from E477, a deterministic seed-zero pass considered the 222 vertices
outside the already published 255-vertex mandatory set.  A vertex was deleted
only when the exact marked-different query remained UNSAT.  Twenty deletions
survived; all 202 rejected deletion attempts returned directly checked proper
four-colourings.  This describes the discovery order, not a minimality proof.

The first capped connector interaction was also tested before publication.
The natural radius-four closure of an axis point on the two unit circles about
`O,V` has 47 formal interior points.  After alignment with E457 it has 17
collisions, giving a 487-point floating support with 2,425 apparent unit edges,
including 73 source-to-connector contacts.  A checked proper four-colouring
retains `O=V`, so that connector relation is neutral.  Because this is
floating selector evidence, it is not an exact family theorem.  The connector
is retired without a larger shell or seed sweep.

The exact theorem in this directory concerns E457 only.  It separates an
improved physical forcing source from the failed first whole composition and
from the global sub-509 record objective.

The E477 coordinates and equality premise were first published in repository
commit `5b28dad38f14e0979a10feb436c95e453dbb34d5`; `core.json` is self-contained,
so replay does not import that parent package.  The 509-point, 2,442-edge Parts
construction remains the working published vertex record.

