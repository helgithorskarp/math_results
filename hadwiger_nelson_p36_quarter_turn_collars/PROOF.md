# Exact closure of the P36 quarter-turn collars

Put

\[
 \omega=(1+i\sqrt3)/2,\qquad
 P=P_{36}=\{a+b\omega:a^2+ab+b^2\leq36\}.
\]

Thus `P` has 127 points.  For an ordered pair `p,q in P`, define

\[
 c_{p,q}=\frac{p-iq}{1-i}
 \quad\hbox{and}\quad
 Q_k=c_{p,q}+i^k(P-c_{p,q})\quad(0\leq k<4).
\tag{1}
\]

Let `G(p,q)` be the complete strict unit-distance graph on the physical set
`Q_0 union Q_1 union Q_2 union Q_3`: equal points are identified, and every
pair of distinct physical points at distance one is an edge.

## Theorem

Every one of the `127^2=16,129` graphs `G(p,q)` is four-colourable.  If
`p != q`, the four patches have empty total intersection and exactly 504
distinct physical points.  There are 16,002 such empty-intersection
placements.  Their edge counts range from 1,368 to 1,592.

This is a finite fixed-quarter-turn family theorem.  It is not a statement
about four arbitrary translated patches or about arbitrary plane
unit-distance graphs.

## 1. The collar and its exact size

Equation (1) is equivalent to

\[
 p-c_{p,q}=i(q-c_{p,q}).
\]

Consequently `p` belongs to both `Q_0` and `Q_1`.  Applying successive
quarter turns gives a cyclic collar: every adjacent pair `Q_k,Q_{k+1}`
shares the point

\[
 x_k=c_{p,q}+i^k(p-c_{p,q}).
\]

All anchor centers are distinct.  Indeed, put `K=Q(i sqrt(3))`.  If two
centers agree, then

\[
 p-p'=i(q-q').
\]

The left side is in `K`.  A nonzero right side could be in `K` only if
`i in K`, which is false.  Hence `p=p'` and `q=q'`.

The same argument shows that an adjacent pair has only its named collision.
An opposite collision would give

\[
 2c_{p,q}=u+v\in K
\]

for some `u,v in P`, while direct expansion gives

\[
 2c_{p,q}=p+q+i(p-q).
\]

Thus an opposite collision forces `p=q`.  If a point belonged to all four
patches, it would equal both `x_0` and `x_1`; this again forces `p=c`, hence
`p=q`.  Conversely `p=q` gives `c=p`, which is a common point.  Therefore
exactly the 127 diagonal anchor pairs have nonempty total intersection.
For every other pair the four named adjacent collisions are distinct and
there are no others.  The support size is consequently

\[
 4|P|-4=4(127)-4=504.
\]

## 2. Complete exact graph reconstruction

Every collar point has a unique representation

\[
 \left(\frac{a+b\sqrt3}{4},\frac{c+d\sqrt3}{4}\right),
 \qquad a,b,c,d\in\mathbb Z.
\tag{2}
\]

For a difference represented by `(a,b,c,d)`, its squared norm is

\[
 \frac{a^2+3b^2+c^2+3d^2+2(ab+cd)\sqrt3}{16}.
\tag{3}
\]

It is a unit vector exactly when

\[
 a^2+3b^2+c^2+3d^2=16,
 \qquad ab+cd=0.
\tag{4}
\]

The first equation bounds `|a|,|c|` by 4 and `|b|,|d|` by 2.  Exhausting
that box gives twelve unit vectors.  The verifier creates the collision-
merged point dictionary for each representative and looks up all twelve
translates of every point.  This reconstructs the complete strict graph;
there is no geometric tolerance or assumed list of cross edges.

The hexagonal dihedral group preserves `P`, commutes with quarter turns up
to reversing their order, and maps the collar at `c` isometrically to the
collar at the transformed center.  Exact canonicalization partitions the
16,129 centers into 1,408 orbits: one orbit of size 1, 126 of size 6, and
1,281 of size 12.  There are 1,392 empty-intersection orbits and 16 common-
point orbits.

As an alternate reconstruction, the controls use the two relative
interfaces

\[
 Q_0-Q_1:\quad u-(iv+(1-i)c),
 \qquad
 Q_0-Q_2:\quad u+v-2c.
\]

They bucket all 16,129 adjacent offsets `u-iv` and all 469 opposite sums
`u+v`, then recover collisions and edges by the twelve unit displacements.
The resulting physical point and edge sets agree entry for entry with the
direct construction for all 1,408 representatives.

## 3. Positive four-colour cover

For `z=a+b omega in P`, write

\[
 r(z)=a-b\pmod3.
\]

Inside each patch, use colours `0,1` for the zero residue and colours `2,3`
for the two nonzero residues.  Each layer has one bit that chooses the
zero-residue colour and one bit that optionally swaps the nonzero colours.
Internal unit edges are automatically proper.

A collision requires its two formal colours to agree.  A cross edge whose
ends lie in the same palette requires them to differ.  Each such condition
is one XOR equation in the relevant four layer bits; a mixed-palette cross
edge is automatically proper.  The verifier tries all sixteen assignments
independently in each channel and then checks the resulting physical word
on every reconstructed edge.

This residue form succeeds on 797 center orbits, representing 8,821 of the
16,129 placements.  It fails on the remaining 611 orbits.  For each failure,
`colourings.json` gives a literal four-colour word in lexicographic physical-
coordinate order.  The verifier checks every digit and every edge of all 611
words.  These are positive witnesses; the producer's backtracking search and
no SAT-unsatisfiability answer are proof premises.

The two routes cover all 1,408 orbits, proving the theorem.

## Scope

Among the 16,002 record-sized empty-intersection placements, 15,342 have no
strict unit edges beyond the four constituent patch graphs after collision
merging.  The other 660 placements, in 58 dihedral orbits, have additional
contacts; the densest has 1,592 edges.  All are covered above.  Thus the
quarter-turn collar supplies no unrestricted non-four signal and is retired.

The theorem does not cover a different relative rotation, a non-cyclic
choice of four motions, five or more patches, arbitrary subpatch placements,
or any construction outside (1).  It proves neither a global lower bound on
the order of five-chromatic plane unit-distance graphs nor a new record.
