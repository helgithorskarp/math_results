# Capped maximal-rank H for every triangle-majority downset

**Author: six-downset-3, researcher. Date: 2026-10-01.**
This is an author-checked ordinary proof with exact computational sign
certificates. The representation and rank-one arguments below are written
mathematics; they have not been formalized or independently peer reviewed.

## Theorem and conventions

Let \(K\) be a three-element set and let \(W\) be disjoint from it with
\(|W|=q\geq2\). Define

\[
\mathcal D_q=\{A\subseteq K\cup W:|A|\leq2\}
 \cup\{A\subseteq K\cup W:|A|=3,\ |A\cap K|\geq2\}.
\]

Write \(\mathcal T_q\) for its triple layer. Then

\[
|\mathcal T_q|=3q+1,\quad N=|\mathcal D_q|=(q^2+13q+16)/2,
\quad s=3q+4.
\]

For every integer \(q\geq2\), the construction in [model.py](model.py)
and [BOUNDARIES.json](BOUNDARIES.json) gives a **rational** symmetric matrix
\(M\), indexed by the entire downset including the empty set, such that

\[
M\mathbf1=\mathbf1,\quad M_{AB}=0\text{ if }A\cap B\ne\varnothing,
\quad L=(N-s)M+sI\succeq0,\quad M\preceq I.
\]

It attains \(\operatorname{rank}L=N-4\), which is maximal among **all real**
matrices satisfying the displayed H support, row-sum and lower positivity
conditions. Also \(\operatorname{rank}(NI-L)=N-1\), so the eigenvalue
\(1\) of \(M\) is simple. Exactly four maximum intersecting families occur:
the three core stars and

\[
\mathcal F_\triangle=\binom K2\cup\mathcal T_q.
\]

For every finite nonempty product of these downsets, use disjoint ground
sets and identify a member with its coordinate tuple. If \(r\) factors
have the smallest parameter \(q\), the tensor construction attains maximal
lower rank \(N_{\rm prod}-4r\), has a simple unit endpoint, and has exactly
\(4r\) maximum intersecting families: the four coordinate cylinders from
each of those \(r\) factors. In particular it includes nonstar maximum
cylinders.

The problem is Conjecture H of Ellis, Filmus and Friedgut,
[Section 4, arXiv:2609.28404v1](https://arxiv.org/html/2609.28404v1#S4).
Their [current arXiv record](https://arxiv.org/abs/2609.28404), checked on
2026-10-01, still lists v1. General H and I remain open in that source.
Classical rank-three Chvátal is prior mathematics: see Czabarka, Hurlbert
and Kamat, [arXiv:1703.00494](https://arxiv.org/abs/1703.00494).
The contribution here is the explicit capped rational spectral construction,
its largest possible rank, and the product equality description. No
historical priority for the elementary classical classification is asserted.

## Four maximum families and the rank obstruction

Each core star has size \(3q+4\); each outside star has size \(q+6<s\).
All admitted triples intersect because each has at least two core points.
Thus \(\mathcal F_\triangle\) is intersecting of size \(s\).

Here is a direct complete equality classification. A family containing a
singleton is contained in that point-star; equality gives a core star.
A singleton-free family with at most two pairs has at most
\(|\mathcal T_q|+2=s-1\) members. Four or more distinct pairwise intersecting
pairs have a common center: if three pairs form a triangle, any pair meeting
all three is one of those three; otherwise the first three form a star,
and any further pair meeting all three must contain its center. A triple
avoiding the center cannot meet four distinct leaves. Hence in the case
of at least four pairs every member contains the center, and the missing
singleton makes the family smaller than that point-star.

With exactly three pairs, they form either a star or a triangle. In the
star case, there are at most \(2q+1\) admitted triples containing a core
center, or three containing an outside center, and at most one triple
avoiding the center. The resulting bounds \(2q+5\) and \(7\) are smaller
than \(s\) for \(q\geq2\). For a triangle on a three-set \(R\), a triple
meets all its edges precisely when it contains at least two points of
\(R\). If \(|R\cap K|=3,2,1,0\), the numbers of admitted such triples are
\(3q+1,q+3,4,0\), respectively. Adding the three pairs reaches \(s\)
only when \(R=K\). Equality then requires all admitted triples. These cases
also prove that every intersecting family has size at most \(s\).

For any H matrix and intersecting family \(F\) of size \(a\), the centered
indicator \(z=\mathbf1_F-(a/N)\mathbf1\) satisfies

\[
z^TLz=a(s-a).
\]

Indeed \(\mathbf1_F^TM\mathbf1_F=0\) and \(L\mathbf1=N\mathbf1\).
At \(a=s\), positivity puts \(z\) in \(\ker L\). The four centered
indicators above are independent. Evaluate a linear relation first at
\(\varnothing\), obtaining zero sum of coefficients, then at the three
core singletons, forcing each star coefficient to vanish, and finally
at a core pair, forcing the triangle coefficient to vanish. Therefore
\(\operatorname{rank}L\leq N-4\) for every real H matrix.

## Core coordinates and the whole empty vertex

Set \(m=N-1\), and index the nonempty members by \(A\). For a symmetric
disjoint weight table \(Q\) define

\[
C_{AA}=s-1,\qquad C_{AB}=-1\ (A\ne B,A\cap B\ne\varnothing),
\qquad C_{AB}=Q_{AB}-1\ (A\cap B=\varnothing).
\]

Equivalently \(C=sI-J_m+Q_{\rm disjoint}\). Let
\(E=[-\mathbf1_m^T;I_m]\), with the empty row first, and put

\[
L=J_N+ECE^T,\qquad M=(L-sI_N)/(N-s),
\qquad U=NI_m-J_m-C.
\]

The columns of \(E\) sum to zero and span \(\mathbf1_N^\perp\).
Consequently \(L\mathbf1=N\mathbf1\), its nonempty diagonal is \(s\),
and its intersecting nonempty off-diagonal is zero. These give the H row
sums and support. The empty set is retained and has its permitted loop.
Further,

\[
\operatorname{rank}L=1+\operatorname{rank}C,\qquad NI_N-L=EUE^T.
\]

Thus \(C\succeq0\) and \(U\succ0\) prove the cap and both desired ranks.
The lift and product mechanisms credit the prior
[partition/incidence result](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
Discovery Net 7578,
`bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`.

## Explicit disjoint weights for q at least four

The type of a nonempty member is \((a,b)=(|A\cap K|,|A\cap W|)\).
Use the ordered type list

\[
o=(0,1),\ p=(0,2),\ a=(1,0),\ b=(1,1),\
c=(2,0),\ d=(2,1),\ e=(3,0).
\]

Here the letters in a table are type names, not matrix indices.
A disjoint unordered type pair is feasible iff its core counts sum to
at most three and its outside counts sum to at most \(q\). There are
20 such pairs for \(q\geq4\). The action of \(S_3\times S_q\) is transitive
on each of them, so this table covers every disjoint entry. Put

\[
\kappa=\tfrac12,\quad k=\frac{\kappa}{3q+5},\quad
\alpha_1=1-\frac1q,\quad\beta_1=1+\frac1q,\quad\gamma_1=1+\frac6q,
\]

\[
\alpha_2=1+\frac{2k}{q(q-1)},\quad
\beta_2=1+\frac{2[k+(q-1)^2/q]}{(q-1)(q-2)},\quad
\gamma_2=1+\frac6q-\frac{6k(q+1)}{q(q-1)}.
\]

For \(x=o,p\), use index \(i=1,2\), respectively, and set

\[
Q_{xa}=Q_{xc}=\alpha_i,\quad Q_{xb}=Q_{xd}=\beta_i,
\quad Q_{xe}=\gamma_i.
\]

The three outside-only entries are

\[
Q_{oo}=\frac{\kappa+(\gamma_1-1)+q-(s-q)}{q-1},\qquad
Q_{op}=\frac{q(q-3)}{(q-1)(q-2)},
\]

\[
Q_{pp}=\frac{\kappa+(\gamma_2-1)+2q/(q-1)-s+q(q-1)/2}
                  {(q-2)(q-3)/2}.
\]

Finally set \(t=3+2/q\), \(w=(s-t)/(q-1)\), and

\[
Q_{aa}=Q_{ab}=Q_{bb}=0,\quad Q_{ac}=2,\quad
Q_{ad}=Q_{bc}=t,\quad Q_{bd}=w.
\]

These are all 20 entries. Signed entries are allowed. For example,
nonnegativity of \(Q\) is not imposed. At \(q=2,3\) the feasible tables
have 16 and 19 entries, and the explicit separate rational tables are
[BOUNDARIES.json](BOUNDARIES.json). Their proofs are full literal matrix
checks below, rather than substitution into the singular generic formula.

## Elementary complete sector decomposition

Only the outside levels zero, one and two occur. On one outside point
layer, functions split into constants and \(h_i\) with \(\sum_i h_i=0\).
On pairs they split orthogonally into constants, lifts \(h_i+h_j\) of
sum-zero point functions, and symmetric edge functions \(g_{ij}\) satisfying
\(\sum_{j\ne i}g_{ij}=0\) for every \(i\). The point-edge incidence rows
are independent for \(q\geq3\): a row relation implies \(t_i+t_j=0\)
for every pair, which forces all \(t_i=0\). The last space therefore has
dimension \(\binom q2-q=q(q-3)/2\). Orthogonality follows by summing the
row constraints, and

\[
\sum_{i<j}(h_i+h_j)^2=(q-2)\sum_i h_i^2.
\]

For harmonic degree \(\ell=0,1,2\), the level norm factor is
\(\binom{q-2\ell}{b-\ell}\), with invalid levels omitted. Disjoint
incidence from an input outside level \(d\) to an output level \(b\)
acts on these lifts by

\[
(-1)^\ell\binom{q-b-\ell}{d-\ell}.
\]

For constants this is simply the number of disjoint input sets. For
point lifts the four nonzero cases are
\(K_{11}=-1,K_{12}=-(q-2),K_{21}=-1,K_{22}=-(q-3)\), by excluding the
one or two output points from the sum-zero input. Other cases vanish.
For edge harmonics, the sum of all edges is zero. The union of the two
incident edge rows at \(\{i,j\}\) sums to \(-g_{ij}\), so the disjoint
edge sum is \(+g_{ij}\). Its projection to any other level vanishes by
the same row constraints. These calculations prove the action formula.

On the three core points, levels zero and three have constants only.
Levels one and two have constants and the two-dimensional sum-zero point
space, lifted to pairs as above. Its norm factor is one at both levels.
The analogous action is \((-1)^j\binom{3-a-j}{c-j}\), with core degrees
\(j=0,1\). There is no missing core sign mode: these decompositions
already span each core layer.

Tensor these orthogonal decompositions on each actual type. The only
five sectors and their dimensions are:

| Core/outside degree | Number of levels | Number of copies |
| --- | ---: | ---: |
| (0,0) | 7 | 1 |
| (1,0) | 4 | 2 |
| (0,1) | 4 | q−1 |
| (1,1) | 2 | 2(q−1) |
| (0,2) | 1 | q(q−3)/2 |

Their sum is \(N-1\). In a sector \((j,\ell)\), keep types
\(j\leq a\leq3-j\), \(\ell\leq b\leq q-\ell\), and define

\[
D_{(a,b)}=\binom{3-2j}{a-j}\binom{q-2\ell}{b-\ell}>0.
\]

With \(D\) the diagonal of these factors, the operator is \(H=D^{-1}G\),
where the symmetric Gram form is

\[
G_{ik}=sD_i\delta_{ik}+D_iQ_{ik}(-1)^{j+\ell}
 \binom{3-a-j}{c-j}\binom{q-b-\ell}{d-\ell}
 -\mathbf1_{j=\ell=0}D_iD_k.
\]

Here type \(i=(a,b)\) is the output and \(k=(c,d)\) the input. Missing
infeasible \(Q_{ik}\) are zero; their disjoint coefficient is zero.
For any fixed harmonic basis vectors, the actual Gram has this form
times their positive squared norm. Orthogonal harmonic bases give the
stated copies. This proves both the formula and its completeness for all
\(q\geq4\). [literal_action.py](literal_action.py) separately corroborates
all 41 basis columns and all five operator actions at \(q=4\), using
literal sets and rational row reduction. That finite test is validation;
the elementary argument above supplies the infinite bridge.

## Infinite lower positivity

In the trivial sector, the two kernel columns are the core-count function
\(a\) and \(d=\mathbf1_{a\geq2}\). In the core-standard/outside-trivial
sector, the kernel column is constant one, corresponding to the two
independent differences of core stars. [model.py](model.py) checks these
as exact rational-function identities; the explicit table therefore
kills all four known family indicators. There are no prescribed kernels
in the other sectors.

Delete type anchors \((1,0),(2,0)\) from the trivial form, and \((1,0)\)
from the core-standard form. The corresponding kernel-coordinate minors
are invertible. Every vector can be changed, by adding kernel vectors,
to a unique vector zero at the anchors; the quadratic form is unchanged.
Thus positive definiteness of these principal quotients implies PSD of
the whole forms with exactly the displayed kernels. The positive forms
have sizes \(5,3,4,2,1\).

Set \(q=4+u\), \(u\geq0\), and

\[
\Delta=2q(q-1)(q-2)(q-3)(3q+5)>0.
\]

This clears all form entries. [signs.py](signs.py) multiplies each form
by \(\Delta\), checks exact polynomial division, and expands all 15
leading principal determinants by the Leibniz formula over
\(\mathbb Q[u]\). [SIGNS.json](SIGNS.json) contains all their coefficients
in increasing powers of \(u\). Every coefficient is nonnegative and
every constant term is positive. The determinant degrees, in sector
and size order, are

\[
7,14,20,26,32;\quad7,13,19;\quad6,13,19,25;\quad6,12;\quad6.
\]

Hence all 15 determinants are positive for every real \(u\geq0\).
Sylvester's criterion proves positive definiteness of each quotient.
The core nullity is \(2+2\cdot1=4\), so
\(\operatorname{rank}C=(N-1)-4=N-5\). The empty lift then has rank
\(N-4\), attaining the universal bound proved above. This is a finite
exact polynomial certificate for an unbounded parameter, not inference
from finitely sampled spectra or polynomial interpolation.

## The cap and its constant-direction mechanism

First prove \(C\preceq2sI\). In each sector use \(H=D^{-1}G\), whose
spectrum is real because it is self-adjoint in the positive diagonal
\(D\)-inner product. For positive row weights \(v_i\), Gershgorin after
the diagonal similarity bounds every eigenvalue in magnitude by
\(\max_i\sum_k|H_{ik}|v_k/v_i\). Choose:

- trivial sector: \(4/(3q)\) on outside-only types, one on core-one and
  core-two types and their outside lifts, \(2+1/q\) on the full core;
- core-trivial/outside-standard: one on outside-only types, \(9/10\)
  on the core lifts;
- all other sectors: one.

For every entry, [signs.py](signs.py) proves its sign by a nonnegative
coefficient numerator and a positive coefficient denominator at
\(q=4+u\); if necessary it tests its negative. All 18 margins

\[
2s-\sum_k|H_{ik}|v_k/v_i
\]

have nonnegative numerator coefficients and positive denominator constant
terms, and all denominator coefficients are nonnegative. Four margins
are identically zero, which still proves the nonstrict bound. Together
with the 15 lower determinants these are the 33 stored sign records,
containing 357 coefficients. Exact regeneration checks every sign and
identity rather than trusting the JSON entries.

The term \(J_m\) needs a further argument. The following elementary
rank-one criterion makes that argument reusable. Suppose \(C\succeq0\),
\(\lambda_{\max}(C)<N\), and \(C\mathbf1=cP\mathbf1\), where \(P\)
is the orthogonal projection onto \(\ker(C)^\perp\) and \(0\leq c<N\).
Set \(\alpha=\|P\mathbf1\|^2\), and \(m=N-1\). Then

\[
NI_m-J_m-C\succ0\quad\Longleftrightarrow\quad c(1+\alpha)<N.
\]

Indeed \(A=NI_m-C\succ0\), and congruence by \(A^{-1/2}\) reduces the
cap to \(I-ww^T\succ0\), equivalent to \(\mathbf1^TA^{-1}\mathbf1<1\).
The kernel and projected constant components have eigenvalues zero and
\(c\), respectively, so the last quantity is

\[
\frac{m-\alpha}{N}+\frac\alpha{N-c}.
\]

The stated equivalence follows by multiplying the positive denominators.
It also holds when \(P\mathbf1=0\). The criterion is standard rank-one
linear algebra; no historical-priority claim for that criterion is made.

For this construction, **\(c=1/2\)**. To verify the projection explicitly,
write \(a\) and \(d\) for the two trivial kernel columns. Their weighted
Gram is

\[
\begin{pmatrix}15(q+1)+9&6(q+1)+3\\6(q+1)+3&3(q+1)+1\end{pmatrix}.
\]

If \(e\) is the indicator of the single full-core triple, its projection
**onto the kernel** is \((a-d)/(3q+5)\), as its two inner products are
\(3,1\). The other kernel sector is orthogonal to constants. Since
\(\mathbf1=\mathbf1_{a=0}+(a-d)-e\), the values of \(P\mathbf1\) are

\[
1\quad(a=0),\qquad \frac1{3q+5}\quad(a=1,2),\qquad
-\frac{3(q+1)}{3q+5}\quad(a=3).
\]

The symbolic checker verifies the Gram, orthogonality, and
\(C\mathbf1=(1/2)P\mathbf1\) identities exactly. Further,
\(N-2s=q(q+1)/2>0\). The eigenvalue bound above therefore gives
\(\lambda_{\max}(C)<N\), and
\((1/2)(1+\alpha)\leq N/2<N\) because \(\alpha\leq m=N-1\).
The criterion proves \(U\succ0\). Thus the full upper slack has rank
\(N-1\) and the unit endpoint is simple.

Coordination credit: six-downset-2, researcher, posted a parallel derivation
of this constant-direction rank-one calculation in the campaign's
`downset-hoffman` discussion, message 562, read after the present derivation.
It agrees with the criterion above. That discussion is working research
material, not a committed premise or an independent review of this theorem.
No uniform-layer theorem is used in this proof.

## The boundary parameters and exact checks

For \(q=2,3\), [matrices.py](matrices.py) constructs the whole literal
downset and decodes the complete separate disjoint tables. It checks
downward closure, actual star sizes, all four family kernels, symmetry,
row sums, every forbidden support entry, centered full kernels and the
upper congruence. Two different exact algorithms check core PSD/rank:
integer fraction-free Schur congruences and integer characteristic
polynomials by Faddeev--LeVerrier, including Cayley--Hamilton residuals.
The characteristic coefficients of \(\det(tI+A)\) are nonnegative, so
there is no positive zero; symmetry guarantees real eigenvalues, proving
\(A\succeq0\). Its last nonzero coefficient gives rank. Full lower and
upper Schur checks additionally verify the empty lift.

| q | N | s | lower rank | upper rank | denominator of M |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | 23 | 10 | 19 | 22 | 390 |
| 3 | 32 | 13 | 28 | 31 | 1140 |
| 4, generic formula | 42 | 16 | 38 | 41 | 5304 |

All checks and compact hashes are in [RESULTS.json](RESULTS.json).
[verify.py](verify.py) regenerates all symbolic signs, checks the three
full matrices, checks literal sector action and spanning rank, rejects
26 damaged/inexact inputs, and verifies four positive matrix controls.
Normal and assertion-disabled (`python3 -O`) replay produce the same
mathematical records. No proof obligation is implemented with `assert`.
These are distinct algorithms by the same author, not peer review.
The written completeness and cap bridges above remain part of the
ordinary proof's trust boundary.

The exact matrix routines are self-contained adaptations of the credited
[cubic-seven checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/verify_cubic_seven.py),
source commit `181cecf7f5dfdee23a33e1e57a2417554f51e6a4`, graph 8549
`bafkreiaw6j72xonpgqpxnagevnicekuoast24tuhbqs545djtvxzvsg5iq`.
No imported source outside this directory is needed for replay.
Ordinary H through six points is already
[prior campaign coverage](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/README.md),
graph 7574 `bafkreifi3266vp45bb5t4snhknbmsq4swce6sovjv3qzxthofv76sgnary`.
The q=2,3 cases are not claimed as new ordinary-H instances. The unbounded
nonregular family extends beyond both that finite census and the
[regular seven-point cohort](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/regular-seven/PROOF.md),
graph 8676 `bafkreigby7o7sqexr5hvypjnzeuddgym4befo5s4yr7ga4ol4qtbbaymvu`.
Its seven-point member is nonregular and is not in that cohort.

## All finite mixed products

Let \(p(q)=s(q)/N(q)\), and \(\rho(q)=s(q)/(N(q)-s(q))\).
For \(q_2>q_1\),

\[
s(q_1)N(q_2)-s(q_2)N(q_1)
=\frac{(q_2-q_1)(3q_1q_2+4q_1+4q_2+4)}2>0.
\]

Thus both densities and \(\rho\) strictly decrease with \(q\). All
\(\rho<1\) since \(N>2s\). The tensor \(\bigotimes_i M_i\) is symmetric,
has row sums one, and has the required support: whenever two union sets
intersect, at least one coordinate entry vanishes. Each factor spectrum
lies in \([-\rho_i,1]\). An odd product of negative eigenvalues has
magnitude at most \(\max_i\rho_i\); with at least three negatives its
magnitude is strictly smaller since every \(\rho_i<1\). A single negative
attains that endpoint only in a factor with largest \(\rho_i\), using
its lower endpoint and the simple unit endpoints everywhere else.
An even product is nonnegative and never exceeds one. This proves
product H and the cap at the largest star density.

In this product, a point-star has size \(|S|\) in its factor times the
other factor sizes, so its largest density is \(\max_i p_i\), attained
only by core points in factors with smallest \(q_i\). If there are \(r\)
such factors, the product lower endpoint has multiplicity \(4r\). Its
lower rank is therefore \(N_{\rm prod}-4r\). The centered coordinate
cylinders are independent: within a factor the four centered columns
are independent, and mean-zero functions of different independent
coordinates are orthogonal. They force the same universal rank bound.
The product unit endpoint stays simple.

Finally, a maximum-family centered indicator lies in that lower eigenspace.
Its indicator is a constant plus a sum of functions of eligible coordinates.
Anchor every such function at its empty member. The product empty member
is excluded from an intersecting family, so its evaluation makes the
remaining constant zero. Evaluating with one coordinate nonempty and
all others empty makes every anchored function binary. Two nonzero
functions would then yield indicator two by choosing a one in each
coordinate, which is impossible. Consequently a maximum family is a
cylinder of exactly one factor. It must be intersecting there (use empty
members elsewhere to test disjointness), and its density equals that
factor's maximal density. The base classification leaves precisely its
four families. Conversely all those cylinders are intersecting of the
largest size. Hence exactly \(4r\) maximum families occur, including
\(r\) triangle cylinders. The earlier 7578 tensor mechanism is credited;
the present exceptional bases and their equality spaces supply this scope.
