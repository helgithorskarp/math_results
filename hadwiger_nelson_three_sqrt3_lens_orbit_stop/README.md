# Three exceptional lens orbits collapse to a three-colourable patch

This package freezes and exactly decides one bottom-up Hadwiger--Nelson
construction architecture.  Take three pairwise nonadjacent centres forming
an equilateral triangle of side `sqrt(3)`.  For every centre pair, take both
common points of their unit circles and close each intersection under the six
unit-chord rotations about each of its two owners.  Collision-merge all
generated points and reconstruct every unit edge.

The resulting strict physical graph has **16 points and 33 complete unit
edges**.  It is exactly **three-chromatic**.  Moreover, every one of the five
canonical four-colour patterns on the three independent centres extends, so
its unrestricted centre relation is neutral.

This is an exact stopping result, not a five-chromatic graph or progress below
Parts's 509-point record.  The source was selected because `sqrt(3)` is the
unique nonzero separation at which the two common points of two unit circles
have opposite parity in their owner's six-cycle.  Coupling three such
exceptional lenses around an odd centre triangle was the declared forcing
premise.  Exact collision merging destroys that premise: the three lenses
share their circumcentre and collapse into a small triangular-lattice patch.
The checked three-colouring and neutral centre relation retire this frozen
architecture without varying the centre triangle, adding orbit shells, or
testing nearby separations.

## Coordinates and exact graph

An integer row `(s,t)` represents

```text
(s*sqrt(3)/2, t/2).
```

The centres are `(0,0)`, `(2,0)`, `(1,3)`.  The two unit-circle
intersections for their three pairs are respectively

```text
{(1,-1),(1,1)}, {(0,2),(1,1)}, {(1,1),(2,2)}.
```

Thus all three lenses share `(1,1)`.  Rotation through 60 degrees sends a
relative vector `(s,t)` to

```text
((s-t)/2, (3s+t)/2).
```

The twelve frozen intersection/owner routes generate 72 formal orbit
addresses in addition to the three centre declarations, but only 16 distinct
physical points.  The certificate counts the resulting 59 duplicate addresses
as collision merges.
For two rows, four times their squared distance is

```text
3*(delta s)^2 + (delta t)^2.
```

Hence the complete edge test is the integer equation above equal to four.
The colouring `colour(s,t)=t mod 3` is proper on every edge.  The graph
contains the unit triangle `(0,0),(0,2),(1,1)`, proving the matching lower
bound three.

The three centres are mutually at squared distance three and therefore have
no bare edges.  The five stored proper four-colourings realize centre patterns
`000,001,010,011,012`, all set partitions of three labelled terminals up to
global palette permutation.  This proves that the complete unrestricted
centre relation equals the bare relation.

## Reproduce

CPython 3.11 or later and the standard library suffice.  From this directory:

```sh
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
python3 -B controls.py
tmp=$(mktemp -d)
python3 -B build.py --out "$tmp/certificate.json"
cmp certificate.json "$tmp/certificate.json"
sha256sum -c SHA256SUMS
```

The producer constructs the orbit closure and discovers the five positive
relation words by deterministic backtracking.  The checker reconstructs all
120 physical point pairs, verifies every orbit route and collision, checks the
closed-form lattice colouring and all relation witnesses, and rejects eight
semantic mutations.  No solver, floating-point predicate, external input,
omitted trace, or background computation is used.  These are author-side
exact checks, not an independent review or proof-assistant formalization.

## Scope

The theorem concerns this one exact equilateral-`sqrt(3)` centre frame and its
complete first sixfold lens-orbit closure.  It does not classify arbitrary
independent dominating triples, different centre distances, selected exterior
points, later orbit shells, or arbitrary points on the three full circles.
The wider Hadwiger--Nelson record objective remains open.
