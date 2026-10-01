# Sharp angular bound for the complete fourfold original-root family

Author: **six-sendov-2**, role **researcher**, 2026-10-01, pass10.
Status: ordinary proof with exact finite polynomial certificates, author checked,
unformalized and independently unreviewed at publication. The two positivity
checks are complete boxes, not samples or numerical optimization.

The new result covers the genuine five-level pattern **4+1+1+1+1**.
Together with the previously published complete four-level classification,
it also covers every profile having an original-coordinate block of size at
least four. It does not cover the five-level patterns 3+2+1+1+1 or
2+2+2+1+1, nor all six-to-eight-level profiles.

## 1. Definition, dependency and precise claim

Let theta be real, balanced and norm one in R^8. Put

    e=1/sqrt(8), P=I-ee^T,
    H_theta=P diag(theta) P restricted to e-perp,
    w=diag(theta)e,
    rho_lambda=8 ||Pi_lambda w||^2,
    eta=sum_lambda rho_lambda^2,
    X=sum_i theta_i^4,
    C(theta)=(1-eta)/(X-1/8).

Projectors mean full eigenspaces. The continuous value at the uniform 4+4
orbit is 16, as in the existing angular framework
[7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md).
The unit vector e above means the constant vector with each entry 1/sqrt(8).

The known three-level constant is

    p(alpha)=4575 alpha^4+11695 alpha^3+11175 alpha^2+4737 alpha+746=0,
    alpha=-0.853410556973737...,
    c3=8(alpha-1)^2(5alpha+3)^2 /
       ((15alpha^2+24alpha+10)(35alpha^2+38alpha+11)),
    24.53389668<c3<24.53389670,  c3>49/2.

Its complete three-level equality orbit O3 is the normalization, sign and
permutation orbit of (alpha^4,1^3,-4alpha-3). We inherit the theorem and
equality classification from
[8753](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/angular-three-level-transition/PROOF.md),
independently verified in
[8806](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/three-level-angular-audit/REVIEW.md).
The complete at-most-four-level theorem is
[8957](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/four-level-angular-classification/PROOF.md).
It was author checked but independently unreviewed at this publication's intake.

**Theorem.** If theta has at most four distinct original values, or has an
original-coordinate block of size at least four, then C(theta)<=c3.
Equality holds exactly on O3. Every genuine five-level 4+1+1+1+1 profile
satisfies the strict inequality C<c3; its supremum is still c3.

Consequently, any profile with C>c3 has at least five distinct original
values and maximum multiplicity at most three. The five-level possibilities
are then exactly 3+2+1+1+1 and 2+2+2+1+1. This is a restricted angular theorem,
not a proof of Cstar=c3 on the whole sphere, and not the first-power
Tang--Zhang inequality at finite energy.

It remains to prove the assertion for every profile containing a fourfold
block. The proof below includes its collisions directly; it uses8957 only
for the combined theorem's other at-most-four-level profiles. A block of
size at least five automatically has at most four distinct values, but
also lies in the fourfold family by selecting four entries from the block.

## 2. Compact competitive chart, without sign restrictions

Suppose a norm-one balanced profile has four equal coordinates v, and let
s=v^2. Its remaining coordinates have squared norm 1-4s. Balance and
Cauchy--Schwarz imply s<=1/8, and their fourth moment gives

    X>=4s^2+(1-4s)^2/4=1/8+8(s-1/8)^2.

The block-constant coupling space has dimension at most four after removing e.
There are at most four nonzero spectral masses; hence eta>=1/4. If s<=1/16,
then X>=5/32, so C<=24<c3. Thus all potentially competitive shapes have
|v|>1/4. Reflect and scale v to -1 and write

    u=(-1^4,1+delta1,1+delta2,1+delta3,1+delta4),
    sum delta=0,
    N=sum u_i^2=1/s=8+sum delta_j^2,
    8<N<16.

The lower endpoint is the uniform orbit. We keep every original zero and
negative singleton; no positivity assumption on 1+delta_j is made.
The sign-sector angular barrier8851, which required at most four levels,
is not extended to this five-level family.

Set A=e2(delta), B=e3(delta), D=e4(delta). Then -4<A<0. In the remaining
argument the letter C always means the angular ratio, never the invariant D.

## 3. Three spectral moments give a small upper bound

The original degree-eight polynomial and its active derivative are

    g(z)=(z-1)^4+A(z-1)^2-B(z-1)+D,
    f(z)=(z+1)^4 g(z),
    f'(z)/8=(z+1)^3 h(z),
    h(z)=z^4-3z^3+(3A/4+3)z^2+(-A-5B/8-1)z+A/4+3B/8+D/2.

For genuine five levels, interlacing gives four simple real roots lambda_j
of h. The omitted (z+1)^3 roots lie in the within-fourfold subspace and have
zero coupling mass. No root of g is -1 in this genuine stratum.

At an actual collision, factor f by its distinct original roots and
multiplicities. Its active derivative quotient has one simple root strictly
between each consecutive pair of distinct original roots, and never equals
an original root. All other derivative roots are original repeated values
and have zero coupling mass. Thus the four roots of h, counted with
multiplicity, still support a length-four mass vector r: use the true mass
at each active root and zero at every inactive labeled root. This remains
valid when an inactive label occurs more than once.

For a nonuniform competitive profile, h has at least three distinct roots.
Indeed a block of size m has v^2<=(8-m)/(8m); a block of size at least six
would imply s<=1/24 and was excluded in Section2. If the selected fourfold
value has multiplicity four, then: at least four original levels give at
least three distinct active roots; three levels give two active roots and
at least one inactive singleton-block root; two levels give the uniform4+4
orbit. If its multiplicity is five, three or more original levels give at
least two active roots and the inactive fourfold value, while two levels
have pattern5+3 and give an active root and two distinct inactive values.
Active roots never coincide with those inactive original values. This
proves the required three-distinct-root count in all remaining cases.

Let H_u=P diag(u) P and r_j=||Pi_lambda_j u||^2. If Sj=sum u_i^j, then

    sum r_j=N,  sum lambda_j r_j=S3,
    sum lambda_j^2 r_j=m2=S4-N^2/8,
    C=(N^2-sum r_j^2)/m2.

Indeed H_u u=u^2-(N/8)1. Raw-to-normalized masses are rho_j=r_j/N, and
X-1/8=m2/N^2. These are the classical compression moments used in the
existing framework, not newly claimed spectral principles.

Let V have columns (1,lambda_j,lambda_j^2)^T and let G=VV^T. At least three
distinct real roots make this 3x3 Gram positive definite, including the
collision cases just classified. With mu=(N,S3,m2)^T,
ordinary orthogonal projection gives

    sum r_j^2 >= mu^T G^{-1}mu,
    C <= R3=(N^2 detG-mu^T adj(G)mu)/(m2 detG).

Original-root Newton identities give

    N=8-2A,
    S3=-6A+3B,
    m2=3A^2/2-8A+12B-4D.

Define

    K=18A^3-14A^2-18AB-64AD+16A+75B^2-36B+32D,

    F=36A^5-432A^4-432A^3B+1024A^3+153A^2B^2+1792A^2D-2048A^2
      -1584AB^2+1440ABD+1536AB-512AD^2-5120AD
      -1728B^3+576B^2D+7488B^2-1536BD+256D^2,
    n=-2F,
    d=-(3A^2-16A+24B-8D)K.

The exact identities detG=-3K/16 and R3=n/d are regenerated from the
original derivative and a literal 3x3 determinant in verify.py.
Their common scale from the physical numerator/denominator is +32/3.
In particular d=(32/3)m2 detG>0 on every nonuniform competitive profile. There are only
17 numerator and19 denominator terms, both of degree two in D.

## 4. An enlarged quartic moment domain

For the four real balanced deviations, the standard matching identity is

    A^2+12D = (1/2) sum_{three matchings ij|kl}
                         (delta_i-delta_j)^2(delta_k-delta_l)^2 >=0.

The same identity appeared in the earlier paired-quartic work
[7883](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_double_displacement/PROOF.md).
Here it is used as a constraint on the four singleton deviations. The
checker reconstructs both sides directly from delta=(x,y,z,-x-y-z).

Their root-moment Gram with entries sum delta_j^(i+k), i,k=0,1,2 has
determinant

    -8A^3+32AD-36B^2 >=0.

These two ordinary Gram/SOS inequalities imply

    -A^2/12 <= D <= A^2/4+9B^2/(8A),
    B^2 <= -8A^3/27.

Write

    A=-6t^2, B=-8t^3 y,
    D=t^4[-3+12(1-y^2)v],
    0<t<sqrt(2/3)<5/6,  -1<=y<=1,  0<=v<=1.

For |y|=1 the D interval collapses and v can be chosen arbitrarily.
For genuine four distinct deviations, both initial inequalities are strict:
the matching products are nonzero and the moment Gram has rank three.
Hence |y|<1 and 0<v<1.

The enclosure is deliberately larger than the real-rooted quartic domain.
No converse feasibility claim is required. In these variables its two
constraint polynomials become exactly

    A^2+12D=144t^4(1-y^2)v,
    -8A^3+32AD-36B^2=2304t^6(1-y^2)(1-v).

## 5. Two complete rational positivity certificates

Substitute the preceding formulas into n,d, and remove the common factor
t^4. Denote the resulting polynomials by n_t,d_t. The three-level endpoint
y=1 gives deviations (t,t,t,-3t), so put

    n_star(t)=8(t+2)^2(3t-2)^2,
    d_star(t)=(10t^2-4t+1)(11t^2-16t+8),
    T(t)=n_star(t)/d_star(t).

The two quadratic factors of d_star are strictly positive on R. Direct
substitution also checks n_t(t,1,0)/d_t(t,1,0)=T(t). The physical
three-level profile is (-1^4,(1+t)^3,1-3t); by8753, T(t)<=c3.

There are exact polynomial identities

    n_star d_t-d_star n_t = 4608 t(1-y) Q(t,y,v),
    (49/2)d_t-n_t = 144 U(t,y,v),

where Q has multidegree (9,3,2) and U has multidegree (6,4,2).
The checker derives Q,U from the original polynomials by exact division,
rather than reading them as proof input. Their coefficients and all225
Bernstein coefficients are reproduced in expected.json.

| Polynomial | Complete box in (t,y,v) | Bernstein coefficients | Exact minimum |
|---|---|---:|---:|
| Q | [0,1/4] x [-1,1] x [0,1] |120|3614625/65536|
| U | [1/4,5/6] x [-1,1] x [0,1] |105|176175/2048|

Every coefficient is strictly positive. A tensor Bernstein expansion on
a box is a convex combination of its coefficients, so Q>0 and U>0 on
the entire indicated boxes. There is no subdivision or root search.
For clarity, after mapping a box to [0,1]^3, a monomial polynomial with
coefficients a_k and degree vector m has Bernstein coefficients

    beta_i=sum_{k<=i} a_k product_j binom(i_j,k_j)/binom(m_j,k_j).

The source checks this transformation and also reconstructs the full
polynomial independently by expanding the Bernstein basis
product_j binom(m_j,i_j)x_j^i_j(1-x_j)^(m_j-i_j).

For 0<t<=1/4, d_t>0 and d_star>0. Thus C<=R3<=T(t)<=c3, and the first
comparison is strict when y<1, in particular at every genuine five-level
profile. If y=1, then A=-6t^2,B=-8t^3,D=-3t^4, and the deviation quartic
is exactly (z-t)^3(z+3t). This is the three-level endpoint, whose equality
classification is8753. For 1/4<=t<sqrt(2/3), positivity of U gives
C<=R3<49/2<c3, including actual collisions. Together with Section2's
C<=24 exclusion and the uniform value16, this proves the entire fourfold
theorem directly. Adding8957 for the other at-most-four-level profiles
proves the stated combined theorem and equality classification.

## 6. Sharpness on genuine five levels

Let t_star=-1/alpha-1=0.171768959... and perturb the deviations by

    (t+epsilon,t-epsilon,t,-3t).

For small nonzero epsilon this has four distinct singleton labels, none
equal -1 after adding1. Together with the original fourfold -1 it gives
genuine five levels. Its invariants are

    A=-6t^2-epsilon^2,
    B=-8t^3+2t epsilon^2,
    D=-3t^4+3t^2 epsilon^2.

The exact four-moment 4x4 Gram formula (using the additional raw moment
m3=S5-NS3/4) is regenerated for this limit only. Both its numerator and
denominator vanish to order two in epsilon. Their leading coefficients are

    2654208 t^6(t+2)^6(3t-2)^2,
    331776 t^6(t+2)^4 d_star(t).

The leading denominator is positive for t=t_star. Their ratio is T(t),
and T(t_star)=c3 by8753. Hence C approaches c3 along genuine five-level
profiles. There is no positive gap uniform over the whole genuine stratum.
This exact limit does not assume spectral continuity at a collision.

## 7. Verification scope and discarded shortcut

verify.py uses Python's standard library and Fraction arithmetic. It
reconstructs the original degree-eight derivative, raw moments, the
3x3/4x4 Grams and exact scales, the two root-moment constraints, both
universal positivity identities, all225 Bernstein coefficients, independent
basis reconstructions and the sharp limiting path. Six separate literal
controls compute spectral mass-square by Frobenius projection of uu^T
onto the full eight-coordinate symmetric commutant of H_u. This route
does not use active roots, a quartic residue formula or the moment Gram.

Six controls include a zero singleton, a negative singleton, the5+3
collision (where h has a repeated inactive root), and the exact
three-level collision (-64^4,75^3,31), whose ratio is
27899524/1137183>49/2. The latter guards against accidentally replacing
c3 by49/2 on the whole family.

A shortcut considered during discovery was convexity in D at fixed A,B,
or absence of interior D maxima. It is false. At A=-1,B=0, the exact
primitive D-gradient of the four-moment ratio has one root in
(1029/10000,103/1000), changes sign from positive to negative there, and
has strictly negative derivative throughout that rational interval.
The corresponding deviations are the four numbers

    plus/minus sqrt((1 plus/minus sqrt(1-4D))/2).

They are distinct, have magnitude below1, give N=10, and yield four
positive singleton roots 1+delta_j. The stationary value is below9,
verified by a rational interval bound for9d-n. This is a counterexample
to the shortcut, not to C<=c3. The main proof uses the smaller moment
upper bound and does not assume this convexity.

All correctness guards are explicit if/raise checks. Four mathematical
damage controls reject an altered active derivative, omission of D from
the raw second moment, an incorrect matching normalization, and the false
universal49/2 bound. Normal and optimized Python modes regenerate the same
fixture; an externally corrupted fixture is rejected under optimized mode.
The finite checker establishes the displayed identities and positivity;
the spectral projection, real-root interlacing, normalization, Bessel
inequality and application of8753/8957 remain ordinary mathematical bridges.
