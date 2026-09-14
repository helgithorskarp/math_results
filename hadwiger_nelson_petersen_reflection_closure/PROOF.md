# Proof and verification boundary

## 1. Geometry

The certificate represents a point as eight rational coefficients of
`1,t,...,t^7`, with `t=exp(pi*i/10)`.  Since `Phi_20` is irreducible, these
form a rational basis.  Physical conjugation sends `t` to `t^(-1)`.
Therefore two rows are equal exactly when all coefficients agree, and a
difference polynomial `f` has squared Euclidean length one exactly when

```text
f(t) f(t^(-1)) - 1 = 0.
```

The verifier shifts this Laurent polynomial by `t^7` and checks exact
divisibility by the monic polynomial `Phi_20`.  This is an if-and-only-if
test, not a numerical filter.

The ten certified base rows are distinct.  Testing all 45 pairs yields
exactly the 15 Petersen edges.  The displayed formulas in the README derive
the same rows: `c*(zeta-1)=1`, outer consecutive differences are fifth roots
of unity, inner step-two differences have modulus one, and the quarter-turn
between the two radii makes each spoke unit.  The all-pairs test also excludes
unlisted contacts.

If `|p-r|=|q-r|=1`, then for `x=p+q-r`,

```text
x-p = q-r,       x-q = p-r.
```

Thus `x` is a common unit neighbour.  Conversely the construction definition
adds one such row for every unordered pair of distinct neighbours of every
current vertex; no geometric case is selected heuristically.  Sorting and set
deduplication merge every collision.  The verifier rebuilds the strict edge
set before each round and again on the final support.  It obtains the point,
edge, wedge, and next-round counts in `expected.json`.  In particular `S2`
has 290 distinct physical points and 865 complete unit edges, while `S3`
would have 2,085 points.

## 2. Exact chromatic number

The checker uses a direct finite-domain exhaustive search for three colours.
Domains are three-bit masks.  Assigning a singleton removes that colour from
every neighbour; an empty domain closes the branch.  Otherwise it chooses a
non-singleton vertex deterministically and branches over every colour still
in its domain.  Each branch fixes a new vertex, so recursion terminates and
covers all assignments compatible with the propagated choices.

The graph has an edge.  Any proper three-colouring can have the endpoints of
the first edge renamed to colours zero and one, so those pins lose no model.
All branches close in 11 recursive nodes.  Positive controls find a
three-colouring of both `S0` and `S1`.

Every one of the 540 relation witnesses is checked directly against all 865
edges.  Any one is a proper four-colouring of `S2`.  Hence
`chi(S2)=4`.  No SAT soundness is used for either bound.

## 3. Terminal relation

A colour-partition pattern is encoded canonically by a restricted-growth
string.  Such a string uses at most four blocks and is feasible on the bare
terminal graph precisely when its endpoints differ on all 15 Petersen edges.
The verifier enumerates these patterns and obtains 540.

The certificate has exactly one row for each of those 540 patterns.  For each
row the verifier checks strict syntax, uniqueness, a proper full-support word,
and exact agreement of the ten terminal colours with the pattern.  Thus every
bare pattern is realized on `S2`.  Restriction of any full colouring to the
terminals cannot violate a terminal edge, so the full relation is exactly the
bare relation.  The interface is neutral.

## 4. Trust boundary

The exact claim trusts the written reductions, CPython rational/integer
arithmetic, the verifier implementation, the irreducibility of the standard
cyclotomic polynomial `Phi_20`, and SHA-256 collision resistance for the
stream identifiers.  The producer and checker use different edge predicates:
quotient-field multiplication versus Laurent divisibility.  This is
author-side independent replay, not proof-assistant formalization or an
independent researcher's review.

The producer's CaDiCaL calls are outside the theorem's negative trust
boundary and only generate positive words that are checked definitionally.
The finite support and relation are exhaustive as stated.  The conclusion
does not quantify over other terminal sets, partial third-round supports,
other seed embeddings, or arbitrary plane unit-distance graphs.
