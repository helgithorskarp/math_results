# Field gate and exact bridge-orbit certificate

## 1. A local field gate

Write R=Q(sqrt(33)) and E=R(i sqrt(3))=Q(i sqrt(3),i sqrt(11)).
Let d in R be positive in the physical real embedding and nonsquare in R.
If either embedding R -> Q_2 sends d to a square, then **the unit-distance
graph of the whole complex field E(sqrt(d)) is four-colourable**.

Indeed, extend that embedding to F=R(sqrt(d)) -> Q_2. Adjoin
omega=(-1+i sqrt(3))/2, giving an embedding F(omega) -> Q_2(omega).
Complex conjugation fixes F and sends omega to omega^2. An element
A+B omega has norm A^2-AB+B^2. For A,B integral over Z_2 and not both even,
this norm is odd. For arbitrary A,B in Q_2, its valuation is therefore
2 min(v_2(A),v_2(B)), using infinity for a zero coefficient. Norm one
implies both coefficients integral and at least one odd.

Colour each point by the pair of its zeroth binary digits in these two
coefficients. If two coefficients differ by an integral 2-adic number,
their negative binary digits coincide and the difference of their zeroth
digits is that difference modulo 2. Thus unit-distance points cannot
receive the same pair: their difference has integral coefficients with
at least one odd. This includes arbitrary denominators. The argument is
the existing field package's classical residue mechanism, applied to the
extended real field. It is not a new general colouring method.

For x nonzero in Q_2, x is a square iff v_2(x) is even and its odd unit is
1 modulo 8. Let r be the compatible lift of sqrt(33) congruent to 1
modulo 8; the two embeddings send sqrt(33) to r and -r. The exact filter
computes v_2(a +/- br) and the odd unit modulo 8 from a finite lift, and
increases precision until all requisite bits are known. It never decides
an unresolved residue. Denominators are handled by separating their power
of 2 and inverting their odd part modulo 8.

For a cross pair a,b in A and |u|=1, put c=conj(a)b and S=|a|^2+|b|^2-1.
The contact equation is c u^2-Su+conj(c)=0. With
Delta=4|a|^2|b|^2-S^2>0, its root is

    u = S/(2c) +/- i sqrt(3)/(2c) sqrt(Delta/3).

The existing exact census groups all pairs by their irreducible monic
quadratic over E. It supplies 1,490 outside-E classes. Taking d=Delta/3
from any representative pair describes the entire extension field.
The choice of pair only changes d by a square in R. The filter identifies
1,260 classes with a Q_2 embedding and 230 without. Exact square tests
in R partition the latter into the following seven field classes:

| Representative d | Quadratic classes | Maximum cross contacts |
|---|---:|---:|
| 32/27 | 42 | 20 |
| (55-7 sqrt(33))/54 | 50 | 16 |
| (55+7 sqrt(33))/54 | 30 | 14 |
| 13/9 | 36 | 10 |
| (40+8 sqrt(33))/81 | 24 | 9 |
| (101-11 sqrt(33))/162 | 24 | 8 |
| (101+11 sqrt(33))/162 | 24 | 8 |

The list concerns rotation-only, published-origin pencils. It is neither
a census of all geometric placements nor a non-four-colourability claim
for any surviving field. In particular d=32/27 is in the square class of
6, which fails the gate at both embeddings because its valuation is odd.
The earlier exploratory d=13+4 sqrt(33) passes at both embeddings; its
whole coordinate field is therefore unsuitable, independent of its finite
attachment decisions.

## 2. Physical 474-point assemblies

Use the exact 159 points A from the pinned source, with coefficients
(a,b,c,d)/12 representing a+b sqrt(33)+i(c sqrt(3)+d sqrt(11)).
Set u=(sqrt(6)+i sqrt(3))/3. Its norm is one and it lies outside E.
The exact graph B=A union uA has 317 distinct points, 1,312 unit edges,
and exactly 20 cross edges whose endpoints are both nonzero. Its other
unit edges are the two copies of the 646 source edges.

For a cross edge (a,ub), take an oriented unit edge (c,d) of A. The third
copy is

    g(z)=a+(ub-a) conj(d-c)(z-c).

Also allow conjugation of the entire normalized expression
conj(d-c)(z-c), accounting for the other chirality. Each g is an isometry
because both multiplying edges have unit length. Writing the normalized
point as q in E gives g(q)=a(1-q)+ubq. If g(q) lies in E, independence of
1,u over E forces q=0. If g(q) lies in uE, it forces q=1. Here a,b are
nonzero. Thus its only overlaps with B are a and ub. Each third copy
adds exactly 157 distinct points, giving 474 total, with every accidental
unit contact retained. There are 20*646*2*2=51,680 raw placements; no
claim that these placements are pairwise nonisometric is needed.

## 3. A finite orbit contains every such third copy

Let T be the union of all normalized point sets
conj(d-c)(A-c) and their conjugates over oriented source unit edges.
Its exact coordinates are integer E coefficients divided by 144.
Exhaustive generation gives 8,428 distinct points and 75,413 complete
unit edges. In particular 0,1 are in T. For any of the 20 bridges define

    H_ab = B union [a+(ub-a)T].

The same independence argument gives exactly two overlaps, so H_ab has
8,743 distinct points. Every assembly attached along this bridge is an
induced point subset of H_ab. This includes arbitrarily many copies along
this one bridge and arbitrary vertex deletions from their union.

The certificate gives a fixed proper 317-digit word for B. Colour T by
the pinned exact four-colouring of E. For each bridge, certificate.json
gives a permutation of that palette. The verifier checks agreement at
both overlapping points and disagreement on every exact cross-unit edge.
It also checks the full internal graphs of B and T. Therefore the glued
word is a proper four-colouring of the entire H_ab. The 20 hosts have
between 76,737 and 76,750 complete edges. No non-four SAT decision or
assumption about terminal interfaces enters the proof.

The other algebraic root of u^2-(2i sqrt(3)/3)u-1=0 is obtained by
sqrt(6) -> -sqrt(6). This field automorphism commutes with complex
conjugation. It preserves and reflects equalities of points and of
squared distances to one. Hence it gives an isomorphic exact unit graph
for every assembly and orbit above, with the same colour certificate.

## 4. Complete exact pair checks and the coupled pilot

The real field has basis 1,sqrt(33),sqrt(6),sqrt(198). Complex points use
eight rational coefficients (a,b,c,d,e,f,g,h) representing

    a+b sqrt(33)+i(c sqrt(3)+d sqrt(11))
    +sqrt(6)[e+f sqrt(33)+i(g sqrt(3)+h sqrt(11))].

For a difference with common denominator s, unit distance is equivalent
to all four integer equations:

    a^2+33b^2+3c^2+11d^2+6(e^2+33f^2+3g^2+11h^2)=s^2,
    ab+cd+6(ef+gh)=0,
    ae+33bf+3cg+11dh=0,
    af+be+ch+dg=0.

The common denominator for B and each physical orbit image is 5,184;
all individual coefficients have absolute value at most 10,368. Python
checks this bound and regenerates coordinates using unbounded integers.
The C++ interface checker uses 128-bit intermediates, far beyond the
needed range. Native T coordinates are checked to have absolute coefficients at most
432; their pair arithmetic uses bounded 64-bit integers.
There is no numerical distance threshold. All 53,433,520 B/image pairs
are checked, yielding 2,872 unit pairs and 40 coincidences across the
20 images. Duplicated internal/overlap edges are merged explicitly.
Python separately verifies every reported positive interface and native
edge using its own unbounded arithmetic. Completeness still relies on
the documented exhaustive C++ pair loops, not just on positive checks.

The two-bridge pilot uses (70,113) and (111,75), the first and eleventh
bridges in sorted source-label order. Their image/image comparison
exhausts 71,031,184 pairs, giving 88 unit pairs and one coincidence.
The union with B has 17,168 distinct physical points and 152,201 complete
edges. coupled_word.txt supplies a proper four-colouring, checked with
`--coupled`. This is only that one coupled host, not all pairs of bridges.

The initial individual-attachment replay also exhausted 2,572,061,920
old/new pairs for the selected phase; its 51,680 output rows matched the
exploratory stream byte for byte. That large replay remains local. The
public orbit proof is stronger for the stated family and much faster to
reproduce. Both public normal and optimized/sanitized replays passed.
This is ordinary exact computational mathematics with author validation;
no independent-author review or proof-assistant certificate is asserted.
