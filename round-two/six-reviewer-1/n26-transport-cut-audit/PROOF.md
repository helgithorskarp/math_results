# Independent original-matrix proof and quantitative consequences

Reviewer: **six-reviewer-1**, independent mathematical reviewer. This is an
ordinary proof with exact integer/rational checks, **unformalized**. The signed
written proof and its full declarative certificate were read before this work;
this is **not a blind review**. The new n26 author's executable, expected output
and file-based certificate remained unopened while this proof and the fresh
primary implementation were developed and sealed. The old n24 source and this
reviewer's prior n24 audit were already exposed and are explicitly credited.

The target is LEMMA10123/0,
`bafkreiawt46t5wd53jy2pbrf2766y46z4nvobajdi7bkio4il5gbryumz4`,
“Original rank-nine PSD cut excludes every deficit-only repair of the n26
normalized transport”, explicitly authored by six-downset-2 / researcher.
The exact defining integer directions, positive weights, 30 rational values and
36 cut coefficients are in [INPUT.json](INPUT.json). They are copied from the
complete signed body, not obtained by running the author's code. The complete
credited old n24 defining data are in [N24_INPUT.json](N24_INPUT.json).

## Original domain, support and all real parameters

Let \(\mathcal D=\{A\subseteq[26]:|A|\le24\}\), with its actual empty
vertex. Its size, point-star size and complement are
\[
 N=67108837,\quad s=33554406,\quad h=N-s=33554431.
\]
There are six **independent real** variables \(d_8,\ldots,d_{13}\), and
30 independent real variables \(t_{ab}\), one for every
\(8\le a\le b\le18\) with \(a+b<26\). No rationality, nonnegativity,
upper cap, centering, rank requirement or bounded box is assumed.

Define symmetric coefficients \(B_{ab}\), \(1\le a,b\le24\).
For \(2\le a\le7\), set \(B_{a,26-a}=s\). For \(8\le a\le13\),
set \(B_{a,26-a}=s-d_a\), and set all symmetric partners equally.
Set \(B_{ab}=t_{ab}\) for the 30 proper labels above. Every other
nonsingleton coefficient is zero. Recover the singleton coefficients by
\[
 B_{1a}=B_{a1}=s-\sum_{b=2}^{24}\binom{25-a}{b-1}B_{ab}\quad(2\le a\le24),
 \qquad B_{11}=s-\sum_{b=2}^{24}\binom{24}{b-1}B_{1b}.
\]
A binomial coefficient outside its usual integer range is zero. Define
\[
 e_a=h-\sum_{b=1}^{24}\binom{26-a}{b}B_{ab},\qquad
 \ell=N-\sum_{a=1}^{24}\binom{26}{a}e_a.
\]
The original matrix \(L\), indexed by actual sets, has nonempty diagonal
\(s\), entry \(B_{|A|,|T|}\) at distinct nonempty disjoint sets, zero at
intersecting distinct sets, actual empty entry \(L_{\emptyset,A}=e_{|A|}\)
and actual empty loop \(L_{\emptyset,\emptyset}=\ell\).
This specifies all original entries for every one of the 36 real parameters.

Every nonempty row sums to \(s+e_a+\sum_b\binom{26-a}{b}B_{ab}=N\).
The empty row sums to \(N\) by its definition. For a point-star
\(S_p=\{A:p\in A\}\), a nonempty set containing \(p\) receives only
its diagonal \(s\). A nonempty set of size \(a\) not containing \(p\)
receives \(\sum_b\binom{25-a}{b-1}B_{ab}=s\), exactly the singleton
recovery equation. The empty-star identity also holds, rather than being
silently deleted. In fact \(\sum_b\binom{25}{b-1}=s\) over \(1\le b\le24\).
The \(h-1\) nonempty original sets avoiding \(p\) each receive total \(s\)
on \(S_p\); summing these entries in the opposite order gives
\(\sum_{a,b}\binom{25}{a-1}\binom{26-a}{b}B_{ab}=s(h-1)\).
Hence \(\sum_a\binom{25}{a-1}e_a=hs-s(h-1)=s\).
Thus \(L1=N1\) and \(L1_{S_p}=s1\) for every actual point.
The checker verifies these equalities as complete 37-component affine vectors.

The associated \(M=(L-sI)/h\) is real symmetric, supported on disjoint
original sets, has row sum 1, and retains the permitted empty loop. Within
this declared face the H lower requirement is precisely \(L\succeq0\).
The following proof excludes a particular slice of this face; it neither
assumes nor proves that the face exhausts all n26 H matrices.

## Two counted energies and nine original directions

For any fixed layer profile \(z=(z_1,\ldots,z_{24})\), set
\[
 F_z(\emptyset)=0,\qquad
 F_z(A)=z_{|A|}(1_{1\in A}-1_{2\in A}).
\]
There are \(2\binom{24}{a-1}\) size-a sets with nonzero signed indicator.
For disjoint ordered size-a and size-b sets, the two distinguished points
must be on opposite sides to contribute. Each orientation has
\(\binom{24}{a-1}\binom{25-a}{b-1}\) pairs, all with sign -1. Therefore
\[
 E_z=F_z^TLF_z
 =2s\sum_a\binom{24}{a-1}z_a^2
 -2\sum_{a,b}B_{ab}\binom{24}{a-1}\binom{25-a}{b-1}z_az_b. \tag{1}
\]
The empty row is retained in \(L\); it contributes zero only to these
specific vectors. Separately the original empty-indicator energy is \(\ell\).
The second implementation sums unordered layer pairs, using
\(24!/((a-1)!(b-1)!(26-a-b)!)\) and factors -4 when \(a\ne b\),
-2 when \(a=b\). It matches every affine coefficient of (1).

Use the target's fixed profiles
\[
 u=(0,0,0,0,0,0,0,525,-533,-538,541,1,-26,1,541,-538,-533,525,0,0,0,0,0,0),
\]
\[
 v=(3,0,0,0,0,0,0,0,0,0,0,7,7,7,0,0,0,0,0,0,0,0,0,0).
\]
Let \(A_i=\{1,\ldots,i\}\), \(T_i=[26]\setminus A_i\), and
\(H_i=1_{A_i}-1_{T_i}\) for \(8\le i\le13\), where these are single
original vertex indicators. All 12 vertices belong to \(\mathcal D\)
and \(A_i\ne T_i\), including \(i=13\). Consequently
\(H_i^TLH_i=2(s-B_{i,26-i})=2d_i\) and \(\|H_i\|^2=2\).
With \(\mu=42186\), \(w=2518\), and
\[
 (\lambda_8,\ldots,\lambda_{13})=
 (14519995358,30698088454,55869155606,86305367440,107807092424,58518767888),
\]
define
\[
 Y=F_uF_u^T+\mu F_vF_v^T+w1_{\emptyset}1_{\emptyset}^T
   +\sum_{i=8}^{13}\lambda_iH_iH_i^T. \tag{2}
\]
All weights are positive, so \(Y\succeq0\) for all real parameters.
The nine columns \((F_u,F_v,1_{\emptyset},H_8,\ldots,H_{13})\)
at original rows
\(\emptyset,\{1\},\{1,3,4,5,6,7,8,9\},A_8,\ldots,A_{13}\)
have first 3 by 3 block
\[
 \begin{pmatrix}0&0&1\\0&3&0\\525&0&0\end{pmatrix},
\]
zero upper-right block and identity 6 by 6 lower-right block. The determinant
is -1575. Thus these original columns are independent, and (2) has
**rank exactly nine**. This uses neither harmonic rank claims nor floating
rank thresholds.

## Complete affine cancellation and fixed-slice exclusion

Every entry above is affine in exactly 36 real coordinates. Checking the
constant term and all 36 coefficients therefore proves an identity on the
entire real face, not merely at feasible probes. The fresh implementation
constructs all 625 coefficient-table cells as 37-component integer vectors,
and compares every one against a second numeric recovery at the zero point
and each coordinate unit point. It separately compares all empty entries
and the loop, and both full energy vectors. No external executable is a
premise of this reasoning.

From (1), (2) and the exact data, all six deficit coefficients cancel:
\[
 \operatorname{tr}(YL)=E_u+42186E_v+2518\ell+
             2\sum_{i=8}^{13}\lambda_i d_i
 =P(t)=48666235273558+\sum_{(a,b)}K_{ab}t_{ab}. \tag{3}
\]
All 30 integers \(K_{ab}\) are the last 30 entries of
`full36_affine_cut_coefficients` in INPUT.json; the first six entries are zero.
The checker compares all 37 coefficients of (3), not its value at one point.
For example the six deficit coefficients of \(E_u\), \(E_v\), \(\ell\)
respectively are

| i | coefficient in E_u | coefficient in E_v | coefficient in ell |
|---|---:|---:|---:|
| 8 | 381579660000 | 12459744 | -371821450 |
| 9 | 835756883676 | 26476956 | -799884800 |
| 10 | 1513796751104 | 47070144 | -1434168450 |
| 11 | 2296089469344 | 70605216 | -2163324800 |
| 12 | 9984576 | 159753216 | -2762102200 |
| 13 | 3656018912 | 86532992 | -1497686400 |

Each row satisfies \(E_{u,i}+42186E_{v,i}+2518\ell_i+2\lambda_i=0\).
For any \(L\succeq0\), all nine original quadratic forms in (2) are
nonnegative, and (3) implies \(P(t)\ge0\).

The credited old n24 data give 30 proper values \(t^{24}_{ab}\).
Define
\[
 \sigma_n(a,b)=\frac{n}{\max\{\binom{n-a-1}{b-1},\binom{n-b-1}{a-1}\}},
 \qquad
 t^0_{a+1,b+1}=t^{24}_{ab}\frac{\sigma_{26}(a+1,b+1)}{\sigma_{24}(a,b)}.
\]
The exact complete old names map to the 30 new names, and all 30 resulting
rational values agree with `fixed_transported_proper_values`. Direct exact
substitution in the *whole* cut gives
\[
 P_0=P(t^0)=-\frac{274356636025866281341291}{98175000000}<0. \tag{4}
\]
It is independent of **every real choice** of \(d_8,\ldots,d_{13}\).
Equations (2)–(4) prove that no deficit-only repair of this fixed transported
slice is PSD, even without an upper cap. This is an exact obstruction, not
an inference from a solver timeout or a negative floating objective.

## Strengthening and improvement opportunities

The following two quantitative consequences are **proved here** with the
same original Y. They measure this fixed slice and this declared face.
They do not assert optimality or feasibility elsewhere.

First the original norms in (2), including the actual empty direction, give
\[
 \tau=\operatorname{tr}Y=37557180749050,
 \qquad
 \rho=-P_0/\tau
 =\frac{274356636025866281341291}{3687176220037983750000000}>0.
\]
For every real deficit vector on the fixed slice,
\[
 \lambda_{\min}(L)\le-\rho,
 \qquad
 \lambda_{\min}(M)\le-\frac{s+\rho}{h}. \tag{5}
\]
Indeed (3) is a positive weighted sum of nine Rayleigh numerators whose
weighted squared norms sum to \(\tau\). At least one of these nine
Rayleigh quotients is at most \(P_0/\tau\); the least eigenvalue is at most
that quotient. This also supplies a negative original direction without
assembling or diagonalizing the 67-million-vertex matrix. Orthogonality of
the directions is not required.

Second write normalized proper coordinates
\(\beta_{ab}=t_{ab}/\sigma_{26}(a,b)\),
\(\beta^0_{ab}=t^0_{ab}/\sigma_{26}(a,b)\). The exact positive coefficient
norm is
\[
 W=\sum_{(a,b)}|K_{ab}|\sigma_{26}(a,b)
   =\frac{22977599721932867752}{11781}.
\]
For **any PSD matrix within this whole 36-real face**, with arbitrary
six real deficits, (3) and the triangle inequality imply
\[
 -P_0\le P(t)-P_0
 \le W\|\beta-\beta^0\|_\infty,
\]
and hence
\[
 \|\beta-\beta^0\|_\infty\ge
 \Gamma=\frac{823069908077598844023873}{574439993048321693800000000}>0. \tag{6}
\]
This is a necessary quantitative minimum motion of at least one normalized
proper coefficient, not a sufficient repair or an optimal distance.
Both rational denominators and numerators are regenerated independently.

The substantial remaining direction is actual rational recovery with all 30
proper entries allowed to move, retaining the original empty row and all
original PSD and upper-cap constraints. Passing this cut or satisfying (6)
is only necessary. Neither minimum-five-class attainment at n26, the full
36-real face's feasibility, arbitrary transports, nor general Conjectures
H or I is settled. Other faces require a new certificate or a proved
reduction before this exclusion can be carried over. Optimizing a stronger
cut or sharp repair distance requires additional rigorous dual/primal
matching, not another deficit-only numerical search at these fixed entries.

## Literal controls, trust boundary and literature scope

The separate fresh bit-set program retains every vertex of
\(\mathcal D_7\) and \(\mathcal D_9\): 120 and 502 vertices.
It uses arbitrary signed rational nonsingleton coefficients, followed by
independently written star recovery. These are **not PSD/H witnesses**.
A predicate-based full matrix and a complement-subset adjacency construction
are compared at all 14,400 and 252,004 positions. Every row, every point-star
including the empty row, every supported zero, two whole quadratic forms,
their norms, all original complement differences and the actual empty loop
are checked. Matrix hashes are computed only after these entire comparisons.
The n26 proof follows the explicit counting and affine identities above,
not extrapolation from these finite controls.

The primary trust boundary is ordinary mathematical reasoning, fresh Python
integer/Fraction arithmetic and its runtime, plus the explicitly attributed
signed input values. There is no solver, floating arithmetic, numerical
PSD/rank decision, harmonic decoder, external executable import or proof
assistant axiom claim in the primary argument. Fresh normal and optimized
runs and semantic damaged-input controls are reproducibility checks.

Ellis–Filmus–Friedgut's original paper
[arXiv:2609.28404v1, Section 4](https://arxiv.org/html/2609.28404v1#S4)
proposes distinct weighted-Hoffman and inertia conjectures. Its loop-aware
weighted matrix definition permits the empty vertex and signed supported
entries. The published intersecting-family theorem does not supply the
present H matrix or an H/I resolution. The explicit n24 source and the
n26 target are campaign prior art; PSD outer products, Rayleigh quotients
and the coefficient-norm bound are classical tools. This review credits
the author's certificate and does not claim its discovery or historical
priority. Candidate-specific exact-constant searches are bounded evidence,
not an exhaustive priority determination.
