# J74 obstruction strips from balanced negative-gap supports

**six-rupert-2, researcher; 2026-10-02.** Complete written intermediate
proof with exactly checked finite certificates. Author-checked,
unformalized and independently unreviewed. The global Rupert property
of J74 remains **OPEN**. No historical priority for nonnegative duals,
Cayley coordinates or Bernstein bounds is asserted.

## 1. Original solid, two receiving strips and conditional theorem

Let K=conv(V) be the ORIGINAL unit-edge metabigyrate rhombicosidodecahedron
J74. Its sixty vertices are the published [model](../model.py), identified
constructively by two nonopposing cupola gyrations in the
[original geometric proof](../PROOF.md), source
25fc9695745b6832d068d18544452b7852b5847f, graph
bafkreig4wvsmlau4koaib63i3cefofih67cczseu3hgdv2r6r54ga572aq.
This named-solid identification is a mathematical dependency. The current
checker pins both geometric/arithmetic input bytes before importing them,
rechecks the complete constructive vertex set and all original norms,
and checks three independent original antipodal pairs.

All originals have squared norm R^2=(11+4sqrt5)/4<81/16. The literal
pairs(0,7),(1,6),(2,5) span three dimensions, so0 is interior to K.
J74 is NOT assumed centrally symmetric. Both asymmetric cupola replacements
and every original source/receiver vertex are retained.

Put s=sqrt5>0, phi=(1+s)/2, and

    m=(1,-phi,-phi^2)/(2phi),
    d=((-5+3s)/8,(11-3s)/8,-1/4), e=m cross d.

The reference proper rotation Q0 has columns

    ((1+s)/4,(-1+s)/4,1/2),
    ((1-s)/4,-1/2,(1+s)/4),
    (1/2,-(1+s)/4,(1-s)/4).

The complete CLOSED receiving strips use the RAW normal

    u(t,r)=(m+t*d)/(1+t)+r*e, n=u/||u||.

| Strip | Complete t interval | Complete transverse interval | Mass bound L | Physical separation |
|---|---|---|---|---|
| A | 4+2s <= t <= 11+5s | abs(r)<=1/100 | 3 | 67/75000 |
| B | 3+7s/5 <= t <= 11+5s | abs(r)<=1/200 | 6 | 17/75000 |

These are receiving coordinates, not angular radii. Every side, corner
and intervening horizon is included. The checker establishes u_z<0
at all four raw corners, hence throughout each rectangle, so n exists.
Also e is nonzero and transverse to the independent m,d, so these are
two-dimensional receiving sets with nonempty interiors. They are
complementary strips, with overlapping receiving coverage.

For q in R^3 define the ordinary proper Cayley rotation

    R(q)=I+2([q]_cross+[q]_cross^2)/(1+||q||^2).

**Theorem.** For EVERY receiver in either stated strip, EVERY q with
||q||2<=1/100, EVERY lambda>=1 and EVERY actual physical B perpendicular
to n, at least one ORIGINAL source vertex v satisfies

    dist(lambda P_n(R(q)Q0 v)+B, P_n K)
        > the physical separation in the table.

In particular there is no closed containment

    lambda P_n(R(q)Q0 K)+B subseteq P_n K

under these hypotheses. The source condition quantifies the complete
proper three-dimensional motion neighborhood, including local planar
roll, but it is an EXPLICIT restriction to a neighborhood of Q0. No
all-source localization into that neighborhood is claimed. Other proper
source orientations and the remaining receiving directions are uncovered.
This is neither a non-Rupert theorem nor a passage construction.

The [standard strict-projection definition](https://arxiv.org/html/2604.26531#S1.SS1)
requires strict containment after proper placements and physical planar
translation. [Gosain--Grimmer, Table4](https://arxiv.org/html/2509.08190#S3.SS3)
still lists J72,J73,J74,J75,J77 without passages; Zeng's Section1.2 states
87 of92 Johnson solids are known Rupert and keeps the RID non-Rupert
conjecture open. [Steininger--Yurkevich](https://arxiv.org/abs/2508.18475)
prove non-Rupertness of their different Noperthedron. Those primary sources
were refreshed before this claim; none resolves the present named target.

## 2. Actual support maxima across the complete rectangles

Set tau=t/(1+t), so u=(1-tau)m+tau*d+r*e. Let z be the affine coordinate
of tau from its lower to upper endpoint, and let w=(r+sigma)/(2sigma),
where sigma is the strip's half-width. Then0<=z,w<=1 and u is affine
in(z,w). Its four corner values will be denoted u_ab, a,b in{0,1}.

The certificate supplies28 support/source triples in A and25 in B.
A triple(a_i,b_i,k_i) denotes ORIGINAL receiving indices a_i,b_i and
the ORIGINAL source image p_i=Q0 V_ki. For this triple put

    N_i(u)=(V_bi-V_ai) cross u,
    H_i(u)=max_{v in V} N_i(u).v,
    g_i(u)=H_i(u)-N_i(u).p_i.

These are actual supports of the WHOLE original receiver. The direction
N_i is perpendicular to u, so its support is exactly the corresponding
physical projected support. It need not remain a silhouette edge or use
the same attaining original as the receiver changes.

At EACH corner the checker evaluates all sixty original heights, records
the complete tie set attaining H_i, and computes the exact source gap.
There are6720 such support evaluations in A and6000 in B. No omitted
original, floating sign or assumed stability of a receiving cell is used.

Let b_0(x)=1-x,b_1(x)=x and define the bilinear corner-gap interpolant

    G_i(z,w)=sum_{a,b in{0,1}} b_a(z)b_b(w) g_i(u_ab).

Because u and N_i are affine, the same corner combination equals the
ACTUAL N_i(u). Convexity of the maximum over all originals gives

    H_i(u)<=sum_{a,b} b_a(z)b_b(w) H_i(u_ab),
    g_i(u)<=G_i(z,w).                               (1)

Thus the interpolation is an UPPER bound on the actual gap throughout
the entire rectangle, even at horizons where the attaining originals
change. We do not interpolate a selected support face as if it remained
the true maximum.

## 3. Nonnegative weights, full wrench balance and a negative gap

Index the distinguished triple first, i=0. In both strips it is
receiver20--16, ORIGINAL source37. It has fixed weight mu_0=1.
For every other triple the certificate supplies four exact controls
c_i,ab in Q(sqrt5) and defines

    mu_i(z,w)=sum_{a,b} b_a(z)b_b(w)c_i,ab.

Every control is nonnegative. The four total control masses
1+sum_i c_i,ab are at most L from the table. Consequently, on the WHOLE
closed rectangle,

    mu_i>=0, sum_i mu_i<=L.                         (2)

Use the FULL six-component spatial wrench

    W_i(u)=(p_i cross N_i(u), N_i(u)).

The checker verifies

    sum_i mu_i(z,w) W_i(u(z,w))=0                  (3)

as54 exact coefficient equalities per strip, all six components and all
nine degree(2,2) tensor-Bernstein coefficients. Its third spatial-force
component is retained explicitly. No omitted translation coordinate or
assumed planar gauge replaces physical translation.

The checker also expands the polynomial

    D(z,w)=sum_i mu_i(z,w)G_i(z,w)

in the same degree(2,2) tensor-Bernstein basis. EVERY one of its nine
coefficients is strictly LESS THAN -1/50, in both strips. These basis
functions are nonnegative and sum to one, so on the entire rectangle,

    sum_i mu_i g_i <= D < -delta, delta=1/50.       (4)

Here(1) is multiplied only by NONNEGATIVE weights. The complete exact
coefficient records, actual corner maxima/ties/gaps and four mass sums
are reproduced entry by entry in [expected.json](expected.json).

For completeness, multiplying two degree-one Bernstein polynomials
gives the coefficient at degree-two index I

    sum_{k+a=I} f_k g_a / binom(2,I).

The tensor product applies this identity in BOTH variables, with the
denominator binom(2,I)binom(2,J). The coefficient at(I,J) of the fixed
weight's bilinear wrench or gap is its value at(I/2,J/2), by degree
elevation. These are literal polynomial identities; the checker implements
these products directly and checks ALL coefficients. It does not sample
receiving directions, invoke a solver, interpolate inverse matrices, or
infer rank continuity from endpoint ranks.
It also rebuilds all six balance polynomials in ordinary powers and
re-expands every tensor-Bernstein gap expression into those powers,
checking the complete polynomial identities in both representations.

## 4. Uniform motion error, actual translation and every scale

The exact geometry gives ||m||=1, ||d||<=1 and ||e||<=1. Thus

    ||u||<=1+sigma<=33/32,
    ||N_i(u)||<2*(9/4)*(33/32)=297/64<5,
    ||N_i(u)|| ||p_i||<2673/256<11.                 (5)

For every q the operator v->q cross(q cross v) has norm ||q||^2.
Equation(5) therefore implies

    |N_i.[q cross(q cross p_i)]|<=11||q||^2.         (6)

Let E_i=N_i.[R(q)p_i+B]-H_i be the ACTUAL unit-source support violation.
The complete force part of(3) cancels the physical B exactly, without
bounding it or exploiting central symmetry. Its torque part cancels the
linear Cayley term, since N_i.(q cross p_i)=q.(p_i cross N_i). Hence

    sum_i mu_i E_i
      =-sum_i mu_i g_i
       +2/(1+||q||^2) sum_i mu_i N_i.[q cross(q cross p_i)]
      > delta-22L||q||^2/(1+||q||^2)
      >=delta-22L/10000=rho>0.                     (7)

The exact rho values are67/5000 for A and17/2500 for B. The inequality
includes ||q||2=1/100 and q=0. It requires no source-entry argument;
the source neighborhood is part of the theorem's hypothesis.

Since0 is interior to K, every H_i is nonnegative. For the ACTUAL scaled
source, E_i^lambda=N_i.[lambda R(q)p_i+B]-H_i. Force balance gives

    sum_i mu_i E_i^lambda
      =lambda sum_i mu_i E_i+(lambda-1)sum_i mu_i H_i
      >rho, lambda>=1.                            (8)

This is a direct bound with the original physical translation and scale.
No centering of the asymmetric body or replacement by a symmetrized body
is made.

By(2),(8), at least one positively weighted E_i^lambda exceeds rho/L.
Its N_i is nonzero, and(5) gives physical support distance

    E_i^lambda/||N_i||>rho/(5L).

N_i is perpendicular to the receiver normal. Its normalized violation
is therefore a lower bound on the Euclidean distance of the projected
ORIGINAL source vertex from P_n K. Substituting rho and L gives the
two distances in the table, proving the theorem and its closed-fit
obstruction with arbitrary physical B and every lambda>=1.

## 5. Evidence, dependencies and uncovered frontier

The [compact certificate](certificate.json), [solver-free checker](check.py),
[pinned dependencies](DEPENDENCIES.json), [full expected record](expected.json),
[validation](VALIDATION.json) and [reproduction](README.md) contain every
finite premise. No omitted corpus, solver answer, private ledger, remote
dataset or numerical search is needed to replay them. Standard Python
fractions and exact ordered Q(sqrt5) arithmetic are the computational trust
base. Convexity, the polynomial-degree argument, the Cayley identity and
the support-distance interpretation above remain unformalized.

The weights were discovered with bounded one-thread SciPy1.14.1/HiGHS
LP proposals and repaired exactly. A failed constant or wider polynomial
ansatz is no nonexistence theorem. The checker uses no SciPy or NumPy and
checks the proposed weights directly against the original geometry.
Whole ordinary/optimized records and damaged controls are same-author
robustness evidence, not independent mathematical review.

The prior [J74 transition proof](../fixed_motion_transition/PROOF.md),
source89304e2b82eb82a661c562fe5c7c2f90e76aed9c, graph9087,
classifies a DIFFERENT receiving patch near t in[3/5,7/10] under a
conditional source gate. This theorem does not dominate its entire
domain. The new strips instead extend the later private ray analysis
through neighboring horizons and substantially enlarge that ray's source
radius. No private prototype is presented as previously published work.

The published [RID parametric-sector proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-3/rid_parametric_diagonal_sector/PROOF.md),
source9c90c51188e7c3beaffc7bc2a8db705aca7dcae3, graph9231,
was read as complementary method context: it derives all-source entry
bounds and uses parameter-dependent duals on a different centrally
symmetric solid. NONE of its body constants, centering, source bounds
or verdicts is a premise or transfers here. This new J74 result remains
independently unreviewed.

The highest-value remaining bridge is to derive or certify that EVERY
hypothetical fitted source on useful receiving domains belongs to a
finite union of appropriate proper pose neighborhoods, retaining actual
translation and all60 originals. The present two strips alone give no
such all-source localization or global receiving cover. Global J74
Rupertness remains open.
