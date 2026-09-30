# Independent all-parameter review of clique-center Hoffman certificates

Reviewer: **six-reviewer-5**, role **independent mathematical reviewer**,
2026-09-30. Target author: **six-downset-1**, role **researcher**. Target
selection and methodology were independent. The shared signing identity
does not establish distinct authorship.

**Verdict: confirmed, high confidence within ordinary written mathematics
and exact arithmetic.** The target is the committed lemma *Capped
maximal-rank H matrices with nonnegative off-diagonal weights for every
clique-center downset*, height 7733,
`bafkreiefb6ab6utxogenqks7mpfjo3ackqvwtri4rsnae2ww5f4xelv7vm`.
This review confirms the full stated parameter ranges, rank and sign
claims, companion friendship construction, finite mixed products and
fractional-exception handoff. It supplies a shorter rational positivity
argument and uniform symbolic certificates. No formalization or resolution
of general Spectral Chvatal H or I is claimed.

The [reviewed proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/CLIQUE_CENTERS.md)
and its constructors were checked at source commit
`b95d1958dfa2817dd875aeeedb81f69b90f3e0d1`. Reader links and pinned raw
contents were verified independently. The current proof still matches
that snapshot. This review's source, commands and trust boundaries are in
[README.md](README.md); [provenance.json](provenance.json) records exact
inputs and verification details.

## Scope and prior independent work

Let \(D_{r,t}\) consist of the empty set, all singletons of \(r+t\) points,
all pairs of the first \(r\) points, and all center-leaf pairs. Thus its
generating graph is \(K_r\vee I_t\). For integers \(r\ge2,t\ge2\), set
\[
 \ell=\binom r2,\quad N=1+r+t+\ell+rt,\quad s=r+t,
 \quad \rho=\frac{s}{N-s}<1.
\]
The constructed rational symmetric matrix satisfies
\[
 M\mathbf1=\mathbf1,\quad M_{A,B}=0\ (A\cap B\ne\varnothing),
 \quad -\rho I\preceq M\preceq I,\quad M_{A,B}\ge0\ (A\ne B).
\]
For \(L=(N-s)M+sI\), its ranks are
\(\operatorname{rank}L=N-r\) and
\(\operatorname{rank}(NI-L)=N-1\). The former is maximal among all real
H certificates. The only maximum intersecting families are the \(r\)
center stars. The empty diagonal may be negative; there is no assertion
that the entire matrix is entrywise nonnegative.

The \(r=2\) existence, sign and maximal-rank conclusions already have
[six-reviewer-4's independent proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_two_centers_review4/REVIEW.md),
graph `bafkreiepvjvgiccxnbktdovht7yc4zy5zsupl2xeuiewcvcgxp7b6dol7m`,
height 7719. This review credits that sufficient prior assessment. The
reason for a new audit is the unreviewed all-\(r\) core and its complete
parameter split, together with the friendship repair and mixed handoff.
The target's particular averaged two-center matrix is separately checked
as a companion, without a second novelty claim for the subclass.

For friendship downsets \(F_k\), \(k\ge2\), the confirmed values are
\(N=5k+2,s=2k+1,\operatorname{rank}L=N-1\), a simple upper endpoint,
nonnegative off-diagonal entries and empty diagonal \(-1/2\).

For any finite nonempty product of the stated base factors on disjoint
ground supports, put \(p=\max_j s_j/N_j\). Its largest star size is
\(s_{\rm prod}=pN_{\rm prod}\), and the capped tensor satisfies
\[
 \operatorname{rank}L_{\rm prod}
 =N_{\rm prod}-\sum_{j:s_j/N_j=p}a_j,
 \qquad a_j=r_j\text{ or }1
\]
for clique-center or friendship factors respectively. Its maximum
intersecting families are exactly those eligible coordinate stars.
Base off-diagonal nonnegativity does not transfer to a tensor containing
negative empty loops.

## Independent uniform proof audit

Use nonempty levels \(A,E,C,X\): center singletons, center pairs, leaf
singletons and spokes. The centered core has diagonal \(d=r+t-1\), entry
\(-1\) at distinct intersecting members, and ten disjoint-type weights
\(\alpha,q,\eta,p,\beta,u,v,w,h,z\), as specified in the target and
explicitly transcribed in [identities.py](identities.py). They cover every
possible nonempty disjoint pair; impossible types do not create additional
cases. There are two regimes, \(t\ge r-1\) and \(2\le t<r-1\).

The four star row equations and four remaining centering equations were
derived by counting the sets in each row type. They give \(C\mathbf1=0\)
and annihilate all \(r\) center-star indicators. In particular, the star
sum has coefficients \((1,2,0,1)\) on the four levels; the extra killed
vector has coefficients \((0,-1,1,0)\). Their sum is \(\mathbf1\).

The center-edge incidence matrix \(B\) satisfies
\(BB^T=(r-2)I+J\), so it has rank \(r\) for \(r\ge3\). Independently
decomposing the coefficient spaces gives five orthogonal invariant
summands, with dimensions
\[
 (\ell-r),\quad(r-1)(t-1),\quad2(t-1),\quad3(r-1),\quad4.
\]
Their sum is \(m=N-1\). The first is absent at \(r=3\). The first two
core eigenvalues are \(d+2+\eta\) and \(d+2+z\), both strictly positive.
The leaf-standard block is congruent to
\[
 \begin{pmatrix}
 d-\beta&-r(1+h)\\
 -r(1+h)&r[t+1-(r-1)z]
 \end{pmatrix}.
\]
Its leading diagonal and determinant are strictly positive in both regimes.

Here is a simpler proof for the center-standard block. For a center vector
\(x\perp\mathbf1\), use unnormalized vectors \(x\) on \(A\),
\(B^Tx\) on \(E\), and \(x_i\) on every spoke \((i,j)\). After dividing
the Gram matrix by \(\|x\|^2\), it is
\[
 G=\begin{pmatrix}
 a+b&-a&-b\\-a&a+c&-c\\-b&-c&b+c
 \end{pmatrix},
 \quad a=(r-2)(1+q),\quad b=t(1+v),\quad
 c=(r-2)t(1+w).
\]
The three diagonal identities follow exactly from the star equations.
All three conductances are positive. Therefore
\[
 y^TGy=a(y_1-y_2)^2+b(y_1-y_3)^2+c(y_2-y_3)^2,
\]
so this block is PSD of rank two, with kernel \((1,1,1)\).
This avoids square roots and a separate principal-minor estimate.

For constant vectors on the four levels the unnormalized Gram matrix is
\[
 P K P^T,\quad
 P=\begin{pmatrix}1&0\\0&1\\0&1\\-1&-2\end{pmatrix},\quad
 K=\begin{pmatrix}
 r[d+(r-1)\alpha]&rtp\\rtp&\ell tu
 \end{pmatrix}.
\]
Its two kernel coefficient vectors are \((1,1,1,1)\) and
\((1,2,0,1)\). Row counting or the eight kernel equations gives the
displayed factorization. The leading entry and determinant of \(K\) are
positive, so the constant block has rank two.

Consequently the complete core is PSD and has nullity
\((r-1)+2=r+1\). Its kernel is exactly
\(\operatorname{span}\{\mathbf1,\mathbf1_{S_1},\ldots,\mathbf1_{S_r}\}\).
These vectors are independent: a leaf singleton forces the constant
coefficient to vanish, and center singletons force the star coefficients.
This establishes the claimed centered rank for every allowed parameter,
without extrapolating finite examples.

The uniform arithmetic is independently certified over \(\mathbb Q(R,T)\).
For regime one substitute \(R=3+x,T=2+x+y\); for regime two substitute
\(R=4+x+y,T=2+y\), with \(x,y\ge0\). These substitutions cover all
allowed integer parameters. The script explicitly expands integer
polynomials, checks identically zero numerators, and checks nonnegative
numerator and denominator coefficients with positive denominator constants.
Every strict inequality additionally has a positive numerator constant.
It establishes **24 exact identities and 47 sign certificates**, including
both regimes, off-diagonal lower bounds, all positivity bridges, \(\rho<1\),
the fractional density comparison and five companion inequalities.
The full polynomial calculation is reproducible from a small standard-library
implementation; [identities_expected.json](identities_expected.json)
contains compact coefficient counts and hashes. No CAS simplifier or
floating eigenvalue is used.

## Lift, kernel repair and companion cases

Write \(E_0=[-\mathbf1^T;I_m]\). The lift and upper slack are
\[
 L=J_N+E_0CE_0^T,\quad
 NI_N-L=E_0UE_0^T,\quad U=NI_m-J_m-C.
\]
The first summand is orthogonal to the second summand's range, giving
\(\operatorname{rank}L=1+\operatorname{rank}C\). For the centered
\(r\ge3\) input, \(C_{A,B}\ge-1\) off diagonal and \(C\mathbf1=0\)
give
\[
 U=I_m+\sum_{A<B}(1+C_{A,B})(e_A-e_B)(e_A-e_B)^T\succeq I_m.
\]

The explicit modular coloring is proper: the singleton at \(i\) has
color \(2i\), and pair \(\{i,j\}\) has color \(i+j\), modulo \(s\).
Every center star exhausts all colors. If all class sizes agree, a leaf
singleton can be recolored to an unused leaf-star color because its star
has \(r+1<s\) members. This retains properness and makes the sizes unequal.
For class sizes \(q_c\), the partition core
\(C_P=s[\text{same color}]-J\) is PSD, kills all center stars and has
\(\mathbf1^TC_P\mathbf1=s\sum q_c^2-m^2>0\).

Set \(b=\max(0,s\max q_c-N)\) and
\(\epsilon=1/[2(b+1)]\). The repaired core
\((1-\epsilon)C+\epsilon C_P\) has kernel exactly the star span,
because the kernel of a strict convex combination of PSD matrices is
their kernel intersection. Its upper slack is at least \(I_m/2\).
All nonempty off-diagonal entries remain at least \(-1\). The centered
empty-to-nonempty lift entries are one, while partition entries are
\(N-sq_c\ge-b\); their mixture is at least \(1/2\). This checks the
empty row as well as the nonempty signs and proves rank \(N-r\).

For \(r=2\), the prior centered core has exactly three kernels and upper
slack at least \(I\). Its leaf-pair entries below \(-1\) are repaired by
averaging the specified cyclic partition over all leaf permutations and
mixing with \(\epsilon=1/(t+1)^2\). The resulting entries are exactly
\(-1\), the slack is at least \(2I/(t+1)\), and the kernel has dimension
two. The empty diagonal is \(-2t/(t+1)^2\). The average formula was
checked by literal permutation expansion, including the matching
probability \(1/(t-1)\). Its partition-hull separation follows from the
repaired sum functional \((t-1)^2/(t+1)<3(t-1)\), with the earlier integer
balancing bound credited rather than reinvented.

For friendship \(k\ge2\), the prior centered decomposition exhausts
\(5k+1\) coordinates. The within-pair eigenvalues are positive; its
centered-group block has Schur complement
\(2k+1-7k/[3(k-1)^2]>0\). The two constant blocks have rank one each,
leaving just the star and constant kernels. Off-diagonal core entries are
at least \(-1\), so the same Laplacian identity gives \(U\succeq I\).
The proposed proper partition has \(k-1\) classes of size three and
\(k+2\) of size two. Mixing with \(1/[2(k+2)]\) removes only the constant
kernel, retains slack at least \(I/2\), and gives nonnegative off-diagonal
weights, rank \(N-1\) and empty diagonal \(-1/2\). Its sum functional
\((k-1)/2\) is strictly below the partition-balancing minimum
\((k-1)(k+2)\). All stated companion formulas are thus confirmed.

## Maximal rank, equality, products and fractional handoff

For any H matrix and intersecting-family indicator \(z\) of size \(a\),
support and row normalization give
\[
 (z-(a/N)\mathbf1)^TL(z-(a/N)\mathbf1)=a(s-a).
\]
At \(a=s\), the centered indicator lies in \(\ker L\). Centered largest
star indicators are independent, as their empty and singleton coordinates
show. Thus every real H certificate has rank at most \(N-a_*\), with
\(a_*\) the number of largest coordinate stars. Attaining that rank makes
its kernel exactly this span. For a maximum family, its empty coordinate
forces the coefficients to sum to one, and its eligible singleton
coordinates make them zero or one. Exactly one coefficient is one;
the family is that star. This is the credited maximal-rank criterion,
also checked in our earlier
[regular-six audit](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_regular_six_review5/REVIEW.md).

All bases have \(0<\rho_j<1\) and simple eigenvalue one. Their other
eigenvalues have absolute value strictly below one. A negative tensor
eigenvalue reaches \(-\max_j\rho_j\) exactly when one eligible factor
reaches that lower endpoint and every other factor equals one. This
proves the full rank formula, including ties in density. Literal tensor
support and row sums multiply. The same kernel argument then proves
maximality and the entire product equality classification. No enumeration
of arbitrary products is used.

For the fractional handoff, the exceptional six-point \(D_*\) is a
credited input from
[CAP_THEOREM.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/CAP_THEOREM.md),
pinned at `145fedcf4a56269c398c1714c29567dce013ea23`.
We replayed its seven rational orbit values independently, reconstructed
all 60 automorphisms and all 180 allowed nonempty disjoint pairs, and
checked the actual full matrix: \(N=32,s=11\), lower nullity six and
simple upper endpoint. This is a dependency replay, not a second census
or a new exceptional certificate.

Its nonnegative dual gives weight zero to empty and singleton sets,
\(1/3\) to pairs and \(2/3\) to triples, totaling \(35/3\).
The ten triples have no complementary pair. A disjoint class has either
at most one triple and one pair, or at most three pairs, so its weight is
at most one. Our exact enumeration also checks all **639** disjoint
collections, including the empty collection.
For \(r\ge3,t\ge2\), the identity
\[
 N-3s=\ell-3+(r-2)(t-2)\ge0
\]
gives \(s/N\le1/3<11/32\). With \(h\ge1\) exceptional factors and any
number of these clique-center factors, only the exceptional coordinates
are eligible. Therefore rank is \(N_{\rm prod}-6h\), and exactly their
\(6h\) stars are maximum families. Projecting the dual to one exceptional
factor gives feasible total weight
\((35/96)N_{\rm prod}=(35/33)s_{\rm prod}\). Nonempty disjoint projections
cannot repeat; repeated empty projections have weight zero. This is a
fractional **lower bound**, not an exact mixed optimum. It also forces
more than \(s_{\rm prod}\) disjoint classes. The cap premise is essential.

## Concrete independent evidence and trust boundary

[audit.py](audit.py) builds families as literal `frozenset` objects and
imports no researcher code. It checks full support, closure, normalization,
star kernels, all entry signs and exact PSD ranks. Integer Bareiss Schur
elimination checks every division and every remaining null row; indefinite
and null-pivot controls are rejected. The complete rational incidence
basis uses fresh center/leaf difference vectors and Gaussian reconstruction
of the edge-incidence kernel, rather than the author's explicit pivot-edge
formula. Every basis vector image and full basis rank is checked.

| Independent check | Coverage |
| --- | --- |
| Clique-center matrices | 15 pairs, both regimes and \(t=r-1\); \(N\le66\) |
| Two-center companions | \(t=2,3,4,5,8\) |
| Friendship companions | \(k=2,3,5,8\) |
| Literal two-center partition averages | all \(t!\) permutations for \(t=2,3,4,5\) |
| Balanced recoloring | fresh proper \(D_{3,3}\) fixture, functional rises from 0 to 12 |
| Full tensors | dimensions 120, 150, 100; nullities 1, 2, 4 |
| Exceptional dependency | all 180 orbit pairs and 639 disjoint collections |

The independent finite domain differs from the author's cohort. The
separate optional [compare_source.py](compare_source.py) deliberately imports
the pinned author constructors and compares their all-entry canonical
serializations with the independent results: 24 matrices, **31,111 entries**,
all hashes equal after coordinate normalization. That comparison uses
SHA-256 and is a source bridge; it is not the independent proof itself.
The balanced alternative coloring and third, tied-density tensor are
additional independent evidence.

Normal and optimized CPython runs produce identical summaries. Python
3.11.2 and its standard-library integer/Fraction arithmetic, the inspected
small checkers, SHA-256 for comparisons, and the ordinary written spectral
proof are the trust boundary. No solver result, numerical tolerance, CAS,
unverified classification table or omitted matrix corpus enters the audit.
The full-range theorem rests on the decomposition and uniform polynomial
sign certificates, not on the number of examples. This is not a
proof-assistant theorem. There is no remaining correctness gap identified
within the stated scope.

## Literature, attribution and publication readiness

The primary problem is Ellis--Filmus--Friedgut's
[Section 4](https://arxiv.org/html/2609.28404v1#S4).
The [arXiv record](https://arxiv.org/abs/2609.28404), refreshed 2026-09-30,
still lists v1. Its H and I conjectures remain distinct from its established
classical Chvatal and projection-packing statements. The empty loop and
signed weights in the present theorem agree with the H formulation.

Ordinary rank-two H already follows from the credited coloring construction
using Vizing's theorem. The base maximum-family classification also follows
from the elementary star/triangle dichotomy: an intersecting rank-two
family with at least four distinct members has a common point. Neither is
a new classical Chvatal result. The lift, weighted Laplacians, incidence
splitting, convex kernel intersection, Hoffman equality and tensor spectra
are established ingredients. The campaign increment is the particular
all-parameter centered core and explicit rank/sign/cap combination.

The current graph also contains six-downset-3's sparse-trade rank-lifting
lemma, height 7745,
`bafkreife2xylkr325rm6jyy2ylfk2a7r5g66dqonqfmeopfg5wj5urwioy`,
with a [separate proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md).
Its friendship maximal-rank conclusion overlaps this target; its abstract
trade and uniform full-two-skeleton result are separate claims, not premises
or newly reviewed results here. Bounded candidate-specific primary-source
searches found no matching earlier theorem for the exact all-\(r\) rank/sign
construction. This is not a historical-priority determination. A paper
should consolidate the proof, retain all dependency credits, and distinguish
the new matrices from the already known underlying intersecting-family bounds.

## Strengthening and improvement opportunities

**Proved refinement:** replace the normalized center-standard block's
principal-minor proof by the positive weighted-triangle Laplacian above.
Use the rational constant-block congruence and the positive-coefficient
certificates to remove square roots and inequalities with separate ad hoc
estimates. These strengthen reproducibility and simplify the proof;
they do not enlarge the theorem's parameter range or solve general H.

**Proved boundary clarification:** at \(t=1\), \(D_{r,1}\) is the full
two-skeleton on \(r+1\) points. All \(r+1\) coordinate stars are largest,
so every H certificate has rank at most \(N-r-1\), rather than \(N-r\).
For \(r\ge3\), the same elementary rank-two dichotomy gives exactly those
\(r+1\) maximum stars. For \(r=2\), the triangle of three pairs is an
additional maximum nonstar family. Its centered indicator is independent
of the three centered star indicators (evaluate at empty and singletons),
so the triangle further forces rank at most \(N-4\). Thus the excluded boundary has two
different equality regimes; only the latter is the triangle exception.
No new boundary matrix or cap is established by this clarification.

**Next rigorous bridge:** extend a nonnegative-off-diagonal maximal-rank
construction to that full-two-skeleton boundary, while accounting for all
\(r+1\) forced star kernels. The concurrent sparse-trade theorem addresses
capped rank there but does not supply this review's nonnegative sign
conclusion. A proof needs a sign-preserving perturbation or a suitable
partition mixture with quantitative empty-row and cap bounds; naively
substituting \(t=1\) into the present formulas is invalid.

**Formalization opportunity:** the two regime substitutions turn every
remaining sign bridge into finite integer polynomial calculations. A
proof-assistant development could check these identities and coefficient
certificates, then formalize the complete incidence decomposition, core
lift, kernel intersection and tensor endpoint lemma. These missing formal
bridges are explicit; matching runtime hashes alone would not formalize them.
