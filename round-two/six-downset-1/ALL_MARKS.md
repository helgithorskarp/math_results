# Capped maximal-rank H for a Boolean cube with any number of distinct marked pendants

Actual author: **six-downset-1**, role **researcher**, round two,
2026-10-01. Status: complete author-checked ordinary proof with exact
rational replay, unformalized and independently unreviewed. This is a
structured class of spectral Chvatal H; general H and I remain open.

## 1. Quantified statement and credited ingredients

Let X have n>=2 coordinates, let x_1,...,x_r be distinct members of X,
where 2<=r<=n, and let a_1,...,a_r be distinct fresh coordinates. Put

\[
 D=2^X\cup\bigcup_{i=1}^r\{\{a_i\},\{a_i,x_i\}\},\qquad
 q=2^{n-1},\quad N=2q+2r,\quad s=q+1.
\]

There is an explicit rational symmetric matrix M on **all** N members,
including the empty set, such that

\[
 M\mathbf1=\mathbf1,\qquad
 M_{AB}=0\quad(A\cap B\ne\varnothing),\qquad
 L=(N-s)M+sI\succeq0,\qquad M\preceq I.
\]

The construction has

\[
 \operatorname{rank}L=N-r,\qquad
 \operatorname{rank}(I-M)=N-1,
\]

and every nonunit eigenvalue lies in

\[
 \left[-\frac{q+1}{q+2r-1},\;
 1-\frac1{2(q+2r-1)}\right].                                      \tag{1}
\]

The negative endpoint has multiplicity exactly r; the unit eigenvalue
is simple. The lower rank N-r is greatest among **all real H matrices**
on D, even without a cap. The only maximum intersecting families are
the r marked stars. Section8 gives the credited strict-product corollary.

The conventions are those in
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4):
the empty vertex has an allowed loop and signed matrix entries are
permitted. The current primary
[arXiv record](https://arxiv.org/abs/2609.28404) was rechecked on
2026-10-01; it still lists v1 of2026-09-23 and does not settle H or I.

The core lift and conditional tensor transport are credited to
[the structural proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
graph7578. The complementary cube spectrum/forced-span ingredients
are credited to8020 and its full-cube review8066. The cap-preserving
rational rank repair was already used in our
[two-facet proof](UNEQUAL_FACETS.md), graph8579, and our
[two-distinct-mark proof](TWO_MARKED_CUBE.md), graph8788.
The latter used a different core and covered n>=3,r=2. The present
orthogonal-star core and complete r-sector estimates extend the scope
to every 2<=r<=n, with n=2 handled explicitly. Ordinary small rank-two
H and that small boundary are prior existence results, not first claims
here. The new result is the all-order rational cap/rank construction.

[Balanced single-pendant completion](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/BALANCED_PENDANT_COMPLETION.md),
graph8424, covers a pendant at a maximum-star coordinate and repeated
pendants at that same coordinate. After one attachment, a different
unmarked old coordinate has star q, smaller than q+1, so that theorem
does not iterate to this family. Our
[arbitrary-petal sunflower](ALL_PETALS.md), graph8700, has independent
[review8779](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/arbitrary-petal-audit/REVIEW.md).
The distinct singleton intersections here do not form a common-core
sunflower; that review supplies no verdict on the present extension.

## 2. Maximum families, forced rank, and the core lift

The marked old stars have size q+1. Other old stars have size q and
fresh-coordinate stars have size2. A family containing a fresh
singleton has size at most2. The r spokes {a_i,x_i} are pairwise
disjoint, so an intersecting family contains at most one. With no
spoke its size is at most q: each old complementary pair contains
at most one member. With spoke i every old member contains x_i,
so equality q+1 forces the full marked star. Since s>=3, these are
exactly the maximum intersecting families.

For any real H matrix and an intersecting s-member family F, its
indicator f satisfies f^TMf=0, including diagonal terms. Its centered
indicator v=f-(s/N)1 has

\[
 v^T L v=0,\qquad L\mathbf1=N\mathbf1.
\]

Thus Lv=0 and Lf=s1. In our family the r centered star indicators
are independent: their empty-coordinate equation first makes the
sum of their coefficients zero; each unique spoke coordinate then
makes its corresponding coefficient zero. Hence rank L<=N-r for
every H matrix. This argument also identifies the required kernels.

For an (N-1)-point nonempty core C with diagonal s-1=q and entry -1
whenever its two nonempty sets intersect, define

\[
 T_0=\begin{pmatrix}-\mathbf1^T\\I\end{pmatrix},\quad
 Q=T_0 C T_0^T,\quad J=\mathbf1\mathbf1^T,\quad
 P_N=I-J/N,\quad
 M=\frac{Q+J-sI}{N-s}.                                           \tag{2}
\]

Then Q1=0, M1=1, the intersection support condition holds, and

\[
 L=Q+J,\quad\operatorname{rank}L=1+\operatorname{rank}C,
 \quad(N-s)(I-M)=NP_N-Q.                                         \tag{3}
\]

A PSD core makes the lower slack PSD. The cap must be checked for
the **full Q**, rather than inferred from the norm of C. In Gram
language, if C has vectors g_A, the empty vector is
g_empty=-sum_{A nonempty}g_A. The nonzero spectra of full Q and
its frame sum_{A in D}g_Ag_A^* agree. This explicitly includes the
empty-vector energy.

## 3. An old cube core with orthogonal marked stars

Index old nonempty cube members. Let P be restricted complementation:
it exchanges the q-1 proper complementary pairs, and its full-set
row/column is zero. Take

\[
 C_0=(q-1)P+(q+1)I-J.                                             \tag{4}
\]

Its diagonal is q and its intersecting off-diagonal entries are -1.
On the pair-antisymmetric space it is2 (dimension q-1); on the
pair-symmetric zero-sum space it is2q (dimension q-2). In the remaining
orthonormal plane (normalized proper-pair sum, full set), it is

\[
 \begin{pmatrix}2&-\sqrt{2q-2}\\-\sqrt{2q-2}&q\end{pmatrix}.
\]

The trace is q+2 and determinant2. Therefore C_0 is positive definite
of rank2q-1 for every q>=2. Choose Gram vectors g_A for it, and write

\[
 G=\sum_{\varnothing\ne A\subseteq X}g_A,\quad F=g_X,\quad
 H_i=-\sum_{A\ni x_i}g_A.
\]

Counting star intersections and complementary pairs gives

\[
 \|G\|^2=\|F\|^2=\|H_i\|^2=q,\quad
 G\cdot F=2-q,\quad G\cdot H_i=F\cdot H_i=-1,\quad
 H_i\cdot H_j=0\ (i\ne j).                                      \tag{5}
\]

Also H_i dot g_A=-1 if x_i belongs to A, and +1 for a proper
nonempty A excluding x_i. Thus setting the spoke vector to H_i
meets every spoke/old intersection constraint.

Let

\[
 h_0=-(G+F)/2,\quad G_\perp=G+h_0,\quad A_i=H_i-h_0,
 \quad Z=\frac1r\sum_i A_i,\quad
 \delta_i=H_i-\overline H=A_i-Z.
\]

Then h_0 has norm1; G_perp, h_0, and every A_i are orthogonal
except among the A_i themselves. Their relevant Gram data are

\[
 \|G_\perp\|^2=q-1,\quad
 (A_i\cdot A_j)_{ij}=qI_r-J_r,\quad
 \|Z\|^2=z=(q-r)/r,\quad
 (\delta_i\cdot\delta_j)_{ij}=q(I_r-J_r/r).                       \tag{6}
\]

For n>=3, q>=r+1, since 2^{n-1}>=n+1. The A_i span r independent
old antisymmetric directions; the delta_i span r-1 directions and
are orthogonal to Z. The remaining n=2,r=2,q=2 boundary has Z=0
and is handled in Section5.

Let F_0=sum_{old nonempty A}g_Ag_A^*. The vectors A_i lie in the
old eigenvalue2 space, and direct row sums give

\[
 F_0h_0=G_\perp+h_0,\quad
 F_0G_\perp=(q+1)G_\perp+(q-1)h_0,\quad F_0Z=2Z.                 \tag{7}
\]

In the normalized basis G_perp/sqrt(q-1), h_0, Z/sqrt(z), its
three-direction compression is

\[
 \begin{pmatrix}q+1&\sqrt{q-1}&0\\\sqrt{q-1}&1&0\\0&0&2\end{pmatrix}.
\]

## 4. Explicit rational Gram seed, including the empty vector

Put R=r+1 and

\[
 K=G+\sum_i H_i=G_\perp+(r-1)h_0+rZ,\quad
 b=\frac{r(q-r-2)}{(r+1)q(r-1)},
\]
\[
 \eta=\frac{rq}{r+1}+\frac{2r}{(r+1)^2}
       -b^2\frac{q(r-1)}r
 =\frac{r[(r^2-2)q^2+(4r+2)q-(r+2)^2]}
 {(r+1)^2q(r-1)}.                                                \tag{8}
\]

For q>=r+1, the bracket is at least
2q^2+10q-(q+1)^2=q^2+8q-1>0. In the exceptional q=r=2 case,
b=-2/3 and eta=4/3, also positive.

In a fresh orthogonal (r-1)-space take regular simplex vectors W_i
with squared norm eta, cross inner product -eta/(r-1), and sum zero.
Assign singleton vectors

\[
 U_i=-K/(r+1)+b\delta_i+W_i,                                    \tag{9}
\]

and retain H_i for spoke i. Formulae(5)--(8) give

\[
 \|K\|^2=(r+1)q-2r,\quad K\cdot H_i=q-1,\quad K\cdot\delta_i=0,
 \quad\|U_i\|^2=q,\quad U_i\cdot H_i=-1.
\]

There are no further singleton intersections to satisfy. The total
nonempty vector sum is K/(r+1), because sum delta_i=sum W_i=0.
Consequently the actual empty vector is

\[
 g_\varnothing=-K/(r+1).                                        \tag{10}
\]

The seed is generally **not centered on nonempty vertices**. Its
empty vector contributes KK^*/(r+1)^2. Including that contribution,
the complete frame is

\[
 F_Q=F_0+\sum_i H_iH_i^*+
       \frac{KK^*}{r+1}+
       \sum_i(b\delta_i+W_i)(b\delta_i+W_i)^*.                    \tag{11}
\]

All Gram entries are rational: (4), the old coefficient vectors,
and the explicit simplex Gram matrix define them without taking
square roots. Real Gram coordinates are only a proof device.
The old vectors already span2q-1 directions; the W_i add r-1.
Thus the seed core rank is2q+r-2, its lower rank is N-r-1,
and it has one excess lower-kernel direction. Section6 removes it.

## 5. Complete frame cap, uniform margin1, and the small boundary

Assume first n>=3, so q>=r+1. Formula(11) splits orthogonally into
the following complete sectors:

| Sector | Dimension | Frame action |
| --- | ---: | --- |
| G_perp,h_0,Z | 3 | F_sym below |
| marked differences paired with simplex | 2(r-1) | r-1 copies of F_anti |
| untouched old pair-symmetric space | q-2 | 2q |
| untouched old pair-antisymmetric space | q-r-1 | 2 |

The dimensions sum to2q+r-2, the full seed Gram span. The marked
differences and W_i have the same standard simplex Gram pattern,
so an isometry matches their normalized bases; this gives precisely
r-1 identical two-dimensional sectors. There are no omitted modes.

In the normalized symmetric basis from(7), set z=(q-r)/r. The frame is

\[
 F_{\rm sym}=\frac1R
 \begin{pmatrix}
 (r+2)q+r&2r\sqrt{q-1}&r\sqrt{(q-1)z}\\
 2r\sqrt{q-1}&2(r^2+1)&2r^2\sqrt z\\
 r\sqrt{(q-1)z}&2r^2\sqrt z&2R+(q-r)(2r+1)
 \end{pmatrix}.                                                  \tag{12}
\]

For A=(N-1)I-F_sym, the diagonal entries are

\[
 \frac{rq+2r^2-1}{R},\qquad
 2q+\frac{r-3}{R},\qquad\frac{q+4r^2-3}{R}.
\]

Its leading principal minors are

\[
 d_1=\frac{rq+2r^2-1}{R},
\]
\[
 d_2=\frac{2rR q^2+(4r^3+r^2-5r-2)q+2r^3-2r^2-r+3}{R^2},
\]
\[
 d_3=\frac{2(r-1)(2r+1)q^2+(12r^3-12r^2-7r+9)q
                 +8r^4-8r^3-12r^2+21r-9}{R}.                   \tag{13}
\]

All are positive. For clarity, substituting t=r-2>=0, the numerators
of d_2 and d_3 respectively become

\[
 (2t^2+10t+12)q^2+(4t^3+25t^2+47t+24)q
                         +2t^3+10t^2+15t+9,
\]
\[
 (4t^2+14t+10)q^2+(12t^3+60t^2+89t+43)q
                  +8t^4+56t^3+132t^2+133t+49.
\]

These are exact polynomial identities, not interpolated sample signs.
The checker independently reconstructs the determinant algebra over
integer two-variable polynomials. Sylvester's criterion proves A>0.

In each antisymmetric two-plane let e=r eta/(r-1). Its frame is

\[
 F_{\rm anti}=\begin{pmatrix}q+2&0\\0&0\end{pmatrix}+vv^*,
 \qquad v=(b\sqrt q,\sqrt e)^T.                                 \tag{14}
\]

For r>=3, q>=r+1 gives

\[
 |b|\le\frac r{r^2-1}\le\frac38,\qquad
 e\le\frac{r^2q}{r^2-1}
       +\frac{2r^2}{(r-1)(r+1)^2}
 \le\frac{9q}8+\frac9{16}.
\]

With D_0=diag(q+2r-2,N), the rank-one budget satisfies

\[
 \theta=v^*D_0^{-1}v
       =\frac{b^2q}{q+2r-2}+\frac eN
       <\frac9{64}+\frac9{16}=\frac{45}{64}.
\]

The second strict inequality uses
((9/8)q+9/16)/(2q+2r)<9/16. By Cauchy--Schwarz,
vv^*<=theta D_0; hence

\[
 NI-F_{\rm anti}\succeq(1-\theta)D_0
 \succ\frac{19}{64}D_0\succeq\frac{19}{8}I\succ I,
\]

because q+2r-2>=8. This is the required unit margin.

For r=2,q>=4, the first leading minor and determinant of
(N-1)I-F_anti are instead

\[
 \frac{5q^2+41q-64}{9q},\qquad
 \frac{2q^3+49q^2+19q-128}{9q}.                                  \tag{15}
\]

With u=q-4>=0 their numerators are5u^2+81u+180 and
2u^3+73u^2+507u+860, respectively, so they are positive. The
checker also reconstructs these identities formally. The untouched
sectors have NI-frame gaps2r and N-2, both greater than1.

For the only excluded boundary n=r=q=2, Z=0. The symmetric frame is

\[
 \begin{pmatrix}10/3&4/3\\4/3&10/3\end{pmatrix}.
\]

Here N=8 and (N-1)I minus this frame has eigenvalues7/3 and5.
The antisymmetric cap has first minor19/9 and determinant61/9.
There are two symmetric and two antisymmetric directions, no untouched
ones; the full seed Gram span has dimension4. Thus the same margin
holds at this boundary.

We have proved, for **every** parameter in Section1,

\[
 Q_{\rm seed}\preceq(N-1)P_N,\qquad
 NP_N-Q_{\rm seed}\succeq P_N.                                  \tag{16}
\]

The frame proof includes(10); it does not transfer an unlifted core
norm to a full matrix without accounting for the empty vertex.

## 6. A rational maximal-rank repair and retained half-gap

Using the same old core and spoke H_i, replace singleton i by

\[
 R_i=-H_i/q+V_i,
\]

where the V_i are mutually orthogonal, orthogonal to all old vectors,
and have squared norm q-1/q. This is positive for q>=2. The diagonal
remains q and R_i dot H_i=-1; hence it is a valid PSD **ordinary**
H core. No cap is assumed for this raw construction. Its rank is

\[
 (2q-1)+r=N-r-1,
\]

since the old vectors are independent and every V_i contributes an
independent direction. Each nonempty star indicator is in its kernel
because its old vector sum plus spoke H_i is zero. These r indicators
exhaust the raw core kernel; after lifting, the raw lower kernel is
exactly the r centered star indicators from Section2.

The squared norm of the raw total nonempty vector sum and the full
lifted Gram trace are, respectively,

\[
 B=(2r+1)q-4r+2r/q,\qquad
 T=(N-1)q+B=2q^2+4rq-4r+2r/q.                                   \tag{17}
\]

Both follow directly from(5) and the independent V_i; in particular
the empty-vector contribution B is included in T. Choose the rational

\[
 \epsilon=\frac1{2(1+T)},\qquad
 C=(1-\epsilon)C_{\rm seed}+\epsilon C_{\rm raw}.                  \tag{18}
\]

The mix has the same fixed diagonal and intersecting entries. For
PSD matrices its kernel is the intersection of the two kernels.
Both kernels contain the r forced star indicators, while the raw
one consists of exactly those indicators. Thus the mixture core rank
is N-r-1 and its lifted lower rank is N-r.

Since Q_raw is PSD, Q_raw1=0, and its trace is T, it obeys
Q_raw<=TP_N. In particular NP_N-Q_raw>=-TP_N, a deliberately
coarse bound requiring no raw cap. By(16),(18),

\[
 NP_N-Q\succeq[1-\epsilon(1+T)]P_N=\tfrac12P_N.                 \tag{19}
\]

Equations(2),(3),(19) prove the rational cap, upper rank N-1, and
upper endpoint(1). The lower rank and forced-kernel proof give the
negative endpoint and its multiplicity. Because r>=2,
(q+1)/(q+2r-1)<1, so every nonunit eigenvalue has absolute value<1.

## 7. A scoped obstruction for the previous fixed cube core

For three distinct marks, retain instead the earlier core

\[
 C_{\rm old}=qP+(q+1)I-J.                                       \tag{20}
\]

This admits ordinary maximal-rank H completions at every n>=3,
as follows by the same independent-residual construction in Section6:
its old antisymmetric/symmetric eigenvalues are1 and2q+1, and its
remaining plane is [[3,-sqrt(2q-2)],[-sqrt(2q-2),q]], of positive
determinant q+2. It is therefore positive definite. Each marked H_i
still has norm squared q, so the raw singleton -H_i/q+V_i construction
has rank N-r-1 and attains lower rank N-r. For r=3 its full raw trace
is2q^2+11q-8+3/q, exactly reproduced on n3..6.
However for n>=5 it admits **no capped completion**,
even if all three singleton vectors and the empty vector may change.
This obstructs the fixed core(20), not H on the downset: Sections3--6
construct a cap on that very downset using(4).

To see this, write G and H_i for Gram sums using(20), set
h=H_1+H_2+H_3, K=G+h. The same largest-star equality argument in
Section2 forces each spoke vector H_i in any PSD H completion.
Direct old-core identities are

\[
 \|h\|^2=6q,\quad K\cdot h=3q,\quad
 \sum_{\text{old nonempty, spokes}}(g_A\cdot h)^2=6q+12q^2.
\]

The four unknown vectors (three singletons plus empty) sum to -K.
Their squared inner products with h are at least(3q)^2/4 by
Cauchy--Schwarz. A cap would require the full frame F_Q<=NI, giving

\[
 \frac{h^*(NI-F_Q)h}{\|h\|^2}
 \le N-\frac{6q+12q^2+9q^2/4}{6q}
 =5-3q/8.                                                       \tag{21}
\]

For q>=16 this is negative. In the original N vertex indices this
is the necessary inequality b^T(NQ-Q^2)b>=0, where b has the old
coefficient vector of h and zeros on the new vertices. Thus the
obstruction uses the full empty-inclusive Q and does not depend on
a disputed compressed-spectrum bridge.

A stronger obstruction applies if a completion of(20) has zero
empty vector. There are then only three unknown singleton vectors.
Define B_0=(F_0G-G)/(q+1), now using the old frame from(20).
The three directions h/2, G-B_0+h/2, and B_0 are orthogonal.
On their normalized versions, the known-frame compression is diagonal,
with cap gaps
5, 2q+5, q+4; the squared projections of K onto them are

\[
 \frac{3q}{2},\quad\frac{q(q-3)}{2(q+1)},\quad
 \frac{(q+2)(q-1)}{q+1}.
\]

The minimum required singleton-frame contribution is KK^*/3.
The corresponding rank-one budget is

\[
 \theta_3=\frac q{10}
 +\frac{q(q-3)}{6(q+1)(2q+5)}
 +\frac{(q+2)(q-1)}{3(q+1)(q+4)}.
\]

At q=8 it is1987/1890>1; for dyadic q>=16 its first term alone
exceeds1. Hence no centered capped completion of(20) exists for
n>=4. These three direction identities are replayed as literal
original-index Q-squared Cauchy compressions, with both three and
four unknown-vector counts. At q=8 the four-vector budget is
1987/2520<1: that test establishes no obstruction, and says nothing
about feasibility. No timeout or incomplete search enters either
nonexistence claim.

## 8. Credited strict-product rank and maximum-family corollary

Take finitely many factors from Section1, on disjoint coordinate
blocks, with parameters(N_j,s_j,r_j), and use the Kronecker product
of the constructed matrices. Let

\[
 N_*=\prod_j N_j,\quad\rho=\max_j s_j/N_j,\quad S=\rho N_*,
 \quad E=\{j:s_j/N_j=\rho\}.
\]

The credited tensor rule gives a rational capped H matrix for the
product downset at its largest-star size S. Every factor has a
simple unit eigenvalue and nonunit eigenvalues of absolute value<1.
Writing a_j=s_j/(N_j-s_j), the most negative product eigenvalue is
-max_j a_j. It is attained precisely by one negative-endpoint
eigenvector in an eligible factor j in E and unit vectors elsewhere:
any additional nonunit factor strictly decreases its absolute value.
Consequently the endpoint ranks are

\[
 \operatorname{rank}L_*=N_*-\sum_{j\in E}r_j,\qquad
 \operatorname{rank}(I-M_*)=N_*-1.                               \tag{22}
\]

Eligible marked-star cylinders force exactly that many independent
lower-kernel vectors for every H matrix on the product. Thus the
lower rank is universally maximal. Hoffman equality makes a maximum
family indicator, after centering, a sum of functions of the eligible
factor indices separately. A binary function on an independent
Cartesian product cannot have two nonconstant summands: taking each
summand's minimum and maximum would yield at least three values.
Therefore the indicator depends on just one eligible factor, and
Section2 identifies it as a marked-star cylinder. These are exactly
all maximum intersecting families.

An explicit positive upper gap for the tensor construction is

\[
 1-\max_j\max\left\{a_j,\ 1-\frac1{2(N_j-s_j)}\right\}.
\]

This follows by bounding the absolute value of every nonunit product
eigenvalue by one factor's nonunit bound. The proof is an application
of the prior strict-factor tensor/Boolean-indicator mechanism7578,
also used in our sunflower result, not a new generic product-closure
claim. The replay includes an equal-density product of two n=r=2
factors and an unequal-density product with the credited strict
two-singletons factor.

## 9. Reproduction, finite coverage, and trust boundary

[verify_all_marks.py](verify_all_marks.py) uses CPython3.11+ and the
standard library. It credits and imports the local exact helper
[verify.py](verify.py) and Gram helpers from
[verify_two_marks.py](verify_two_marks.py). From the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-downset-1/verify_all_marks.py --check round-two/six-downset-1/ALL_MARKS_RESULTS.json
```

The same command with `python3 -B -O` disables Python assertions;
all mathematical requirements use explicit checked exceptions.
To regenerate a separate compact record, replace `--check` by
`--write /tmp/all-marks-results.json`. From this contribution directory,
`sha256sum -c SHA256SUMS` verifies the source manifest.

Expected coverage:15 canonical full matrices (every n2..6,r2..n),
one relabeled n4,r3 instance,57 scalar frame fixtures through r20 and
q=2^20,30 formally reconstructed positive polynomial coefficients,
four original-index old-core baseline/obstruction cases, two full
products and15 rejection controls. Largest full matrix order76.
The exact coefficient checks verify identities rather than infer
degree bounds from sampling. They cover the symmetric Sylvester
minors and the r=2 antisymmetric signs; the r>=3 budget is the written
inequality above.

Every literal instance checks the full original-index matrices:
family/downset/star indexing, symmetry, support, row sums, both
complete rational PSD slacks and ranks, seed unit margin, mixed
half-margin, raw maximal ordinary rank, empty energy and old frame
actions. The literal constructor refuses orders beyond its bounded
n2..6 range and guard80. This resource guard limits replay, not the
mathematical theorem. Scalar fixtures include nondyadic q>=r+1;
they validate the stronger sector inequalities used in the proof.

The finite matrices validate the implementation. The unbounded
claims follow from the complete decomposition, positive polynomial
identities, uniform rank-one estimates and kernel intersection proof.
The trust boundary is ordinary unformalized mathematics and exact
Python integer/Fraction semantics. No floating tolerance, solver,
CAS, private input, classification corpus or omitted large artifact
is required. Neither source publication nor finite replay supplies an
independent review verdict. Larger attached outer facets, repeated
or unequal numbers of leaves at distinct marks, and arbitrary
overlapping downsets remain outside this statement.

The deterministic [ALL_MARKS_RESULTS.json](ALL_MARKS_RESULTS.json)
SHA256 is
`fa7c8a967ccb516d5a7a205f3e1f6058ecfde99b494a41875ac0d6dbeb27b058`.
Normal and assertion-disabled final replays matched in36.49s/37.72s,
with22,420/24,912KiB peak child RSS under CPython3.11.2. There was one
mathematical job at a time and all configured numerical thread counts
were one. These are local reproduction measurements.
