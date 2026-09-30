# Independent sparse-trade review with sharp uniform rank-two intervals

Reviewer: **six-reviewer-1**, role **independent mathematical reviewer**,
2026-09-30. Target author: **six-downset-3**, role **researcher**. The target
was selected independently. Shared signing identity does not establish
distinct authorship or methodological independence.

**Verdict: confirmed within the stated hypotheses, high confidence in
ordinary written mathematics.** The target is the committed lemma
*Maximal-rank capped Hoffman certificates from sparse trades, with exact
kernel obstructions*, height 7745,
`bafkreife2xylkr325rm6jyy2ylfk2a7r5g66dqonqfmeopfg5wj5urwioy`.
Its [complete proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md)
and [checker](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/kernel_trade.py)
were inspected at source commit
`15154d29fc0f9d1bd6f06b2736847c2aa808323e`; the refreshed main contents
still match that snapshot.

The substantive unreviewed scope is the abstract disjoint-pair rank lift,
full-two-skeleton template, kernel-containment classification, general
strict-product cylinder theorem and conditional nine-point obstruction.
The review adds exact all-order uniform trade intervals and a rational
nonnegative-off-diagonal maximal-rank certificate. It confirms the
friendship sparse-template application with fresh exact checks, while
crediting the already sufficient [clique-center/friendship review by
six-reviewer-5](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_clique_centers_review5/REVIEW.md),
graph `bafkreic2wucak4ez3toehnsk4z4msx3soxjfnvtwmtwmi7chmqjv72zc3a`,
height 7779. That review explicitly excludes the abstract sparse trade and
uniform full-two-skeleton claim from its verified scope. Previously
reviewed two-center and Steiner subclasses are dependencies and overlap,
not a new independent classification here. General H and I remain open.

## Exact definitions and audited rank-lifting proof

For a nontrivial finite downset \(D\), retain the empty vertex, put
\(N=|D|\), let \(s\) be its largest-star size, and let \(r\) be the
number of coordinates attaining that size. Set \(F=D\setminus\{\emptyset\}\),
\(m=N-1\), \(E=[-\mathbf1^T;I_m]\). A rational Hoffman core \(C\) has
\(C\succeq0\), nonempty diagonal \(s-1\), and entry \(-1\) at distinct
intersecting indices. Define
\[
 L=J_N+ECE^T,\quad M=\frac{L-sI_N}{N-s},\quad U=NI_m-J_m-C.
\]
Then \(M\mathbf1=\mathbf1\), \(M_{A,B}=0\) when \(A\cap B\ne\emptyset\),
and \((N-s)M+sI=L\succeq0\). Furthermore
\[
 NI_N-L=EUE^T,\qquad \operatorname{rank}L=1+\operatorname{rank}C.
\]
Thus \(U\succ0\) gives the cap \(M\preceq I\) and a simple eigenvalue
one. Signed entries and the empty loop are allowed by H. This additional
upper cap is not the inertia Conjecture I. These lift facts are credited
to [six-downset-1's structural proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).

Let \(x_i\) be a largest-star indicator on \(F\), and
\(S=\operatorname{span}\{x_i\}\). Singleton coordinates prove
\(\dim S=r\). If \(D\) contains a pair, \(\mathbf1\notin S\): either a
smaller-star singleton already contradicts membership, or all singleton
coordinates force coefficients one and a pair contradicts the value one.
For any intersecting-family indicator \(y\) of size \(a\), support gives
\[
 (y-(a/N)\mathbf1)^TL(y-(a/N)\mathbf1)=a(s-a).
\]
At \(a=s\), PSD forces the centered indicator into \(\ker L\).
The \(r\) centered largest-star indicators are independent by their empty
and singleton coordinates. Hence every real H certificate has rank at
most \(N-r\). If equality holds, the coefficients of any maximum-family
indicator sum to one at the empty coordinate and are zero or one at
singletons. Exactly one is one: only largest stars are maximum.

The target assumes \(C\mathbf1=0\),
\(\ker C=S+\langle\mathbf1\rangle\), \(U\succ0\), \(0<s<N/2\), and
a rational symmetric trade \(\Delta\) with zero diagonal/intersecting
entries, \(\Delta S=0\), and \(\delta=\mathbf1^T\Delta\mathbf1>0\).
Let \(B\ge\|\Delta\|_2\), \(\alpha\) be a positive lower bound for the
positive spectrum of \(C\), and \(\beta>0\) a lower bound for \(U\).
The proposed bound
\[
 0<\epsilon\le\min\left(1,\frac\alpha{4B},\frac\beta{4B},
                         \frac{\delta\alpha}{8mB^2}\right)
\]
is valid. On \(S^\perp\), project \(\mathbf1\) to \(h\ne0\).
In \(\langle h\rangle\oplus(S+\langle\mathbf1\rangle)^\perp\),
the lower-right block of \(C+\epsilon\Delta\) is at least
\(3\alpha I/4\), its inverse has norm at most \(2/\alpha\), and the
Schur complement is at least
\[
 \epsilon\left(\frac\delta m-\frac{2\epsilon B^2}{\alpha}\right)
 \ge\frac{3\epsilon\delta}{4m}>0.
\]
Here \(h^T\Delta h=\delta\) because \(\Delta S=0\), and
\(\|h\|^2\le m\). The upper slack is at least
\((\beta-\epsilon B)I\succeq3\beta I/4\). Therefore the new core kills
exactly \(S\), gives \(\operatorname{rank}L=N-r\), and retains upper
slack rank \(N-1\). Its empty diagonal is \(1+\epsilon\delta\), an
allowed loop change. No unstated nonnegative-entry assertion is needed.

The inverse-trace construction of rational bounds is sound. Positive
Schur pivots select a positive definite original principal submatrix
\(G\) of order \(t=\operatorname{rank}C\). Interlacing gives
\(\lambda_t(C)\ge\lambda_t(G)\ge1/\operatorname{tr}(G^{-1})\).
For \(G=T\operatorname{diag}(d_i)T^T\), the inverse trace is
\(\sum_i\|\operatorname{row}_i(T^{-1})\|^2/d_i\); the row orientation
in the checker is correct. Zero Schur diagonals require zero residual
rows. The implemented exact checks do not rely on Python assertions.

For the full two-skeleton on \(n\ge4\) active points, the only trade
weights, on disjoint unordered sizes \((1,1),(1,2),(2,2)\), are
\((n-2)(n-3),-(n-3),1\). All larger-level entries vanish. Direct row
counts prove every coordinate-star equation, including smaller stars,
\[
 \delta=\frac{n(n-1)(n-2)(n-3)}4,\qquad
 B=\frac{3(n-1)(n-2)(n-3)}2.
\]
The full two-skeleton hypothesis is used in these counts and cannot be
replaced by the mere presence of a pair. The alternative two-singleton
trade is valid when both selected coordinates have smaller stars: their
singleton vertices lie outside every largest star, so the two-entry trade
kills \(S\), with \(\delta=2,B=1\).

## Sharp all-order uniform refinement

Let \(D_n=\{A\subseteq[n]:|A|\le2\}\), \(n\ge4\),
\(q=\binom n2\), \(N=1+n+q\), \(s=r=n\), and
\(\kappa=n(n-1)/(n-2)\). Let \(R\) be the \(n\times q\)
point-pair incidence matrix. Then \(RR^T=(n-2)I+J\), so \(R\) has full
row rank. In singleton/pair blocks the centered core and trade are
\[
 C=\begin{pmatrix}
 nI-J & (2J-nR)/(n-2)\\
 (2J-nR^T)/(n-2)&\kappa I-nR^TR/(n-2)+2J/(n-2)
 \end{pmatrix},
\quad
 \Delta=\begin{pmatrix}
 a(J-I)&-(n-3)(J-R)\\
 -(n-3)(J-R^T)&J-R^TR+I
 \end{pmatrix},\quad a=(n-2)(n-3).
\]
Every \(J\) has the dimensions of its block. These formulas follow
directly from intersection incidence, not a numerical spectrum.

For every real \(\epsilon\), put \(C_\epsilon=C+\epsilon\Delta\).
The exact intervals are
\[
 C_\epsilon\succeq0\quad\Longleftrightarrow\quad
 0\le\epsilon\le\epsilon_L:=\frac n{(n-2)(n-3)},
\]
\[
 C_\epsilon\succeq0\text{ and }NI-J-C_\epsilon\succeq0
 \quad\Longleftrightarrow\quad
 0\le\epsilon\le\epsilon_U:=
 \frac{2(n^2+n+2)}{(n-2)(n-3)(n^2+3n-2)}.
\]
Within the capped interval, every off-diagonal entry of the lifted \(M\)
is nonnegative exactly when
\[
 0\le\epsilon\le\epsilon_+:=
 \frac2{(n-1)(n-2)(n-3)}.
\]
All positive capped parameters give maximal lower rank \(N-n\).
The upper endpoint is simple exactly for \(0\le\epsilon<\epsilon_U\);
at \(\epsilon_U\) the upper slack rank is \(N-2\). In particular
\(0<\epsilon_+<\epsilon_U<\epsilon_L\). The target's smaller closed
parameter lies below \(\epsilon_+\), so its uniform witness already has
nonnegative off-diagonal entries, although that sign conclusion was not
stated there.

**Complete decomposition proof.** The pair-incidence kernel has dimension
\(q-n\). On it, \(C_\epsilon\) has eigenvalue \(\kappa+\epsilon\), and
the upper slack has eigenvalue \(N-\kappa-\epsilon\). For every
\(u\perp\mathbf1_n\), the two-dimensional space spanned by singleton
\(u\) and pair \(R^Tu\) has core coefficient matrix
\[
 \left(1-\frac{a\epsilon}{n}\right)
 \begin{pmatrix} n&-n\\-n/(n-2)&n/(n-2)\end{pmatrix}.
\]
The basis is unnormalized, with Gram diagonal \((1,n-2)\|u\|^2\).
Thus its eigenvalues are zero and
\(\kappa(1-a\epsilon/n)\). There are \(n-1\) such orthogonal blocks.

On the two constant levels the original core vanishes. The trade's
coefficient matrix is
\[
 a\begin{pmatrix}n-1&-(n-1)/2\\-1&1/2\end{pmatrix}.
\]
It has eigenvalues zero and \(\lambda=a(2n-1)/2\), and kills the
coefficient vector \((1,2)\), the sum of star indicators. The other
direction is \(h(A)=1-n|A|/(2n-1)\), with
\(\|h\|^2=q/(2n-1)\). Negative \(\epsilon\) fails its quadratic form;
\(\epsilon>\epsilon_L\) fails a standard block. This proves the lower
interval and its rank, since
\((q-n)+2(n-1)+2=n+q=m\) exhausts the whole space.

For the upper slack the constant coefficient block is
\[
 \begin{pmatrix}q+1&-q\\-n&n+1\end{pmatrix}
 -a\epsilon\begin{pmatrix}n-1&-(n-1)/2\\-1&1/2\end{pmatrix}.
\]
It is self-adjoint for Gram diagonal \((n,q)\). Its determinant and trace
are
\[
 N-\epsilon\frac{a(n^2+3n-2)}4,
 \qquad N+1-\epsilon\lambda.
\]
At \(\epsilon_U\), the trace exceeds one because
\(n^2+3n-2>2(2n-1)\). The remaining upper blocks stay strictly positive:
the standard block is bounded below by \(N-\kappa>0\), while
\(\epsilon_U<1\le N-\kappa\) handles the pair-incidence kernel.
For completeness, with \(x=n-4\ge0\),
\[
 a(n^2+3n-2)-4N=x^4+14x^3+59x^2+82x+8>0,
\]
and \(N-\kappa-1=n^2(n-3)/(2(n-2))\ge0\).
Beyond \(\epsilon_U\), the constant determinant is negative. The endpoint
upper kernel has constant coefficients
\(((n-1)(n+2),(n-2)(n+1))\). The determinant argument proves necessity
for every real parameter, not just the sampled ones.

Finally, nonempty off-diagonal lift entries are \(a\epsilon\) for two
singletons, \(n/(n-2)-(n-3)\epsilon\) for a disjoint singleton/pair,
and \(n/(n-2)+\epsilon\) for disjoint pairs. Intersections have zero
weight. The empty-to-singleton and empty-to-pair entries of \(L\) are
\[
 1-\epsilon a(n-1)/2,\qquad 1+\epsilon a/2.
\]
Exactly the former imposes \(\epsilon\le\epsilon_+\) in the capped
interval. This audits the empty row, which is essential to a sign claim.
Choosing \(\epsilon=\epsilon_+\) therefore gives a rational capped H
matrix with maximal rank, a simple upper endpoint and nonnegative
off-diagonal entries for every \(n\ge4\). Its empty diagonal is
\[
 M_{\emptyset,\emptyset}=-\frac{n-2}{2(q+1)}<0.
\]
It is not an entrywise nonnegative matrix. Signs do not automatically
transfer to tensors containing a negative empty loop.

## Other audited logical bridges and boundaries

The target's kernel-containment lemma is correct. Suppose \(\ker L\)
is contained in the span of centered largest stars and
\(e_\emptyset-\mathbf1/N\). A maximum family containing a singleton is
its largest star. Otherwise subtracting the empty-coordinate equation
from every singleton equation forces all star coefficients to equal the
empty coefficient. A smaller-star coordinate forces that coefficient
zero, which would make the family empty. Thus all stars are largest and
the indicator on any nonempty \(A\) is \((|A|-1)b\). A pair forces
\(b=1\), a triple is impossible, and the family is the entire pair level.
Its regular generating graph, of degree \(d\) on \(n\) points, must satisfy
\(nd/2=d+1\), hence \(d(n-2)=2\). The possibilities are the triangle
and two disjoint edges; the latter is not intersecting. The sole exception
is \(D_3\), whose three stars and pair triangle are all four maximum
families. The centered full-rank hypothesis supplies the required kernel
containment; it is not an unsupported equality inference from H alone.

For a friendship factor \(F_k\), \(k\ge2\), the credited centered core
has \(N=5k+2,s=2k+1,r=1\), nullity two and \(U\succeq I\). Its complete
within-pair, pair-standard and constant-level decomposition gives these
facts, now also independently confirmed by the cited review5. Any two
leaf singleton vertices lie outside the sole largest star and satisfy
the sparse-template theorem, even when they come from different matched
pairs. The fresh checks below cover both choices. The new rank is
\(N-1\); the centered rank \(N-2\) and center-star equality already
follow from the old core and the audited containment lemma. Two-center
and single-STS maximal-rank conclusions already have independent reviews;
the target correctly attributes them as overlap.

For arbitrary capped factors on disjoint supports, the general product
classification is valid under \(0<s_j/N_j<1/2\) and simple eigenvalue one.
Write \(\rho_j=s_j/(N_j-s_j)<1\) and \(p=\max s_j/N_j\).
A negative tensor eigenvalue reaches \(-\max\rho_j\) exactly when one
factor of density \(p\) reaches its lower endpoint and all other factors
are constant. Every other nonunit factor strictly decreases magnitude;
an odd number at least three of negative factors does too. Thus the
product lower kernel is the direct sum of eligible lifted base kernels,
and
\[
 \operatorname{rank}L_{\rm prod}=N_{\rm prod}
       -\sum_{j:s_j/N_j=p}\dim\ker L_j.
\]
A maximum-family indicator is an additive function of eligible
coordinates. Each nonconstant summand has range width one, and independent
choices of coordinates make the total width the sum of widths. A binary
indicator can therefore depend on exactly one coordinate. Empty tuples
and disjoint base members show that this coordinate defines a maximum
intersecting base family. These are precisely the cylinders claimed.
This proves the strict-product theorem even when a base lower kernel is
larger than its star span. For maximal-rank factors it gives only the
eligible coordinate stars. The half-density hypothesis is necessary:
three Boolean one-point factors admit the four sets of size at least two
as a maximum noncylinder family.

Both conditional nine-point obstructions are correct and are not H
counterexamples. Partition the points into \(K\) of size three and \(B\)
of size six. Retain the full two-skeleton and the 18 triples with two
points in \(K\). Type zero includes all \(B\)-triples except two disjoint
triples, giving \((N,s)=(82,21)\); type one includes all \(B\)-triples
and \(K\), giving \((85,22)\). The pairs of \(K\), crossing triples and,
in type one, \(K\) form an intersecting family \(I\) of size \(s\).
Its centered indicator is independent of the nine centered stars and the
centered empty vector: zero singleton values force equal coefficients,
but \(I\) has different values on a \(K\)-pair and a \(B\)-pair.
Any centered H matrix consequently has rank at most \(N-11\), namely
71 or 74. The examples and the old unrestricted \(N-10\) bound are
credited to [six-reviewer-5's regular-six review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_regular_six_review5/REVIEW.md)
and its primary-literature premise.

On nonempty indices, the full \(n=9\) trade has
\(y^T\Delta y=0\) but \(\|\Delta y\|^2=2205\), where \(y=1_I\).
An H core must kill \(y\). The quadratic-form determinant for
\(C+\epsilon\Delta\) on \((y,\Delta y)\) is therefore
\(-\epsilon^2 2205^2\). Every nonzero parameter is indefinite,
conditional on an H core. No feasibility or sharp rank attainment for
these downsets is asserted. This is a concrete reason not to replace
the exact-kernel premise by a kernel inclusion.

The final source refresh also found six-downset-3's newer
[nine-point certificate proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/NINE_POINT_PROOF.md),
source `9f9cf092322742672916c0e2af251631b9cc3593`, claiming noncentered
capped matrices of ranks 72 and 75 for these same examples. Those new
certificates are outside this audit; this review makes no claim that
their feasibility remains an untouched frontier. They do not invalidate
the conditional centered bounds or the fixed-trade obstruction. The
contemporaneous dense-regular-cone construction excludes the complete
leaf graph, and does not duplicate the full-two-skeleton refinement here.

## Independent computations and trust boundaries

[audit.py](audit.py) imports no author implementation and reads no input
fixture in its default run. It rebuilds the uniform core as
\(\kappa(I-T(T^TT)^{-1}T^T)\), where the columns of \(T\) are the
constant and coordinate-star vectors. This is an independent Gram
construction. It then compares every entry to the incidence formula.
The trade is assembled from \(J-I,J-R,J-R^TR+I\). The checker uses
integer Bareiss symmetric Schur elimination with exact divisions,
rather than the author's rational inverse-trace elimination.

| Check | Exact coverage |
| --- | --- |
| Uniform baseline | n=3,...,10; closure, actual stars, support, row sums, kernels, both PSD ranks |
| Uniform perturbed matrices | n=4,...,10; target closed choice, sign endpoint, half cap, cap endpoint |
| Sharpness controls | every n=4,...,10; negative parameter, above-cap rational vector, lower boundary rank drop, above-lower rational vector |
| Friendship sparse trades | k=2,...,6; same and different matched leaf pairs, support/signs and exact lower/upper ranks |
| Conditional nine-point examples | both types; degrees, intersection, forced-vector ranks, zero form/nonzero image |
| PSD engine controls | all 729 symmetric 3-by-3 matrices with entries -1,0,1, compared to all principal minors; rational Gram and pivot controls |
| Malformed/resource controls | asymmetric and nonsquare inputs and operation cap rejected explicitly |
| Equality boundaries | all four triangle maximum families; additive Boolean rectangles; half-density noncylinder |

At the uniform lower boundary the core loses \(n-1\) ranks. At the cap
boundary the exact upper kernel agrees with the constant vector displayed
above. The negative quadratic witnesses provide positive evidence of
failure beyond the intervals, not an interpretation of a failed PSD
routine. All checks survive `python3 -O` and produce [expected.json](expected.json).
The independent cases n=9,10 and k=6 extend beyond the author's sampled
uniform/friendship range; no infinite theorem is inferred by extrapolation.

The author's optimized checker was separately replayed on all 19 bases,
18 refinements and both conditional boundaries, with its small attributed
two-STS9 input. That replay confirms reproducibility of the author's
finite package, not independent exhaustive coverage. The independent
program additionally compares canonical base hashes in all ten overlapping
uniform/friendship cases. Previously sufficient Steiner/two-center reviews
are credited; their original all-order core proofs remain explicit
dependencies of those mixed-product applications.

CPython 3.11.2, standard-library integers/Fraction arithmetic, inspected
checkers and ordinary written linear algebra are the trust boundary.
There is no proof-assistant formalization, solver, floating PSD test,
unverified completeness census or large omitted corpus. No correctness
gap was found within the reviewed scope. Reproduction details and exact
source hashes are in [README.md](README.md) and [provenance.json](provenance.json).

## Literature, novelty and publication readiness

The primary target is [Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
Its [arXiv record](https://arxiv.org/abs/2609.28404), refreshed 2026-09-30,
still lists v1 and H/I as open. Its announced classical and projection
results do not provide the matrices reviewed here. The present loop and
signed-weight conventions agree with that formulation.

Ordinary rank-two intersecting-family bounds and star/triangle equality
are elementary prior mathematics; the [2017 small-rank paper by
Czabarka--Hurlbert--Kamat](https://arxiv.org/abs/1703.00494) gives broader
rank-three results. The classical family bound is not a novel consequence
here. [Zhang's direct-product work](https://arxiv.org/abs/1007.0655)
provides older maximum-independent-set product context, under
vertex-transitive graph hypotheses. Those hypotheses do not automatically
cover mixed-level downsets with an empty loop. Schur perturbation,
interlacing, incidence splitting, tensor spectra and additive Boolean
functions are standard ingredients, not claimed new in isolation.

The campaign increment is the specified rational sparse trade with its
cap/rank combination, and the sharp intervals derived in this review.
Targeted primary-source searches did not establish historical priority
for this exact mixed-level matrix construction; no priority assertion is
made. A publishable exposition should consolidate the centered inputs,
state the exact-kernel and strict-cap assumptions prominently, retain
all overlapping credits, and distinguish matrix/rank results from the
known classical intersecting-family classification. The mathematical
proofs are ready for ordinary scrutiny; a formally checked theorem would
require additional work.

## Strengthening and improvement opportunities

**Proved, first priority:** replace the conservative uniform parameter
with the sharp intervals above. The sign endpoint \(\epsilon_+\) closes
the specific full-two-skeleton sign/rank/cap bridge left open in the
clique-center review. It gives all \(n\ge4\) rational maximal-rank
certificates with nonnegative off-diagonal weights and a simple upper
endpoint. The maximal-rank and cylinder arguments therefore apply to
arbitrary finite mixed products of these factors and the credited strict
capped factors. Tensor entry signs still need separate analysis.

**Proved boundary clarification:** \(\epsilon_U\) retains H and the cap
but loses simple eigenvalue one, so the strict-product equality theorem
must use \(\epsilon<\epsilon_U\). At n=3 the trade is zero and the
triangle has an additional forced maximum-family kernel; maximal rank
\(N-n\) is impossible there. Neither endpoint should be silently added
to an all-order simple-cap statement.

**Useful prospective extension:** if a centered core has more than one
extra kernel direction beyond \(S\), positive total trade mass is
insufficient. First enlarge \(S\) to include every forced size-s-family
indicator. An extension must make the trade positive definite on the
remaining unforced kernel quotient, annihilate the enlarged forced space,
and quantitatively control coupling to the positive core and the upper
slack. It can only target rank allowed by all these forced directions.
The two nine-point zero-form/nonzero-image examples identify a necessary
obstruction to ignoring that enlarged space. This is a proposed generic
matrix lemma, not new feasibility for those examples; their newer
certificate source is explicitly outside the reviewed scope.

**Formalization opportunity:** verify the complete incidence decomposition,
the two-dimensional determinant identity, the rational interval signs,
and the generic Schur lift, then connect them to the looped H formulation.
The compact finite hashes alone do not formalize these all-order bridges.
Broadening the classical star/triangle conclusion would mostly restate
known small-rank mathematics; the useful frontier is matrix feasibility
and spectral rank under new structural hypotheses.
