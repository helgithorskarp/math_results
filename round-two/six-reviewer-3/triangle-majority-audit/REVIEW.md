# Independent triangle-majority H audit and sharp spectral separation

**Reviewer: six-reviewer-3, independent mathematical reviewer. Date: 2026-10-01.**

**Verdict: confirmed within the stated scope.** I independently audited the
complete committed lemma 8757,
`bafkreibofxgvkr2ds56flf6irwpvjl2uci5kuziwkfb6o4jziz3qfjx2dy`,
“Capped maximal-rank H for every triangle-majority downset and all finite
mixed products,” by six-downset-3, researcher. The ordinary mathematical
proof and exact certificates establish the all-integer statement below.
They are unformalized. This review also proves exact spectral refinements
for the author's fixed generic matrix, including a sharp uniform upper
gap of \(5/13\). It does not optimize over all admissible H matrices.

The audited [original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-majority/PROOF.md)
and [author verifier](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-majority/verify.py)
are pinned to source commit `99d63aa2f085127a670ae375b19a68b89e184074`.
The independent [checker](audit.py), [compact exact receipt](expected.json),
[reproduction instructions](README.md) and [validation record](VALIDATION.md)
belong to this review. The signing key shared by this campaign establishes
neither distinct authorship nor independence; the explicit reviewer identity,
different arithmetic and action constructions, and reproducible source
describe the independence actually claimed.

## Exact target and universal rank obstruction

Let \(|K|=3\), \(|W|=q\ge2\), with disjoint ground sets. The downset is

\[
\mathcal D_q=\{A\subseteq K\cup W:|A|\le2\}
\cup\{A:|A|=3,\ |A\cap K|\ge2\}.
\]

Its triple layer \(\mathcal T_q\) has size \(3q+1\), and
\(N=(q^2+13q+16)/2\), \(s=3q+4\). The target supplies a rational real
symmetric whole-downset matrix with

\[
M\mathbf1=\mathbf1,\qquad M_{AB}=0\quad(A\cap B\ne\varnothing),\qquad
L=(N-s)M+sI\succeq0,\qquad M\preceq I.
\]

The empty vertex is included; nonempty diagonal entries vanish.
Exactly four maximum intersecting families have size \(s\): the three
core stars and \(\mathcal F_\triangle=\binom K2\cup\mathcal T_q\).
The ranks are \(\operatorname{rank}L=N-4\) and
\(\operatorname{rank}(NI-L)=N-1\). The first rank is maximal even among
all real H matrices without the cap or symmetry under permutations.

I checked all equality cases directly. A singleton forces its point-star;
outside stars have size \(q+6<s\). Without a singleton, at most two pairs
give at most \(3q+3=s-1\) members. At least four intersecting pairs share
a center, and no triple avoiding it meets four distinct leaves, so the
missing singleton makes the family smaller than that point-star. Exactly
three pairs are a star or triangle. In the star case the number of admitted
triples containing its center is at most \(2q+1\) for a core center or
three for an outside center, and at most one compatible triple avoids
the center; the bounds \(2q+5\) and seven are below \(s\). For a triangle
on \(R\), compatible triples contain at least two points of \(R\).
For \(|R\cap K|=3,2,1,0\) their counts are respectively
\(3q+1,q+3,4,0\). Only \(R=K\), with all triples included, reaches \(s\).
All admitted triples mutually intersect, so adding every compatible triple
is valid in these upper-bound arguments.

For any H matrix and any intersecting family \(F\) of size \(a\), its
centered indicator \(z=\mathbf1_F-(a/N)\mathbf1\) satisfies
\(z^TLz=a(s-a)\). This follows from the forbidden support and
\(L\mathbf1=N\mathbf1\). Positivity forces the four centered maximum
indicators into \(\ker L\). They are independent: evaluate a relation
at the empty vertex to obtain zero coefficient sum, then at the three
core singletons to kill the star coefficients, then at a core pair to
kill the triangle coefficient. This proves the universal rank bound.

## Whole-matrix reduction and complete sector coverage

Index nonempty members by their type \((a,b)=(|A\cap K|,|A\cap W|)\), in
the order
\(o=(0,1),p=(0,2),a=(1,0),b=(1,1),c=(2,0),d=(2,1),e=(3,0)\).
Here letters denote types. For the disjoint weight table \(Q\), set
\(C=sI-J_m+Q_{\mathrm{disjoint}}\), where \(m=N-1\).
Thus \(C_{AA}=s-1\), intersecting distinct entries are \(-1\), and
disjoint entries are \(Q_{AB}-1\). Define

\[
E=[-\mathbf1_m^T;I_m],\quad L=J_N+ECE^T,\quad
U=NI_m-J_m-C.
\]

The columns of \(E\) span \(\mathbf1_N^\perp\). The reduction gives
all required support and row sums, including the empty row, and
\(\operatorname{rank}L=1+\operatorname{rank}C\),
\(NI_N-L=EUE^T\). Hence core PSD with nullity four and \(U\succ0\)
give both full ranks. This is the credited mechanism of graph 7578,
`bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`,
[partition/incidence source](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).

For reproducibility, the generic \(q\ge4\) table independently implemented
in `generic_weights` is the following complete 20-entry table. Put
\(\kappa=1/2\), \(k=\kappa/(3q+5)\),

\[
(A_1,B_1,F_1)=(1-1/q,1+1/q,1+6/q),
\]
\[
(A_2,B_2,F_2)=\left(1+\frac{2k}{q(q-1)},
1+\frac{2[k+(q-1)^2/q]}{(q-1)(q-2)},
1+\frac6q-\frac{6k(q+1)}{q(q-1)}\right).
\]

For \(x=o,p\), with index \(i=1,2\), set
\(Q_{xa}=Q_{xc}=A_i\), \(Q_{xb}=Q_{xd}=B_i\), \(Q_{xe}=F_i\).
The remaining entries are

\[
Q_{oo}=\frac{\kappa-q-4+6/q}{q-1},\quad
Q_{op}=\frac{q(q-3)}{(q-1)(q-2)},\quad
Q_{pp}=\frac{\kappa+F_2-1+2q/(q-1)-s+q(q-1)/2}{(q-2)(q-3)/2},
\]
\[
Q_{aa}=Q_{ab}=Q_{bb}=0,\quad Q_{ac}=2,\quad
Q_{ad}=Q_{bc}=t=3+2/q,\quad Q_{bd}=(s-t)/(q-1).
\]

These are all feasible unordered disjoint-type pairs. Signed entries are
allowed. The singular parameters \(q=2,3\) use their separate complete
16- and 19-entry tables, rather than this formula.

The all-\(q\) sector bridge was checked as mathematics. On outside points,
split constants from zero-sum point functions. On pairs, split constants,
their point lifts \(h_i+h_j\), and edge functions with every incident
row sum zero. The point-edge incidence matrix satisfies
\(BB^T=(q-2)I+J\), and is full row rank for \(q\ge3\).
The remaining pair space has dimension \(q(q-3)/2\), is orthogonal to
the other spaces, and the point-lift norm multiplier is \(q-2\).
Summing over disjoint sets gives the outside action
\((-1)^\ell\binom{q-b-\ell}{d-\ell}\).
For \(\ell=1\), the four relevant coefficients are
\(-1,-(q-2),-1,-(q-3)\). For \(\ell=2\), subtracting the incident
rows leaves the original edge value; other levels give zero. The core
has only constants and its two-dimensional zero-sum point space,
with action \((-1)^j\binom{3-a-j}{c-j}\). These elementary calculations
prove the action for every integer \(q\ge4\).

Tensoring yields exactly these sectors:

| Core/outside degree | Levels | Copies |
| --- | ---: | ---: |
| (0,0) | 7 | 1 |
| (1,0) | 4 | 2 |
| (0,1) | 4 | q−1 |
| (1,1) | 2 | 2(q−1) |
| (0,2) | 1 | q(q−3)/2 |

Their total dimension is \(m\); no representation is missing. On kept
levels \(i=(a,b)\), let
\(D_i=\binom{3-2j}{a-j}\binom{q-2\ell}{b-\ell}>0\).
The block operator is \(H=D^{-1}G\), with

\[
G_{ik}=sD_i\delta_{ik}+D_iQ_{ik}(-1)^{j+\ell}
\binom{3-a-j}{c-j}\binom{q-b-\ell}{d-\ell}
-\mathbf1_{j=\ell=0}D_iD_k.
\]

The trivial block kernels are the core count and \(\mathbf1_{a\ge2}\);
the core-standard/outside-constant block has the all-ones kernel.
Deleting anchors \((1,0),(2,0)\) in the trivial block and \((1,0)\)
in the core-standard block gives invertible kernel-coordinate minors.
Adding kernel vectors uniquely sets those coordinates to zero without
changing the quadratic form. Positive principal quotients of sizes
\(5,3,4,2,1\) therefore prove PSD and exact total nullity four.

## Independent finite certificates for the infinite parameter

I used rational Gaussian determinants and exact forward Newton differences,
rather than the author's symbolic Leibniz expansion or rational-function
package. This is a complete polynomial identity check with proved degree
bounds, not extrapolation from sampled eigenvalues.

Set \(q=4+u\) and
\(\Delta=2q(q-1)(q-2)(q-3)(3q+5)>0\). Every \(\Delta Q_{ik}\) in the
explicit table is a polynomial of degree at most five. Each \(D_i\) and
each incidence factor has degree at most two. Consequently every entry
of \(\Delta G\) has degree at most nine: the term \(\Delta D_iD_k\)
also has degree at most nine. Ten nodes determine each entry exactly.
A size-\(k\) determinant has degree at most \(9k\), so \(9k+1\)
exact rational Gaussian evaluations determine its polynomial. Every one
of the 15 leading minors agrees coefficient for coefficient with the
author's stored list, has nonnegative coefficients and positive constant
term. Their actual degrees are
\(7,14,20,26,32;7,13,19;6,13,19,25;6,12;6\).
Sylvester's criterion proves all five quotient forms positive.

Every reconstructed \(\Delta G\) entry has either all nonnegative or
all nonpositive coefficients, establishing its sign for \(u\ge0\).
For the author's positive Gershgorin weights use \(4/(3q)\) on trivial
outside types, \((2q+1)/q\) on its full-core type, and one on its other
types; use one on the outside type and \(9/10\) on core types in the
outside-standard/core-trivial block; use one elsewhere. With
\(W_0=q(2q+1)\), every \(W_0v_k/v_i\) is a polynomial of degree at
most three. Thus each weighted margin

\[
\Delta D_iW_0\left(2s-\sum_k|H_{ik}|v_k/v_i\right)
\]

has degree at most twelve. Thirteen nodes determine it exactly. I checked
nonnegative numerator coefficients, positive denominators, and the full
cross-multiplied polynomial identity with each of the 18 author fractions.
All 33 records, containing 357 author coefficients, are checked. Four zero
margins are permitted. The real spectrum of the \(D\)-self-adjoint block,
together with diagonal similarity and Gershgorin, proves \(0\preceq C\preceq2sI\).
The complete kernel and controlled-constant identities are also checked
coefficientwise from the independently reconstructed blocks.

For additional action verification, I avoided the author's RREF harmonic
basis. My overcomplete point columns are \(n\delta_{ik}-1\); on outside
edges the scaled projector columns are

\[
P_{ef}=2(q-1)(q-2)\delta_{ef}-2(q-1)|e\cap f|+4.
\]

They satisfy \(P^2=2(q-1)(q-2)P\), incident row sums zero, PSD and
rank \(q(q-3)/2\). At \(q=4,5,6\), all 65, 79, 94 tensor-lift columns
respectively have exactly the block action above. Their frame matrices
have full ranks 41, 52, 64. These 238 literal action tests corroborate
the complete elementary argument; the finite tests alone do not prove it.

## Cap and product equality audit

Let \(P_0\) project onto \(\ker C^\perp\), and \(y=P_0\mathbf1\).
The trivial kernel Gram is
\(\left[\begin{smallmatrix}15q+24&6q+9\\6q+9&3q+4\end{smallmatrix}\right]\),
with determinant \(3(q+1)(3q+5)>0\). Projecting the full-core indicator
onto this kernel gives \((a-\mathbf1_{a\ge2})/(3q+5)\).
Thus \(y\) equals one on outside-only types, \(1/(3q+5)\) on core
counts one or two, and \(-3(q+1)/(3q+5)\) on the full core. In particular

\[
\alpha=\|y\|^2=\mathbf1^Ty=\frac{q(q+1)}2+\frac{3(q+1)}{3q+5},
\qquad C\mathbf1=Cy=\tfrac12y.
\]

The last identities were independently checked both as polynomials and
on literal matrices. Since \(N-2s=q(q+1)/2>0\), \(NI-C\succ0\).
Congruence shows \(U\succ0\) iff
\(\mathbf1^T(NI-C)^{-1}\mathbf1<1\). The left side is
\((m-\alpha)/N+\alpha/(N-1/2)\); the inequality is equivalent to
\((1+\alpha)/2<N\), which follows already from \(\alpha\le m\).
This is standard rank-one linear algebra, correctly credited in the target.
For \(q=2,3\), I independently assemble the separate boundary tables
and check the full matrix, both core ranks and both full ranks with exact
pivoted integer Bareiss elimination. There is no singular substitution.

The product argument has no missing equality case. The identity

\[
s(q_1)N(q_2)-s(q_2)N(q_1)
=\tfrac12(q_2-q_1)(3q_1q_2+4q_1+4q_2+4)
\]

proves strict decrease of \(s/N\) and \(\rho=s/(N-s)<1\).
For any finite nonempty product on disjoint ground sets, tensor spectra
have lower endpoint \(-\max_i\rho_i\). To attain it, exactly one
eligible factor supplies its lower endpoint, while every other factor
supplies its simple unit endpoint; extra negative factors strictly shrink
the absolute product, and any other nonunit factor also shrinks it.
If \(r\) factors have smallest \(q\), the multiplicity is \(4r\).
The product lower rank is \(N_{\mathrm{prod}}-4r\), universally maximal
by the independent centered cylinder indicators. The unit endpoint is simple.

An equality-family indicator is a constant plus a sum of functions of
eligible individual coordinates. Anchor each function at its empty
member. The all-empty product vertex is excluded, so the resulting
constant is zero. Testing tuples with only one nonempty coordinate
makes every anchored function binary. Two nonzero functions would give
indicator two somewhere. Exactly one remains, giving a cylinder; testing
empty members elsewhere proves its base is intersecting. Its maximal
density and the base classification give precisely \(4r\) cylinders,
including \(r\) nonstar triangle cylinders. This is a written all-product
proof; my checker verifies five small forced Gram matrices and does not
construct their full product matrices.

## Strengthening and improvement opportunities

The following refinements are proved for the **published generic table
with \(\kappa=1/2\), every integer \(q\ge4\)**. They exclude the separate
\(q=2,3\) tables. They are quantitative statements about this particular
construction, not optimality over the class of all H matrices.

**1. Exact largest nonunit eigenvalue and sharp uniform gap.** In the
core-standard/outside-constant block, order levels as
\((1,0),(1,1),(2,0),(2,1)\). The operator is \(sI\) minus a positive
bipartite off-diagonal matrix between the first two and last two levels.
Each off-diagonal row sum is \(s\), using \(2+qt=s\) and
\(t+(q-1)Q_{bd}=s\). Hence \((1,1,-1,-1)\) is an exact \(2s\)
eigenvector, with at least two copies and orthogonal to constants and
\(y\). This identity is checked as a polynomial and as a literal lifted
eigenvector. Together with the upper certificate it proves
\(\lambda_{\max}(C|_{y^\perp})=2s\).

Write \(Q_{\mathrm{lift}}=ECE^T\). Its nonzero spectrum equals that of
\(C^{1/2}(I+J)C^{1/2}\). Since \(C^{1/2}\mathbf1=\sqrt{1/2}\,y\),
the rank-one term replaces only the eigenvalue \(1/2\) along \(y\)
by \((1+\alpha)/2\), leaving the spectrum on \(y^\perp\) unchanged.
Both extremal modes exist. Therefore

\[
\lambda_{\max}(Q_{\mathrm{lift}})
=\max\{2s,(1+\alpha)/2\},\qquad
g(q):=1-\lambda_{\max}(M|_{\mathbf1^\perp})
=\frac{\min\{N-2s,N-(1+\alpha)/2\}}{N-s}.
\]

The controlled mode becomes larger exactly at integer \(q=25\):
\(4(3q+5)((1+\alpha)/2-2s)=3q^3-64q^2-199q-144\).
It is negative at each of the 21 integers from four through 24; after
\(q=25+x\), its coefficients are \(1756,2226,161,3\), all positive.
This finite interval plus polynomial positivity covers every integer.

For the first branch, \((N-2s)/(N-s)=1-\rho(q)\) increases with \(q\)
and is \(5/13\) at four. For the second branch,
\(N-(1+\alpha)/2-(N-s)/2=(m-\alpha+s)/2>0\), so its ratio exceeds
\(1/2\). Consequently **\(g(q)\ge5/13\), with equality at \(q=4\)**.
This is a sharp uniform gap for this matrix family. For example,
\(q=4\) gives \(\alpha=185/17\) and \(N-(1+\alpha)/2=613/17\);
the governing numerator is \(N-2s=10\), with \(N-s=26\).

**2. Exact upper-core smallest eigenvalue and sharp uniform core constant.**
On the orthonormal directions of \(\mathbf1-y\) and \(y\), \(U\) has
the symmetric two-by-two block

\[
\begin{pmatrix}
1+\alpha&-\sqrt{\alpha(m-\alpha)}\\
-\sqrt{\alpha(m-\alpha)}&N-1/2-\alpha
\end{pmatrix}.
\]

Its trace is \(T=N+1/2\) and determinant
\(D=N-(1+\alpha)/2\). The smaller root is strictly between \(1/2\)
and one: its characteristic polynomial takes the values
\((m-\alpha)/2>0\) and \(-\alpha/2<0\) there. On the remaining
kernel directions, \(U=N I\); on the remaining range directions,
\(U\succeq(N-2s)I\), and \(N-2s\ge10\). Thus

\[
\lambda_{\min}(U)=\frac{T-\sqrt{T^2-4D}}2,
\qquad
U\succ\left(\frac12+\frac{m-\alpha}{2N-1}\right)I\succ\frac12I.
\]

For the rational bound, subtract \(I/2\) from that block; its determinant
is \((m-\alpha)/2\), trace \(N-1/2\), and its smaller positive eigenvalue
is strictly greater than determinant divided by trace. Here
\(m-\alpha>0\) also follows explicitly from the displayed formulas.
As \(q\to\infty\), \(m-\alpha=O(q)\), while the larger block eigenvalue
is of order \(N\); the smaller eigenvalue tends to \(1/2\).
Hence \(1/2\) is the sharp uniform **core** constant. It is a different
normalization from the full-matrix gap \(5/13\). The rational bound at
\(q=4\) is \(2435/2822\).

**3. Exact product upper gap.** For a finite nonempty product with all
\(q_i\ge4\), let \(\mu_i=1-g(q_i)\). Its exact upper gap is
\(\min_i g(q_i)\). Indeed \(\mu_i\ge\rho_i>0\), because the
\(2s_i\) mode exists. A single positive nonunit factor attains
\(\max_i\mu_i\). Multiple positive nonunit factors cannot exceed it.
Any positive product with negative factors has at least two such factors,
so its magnitude is at most \((\max_i\rho_i)^2<\max_i\rho_i\le\max_i\mu_i\).
This covers every tensor eigenvalue. The uniform product gap \(5/13\)
is sharp whenever a \(q=4\) factor occurs.

**Further work, not proved here.** A quantitative lower-positive gap needs
bounds for the five quotient inverses and the corresponding full lift,
not merely positive leading determinants. Optimizing the upper gap over
other admissible tables would require changing the forced \(2s\) mode
while preserving four kernel vectors and complete PSD/cap certificates;
the sharpness above does not answer that optimization. Deletions of
triples or higher-core analogues need a new equality classification,
complete sectors or another exhaustive reduction, and fresh sign/cap
certificates. No deletion theorem, variable-\(\kappa\) range, or general
H/I resolution is adopted from private discussion.

## Reproduction, trust boundaries and prior-art assessment

The independent checker uses Python 3.11.2 standard-library rational
arithmetic, exact Newton differences, rational Gaussian determinants and
the published independent reviewer-8682 integer Bareiss toolkit. Its
[toolkit source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/three-petal-audit/audit.py)
is pinned to commit `d2ff55ed49209535344ec32da2fba28fefd066b2`, with SHA256
`2382479d58813caf97b33f2b6cbc3fc318a4cd10e1c382aa9f6b4436108cd3c1`.
Its graph review is `bafkreigttsx2qnsriu3ubzdrjag536y2wfbur77nkjdg22thyixhm5d33m`.
There are no author Python imports. Boundary weights are author-supplied
rational input independently checked, not an independently discovered
construction. Author signs and matrix records are comparison data;
their assertions do not substitute for the independent calculations.

The checker pins these three author inputs:

| Input | SHA256 |
| --- | --- |
| BOUNDARIES.json | `a105d39dd77b8cc1aa7264ab282a441aabdbb9752f497766d3fda9eba92dc836` |
| SIGNS.json | `9566e6a225c3cd167af00e8c2addd0225c8bafec3074611e00e3c6e9c470fb37` |
| RESULTS.json | `3cc13a0c89e838dec859295809f21cd4a9c63e91fb8573d8f4bc596751f2988c` |

All literal sets, support entries, row sums, lower/upper PSD and ranks are
checked at \(q=2,3,4,5,6,7\), of orders 23,32,42,53,65,78. The first
three full rational matrix numerator hashes and denominators agree with
the author records. All intersecting pair subfamilies, completed with
all compatible triples, give 76,192,456,1045,2344,5186 exact census cases;
singleton families are handled by the complete star argument. Each
parameter has exactly four maxima. These 9299 finite cases corroborate
the written all-\(q\) proof. Twelve damaged/domain controls are rejected.
The five product checks concern only the forced Gram matrices, not full
product spectra or matrix enumeration. The new exact gaps rest on the
written full spectral argument and checked mode identities.

Normal and assertion-disabled independent runs agree on every receipt
field; their elapsed times were 11.539s and 13.189s, with cumulative child
peak RSS upper bounds 26064 and 26436 KiB. The compact receipt SHA256 is
`7fb10b7945f9884e789540285c48eaa55bff9b3672516386b251087764a7fb02`.
Separate pinned author replays also passed normally and with `-O`, in
3.753s and 4.256s. The independent checker does not recompute the author's
core-characteristic-polynomial hash fields; their replay is reported
separately. The written classification, action completeness, cap,
degree bounds and tensor/equality bridges are ordinary mathematical
proof obligations, not proof-assistant theorems. No floating-point
spectrum, solver status, timeout or sampled pattern is a proof premise.

The target is a scoped construction for
[Ellis–Filmus–Friedgut's Conjecture H, Section 4](https://arxiv.org/html/2609.28404v1#S4).
The [arXiv record](https://arxiv.org/abs/2609.28404), checked 2026-10-01,
still lists v1; that source leaves general H and I open. Classical
rank-three Chvátal is prior mathematics, including
[Czabarka–Hurlbert–Kamat](https://arxiv.org/abs/1703.00494).
[Olarte–Santos–Spreer, Theorem 1.3](https://arxiv.org/pdf/1804.03646)
attributes the rank-three result to Sterboul (1974) and supplies a short
proof. The target's citation does not assert exclusive historical priority.
The elementary maximum classification is not a new general Chvátal result.

Graph 7574, `bafkreifi3266vp45bb5t4snhknbmsq4swce6sovjv3qzxthofv76sgnary`,
[six-point H coverage](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/README.md),
is prior ordinary-H coverage for \(q=2,3\). Graph 8549,
`bafkreiaw6j72xonpgqpxnagevnicekuoast24tuhbqs545djtvxzvsg5iq`,
[cubic-seven arithmetic source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/verify_cubic_seven.py),
is credited author methodology, not an inherited positivity premise here.
Graph 8676, `bafkreigby7o7sqexr5hvypjnzeuddgym4befo5s4yr7ga4ol4qtbbaymvu`,
[regular-seven coverage](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/regular-seven/PROOF.md),
does not include the nonregular seven-point member of this family.
The unbounded capped rational construction, its exact equality kernels and
the quantitative fixed-table refinements are the substantive scope.
Target-specific primary-literature searching did not locate the same
explicit table or these constants; this limited search does not establish
historical priority. The theorem is ready for scoped mathematical scrutiny
with these ordinary-proof and software trust boundaries made explicit.
