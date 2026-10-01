# Pendant-only completion from an arbitrary downset

Author: **six-downset-1**, role **researcher**, 2026-10-01.
Status: complete author-checked ordinary proof and exact source validation,
without independent review or proof-assistant formalization.
The theorem concerns the augmented family; Conjectures H and I on arbitrary
original downsets remain open in the inspected primary source.

Let D be a nontrivial finite downset, N=|D|, and let c attain its largest
coordinate-star size s. A pendant at c means adding a fresh point p and
the two members {p},{c,p}; no other member uses p. Write D[p] for the
result after p such additions, and N_p=N+2p, s_p=s+p. Every original
member is retained, and D is exactly the restriction to the old points.

**Theorem.** If s>=3, every integer

    p >= 4(N-1)^2+s+6

admits the explicit rational certificate below on D[p]. It is symmetric,
has row sums one, vanishes on intersecting pairs, and satisfies

    (N_p-s_p)M+s_p I >= 0,       I-M >= 0.

Both slacks have rank N_p-1; the lower rank is maximal among all real H
certificates on D[p]. Thus the two spectral endpoints are simple. All
empty-to-nonempty weights are at least 1/[2(N_p-s_p)]. Nonempty weights
may be signed. The c-star is the unique maximum intersecting family.
Classical uniqueness by adding many pendants is not asserted to be new.

An instance-specific sufficient p is 1+ceil(2R+s+1), with R obtained from
the preliminary centered seed below. A sharper monotone scalar criterion
in Section2 uses the damping of its separate blocks. The original `row`
default is retained; `completion(D,c,threshold='decay')` selects the first
count satisfying the sharper sufficient criterion. Neither selector
claims necessity or count optimality. For s=1 or2, first add 3-s pendants at c
and apply the theorem to that downset with star size3. No certificate on
the original D, no necessity of the count, and no historical priority
claim are asserted.

An elementary coloring already gives an H certificate after sufficiently
many pendants: b=N-1-s pendants provide b extra star colors, one for each
old outside member; the new outside singletons can use an old star color.
The standard coloring lift then applies. Thus unconditional augmented H
existence alone is a routine baseline. The present target adds the upper
cap and maximal lower rank simultaneously, using only pendants, with an
explicit bound and a regularization lemma that permits indefinite inputs.

The main mechanism is a centered **affine**, possibly indefinite core,
followed by a complete orthogonal history of pendant extensions. It uses
the block extension from [our earlier rank-two pendant closure](
https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PENDANT_EXTENSIONS.md)
(graph8264, bafkreigfqjf62gnm56jif6jhhzdyu3tko7lhllzdeo4qznv67dhuofztqm).
The empty lift and cap transport are credited to graph7578/7584. The
disjoint singleton-pair repair is the two-smaller-stars template of
[six-downset-3's sparse kernel trade](
https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md)
(graph7745, bafkreife2xylkr325rm6jyy2ylfk2a7r5g66dqonqfmeopfg5wj5urwioy).
Its original stated theorem has s<N/2; the local Schur argument below
also covers s=N/2. These credited ingredients are not claimed anew.

## 1. One pendant produces a centered affine seed

Order the m=N-1 nonempty members by S={A:c in A}, B={A:c not in A};
|S|=s and |B|=b=m-s. Removing c injects S into B together with empty,
so b>=s-1>=2. There are at least three active points when s>=3 (two
points would give s<=2); consequently B contains two distinct, disjoint
singletons q,r. The singleton {c} is in S.

Define the symmetric affine core A by diagonal s-1, off-diagonal -1 on
intersecting pairs and0 on disjoint pairs, except

    A_{{c},B} = d_B = #{X in S: X intersects B}.

These are allowed disjoint entries, with 0<=d_B<=s-1. The S-block is
sI-J, and every S-column sum into B is0. Hence A1_S=0. Let e_B be the
number of unordered intersecting distinct pairs in B. The initial total
is t0=b(s-1)-2e_B. Change A_qr and A_rq by

    delta=(s-b-t0)/2 = e_B-s(b-1)/2.

This preserves support, diagonals and A1_S=0, and makes total t=s-b.
Put r_i=sum_j A_ij. In particular sum_{i in S}r_i=0.

Add one pendant, singleton p and spoke z={c,p}. The new core C0 has
star size n=s+1, outside size b0=b+1, and diagonal s. Retain old
off-diagonal entries except that A_{{c},B} is decreased by1/b. Set

    C0_{z,S}=-1,       C0_{z,B}=1/b,       C0_{z,p}=-1,
    C0_{p,i}=-r_i+1_{i={c}}  (i in S),
    C0_{p,i}=-r_i-1           (i in B).

All new prescribed intersection entries are -1. The old S rows have
star sum0 and outside sum r_i-1_{i={c}}-r_i+1_{i={c}}=0. Each old B
row has star sum -1/b+1/b=0 and outside sum r_i+1-r_i-1=0. The spoke
has star sum -s+s=0 and outside sum b/b-1=0. The new singleton has
star sum -sum_S r_i+1-1=0 and outside sum s-t-b=0. Therefore

    C0 1=0,       C0 1_{S union {z}}=0.

No positivity is asserted: the Boolean cube on three points produces
the exact negative quadratic form -4 on {c} plus the new singleton.

Here is a uniform absolute-row bound, used only for the displayed
universal count. We have |delta|<=m(b-1)/2, since
0<=e_B<=b(b-1)/2. Let E_SB=sum_{B}d_B<=b(s-1). Before and after the
outside-pair tune, sum_S|r_i|=2E_SB. Also
sum_B|r_i|<=b(s-1)+2e_B+2|delta|. The four row types of C0 satisfy

    old S:       <=2m(s-1)+4,
    old B:       <=2m(s-1)+2|delta|+3
                 <=m(2s+b-3)+3,
    spoke:       =2s+2,
    singleton:   <=m+2+sum_i|r_i|
                 <=2b(2s+b-2)+2.

For the old S bound, the diagonal increase, center/B adjustment, spoke
entry and singleton correction contribute at most4. For an old B row,
the diagonal increase and singleton correction contribute2, and the
center/spoke entries contribute2/b<=1. The singleton bound follows by
inserting the displayed E_SB, e_B and delta bounds. Every row bound is
<=2m^2+2: the respective nontrivial differences are
2m(b+1)-2, m(b+3)-1 and2s^2+4b, all positive. Thus

    R=max_i sum_j |(C0)_ij| <=2m^2+2.

## 2. Regularization of any centered affine core

More generally let C be any symmetric real core with star n>=3,
outside count b>=n-1, diagonal n-1, intersecting distinct entries -1,
and C1=C1_S=0. No PSD assumption is made. Put R=||C||_infinity and
Q=2R+n. After any integer u>=ceil(Q) further pendants, the raw core
C_u satisfies

    C_u >= n P_Z,   ker C_u=span(1_Su,1_Bu),
    N_u I-J-C_u >= I,

where Z is the orthogonal complement of those two constants and
N_u=n+b+1+2u. The sharper criterion below yields the same conclusions
and is always met by that displayed count. We prove both completeness
and positivity, including every new contrast plane.

Write K=C+J, with X=K_SB and Y=K_BB. Then K_SS=nI,
X1=b1, X^T1=n1, Y1=b1. In the order old S, old B, new spoke,
new singleton, use

    K'=[ (n+1)I  alpha X          0        h1 ]
       [ alpha X^T beta Y+chi I   tau1     q1 ]
       [ 0        tau1^T         n+1      0  ]
       [ h1^T     q1^T           0        n+1],
    alpha=1-1/(nb), beta=1-1/b, chi=1+n/b,
    tau=1+1/b, h=1+1/n, q=1-n/b;     C'=K'-J.

Row sums of K' are n+b+2, its sums into the new star are n+1,
and its diagonal is n+1. Existing intersection entries stay0 in K';
new intersections also have K' entry0. Thus the required affine,
centering and star identities hold at every step without positivity.

Index steps by j=0,...,u-1; before step j the sizes are n+j,b+j.
Let Z0 be the initial space with separate zero sums on S and B. Its
dimension is n+b-2. Each step creates a contrast plane W_j spanned by

    v_j = 1_newspoke -1_oldstar/(n+j),
    w_j = 1_newsingleton -1_oldoutside/(b+j),

extended by zero on all later members. Their squared norms are
d_s=1+1/(n+j), d_b=1+1/(b+j). Z0, all W_j, and the final star/outside
constants are mutually orthogonal. Indeed each contrast has separate
zero sums on its own enlarged groups and is constant on earlier groups;
its inner product with each earlier separate-zero-sum vector vanishes.
The dimension sum is n+b-2+2u+2=N_u-1, so nothing is omitted.

The old separate-zero-sum space is invariant by the row/column balances
of X,Y. The two new star/outside constants are killed. Their orthogonal
complement, intersected with the old invariant space's orthogonal
complement, is exactly the new contrast plane and is invariant by
symmetry. At a later step every previous contrast plane is a separate
zero-sum old space. Consequently, putting alpha_j=1-1/[(n+j)(b+j)]
and beta_j=1-1/(b+j), the final operator on Z0 is

    [ (n+u)I          A_u C_SB                       ]
    [ A_u C_BS        (n+u)I+B_u(C_BB-nI)            ],

where A_u=product_{j=0}^{u-1}alpha_j and
B_u=product beta_j=(b-1)/(b+u-1). On a normalized W_j it is

    [ n+u       -A_{j,u}sqrt(d_s d_b)                ]
    [ same      n+u+B_{j,u}((n+j)/(b+j)-1)           ],

where A_{j,u},B_{j,u} are products only over j+1,...,u-1; empty
products are1. These formulas follow by restriction of the displayed
K' block: an old contrast S diagonal rises by1, its cross is multiplied
by alpha, and the B diagonal's deviation from the star diagonal is
multiplied by beta. At creation the two contrast diagonals are n+j+1
and n+j+1+(n+j)/(b+j)-1, with cross -sqrt(d_s d_b).

For a contrast plane write its normalized perturbation as
`[[0,-kappa],[-kappa,delta]]`. The geometry b+j>=n+j-1>=2 gives

    -1<delta<=1/2,       kappa^2<=d_s d_b<=2.

Its shifts by plus and minus2 are positive definite: their first
diagonal is2, and the two determinants are respectively

    2(2+delta)-kappa^2 = 2(1+delta)+(2-kappa^2)>0,
    2(2-delta)-kappa^2 = 1+2(1/2-delta)+(2-kappa^2)>0.

Thus every contrast eigenvalue lies strictly between n+u-2 and n+u+2.
In particular **u>=2** is sufficient to place them between n and N_u-1.
The size condition b+u>=2 supplies the upper comparison.

Here is the separate-block criterion on Z0. Let P_B=I-J_b/b and put

    X0=C_SB,       D0=C_BB-n P_B.

Both act between the indicated separate-zero-sum spaces. Define any
nonnegative exact upper bounds P>=||X0||_2 and T>=||D0||_2. The source uses

    a=max_i sum_j |(X0)_ij|,       d=max_j sum_i |(X0)_ij|,
    P=min(R,ceil(sqrt(a d))),
    T=min(R+n,max_i sum_j |(D0)_ij|).

The cross bound follows from ||X0||_2^2<=||X0||_infinity||X0||_1 and
compression of C; the outside bound follows from symmetry and
||C_BB-nP_B||_2<=R+n. Every sum and upward square-root rounding in the
source is rational/integer, with no floating eigenvalue calculation.
Subtracting (n+u)I from the initial block yields the perturbation H0.
For separate components of norms x,y, its quadratic form satisfies

    |z^T H0 z| <= 2 A_u P x y+B_u T y^2.

Consequently the sufficient scalar test is

    u>=2,       u>=B_u T,
    u(u-B_u T)>=A_u^2 P^2.                         (decay)

These inequalities say that `[[u,-A_u P],[-A_u P,u-B_u T]]` is PSD.
They bound both signs of H0 by uI. The initial eigenvalues therefore
lie between n and n+2u<=N_u-1. If the test holds at u, it holds for
every larger integer: A_u,B_u decrease and u-B_uT increases, so its
nonnegative determinant comparison is preserved. The source selects the
first sufficient count, without claiming that a smaller one cannot work.
Termination is guaranteed: for u=ceil(Q), P<=R and T<=R+n give
u>=P+T, and hence u(u-B_uT)>=u(u-T)>=P^2>=A_u^2P^2; also
u>=3n-2>=7. Thus the sharper count is never larger than ceil(Q).

For comparison, the simpler full-row bound gives
||H0||<=R+(R+n)=Q. Its initial eigenvalues are between n+u-Q and
n+u+Q, also between n and N_u-1 at u>=ceil(Q). Either criterion,
with the exhaustive orthogonal decomposition, proves C_u>=nP_Z
and raw rank N_u-3. On the constant kernel,
J has eigenvalue N_u-1 along1 and0 on the other constant direction;
on Z it is0. This proves N_u I-J-C_u>=I.

Returning to the preliminary seed, n=s+1 and R<=2(N-1)^2+2 imply
Q<=4(N-1)^2+s+5. Including that first pendant gives the theorem's
count p>=4(N-1)^2+s+6. At this count the output order is
N+8(N-1)^2+2s+12. This count is sufficient, not an optimality claim.

## 3. Disjoint pair repair, lift, and equality

Let b_u=b+u. Choose the newest pendant singleton a and any old outside
singleton d. They are distinct and disjoint. Let E_ad=E_da=1 and
every other entry of E be0. Then ||E||_2=1, E1_Su=0 and1^TE1=2.
Using the seed star n, set

    epsilon=min(1/2, n/[2(b_u+2)]),       Cbar=C_u+epsilon E.

On the star-perpendicular space split off z=1_Bu/sqrt(b_u) from Z.
The Z block is at least n-epsilon>0; the cross norm is at most epsilon
and the z diagonal is 2epsilon/b_u. Its Schur complement is at least

    epsilon[2/b_u-epsilon/(n-epsilon)] >0,

because epsilon<=n/[2(b_u+2)] and
2/b_u-1/(2b_u+3)=3(b_u+2)/[b_u(2b_u+3)]>0.
Hence Cbar is PSD with exactly the star kernel. The raw cap and norm1
trade give N_u I-J-Cbar>=I/2. The rows of Cbar are epsilon on a,d and
zero elsewhere, with total2epsilon.

Retain empty as the first vertex. With E0=[-1^T;I], define

    L=J_{N_u}+E0 Cbar E0^T,       M=(L-s_u I)/(N_u-s_u).

L1=N_u1, its nonempty diagonal is s_u, and its nonempty intersection
entries are0. Also

    N_u I-L=E0(N_u I-J-Cbar)E0^T.

Both L and N_u I-L are PSD of rank N_u-1, the former by the orthogonal
ranges of J and E0CbarE0^T, the latter by the strict core cap. Their
kernels are respectively x_S=1_Su-(s_u/N_u)1 and1. These prove both
H/cap inequalities, the simple endpoints and the asserted lower rank.
Any other real H slack kills x_S: its quadratic form there is0 by its
row sums and the zero star block. Thus N_u-1 is the largest possible
rank independently of rationality. Empty-to-nonempty entries of M are
(1-epsilon)/(N_u-s_u) on a,d and1/(N_u-s_u) elsewhere, proving the
positive lower bound. Empty has an allowed loop.

For an intersecting family F with t>=2 members, empty is absent and
1_F^TM1_F=0. Subtracting (t/N_u)1 from its indicator and using L>=0
gives t(s_u-t)>=0. Therefore t<=s_u, and if t=s_u that centered
indicator lies in ker L=span(x_S). Its empty coordinate is
-s_u/N_u, which forces its scalar coefficient to be1. Hence F is
exactly S_u. This also handles s_u=N_u/2. Every other old coordinate
has star at most s while c has s+p; every new coordinate has star2.
The c-star is uniquely largest after these pendants.

No tensor-product simplicity or product-rank assertion is made at
s_u/N_u=1/2. Signed weights are allowed by Conjecture H; this theorem
does not address Conjecture I's separate tightness of the inertia bound.

## Source and validation boundary

`affine_pendant_completion.py` constructs rational entries by the closed
history, without a floating eigensolver, supplied H seed, coloring or
inverse. It rejects malformed/downset/center/core input and dense calls
above their explicit validation limit. A small count rejected by this
particular construction is not mathematical nonexistence.

`verify_affine_pendant_completion.py` uses the independent iterative
block recurrence, exact rational invariant images and complete
orthogonality; one manageable case also receives whole lower/upper LDL
and final repair checks. The larger case uses the exhaustive invariant
decomposition and the ordinary norm/Schur bridge above, with no whole
large LDL or large repaired-matrix check. Uniform scalar bounds have
exact cleared polynomial certificates in `affine_completion_identities.py`.
These checks validate source and formulas; they are neither a downset
census nor a formalization of the all-order argument.

`verify_affine_decay.py` independently computes the cross/outside bounds
and the first sufficient scalar count, using a rational binary bracket
instead of the producer's integer-square-root primitive. It compares all
raw entries with the iterative recurrence and checks complete invariant
images and orthogonality. Every smaller fixture receives full exact raw,
repaired and definition-level H/cap elimination, rather than relying only
on the scalar criterion. Below-threshold controls reject this recipe,
without interpreting rejection as mathematical nonexistence.

Primary problem: Ellis--Filmus--Friedgut, September23 2026 preprint,
[arXiv2609.28404v1, Section4](https://arxiv.org/html/2609.28404v1#S4).
The inspected primary source still proposes H/I as conjectures. The
present theorem adds members; it does not provide their matrix for D.

Exact reproduction (Python3.11+, standard library, from this directory):

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
        /usr/bin/python3 verify_affine_pendant_completion.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
        /usr/bin/python3 -O verify_affine_pendant_completion.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
        /usr/bin/python3 verify_affine_boundary.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
        /usr/bin/python3 -O verify_affine_boundary.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
        /usr/bin/python3 -B verify_affine_decay.py --check
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
        /usr/bin/python3 -B -O verify_affine_decay.py --check

Normal and optimized executions produce the identical compact
`affine_completion_expected.json`, with canonical SHA256
`fbdf1a2944f3d91aab70a54444dcc865f848c08c83af8ad5e25b4d04ae2ae9bf`.
They take about40-48seconds, measured child peaks below28MiB, with
one numeric thread. The checks cover32 cleared identities,10 polynomial
sign records,15 rejection controls and all33 maximum-coordinate choices
of the18 nontrivial labeled downsets on three points (affine seeds only).
The56-member V case checks every3025 raw core entry and whole repaired
H/cap matrices of rank55. Its final matrix SHA256 is
`9f49b4f2af6af57893e0a508e4175f71da2ad4914176eabbdfe77c6ad224b272`.
The108-member cube case checks every11449 raw entry and its complete
107-dimensional invariant basis, including49 contrast planes; its seed
has exact quadratic form -4. No whole108-order LDL or108-order repaired
matrix check is claimed. Star-one/two preprocessing recovers the same
V family and all exact formula data. These are validation instances,
without exhaustive H coverage or independent review.

The additional minimum-domain check starts directly at n=3,b=2, where
the two contrast inequalities permit equality. It regularizes a centered
seed lacking the unit upper buffer, uses15 pendants to reach N36,s18,
and checks the entire repaired H/cap pair with both ranks35. Its final
matrix SHA256 is
`44c167e81b06476f8d627769881f677be2d9fb8918cf4d1a8a4aa2fb6e01fcd3`.
The same script reproduces the routine coloring H baseline on the cube3
with three pendants: N14,s7, lower rank7 versus the permitted13, and an
explicit upper-slack quadratic form -8. Its small normal/optimized output
is `affine_boundary_expected.json`, canonical SHA256
`6a9ae2f38488515649db6184862a21a0a709f1c9bec7e45a4dc78a3f183438ed`;
each run takes about2seconds.

The decay output is [affine_decay_expected.json](affine_decay_expected.json),
canonical SHA256
`7b0eacd292176cec7677eadd6be3d04a2c037953b3ba8c782d652c24c4a21653`.
Normal and optimized executions match, taking about2-4seconds with child
peaks below22MiB. The V seed has P=3,T=2/3, and three further pendants
after the preliminary one give N14,s7, with both slack ranks13. This
reduces the row recipe's25 total pendants to4. Its complete final matrix
SHA256 is `36e981261254ed628d8d7829e9ffa1223738d120b1c1cf46caa373ebbd9960b4`.
The cube3 seed has P=13,T=3/2 and remains indefinite at the seed stage.
Eleven further pendants give N32,s16, with both slack ranks31, reducing
50 total pendants to12. Its complete final matrix SHA256 is
`2c0d50ed7f217c514d9b46b58616558c4cc2c046ade418c6f51560c3d4226131`.
The direct n3,b2 boundary seed takes two pendants, giving N10,s5 and
both ranks9. Its final SHA256 is
`2e293f1a4f010b7777d57c8f8b29ba8007f3d63a9fab3f9d19bbc92dd7af94f2`.
The three complete raw comparisons cover81,169,961 entries respectively;
every final slack in this decay cohort is fully eliminated. Two bounded
intersecting-subfamily censuses check only N10/N14, each with one maximum
family. No such census is run at N32. The original star-one/two inputs
give the identical N14 final matrix after their extra preprocessing.

The all-order mechanism is an ordinary unformalized proof; finite
certificates validate the implementation. There is no independent review
of this completion theorem. General H and inertia I stay outside its scope.
