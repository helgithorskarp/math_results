# Field confinement for dense506 three-point repairs

**Theorem (exact computer-assisted).** Fix either pinned dense506 host H
and its published proper four-colouring c. Write

\[
 z=\sqrt{33},\qquad r=\sqrt{-408+72z}>0,\qquad
 F=\mathbb Q(z,r),\qquad K=F(i\sqrt3)\subset\mathbb C.
\]

If c fails to extend after any three Euclidean-plane points are added,
**all three added points belong to K**. Equivalently, adding any three
points of which at least one is outside K preserves extension of c.
Every subgraph of such an enlarged graph is therefore four-colourable,
including every <=508 one-deletion/three-point repair in this case.

The case of three added points in K is open. A failure to extend this one
fixed colouring would not itself prove five-chromaticity. No <=508
five-chromatic graph is established. Other host placements and larger
addition patterns are not covered.

## Imported geometric reduction

We use scaled coordinates (X,Y) for X+i*sqrt3*Y, with norm
N(X,Y)=X^2+3Y^2. Membership in K is equivalent to (X,Y) in F^2.
Let J(X,Y)=(-3Y,X) and R=(I+J)/2; R is rotation by 60 degrees.

The exact hosts use the Parts tables A,V of sizes 159,214, with
alpha=i*sqrt3, beta=alpha*z/3,

\[
 t=(5+z+5\alpha-\beta)/12,\quad B=A\cup(\overline A+t),
\]
\[
 u_\pm=[-18-6z-30\alpha+6\alpha z
          \pm r(3+6\alpha+\alpha z)]/72,
 \quad H_\pm=B\cup u_\pm(V-V[10]),
 \quad V[10]=\alpha/6.
\]

The [original exact host/C3 theorem](../hadwiger_nelson_dense506_two_point_extension/PROOF.md)
specifies the labels and fixed colour row. Each host has 506 vertices and
2,389 unit edges. All X,Y coordinates use denominator D=2592 and the
faithful basis (1,z,r,zr). The colour-row SHA-256 is
`010e6190aa14b6eadc285a6131d7b455bd5434f79ed9b4f69cdfb2848acddcb4`.

The [preceding midpoint reduction](../hadwiger_nelson_dense506_triangle_midpoint_reduction/PROOF.md),
source `c6166e1d4f0911a5ae5db6641248305e5f617975`, is an explicit premise.
It shows that every remaining non-field failure consists of three points
x0,x1,x2 outside H union C3(H), forming a unit equilateral triangle. Each
has exactly two differently coloured H neighbours, and all three available
lists are the same two-colour set. The three host pairs therefore all
use the same complementary pair of host colours.

The three x_i lie in one real quadratic extension of F in scaled
coordinates. Its nontrivial conjugation tau fixes the H points and sends
each x_i to the other unit-circle intersection at its host pair. Write
m_i=(x_i+tau(x_i))/2, which is precisely that host pair's midpoint.
The preceding result excludes mixed field membership, translated conjugate
triangles and coincident midpoints. Thus the m_i form a nondegenerate
oriented equilateral triangle of side ell with 0<ell<1. The lines through
the three host pairs are concurrent at a point o in F^2; they cannot all
be parallel. No new scan of the old C3 or eligible-centre census is used.

## A necessary unit-radius equation at the concurrency point

Put L=ell^2. The direct isometry taking the labelled triangle x_i to
its conjugate triangle is a nontrivial rotation about o. If its angle is
theta, averaging the two triangles gives a similarity of squared scale
L=(1+cos(theta))/2. For each i,

\[
 N(x_i-m_i)=\frac{1-L}{L}N(m_i-o).                         \tag{1}
\]

Indeed x_i-m_i is the half difference of x_i-o and its rotation, whereas
m_i-o is the half sum. Their squared norm ratio is
(1-cos(theta))/(1+cos(theta)). The denominator is nonzero because ell>0.

Let d_i be the full vector between the two H neighbours of x_i.
The vector x_i-m_i is perpendicular to d_i. The unit distance from x_i
to either host endpoint, together with (1), gives

\[
 4(1-L)N(m_i-o)=L(4-N(d_i)),\qquad i=0,1,2.              \tag{2}
\]

Equations (2) and concurrence are necessary. We need not solve a square
root or assert sufficiency. The computation deliberately retains midpoint
triangles of every positive side length, and does not impose root-sign,
field-square or real-positivity tests. This enlarges the tested family.

## Complete midpoint triangle census

Take every unordered host pair whose two colours differ. There are 96,003.
Group these pairs by their two host colours and exact midpoint. The six
host-colour groups have the following census; distinct midpoint indices
are in lexicographic order of their eight integer coordinate numerators.

| Host colours | Distinct midpoints | Unordered midpoint pairs | Midpoint triangles |
|---|---:|---:|---:|
| 01 | 10,377 | 53,835,876 | 524,077 |
| 02 | 10,369 | 53,752,896 | 775,261 |
| 03 | 10,889 | 59,279,716 | 811,210 |
| 12 | 10,216 | 52,178,220 | 575,682 |
| 13 | 10,797 | 58,282,206 | 629,492 |
| 23 | 10,048 | 50,476,128 | 734,830 |
| Total | 62,696 | 327,805,042 | 4,050,552 |

For each i<j the enumerator checks both third points

\[
 m_i+R(m_j-m_i),\qquad m_i+R^{-1}(m_j-m_i).
\]

It keeps a point only if its index k exceeds j. This counts each
unoriented equilateral triangle exactly once: its two least indices
specify i,j, and its third vertex specifies one orientation. Coincident
midpoints are excluded by i<j<k. Membership is an exact eight-coordinate
lookup, including full key equality after hashing.

Choosing one actual H pair at each midpoint gives exactly
**140,742,349 host-pair assignments**. Every possible non-field failure
from the imported reduction occurs among these assignments. No host pair
is omitted for excessive chord length or any other geometric heuristic.

## Denominator-free modular filter

Use integer numerators with common coordinate denominator 2D. Thus
M_i=2D*m_i is the sum of its two original host numerators, and
v_i=2D*d_i is twice their difference. Write Q=(2D)^2 and
A=N(M_1-M_0), so L=A/Q. For vectors in scaled coordinates, let
[u,v]=u_X*v_Y-u_Y*v_X.

Choose a pair a,b for which delta=[v_a,v_b] is nonzero. Its line
intersection has numerator

\[
 \kappa=[v_b,M_b-M_a],\qquad
 O=\delta M_a-\kappa v_a,\qquad 2D\,o=O/\delta.
\]

For W_i=delta*M_i-O, concurrence and (2) become the polynomial equalities

\[
 [v_i,W_i]=0,\qquad
 4(Q-A)N(W_i)=A(4Q-N(v_i))\delta^2,\quad i=0,1,2.        \tag{3}
\]

All coefficient calculations lie in F. The first implementation evaluates
(3) modulo p=10007 using z=283,r=6718. These satisfy z^2=33 and
r^2=-408+72z modulo p. If any pair of lines has nonzero determinant in the
finite field, the implementation uses that pair and tests all six
identities. If **all three determinants vanish modulo p, it retains the
assignment without rejecting it**. This singular fallback is essential.

A genuine exact solution cannot be lost: a chosen nonzero modular
determinant comes from a nonzero exact determinant; (3) follows by clearing
that denominator. Exact polynomial identities remain identities under the
checked modular homomorphism. The exceptional case is retained. No
floating-point decision is used, and modular survival is not a proof of
geometric feasibility.

The filter leaves **34,938 assignments**. Exact field arithmetic shows
that in every one all three host-pair directions are parallel. There are
104,814 exact pairwise determinant checks. Parallel lines through three
noncollinear midpoints cannot all be concurrent: parallel lines sharing
a point would be one line and would contain all three midpoints.
Therefore no survivor is a non-field obstruction. This proves the theorem.

## Independent computations and exact identities

The full midpoint census has two different exact representations.
[enumerate.cpp](enumerate.cpp) performs eight-integer lookups. The
[packed audit](packed_audit.py) embeds a vector (a0,...,a7) as the Python
integer sum a_t*B^t with B=262144. Linear rotations become addition of
precomputed integers. If M bounds every input coefficient, the difference
between a candidate lookup key and an existing doubled point has every
coefficient bounded by 10M. Here M=9072 and 10M<B-1. The highest nonzero
digit therefore dominates all lower digits, proving that a zero packed
difference is exactly a zero vector. There are no carry ambiguities.
The audit considers all 327,805,042 pairs and matches every one of the
4,050,552 emitted rows to the native stream in order, including EOF.

The second screen reconstructs H- with the
[independent reviewer's generic eight-basis arithmetic](../hadwiger_nelson_dense506_two_point_extension_review1/independent_check.py).
It verifies the entire partition of the 96,003 host pairs, supplies a
second modular image p=5051,z=2194,r=528, and uses
[a separate Cramer-rule intersection calculation](audit_screen.cpp).
For a line represented by (a,b,c)=(-v_Y,v_X,v_Y*M_X-v_X*M_Y), the second
calculation obtains the intersection from its line coefficients rather
than the primary vector-difference formula. It rescans all 140,742,349
assignments and produces the **identical 34,938-row survivor stream**.

Finally [audit_exact.py](audit_exact.py) checks parallelism using generic
complex quotient-ring multiplication: u*conjugate(v)=v*conjugate(u).
It independently verifies all 104,814 equalities for H-, and all residual
midpoint-triangle relations. Primary checks use the real four-coordinate
determinant for H+. The automorphism r->-r also explains why exact
incidences and the same labels apply to both hosts.

Canonical file identities, including their final newline:

| Stream | Bytes | SHA-256 |
|---|---:|---|
| Midpoint triangles | 78,343,591 | bac810715525907a23cdff32f98e9237ae16f37aa29c4f1523e3395bb6b02d54 |
| Each survivor stream | 1,456,306 | 88580a61a55170031b3207f53a8b3a058713fb2cb414339bb5bd9ffff18fa920 |

Triangle rows are `group i j k epsilon`. Survivor rows append the six
host labels, pair by pair in that midpoint order. Group order is
01,02,03,12,13,23; native loops use increasing i,j and epsilon=-1,+1.
Host-pair lists use increasing first and second labels. The source and
expected identities regenerate these streams; the large streams are not
public certificates by themselves and are not committed.

## Controls, arithmetic bounds and trust

A positive control is an actual unit triangle with six rational host
points in scaled coordinates. Its host numerators, divided by72, are

```
(-51,-17), (51,17), (57,-17), (-45,17), (3,37), (3,-31).
```

Their pair midpoints are m0=(0,0), m1=(1/12,0), m2=(1/24,1/24).
With o=(1/24,1/72) and q=143/3, put
x_i=m_i+J(m_i-o)*sqrt(q). The controls check all six host incidences and
all three triangle edges exactly by separating the constant and radical
coefficients. The six hosts have no unit edges. Both native screens keep
this nonsingular geometric fixture; it is not a claimed record graph.
Doubling one chord without moving its midpoint breaks the unit-radius
condition and both screens reject it. A parallel singular fixture is
retained by both screens, as required for completeness. Native and packed
midpoint enumeration match the positive fixture; duplicate input midpoints
are rejected.

Strict-warning builds use GCC12.2, C++17 and -O3. Address and undefined-
behaviour sanitizer builds cover the first30 indices in all six midpoint
groups and the first10,000 triangles in each screen; outputs match their
optimized counterparts. Actual midpoint coefficients have absolute value
at most9072, and an enumerator key is bounded by8M. The input guard bounds
coefficients by10^8 even outside this instance, leaving those linear
expressions below8*10^8. Hash multiplication uses unsigned wraparound;
collisions are resolved by full key comparison.

Screen coordinates and all reduced intermediates are in [0,p), with
p<=20000. Unreduced products/sums in the written formulas are bounded by
4p^2, well within signed64-bit range. Counts in this run are below2^32;
64-bit unsigned counters suffice. Python exact checks use arbitrary-
precision integers. There are no square-root approximations, native solver
calls, incomplete proof traces or random choices.

The imported midpoint reduction and earlier extension results remain
premises. The new computation has author checks with independent
representations, a second modular image and exact residual verification;
it is not an external review of this new theorem. Remaining trust includes
those premises, source/data identity, CPython and compiler/runtime semantics,
and ordinary unformalized mathematical and code reasoning. Complete
reproduction requires regenerating the finite scans and running their
checks; summary counts and hashes alone do not prove their completeness.

The next remaining case consists entirely of field points. Each relevant
point is a unit-circle intersection of one of the 96,003 differently
coloured host pairs, giving at most192,006 candidates before duplicates
and other exclusions. That field-point census has not been started here.
