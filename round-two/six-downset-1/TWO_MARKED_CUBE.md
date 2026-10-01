# A Boolean cube with pendant edges at two distinct marks

Actual author: **six-downset-1**, role **researcher**, round two,
2026-10-01. Complete author-checked ordinary proof; unformalized and not
independently reviewed. The finite exact replay validates the displayed
construction and its decomposition. The inequalities below, rather than
the fixtures, establish the infinite quantifiers.

## 1. Precise statement and prior ingredients

Let n>=3, let X be an n-element set, choose distinct x,y in X, and take
fresh points a,d outside X. Put

    D_n = 2^X union {{a},{a,x},{d},{d,y}},
    q=2^(n-1), N=2q+4, s=q+1.

**Theorem.** There is an explicitly specified rational symmetric matrix M
indexed by every member of D_n, including the empty set, such that

    M1=1, M[A,B]=0 whenever A intersects B,
    L=(N-s)M+sI >=0, I-M >=0,
    rank(L)=N-2, rank(I-M)=N-1.

The lower rank is greatest among all H matrices for this family. On the
orthogonal complement of the constant vector,

    -(q+1)/(q+3) <= M <= 1-1/[2(q+3)].                 (1)

The lower endpoint has multiplicity exactly two, and the unit eigenvalue
is simple. The only maximum intersecting families are the x- and y-stars.

The H conventions are those of
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4):
the empty loop is allowed and matrix entries may be signed. The live
[arXiv record](https://arxiv.org/abs/2609.28404), checked October 1, lists
v1; general H and I remain open. The spectral cap is an additional
property, not part of the definition of H.

The empty-vertex core normalization is credited to
[the structural source, Section 2](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
graph7578. The standard maximum-family forced-kernel argument is also
recalled in [the two-facet proof](UNEQUAL_FACETS.md), graph8579.
Complement pairing and the complete cube spectrum are prior
ingredients, including graph8020/8066; the shifted cube calculations also
appear in [UNEQUAL_FACETS.md](UNEQUAL_FACETS.md). Convex kernel repair with
a trace bound was used in [the two-facet proof](UNEQUAL_FACETS.md) and is
restated here with the present raw matrix's own trace.

The earlier
[one-pendant construction](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/BALANCED_PENDANT_COMPLETION.md),
graph8424, attaches at a largest-star mark of a balanced family. After
attaching the first edge to a cube, its chosen mark is uniquely largest;
the different mark used for the second edge does not satisfy that
hypothesis. D_n has N-2s=2. Its three facets X,{a,x},{d,y} also have distinct
singleton intersections, so the prior common-core Boolean sunflower
construction in [ALL_PETALS.md](ALL_PETALS.md), graph8700, does not cover
it. The increment here is a complete centered cap construction for this
infinite family and a rank repair preserving an explicit gap. No claim
of historical priority for individual small examples is made.

## 2. Family structure and core normalization

Every old coordinate has a cube star of size q. The x- and y-stars each
gain its own pendant edge and have size q+1; the new a- and d-stars have
size two. Thus s=q+1.

An intersecting family containing {a} is confined to {a},{a,x}, and
similarly for {d}. An intersecting family contained in the cube has size
at most q, by pairing complementary subsets. The two new edges {a,x}
and {d,y} are disjoint. If an intersecting family of size s uses {a,x},
all its cube members contain x, so equality forces the full x-star;
the y case is identical. These observations prove the claimed complete
classification of the maximum families.

Index the m=N-1 nonempty sets after the empty set, and put

    E=[-1^T; I_m], P_N=I_N-J_N/N.

For a symmetric core C define

    Q=ECE^T, L=J_N+Q, M=(L-sI_N)/(N-s).               (2)

It suffices that

    C>=0, C[A,A]=s-1=q,
    C[A,B]=-1 for distinct intersecting nonempty A,B. (3)

Then Q1=0 and (2) gives every original H condition. The cap is equivalent
to N I_m-J_m-C>=0; on the original indices its scaled upper slack is

    (N-s)(I-M)=N P_N-Q.                              (4)

We specify cores as real Gram matrices. Every Gram entry below is
rational, even though a Gram factor may involve square roots.

## 3. The old cube and the centered seed

Let P be the complement matrix restricted to the 2q-1 old nonempty cube
sets. Its row at the full set is zero. On these old indices put

    C_0=qP+(q+1)I-J.                                (5)

This is the usual complement-pair cube core plus I. Its spectrum is

    2q+1, multiplicity q-2;
    q+2,  multiplicity 1;
    1,    multiplicity q.                           (6)

For completeness, the q-1 pair-antisymmetric directions have eigenvalue
1, while the q-2 pair-symmetric directions of coordinate sum zero have
eigenvalue 2q+1. On the remaining plane, using the normalized sum of the
2q-2 proper nonempty coordinates and the full-set coordinate, (5) is

    [3, -sqrt(2q-2); -sqrt(2q-2), q],

whose eigenvalues are 1 and q+2. This accounts for all 2q-1 dimensions.
In particular C_0 is positive definite. Choose old vectors g_A with
Gram C_0 and define

    G=sum_{A nonempty subset of X} g_A,
    H_x=-sum_{A contains x} g_A,
    H_y=-sum_{A contains y} g_A,
    K=G+H_x+H_y, delta=H_x-H_y.

Writing 1_x,1_y for the old star indicators gives C_0 1_x=1_x and
C_0 1_y=1_y. Hence H_x,H_y belong to the eigenvalue-one space of the old
frame, and direct inner products give

    ||G||^2=3q-2, G.H_x=G.H_y=-q,
    ||H_x||^2=||H_y||^2=q, H_x.H_y=q/2,
    ||K||^2=2q-2, K.H_x=K.H_y=q/2,
    ||delta||^2=q, K.delta=0.                        (7)

Also H_x.g_A is -1 if x is in A and zero otherwise, and analogously for
y. Assign the new edges {a,x},{d,y} the vectors H_x,H_y.

Take W orthogonal to the old span with

    b=(q-4)/(2q), eta=||W||^2=(q^2+10q-16)/(4q)>0,
    v=b delta+W.

Assign the new singleton vectors

    U_a=-K/2+v, U_d=-K/2-v.                         (8)

Since ||v||^2=q b^2+eta=(q+1)/2 and K.v=0, both new
singleton norms squared equal q. Furthermore

    U_a.H_x=U_d.H_y=-q/4+bq/2=-1.

Those are their only required intersections. Old intersections and the
spoke intersections were already verified, so the seed Gram C_seed
satisfies (3). Its total vector sum is zero:

    G+H_x+H_y+U_a+U_d=0.                            (9)

Thus C_seed 1=0 and its full Q_seed is diag(0,C_seed). The old span has
dimension 2q-1 and W adds one independent dimension, so

    rank(C_seed)=2q, rank(L_seed)=2q+1=N-3.          (10)

This seed has one extra lower-kernel direction. It will be repaired.

## 4. Complete cap proof for every n>=3

Let F_0=sum_A g_A g_A^T be the old frame operator. Its positive spectrum
is (6), because a Gram matrix and its frame have the same nonzero
eigenvalues. Set H_+=(H_x+H_y)/sqrt(2) and
H_-=(H_x-H_y)/sqrt(2). Their squared norms are 3q/2 and q/2, respectively.
By (8), the seed frame is

    F_seed=F_0+H_+H_+^T+H_-H_-^T+(1/2)KK^T+2vv^T. (11)

We now account for its entire 2q-dimensional span, not only the changed
eigenvalues. The vector G has no component in the pair-symmetric
sum-zero space. Write G=G_low+G_high according to the old eigenvalues
1 and q+2. Computing from C_0 1, whose proper coordinates are 2 and
whose full coordinate is 2-q, yields

    ||G_high||^2=(q+2)(q-1)/(q+1),
    ||G_low||^2=2q^2/(q+1),
    G.H_+=-sqrt(2)q, G.H_-=0.                      (12)

For an explicitly checkable projection, G_high has coefficient vector
(C_0 1-1)/(q+1) in the old g_A basis. Decompose K into three orthogonal
vectors K_+,K_0,K_h: the H_+ direction, the remaining low component, and
G_high. They are nonzero for q>=4, and

    K_+=(H_x+H_y)/3,
    K_0=G-G_high+(2/3)(H_x+H_y), K_h=G_high,
    ||K_+||^2=q/3,
    ||K_0||^2=2q(q-2)/[3(q+1)],
    ||K_h||^2=(q+2)(q-1)/(q+1).                    (13)

The symmetric three-dimensional sector in their normalized basis has
operator

    F_sym=D+(1/2)kk^T,
    D=diag(1+3q/2,1,q+2),
    k=(||K_+||,||K_0||,||K_h||).

Let A=N I-D. Its diagonal is

    ((q+6)/2, 2q+3, q+2),

and its least entry is (q+6)/2. The weighted rank-one norm is

    theta=(1/2) k^T A^(-1) k
      =(1/2)[2q/(3(q+6))
             +2q(q-2)/(3(q+1)(2q+3))+(q-1)/(q+1)].

The middle term is strictly smaller than 1/3 and the final term is
strictly smaller than 1. Since the first term equals
2/3-4/(q+6),

    theta<1-2/(q+6).

Consequently

    N I-F_sym=A-(1/2)kk^T
      >=(1-theta)A > [2/(q+6)] A >= I.             (14)

The antisymmetric sector is span(H_-,W). Before the 2vv^T addition its
operator is diag(1+q/2,0). It is PSD and its complete trace is

    trace(F_anti)=1+q/2+2||v||^2=3q/2+2.

For a PSD matrix the largest eigenvalue is at most its trace. Hence

    N I-F_anti >= (q/2+2)I >=4I.                    (15)

There remain exactly q-2 old high directions, untouched in (11), with
eigenvalue 2q+1 and gap N-(2q+1)=3. The q-3 remaining low directions
are also untouched, with eigenvalue 1 and gap N-1. The dimension count

    3+2+(q-2)+(q-3)=2q

equals the full seed span established in (10). Thus (14)-(15) and both
unchanged sectors prove

    C_seed <= (N-1)I,
    N P_N-Q_seed >= P_N.                           (16)

The second inequality uses the centering (9), not an assumption that a
noncentered Gram bound transfers unchanged to Q. This proves a uniform
scaled cap margin of one for the seed, for every n>=3.

## 5. Explicit ordinary rank repair and retained cap

Keep the old and spoke vectors. Replace the two singleton vectors by

    R_a=-H_x/q+W_a, R_d=-H_y/q+W_d,
    ||W_a||^2=||W_d||^2=q-1/q,

where W_a,W_d are mutually orthogonal and perpendicular to the old
span. Their norms squared are q and their own-spoke inner products are
-1, so the raw Gram C_raw again satisfies (3). Its rank is

    (2q-1)+2=2q+1,

because the old span is full and both new perpendicular directions are
nonzero. Its two kernel vectors are precisely the nonempty indicators
of the x- and y-stars: each old star sum is canceled by its spoke.
These two vectors are also in the seed kernel.

The raw certificate is used only for ordinary H and rank; no cap is
assumed for it. Its total vector sum has squared norm

    B_raw=||K-(H_x+H_y)/q||^2+2(q-1/q)
         =4q-4+1/q.

Therefore the trace of its full lifted Q_raw is the explicit rational

    T=(N-1)q+B_raw=2q^2+7q-4+1/q.                   (17)

Since Q_raw>=0 and Q_raw 1=0,

    Q_raw <= T P_N,
    N P_N-Q_raw >= -T P_N.                         (18)

Choose

    epsilon=1/[2(1+T)],
    C=(1-epsilon)C_seed+epsilon C_raw.               (19)

This is a rational core satisfying (3), with 0<epsilon<1. For two PSD
matrices a mixture with positive weights has the intersection of their
kernels. Since the raw kernel is already contained in the seed kernel,
C has nullity exactly two. From (2), rank(L)=1+rank(C)=N-2.

Combining (16) and (18), on the original indices,

    (N-s)(I-M)
      >=[1-epsilon(1+T)] P_N=(1/2)P_N.             (20)

This proves the upper bound in (1), a simple unit eigenvalue, and
rank(I-M)=N-1. The lower bound follows directly from L>=0.

To see universal maximality, let M' be any H certificate at s and let
z=1_F-(s/N)1 for a size-s intersecting family F. All entries of M' on
F-by-F vanish, including the nonempty diagonal. Thus

    z^T[(N-s)M'+sI]z=0.

Positivity forces that slack to kill z. The centered x- and y-star
indicators are independent: their difference is nonzero, and an empty
coordinate followed by the {a,x} coordinate separates any proposed
linear relation. Every H slack therefore has nullity at least two.
The construction (19) attains this bound. This concludes the theorem.

## 6. Exact replay, scope, and trust boundary

[verify_two_marks.py](verify_two_marks.py) uses Python's standard-library
Fraction and the credited original-definition checker in
[verify.py](verify.py). No optimizer, floating-point eigensolver, external
data or proof-assistant environment is needed. From the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-downset-1/verify_two_marks.py --check round-two/six-downset-1/TWO_MARKED_RESULTS.json
```

The compact expected output is four literal instances, 24 rational frame
fixtures, ten rejection controls, largest literal N=68, and results hash
`8c08c7e6ca3d399f99300d740c4ce9b33ed2042180fc17b61382c3442f4903ad`.
The full compact evidence is [TWO_MARKED_RESULTS.json](TWO_MARKED_RESULTS.json).
The literal cases have (n,N,s,lower rank,upper rank) equal to

    (3,12,5,10,11), (4,20,9,18,19),
    (5,36,17,34,35), (6,68,33,66,67).

The replay verifies row sums, signed support, both PSD slacks and ranks
on every original set index, the full half-gap in (20), both forced
kernel vectors, the literal orthogonal decomposition (13), the raw trace
(17), and the rational congruences of both changed sectors. Additional
scalar frame fixtures include all q=2^k for 2<=k<=20 and q=5,6,7,31,10000;
the nondyadic fixtures check the algebra, not actual additional cubes.
Corrupt support and row sums, a wrong star parameter, invalid domains,
and invalid singular/negative PSD inputs must be rejected. Checks use
explicit exceptions and remain active under Python -O.

The literal order guard n<=6 controls local resource use only. It is not
a theorem restriction. Ordinary proof obligations (6), (12)-(15), and the
complete dimension count close the unbounded bridge. Arithmetic replay
does not independently formalize them. The earlier independent reviews
of two/three-petal constructions do not review this seed or its sector
calculation. No conclusion is drawn about arbitrary three-facet paths
with larger outer petals, three or more distinct marked pendants, or
general Conjectures H/I.
