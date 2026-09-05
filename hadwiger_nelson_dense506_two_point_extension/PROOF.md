# A fixed dense506 colouring extends after any two plane points are added

Put alpha=i sqrt(3), beta=i sqrt(11), z=sqrt(33), with positive real square
roots, and let A and V be the pinned Parts v159e646 and v214e977 coordinate
sets. Define

\[
 t=(5+z+5\alpha-\beta)/12,\qquad B=A\cup(\overline A+t),
 \qquad r=\sqrt{-408+72z},
\]
\[
 u_\pm={-18-6z-30\alpha+6\alpha z
       \ \pm r(3+6\alpha+\alpha z)\over72},\qquad
 H_\pm=B\cup u_\pm(V-V[10]).
\]

The source anchor V[10] is alpha/6. These are the two explicit maximum
contact point sets in the [preceding dense-origin construction](../hadwiger_nelson_dense506_origin_attachment/PROOF.md).
Each has 506 distinct vertices and 2,389 strict unit edges.

**Theorem (exact computer-assisted).** The fixed four-colouring in
`host_colors.txt`, with the vertex labels below, extends to a proper
four-colouring of the strict unit-distance graph on H_epsilon union S
for every subset S of the Euclidean plane with at most two elements,
for either sign epsilon. Thus neither fixed embedding can produce a
five-chromatic graph of order at most 508 by adding arbitrary plane points.

The existing colours of all 506 host vertices remain fixed. The extension
colours may depend on S. The theorem does not assert simultaneous extension
to three or more arbitrary points, cover other relative rotations or
translations of the source gadgets, or establish a new record graph.

## 1. The finite obstruction to a fixed colouring

For a point p outside a fixed host H with fixed proper colouring c, let

\[
 L(p)=\{0,1,2,3\}\setminus\{c(v):v\in H,\ |p-v|=1\}.
\]

These are exactly the colours available when p is adjoined. If p has at
most two host neighbours, then |L(p)| is at least two. Define C to be all
points outside H with at least three host neighbours.

Three distinct points on a unit circle cannot be collinear, since a line
meets a circle in at most two points. They determine its centre uniquely.
Consequently C is finite: it is exactly the set of nonhost unit-circle
centres of host triples. No radius, angular grid or coordinate-field
restriction is imposed on the unknown point in this reduction.

To prove that c extends to any set of at most two points, it is sufficient
to check the following finite conditions:

1. L(p) is nonempty for every p in C.
2. No two points p,q in C at unit distance have L(p)=L(q)={a} for the same
   single colour a.

Indeed every outside point has a nonempty list, including those outside
C. Two nonadjacent new points can be coloured independently. For two
adjacent new points, nonempty lists admit distinct colours unless both
are the same singleton. If at least one new point lies outside C, its
list has size at least two and this exception is impossible. If both
lie in C, condition 2 excludes it. Repeated points and points already in
H reduce to a smaller set of new vertices.

This gives the claimed extension while preserving the host colouring.
It is stronger than merely proving four-colourability separately for each
extension. The original search reduction also follows from the minimum
degree-four condition for a minimal non-four-colourable extension, but
that additional criticality argument is not needed for this certificate.

## 2. Exact coordinate field and the second root

Let R=Q(z), E=R(alpha), F=R(r), and K=F(alpha)=E(r). Here alpha squared is
-3, beta=alpha*z/3, and r squared is -408+72z. The latter is positive in
the chosen real embedding because 408 squared is less than 72 squared
times 33, while its other R-conjugate is negative. It is therefore not a
square in R. Since F consists of real numbers in the chosen embedding,
K has degree eight over Q, with basis

```
1, z, alpha, alpha*z, r, z*r, alpha*r, alpha*z*r.
```

Complex conjugation fixes z,r and negates alpha. The automorphism sigma
fixing E and sending r to -r commutes with complex conjugation. It sends
H_plus to H_minus label by label and preserves equality and every unit
relation: N(p-q)=1 if and only if N(sigma(p)-sigma(q))=1.

A point at unit distance from three distinct host vertices belongs to K.
To see this without assuming its coordinates lie there, write a host point
as X+alpha*Y with X,Y in F, and an arbitrary plane point as x+alpha*y with
real x,y. Subtracting two pairs of unit-circle equations gives two linear
equations in x,y with coefficients in F. Noncollinearity makes their
determinant nonzero, so x,y belong to F. Thus every member of C is in K.
Applying sigma in both directions proves C_minus=sigma(C_plus), with
identical labelled host-neighbour lists and unit relations between its
points. It is enough to compute C_plus and use the same host colours for
both signs. Points outside these finite sets are handled directly by the
list argument in section 1.

The source order retains A first in B, then appends new points of
conjugate(A)+t in source order. Labels 0 through 292 are B; append the
rotated V vertices other than V[10] in source order to obtain 506 labels.
The primary and independent programs rebuild these coordinates. Integer
numerators have common denominator D=2592 in the displayed basis.

## 3. Complete unit-circle census

Write each host numerator as X+alpha*Y, with X,Y in the integral span of
1,z,r,z*r. Its squared norm is X squared plus 3Y squared. For a triple of
distinct numerator points, let a,b,c be its three squared side lengths in
F. The ordinary circumradius formula and Heron's identity give the exact
unit-circumradius condition

\[
 abc=D^2\bigl(2ab+2bc+2ca-a^2-b^2-c^2\bigr).
\]

For these distinct real plane points, a collinear triple cannot satisfy
this equality: its right side is zero and its left side is positive.

There are exactly choose(506,3)=21,464,520 unordered host triples.
The primary scan first removes triples with a common host unit neighbour.
Their unique unit-circle centre is that host point, hence is excluded from
C. The exact host graph identifies 93,131 such triples. There is no removal
based on approximate distance or geometric appearance.

For all remaining triples evaluate the displayed necessary identity
modulo 10007, at z=283 and r=6718. These values satisfy z squared =33 and
r squared =-408+72z modulo 10007; D is invertible. This defines a ring map
on the integral coordinate algebra with D inverted. Exact equality must
survive this map; injectivity is neither asserted nor needed. It is not a
homomorphism from the entire number field to a finite field.

The modular test leaves 11,961 triples. Exact arithmetic retains 10,517.
For each retained triple p,p+d,p+e, put d=(dX,dY), e=(eX,eY),
a=N(d), b=N(e), and h=dX*eY-eX*dY. The circumcentre relative to p is

\[
 x={a\,eY-b\,dY\over2h},\qquad
 y={dX\,b-eX\,a\over6h}.
\]

All divisions are exact field operations. Add p and divide by D to recover
the physical point. Canonical rational coordinates deduplicate these
centres to exactly **1,420 points**. Their full host-neighbour histogram is:

| Host neighbours | Completion points |
|---|---:|
| 3 | 670 |
| 4 | 368 |
| 5 | 205 |
| 6 | 93 |
| 7 | 54 |
| 8 | 17 |
| 9 | 2 |
| 10 | 8 |
| 11 | 3 |

Every centre of degree d occurs in precisely choose(d,3) retained triples,
and their union of incident labels is its complete neighbourhood. As an
additional direct check, all 718,520 candidate/host pairs are screened and
then tested exactly when necessary, recovering precisely the same lists
and 5,710 unit incidences.

All 1,007,490 candidate/candidate pairs are also screened and tested exactly,
yielding **3,975 unit edges**. The candidate-coordinate denominators in the
canonical basis are among

```
1,2,3,6,9,12,18,24,36,48,72,108,144,216,432.
```

None is divisible by either verification modulus. The adjacency routines
nonetheless fall back to exact arithmetic if a denominator is not
invertible; such a case is not discarded by a modular division.

## 4. The fixed colouring certificate

`host_colors.txt` contains one row of 506 colour digits and a newline,
**507 bytes** in total. The checker tests it against all 2,389 host edges.
It can also be recovered from B row 4 and V row 1 of the preceding dense
attachment certificate: translate the V colour at anchor 10 to zero using
XOR, then apply the permutation (0,3,1,2). All indices are zero based.
No new SAT computation was used in this result.

The available-list census on the 1,420 completion points is:

| Available colours | Points |
|---|---:|
| 1 | 941 |
| 2 | 461 |
| 3 | 18 |

There are no empty lists. Among the 3,975 candidate unit edges, 1,880 have
singleton lists at both endpoints. **None has the same singleton colour
at both endpoints.** These are exactly the two finite conditions of
section 1, proving the theorem for H_plus and, by section 2, H_minus.

The independent audit also explicitly chooses an allowed pair of colours
for all 1,007,490 candidate pairs, checking inequality on every unit edge.
Its canonical stream uses little-endian unsigned 16-bit candidate labels
and unsigned 8-bit colours. Its SHA-256 is
`fd6e2b6a765b49c09f291f80711ea6534060b83390f49f92ea8e8d0e2585c2f5`.
This stream is regenerated rather than committed.

## 5. Independent verification and exact scope

The primary program uses four-dimensional real-field arithmetic,
Heron's identity, and two real linear circumcentre equations. The audit
uses the original eight-dimensional complex algebra, the determinant
identity

\[
 abc+D^2(\overline d e-\overline e d)^2=0,
\]

and the complex circumcentre formula

\[
 v={N(d)e-N(e)d\over\overline d e-\overline e d}.
\]

Its different modular map is 5281, z=126, r=3928. It scans every triple
without removing known host centres first, retaining 106,336 modular cases.
Exact arithmetic reconstructs 93,131 triples centred at host vertices and
10,517 at new points. Every new centre, every positive triple and every
neighbour list matches the primary computation entry by entry. Independent
adjacency screens followed by generic complex norms reproduce every
candidate/host and candidate/candidate unit relation. Available colour
sets and every pair extension are checked directly, without the primary
bitmask criterion.

Canonical SHA-256 values (compact JSON encodings):

- New-centre triples: `7f03bc7c1c61fc5d3ea5a0c0d8b512dd58c3bcdbd753716068e5bd83ab7ca2a2`.
- Completion points: `3bcfcab7e411f6adff3426ceb1cfff97718d634fe41a0e7a71982a57995c4c45`.
- Host-neighbour lists: `7c71b32a5807e4e9baab0c17953c9e2ba688e7e0d290caa9be6e23b752f564af`.
- Candidate unit edges: `7912eb1140ca9a570128233517073becd52380fe3840f7cc126bc85a7493f27e`.
- Available colour masks: `3521c2b5b0fa8942608728d88416688ca8b5a1d207aad59d2fd79d41be27bdb6`.

Controls check 80 nonzero field inverses, rejection of a zero inverse,
unit and nonunit circles, collinearity, both quadratic rotations of a
translated circle, all 512 two-list/adjacency cases, a direct exact scan
of 4,960 small-instance triples, and rejection of invalid host colourings.

The proof rests on elementary real-plane geometry, unformalized field
algebra, pinned coordinate input, and exact Python integer/Fraction
execution. The alternative arithmetic audit is by the same researcher;
it is not external peer review or proof-assistant formalization. No
floating-point distance, solver UNSAT assertion, or advertised forcing
property of the source gadgets enters the result. It rules out arbitrary
at-most-two-point additions to the two specified 506-point embeddings,
not the team's entire construction direction or all 508-vertex graphs.
