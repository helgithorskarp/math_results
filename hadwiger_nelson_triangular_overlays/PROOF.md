# Two intersecting triangular lattices

Write

\[
 \omega=(1+i\sqrt3)/2,\quad R=\mathbb Z[\omega],\quad K=\mathbb Q(\omega),
 \qquad N(a+b\omega)=a^2+ab+b^2.
\]

All embeddings below are the displayed physical embedding in the complex
plane. A unit-distance graph has distinct points as vertices and **all** pairs
at Euclidean distance one as edges. No assertion of graph planarity is made.

**Theorem.** If two unit triangular lattices have a common vertex, the strict
unit-distance graph on their union is four-colourable. The bound is sharp.
Consequently every finite subset of this union is four-colourable, regardless
of its size or the shapes of its two patches.

A common vertex can be translated to the origin and one lattice rotated to
`R`. The other is then `alpha R`, where `|alpha|=1`. Reflections do not enlarge
the family because conjugation preserves `R`. Thus it suffices to colour
`R union alpha R` for every complex unit `alpha`.

## 1. The residue colouring

There is a ring homomorphism

\[
 \rho:R\longrightarrow\mathbb F_3,
 \qquad \rho(a+b\omega)=a-b\pmod3.
\]

Indeed, `omega^2-omega+1` vanishes at `-1` modulo three. Conjugation acts
trivially after reduction, so `N(z) = rho(z)^2 (mod 3)`. In particular, a
unit difference has nonzero residue. This gives a proper three-colouring
of a triangular lattice; its residue-zero class is independent.

The triangular lattice has a unique three-colouring up to permutation of
colour names. Fix one unit triangle: the colour at the third vertex of any
adjacent unit triangle is forced, and the adjacency graph of the triangular
tiling is connected. In particular, every vertex with residue zero has the
same colour as the origin in every proper three-colouring.

## 2. Rotations inside K

Suppose `alpha=(a+b omega)/d`, with integer `a,b,d`, `d>0`, and
`gcd(a,b,d)=1`. Since `N(alpha)=1`,

\[
 a^2+ab+b^2=d^2.
\]

The denominator `d` is not divisible by three. Otherwise reduction modulo
three gives `a=b (mod 3)`. Writing `a=b+3h` gives
`a^2+ab+b^2=3b^2+9bh+9h^2`; reduction modulo nine then implies `3|b`,
hence `3|a`, contradicting primitivity.

The homomorphism `rho` therefore extends to `R[1/d]`, which contains both
lattices. Its values on a unit difference remain nonzero, giving a proper
three-colouring of their union. Coincident labels receive the same colour.

## 3. The one-dimensional contact constraint

Now suppose `alpha` is not in `K`. The two lattices intersect only at zero:
any nonzero equality `z=alpha w` would put `alpha=z/w` in `K`.

For `t` in `K` define the real-linear expression

\[
 \ell(t)=\alpha t+\overline{\alpha t}.
\]

The set `W={t in K: ell(t) in Q}` is a rational vector space of dimension at
most one. If it had dimension two, then `ell(1)` and `ell(omega)` would both
be rational. Writing `alpha=x+i sqrt(3)y`, these values are `2x` and `x-3y`,
forcing rational `x,y` and hence `alpha in K`, a contradiction.

Every cross-layer unit contact with nonzero `z,w` satisfies

\[
 |z-\alpha w|^2=1
 \quad\Longrightarrow\quad
 \ell(w\bar z)=N(z)+N(w)-1\in\mathbb Z.
 \tag{1}
\]

If there are no such contacts, the two three-colourings can plainly be
aligned at the origin. Otherwise `W` has dimension one and contains a
nonzero lattice element. Consequently

\[
 R\cap W=\mathbb Z\gamma
\]

for an element `gamma=A+B omega` with coprime integer coefficients. For each
contact, write `w bar(z)=m gamma`, `m` an integer, and write
`ell(gamma)=p/q` in lowest terms with `q>0`. Equation (1) becomes

\[
 mp=q\bigl(N(z)+N(w)-1\bigr).
 \tag{2}
\]

Consider contacts with **both residues nonzero**. Then `N(z)=N(w)=1 (mod 3)`,
so the parenthesized expression is `1 (mod 3)`. Also
`rho(w)rho(z)=m rho(gamma)` is nonzero, so neither `m` nor `rho(gamma)` is
zero modulo three. Equation (2) and `gcd(p,q)=1` imply that both `p` and `q`
are nonzero modulo three. Hence every such contact has the same product

\[
 \rho(z)\rho(w)=\varepsilon,
 \qquad \varepsilon=qp^{-1}\rho(\gamma)\in\{1,-1\}.
 \tag{3}
\]

If no contact has both residues nonzero, choose either sign for epsilon.
This argument does not assume in advance that the angle is algebraic.

## 4. Four colours, and the exact three-colour obstruction

Use four colour names `A,B,+,-`. On the first lattice give residue zero
colour `A` and nonzero residues their signs. On the second lattice give
nonzero residue `r` the sign `-epsilon*r`; give its nonzero points of
residue zero colour `B`. Give the shared origin colour `A`.

Within either lattice this merely splits an independent residue class and
renames the other colours. On a cross-layer edge:

- two nonzero residues receive opposite signs by (3);
- one zero residue and one nonzero residue receive different colour names;
- two zero residues receive `A` and `B`.

The origin cannot be an endpoint of the last case, because every unit
neighbour of zero has norm one and nonzero residue. Thus this is a proper
four-colouring of the strict graph.

Moreover, if there is **no** cross edge joining two residue-zero vertices,
one can replace every `B` by `A`, obtaining a three-colouring. If such an
edge exists, three colours are impossible: uniqueness of the lattice
three-colouring makes both its endpoints have the origin's colour. Thus,
for `alpha` outside `K`, existence of a zero-to-zero cross edge is precisely
the obstruction to three-colourability.

The four-colour bound is attained. Take
`alpha=(5+i sqrt(11))/6` and `z=w=1+omega`. Both endpoints have residue
zero, and

\[
 |z-\alpha z|^2=3\bigl(2-2\operatorname{Re}\alpha\bigr)=1.
\]

The two four-point diamonds `{0,1,omega,1+omega}` and its alpha image
already contain the seven-vertex Moser spindle. This sharpness example is
classical; no novelty is claimed for it.

## 5. Complete target-sized finite family

For a concrete construction gate define

\[
 P=\{a+b\omega:a,b\in\mathbb Z,\ a^2+ab+b^2\le67\},
 \qquad G_\alpha=\operatorname{UD}(P\cup\alpha P).
\]

The patch has 253 vertices and 702 unit edges. It is centrally based and
invariant under multiplication by `omega`. Every union has at most
`2*253-1=505` vertices, so every member was a physical, target-sized
candidate. The theorem closes all of them without assuming that the
rotation belongs to a predetermined coordinate field.

The verifier also proves uniqueness of the patch's three-colouring: starting
with its central unit triangle, 250 forced third-vertex steps reach every
remaining point. Therefore the zero-to-zero criterion from section 4 gives
the exact chromatic number for this finite patch, too.

Here is a complete finite reduction of its exceptional angles. Write
`alpha=x+i sqrt(3)y`, so `x^2+3y^2=1`. For each ordered pair of nonzero
points `z,w` in `P`, put `w bar(z)=A+B omega` and `k=N(z)+N(w)-1`. The
cross-contact equation is the integer line

\[
 (2A+B)x-3By=k.
 \tag{4}
\]

Divide all three coefficients by their gcd and normalize the sign. A line
`ux+vy=k` meets the rotation ellipse exactly when

\[
 D=3u^2+v^2-3k^2\ge0.
\]

With `S=3u^2+v^2`, its roots are

\[
 x=\frac{3uk\pm v\sqrt D}{S},\qquad
 y=\frac{vk\mp u\sqrt D}{S}.
 \tag{5}
\]

There are exactly 1,542 primitive lines. For 624 of them, `D` is not a
square; each gives two distinct rotations outside `K`. No rotation outside
`K` lies on two different rational lines, by section 3. The remaining 918
lines give 498 distinct rational points of the ellipse, after exact
deduplication. Tangencies and shared rational roots are included.

Nonzero coincidences are separately enumerated as `alpha=z/w` with
`N(z)=N(w)`. All their angles occur among those 498 rational rotations.
Thus no coincidence-only parameter has been omitted. The 12 cross-label
unit contacts involving an origin are present for every rotation; they are
the already counted within-layer edges at the shared origin.

At all other angles there are no additional contacts or coincidences. The
graph is the union of two copies of `P` sharing just the origin, with
505 vertices, 1,404 edges, and chromatic number three.

For the 1,746 exceptional rotations the complete census is:

| Vertices | Unit edges | Chromatic number | Rotations |
|---:|---:|---:|---:|
|253|702|3|6|
|469|1404|3|12|
|487|1404|3|12|
|493|1404|3|12|
|499|1404|3|60|
|499|1434|3|12|
|505|1410|3|252|
|505|1410|4|168|
|505|1416|3|900|
|505|1416|4|228|
|505|1422|3|12|
|505|1428|3|48|
|505|1440|3|24|

These counts refer to distinct complex rotation parameters. They do **not**
count graph isomorphism classes or distinct unlabelled point sets. Many
parameters give congruent or identical point sets. In particular the six
lattice symmetries all give `P` itself.

## 6. Computational trust boundary

The all-lattice theorem in sections 1–4 is an elementary proof and has no
solver or enumeration premise. Sections 5 and the table additionally rely
on exhaustive exact computations with Python arbitrary-precision integers
and rational numbers.

`produce.py` works in the Eisenstein basis, enumerates all ordered contacts,
constructs the line roots by (5), and separately enumerates coincidences.
It emits a reproducible private catalog, not a solver verdict.

`verify.py` imports no producer code. It constructs the patch by Cartesian
rows `(X/2,sqrt(3)Y/2)`, enumerates all contact lines using Cartesian dot
products, and independently enumerates rational roots by
`x=(1-3t^2)/(1+3t^2), y=2t/(1+3t^2)`, including `t=infinity`.
It compares every line, root, edge, and coincidence entry, rather than just
aggregate counts. A separate Cartesian enumeration of all equal-norm
ordered pairs reconstructs every nonzero-coincidence angle and verifies
that each is included among the rational contact angles.

For every irrational line it builds the actual moved coordinates over
`Q(sqrt(D))` in the Cartesian representation. It evaluates all `253^2`
cross-pair squared norms and requires both the rational and radical
coefficients of `norm-1` to vanish. This checks both signs in (5) at once:
the radical coefficient changes sign, and the rational coefficient does
not. For rational rotations it performs integer norm comparisons after
clearing a common denominator. These are 71,818,098 complete cross-pair norm
evaluations, without modular or floating-point filters. Within-layer pairs
are checked once and transferred by the verified isometries. Coinciding
labels are merged before counting rational-case graph edges.

The verifier checks the displayed residue colourings against every edge,
checks the 250-step patch propagation, and checks each zero-to-zero lower
witness. `controls.py` rejects 18 corruptions and independently reconstructs
the seven-point sharpness example, then exhausts all `3^7+4^7=18,571`
colour assignments. No SAT solver, external graph data, or numeric
tolerance is a proof premise. This work is not formally verified or
externally peer reviewed as part of this package.

## 7. Scope and prior work

This construction starts directly from the Euclidean triangular lattice.
It is independent of the Parts mutation hosts, the Haugland heptagon
assembly, finite-field lifts, and Exoo's two-distance source. The residue
colouring and the Moser spindle are standard ingredients. A targeted
literature and Discovery Net search found no matching two-intersecting-
lattice theorem; this is a search observation, not a priority claim.

Related prior work fixes the Moser angle
`beta=(5+i sqrt(11))/6`. Ákos Dúcz,
[A note on geometric colorings of the Moser lattice](https://arxiv.org/html/2606.12325v1),
proves geometric four-colourings of the entire additive lattice
`R+beta R` and its multiplicative closure. This contains `R union beta R`
as one special case here. Our theorem quantifies over every unit alpha;
it makes no geometric-colouring or additive-closure claim at other angles.
Alm and Manske's earlier
[vector-graph theorem](https://ajc.maths.uq.edu.au/pdf/66/ajc_v66_p044.pdf)
colours the graph of a fixed set of spindle directions and their integer
span; its edge relation uses those prescribed directions. Our graph
includes every Euclidean unit contact on the stated union.

The selected record target is described in Jaan Parts,
[Graph minimization, focusing on the example of 5-chromatic unit-distance
graphs in the plane](https://arxiv.org/abs/2010.12665).
These literature sources are context, not imported computational premises
for this proof.

The result does not cover unions of three or more lattice orientations,
two translated full lattices with no common vertex, different lattice
scales, or additions from other coordinate sources. It establishes no
five-chromatic graph with at most 508 vertices and no record improvement.
