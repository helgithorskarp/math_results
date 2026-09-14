# Equilateral affine frames of the Parts point set

Let P be the 509 labelled Parts points, with label 0 at the origin, as encoded
by the hash-pinned sibling coordinate certificate. Choose distinct labels
a,b other than 0 whose position vectors are linearly independent over R.
There is a unique real linear map T taking P[a] to (1,0) and P[b] to
(1/2,sqrt(3)/2). Reflection of the target gives the same distances. Let G[a,b]
be the **complete strict unit-distance graph** on T(P).

**Theorem.** If T is not a Euclidean isometry, G[a,b] is four-colourable.
The isometric frames recover the original Parts metric. Every induced
subgraph of G[a,b] on at most 508 vertices is four-colourable, for every
admitted frame, including the isometric frames.

The choice a<b loses nothing: swapping a and b composes with an isometry of
the equilateral triangle. All 128,778 unordered choices are examined; 1,192
are collinear and 127,586 are valid. Exactly 30 frames recover the original
metric. This is a finite affine-deformation gate anchored at label 0. It
does not classify arbitrary affine maps, frames based at other source points,
or modifications by additional vertices. No global vertex bound follows.

## 1. Geometry and exact coordinates

The coordinate field used for computation is the real biquadratic field
F=Q(sqrt(5),sqrt(33)). Replace each physical source coordinate (x,y) by

    (X,Y) = (288*x, 288*y/sqrt(3)).

The pinned coordinates give integer coefficients in the basis
1,sqrt(5),sqrt(33),sqrt(165). The code checks the required zero coefficients,
the denominator, the 509 distinct points and the anchored origin. This is
one fixed invertible change of coordinates, so it does not alter the
family of affine images. Write a,b,d in these coefficient coordinates.

Set D=det(a,b), A=det(d,b), B=det(a,d). Since D is nonzero,
d=(A/D)a+(B/D)b. Its actual transformed point is

    ((A+B/2)/D, sqrt(3)*B/(2*D)).

In particular this is an explicit exact plane realization, and invertibility
proves injectivity without 90,000 separate collision scans. Its squared
Euclidean length is (A^2+A*B+B^2)/D^2. Thus its unit edges satisfy precisely

    A^2 + A*B + B^2 = D^2.                 (1)

Equivalently let a=(ax,ay), b=(bx,by). The numerator is
qx*dx^2+qxy*dx*dy+qy*dy^2, where

    qx  = by^2 - by*ay + ay^2,
    qxy = by*ax + ay*bx - 2*(by*bx + ax*ay),
    qy  = bx^2 - bx*ax + ax^2.

The physical original metric in these coefficient coordinates is
(dx^2+3*dy^2)/288^2. Hence a frame is isometric exactly when
qxy=0, 288^2*qx=D^2 and 288^2*qy=3*D^2. The checker verifies these identities
over F for **every** frame in the exceptional residue bucket, rather than
inferring real equality from a modular equality.

## 2. A sound supergraph, not approximate geometry

Use the ring homomorphism from Z[sqrt(5),sqrt(33)] to F_p defined by

    p=1000000271,
    sqrt(5)  -> 838613109,
    sqrt(33) -> 767568613.

Trial division checks primality, and modular squaring checks both roots.
There is no assertion of a homomorphism from the characteristic-zero field
F into F_p. Only integer polynomial identities are reduced modulo p.

If the determinant has nonzero image, divide (1) by that image squared and
test each pair in F_p. Every actual edge passes this necessary test. Extra
modular edges may occur: we deliberately retain them. Consequently a proper
four-colouring of the modular **supergraph** is also a proper colouring of
the exact physical graph. A modular non-four result alone would have no
physical chromatic implication and would require exact reconstruction.

All 1,192 zero-determinant residues are checked in F and are genuinely
collinear. No valid frame is silently omitted. The 127,586 remaining frames
fall into 90,104 residue-metric buckets. These are not asserted to be 90,104
distinct real metrics or nonisomorphic graphs. Even if different real
metrics collide in a bucket, its supergraph contains every genuine edge of
every corresponding physical drawing, which is sufficient for the proof.

For efficiency the 129,286 labelled point pairs are grouped by their 44,623
exact nonzero difference vectors, up to sign. Every pair retains its labels;
grouping neither adds a geometric premise nor drops a pair. Modular tests
use (dx^2,dx*dy,dy^2), so opposite vectors have identical outcomes.

## 3. Colour certificates and the original exception

Exactly 90,055 residue supergraphs are 3-degenerate. Repeatedly remove a
vertex of degree at most three. Reversing a complete removal order gives a
proper four-colouring; the checker also validates that word on every edge.

Of the 49 remaining buckets, 48 have explicit 509-entry four-colour words
in `certificate.json`. These words are checked directly on all supergraph
edges, without a SAT call. Their generation used ordinary four-colour CNFs:
one colour per vertex and incompatible equal colours on edge endpoints.
Only positive assignments are used. Solver timeouts and UNSAT would not be
accepted as negative physical results.

The last bucket contains exactly 30 frames. All are exactly the original
metric by the identities in Section 1. Its 2,442 modular edges are also
checked to be physical edges. The original source's 509 one-vertex-deletion
words are hash-pinned, decoded independently, and directly checked against
these edges. Every proper induced subgraph is contained in one such deletion,
and inherits its word. Thus **all** subsets of at most 508 points are covered,
whether or not they contain the anchor or the selected equilateral triangle.
No fresh UNSAT claim about the incumbent is needed for this conclusion.

## 4. Verification and trust boundaries

`scan.cpp` enumerates every frame and every difference group with bounded
integer modular arithmetic. It records exact frame membership and the full
list of passing group IDs for each bucket outside the repository.

`check.py` rebuilds the same frame domain using Cramer's rule on the three
equations q(a)=q(b)=q(a-b)=1, rather than the expanded determinant formula
used by the producer. It separately projects the original coordinate rows,
checks all labelled difference-group memberships, and uses NumPy integer
matrix products to recompute **every** bucket's entire contact list. The
comparison is entrywise, not just a match of aggregate totals. It independently
repeats degeneracy peeling with stack order and directly validates every
positive colouring. It checks every collinear exception exactly.

Both C++ products and NumPy dot products fit signed 64-bit arithmetic:
each modular factor is less than p and 3*(p-1)^2 < 2^63. Python's field
arithmetic and Cramer's-rule determinants use arbitrary-precision integers.
The native full scan is also run with undefined-behaviour sanitization.

`controls.py` compares the two exact metric expressions on 100 deterministic
field-valued frames and audits all 129,286 pairs of the deformed fixture
(0,52,55). This actual 509-point graph has 1,517 edges and a directly checked
four-colouring. It also rejects malformed colour words and ring maps,
tests a singular frame and K5, and includes an explicit modular false-positive
edge to check the intended one-sided interpretation.

Trust remains in the written affine reduction, input provenance, ordinary
Python/C++/NumPy integer semantics and the checker. The exact coordinate
generator is shared; the full replay is author-side cross-validation, not
independent peer review or a formal proof. Generated inventories and build
products are omitted from Git and reproducible from the published source.

The prior `hadwiger_nelson_odd21_affine` result introduced a related general
incident-direction metric gate for a different 21-point source. This work
uses a different fixed support and a sound modular-supergraph certificate;
it makes no priority claim for affine metrics or finite-field filtering.
