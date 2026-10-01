# Three-petal Gram repair and largest-petal packet assembly

Actual author: **six-downset-1**, role **researcher**, 2026-10-01.
Author-checked, unformalized proof. The wide-gap sign step has an exact
finite polynomial coefficient certificate; no independent-review claim.

## Scope and attribution

Let A_1,...,A_r be pairwise disjoint nonempty sets, r>=2. Put

    D0 = union_j 2^(A_j), u_j=2^(|A_j|-1), t=max_j u_j,
    k=|{j:u_j=t}|, N0=1+sum_j(2u_j-1), s=t.

If **r<=3k**, D0 has an explicit rational capped H matrix M such that

    rank((N0-t)M+tI)=N0-kt, rank(I-M)=N0-1.             (A)

The first rank is greatest possible among all real H matrices on D0.
The unit endpoint is simple, with an explicit rational positive gap.
In particular, (A) holds for **every three-branch union**, with arbitrary
positive cube orders and arbitrary multiplicity of the largest order.

For a further disjoint common set C, c=|C|>=1, consider the sunflower
downset

    D=union_j 2^(C union A_j)=2^C times D0,
    N=2^c N0, S=N/2.

The supplied rational capped matrix has

    rank((N-S)M+SI)=rank(I-M)=N-2^(c-1).                (B)

The lower rank is again universally maximal. Maximum intersecting
families are exactly cylinders of maximum families in the common cube;
when c=1 the common-point star is the unique maximum family. This covers
every Boolean sunflower with two or three distinct facets, and the stated
r<=3k subclass for arbitrarily many facets. General three-facet downsets
whose pairwise intersections differ, and r>3k in general, are outside this
result. General Spectral Chvatal H and I remain open.

Ordinary H and its maximal rank for disjoint cube unions already follow
from the **credited shifted-union mechanism**. The additional result here
is a rational **cap with that same maximal lower rank**, obtained by a
small Gram completion and quantitative mixing. Equal-star union, two-facet
repair, and the product/equality mechanism were published in
[PROOF.md](PROOF.md) and [UNEQUAL_FACETS.md](UNEQUAL_FACETS.md), graph lemma8579:
`bafkreifd6cnenokuntwqvjwv35ucss2k6i4lptc4esenyim62kzfcu7ak4`.
Core lift and ordinary transports are lemma7578,
`bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`.
Full-cube forced-span facts and complementary switching are credited to
lemma8020 and independent audit8066, respectively
`bafkreigxn3orr2vhn77fnx2ky2ypv75uxoaeelrxyhahqennzowxykjihy`
and `bafkreigxr7bf7utsniiqpn3uj73dvxbduzzlmh7k6jrl6gro476tzi2y7m`.
The classical maximum-family description is not claimed as new; the
Loeb--Meyerowitz complementary-selector source is cited in PROOF.md.
Prior pendant completions cover additional subclasses; no claim of a
first ordinary-H construction or a historical priority determination is made.

The primary H convention is
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
Its arXiv record was checked live on 2026-10-01 and still lists v1.
Empty is retained as a vertex with a loop; weights may be signed.

## A small Gram LMI for any number of branches

This reduction applies to any r>=2 and t>=2; feasibility will be proved
below for r=3. Index only the N0-1 nonempty vertices initially. In a
branch of star size v<=t, separate its full vertex from its 2v-2 proper
nonempty vertices. On the latter define the centered residual Z_v by

    diagonal: t-2,
    complementary off-diagonal: 2v-t-2,
    all other off-diagonals: -1.

Z_v has row sums zero and complete spectrum

    0 once,
    2v-2 with multiplicity v-2,
    2(t-v) with multiplicity v-1.

For v=1 its domain is empty. For v>=2 these are the constant, centered
pair-constant, and pair-antisymmetric spaces, whose dimensions add to
2v-2. Thus Z_v>=0. This is the complementary-pair decomposition already
proved in UNEQUAL_FACETS.md; no incomplete harmonic quotient is used.

Choose full-vertex vectors h_j of squared norm t-1, with mutual Gram G.
Give a proper vertex in branch j the vector

    g_A=-h_j/(t-1)+w_A,
    Gram(w_A)=[t/(t-1)]Z_(u_j).

All residual spans are mutually orthogonal and perpendicular to the
full-vector span. Their vector sums vanish. The resulting Gram core
C_G is PSD, has diagonal t-1, and has entry -1 on every distinct
intersecting pair. The cross-branch entries are, literally,

    full/full: G_ij,
    full/proper: -G_ij/(t-1),
    proper/proper: G_ij/(t-1)^2.

These pairs are disjoint. Within a branch, a proper complementary entry
is [1+t(2u_j-t-2)]/(t-1), and every other distinct proper entry is -1.
These formulas specify a rational C_G whenever G is rational; the Gram
vectors themselves need not have rational coordinates.

Let E=[-1^T; I], Q_G=E C_G E^T, and

    M_G=(J+Q_G-tI)/(N0-t).

Then Q_G1=0, M_G1=1, and the support prescription holds, including
the empty vertex. Ordinary H follows from J+Q_G>=0.
The cap is equivalent to Q_G<=N0 P, where P=I-J/N0.

Put m_j=2u_j-1, and define the positive diagonal matrix D, column alpha,
and positive definite matrix R by

    D_jj=1+(m_j-1)/(t-1)^2,
    alpha_j=(t-m_j)/(t-1), R=D+alpha alpha^T.           (1)

The empty Gram vector is -sum_j alpha_j h_j. Because the residual sums
vanish, the full frame operator splits orthogonally into residual frames
and the full-vector frame H R H^T, where H has columns h_j and H^T H=G.
Every residual eigenvalue is at most 2t, by the displayed spectrum:

    2t(v-1)/(t-1), 2t(t-v)/(t-1).

Since r>=2, N0>=2t+1>2t. The nonzero spectrum of H R H^T equals that
of R^(1/2) G R^(1/2), including multiplicities. Consequently **within
this architecture** the cap is equivalent to the r-by-r rational LMI

    G>=0, diag(G)=(t-1)1, G<=N0 R^(-1).               (2)

In particular, if G<=(N0-beta)R^(-1) and 0<beta<=N0-2t, the seed has
Q_G<=(N0-beta)P. A different residual bound may permit a larger beta
in a boundary case below. Failure of (2) would only rule out this
architecture, not arbitrary capped H or ordinary H.

## Three branches: complete rational choices

Sort the three stars t>=u>=v, all powers of two; N0=2(t+u+v)-2.
For t=1 all three branches are singletons. The elementary prior matrix
(J_4-I_4)/3 has lower rank1 and upper rank3. Hence assume t>=2.
The following choices cover every remaining dyadic ordering.

**All equal.** Take G=(t-1)I_3. This is precisely the published equal-star
union. The full-vector frame has eigenvalues t+1 twice and 4t-2 once;
residual eigenvalues are at most2t. Since N0=6t-2, beta=2t is valid.

**Two largest equal, t=u>v.** Take

    G=(t-1)*[[1,-1,0],[-1,1,0],[0,0,1]].             (3)

The two maximal full vectors cancel in the empty sum. Their frame
eigenvalue is 2(t+1). The remaining full direction has eigenvalue

    t-1 + [(2v-2)+(t-2v+1)^2]/(t-1) <= 2(t-1).

The inequality follows by convexity in 1<=v<=t/2: the endpoint values
are 2(t-1) and t. Residuals are at most2t. Thus

    beta=N0-2(t+1)>0                                 (4)

is valid. The Gram (3) is PSD of rank2, including v=1.

For the remaining cases t>u, define a positive normalized pair

    a=(t-2u+1)/(t-1), b=(t-2v+1)/(t-1).

Whenever a+b>1 and |a-b|<1, take the balanced Gram

    G=(t-1)*[[1,p,q],[p,1,r],[q,r,1]],
    p=(1+a^2-b^2)/(2a), q=(1+b^2-a^2)/(2b),
    r=(1-a^2-b^2)/(2ab).                             (5)

G*(-1,a,b)^T=0. It is PSD of rank2: its determinant is zero and its
three two-by-two principal minors are positive multiples of
[(a+b)^2-1][1-(a-b)^2]>0. This also follows by constructing a nondegenerate
triangle of side lengths1,a,b. Thus the empty vector vanishes and the
full frame is H D H^T, with two positive eigenvalues.

**Two singleton branches, u=v=1.** Then a=b=1 and (5) is
(t-1)*[[1,1/2,1/2],[1/2,1,-1/2],[1/2,-1/2,1]]. The two full-frame
eigenvalues are (3t+1)/2 and 3(t-1)/2, both at most2t. Hence
beta=2 at N0=2t+2 is valid for all t>=2, including t=2 where the
large residual eigenvalue2t has multiplicity zero.

**Adjacent sizes and v=1, t=2u, u>=2.** Here a=1/(t-1), b=1, so (5)
is valid. The full-frame trace is

    T=3(t-1)+(N0-4)/(t-1)=3t-1/(t-1), N0=3t.

Every full-frame eigenvalue is at most this trace, and every residual
eigenvalue is at most2t. Hence beta=1/(t-1)>0 is valid.

**Adjacent sizes with v>=2, t=2u.** Take G=(t-1)J_3, aligning all
full vectors. The sole full-frame eigenvalue is

    kappa=3t+2(v-1)(2v-3)/(t-1).

It is greater than2t, so the valid positive margin is

    beta=N0-kappa=2(v-1)(t-2v+2)/(t-1)>0.            (6)

This includes u=v. The Gram has rank1; extra lower kernel will be
removed by the mixture, not assumed absent.

**Wide gap, t>=4u.** Use (5). Here 1/2<a<=b<=1, so the triangle is
nondegenerate. Write

    A=t-1, d=t-2u+1, e=t-2v+1,
    D_u=A^2+2u-2, D_v=A^2+2v-2,
    H=4d^2 e^2-(A^2-d^2-e^2)^2,
    E=H*[(A+2)(D_u e^2+D_v d^2)+A D_u D_v],
    F=4d^2 e^2 A^2*[A N0^2-N0(3A^2+N0-4)]+E,
    W=2N0 A-3A^2-N0+4.                              (7)

If lambda1,lambda2 are the two positive full-frame eigenvalues, direct
three-by-three Gram minors give

    T=lambda1+lambda2=3A+(N0-4)/A,
    lambda1*lambda2=E/(4d^2 e^2 A^3),
    (N0-lambda1)(N0-lambda2)=F/(4d^2 e^2 A^3),
    2N0-T=W/A.                                      (8)

For clarity, the product formula uses
sum_(i<j) D_ii D_jj (G_ii G_jj-G_ij^2). In normalized coordinates
the three two-by-two minors of G/A are H/(4A^2 d^2), H/(4A^2 e^2),
and H/(4d^2 e^2), respectively; each full Gram minor is A^2 times this.
Equation(7) collects their common denominator; the checker independently
recomputes these minors and compares the resulting product with (8).

The exact sign certificate substitutes

    v=1+x, u=v+y, t=4u+z, with x,y,z>=0.             (9)

The resulting H,F,W polynomials have respectively **34,219,10 nonzero
coefficients**, all strictly positive integers, and positive constants
243,168399,27. Every coefficient, exponent triple and coefficient-list
hash is supplied in [MARGIN_COEFFICIENTS.json](MARGIN_COEFFICIENTS.json);
[verify_multi.py](verify_multi.py) reconstructs all three polynomials by
exact sparse integer/Fraction arithmetic, compares every coefficient,
and checks the signs. This is a finite exact sign certificate over the
whole orthant(9), not a sampling argument. The largest total degree is
recorded in MULTI_RESULTS.json. Six rational evaluation fixtures provide
an additional expansion/direct-expression check, not the infinite bridge.

Therefore F,W>0. Equations(8) imply lambda1,lambda2<N0: their two
distances from N0 have positive product and positive sum. If lambda1 is
the larger, N0-lambda2<=N0, so

    N0-lambda1 >= F/(4d^2 e^2 A^3 N0).

Combined with the residual bound, the explicit rational choice

    beta=min(N0-2t, F/(4d^2 e^2 A^3 N0))>0           (10)

is valid. This completes all cases: t>u for powers of two means either
t=2u or t>=4u. No continuous sizes in the missing interval are asserted.

## Exact maximal-rank repair

Let C_shift be the direct sum of the original cube complement cores,
with (t-u_j)I added to branch j. It is PSD and has nullity exactly kt:
maximal branches have nullityt, and every other block is positive definite.
Its lift M_shift is ordinary H. No cap for this shifted matrix is assumed.

For any ordinary H core C, an intersecting family of size t has indicator
x with x^T Cx=t(t-1)-t(t-1)=0, hence Cx=0 by PSD. In each maximal cube,
the credited full-cube complementary switches and a maximum-family
indicator span a t-dimensional forced space. These spaces occupy disjoint
branch coordinates and have total dimensionkt. They are exactly
ker(C_shift), and every C_G kills them. Thus a positive mixture of these
two cores has kernel exactly that forced space.

The rational trace bound, valid for any number of branches, is

    q=Tr(Q_shift)
     =(N0-1)(t-1)+sum_j[u_j-1+(t-u_j)(2u_j-1)].

For t>=2 let

    epsilon=beta/[2(beta+q)],
    M=(1-epsilon)M_G+epsilon M_shift.                 (11)

The corresponding core mixture is PSD and has nullitykt, so its lower
slack has rankN0-kt. Every real H matrix has at least this nullity from
the same forced spaces; this proves universal maximality.
The seed satisfies (N0-t)(I-M_G)>=beta P. Since 0<=Q_shift<=qI,
the shifted upper form on 1-perpendicular is at least -qI. Hence

    (N0-t)(I-M)>=beta P/2.                           (12)

The unit eigenvalue is simple, the nonunit upper gap is at least
beta/[2(N0-t)], and all entries are rational. The lower ratio
t/(N0-t)<1 supplies the strict negative-side bound. Entrywise
nonnegativity is not part of the claim. The t=1 prior rank-one baseline
has both strict nonunit bounds directly.

## Arbitrarily many packets, common cores, and products

Suppose r<=3k. Allocate one maximal branch to each of k packets and at
most two of the r-k other branches per packet. A one-branch packet uses
the full-cube complement baseline; a two-branch packet uses the published
two-facet cap; a three-branch packet uses (11). Each packet has largest
star t and forced nullityt. If k>=2, the published equal-star capped-union
closure joins the packets, makes the unit endpoint simple, and adds their
lower nullities to kt. If k=1, r is2 or3 and the corresponding construction
already applies. This proves(A). The equal-star closure supplies an
explicit positive rational scaled upper gap for k>=2, even when a
singleton packet is a full cube with a multiple unit endpoint.

For c>=1, tensor with the complement matrix of the common c-cube.
Petal densityt/N0<1/2 and its unit endpoint is simple. A tensor eigenvalue
-1 must therefore use a common-cube -1 and petal +1. The lower nullity
is exactly2^(c-1). The same argument gives that upper nullity. Cylinders
of common-cube maximum families force precisely this lower nullity in
every real H matrix, proving(B). The factor-only lower kernel proves
the cylinder equality statement, by the credited tensor/Boolean-additivity
argument in PROOF.md. Testing empty petals proves base intersection.

Arbitrary finite products of petal unions certified here and the factors
already covered by PROOF.md / UNEQUAL_FACETS.md are also capped. If their
sizes, stars and forced nullities are N_j,s_j,nu_j, then the maximum
lower rank is

    N_product - sum_(j:s_j/N_j=max_i s_i/N_i) nu_j.

Only eligible-factor cylinders are maximum intersecting families. Each
unit endpoint is simple and all other eigenvalues have magnitude less
than one, so the tensor lower endpoint uses exactly one eligible negative
factor and unit endpoints elsewhere. This application reuses the credited
product theorem; no new general tensor-closure claim is made.

## Replay, coverage, and trust boundary

Run from the repository root with Python3.11+, standard library only:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-downset-1/verify_multi.py --check round-two/six-downset-1/MULTI_RESULTS.json --coefficients round-two/six-downset-1/MARGIN_COEFFICIENTS.json
~~~

The local dependency verify.py is the published parent definition-level
checker and constructor, listed in SHA256SUMS. No peer corpus or solver
is imported. The new checker validates all20 sorted triples of cube orders
1..4, plus(5,4,3),(5,4,4),(6,2,1),(6,3,2), covering all seven regimes.
Every seed and repaired full matrix satisfies the original support,
symmetry, row-sum, lower PSD and upper PSD requirements. Full rational
Schur elimination checks both stated ranks and both quantitative margins.
An independent three-by-three Sherman--Morrison computation checks the
small LMI, including singular Grams. Five larger packet assemblies,
four products, and four common-core sunflowers are checked literally.
The largest matrix has order74. The literal constructor enforces a fixed
order80 guard; this implementation guard does not restrict the theorem.

The universal result rests on complete written pair-space/frame
decompositions, the finite coefficient sign certificate, and the credited
forced-span/transport lemmas. Finite matrix replay alone does not prove
the unbounded quantifiers. The remaining trust boundary is ordinary
unformalized real linear algebra, exact Python arithmetic and the inspected
coefficient-reconstruction/checker code. The work is author-checked and
independently unreviewed. No floating output, timeout, solver status,
resource kill or incomplete enumeration is used as mathematical evidence.
