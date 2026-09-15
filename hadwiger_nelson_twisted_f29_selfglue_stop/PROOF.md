# Exact construction and finite proof

## 1. Source and selected roles

The source coordinate row `(a,b,c,d)` denotes

```text
(a+b*sqrt(33) + i*(c*sqrt(3)+d*sqrt(11)))/12.
```

Complete reconstruction gives 29 distinct points and 75 unit edges.  Its
centre is row 0.  The 14 marked centre-neighbours are

```text
4 5 6 7 9 10 12 14 15 17 18 22 25 28.
```

The verifier directly proves two source facts.  First, F29 has no proper
three-colouring.  Second, after deleting the centre, no proper four-colouring
uses only colours 0 and 1 on the displayed neighbours (colour symmetry makes
this the complete at-most-two-colour test).  The full union word restricts to
a proper four-colouring of the source, proving the matching upper bound.

Role 4 was selected because it is a marked neighbour.  Role 1 was selected
because it occurs in the odd cycles `(1,11,23)` and `(1,3,2,8,11)` in the
source's finite palette proof.  This identifies the forcing premise before
constructing or colouring the union.

## 2. Frozen half-turn

Set `s=p_4+p_1`.  Exact expansion in the source field gives

```text
|s|^2 = 5/3.
```

Set `q=sqrt(35)/5`, so `q^2=7/5`, and choose the displayed oriented unit-circle
intersection

```text
w = (s+i*q*s)/2.
```

Because multiplication by `i` rotates through 90 degrees,

```text
|w|^2 = |s|^2(1+q^2)/4 = (5/3)(12/5)/4 = 1,
|s-w|^2 = 1.
```

The isometry `g(z)=w-z` is an involutory half-turn and swaps the two source
centres.  The two role contacts follow without approximation:

```text
|p_4-g(p_1)| = |p_4-(w-p_1)| = |s-w| = 1,
|p_1-g(p_4)| = 1.
```

Together with `|0-w|=1`, these are the three prescribed inter-copy edges.
The square classes of 3, 11 and 35 are independent in
`Q*/(Q*)^2`, so the monomials in `sqrt(3),sqrt(11),sqrt(35)` form the standard
eight-element basis.  The reconstructed `w` has nonzero coefficients in the
last four basis positions, which contain `sqrt(35)`.  Hence the frame lies
outside the original F29 coordinate field.

## 3. Complete physical graph

The checker represents each real coordinate by its eight rational basis
coefficients.  It inserts both 29-point copies, merges equal tuples, and then
tests squared distance one for all unordered pairs.  The results are:

```text
formal addresses       58
physical points        58
collisions              0
source edges per copy  75
internal edge union   150
cross-copy edges       21
complete edges        171
```

The point and edge streams have SHA-256 digests

```text
points 13452bc53b33d560132c3562fc77bc2c2d6141678eed6b2d3c163713279e581b
edges  efcb7bd37abef4bfc220bcd447f548e724f3c1fc0b7339b447d98a62219bb995
```

The extra-edge list in [certificate.json](certificate.json) is compared with
the reconstructed stream exactly.  Thus the colour claims concern the strict
physical unit graph, not an imposed subgraph.

## 4. Chromatic and relation decisions

The 58-digit word in the certificate is checked on all 171 edges.  Since one
copy of F29 is an induced physical subgraph and its exhaustive three-colour
search fails, the union has chromatic number exactly four.

Use the ordered active interface

```text
(0, w, p_4, p_1, g(p_4), g(p_1)).
```

In physical labels this is `(0,29,4,1,33,30)`.  Its induced graph has seven
edges and exactly 23 canonical proper four-colour patterns.  A canonical word
starts with 0 and introduces colour names in first-occurrence order.  The
certificate supplies a full proper colouring for every one of those 23 words,
with the six interface colours pinned literally.  Any restriction of a full
colouring is proper on the induced interface, giving one containment; the 23
checked witnesses give the reverse containment.  Therefore the complete
unrestricted interface relation equals the bare one.

This establishes a neutral interaction despite all 21 actual cross edges.  It
is the required exact stopping condition for this one frozen construction,
not a theorem about arbitrary F29 placements.

