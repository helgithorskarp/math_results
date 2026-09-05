# One arbitrary point and two completion points cannot repair dense506

**Theorem (exact computer-assisted).** Let H be either of the two pinned
506-point dense hosts below, let C be all nonhost plane points having at
least three unit neighbours in H, and let c be the published fixed
four-colouring of H. For every plane point x and every T subset of C with
|T| at most two, the strict unit-distance graph on H union T union {x}
has a proper four-colouring extending c.

These graphs have at most 509 vertices. In particular, deleting any host
vertex, or taking any other subgraph, cannot produce a five-chromatic graph
of order at most 508 in this stratum. No record improvement is constructed.
The theorem does not cover three-point additions using at least two points
outside H union C, or another relative placement.

## Hosts and imported support

Use the pinned Parts tables A (159 points) and V (214 points), in their
source row order. Put

\[
 \alpha=i\sqrt3,\quad z=\sqrt{33},\quad\beta=\alpha z/3,
 \quad r=\sqrt{-408+72z}>0,
\]
\[
 t=(5+z+5\alpha-\beta)/12,\quad B=A\cup(\overline A+t),
\]
\[
 u_\pm=\frac{-18-6z-30\alpha+6\alpha z
                  \pm r(3+6\alpha+\alpha z)}{72},\qquad
 H_\pm=B\cup u_\pm(V-V[10]).
\]

Here V[10]=alpha/6. The exact host construction and fixed colour row are in
the [two-point extension source](../hadwiger_nelson_dense506_two_point_extension/PROOF.md),
commit `dc57db82a86037be322374b20b31a65fb73df452`. Its
[independent exhaustive review](../hadwiger_nelson_dense506_two_point_extension_review1/README.md)
is at `de9cd586d128b12df93d3fdb228d573fe373575c`.

For each H, its complete C=C3(H) has 1,420 points. All coordinates belong to
K=Q(z,r,alpha), with alpha^2=-3, z^2=33 and r^2=-408+72z. The
[simultaneous completion theorem](../hadwiger_nelson_dense506_completion_closure/PROOF.md),
source `b20e53348fd367cb9d9ad182371414b3d23edac8`, proves that the full
U=H union C, of order 1,926 and size 12,074, has a four-colouring preserving
c. The [independent completion review](../hadwiger_nelson_dense506_completion_closure_review1/README.md),
source `7cbe117f52d85926033e40e140b732d8a000138a`, accepted this imported
result during the present pass. This covers x in U. It also covers every
pair of C points while keeping c fixed. Below assume x outside U and two distinct chosen points p,q in C;
fewer distinct added points are covered by the earlier two-point theorem.

Host labels 0 through 505 and candidate labels 0 through 1419 are inherited
exactly. Candidate j has U label 506+j. The candidate order is lexicographic
in the canonical tuple (d,X1,Xz,Xr,Xzr,Y1,Yz,Yr,Yzr), representing

\[
 [X_1+X_z z+X_r r+X_{zr}zr+
   \alpha(Y_1+Y_z z+Y_r r+Y_{zr}zr)]/d,
\]

with positive d and gcd of all nine entries equal to one. Use the same
labels for H_minus under the automorphism sigma:r->-r. In this census all
H and C coordinates can be multiplied by D=2592 to become integral in the
basis (1,z,r,zr,alpha,alpha*z,alpha*r,alpha*z*r).

## The only possible list obstructions

For a plane point v outside H let L(v) be the colours in {0,1,2,3} absent
from its unit neighbours in H. For candidates these lists are nonempty,
and no unit edge in C has equal singleton lists at both ends, by the
imported two-point theorem (also checked again here).

Since x is outside C and outside H, it has at most two host neighbours.
If it has at most one, or two of the same colour, then |L(x)| is at least
three. Colour p and q first, then give x a colour different from their
colours. Thus the only remaining case has exactly two host neighbours
h_i,h_j of different colours, and

\[
 M=L(x)=\{0,1,2,3\}\setminus\{c(h_i),c(h_j)\},\qquad |M|=2.
\]

If x is adjacent to at most one of p,q, the same argument works with its
two available colours. Suppose it is adjacent to both. The following
three-vertex list criterion is complete under the candidate-pair hypothesis:

- If p,q are nonadjacent, failure occurs precisely when their lists are
  different singleton subsets of M.
- If p,q are adjacent, failure occurs precisely when both lists are subsets
  of M.

For the first case, failure means every permitted choice of colours for p
and q uses both members of M. This forces the two different singleton
lists; any additional or outside choice avoids the failure. For the
triangle, a proper colouring chooses distinct representatives of its three
lists. Every individual list is nonempty. Every union of two lists has
size at least two: M has size two, and the candidate pair has no equal
singleton obstruction. Therefore the only possible failure of the
three-set matching condition is that the total union has size two. This
is exactly L(p) union L(q) subset M. Equivalently, the criterion follows by
direct enumeration of three colour choices; the controls exhaust all
10,704 applicable palette/edge cases and confirm the criterion exactly.

In particular, every failure requires two unit neighbours p,q of x in C
whose lists are subsets of M. Call such C-neighbours **eligible** for x.
It suffices to enumerate all x with at least one eligible C-neighbour and
then inspect pairs of its eligible neighbours.

## Complete finite geometry

Fix i<j with c(h_i) different from c(h_j), and a candidate p whose list is
contained in the complementary two-colour palette M. If x is a common
unit neighbour of h_i,h_j,p, these three distinct points lie on its unit
circle and are noncollinear. They determine x uniquely. Every possible
list obstruction is therefore captured by the finite domain of such
host-host-candidate triples.

No assumption that arbitrary x lies in K is made. The unit-circle equations
for these three neighbours, after subtracting one from the other two,
form a nonsingular real linear system. In coordinates X+alpha*Y, its
coefficients lie in F=Q(z,r), so its unique solution belongs to F^2 and
hence x belongs to K. This is a consequence of the incidences, not a grid
restriction on the theorem.

For three scaled points let a,b,c in F be their squared side lengths, where
the scaling is D=2592. Their circumradius is one in the unscaled plane iff

\[
 abc=D^2(2ab+2ac+2bc-a^2-b^2-c^2).
\]

The side lengths are strictly positive for distinct points. Thus a
collinear triple, whose area term is zero, cannot pass this equation. For
a surviving triple write its differences from the first point as
(dx,dy),(ex,ey), and let det=dx*ey-ex*dy in F. Its scaled centre relative
to the first point is

\[
 X=\frac{a\,ey-b\,dy}{2\det},\qquad
 Y=\frac{dx\,b-ex\,a}{6\det}.
\]

These formulae come directly from the two subtracted circle equations.
Exact field arithmetic gives each canonical centre. Triples with a known
centre in U are already closed by the simultaneous completion theorem;
they may be removed using the full verified U adjacency. Every recovered
centre outside U has exactly its indicated two host neighbours, since a
third would place it in the complete C3(H). Consequently its eligible
neighbour list is exactly the list of candidate indices recovered for that
same host pair. The audit additionally reconstructs all its U neighbours
to check this inference entry by entry.

## Exact census and colouring certificate

There are 96,003 differently coloured host pairs and **52,550,758** eligible
host-host-candidate triples. The primary screen removes 62,877 triples
centred in U. Reducing the circle equation modulo

\[
 p=10007,\quad z\mapsto283,\quad r\mapsto6718
\]

leaves 6,175 rows for exact testing. Exactly **1,999** have external
centres, giving **1,085 distinct points**. Their numbers of eligible
C-neighbours are:

| Eligible C-neighbours | Points |
|---|---:|
| 1 | 466 |
| 2 | 372 |
| 3 | 204 |
| 4 | 38 |
| 5 | 5 |

Thus 619 points have at least two eligible neighbours, giving

\[
 372\binom22+204\binom32+38\binom42+5\binom52=1262
\]

candidate pairs. None has either list obstruction. Both the primary
verifier and the audit explicitly choose permitted colours for x,p,q in
every one of the 1,262 cases. Combining these choices with c colours the
whole H union {x,p,q}; restriction handles every deletion. Together with
the elementary cases above, this proves the theorem.

The [primary source](engine.py) and [verifier](verify.py) regenerate all
points and incidences. The canonical point-list SHA-256 is
`28b46f5eae9a537d8a189d03284e32d9012fbccde35f05bd72e19ee1f1699f43`.
The sorted positive triple stream has SHA-256
`940266d1d44a967083fdaf371623bff7bf03fc2eca5e938c8de838a8b9891c96`.
These hashes use compact JSON without a trailing newline.

For a compact colour certificate, each implementation chooses the
lexicographically first proper triple colour (cx,cp,cq), and hashes the
JSON row [outside_index,p_index,q_index,cx,cp,cq] followed by a newline,
ordered by outside index and candidate pair. This complete witness stream
has SHA-256
`5dce583891389a59cecc768c67db11e1b5afd4820fdb50bd4c6124faa5f7dcaf`.
Its rows are regenerated rather than committed as an exhaustive dump.

## Audit and exact scope

The [audit](audit.py) uses the independently published reviewer's generic
quotient-ring monomial multiplication, not the primary real-field
arithmetic. It rebuilds the full U graph and candidate lists. It then
rescans every eligible triple **without early U-centre removal**, using
p=5281,z=126,r=3928 and the direct determinant equation abc-12*det^2=0 in
normalized modular coordinates. All 72,379 survivors are decided by exact
complex norm arithmetic. In scaled complex coordinates d,e from the first
vertex, the exact identity is

\[
 abc+D^2(\bar d e-\bar e d)^2=0.
\]

This independently gives 62,877 known-centre triples and the same 1,999
external triples and 1,085 points, matched entry by entry.

For each of the two roots the audit checks all 1,085*1,926=2,089,710
point-to-U pairs. There are 6,857 true incidences, including exactly 2,170
host incidences. Modulo 5281, respectively 7,010 and 7,028 norm tests survive;
all are decided exactly. All eligible neighbour lists match the primary
census. Both roots give all 1,262 explicit colour witnesses.

The r->-r automorphism commutes with complex conjugation and preserves
unit-distance equalities. It maps H_plus,C_plus and the complete relevant
triple domain to their minus counterparts. The audit checks its action on
all 64 basis products and verifies the labelled incidences for both roots.
Thus a second exhaustive triple scan for the other root is unnecessary.

The modular tests reject impossible equalities only; every survivor is
checked in exact arithmetic. Denominators of the fixed U points divide
2592. For recovered-point incidence checks, noninvertible modular
denominators fall back to exact arithmetic. No floating-point decisions or
SAT calls are used. The enumeration and verifier are ordinary mathematical
code, not a proof-assistant formalization.

Imported trust comprises the complete C3 census, the fixed host colouring,
the simultaneous U colouring, source coordinate tables and their pinned
geometric construction. The present audit rechecks geometry and incidences
needed for this stratum but does not repeat the earlier 21,464,520-triple
C3 completeness proof. SHA-256 is used for data identity; CPython provides
arbitrary-precision integer semantics. The audit is an author-run check
using independently derived published arithmetic, not a new external review.
External review of this theorem remains pending.

A possible one-deletion/three-point counterexample must now use at least
two new points outside H union C. These cases are not tested here. The
current census is preserved for reuse, but no adjacency census between
its outside points or subsequent repair stratum was started in this pass.
