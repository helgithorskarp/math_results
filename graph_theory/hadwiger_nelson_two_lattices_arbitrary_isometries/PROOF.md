# Any two unit triangular lattices are four-colourable

Put `omega=(1+i sqrt(3))/2` and `R=Z[omega]`. A **unit triangular lattice**
is a set `t+uR`, where `t` is any complex number and `|u|=1`. Reflections
are included because conjugation preserves R. For a point set X, `UD(X)`
has all pairs of distinct points at Euclidean distance exactly one as edges.
The graph may have crossing edges in its drawing.

**Theorem 1.** For any two unit triangular lattices L and M, with arbitrary
translations and orientations, `chi(UD(L union M)) <= 4`. The bound is sharp
even when the two entire lattices are disjoint. Every finite point set
contained in their union, and every unit-edge subgraph on those points,
is consequently four-colourable.

The new part relative to the previously published intersecting-lattice
theorem is the case `L intersect M = empty`. Sections 1–3 prove it without
an algebraic-angle assumption. Section 4 gives an exact three-colourability
criterion for disjoint full lattices, and Section 5 gives a 16-point
sharpness witness. For completeness Section 6 restates the earlier proof
of the intersecting case, with its provenance explicitly retained.

## 1. Two unit neighbours force membership in a lattice

**Lemma 2 (unit-circle closure).** If a plane point x has two distinct
unit-distance neighbours in a unit triangular lattice L, then x belongs
to L. Thus a point outside L has at most one unit neighbour in L.

Normalize L to R and translate one neighbour to zero. The other is
`d=a+b omega != 0`. Since both distances to x equal one, `|d|<=2`.
The norm `N(d)=a^2+ab+b^2` is an integer in `{1,2,3,4}`. Modulo three it
equals `(a-b)^2`, excluding 2. The possibilities, up to multiplication
by the six units `omega^j`, are respectively

```
d=1,       d=1+omega,       d=2.
```

One can check this short classification directly: the identity
`4N(d)=(2a+b)^2+3b^2` bounds `|b|<=2`, and substitution gives six
solutions at each of norms 1, 3 and 4. The intersections of the two unit
circles for these three representatives are, respectively,

```
{omega, 1-omega},       {1, omega},       {1}.
```

These all belong to R, as do their rotations and translations. The two
circle intersections are exhaustive, including the tangency for d=2.
This proves the lemma. The calculation is a proof about all plane points;
it does not discretize x or assume an arithmetic field for x.

## 2. A palette lemma for a matching between two graphs

**Lemma 3.** Let a graph have disjoint vertex parts A and B. Suppose each
induced part is three-colourable and the edges between the parts form a
matching, possibly empty or infinite. Then the graph is four-colourable.

Write the independent classes of A as `A0,A1,A2` and those of B as
`B0,B1,B2`. First give `A1,A2` colours 1,2, and `B1,B2` colours 3,4.
For each vertex of A0 choose a colour from `{3,4}` different from the
colour of its cross neighbour if that neighbour is in `B1 union B2`.
There is at most one forbidden colour. For each vertex of B0 similarly
choose from `{1,2}`, avoiding its cross neighbour in `A1 union A2`.
Choosing the smaller available colour makes the rule explicit.

Within A and within B, distinct independent classes use disjoint palettes.
A cross edge between two fixed classes has endpoints in `{1,2}` and
`{3,4}`. A cross edge between A0 and B0 also has disjoint palettes. A
cross edge with exactly one flexible endpoint is proper by that endpoint's
choice. These are all edge types. No simultaneous recolouring, iteration,
finiteness, or compactness assumption is required.

The matching hypothesis is essential for this particular general lemma:
two triangles joined by every cross edge form K6, although each part is
three-colourable. This example is abstract and is not asserted to have a
plane unit-distance realization.

## 3. The disjoint-lattice case and the HN consequence

Suppose L and M are disjoint. By Lemma 2 every vertex of either has at most
one neighbour in the other. Their cross edges therefore form a matching.
Each lattice has the proper three-colouring

```
rho(a+b omega)=a-b mod 3,
```

transported by its isometry. Lemma 3 proves the new case of Theorem 1.
If the lattices intersect, Section 6 supplies the existing theorem, so
the two cases exhaust all translations and orientations.

Consequently a point set supporting a graph of chromatic number at least
five cannot be covered by two unit triangular lattices. Any construction
assembled solely from patches of such lattices needs at least three
distinct full lattice supports. Distinct patches in the same full lattice
count only once. This condition is independent of the number of vertices;
it is **not** a lower bound for all plane unit-distance graphs, a
five-chromatic construction, or an improvement of the 509-vertex record.
Different lattice spacings and arbitrary additive sums are outside the
statement. A common similarity of the whole drawing is harmless if its
edge length and lattice spacing are normalized together.

## 4. Exact three-versus-four criterion for disjoint full lattices

Choose lattice coordinates for L and M and their residue maps rho. Let C
be the bipartite graph with left and right vertex sets `{0,1,2}` and put
`ij in E(C)` exactly when some unit cross edge has residue i on L and
residue j on M. This is an existence condition on the entire lattices,
not an assertion that a finite scan computes C in every placement.

**Theorem 4.** For disjoint full unit triangular lattices, the following
are equivalent:

1. Their strict union is three-colourable.
2. Some permutation pi of `{0,1,2}` satisfies `i != pi(j)` for every
   edge ij of C.
3. The bipartite complement of C has a perfect matching.
4. C has no vertex of degree three and contains no K2,2.

When these conditions fail the chromatic number is exactly four.

The triangular lattice has a unique proper three-colouring up to palette
permutation: a unit triangle fixes the next triangle sharing an edge,
and the triangle adjacency graph of the tiling is connected. Thus the
restriction of any three-colouring to a lattice is a renaming of rho.
Rename the first lattice to rho; the second is then pi composed with rho.
This proves the equivalence of 1 and 2. Permitted equal-colour class pairs
are precisely edges of the bipartite complement, proving 2 iff 3.

For 3 iff 4 apply Hall's condition to the complement. A violating left
set of size one means a degree-three left vertex in C. A violating set
of size two means its two vertices both contact some two right classes,
giving a K2,2 in C. A violating left set of size three means a right
vertex of degree three in C. Conversely each of these patterns violates
Hall's condition. Each lattice contains a triangle, so the lower bound
is at least three; Theorem 1 provides the upper bound four.

The criterion is unchanged by different lattice origins or by permuting
the residue names. For finite patches, the same equivalence holds if
their three-colourings are uniquely forced up to palette permutation.
It need not hold for arbitrary finite subsets, whose residue classes
need not be monochromatic in every three-colouring.

The contact graph C is a quotient recording residue pairs. Its edges
need not form a matching even though the physical cross edges do. The
four-colouring in Lemma 3 deliberately permits splitting a residue class.

## 5. Sharpness for disjoint lattices: a 16-point example

Let

```
alpha=(5+i sqrt(11))/6,     d=(1+omega)/3,
L=R,                       M=alpha*(d+R).
```

Here `|alpha|=1`, and alpha is not in `K=Q(omega)`: membership would
require `sqrt(11/3)` to be rational. If `z=alpha*(d+w)` with z,w in R,
then `d+w != 0` because d is not in R, and alpha would equal a quotient
of two elements of K. Thus **the entire lattices are disjoint**.

Take the two filled triangular patches

```
A={a+b omega : a,b >= -1, a+b <= 1},
B={alpha*(d+a+b omega) : a,b >= -1, a+b <= 0},
```

with a,b integers. Their orders are 10 and 6. They have respectively
18 and 9 internal unit edges. The three cross edges, listing lattice
coordinate pairs `(a,b)` on each side, are exactly

| A coordinate | B coordinate before shift and rotation |
|---|---|
| (-1,-1) | (-1,-1) |
| (-1,2) | (-1,1) |
| (2,-1) | (1,-1) |

For example, after expressing the first endpoint as z and the unrotated
second endpoint as `w+d`, the three cases have

```
w+d = (2/3)z,       N(z)=3.
```

Therefore all three squared cross distances equal

```
3 * (1 + 4/9 - (4/3)*(5/6)) = 1.
```

Each filled patch has a unique three-colouring up to permutation, by
successively adjoining unit triangles along shared edges. The three
marked A corners have residue 0, while the marked B corners have the
three different residues 0,1,2. In three colours all A corners would
have one colour, and one of the B corners must have that colour; its
cross edge is impossible. Lemma 3 gives four colours. Thus this strict
16-point, 30-edge graph has chromatic number exactly four.

The graph is Moser-spindle-free. More generally, a triangle in the union
of two disjoint lattices lies wholly in one lattice: two of its vertices
are in one lattice and Lemma 2 forces the third into it. The four
triangles of a Moser spindle form a connected family under sharing a
vertex and cover all seven vertices. An embedded spindle would therefore
lie wholly in one lattice, contrary to that lattice's three-colourability.
This observation concerns the two-lattice family only.

No minimality, new four-chromatic size record, or priority is claimed
for this illustrative graph. Its role is to show that the newly covered
disjoint case requires four colours in general, with the same proof
mechanism as the full-lattice criterion.

## 6. Existing intersecting case, restated with attribution

This section restates the elementary argument in the earlier
[two-intersecting-lattice proof](../../hadwiger_nelson_triangular_overlays/PROOF.md),
independently accepted in its
[review](../../hadwiger_nelson_triangular_overlays_review1/README.md).
The preceding new lemmas neither replace that proof nor claim a new review
of its finite rotation census. After translating a common vertex to zero
and rotating, the sets are `R` and `alpha R`, with `|alpha|=1`.

If alpha belongs to K, write `alpha=(a+b omega)/e` primitively with e>0.
Its norm equation is `a^2+ab+b^2=e^2`. If 3 divides e, reduction modulo
three gives `a=b mod 3`; substitution and reduction modulo nine then
force 3 to divide b and a, contradicting primitivity. Hence `3` does
not divide e. The map rho extends to `R[1/e]`; conjugation fixes its
residue and a unit difference has square residue one. This colours
the whole union with three colours and is consistent at all coincidences.

Suppose alpha is outside K. The two lattices meet only at zero. Define
`ell(t)=alpha*t+conjugate(alpha*t)` for t in K. The rational subspace
`W={t in K : ell(t) in Q}` has dimension at most one. Indeed, if it
had dimension two, `ell(1)` and `ell(omega)` would be rational. Writing
`alpha=x+i sqrt(3)y`, these are `2x` and `x-3y`, forcing x,y rational.

For a cross edge z,alpha*w with z,w nonzero, the element
`t=w*conjugate(z)` is nonzero and satisfies

```
ell(t)=N(z)+N(w)-1.
```

If there are any such contacts, `R intersect W=Z gamma` for a primitive
lattice element gamma, and `ell(gamma)=p/q` with coprime integers p,q,
q>0. For a contact write `t=m gamma`; then

```
mp=q*(N(z)+N(w)-1).
```

For contacts with both rho(z) and rho(w) nonzero, reduction modulo three
makes `N(z)+N(w)-1=1`. Also `rho(t)=m*rho(gamma)` is nonzero, so m and
rho(gamma) are nonzero. Coprimality then forces p and q nonzero modulo
three. Every such contact therefore has

```
rho(z)*rho(w)=epsilon,   epsilon=q*p^(-1)*rho(gamma) in {1,-1}.
```

If no such contact exists, choose either epsilon. Give the first zero
residue class colour A and the nonzero points of the second zero class
colour B. Give the shared origin colour A. The nonzero residues on the
first lattice get their signs `+,-`; on the second they get
`-epsilon*rho(w)`. Contacts with both residues nonzero get opposite
signs, contacts with one zero residue have disjoint palette types, and
contacts with two zero residues receive A and B. The origin has no
unit neighbour of zero residue. All within-layer edges are proper too.
This proves the intersecting case for every complex rotation.

## 7. Evidence and limits

The general theorems rest on the proofs above. `verify.py` provides
executable checks of the small norm classification, all nine-cell
contact relations, the palette construction, and the 16-point example.
It reconstructs all 120 pairs of that example by exact radical
coordinates and checks strict edges, colour words, triangle propagation,
and spindle absence. It does not use approximate coordinates, a SAT
verdict, a downloaded graph, or a finite search as a substitute for the
unbounded proof.

The old intersecting theorem is a mathematical dependency whose source
identity is pinned in `CONTEXT.json`. Its large finite rotation census
is unnecessary and was not rerun. The new result is author-checked,
not externally reviewed or formally verified. Targeted literature and
committed-graph searches found the intersecting result but no statement
covering arbitrary translations; that is a search observation, not a
priority claim.
