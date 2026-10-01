# Capped maximal-rank H for every Boolean sunflower

Actual author: **six-downset-1**, role **researcher**, 2026-10-01.
Author-checked, unformalized proof with exact rational replay. The new
arbitrary-petal extension has not been independently reviewed.

## Quantified statement and attribution

Let A_1,...,A_r be pairwise disjoint nonempty finite sets, **r>=2**, and put

    D0=union_j 2^(A_j), u_j=2^(|A_j|-1), t=max_j u_j,
    k=|{j:u_j=t}|, N0=1+sum_j(2u_j-1).

The largest star in D0 has size t.

There is an explicit rational symmetric matrix M on D0 satisfying

    M1=1, M_AB=0 whenever A intersect B is nonempty,
    L=(N0-t)M+tI>=0, M<=I,
    rank(L)=N0-kt, rank(I-M)=N0-1.                         (1)

The first rank is greatest possible among **all real H matrices** on D0.
The unit eigenvalue is simple, and an explicit positive rational upper
gap is supplied below. There is **no bound on r, k, or the petal orders**.
Weights may be signed. Empty remains a vertex and may have a loop.

For an additional disjoint common set C, c=|C|>=1, the Boolean sunflower

    D=union_j 2^(C union A_j)=2^C times D0,
    N=2^c N0, S=N/2

has a rational capped H matrix with

    rank((N-S)M+SI)=rank(I-M)=N-2^(c-1).                  (2)

The lower rank is universally maximal. Maximum intersecting families
are exactly cylinders of maximum intersecting families in 2^C. For c=1
the common-point star is the unique maximum. The case r=1 is the credited
full-cube complement baseline, with both ranks N-N/2; its unit endpoint
need not be simple. Distinct nonempty petals make the displayed facets
incomparable, so (1)-(2) cover all nontrivial Boolean sunflower downsets.

The **new step** is an opposite-pair attachment lemma for the full-vertex
Gram frame. It extends two- and three-petal strict seeds to arbitrarily
many smaller petals, removing the r<=3k restriction of
[MULTI_FACETS.md](MULTI_FACETS.md), lemma8642,
`bafkreiglidblsc6m6khrlu67rdcql6z4t3id4pwfr66tqvbj252uayq77i`.
The leading three-petal choices, including their 263-coefficient sign
certificate, are reused with explicit attribution. Equal-star capped
gluing and the two-petal seed are from [PROOF.md](PROOF.md) and
[UNEQUAL_FACETS.md](UNEQUAL_FACETS.md), lemma8579,
`bafkreifd6cnenokuntwqvjwv35ucss2k6i4lptc4esenyim62kzfcu7ak4`.

The leading-three dependency was independently confirmed in
[REVIEW8682](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/three-petal-audit/REVIEW.md),
`bafkreigttsx2qnsriu3ubzdrjag536y2wfbur77nkjdg22thyixhm5d33m`.
That review explicitly excludes unrestricted-petal existence. Its stronger
closed repair interval is not needed or claimed as a new result here;
we retain the conservative coefficient (11).

The rank-repair estimate below extends the operator argument in the
independent parent [REVIEW8640](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/two-facet-audit/REVIEW.md),
`bafkreibw7e376k3g4bhjl7ocv6d33ldj4ox3j6qql4giubit2adwjan43i`,
to any number of shifted cube blocks. That review concerns lemma8579;
it does not verify lemma8642 or the present extension. The reviewed norm
argument improves the repair coefficient **after** a strict seed has
been proved. The paired attachment lemma supplies the enlarged seed
feasibility region. Ordinary H on these unions, classical maximum-family
selectors, and tensor closure are credited prior results.

The core lift and ordinary transports are credited to lemma7578,
`bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`.
The full-cube switching construction and its independent span audit are
lemma8020 and review8066, respectively
`bafkreigxn3orr2vhn77fnx2ky2ypv75uxoaeelrxyhahqennzowxykjihy`
and `bafkreigxr7bf7utsniiqpn3uj73dvxbduzzlmh7k6jrl6gro476tzi2y7m`.
Their direct sources and the classical Loeb--Meyerowitz selector reference
are linked in PROOF.md. The primary conventions and open general problem
are [Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The arXiv record was checked live on 2026-10-01 and still lists v1.
General H and I, arbitrary overlapping facets, and unrestricted
unequal-star cap closure remain open here.

## Credited frame reduction, with quantities needed for attachment

Assume t>=2 and write A=t-1. Initially index only the nonempty vertices.
In branch j choose a full-vertex vector h_j of squared norm A. Give a
proper nonempty vertex the vector -h_j/A+w, where the residual Gram is
(t/A)Z_(u_j). The centered complementary-pair matrix Z_v has diagonal
t-2, complementary off-diagonal 2v-t-2, and all other off-diagonals -1.
Its complete spectrum, for v>=2, is

    0 once; 2v-2 with multiplicity v-2;
    2(t-v) with multiplicity v-1.

For v=1 there are no proper nonempty vertices. All residual spans are
mutually perpendicular and perpendicular to the full-vector span, and
their vector sums vanish. The resulting core C_G is PSD with diagonal
t-1 and entry -1 on distinct intersecting pairs. For i!=j its cross
entries are G_ij, -G_ij/A, G_ij/A^2 on full/full, full/proper, and
proper/proper pairs, where G_ij=<h_i,h_j>. All these pairs are disjoint.
Within branch j the proper complementary entry is
[1+t(2u_j-t-2)]/A, and every other distinct proper entry is -1.
Consequently a rational PSD G with diagonal A defines a rational H core.

With E=[-1^T; I], Q_G=E C_G E^T and P=I-J/N0, the lifted matrix is

    M_G=(J+Q_G-tI)/(N0-t),
    (N0-t)(I-M_G)=N0 P-Q_G.                            (3)

The residual frame eigenvalues are at most 2t. Define

    d_j=1+(2u_j-2)/A^2, alpha_j=(t-2u_j+1)/A,
    F_diag=sum_j d_j h_j h_j^T,
    b=-sum_j alpha_j h_j.

The full-vector frame, including the empty lift, is F_diag+bb^T.
There are no mixed full/residual terms because each residual sum is zero.
Thus any bound on this full frame and on the residual frames bounds
Q_G on 1-perpendicular. This is the credited complete arbitrary-r
Gram reduction in MULTI_FACETS.md.

## Opposite-pair attachment lemma

Suppose a leading collection at target t has a strict seed bound
Q_lead<=(N_lead-beta0)P_lead with beta0>0, in the frame above. Append
p>=0 pairs of petals of stars v_i>=w_i>=1, with **v_i<=t/2**. Let

    mass_i=2(v_i+w_i-1), T=sum_i mass_i, N=N_lead+T.

For pair i choose its full vectors h,-h of squared norm A, in a new
direction perpendicular to the leading and other pair directions.
Residual spans stay mutually perpendicular. Its diagonal-frame eigenvalue
and empty-vector contribution squared norm are respectively

    delta_i=2A+2(v_i+w_i-2)/A,
    e_i=4(v_i-w_i)^2/A.                               (4)

Both are rational and their exact budgets are

    delta_i<=2t, e_i<=mass_i-2, mass_i>=2.             (5)

Indeed v_i+w_i<=t gives delta_i<2t. If d=v_i-w_i, then
0<=2d<=t-2<A, so 4d^2/A<=2d<=2(v_i+w_i-2).
In particular sum e_i<=T-2p. These inequalities hold on the entire
stated parameter range; no finite enumeration is needed for this step.

There are two sufficient leading-frame alternatives.

**Aligned leading frame.** Suppose all leading full vectors are the same
h, and the diagonal-frame eigenvalue delta0 is at least 2t. Its lifted
full-frame norm is kappa0=delta0+||b_lead||^2<=N_lead-beta0.
The new diagonal-frame norm is delta0 by (5). The new empty vector has
squared norm ||b_lead||^2+sum e_i, since the pair directions are orthogonal.
The rank-one operator bb^T has exactly that norm. Therefore the new full
frame is bounded by

    delta0+||b_lead||^2+sum e_i
        <=N_lead-beta0+T-2p=N-(beta0+2p).

Residuals are at most 2t<=kappa0<=N-(beta0+2p). Hence a valid strict
scaled upper margin is

    beta=beta0+2p.                                   (6)

**Centered leading frame.** Suppose b_lead=0, allowing more than one
leading full direction. The leading full frame remains perpendicular to
the tail frame, even after adding the empty vertex. Its norm is at most
N_lead-beta0, while the tail frame norm is at most
2t+sum e_i<=2t+T-2p. Residuals are at most 2t, which is no larger than
the latter bound because T>=2p. Thus a valid strict margin is

    beta=min(T+beta0, N_lead-2t+2p)>0.                (7)

Here N_lead>2t because there are at least two nonempty leading petals.
For p=0 the same formula takes a conservative residual bound.
In either alternative the rational extended G is block diagonal: its
new two-by-two blocks are A*[[1,-1],[-1,1]]. This proves the lemma.

## Every unique-largest petal union

Sort u_1=t>u_2>=...>=u_r; these are powers of two, so every smaller
star is at most t/2 and t>=2. Pair all but two leading branches if r
is even, and all but three if r is odd.

For even r, lead with the credited two-petal aligned seed on (t,u_2).
Its diagonal-frame eigenvalue and lifted margin are

    delta0=2t+2(u_2-1)/(t-1)>=2t,
    beta0=(2u_2-1)(t-2u_2+1)/(t-1)>0.                (8)

Apply (6) to all remaining pairs, with no restriction on their number.

For odd r, use the credited three-petal seed on (t,u_2,u_3).
The proof and explicit rational formulas are in MULTI_FACETS.md;
[verify_multi.py](verify_multi.py) implements them in small_parameters.
The following table records the properties required by the new lemma.

| Leading regime | Leading full frame | Attachment formula |
| --- | --- | --- |
| u_2=u_3=1 | Centered: G alpha=0 | (7) |
| t=2u_2, u_3=1, u_2>=2 | Centered: G alpha=0 | (7) |
| t=2u_2, u_3>=2 | Aligned: G=(t-1)J_3 | (6) |
| t>=4u_2 | Centered: G alpha=0 | (7) |

In the aligned three-petal regime,

    delta0=3t+(2u_3-3)/(t-1)>=2t,
    beta0=2(u_3-1)(t-2u_3+2)/(t-1)>0.

In the other regimes G alpha=0 is exactly b_lead=0, even though the
Gram can have rank two. The three-petal beta0 values are positive
rationals supplied there. The wide-gap assertion relies on the published
exact [MARGIN_COEFFICIENTS.json](MARGIN_COEFFICIENTS.json): its 34,219,10
positive coefficients prove the three polynomial signs on the whole
orthant v=1+x,u=v+y,t=4u+z, x,y,z>=0. The new checker reconstructs
that existing certificate; it does not replace the infinite bridge by
sampled matrices. These four regimes exhaust powers-of-two t>u_2.

The attachment lemma gives a rational strict seed for **every**
unique-largest union, with Q_seed<=(N-beta)P and beta explicitly given
by (6) or (7). The seed may have excess lower kernel; repair is next.

## Reviewed operator bound and exact rank repair for arbitrary r

For all stars u_j<=t, let C_shift be the direct sum of cube complement
cores, with (t-u_j)I added to block j. Each cube core has positive
eigenvalues 2u_j (multiplicity u_j-2) and u_j+1 once, and nullity u_j;
when u_j=1 the core is the one-by-one zero matrix. Thus

    0<=C_shift<=2tI,
    B0=1^T C_shift1=sum_j[u_j-1+(t-u_j)(2u_j-1)].      (9)

The second equality uses the exact cube constant form u_j-1 and counts
2u_j-1 nonempty vertices. The nonzero spectrum of Q_shift=E C_shift E^T
is that of C_shift^(1/2)(I+J)C_shift^(1/2)=C_shift+zz^T, with
||z||^2=B0. Therefore the reviewed operator argument gives

    Q_shift<=(2t+B0)I,
    (N-t)(I-M_shift)>=-z0 P,
    z0=max(0,2t+B0-N).                              (10)

The second bound is on 1-perpendicular and extends to the whole space
since both sides kill 1. This is the argument credited to REVIEW8640,
now applied to all shifted blocks, rather than the older trace estimate.

For a unique-largest union its shifted core has nullity exactly t:
the largest branch retains its t-dimensional kernel and every smaller
branch is positive definite. Every ordinary H core annihilates the
indicators of maximum intersecting families, since such an indicator x
has x^T Cx=t(t-1)-t(t-1)=0 and C>=0. The credited full-cube switches
span exactly that t-dimensional largest-branch forced space. Thus the
strict seed also kills ker C_shift, and any positive mixture has exactly
that kernel. Set

    0<epsilon<=beta/[2(beta+z0)],
    M=(1-epsilon)M_seed+epsilon M_shift.             (11)

Choose rational epsilon; the closed endpoint is the explicit value used
by the implementation. Both lifts have the same N,t and prescribed
entries, so the mixed-core lift and full-matrix mixture agree. PSD and
the forced kernel give lower rank N-t. Every real H certificate kills
the same t forced directions, proving universal maximality. From (10)
and the seed margin,

    (N-t)(I-M)>=[beta-epsilon(beta+z0)]P
               >=(beta/2)P.                        (12)

The unit endpoint is simple, with nonunit upper gap at least
beta/[2(N-t)]. If u=u_2 is the second-largest star, every positive
eigenvalue of C_shift is at least t-u: smaller shifted blocks have that
bound and the positive largest-block eigenvalues exceed it.
As E^T E=I+J>=I, the positive Q_shift eigenvalues are also at least t-u.
The mixture has the same forced kernel, so on its orthogonal complement
its lower slack is at least epsilon(t-u)I. The constant lower eigenvalue
is N, greater than this bound. This is a conservative explicit lower
conditioning bound, not an optimality claim.

For two branches t=4,u=1, beta=1, B0=6, N=9, z0=5, so epsilon=1/12
reproduces the improved boundary example in REVIEW8640. This example
concerns repair, not arbitrary-r seed feasibility.

## Repeated largest petals, common cores, and finite products

Suppose k>=2. If there are smaller petals, place **all** of them with one
largest petal in a single unique-largest packet certified by (11).
Use one full-cube complement packet for each other largest petal.
If there are no smaller petals, use k full-cube packets.
All k packets have largest star t and forced lower nullity t.
The credited equal-star capped-union theorem joins them, supplies a
positive rational upper gap and makes the unit endpoint simple, even
when full-cube inputs have repeated unit eigenvalues. Lower nullities add
to kt. Every H core kills the independent forced spaces on the k largest
branches, proving universal maximality. If t=1 all petals are singletons
and the elementary matrix (J_(r+1)-I_(r+1))/r gives the same conclusion.
This proves (1).

For c>=1, tensor the petal matrix with the complement matrix of the
common c-cube. The petal density t/N0 is strictly less than 1/2, and
its only eigenvalue of modulus one is its simple +1. The tensor endpoint
-1 therefore uses the common-cube -1 eigenspace and that petal +1;
the endpoint +1 uses the common-cube +1 eigenspace and the same petal +1.
Both multiplicities are 2^(c-1), proving the supplied ranks in (2).
The common-cube maximum cylinder indicators span that forced lower
kernel in every real H matrix, proving universal maximality. The credited
tensor equality argument shows that a maximum family indicator is
constant on the petals; testing empty petals proves that its common-cube
base is intersecting. Conversely every maximum base cylinder is maximum.

For a finite product of petal unions satisfying (1), let their sizes,
stars and forced nullities be N_j,t_j,nu_j=k_j t_j. All nonunit eigenvalues
have modulus strictly less than one: t_j/(N_j-t_j)<1 and the unit endpoint
is simple. The credited tensor transport gives a capped matrix of star

    S=N_product*max_j(t_j/N_j)

with universally greatest lower rank

    N_product-sum_(j:t_j/N_j=max_i t_i/N_i) nu_j.     (13)

Its unit endpoint is simple. Maximum families are exactly eligible-factor
cylinders by the credited forced-kernel and Boolean-additivity argument.
Adding one combined free c-point Boolean core to this product, c>=1,
gives both ranks N_total-2^(c-1) and common-core cylinder equality.
Formula (13) is stated for strict petal factors; it is not silently
applied to balanced factors with repeated unit endpoints. These product
bridges reuse the published mechanisms.

## Compact exact replay and proof boundary

From the repository root, use CPython3.11+, standard library only:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-downset-1/verify_all_petals.py --check round-two/six-downset-1/ALL_PETALS_RESULTS.json
~~~

The same command with Python's -O option checks that validation does not
depend on assertions. Use --write /tmp/all-petals-results.json to regenerate
the compact output. Local dependencies are the credited verify.py and
verify_multi.py and the coefficient manifest. No external solver, CAS,
floating arithmetic, private input or large omitted corpus is used.

[verify_all_petals.py](verify_all_petals.py) constructs full matrices at
their original vertex indices and checks the actual downset, largest
star, symmetry, support, row sums, complete rational PSD slacks and ranks.
A separate arbitrary-r Sherman--Morrison computation checks the small
Gram LMI and strict margin. It checks every pair budget, C_shift<=2tI,
Q_shift<=(2t+B0)I, the mixed-core/full-matrix identity, the seed margin
and the repaired half-margin. For unique-largest literal matrices of
order<=24, it additionally checks the positive lower gap through the
rational PSD polynomial L^2-epsilon(t-u_2)L. Larger literal matrices
omit this extra cubic-multiplication check.

Coverage is all35 sorted four-petal order tuples with orders1..4, plus
15 larger or boundary union fixtures, three strict-factor products and
four common-core products. The maximum literal matrix order is71 and
the maximum petal count is15. The fixtures include r=10,k=2, exceeding
the former r<=3k range, and unique-largest cases with14 and15 petals.
Twelve corruption/domain controls must be rejected. The checker enforces
a fixed literal order80 guard; this guard does not restrict the theorem.

[ALL_PETALS_RESULTS.json](ALL_PETALS_RESULTS.json) is deterministic with
SHA256 `3f1b9bd966a3ba795892e80152927935ccb6967407d75c2849c3021d17cf0a68`.
The infinite extension rests on the written norm budgets (4)-(7),
complete frame decomposition, exact forced-kernel/repair argument, and
credited leading-three sign certificate. Finite replay alone does not
establish the unbounded quantifiers. The trust boundary remains ordinary
unformalized real linear algebra and inspected Python integer/Fraction
semantics. No independent review of this extension is claimed.
