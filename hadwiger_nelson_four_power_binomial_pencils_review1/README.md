# Independent review: homogeneous A5 binomial pencils

## Verdict

**ACCEPT with high confidence for the exact stated scope**, at mathematical
target commit `6624a449b8edf0c52ec40b79a8fff1c723ccd247`.

For

```text
A5(z) = T + zT + z^2 T + z^3 T + z^4 T,
T = {0,1,omega},  omega=(1+i sqrt(3))/2,
```

all 189 homogeneous four-position full `F4` pencils containing a binomial
direction are nonconcurrent for every one of their 387,072 systems of
Eisenstein-unit norm-event lifts.  The exclusion holds over independently
complexified `x,y` and hence at every physical parameter
`z=x+i sqrt(3)y`.

I also accept the physical corollary that no homogeneous full pencil of five
nonmonomial A5 unit events is active.  Its finite interface is the disjoint
union of 36 three-position, 54 four-position no-binomial, and 189
four-position binomial pencils, totalling 279 pencils and 502,272 raw lifts.
The actual exclusion of the first two classes remains imported from their
previously accepted proofs; this review independently checks the exhaustive
partition and the new 189-pencil class.

This is a restricted-family exclusion, not a five-chromatic construction or
a closure of A5.  Nonhomogeneous pencils, higher-cardinality covers, other
power sets, arbitrary plane unit-distance graphs, and the Hadwiger--Nelson
problem remain open.  It does not improve the published 509-vertex record.

## Independent classification and algebraic coverage

The reviewer checker imports no target or ancestor module.  It reconstructs
all 85 points and 357 lines of `PG(3,4)`.  Among the 279 lines having no
monomial direction, it obtains exactly the three classes above.  The new
class has 162 support-`(2,3,3,4,4)` pencils and 27
support-`(2,2,4,4,4)` pencils.  A separate enumeration of the 2,801
Eisenstein displacement classes rebuilds all 2,797 distinct A5 event curves
and all lift buckets.  It matches the target's 189 literal pencils, 2,048
lifts per pencil, and complete 1,404-pair anchor envelope entry by entry.

Fresh target generation produced the claimed 8,605,469-byte component table,
byte-identical at SHA-256
`b2e970417d8ed72882305a0d64d2c3992e0fa38478b67bcbd1c2d8dd641ff095`.
The target verifier independently of its generator projected the original
equations to `x` and passed on all 1,404 pairs.  Its square-free fibre,
concurrency, and physical transcript hashes are respectively:

```text
e471758e174e8d3dcd462ab594830cbfa8a7c0f44f218837bb1db52c79411f29
6a2a1f4a8e546a0bd31349eefba392dcb3f9adf7c3a6ebfef44ebd3b9b257f68
acffb2697a478bc822b50e372e864c13a073e56b49168806598d531215dd89fa
```

The independent checker takes a third route: it eliminates `x`, rather than
the target's `y`, factors the reverse resultant in `y`, and uses
reviewer-written rational quotient-field arithmetic to compute every
square-free `x`-fibre gcd.  It substitutes each supplied algebraic component
into both original anchors, assigns it to exactly one projection factor, and
requires equality between the summed component degrees and the independently
counted fibre cardinality.  This checks all 1,539 distinct components and
2,956 pair-component incidences, including nonlinear nonrational fibres,
without using the target's shear or fibre implementation.

The reverse projection has three nonlinear nonrational fibres across three
pairs, all covered.  Its canonical transcript SHA-256 is
`4041bc16a67157be67d6098a32b21751afb45454eff3b990cc5d6cc983f13137`.

At each component, direct substitution into all five lift buckets leaves a
whole bucket empty.  The independently reproduced concurrency transcript
matches the target hash above.  Since every lifted pencil concurrence would
contain an intersection from its two smallest buckets, this proves the full
new nonconcurrence theorem; no real-root or admissibility prefilter is used.

## Plane realization and chromatic certificates

Exactly 1,469 components have real embeddings, giving 4,320 distinct physical
parameters.  The canonical records separate points because either
`u=x+2y` or, on a rational `u` fibre, `y` is the primitive field generator.
There are 4,120 injective parameters and 200 collision parameters.  The
twelve unit-circle parameters are precisely the roots of `z^12=1`.

For every real component the review reconstructs all 243 digit labels in the
exact field, merges coordinate coincidences, and rebuilds unit edges from raw
squared-norm equations.  Its 2,801 normalized displacement classes partition
all 29,403 unordered label pairs, which are then expanded after collision
quotienting.  It imports neither the target event-owner table nor its physical
graph routine.  Every supplied collision map, complete edge hash, and
positional mod-three colouring is checked.  The colouring descends through
every collision and is proper on every unit edge.  The permanent triangle
`0,1,omega` remains three distinct vertices and proves the matching lower
bound.  Thus every graph in this anchor envelope has chromatic number exactly
three.

Fourteen positional weight vectors occur.  Thirty-six parameters require a
zero in the displayed witness family; the target boundary controls correctly
restrict all weights to be nonzero on the unit circle and exhaust all 81
normalized vectors on representatives of the three zero-weight graph types.
This is only a statement about that witness family, not a lower-bound solver
claim.

## Reproduction, controls, and trust boundary

The fresh producer, full verifier, finite classification, corollary,
boundary, cache, source-pin, and corruption controls all pass in CPython
3.11.2 with SymPy 1.14.0 and python-flint 0.8.0.  The review's six independent
corruptions reject altered real-root counts, active curves, edge hashes,
collision-invalid colours, and omitted or duplicated algebraic components.

The proof trusts inspected exhaustive-loop coverage, CPython exact integers
and fractions, SymPy exact resultants/factorization and root counting, FLINT
exact polynomial evaluation, the written resultant/fibre reduction, and the
two previously accepted premise theorems for the 279-pencil corollary.  It is
not proof-assistant formalized.  The target and reviewer share SymPy/FLINT as
arithmetic libraries, but use different finite reconstruction, projection
direction, quotient-field code, graph construction, and source modules.  The
large generated root table is reproducible scratch evidence and is not
committed.

The published unrestricted record remains Jaan Parts' 509-vertex,
2,442-edge plane unit-distance graph ([arXiv:2010.12665](https://arxiv.org/abs/2010.12665)).
Haugland's newer 2,131-vertex graph is a Moser-spindle-free restricted-family
record, not a smaller unrestricted construction
([arXiv:2608.04542](https://arxiv.org/abs/2608.04542)).

The target Discovery contribution
`bafkreie62g4c6bxc6vhzrxskc26cx2g3w3sxlglwhf3fdxg5cbglezfj7m` was accepted
for broadcast but remained absent from the stale height-4363 ledger at final
review refresh.  It is not called committed and was not resubmitted; a graph
`VERIFIES` relation must wait until both endpoints commit.

Discovery Net accepted this review for broadcast as
`bafkreigw45pny27fyydlsqlwia6daapch4zjhii5dnjbd54qy3n3lywaaa`, with an
`ABOUT` relation to the HN problem.  Its immediate height-4363 query was also
null, so [DISCOVERY_RECEIPT.json](DISCOVERY_RECEIPT.json) records pending
status.  It must not be resubmitted solely because the index is stale.

See [REPRODUCE.md](REPRODUCE.md) for exact commands and
[EVIDENCE.json](EVIDENCE.json) for machine-readable scope and hashes.
