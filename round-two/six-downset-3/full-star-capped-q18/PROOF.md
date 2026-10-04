# A capped Hoffman certificate on the q18/k9 downset

Actual author: **six-downset-3, researcher**, 2026-10-04. This is an
ordinary proof with exact finite certificates. The checker is separate
from the numerical producer but is written by the same author. This new
carrier is independently **UNREVIEWED**, and the ordinary completeness,
real perturbation and congruence arguments are **UNFORMALIZED**.

Let `a,b,c` be distinct, and let `Z,W` be disjoint nine-element sets
disjoint from them. On their 21-element union define

\[
 D=\{A:|A|\leq2\}\cup
   \{A:|A|=3,\ |A\cap\{a,b,c\}|\geq2\}
   \setminus\{\{b,c,z\}:z\in Z\}.
\]

The deletion applies to the union. All triples' subsets remain, so this
is a downset. It has `N=1+21+210+46=278` members. The point-stars have
sizes `58,49,49`, nine of size23 and nine of size24. Thus the maximum
star is uniquely `S_a`, with `s=58`. Relabeling covers every such choice
of the three core points and two pools.

**Theorem.** The rational matrix defined below satisfies Conjecture H on
this downset, retaining its actual empty vertex and loop, and also
satisfies the additional cap `M <= I`. Both `L=220M+58I` and `278I-L`
have rank277. The minimum and unit eigenvalues of `M` are simple. At the
center its other276 eigenvalues belong to

\[
 [-29/110+1/7040,\ 1-1/7040].
\]

These properties persist on a **29,802-dimensional closed real box**
of independent repairs, with each coefficient bounded in absolute value
by `1/3814656`. On that box the two nonzero endpoint floors are at least
`1/64` and the other276 eigenvalue gaps are at least `1/14080`.
No entrywise nonnegativity, other carrier, full family classification or
general H/I conclusion is asserted.

## Explicit matrix and empty completion

Use bits0,1,2 for `a,b,c`, bits3..11 for `Z`, and bits12..20 for `W`.
Index the proper members by increasing masks. Put
`o(A)=(A&7, |A intersect Z|, |A intersect W|)`.
The certificate includes all143 unordered orbit keys for disjoint,
nonanchor proper pairs and their integer numerators over **16384**.
These are new coefficients: the q16 numerators are multiplied by15
and their original denominator by16. This was a proposal mechanism;
none of the parent matrix's PSD facts, factors, dimensions or margins
are transported. The final coefficients and new factors are wholly
included in this packet; checking requires no parent download or code.

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
over `D=16384`, and form exactly

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

## Full real box, ranks and spectral gaps

There are30,021 disjoint unordered proper pairs and219 nonstar anchor
equations. A complete independent repair basis consists of a symmetric
unit edge for every disjoint nonstar pair, and, for each disjoint
nonstar `A` and star `B!={a}`, the anchored trade
`R=edge_(A,B)-edge_(A,{a})`.
Every such repair fixes the support and diagonal and annihilates `h`.
Conversely every support-preserving repair annihilating `h` is determined
by its nonanchor entries; the anchor equations recover all remaining
entries. This proves the full independent dimension **29802**.

Every unit edge has operator norm1; every anchored trade has norm
`sqrt(2)<=2`. For arbitrary independent real coefficients satisfying
`|t_j|<=1/(128*29802)=1/3814656`, their sum has norm at most1/64.
Hence the displaced `C` has exact kernel `span(h)` and floor1/64 on
its perpendicular, and its `U` is positive definite with floor1/64.
This proves a whole real box, without enumerating corners or samples.

Since `E` is injective and `J` has orthogonal range, the center and box
have `rank L=277`. The upper core is positive definite, so its lift has
rank277 and kernel exactly `span(1)`. The lower kernel is exactly the
centered maximum star. Thus `M` has simple minimum `-58/220=-29/110`
and simple unit eigenvalue. Because `E^TE=I+J>=I`, the nonzero eigenvalues
of both lifted endpoints are at least the respective proper floor.
Dividing by220 gives point gaps1/7040 and box gaps1/14080.

## A precise entry-capacity obstruction at this new seed

Every negative admissible entry is in the actual empty row. The complete
negative row census is:

| Proper member orbit `(core,Z,W)` | Members | `M[empty,A]` |
|---|---:|---:|
| `(0,0,2)` |36|`-36259/3604480`|
| `(0,2,0)` |36|`-32877/3604480`|
| `(6,0,1)` |9|`-999/3604480`|
| `(7,0,0)` |1|`-20819/3604480`|

There are164 negative ordered positions, including their transposes.
The minimum is `-36259/3604480`. The actual empty loop is positive,
`126347/225280=2021552/3604480`. These signed entries are permitted by H.

**Restricted obstruction.** No real symmetric proper repair `R`, with
zero diagonal, zero intersecting entries, and `Rh=0`,
of this seed whose nonstar/nonstar proper entries all weakly decrease
can make every admissible `M` entry nonnegative, even allowing arbitrary
anchored star trades. This is not an unrestricted positivity or H
nonexistence statement.

Indeed, anchored star trades leave every nonstar proper row sum and the
total proper row sum unchanged. Nonpositive nonstar/nonstar changes
weakly decrease all nonstar row sums. Correcting the81 negative nonstar
empty entries requires their total row-sum decrease to be at least
`2497887/16384`. The remaining nonstar row sums cannot increase.
The total proper row-sum change therefore is at most `-2497887/16384`.
The empty-loop numerator in units of `M` is the old one plus that
total change divided by220, and is at most

\[
 (2021552-2497887)/3604480=-476335/3604480<0.
\]

This contradicts entrywise nonnegativity. The star-member orbit
`(7,0,0)` is deliberately excluded from the81-member deficit; its
correction does not improve this loop budget. Thus a positive-entry
construction from this center requires increases on some nonstar
pairs. The checker certifies the entire original deficit census; the
arbitrary-real repair implication is the ordinary argument just given.

## Attribution, literature and remaining scope

The named problem is [Ellis--Filmus--Friedgut, Section4, Conjecture H](https://arxiv.org/html/2609.28404v1#S4).
The [primary history](https://arxiv.org/abs/2609.28404) was live checked
on2026-10-04: only v1 from23 September2026 was listed; H and I remain
conjectural. The announced classical/projection proof is literature,
not an H matrix for this new carrier.

The carrier family comes from the earlier D3
[core-edge-six source](../core-edge-six-cutoff/PROOF.md).
The proposal coefficients and complete original basis mechanism come
from the public D3 [q16 seed](../full-star-capped-q16/PROOF.md), source
`52ce9643a4eb700056e37c0df6e3ed3736f71808`, LEMMA10242.
The earlier [q16 audit](../../six-reviewer-5/full-star-q16-audit/REVIEW.md),
REVIEW10252, covers that original carrier only. Neither its certificate
nor its favorable verdict is used as a q18 positivity premise.
The new q17 scaling suggestion received from researcher six-downset-2,
message3671, motivated this finite q18 scaling grid; its private proof,
matrix, floor and carrier are distinct and not inputs here.
The separate [proper-envelope review](../../six-reviewer-5/proper-envelope-audit/REVIEW.md),
REVIEW10268, concerns the preceding norm theorem and conditional q16
box; its verdict does not review this q18 seed.

The checker is adapted from the earlier public same-author implementation,
with a separate fresh core/outside census, nine-point pool bases, new
weighted residual factors and both full original actions. This is an
open author proof, not independent review or formalization. A failed
literal unscaled q18 transfer preceded this new15/16 construction; it
rejects only that earlier candidate. The standard linear algebra,
interpreter and checker correctness remain trust boundaries. Historical
priority for those methods and general spectral conjecture resolution
are not claimed.
