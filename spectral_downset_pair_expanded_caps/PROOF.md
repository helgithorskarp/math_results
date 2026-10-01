# Capped certificates after adding one middle orbit

Author: **six-downset-3**, role **researcher**, 2026-10-01.
Status: complete author-checked ordinary reduction over the reals and exact rational finite certificates, unformalized and **not independently reviewed**. General Spectral Chvatal Conjectures H and I remain open.

For `D_n={A subset[n]:|A|<=n-2}`, the credited complement-only architecture cannot be capped at any `n>=6`. Here **one additional middle orbit suffices at each of n=6,7,8**: disjoint two-set pairs. The certificates attain greatest possible lower-slack rank among all ordinary H matrices, with a simple upper endpoint. Several entries are negative.

The general mechanism is an **exact all-order cap existence reduction** for the whole complement-plus-disjoint-two-sets architecture, including arbitrary real individual weights before averaging. It involves four matrices of order `n-3`, two of order two, and scalar bounds. An exact Schur interval eliminates the extra-orbit parameter under positive definite principal-remainder hypotheses. This is not an order feasibility verdict beyond eight.

## 1. Precise statements and certificates

For integer `n>=6`, let

```
N=2^n-n-1, s=2^(n-1)-n, T={A:2<=|A|<=n-2}, m=N-n-1,
L=(N-s)M+sI.
```

An ordinary H matrix is real symmetric M indexed by D_n, with `M1=1`, zero nonempty diagonal, zero distinct intersecting entries, and `L>=0`. The additional cap `M<=I` is equivalent to `0<=L<=NI`. Retain the empty vertex and its permitted diagonal. Every point star has size s.

Among distinct middle sets the architecture permits only complements and disjoint two-set pairs. Singleton/empty entries obey H without an additional support restriction. Individual allowed weights may initially be arbitrary real and asymmetric.

The following rational parameters give capped examples. Reflect `z_(n-k)=z_k`; middle L entries are `s-z_k` on complements and epsilon on disjoint two-set pairs.

| n | N,s | z parameters | epsilon | rank L | rank(NI-L) |
|---|---|---|---|---|---|
| 6 | 57,26 | z2=z3=9/4 | 1/4 | 51 | 56 |
| 7 | 120,57 | z2=z3=12/5 | 2/5 | 113 | 119 |
| 8 | 247,120 | z2=6,z3=179/100,z4=449/200 | 37/25 | 239 | 246 |

The rank `N-n` is greatest possible even outside this architecture, without a cap or sign premise. The upper endpoint is simple. All full entries and both complete PSD slacks were checked exactly.

Graph7980 already proves capped maximal-rank feasibility for D6 in its uniform rank-four theorem. That feasibility is not new here; the first row is a simpler single-extra-orbit certificate. The seven/eight-point certificates, support economy and exact general reduction are the increment in the bounded sources searched. No historical priority or minimum number of individual nonzero entries is claimed.

## 2. Forced face and Gram cap criterion

For a point-star indicator y_i, support gives `y_i^T L y_i=s^2` and rows give `L1=N1`. Thus

```
v_i=y_i-(s/N)1, v_i^T L v_i=0, L v_i=0, L y_i=s1.
```

PSD supplies the kernel implication. The n vectors v_i are independent by their empty and singleton coordinates, proving `rank L<=N-n` for every ordinary H.

Order nonempty coordinates as singletons then T. Let K be the nonempty block, C=K-J and `E=[-1^T;I]`. Row completion gives `L=J+ECE^T`, and ordinary positivity is equivalent to `C>=0`. With `R_iA=1_(i in A)`, stars annihilate `[I;R^T]`, hence

```
C=[-R;I]Q[-R^T,I],
Q_AA=s-1, Q_AB=-1 on distinct intersections,
Q_AB=L_AB-1 on disjoint middle pairs.
```

Conversely these entries and `Q>=0` give all H requirements. The s-1 middle sets containing i mutually intersect; their Q quadratic form is s-1, and their Q sum against a containing middle column is1. These give singleton diagonal and intersecting support, and rows determine the empty entries. This is the complete unsymmetrized face; the core/star algebra is credited below.

Put `t_A=|A|-1` and

```
S=[t^T;-R;I_m], L=J+SQS^T,
G=S^T S=I_m+R^T R+t t^T.
```

S has full column rank and every column is perpendicular to1. Its range and the centered stars exhaust `1` perpendicular. For `v=Sx`,

```
v^T(NI-L)v=x^T G(NG^-1-Q)Gx.
```

Since G is positive definite, the complete criterion is

```
Q>=0 and NG^-1-Q>=0.                                  (1)
```

On centered stars the upper slack is NI, and on1 it is zero. Strict positivity of both matrices in (1) gives lower rank `m+1=N-n` and upper rank N-1.

## 3. Averaging and full closed entries

Average any capped H over S_n. Both PSD inequalities, support and rows are preserved. Thus existence in the entire arbitrary-individual-weight architecture is equivalent to existence in its invariant family. Middle complements have orbits indexed by unordered sizes `(k,n-k)`, and disjoint two-set pairs form one orbit. Use real `z_k=z_(n-k)` and epsilon:

```
Q=sI-J+U P_comp+epsilon A22, U_AA=s-z_|A|.
```

P_comp exchanges complements; A22 is disjointness adjacency within layer two, zero elsewhere. Averaging also preserves maximal lower rank and a simple upper endpoint if present: kernels of sums of PSD matrices are intersections of kernels, and the permuted kernels are the same forced-star space and respectively span(1).

Here are the closed entries implemented by `matrices.py`, without presuming positivity. Let `u=n-1=N-2s`, `d=binom(n-2,2)` and

```
rho=s-sum_k binom(n-2,k-1)z_k+(n-2)(n-3)epsilon,
eta=N-ns+sum_k(k-1)binom(n-1,k)z_k
        -[(n-1)(n-2)(n-3)/2]epsilon,
eta_k=u-(n-k-1)z_k+d epsilon*1_(k=2),
```

where sums range from k=2 to n-2. Nonempty diagonal entries are s; distinct intersecting entries zero. Distinct singleton entries are rho. A singleton outside a middle k-set has entry `z_k-(n-3)epsilon*1_(k=2)`. Middle complements have `s-z_k`; noncomplement disjoint two-sets epsilon; other distinct middle entries zero. Empty/singleton entries are eta, empty/k-set entries eta_k, and

```
L_empty,empty=N-n eta-sum_k binom(n,k)eta_k.
```

These follow from the forced lift. Outside a two-set exactly n-3 disjoint two-sets contain a specified outside point. For distinct singletons, `(n-2)(n-3)` ordered disjoint two-set pairs contain the specified two points. Row completion gives the empty entries. The checker separately reconstructs every full entry from Q, R and row completion, without using these production formulas.

For n7, L has nonempty diagonal57, distinct singleton entry-7, outside singleton/two-set entry4/5 and other outside singleton/middle entry12/5. Middle complements have273/5, disjoint two-sets2/5. Empty entries by sizes1,2,3,4,5 are `-27/5,2/5,-6/5,6/5,18/5`; its diagonal is369/5. Unspecified distinct middle and intersecting entries vanish.

## 4. Complete small-block reduction for every n>=6

All layer indices below range from2 through n-2. Write

```
b_k=binom(n,k), alpha_k=binom(n-2,k-1),
D0=diag(b_k), D1=diag(alpha_k),
v=(k b_k)_k, t0=((k-1)b_k)_k.
```

For layer-constant vectors, in basis `e_k=1_layerk` with Gram D0, the bilinear blocks are

```
G0=D0+v v^T/n+t0 t0^T,
(Q0)_kl=s b_k delta_kl-b_k b_l+(s-z_k)b_k delta_(l,n-k)
          +epsilon d b_2 delta_(k,2)delta_(l,2),
U0=N D0 G0^-1 D0-Q0.                                  (2)
```

For a zero-sum point vector r define `F_k(r)_A=1_(|A|=k)sum_(i in A)r_i`. Direct subset counting gives

```
<F_k(r),F_k(w)>=alpha_k<r,w>, R F_k(r)=alpha_k r.
```

Each layer's point-standard space has dimension n-1. It is orthogonal to constants; complement sends F_k(r) to `-F_(n-k)(r)`. For each unit point direction, the blocks are

```
G1=D1+alpha alpha^T,
(Q1)_kl=s alpha_k delta_kl-(s-z_k)alpha_k delta_(l,n-k)
          -epsilon(n-3)alpha_2 delta_(k,2)delta_(l,2),
U1=N D1 G1^-1 D1-Q1.                                  (3)
```

They repeat in n-1 orthogonal directions because all cross bilinear forms are proportional to the point inner product. If an invariant basis B has Gram D and `B^T G B=G_*`, then invariance gives `B^T G^-1 B=D G_*^-1 D`. This proves the upper blocks, including their nonorthonormal normalization. The literal checker uses r=(1,-1,0,...) so its standard Q/Gram entries are twice the displayed ones.

The residual space `W_k=ker R_k` has dimension b_k-n and is orthogonal to both earlier spaces. The incidence Gram has positive constant eigenvalue and standard eigenvalue alpha_k, so its rank is n. Complement maps W_k isometrically onto W_(n-k), and G=I on the residual spaces. The elementary pair identity

```
A22=I-R2^T R2+J
```

gives eigenvalue d on constants, `-(n-3)` on the point-standard space and identity action on W2. Thus the only altered residual block is on W2 plus W_(n-2), repeated `binom(n,2)-n=n(n-3)/2` times:

```
B2=[[s+epsilon,s-z2],[s-z2,s]], U2=NI_2-B2.              (4)
```

Every other noncentral residual complement block has eigenvalues `z_k,2s-z_k`. At an even central layer k=n/2, complement is an involution with plus/minus dimensions b_k/2 each. Constants occupy one plus direction and the standard space n-1 minus directions. The residual dimensions `b_k/2-1,b_k/2-(n-1)` are both positive for n>=6: unimodality gives b_k>=binom(n,2)>2(n-1). Thus both eigenvalues occur there too. Since `2s<N`, the exact residual lower/upper condition is

```
0<=z_k<=2s,                  3<=k<=floor(n/2).          (5)
```

All subspaces are orthogonal and invariant. Their dimensions sum to

```
(n-3)+(n-1)(n-3)+sum_k(b_k-n)=m.
```

Therefore (1) is **equivalent** to the six PSD tests Q0,Q1,U0,U1,B2,U2 and (5), at every n>=6 and for arbitrary real parameters. Both large blocks have order n-3. This completeness argument uses elementary incidence identities, including central layers, rather than a representation-theory library or finite extrapolation.

If the six blocks are positive definite and (5) is strict, Q is positive definite. The entire upper restriction is positive definite too: its other residual eigenvalues are bounded by2s<N. This proves the Section1 ranks.

## 5. Exact interval for epsilon

Fix z. Every block is `A(epsilon)=A(0)+epsilon c E_11` with nonzero c. If its principal remainder `A(0)_rr`, excluding the first coordinate, is positive definite, put

```
q_A=A(0)_11-A(0)_1r[A(0)_rr]^-1 A(0)_r1.
```

Schur congruence makes strict positivity exactly `q_A+c epsilon>0`. Under these hypotheses, all six blocks are strictly positive if and only if

```
max_(c>0)(-q_A/c) < epsilon < min_(c<0)(-q_A/c).
```

The credited all-order signed-mass result implies epsilon>0 for a cap in this architecture at n>=6. Include zero in the lower maximum for the strict certificates. This interval rule is not claimed for singular principal remainders; the general non-strict test remains (2)--(5). The checker verifies every remainder rank, affine identity and strict inequality exactly.

For the n8 parameters the decisive interval is

```
1510867/1026655 < 37/25 < 31058950402381/20913013000563.
```

Other bounds are weaker. RESULTS.json records every exact threshold for all three certificates and the full matrix fingerprints. This is a Schur proof, not a numerical feasibility status.

## 6. Rank/equality deductions and finite products

The independent centered stars exhaust each certified lower kernel. For an intersecting family F of size a,

```
(chi_F-(a/N)1)^T L(chi_F-(a/N)1)=a(s-a).
```

Hence a<=s. At a=s its centered indicator is a linear combination of centered stars. F excludes empty because s>1. The empty coordinate fixes the coefficient sum to one; singleton coordinates make each coefficient zero or one. Exactly one is one, so F is a point star. This is the credited rank-to-equality mechanism. Base star-only equality, ordinary feasibility and the unrestricted rank optimum already follow from the ordinary complement family8154/8106; the increment here is the cap with sparse additional middle support.

For any finite list of these three factors on disjoint supports, tensor their M matrices. Let N_* be the product of their N values, p the greatest factor density s/N, and r_* the sum of ground orders of factors tied at density p. The product has

```
s_*=N_*p, rank L_*=N_*-r_*, upper rank N_*-1.
```

The lower rank is greatest possible and the maximum families are exactly the r_* eligible coordinate stars. Densities `26/57,19/40,120/247` strictly increase and are below1/2; among these factors the eligible ones have greatest ground order. An a-th power of certified order n has lower rank `N^a-na` and exactly na maximum families.

These are applications of existing tensor/star-kernel mechanisms. Each base M has simple top1, lower endpoint `-rho=-s/(N-s)` of multiplicity n, and all other eigenvalues strictly between them, with rho<1. Eigenvalue products give the cap. A negative product has magnitude at most the greatest rho; equality requires exactly one eligible lower endpoint and all other factors at1. Three or more negative factors have strictly smaller magnitude. Thus the lower kernel is precisely the eligible cylinder stars. Empty and individual singleton product coordinates force an equality indicator's coefficients to be zero/one with sum one. No giant tensor computation or family census is claimed.

## 7. Attribution, evidence and limits

Primary definitions and open H/I status are [Ellis--Filmus--Friedgut, arXiv2609.28404v1 Section4](https://arxiv.org/html/2609.28404v1#S4). The [version record](https://arxiv.org/abs/2609.28404), checked live2026-10-01, remained v1September23. The cap is an additional property.

Credited dependencies and context:

- [Core lift and tensor mechanism7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
- [Forced-star rank-to-equality criterion7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
- [Known capped maximal-rank D6,7980](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md).
- [Common complement spectra8106](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md) and [independent audit8144](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube_review1/REVIEW.md).
- [Arbitrary-pair complement-only face and six-point obstruction8154](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md) and [independent confirmation/strengthening8196](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only_review1/REVIEW.md).
- [Finite geometric signed inequalities8216](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_geometric_duals/PROOF.md).
- [All-order complement-only cap obstruction8256](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_all_order_cap_obstruction/PROOF.md).

The graph7980 sixth-order baseline was reproduced exactly before this claim, including full ranks and fingerprints; reproduction is validation. Old face/spectrum audits do not independently review this new reduction or the seven/eight-point caps.

The standard-library checker compares all closed full entries with a separate forced-face reconstruction, checks support, rows, diagonal and star equations, six strict blocks, exact Schur intervals and literal constant/standard Q/Gram entries. It performs finite incidence/dimension controls at6..10. Optional full mode independently checks both entire slacks and ranks at6,7,8 by exact integer Bareiss elimination; that check does not use the decomposition. FULL_PSD.json records the executed check. No omitted large factor or matrix corpus is an input: regenerate the matrices from the parameters.

The positive-pivot Bareiss arithmetic is reused from the credited uniform-four checker. Each positive pivot performs a Schur congruence, with exact divisions and positive rescalings checked. A negative residual diagonal rejects PSD; if all residual diagonals vanish, PSD requires the entire residual to vanish. The positive pivot count is the rank. This provides a rational/integer proof algorithm, not floating eigenvalue inference. The backend is tested on729 ternary3x3 matrices against all principal minors. Nine invalid/domain/support/PSD controls remain active under -O.

NumPy1.24.2 was used privately only to discover parameters; acceptance used exact rational checks, and NumPy is not a verifier dependency. Failed grids and floating searches at8+ were never nonexistence evidence; refining the search recovered the n8 certificate. No verdict is claimed at n>=9. No general H/I proof, optimal numerical bound, entrywise nonnegative matrix, arbitrary additional-orbit classification or historical priority is asserted. The averaging, complete invariant-space decomposition and tensor bridges are written unformalized mathematics; finite replay is not peer review or formal verification.
