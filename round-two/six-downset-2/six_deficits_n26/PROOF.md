# A rank-nine original PSD cut for the n26 transport

Actual author **six-downset-2**, role **researcher**, 2026-10-03.
Status: exact integer author certificate and ordinary unformalized proof;
independent review of this new result is pending.

**Theorem.** On the specific original 36-coordinate invariant face below,
every H matrix satisfies the proper-coefficient-only inequality in
[CERTIFICATE.json](CERTIFICATE.json). Its rank-nine positive semidefinite
dual is independent of all 36 coefficients. The thirty proper values
obtained by the declared normalized transport of the published n24
certificate violate that inequality. Consequently **no choice of the six
real deficits** repairs that fixed thirty-coefficient slice, even for
ordinary uncapped H. The whole 36-real-coordinate face remains open.

## Original face and quantified domain

Let D={A subset[26]: |A|<=24}, including the actual empty vertex. Put

    N=67108837, s=33554406, h=N-s=33554431.

Let d8,...,d13 and all thirty t[a,b] below be arbitrary independent REAL
numbers. For 2<=a<=13 put

    B[a,26-a]=B[26-a,a]=s-d_a    if a in8,...,13;
    B[a,26-a]=B[26-a,a]=s        if a in2,...,7.

For a<=b, a+b<26 and a,b in {8,...,18}, set B[a,b]=B[b,a]=t[a,b]. These
are exactly the thirty proper labels in CERTIFICATE.json. Set every
other nonsingleton entry to zero. Recover all singleton entries from the
original point-star equations:

    B[1,a]=s-sum_{b=2}^{24} b B[a,b] C(26-a,b)/(26-a),   a>=2;
    B[1,1]=s-sum_{b=2}^{24} b B[1,b] C(25,b)/25.

Define the ORIGINAL matrix L by L[A,A]=s for nonempty A, L[A,T]=B[|A|,|T|]
for distinct disjoint nonempty A,T, and zero for intersecting distinct
nonempty A,T. The actual empty row and permitted loop are

    e_a=L[empty,A]=N-s-sum_b C(26-a,b)B[a,b];
    ell=L[empty,empty]=N-sum_a C(26,a)e_a.

All original rows are N and all original point-star sums are s, including
the empty star. The singleton equations give the outside star rows;
inside star rows have their single diagonal contribution s. The checker
reimplements these equations and compares every entry and every empty
entry with the credited public decoder at all37 affine-basis probes.
There is no sign, centering, box, rationality, cap, strict-gap or rank
hypothesis on these real competitors.

M=(L-sI)/h has the original symmetry, intersecting zeros and unit rows.
Original H would require L>=0. The extra upper cap L<=NI is not used in
this theorem. The declared proper-support face is a hypothesis; the
theorem does not say that every n26 H matrix belongs to this face.

## Nine explicit original directions

For an integer profile z1,...,z24, write

    F_z(empty)=0;
    F_z(A)=z_|A| (1_[1 in A]-1_[2 in A]).

Use the two profiles

    u=(0,0,0,0,0,0,0,525,-533,-538,541,1,-26,1,541,-538,-533,525,0,0,0,0,0,0);
    v=(3,0,0,0,0,0,0,0,0,0,0,7,7,7,0,0,0,0,0,0,0,0,0,0).

Let e_empty be the indicator of the actual empty vertex. For i=8,...,13
let A_i={1,...,i}, T_i=[26]\A_i and H_i=e_{A_i}-e_{T_i}. Both endpoints
are vertices of D. Their exact original energies are

    H_i' L H_i=2d_i,             e_empty' L e_empty=ell.

Take the positive integer weights

    mu=42186, w=2518;
    (lambda8,...,lambda13)=
      (14519995358,30698088454,55869155606,
       86305367440,107807092424,58518767888).

The parameter-independent original matrix

    Y=F_u F_u' +mu F_v F_v' +w e_empty e_empty'
        +sum_{i=8}^{13} lambda_i H_i H_i'

is PSD as a positive sum of original outer products. It has rank exactly
nine. Indeed, its nine defining columns have a nonzero9-by9 minor at the
original vertices empty, {1}, {1,3,4,5,6,7,8,9}, A8,...,A13. In column
order F_u,F_v,e_empty,H8,...,H13 its determinant is -1575. Positive
weights do not change their span. No compressed harmonic rank is being
substituted for original rank here.

## Literal energy and cancellation

Direct counting in the original matrix gives, for any fixed integer z,

    E_z=F_z' L F_z
       =2s sum_a C(24,a-1) z_a^2
          -2 sum_{a,b} B[a,b] C(24,a-1) C(25-a,b-1) z_a z_b.

For a diagonal term there are2 C(24,a-1) sets containing exactly one of
the two distinguished points. For a disjoint ordered pair with nonzero
product, the two points must occur on opposite sides. Each of the two
opposite sign choices has C(24,a-1)C(25-a,b-1) ordered pairs, and their
product of signs is -1. This accounts for the factor and the sign.
Binomials outside their ordinary range are zero. Actual empty terms
vanish because F_z(empty)=0; the actual empty energy is separately
retained with positive weight w.

The six deficit coefficients in these exact affine energies are:

| i | coefficient in E_u | coefficient in E_v | coefficient in ell |
|---|---:|---:|---:|
|8|381579660000|12459744|-371821450|
|9|835756883676|26476956|-799884800|
|10|1513796751104|47070144|-1434168450|
|11|2296089469344|70605216|-2163324800|
|12|9984576|159753216|-2762102200|
|13|3656018912|86532992|-1497686400|

For each row, exactly

    coeff_i(E_u)+42186 coeff_i(E_v)+2518 coeff_i(ell)+2lambda_i=0.

One can obtain the first two columns directly: for i<13, the coefficient
in E_z is4 C(24,i-1)(z1-z_i)(z1-z_{26-i}); for i=13 it is
2 C(24,12)(z1-z13)^2. Substitution in the actual empty equations gives
the third column. Thus

    tr(Y L)=E_u+42186 E_v+2518 ell+2sum_i lambda_i d_i
           =P(t)
           =48666235273558+sum_{30 proper labels} K[a,b] t[a,b].

All thirty exact integer K[a,b], in complete label order, are in
CERTIFICATE.json. The checker regenerates the whole affine expression
before comparing it. Every parameter appears affinely in B, the actual
empty entries and this fixed-vector energy, so all37 rational basis
checks identify the expression for **every real** parameter vector.
This is an affine-identity argument, not finite sampling of feasible
matrices or a rational-only nonexistence conclusion.

If L were PSD then each of its nine original quadratic energies would
be nonnegative. Therefore tr(Y L)>=0 and P(t)>=0 on the entire declared
real face. No harmonic completeness, mean projection or upper cone is
needed for this necessary inequality.

## The excluded thirty-coefficient slice

Let t be the exact thirty rational values recorded in CERTIFICATE.json.
Their provenance is the n24 certificate10080: labels (a,b) shift to
(a+1,b+1), retaining the invertibly scaled coordinates

    sigma_n(a,b)=n/max(C(n-a-1,b-1),C(n-b-1,a-1));
    t26[a+1,b+1]=t24[a,b] sigma26(a+1,b+1)/sigma24(a,b).

The pinned public n24 data are credited, not a new baseline result.
The checker reproduces all thirty values exactly. Substitution gives

    P(t)=-274356636025866281341291/98175000000 <0.

This value is independent of d8,...,d13. It contradicts lower PSD for
every real choice of those six numbers. In particular, changing a
common factor, recovering six unrelated rational deficits, relaxing the
upper cap, or increasing a solver budget cannot repair this fixed
thirty-coefficient slice. At least one proper coefficient must change
in any original H witness in this declared face.

## Verification and limits

[verify.py](verify.py) uses only CPython's standard-library integers and
Fraction. It reads the compact defining data and three hash-pinned,
already published public dependencies listed in [CREDITS.json](CREDITS.json).
No numerical proposal, dual, large proof corpus or private data is an
input. The all37 original affine-basis comparisons cover23125 full table
entries and every actual empty entry. A credited literal n8 original
matrix8319 supplies a cold247-vertex/61009-entry control, two literal
signed-profile energies, all three complement-difference energies and
the actual empty-indicator energy. This is validation, not new n8 work.
Eight altered certificates are rejected in each isolated normal/-O
mode; their entire6690-byte mathematical records are identical.

A single full original28-cone six-deficit floating solve suggested the
direction; its status was optimal_inaccurate and its negative objective
was **not** accepted as nonexistence. A rational dual recovery and one
deterministic integer coarsening supplied the explicit certificate above.
The theorem follows from the exact original identity and positive
weights, independently of the solver status or tolerances.

Primary problem: [Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [version history](https://arxiv.org/abs/2609.28404) was rechecked live
2026-10-03: v1 of2026-09-23 remains the listed version. H and I are
separate proposed spectral conjectures. The primary classical Chvatal
theorem does not supply this matrix. Star-only recovery9365 and generic
face/model10008 are credited; the exact n24 source10080 supplies defining
data. This proof uses none of their harmonic-completeness conclusions.

The new theorem is a proper-only necessary cut and an exact exclusion of
one prescribed six-real-parameter repair slice. It is not full36-face
infeasibility, a counterexample to H/I, n26 minimum-class unattainability,
an all-order classification, or historical-priority claim. The ordinary
counting, affinity, original-vector rank and PSD arguments remain
unformalized. CPython/Fraction execution and the credited control are
explicit additional trust boundaries; same-author replays are not
person-independent review. General H and the remaining n26 target stay
open.
