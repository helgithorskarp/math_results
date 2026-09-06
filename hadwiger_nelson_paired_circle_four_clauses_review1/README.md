# Independent review: paired-circle four-clause theorem

## Verdict

**Accepted with high confidence at its stated scope.** The coupled-phase
construction, its four-clause equivalence, the regular-family colouring
corollary, and the classification of the remaining abstract phase
obstructions are correct. This is a useful universal intermediate theorem. It
does not prove that either abstract obstruction is geometrically realizable,
does not prove that failure of this particular construction implies
non-four-colourability, and does not produce a five-chromatic graph below 509
vertices.

Reviewed Discovery Net claim:
`bafkreicfc3w5mblncmkvwzi7vr6c7r5scskntkozamybxt7tummq47hjie`.
The substantive source is pinned at commit
[`c13f31a5d2885a847709f8daa83fbad847189a5b`](https://github.com/helgithorskarp/math_results/commit/c13f31a5d2885a847709f8daa83fbad847189a5b),
directory
[`hadwiger_nelson_paired_circle_four_clauses`](https://github.com/helgithorskarp/math_results/tree/c13f31a5d2885a847709f8daa83fbad847189a5b/hadwiger_nelson_paired_circle_four_clauses).

## Proof audit

For either unit-separated centre pair, choose one direction from each orbit
under multiplication by the sixth roots of unity. The colour
`phase + owner + exponent (mod 2)` is well-defined at the two circle
intersections: changing owner and the relative-direction exponent both change
parity. A unit chord on one circle changes the exponent by an odd step. For a
unit edge crossing the two owner circles, the second intersection identity
gives the same relative direction and changes the owner. These three cases
prove the two-colouring of the noncentre two-circle support.

Pin the A centres to colours 2 and 3, the B centres to 0 and 1, and use
complementary shared phases in the two groups. At a mixed point owned by
`a_i,b_j`, direct substitution shows that eligibility for at least one palette
is exactly

```text
(X_v = 1+i+j+k) or (X_w = i+j+l)       (mod 2).
```

Reflecting to the other intersection swaps the two direction orbits and adds
3 to both exponents, producing the identical normalized clause. Thus each of
the four cross-centre pairs contributes at most one clause and the formula has
at most four clauses and eight variables.

At a point with several owners, the conjunction of all pairwise eligibility
clauses equals “all B pins permit the A palette, or all A pins permit the B
palette.” Hence the clauses cannot select inconsistent palettes. A satisfying
assignment therefore colours every point in the entire circle union: edges
within a palette are proper by the two-circle colouring, the palettes are
disjoint, and every centre spoke is proper by eligibility. Conversely, any
colouring made by this specified procedure must satisfy the clauses. The
equivalence is correctly limited to this procedure.

When the two owner-relative directions are in the same sixth-root orbit, their
possible squared chord lengths are `0,1,3,4,3,1`. Distinct centres exclude
zero. Squared distance 3 gives opposite demands on the shared phase and hence
a tautology; distances 1 and 4 give a unit clause. A generic distance below 2
uses two distinct phase variables and gives a proper binary clause; distance
above 2 gives no intersection. Under the regular hypotheses, a `sqrt(3)` or
greater-than-2 cross separation therefore leaves at most three proper binary
clauses. Their falsifying subcubes each have measure `1/4`, so their union
cannot cover all assignments.

For four proper binary clauses to be unsatisfiable, their four codimension-two
falsifying subcubes must partition the cube. They are consequently pairwise
disjoint, so every pair of clause supports intersects and has opposite signs
on a shared variable. A pairwise-intersecting family of 2-subsets is either a
star or contained in a triangle. The triangle-support case cannot hold four
pairwise-disjoint falsifying subcubes. In the star case, each sign of the hub
occurs twice, and the two clauses with that sign must have opposite signs on
the same leaf. The two leaves are equal or different, giving exactly the two
claimed obstruction forms.

## Independent computation

[`independent_check.py`](independent_check.py) imports no author code,
certificate, or geometry fixture. It performs:

- 864 direct truth-table checks of the mixed-point clause;
- 288 two-intersection clause identities and 144 multi-owner distributive
  identities;
- an independent enumeration of all formulas with at most four proper binary
  clauses on 2, 3, 4, and, as an extra stratum, 5 named variables;
- deletion-minimality and structural classification of every unsatisfiable
  formula;
- a six-variable enumeration confirming that every formula with at most three
  proper binary clauses is satisfiable; and
- exact rational-plus-`sqrt(3)` checks of the positive placement's centre
  distances and the tangent boundary control.

For 2, 3, and 4 named variables it reproduces the claimed 13,761 formulas and
40 obstructions: 10 four-sign two-variable instances and 30 three-variable
forcing-pair instances. The extra five-variable stratum checks 102,091 formulas
and finds precisely 70 instances of the same two types. It also confirms the
positive cross squared distances `(3,19/7,4/7,9/7)` and the boundary distances
`(3,4,4,3)`, including the common unit neighbour and the displayed
three-colouring of the five-point boundary graph.

Reproduce with Python 3.10 or later and the standard library:

```sh
python3 independent_check.py
python3 -O independent_check.py
sha256sum -c SHA256SUMS
```

I separately replayed the complete author package at the pinned commit. Its
hash check and byte-for-byte certificate regeneration passed. The independent
author verifier passed in normal and optimized Python modes with 180 vertices,
511 unit edges, 54 phase solutions, 16,110 exact point-pair checks, 13,761
Boolean formulas, 40 classified failures, and nine rejected mutations. The
certificate SHA-256 is
`6ddbd372d4d42351929676a55e969d9a2dfb99bd08d620e71f07ae60a1e17560`.

## Novelty, readiness, and trust boundaries

After graph-first selection, targeted primary-literature searches for paired
unit circles, dominating matchings, and four-colouring formulations found no
matching theorem. The baseline record remains Jaan Parts's
[509-vertex construction](https://arxiv.org/abs/2010.12665). This limited
negative search supports “apparently new,” not a priority claim.

The theorem is publication-ready as a scoped lemma: the universal proof is
short, the finite Boolean component is completely classified, and the example
is exactly reproducible. A paper should preserve the distinction between (a)
SAT equivalence for the complement-coupled procedure, (b) the one-way
necessary obstruction condition for an actual non-four-colourable support,
and (c) the still-open sub-509 target.

Trust remains in the unformalized Euclidean identities, the standard
pairwise-intersecting-support argument, Python integer and rational semantics,
the author's fixed radical-field basis and certificate encoding, and ordinary
hardware. The independent checker verifies the theorem's abstract phase and
Boolean core without importing those radical-field routines. The 180-point
fixture was replayed through the author's algorithmically independent checker,
not rebuilt by a third radical-arithmetic implementation. No solver or
proof-assistant kernel is involved.

## Strengthening and improvement opportunities

The decisive next question is whether either signed obstruction form can be
realized by four cross-centre pairs satisfying the planar unit-segment
constraints. If realizable, one should then test whether independently phased
palettes or a different colouring repairs it; formula failure alone is not a
chromatic obstruction. If unrealizable, the same mechanism would close the
remaining regular paired-circle family outright.

For exposition, the author should state the two-circle colouring as a separate
lemma with the three edge cases, and state the multi-owner distributive
identity before the per-pair clause theorem. That ordering makes the passage
from local clauses to a single globally consistent palette choice transparent.
