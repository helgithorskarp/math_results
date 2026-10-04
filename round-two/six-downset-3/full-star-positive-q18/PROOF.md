# An entry-positive capped Hoffman matrix on the q18/k9 downset

Actual author: **six-downset-3, researcher**, 2026-10-04. Complete ordinary
proof with exact finite certificates; independently **UNREVIEWED**. The
verifier is separate from the numerical producer but by the same author.
The completeness, physical-norm, arbitrary-real box, rank/congruence and
weighted-Laplacian bridges are **UNFORMALIZED**.

Let `a,b,c` be distinct and let `Z,W` be disjoint nine-element sets disjoint
from them. On the21-point ground define

\[
D=\{A:|A|\le2\}\cup
\{A:|A|=3,\ |A\cap\{a,b,c\}|\ge2\}
\setminus\{\{b,c,z\}:z\in Z\}.
\]

The deletion applies to the union. Every triple's proper subsets remain,
so this is a downset. It has N278 members, including the actual empty
vertex and loop. The point-star sizes are58,49,49,nine23 and nine24. Its
unique greatest star is `S_a`, of size58. Relabeling preserves the theorem.

**Theorem.** The explicit rational original278-by278 matrix M below has
disjointness support, M1=1, and L=220M+58I>=0. **Every allowed entry is at
least1/2048**, including all empty-row entries and the empty loop. Moreover
M<=I. Both L and278I-L have rank277, M has simple least eigenvalue-29/110
and simple greatest eigenvalue1, and its other276 eigenvalues lie in

\[
[-29/110+1/7040,\ 1-1/2048].
\]

All these properties persist on the **complete29,802-dimensional closed
REAL box** of independent original repairs |t_j|<=1/3814656. Throughout
that box, every allowed M entry remains at least1/2048, both nonzero
proper endpoint floors are at least1/64, and the other276 eigenvalues lie
in

\[
[-29/110+1/14080,\ 1-1/2048].
\]

This strictly pays entry positivity on a carrier whose previous signed
center had four negative empty-row orbits and excluded all repairs that
only decreased nonstar edges. It is a **new matrix**, with fresh factors.
The old center is still valid signed H evidence. No all-downset H/I,
other carrier, optimal margin, first-open-order or historical-priority
claim follows.

## Explicit matrix and empty completion

Use bits0,1,2 for `a,b,c`, bits3..11 for `Z`, and bits12..20 for `W`.
Index the proper members by increasing masks. Put
`o(A)=(A&7, |A intersect Z|, |A intersect W|)`.
The certificate includes all143 unordered orbit keys for disjoint,
nonanchor proper pairs and their **new** integer numerators over
**1048576**. A single bounded numerical phase-I search varied all143
entries, all twelve small endpoint blocks and all180 actual-entry orbit
inequalities. Its coefficient proposal was rounded to this dyadic grid.
Fresh factors were then proposed and accepted only after the separate
integer verifier reconstructed every original action and residual. No
numerical optimization, approximate eigenvalue, old coefficient PSD
certificate or parent margin is a proof input. All defining values and
factors are included here; checking needs no parent download or code.

Define the 277-by-277 rational symmetric proper core `C` by diagonal57,
by -1 on distinct intersecting pairs, and by the listed values on
disjoint pairs not containing the anchor `{a}`. For every nonstar `A`,
set

\[
 C[A,\{a\}]=C[\{a\},A]
   =-\sum_{B\in S_a\setminus\{\{a\}\}}C[A,B].
\]

The star/star block is `58I-J`, so its row sums vanish. The displayed
anchor rule gives `Ch=0` on every other row, where `h=1_(S_a)`.
All proper support and diagonal positions are fixed as required.
With `n=277`, put

\[
 E=\begin{bmatrix}-\mathbf1_n^T\\I_n\end{bmatrix},\quad
 U=278I_n-J_n-C,\quad
 L=J_{278}+ECE^T,\quad M=(L-58I_{278})/220.
\]

The empty vertex is the first actual vertex. In particular,
`L[empty,A]=1-sum_B C[A,B]` and
`L[empty,empty]=1+sum_(A,B) C[A,B]`.
The columns of `E` span `1^perp`, so `L1=2781` and `M1=1`.
The proper block of `L` is `J+C`, which proves every required
intersecting entry of `M`, including proper diagonals, is zero.
The identity `278I-J=E(278I_n-J_n)E^T` holds also on the empty row;
therefore `278I-L=EUE^T`.

The separate checker reconstructs every76,729 proper position and
every77,284 actual lift position. It checks symmetry, support, every
row sum, all point-stars, both endpoint identities, and the whole action
of `L` on the centered maximum star. It also records whole original
matrix digests. A numerical or quotient row check is not the proof.

## All277 original proper directions

Six mutually orthogonal subspaces exhaust the proper Euclidean space:

| Sector | Explicit functions | Dimension |
|---|---|---:|
| TT | indicators of the23 physical member orbits |23|
| Z | on each of eight eligible orbits, sum of a zero-sum function on its Z points |64|
| W | the corresponding nine eligible W orbits |72|
| ZZ | functions on the36 Z-pairs with every point-incidence sum zero |27|
| WW | the corresponding W-pair space |27|
| ZW | mixed-pair arrays with all nine row and column sums zero |64|

For each standard orbit the eight vectors `e_0-e_j`, `1<=j<=8`,
have Gram a positive orbit multiplier times `I_8+J_8`, so all copies
are independent. The TT indicators have disjoint positive masses.
For a within-pool pair sector take every edge `(i,j)` on `{1,..,8}`
other than `(1,2)` as a free pivot. Put2 on it, -2 on `(1,2)` and
`-2*1_(t in {i,j})+2*1_(t in {1,2})` on `(0,t)`.
These27 vectors have zero incidence and their own unique free pivot2,
so they are independent. The64 mixed rectangles
`(e_0-e_i)(e_0-e_j)^T` have unique interior pivot1.
Zero sums prove cross-sector orthogonality. The checker also verifies
every cross-sector Gram position and these complete independence
decoders. The dimensions sum to277, proving completeness without an
unexamined representation-theoretic remainder.

For each endpoint it checks the original row of the image of every
basis vector: **2*277^2=153458 positions**. Its direct original-entry
Gram computations and action decoders show that every standard copy
has the stated small action, and every pair/rectangle direction has
the stated scalar action. Thus twelve original blocks suffice for
both full matrices, with no assumption about omitted sectors.

The lower TT Gram annihilates the actual star indicator, whose anchor
coefficient is1. Delete only the plain-anchor TT coordinate to obtain
the22-by-22 certificate. Adding a multiple of the star does not change
the energy; hence this positive principal form controls the whole TT
space modulo the known kernel. The upper TT block retains all23
coordinates. Standard blocks retain all eight or nine coordinates.

## Exact residual certificates and physical norms

Six nonscalar blocks each include a new triangular integer factor `V`
over `Q=2^32`. Let `G` be a block Gram matrix, whose entries are integers
over `D=1048576`, and form exactly

\[
 F=G-(V/Q)(V/Q)^T.
\]

The checker recomputes every residual entry and every row margin
`d_i=F_ii-sum_(j!=i)|F_ij|`. All margins are positive, and, with
`m_i` the squared norm of its actual prototype, it verifies

\[
 d_i\geq m_i/32.
\]

Since `2|x_i x_j|<=x_i^2+x_j^2`,
`F >= diag(d_i) >= (1/32)diag(m_i)`, and the added factor is PSD.
The six scalar sectors are checked exactly with prototype norm squared4.
Consequently all blocks dominate `1/32` times their physical norm.

For a standard sector use an orthonormal zero-sum pool basis. Its energy
and norm matrices are the checked prototype matrices multiplied by the
same factor1/2; this proves the stated bound on every copy. For lower
TT, take `x perpendicular h` and subtract its plain-anchor coefficient
times `h`. The new vector `y` has anchor coefficient zero, unchanged
energy, and projects orthogonally back to `x`. Thus `||y||>=||x||`,
and the same weighted norm bound proves the lower bound on `h^perp`.
All twelve exact block bounds are regenerated in `EXPECTED.json`.
This proves on the **original** proper spaces

\[
 C h=0,\qquad C|_{h^\perp}\succeq I/32,\qquad U\succeq I/32.
\]

The approximate Cholesky calculation only proposed `V`; the checker
uses integers and Fractions. Positive floating eigenvalues, factor
rounding, parent verdicts and elapsed computation are not premises.

## Complete real box and positive entries

There are30,021 disjoint unordered proper pairs and219 nonstar anchor
conditions. For each disjoint nonstar/nonstar pair use its symmetric
unit edge R. For each disjoint nonstar A and star B different from {a},
use the anchored trade

\[
R=\operatorname{edge}_{A,B}-\operatorname{edge}_{A,\{a\}}.
\]

These fix all required diagonal and intersecting positions and annihilate
h. Conversely a repair with those properties is determined by its
nonanchor entries; Rh=0 recovers each nonstar anchor entry. Star/star
entries are fixed. This proves all29,802 coordinates independent and
complete, without imposing symmetry on their real coefficients.

A unit edge has operator norm1 and an anchored trade norm sqrt(2)<=2.
For arbitrary real |t_j|<=eps=1/(128*29802)=1/3814656, therefore

\[
\|\sum_j t_j R_j\|\le2(29802)\varepsilon=1/64.
\]

C retains kernel span(h) and floor1/64 on its perpendicular. Its opposite
change in U retains floor1/64. All support and row identities persist.

The **actual empty completion** of a unit edge has entries +1 at its
proper endpoints, -1 at their empty incidences, and +2 at the empty loop.
The completion of an anchored trade has +1 at A,B, -1 at A,a, -1 at
empty,B and +1 at empty,a, with transposes; its loop change is zero.
The checker binds every29,802 generator's supported positions and zero
row sums. Thus any actual lifted position changes by at most2 per
unit generator, and at most1 per trade. The entire real box changes
**each actual M position** by at most

\[
2(29802)\varepsilon/220=1/14080.
\]

Direct integer reconstruction gives the exact center's minimum over all
60,597 admissible ordered entries:

\[
w_0=17433/20971520.
\]

In particular `w_0-1/14080 >=1/2048`. This proves the positive floor
throughout the complete real box, without evaluating sample points or
corners. The actual empty loop at the center is653267/10485760.

## Ranks and the stronger upper gap

E is injective and its range is orthogonal to1, whereas J has range
span(1). C has its single star kernel, so rank L=277. U is positive
definite, so rank EUE'=277 and its kernel is exactly span(1). The actual
lower kernel is the centered star vector278h_actual-58*1: its empty
coordinate is-58 and E' times it is278h. This proves the simple least
and greatest eigenvalues stated above. E'E=I+J>=I transfers each proper
nonzero floor to the actual endpoints; dividing by220 gives lower gaps
1/7040 at the center and1/14080 throughout the box.

Entry positivity gives a stronger upper bound directly. For any real
x perpendicular1, symmetry and M1=1 imply the ordinary weighted-Laplacian
identity

\[
x^T(I-M)x=\tfrac12\sum_{A,B}M[A,B](x_A-x_B)^2.
\]

Every nonempty vertex is disjoint from empty and its weight to empty is
at leastw=1/2048. All other summands are nonnegative. Hence

\[
x^T(I-M)x\ge w\sum_{A\ne\emptyset}(x_A-x_\emptyset)^2
=w(\|x\|^2+278x_\emptyset^2)\ge w\|x\|^2.
\]

The same argument applies throughout the box. This proves both upper
interval endpoints1-1/2048. The full fresh U certificates are also checked;
the stronger gap uses this explicit positive-weight argument, not a
numerical bound or transported parent margin.

## Why the new repair escapes the old capacity obstruction

[The signed q18 center](../full-star-capped-q18/PROOF.md), source
2bd233ac02ac1c4fc162e7fb4a9a5be8930882d9, LEMMA10276, is credited as the
proposal starting point. COMPARISON.json includes its full143 coefficient
numerators over16384. The checker binds every comparison value and
reconstructs its original core and row/loop census. Neither comparison
factors nor comparison PSD facts are used for this new point.

The old center had81 bad nonstar empty-row entries, whose total deficit
in C units was d=2497887/16384. Its positive empty-loop capacity in the
same units was ell=2021552/16384. For any real support/star-preserving
repair, let P and T be the sums of positive and absolute-negative
unordered nonstar edge changes in C units. Anchored trades have zero
nonstar row sums and zero total sum. Fixing all bad rows needs at leastd
row decrease; each negative nonstar edge pays at most twice its magnitude,
so T>=d/2. Nonnegative loop needs ell+2(P-T)>=0. Consequently

\[
P\ge(d-\ell)/2=476335/32768>0.
\]

This is a necessary real mass budget, not an optimal value or a PSD
criterion. It explains precisely why decreasing nonstar entries alone
cannot work. The **new exact center** makes9,919 unordered nonstar
entries increase and9,603 decrease, with no zeros, and has

\[
P=802154061/262144,\qquad T=3266119971/1048576.
\]

The checker verifies its entire loop change is2(P-T)=-57503727/524288
in C units, and that the new positive loop equals653267/10485760 in M
units. These data show the construction pays the budget outside the
excluded cone. No minimality, sparsity or uniqueness of this repair is
asserted. The all-real accounting argument remains ordinary mathematics.

## Literature, provenance and trust boundary

The named target is [Ellis--Filmus--Friedgut, Section4, Conjecture H](https://arxiv.org/html/2609.28404v1#S4).
The [primary submission history](https://arxiv.org/abs/2609.28404) was live
checked2026-10-04 and listed only v1 from23 September2026. H and I remain
conjectural. The classical Chvatal/projection results in that primary
preprint do not supply the matrix constructed here. H permits signed
weights; the present entry-positive conclusion is a stronger finite claim.

The carrier comes from the earlier D3
[core-edge-six source](../core-edge-six-cutoff/PROOF.md), LEMMA9826. The
complete physical basis mechanism originated in the D3
[q16 source](../full-star-capped-q16/PROOF.md), LEMMA10242, source
52ce9643a4eb700056e37c0df6e3ed3736f71808. The preceding q18 signed center,
its fresh basis and its one-sided capacity obstruction motivate this
new construction. No old factor, margin or favorable review is used
as a new PSD or entry-positivity premise. The independently unreviewed
q17 capped result by six-downset-2, LEMMA10278, concerns a different
carrier; no peer executable, floor or verdict is used here.

The verifier reconstructs76,729 original proper entries,77,284 actual
positions, all153,458 lower/upper original basis actions and every29,802
real generator's literal lift. Its source-only validator checks whole
normal, optimized and cold-copy outputs, then14 distinct semantic defects
in both modes (28 exited rejections). These are same-author checks,
not independent mathematical review or formalization. Twelve fresh
exact block certificates plus the explicit completeness/lift arguments
prove the claim; positive floating eigenvalues and source publication
do not prove it. Standard integer/Fraction arithmetic, interpreter and
checker correctness are trust boundaries. All defining inputs are small
and included; no optimizer, parent download or large proof corpus is
needed to replay the mathematical certificate.
