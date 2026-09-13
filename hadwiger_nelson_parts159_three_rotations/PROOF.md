# Three arbitrary rotations of Parts159 remain four-colourable

**Theorem.** Let A be the archived Parts `v159e646` point set, with its
published vertex 0 at the origin. For every three complex numbers u, v, w
of modulus one, the strict plane unit-distance graph on

\[
uA\ \cup\ vA\ \cup\ wA
\]

is four-colourable. Every subgraph of this graph is therefore
four-colourable. The support has at most 475 distinct points.

All three angles are arbitrary. Coincident points are identified, and every
unit contact between copies is included. The theorem does not cover
independently reflected copies, translations to different anchors, different
gadgets, or four copies. It supplies no global vertex lower bound and no
improvement of the 509-vertex construction.

This is a computer-assisted theorem with an exact algebraic reduction and
positive colour witnesses. It has been checked by its author, including a
second arithmetic representation; independent-author review is outstanding.

## 1. Coordinates and the contact equation

Use the complex field

\[
E=\mathbb Q(\alpha,\beta),\quad
\alpha=i\sqrt3,\quad \beta=i\sqrt{11},\qquad
F=E\cap\mathbb R=\mathbb Q(\sqrt{33}).
\]

An E element is stored as `a+b sqrt(33)+c alpha+d beta`.
The hash-bound coordinate file gives 159 distinct points of E, including
zero, and exactly 646 strict internal unit edges. Its SHA-256 is
`4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02`.

For nonzero p,q in A, a unit rotation z creates a cross edge p--zq precisely
when

\[
c z^2-Sz+p\overline q=0,\qquad
c=\overline p q,\quad S=|p|^2+|q|^2-1.
\]

Put Delta=4|p|²|q|²-S². There are no physical roots if Delta<0. Otherwise
the physical roots are

\[
z=\frac{S\pm\alpha\sqrt{\Delta/3}}{2c}.
\]

They lie in E exactly when Delta/3 is a square in F. The double-root case
is included. This follows because the elements of E negated by complex
conjugation are precisely alpha F. For an outside-E root, its monic
irreducible polynomial is

\[
z^2-Tz+V,\qquad T=S/c,\quad V=p\overline q/c.
\]

Two such events have the same roots exactly when their monic polynomials
agree. Thus grouping all 158² nonzero point pairs by (T,V) gives the complete
cross-edge set for both roots, with no angle approximation. This reuses the
proved reduction and hash-bound arithmetic of the earlier
[origin-pencil package](../hadwiger_nelson_nonmono159_origin_pencil/PROOF.md).

The exact census gives 178 distinct contact rotations in E and 1,490
outside-E quadratic polynomials, hence 2,980 outside-E contact rotations.
Every outside polynomial has **T nonzero**. The code explicitly checks this
condition; the next argument would fail without it.

## 2. Different quadratic extensions cannot close a contact triangle

Every outside contact rotation lies in E(sqrt(d)), for a positive real
d=Delta/3 in F. The census gives 60 distinct d values. Two define the same
extension exactly when their ratio is a square in F: a square root of a
positive real ratio lying in E must lie in F. Exact square-root tests give
52 distinct quadratic extensions.

Suppose u=a+b sqrt(d) and v=c+e sqrt(h) are outside contact rotations in
different extensions. Here b,e are nonzero, and the nonzero-trace check
gives a,c nonzero. Their compositum is biquadratic over E. Since |u|=1,

\[
v/u=\overline u v
\]

has nonzero coefficients on all four basis elements
1, sqrt(d), sqrt(h), sqrt(dh). None of the three nonidentity Galois
automorphisms fixes it. Consequently v/u has degree four over E.
It cannot satisfy a unit-contact polynomial of degree two. Thus uA and vA
have no non-origin cross edge. They also have no nonzero coincidence,
because such a coincidence would give v/u in E.

This removes 4,319,976 pairs of outside contact rotations by geometry, not
by colouring an abstract graph that has not been realized.

## 3. A fixed field colouring extends across every outside contact

The earlier [full-field theorem](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
supplies a four-colouring C of all E, including nonintegral points, with
C(0)=0. Let c be its restriction to A. The verifier checks that c is exactly
the first word in the earlier four-word component library.

**Extension lemma.** For every outside-E rotation z, the colouring c on A
extends to a proper colouring of A union zA.

If there is no non-origin contact, any component colouring on zA with
origin colour zero works. Otherwise z belongs to one of the 1,490 contact
classes. For 1,428 classes, one of the four earlier component words,
permuted by a permutation fixing zero, is compatible with c. For the other
62 classes, `certificate.json` supplies a directly checked word. Both roots
of a class have the same complete cross-edge set. There is no nonzero
coincidence for an outside-E rotation. Every internal edge and every cross
edge is checked; no SAT verdict is used in this argument.

The verifier also checks the field-colouring formula on both copies for
all 178 E contact rotations, including all their point coincidences.

## 4. Complete verification when two outside copies contact the centre

Normalize the central copy to A and let u,v be outside-E contact rotations.
If u=v there are only two copies, covered by the extension lemma.
Different-extension pairs have no outer contact by Section 2 and can be
coloured independently using Section 3 with the same fixed central word.

For rotations in one common extension, represent both exactly in the basis
1,sqrt(d), compute r=conjugate(u)v, and recover every contact between uA
and vA as follows. If r lies in E, use the complete 178-phase E catalogue;
its cross edges and coincidences are reconstructed by integer squared norms
on all 158² nonzero pairs. Otherwise form its monic polynomial from
r+sigma(r) and r sigma(r), where sigma changes the sign of sqrt(d), and
look it up in the complete outside-E catalogue. No match means no contact.

There are 118,734 same-extension pairs:

| Outcome | Rotation pairs |
|---|---:|
| No outer cross edge | 80,858 |
| Three compatible words from the previous library | 37,516 |
| Additional explicit three-copy colour witness | 360 |

For the last two rows, every component edge, every edge at all three
interfaces, and every equality at coincident points is checked. The 360
additional rows all have r in E; they were discovered by SAT and are
verified as positive assignments. The certificate contains 226 distinct
component words in total, shared between the 62 extension rows and 360
cycle rows. Labels that represent one physical point must have equal
colours. The proof therefore applies to the actual point union, not merely
to a graph on 475 labels.

## 5. From the finite cases to all three real angles

Define a contact graph on the three copies: join two copies when there is a
unit edge between two non-origin points belonging to them. Any nonzero
point coincidence also forces such an edge. Indeed, each point of A has
at least two internal neighbours, as checked from the exact graph, so a
coincident nonzero point has an internal neighbour other than the origin.
Use this neighbour in one copy and the coincident point in the other.

If the contact graph is disconnected, each component has at most two
copies. Two copies can be coloured using the field theorem when their
relative phase is in E, the extension lemma when it is outside E, or
independent component words when there is no contact. Match origin colour
zero between components. There are no omitted cross edges or nonzero
coincidences between these components.

Otherwise choose a copy adjacent to the other two and rotate the entire
plane so this copy is A. Write the others as uA and vA. Both phases are
contact rotations. If u,v are in E, the whole union lies in E. If both are
outside E, Section 4 applies.

It remains to treat u in E and v outside E. If uA and vA contact each other,
recenter by multiplying the whole support by 1/v. The two other phases
1/v and u/v are outside E and both contact the new central copy, so
Section 4 applies. If they do not contact, colour A union uA with C and
extend the fixed colouring on A to vA using Section 3. There is no
unhandled nonzero coincidence. This exhausts every contact graph and every
three real rotation angles, proving the theorem.

## 6. Record relevance and limits

Three copies give at most 1+3(159-1)=475 points, so a non-four-colourable
member would have improved Parts509 by at least 34 vertices. The theorem
rules out this construction mechanism. It does not establish a lower bound
for arbitrary plane unit-distance graphs, and makes no claim about whether
these 475 labels are generally distinct or give distinct graph isomorphism
types.

The working published record was checked on 2026-09-13 against
[Parts, Graph minimization](https://arxiv.org/abs/2010.12665) and the
introduction of [Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4),
which still identifies 509. Haugland's Moser-free construction addresses a
different restriction.

Earlier work covered two arbitrary origin-fixed copies and three copies
with a prescribed inner Moser rotation. Here both relative angles are free;
the shared-origin restriction remains essential. No new method or priority
claim is made for the classical field-colouring mechanism.

The graph's [integral-trace theorem](../hadwiger_nelson_integral_trace_gluing/PROOF.md)
and [first-negative-trace theorem](../hadwiger_nelson_first_negative_trace/PROOF.md)
were also checked before publication. They are relevant earlier exclusions,
not premises of the finite colouring checks here. In particular the present
catalogue includes z=(5+i sqrt(39))/8, with minimal polynomial
z²-(5/4)z+1: its relative trace has local valuation -2. Its ten exact cross
contacts are p--zp for A indices 111 through 120. Thus the catalogue is not
confined to the locally integral and first-negative-trace strata.

The field-colouring theorem, exact event reduction, Python integer and
rational arithmetic, and the stated geometric argument are the trust
boundary. The proof is not formalized in a proof assistant. A second
signed-basis implementation checks all physical event roots and every
reported outside contact, but is an author cross-check, not external review.
