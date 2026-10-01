# Equal-load pendant closure at distinct Boolean-cube marks

Actual author: **six-downset-1**, role **researcher**, round two,
2026-10-01. Status: complete author-checked ordinary proof with exact
rational validation; unformalized and independently unreviewed. General
spectral Chvatal H and I remain open.

## 1. Quantified result and prior scope

Let X have n>=2 coordinates and let x_1,...,x_r be distinct members,
2<=r<=n. At each mark attach d>=2 fresh coordinates a_(i,k), all
distinct. Let

\[
 D=2^X\cup\bigcup_{i=1}^r\bigcup_{k=1}^d
     \{\{a_{i,k}\},\{a_{i,k},x_i\}\},\quad
 q=2^{n-1},\quad m=rd,\quad N=2q+2m,\quad s=q+d.
\]

There is an explicit rational symmetric matrix M on every member,
including the empty set, satisfying

\[
 M\mathbf1=\mathbf1,\quad M_{AB}=0\ (A\cap B\ne\varnothing),\quad
 L=(N-s)M+sI\succeq0,\quad M\preceq I.
\]

It attains the universally greatest lower rank N-r and upper rank N-1.
The only maximum intersecting families are the r marked stars. Its
negative endpoint has multiplicity r, its unit eigenvalue is simple,
and every nonunit eigenvalue lies in

\[
 \left[-\frac{q+d}{q+(2r-1)d},\quad
 1-\frac2{3[q+(2r-1)d]}\right].                                  \tag{1}
\]

Finite products of these strict factors have the credited maximal-rank
and eligible marked-star cylinder description in Section7.

The [distinct-mark result8863](ALL_MARKS.md) covers d=1. Together these
give capped maximal-rank H for every equal positive load at distinct
cube marks. The new step is the unbounded repeated-load construction
d>=2, rather than a finite enlargement of the d=1 tests. The singleton
correction now uses the full centered spoke, including within-mark
simplex directions; this avoids quadratic energy in d from using only
the old marked-difference directions.

The core/lift and conditional tensor principle are credited to
[structural result7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
The forced-star rank and trace mixture are credited to
[two-facet result8579](UNEQUAL_FACETS.md), [two-mark result8788](TWO_MARKED_CUBE.md),
and8863. Cube complementary-pair structure is credited to8020 and
its full-cube audit8066. The present proof supplies the new equal-load
Gram construction and every missing full-frame estimate explicitly.

[Balanced single-pendant completion8424](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/BALANCED_PENDANT_COMPLETION.md)
already permits repeated pendants at the same maximum-star mark.
After the first distinct attachment an unmarked old coordinate has a
smaller star, so that result does not iterate to equal loads at several
distinct marks. Small ordinary rank-two H existence is also prior art;
we make no first-existence or historical priority claim for such cases.

The primary problem conventions are
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4),
including an allowed empty loop and signed weights. The
[arXiv record](https://arxiv.org/abs/2609.28404) was rechecked on
2026-10-01 and still lists only v1 of2026-09-23. Ordinary Chvatal's
conjecture is proved in that literature; the assigned spectral H/I
conjectures are the open targets. No review of a predecessor is a
review of this new statement.

## 2. Family structure, forced rank, and full lift

Marked stars have q+d members, unmarked old stars q, and fresh stars2.
A family with a fresh singleton has size at most2. Spokes at different
marks are disjoint, so an intersecting family can contain spokes from
only one mark, at most d of them. Its old members must then all contain
that mark, giving at most q+d. Equality forces exactly that entire
marked star. With no spokes, complementary old cube pairs bound the
size by q. Since s>=4, the r marked stars are exactly all maximum
intersecting families.

For every real H certificate, including one without a cap, the centered
indicator of every intersecting s-member family is killed by L:
its lower quadratic form is zero, and L is PSD. The r centered marked
star indicators are independent, using first the empty coordinate and
then one unique spoke at each mark. Hence every H matrix has
rank L<=N-r. This proves the universal rank target without assuming
symmetry or nonnegative entries.

Write w=s-1=q+d-1. For a PSD core C on the nonempty vertices, with
diagonal w and entries -1 on intersecting pairs, take

\[
 T_0=\begin{pmatrix}-\mathbf1^T\\I\end{pmatrix},\quad
 Q=T_0CT_0^T,\quad J=\mathbf1\mathbf1^T,\quad P_N=I-J/N,\quad
 M=(Q+J-sI)/(N-s).
\]

Then Q1=0, M1=1, the support constraints hold, and

\[
 L=Q+J,\quad\operatorname{rank}L=1+\operatorname{rank}C,\quad
 (N-s)(I-M)=NP_N-Q.                                               \tag{2}
\]

In Gram language the empty vector is the negative total nonempty
vector sum. The nonzero eigenvalues of Q agree with those of the
**full** frame, including this empty vector. All cap estimates below
apply to that frame; no unlifted core norm is substituted for it.

## 3. Old core, spoke splitting, and rational singleton completion

On old nonempty cube members let P exchange the proper complementary
pairs and have zero full-set row. Use

\[
 C_d=(q-d)P+(q+d)I-J.                                             \tag{3}
\]

It has diagonal w and intersecting entries -1. Its pair-antisymmetric
eigenvalue is2d (dimension q-1), its pair-symmetric zero-sum eigenvalue
is2q (dimension q-2), and the remaining orthonormal plane is

\[
 \begin{pmatrix}2&-\sqrt{2q-2}\\-\sqrt{2q-2}&w\end{pmatrix}.
\]

The latter has positive trace and determinant2d, so C_d is PD of
rank2q-1. This remains true for d>q, when its allowed complementary
coefficient q-d is negative.

Let g_A be old Gram vectors; put G=sum_{old nonempty}g_A, F=g_X,
and H_i=-sum_{A containing x_i}g_A. Direct complementary-pair counts
give

\[
 \|G\|^2=\|F\|^2=w,\quad G\cdot F=d+1-q,\quad
 \|H_i\|^2=qd,\quad H_i\cdot H_j=0\ (i\ne j),\quad
 G\cdot H_i=F\cdot H_i=-d.                                       \tag{4}
\]

Also H_i dot g_A=-d if A contains x_i, and +d for a proper old
nonempty A excluding x_i. Define h_0=-(G+F)/2, G_perp=G+h_0,
A_i=H_i-h_0, Z=sum_i A_i/r, and delta_i=H_i-sum_j H_j/r.
Then G_perp,h_0,Z are orthogonal, with squared norms

\[
 q-1,\quad d,\quad z=d(q-r)/r,
\]

and the A_i Gram matrix is d(qI_r-J_r). For n>=3, q>=r+1;
when n=r=q=2, Z=0 and its direction is omitted.

In fresh mutually orthogonal within-mark spaces take T_(i,k) with

\[
 T_{i,k}\cdot T_{i,l}=(q+d)\mathbf1_{k=l}-(q/d+1),\qquad
 \sum_k T_{i,k}=0.
\]

These are regular simplices of dimension d-1, orthogonal to all old
vectors and to the other marks' simplices. Assign spokes

\[
 S_{i,k}=H_i/d+T_{i,k}.                                          \tag{5}
\]

Their diagonal is w, same-mark cross inner products are -1, and
old intersecting pairs have inner product -1. Different-mark spokes
have inner product0, an allowed value. Their sum at mark i is H_i,
so every marked-star vector sum is zero, as required.

Let H=sum_i H_i=sum_{i,k}S_(i,k), K=G+H, and center the spokes by
V_(i,k)=S_(i,k)-H/m. Formula(4) gives

\[
 \|K\|^2=B=(m+1)q+d-1-2m,\quad K\cdot S_{i,k}=q-1,\quad
 K\cdot V_{i,k}=0,\quad
 \|V_{i,k}\|^2=V_{i,k}\cdot S_{i,k}=\ell=w-q/m>0.
\]

The centered-spoke Gram matrix has eigenvalue q on the r-1 directions
constant within marks and summing to zero over marks, and q+d on the
m-r within-mark zero-sum directions. Its constant direction is zero.
Choose

\[
 c=\frac{q-m-2}{(m+1)\ell},\qquad
 \eta=w-\frac B{(m+1)^2}-c^2\ell.                                 \tag{6}
\]

The residual is strictly positive. In fact

\[
 (m+1)^2\ell\eta=
 (m^2-2)q^2+[2(m^2+m-1)(d-1)+4m+2]q
 +m(m+2)(d-1)^2+2m(d-1)-(m+2)^2.                                \tag{7}
\]

For d>=2 the last line is at least -4, its value at d=2. Since
m>=4,q>=2, the quadratic term alone is at least56, and the q-term
is positive. This proves eta>0 for all parameters, not by sampling.
The checker reconstructs the identity formally and its positive
coefficients after q=Q+2,m=M+4,d=D+2.

In another orthogonal (m-1)-space choose a global regular simplex W_u,
where u=(i,k), with norm squared eta, cross inner product -eta/(m-1),
and sum zero. Assign singleton vectors

\[
 U_u=-K/(m+1)+cV_u+W_u.                                          \tag{8}
\]

They have norm squared w. Their only mandatory intersection is their
own spoke, and

\[
 U_u\cdot S_u=-\frac{q-1}{m+1}+c\ell=-1.
\]

All vectors have rational Gram entries; no square roots need be
evaluated to construct the core. The total nonempty sum is K/(m+1),
so the actual empty vector is -K/(m+1). The full seed frame is

\[
 F_Q=F_0+\sum_u S_uS_u^*+\frac{KK^*}{m+1}
                  +\sum_u(cV_u+W_u)(cV_u+W_u)^*,                 \tag{9}
\]

where F_0 is the old frame. In particular the common-vector term
includes all singleton means **and the empty-vector energy**.

## 4. Every sector and the symmetric cap

The old frame actions are

\[
 F_0h_0=d(G_\perp+h_0),\quad
 F_0G_\perp=(q+1)G_\perp+(q-1)h_0,\quad F_0Z=2dZ.
\]

The complete seed Gram span splits as follows for n>=3:

| Sector | Dimension | Frame |
| --- | ---: | --- |
| G_perp,h_0,Z | 3 | F_sym |
| between-mark standard directions, paired with W | 2(r-1) | copies of F_between |
| within-mark standard directions, paired with W | 2r(d-1) | copies of F_within |
| untouched old pair-symmetric directions | q-2 | 2q |
| untouched old pair-antisymmetric directions | q-r-1 | 2d |

The dimensions sum to N-r-2. The W simplex realizes the same
between/within orthogonal decomposition of zero-sum functions on the
m spoke indices. Thus the pairing accounts for every new W direction;
the table is an exhaustion, rather than a selected compression.
For n=r=q=2, Z is absent, there are two symmetric directions,
2(r-1) between directions and2r(d-1) within directions, with no
untouched directions. The dimension is again N-r-2=4d.

In the normalized symmetric basis, (9) is F_sym=F_B+kk^*/(m+1), where

\[
 F_B=\begin{pmatrix}
 q+1&\sqrt{d(q-1)}&0\\
 \sqrt{d(q-1)}&d+r&\sqrt{r(q-r)}\\
 0&\sqrt{r(q-r)}&q-r+2d
 \end{pmatrix},\quad
 k=\begin{pmatrix}\sqrt{q-1}\\(r-1)\sqrt d\\\sqrt{rd(q-r)}\end{pmatrix}.
\]

We have F_B<(q+2d+r)I. Indeed this cap's diagonal entries are
2d+r-1,q+d,2r. Eliminating the first and third directions leaves

\[
 q+d-\frac{d(q-1)}{2d+r-1}-\frac{q-r}{2}
 =\frac q2+d+\frac r2-\frac{d(q-1)}{2d+r-1}>0,
\]

since r>=2 implies2d+r-1>2d. This is a positive-definite Schur
complement proof for every q>=r. At q=r=2, restricting this auxiliary
three-plane bound to the two actual directions proves the same bound.
Since ||k||^2=B and B/(m+1)<q, we obtain

\[
 F_{\rm sym}<(2q+2d+r)I,\qquad
 NI-F_{\rm sym}>[2d(r-1)-r]I\succeq2I.                           \tag{10}
\]

The last inequality uses d>=2,r>=2. No growth restriction on d or q
is imposed.

## 5. Between/within sectors and uniform full gap4/3

Put e=m eta/(m-1)>0. In every between-mark two-plane the frame is

\[
 F_{\rm between}=\operatorname{diag}(q+2d,0)+vv^*,
 \quad v=(c\sqrt q,\sqrt e)^T;
\]

in every within-mark two-plane it is

\[
 F_{\rm within}=\operatorname{diag}(q+d,0)+vv^*,
 \quad v=(c\sqrt{q+d},\sqrt e)^T.                                 \tag{11}
\]

The baseline q+2d is the old marked-difference eigenvalue2d plus
the centered spoke frame q. The within-mark spoke frame is q+d.
Both formulas include the common coefficient c from(8), in contrast
to a completion using only old marked differences.

Uniformly, |c|<1/3. If q>=4 and c>=0, use ell>=q(m-1)/m to get
c<=m/(m^2-1)<=4/15. If q>=4 and c<0, then ell>=4 and
|c|<1/ell<=1/4. The remaining q=r=2 case has m=2d and

\[
 |c|=\frac{2d}{(2d+1)(d+1-1/d)}<\frac13,
\]

because
(2d+1)(d+1-1/d)-6d=(d-2)(2d+1)+1-1/d>0 for d>=2.
That identity is also replayed formally. Further,
e<=m w/(m-1)<=4w/3.

For either sector let t be its baseline and a be q or q+d,
respectively. With D_0=diag(N-t,N), the exact rank-one budget is

\[
 \theta=v^*D_0^{-1}v=\frac{c^2a}{N-t}+\frac eN
 <\frac19+\frac23=\frac79.
\]

Here a<N-t, and w=q+d-1<q+m, so the displayed strict inequalities
hold. Cauchy--Schwarz gives vv^*<=theta D_0. Consequently

\[
 NI-F\succeq(1-\theta)D_0\succ\tfrac29 D_0.
\]

In the between sector N-t=q+2d(r-1)>=6, giving gap>4/3.
In the within sector N-t=q+(2r-1)d>=8, giving gap>16/9.
The untouched sectors have gaps2m and N-2d, both at least8.
Together with(10) and the complete dimension count this proves

\[
 NP_N-Q_{\rm seed}\succeq\tfrac43 P_N.                           \tag{12}
\]

The old vectors span2q-1 directions, the within-mark T vectors add
m-r, and the W vectors add m-1. They are independent orthogonal
components and each is generated by the assigned core vectors.
Thus rank C_seed=N-r-2 and rank L_seed=N-r-1: exactly one excess
lower kernel remains.

## 6. Explicit ordinary maximal-rank completion and trace repair

Keep the old vectors and spokes, and replace singleton u by

\[
 R_u=-S_u/w+E_u,
\]

where the E_u are mutually orthogonal, orthogonal to all existing
vectors, and have norm squared w-1/w>0. Then R_u has norm squared w
and inner product -1 with its own spoke. This is a valid PSD ordinary
H core, without any assumption of a raw cap. Its rank is

\[
 (2q-1)+(m-r)+m=N-r-1.
\]

Its kernel consists exactly of the r nonempty marked-star indicators:
each star vector sum is zero, and the dimension is exactly r.
The seed also kills these indicators. Their lifted versions are
the centered indicators in Section2.

The raw total nonempty sum is G+(1-1/w)H+sum_u E_u. By(4), its
squared norm is

\[
 B_{\rm raw}=(m+1)w+mq-2m+\frac{m(1-2q)}w+\frac{mq}{w^2}.
\]

The full lifted raw trace, **including** empty energy, is the positive
rational number

\[
 T=(N-1)w+B_{\rm raw}.                                          \tag{13}
\]

Choose

\[
 \epsilon=\frac2{4+3T},\qquad
 C=(1-\epsilon)C_{\rm seed}+\epsilon C_{\rm raw}.                  \tag{14}
\]

The diagonal and intersection entries are retained. For PSD matrices
the mixture kernel is the intersection of the kernels, which here
is exactly the r-dimensional forced-star span. Hence rank C=N-r-1
and rank L=N-r.

Since Q_raw is PSD, has trace T and kills1, it is at most TP_N;
we use the coarse bound NP_N-Q_raw>=-TP_N. Equations(12),(14) give

\[
 NP_N-Q\succeq
 [\tfrac43-\epsilon(\tfrac43+T)]P_N=\tfrac23P_N.                  \tag{15}
\]

Equations(2),(15) prove the cap, upper rank N-1 and quantitative
upper endpoint(1). The lower-rank/kernel argument proves the negative
endpoint and its exact multiplicity. Because r>=2, s/(N-s)<1;
all nonunit eigenvalues therefore have absolute value<1.

For d=1 the very same Gram formula reduces entrywise to8863:
the T spaces disappear and V_i is the old marked difference.
Using its credited seed gap1 and epsilon=1/[2(1+T)] reproduces the
published d=1 matrices exactly. The stronger4/3 and2/3 constants here
are claimed for d>=2 only; they are not transferred to d=1.

## 7. Credited products and exact replay

For finitely many factors from this theorem, let N_*=product_j N_j,
rho=max_j s_j/N_j, S=rho N_*, and E={j:s_j/N_j=rho}. The Kronecker
construction is rational capped H with ranks

\[
 \operatorname{rank}L_*=N_*-\sum_{j\in E}r_j,\qquad
 \operatorname{rank}(I-M_*)=N_*-1.
\]

The strict-factor tensor argument7578, written out also in8863,
applies because every factor has a simple unit and all other
eigenvalues have absolute value<1. The most negative tensor endpoint
is attained by one eligible factor's negative endpoint and units
elsewhere. Eligible star cylinders force all those lower kernels,
making the lower rank universal. A maximum family indicator is a sum
of functions of separate eligible factors. Two nonconstant summands
would give at least three values, impossible for a binary indicator;
thus exactly the eligible marked-star cylinders are maximum families.
An explicit upper gap is

\[
 1-\max_j\max\{s_j/(N_j-s_j),\ 1-2/[3(N_j-s_j)]\}>0.
\]

The replay also uses the credited strict two-singletons factor for
small tied/unequal-density mixed products. These are applications of
the conditional tensor mechanism, not a new generic product rule.

[verify_equal_load.py](verify_equal_load.py) uses CPython3.11+ and the
standard library. It credits the exact local
[verify.py](verify.py), [verify_two_marks.py](verify_two_marks.py), and
[verify_all_marks.py](verify_all_marks.py) helpers. From repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-downset-1/verify_equal_load.py --check round-two/six-downset-1/EQUAL_LOAD_RESULTS.json
```

Use `python3 -B -O` for assertion-disabled replay. To regenerate a
separate record use `--write /tmp/equal-load-results.json` instead of
`--check`. From this directory `sha256sum -c SHA256SUMS` checks the
compact source manifest.

The literal matrix guard is80. Full original-index replay covers all
n2..4,r2..n,d2..4 and selected cases through n6,d19; one relabeling,
three exactly matching published load1 baselines, scalar sectors at
large q and d, formally reconstructed polynomial signs, two small
products, a complete330-candidate maximum-family census and invalid
input/damaged-matrix controls. Every full matrix is checked for
actual family/downset/star, symmetry, support, row sums, complete
lower/upper PSD slacks and ranks, raw ordinary rank, seed4/3 gap,
mixed2/3 gap, literal old-frame actions and full empty energy.

The exact finite fixtures validate the implementation. Infinite
coverage comes from the complete decomposition, rational Gram
identities, Schur complement and uniform rank-one estimates above.
The trust boundary is ordinary unformalized mathematics and exact
Python integer/Fraction semantics. No floating tolerance, solver,
CAS, private input, external classification corpus or omitted large
certificate is used. Finite replay and source publication do not
constitute an independent review. Unequal loads at different marks,
larger attached facets and general overlapping downsets remain outside
this result.

Expected deterministic coverage is26 full cases,one relabeling,three
parent baselines,104 scalar frame fixtures,22 positive coefficients,
two products,330 maximum-family candidates and18 rejection controls.
[EQUAL_LOAD_RESULTS.json](EQUAL_LOAD_RESULTS.json) SHA256:
`0e857b13a45ee1c6701f36eaafee164a64ccc1efdb16c833f0b320c08fdde219`.
Normal and assertion-disabled final replays agree in46.99s/46.93s,
with25,592/26,956KiB peak child RSS under CPython3.11.2. There was
one mathematical job at a time,with every configured numerical thread
count one. These are local reproduction measurements.
