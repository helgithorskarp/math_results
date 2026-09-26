# Complete classification with one six-point plane

Let a subset of `F_5^3` be line-free when it contains none of the 775
five-point affine lines.

**Theorem.** Every line-free 70-set with a six-point plane is affinely
equivalent to exactly one of the three sets in `seeds.json`. Each such set
is inclusion-maximal and has point sum zero. Its number of six-point
planes is respectively 5, 7, or 4. Every six-point section has no three
collinear points.

The proof is an exact exhaustive computation with a complete geometric
reduction. No property of affine automorphism groups is assumed.

## 1. Planar bounds and coordinates

`planar_menus.cpp` builds the 30 planar affine lines directly and visits
every subset of the relevant sizes in increasing bit-mask order. The
Gosper successor enumerates each fixed-weight mask once, ending when its
25th bit is reached. The independently expected binomial counts are:

| Size | All subsets tested | Accepted condition | Accepted subsets |
|---:|---:|---|---:|
| 6 | 177,100 | at most three points on each line | 148,000 |
| 16 | 2,042,975 | no full line | 28,375 |
| 17 | 1,081,575 | no full line | 0 |

There is no larger planar line-free set, because a set of size at least17
would contain a line-free 17-subset. Thus every plane section has size at
most16. Every plane of a 70-set has at least `70-4*16=6` points.

Suppose a six-point section H exists. Choose affine coordinates so H is
`x=0`. Its four parallel sections all have size16. If a line in H contains
k selected points, the six planes through it have total incidence
`70+5k`. Five of them have at most16 points, so
`70+5k <= 6+5*16`, giving `k<=3`.

The 148,000 possible small sections are partitioned into 21 affine plane
orbits. `CAPS.json` lists their minimum masks and sizes. The verifier
applies every one of the 12,000 maps in `AGL(2,5)` to every representative,
checks its orbit size and minimum, and checks disjoint coverage of the
entire generated menu. Every such planar map extends to three-space by
leaving x unchanged. We may therefore fix the small section C to one of
these 21 representatives.

Let A be the section at `x=1`, and let `a=sum(A)` in `F_5^2`. The shear
`(x,y,z) -> (x,(y,z)-x*a)` fixes C and makes the sum of A zero, since
`|A|=16=1` in the field. No other section is constrained by this operation.
Exactly 1,135 of the 28,375 planar 16-sets are centered; this is also
consistent with a unique centered translate in every translation orbit.
The section B at `x=4` is any of the 28,375 planar 16-sets.

It suffices to check every pair `(A,B)` for each C. The total is

```
21 * 1135 * 28375 = 676318125.
```

There is no quotient by a conjectured symmetry, no arbitrary permutation
of parallel sections, and no assumption about the remaining point sum.

## 2. The bipartite completion graph

Put 25 vertices on each side, representing possible selected points at
`x=2` and `x=3`. For each `u in C` and `v in F_5^2`, add the edge

```
(u+2v, u+3v)
```

when `u+v in A` and `u+4v in B`. This is precisely the remaining pair of
points on a transverse line whose other three points are already selected.
Equivalently an edge from p to q is present exactly when

```
3(p+q) in C,   2p-q in A,   2q-p in B.
```

The independent reference checker uses this second formula, reconstructing
edges from endpoint interpolation rather than the production generator's
parameters `(u,v)`.

The holes in each remaining 16-section form a nine-point set. They must
together cover every edge. A matching of size19 therefore excludes the
pair `(A,B)`. Production code starts with a greedy matching, then uses
augmenting paths if necessary. It stops as soon as 19 edges are found.
If fewer are found after all unmatched left vertices are processed, the
matching is maximum. For every reported matching the endpoints are distinct;
the reference checker also compares against a full breadth-first
augmenting-path computation.

## 3. The additional test at matching size18

An 18-edge matching forces a cover of size18 to choose exactly one endpoint
from each matched edge and no unmatched vertex. Write `X_i=1` when the
left endpoint of matched edge i is chosen. For a graph edge from the left
endpoint of pair i to the right endpoint of pair j, the cover condition is
`X_j => X_i`. An edge from an unmatched left vertex forces `X_j=0`;
an edge to an unmatched right vertex forces `X_i=1`.

The desired nine holes on each side exist at this relaxation precisely
when these implications admit an assignment with nine true variables.
The code computes transitive implication closure and reverse closure.
Choosing a variable true forces its forward closure; choosing it false
forces its reverse closure. It recursively branches until all18 variables
are assigned, rejecting a contradiction or more than nine variables of
either value. This is a complete Boolean enumeration. No solver verdict
is used in the proof.

Matching sizes below18 pass to the next step without this test; a failure
to reject is never treated as a completed spatial construction.

## 4. Exact completion

For every surviving triple `(C,A,B)`, enumerate every line-free 16-set D
in the `x=2` plane. Its neighbors N in the bipartite graph must all be holes
of the `x=3` section. If `|N|>9`, discard D. If `|N|=9`, the remaining
section is uniquely the complement of N, which is checked against the
complete planar 16-menu. If `|N|<9`, visit the whole menu and retain every
16-set disjoint from N.

This step is necessary and sufficient. All lines within the five sections
are already forbidden by their planar menus. Every other affine line can
be uniquely written as `(x,u+x*v)`, after scaling its direction to have
first coordinate1. If its three points in C,A,B are selected, its remaining
two are an edge and cannot both be selected. Thus all 775 spatial lines
are accounted for. Conversely every completion appears in this enumeration.

The exhaustive result has 104 distinct normalized solutions, all for
the small-section mask3238. They are stored compactly in `models.json`
as five planar masks. This small section is a six-arc. Since the reduction
may begin with any six-point plane, every such plane has this type.

## 5. Identification and independent point checks

Every one of the 104 models has an explicit affine map from one of the
three seeds. The verifier checks the matrix determinant, applies the map
to all70 seed points, and compares the exact image with the model. The
identified models split into 24 paper-type, 56 order-three-type, and
24 reflected-type solutions. The three seeds have different numbers of
six-point planes, so their affine types are distinct.

Independently of the completion code, the verifier builds all775 spatial
lines from pairs of points and all155 affine planes from linear equations.
It checks every seed and every model for cardinality, line-freeness,
plane-section counts, and coordinate sum zero. It also tests maximality:
every point outside the set completes a line containing four selected
points. Consequently every affine image of every model is maximal.

Point sum zero is preserved by affine maps here: for `p -> M p+b`, the
sum becomes `M sum(p)+70b=M sum(p)` in characteristic5. The identification
therefore establishes every assertion of the theorem.

## 6. Consequence for the 71-point decision

Every plane in a line-free 71-set has at least `71-4*16=7` points. If a
seven-point section existed, deleting one of its points would yield a
70-set having a six-point plane. The theorem says that set is maximal,
contradicting the original 71-point extension. Thus every plane would
contain at least eight points.

This conditional corollary is not an independent proof excluding all
71-point sets. In particular, this classification makes no assumption
that an arbitrary 70-set has a six-point plane.

## Trust boundary

The theorem depends on the written reduction, complete ordinary C++ and
Python enumeration, exact integer/bit arithmetic, and compiler/runtime
correctness. It is not a proof-assistant formalization. Masks use at most25
bits; the Gosper intermediate stays below2^26; spatial Python masks use
arbitrary-precision integers; counters use64-bit unsigned integers. There
is no floating-point decision. Sanitizers and independent comparisons
validate implementations without eliminating this trust boundary. Hashes
identify complete runs; they do not themselves establish the theorem.
