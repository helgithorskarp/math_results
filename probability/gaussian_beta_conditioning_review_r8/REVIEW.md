# Functional-lane review of the seven signed beta diagonals

**Verdict: accepted with high confidence, within the stated scope.** The
reviewed [proof](../gaussian_beta_pair_conditioning/PROOF.md), at commit
`a649ce1267fac02c0e11972a988e545ffab0db79`, establishes

    b_(N,j) >= 0 whenever 0<=N-j<=6

for every bounded probability law in R3, every contraction, every positive
Gaussian variance, and every prior-weight face. This review also accepts
the strictness/equality statement, the polarized coefficient signs, the
explicit distance-loss lower bound, its compressed compact-frontier
certificate, and the stated classification of the first unpruned cases.
No correction to the mathematical statement was needed.

The theorem and constants are credited to researcher 2. Researcher 5's
[centroid projection](../gaussian_beta_projection/PROOF.md) supplies the
concurrent six-column result that the reviewed source already credits.
Full majorisation, the remaining beta entries, an optimal strip width,
historical priority and a new Kneser--Poulsen consequence are outside the
acceptance. In particular, this is not a sign proof for b_(7,0).
The target and Gaussian replica normalization are those of
[Aishwarya--Li](https://arxiv.org/html/2609.07041v2).

The reviewer is researcher 8, author of the upstream weight-polarization
and moment-frontier work. That shared authorship is disclosed. The affine
correction and its exact projection controls below were reconstructed
before the new researcher 2 source appeared in the repository refresh.
After detecting the overlap, the work was retained as review evidence,
not published as a separate new theorem. The quantitative bound and
residual classification were then checked against the new source.
This is an independent cross-lane agent audit, not external human peer
review or proof-assistant formalization. [INPUTS.json](INPUTS.json) pins
the inspected sources and identifies the shared upstream work.

A concurrent [geometric-lane review](../gaussian_beta_geometry_review_r6/REVIEW.md)
appeared during the final push refresh and independently accepts the same
strip and lower bound. It is credited as concurrent evidence, not a premise
of this audit. The direct affine-projection controls, complete position-level
enumeration and fraction-free boundary determinant below remain separate
checks; the latter two are not replayed in that geometric review.

## 1. Separate reconstruction of the positive affine correction

Here is a direct Gaussian-dimension expansion of the same offset mechanism;
it does not assume the author's conditional Poisson formula. Fix finite
Euclidean centers z_i, a nonempty positive block B, a remaining block L,
and s>0. Blocks select disjoint labeled positions, with repeated centers
allowed. Put b=|B|. Assume the affine span of the remaining centers has
dimension at most five. When L is empty the desired kernel is positive
immediately, so suppose L is nonempty.

Choose an origin o in that affine span, and orthogonally decompose

    z_i-o = u_i+v_i,

where the u_i belong to its direction space. Every v_l for l in L is zero.
Set

    E=sum_(i in B)|v_i|^2,   W=sum_(i in B)v_i,   A=|W|^2/(2s).

For J subset L and m=b+|J|, the centroid identity gives exactly

    Q_(B union J)(z) = Q_(B union J)(u)+E-|W|^2/m,        (1)

where Q is the sum of squared deviations from the subset mean. Thus,
writing K_d(C)=|C|^(-d/2) exp[-Q_C/(2s)],

    K_5(B union J;z)
      =exp[-E/(2s)] exp(A/m) K_5(B union J;u)
      =exp[-E/(2s)] sum_(h>=0) A^h/h! K_(5+2h)(B union J;u).
                                                               (2)

All the projected centers fit in R5. For each h, pad them to R^(5+2h),
put phi_i(x)=exp[-|x-u_i|^2/(2s)] and C_d=(2 pi s)^(-d/2),
and apply Gaussian multiplication:

    I_h := sum_(J subset L) (-1)^|J| K_(5+2h)(B union J;u)
         = C_(5+2h) integral product_(i in B) phi_i(x)
                                  product_(l in L)(1-phi_l(x)) dx
         > 0.                                                (3)

The integral is finite. Its integrand is positive away from finitely many
centers, so strict positivity holds also with coincident centers. The
series in (2) can be interchanged with the finite subset sum: its absolute
sum is bounded by 2^|L| b^(-5/2) exp(A/b), before the common prefactor.
Consequently the original alternating kernel is

    K = exp[-E/(2s)] sum_(h>=0) A^h/h! I_h > 0.          (4)

This confirms the affine-offset sign. Dropping the term |W|^2/m in (1)
would be incorrect; the independent checker includes an explicit adverse
control for that omission. If W=0, the series reduces to its h=0 term and
recovers the prior centroid projection.

For completeness, the positive series also has a direct remainder bound.
Writing z=A/b and Q_B(u) for the projected positive-block variance,

    0 <= I_h <= b^(-5/2-h) exp[-Q_B(u)/(2s)]

follows by bounding every complement factor in (3) by one. After h=L0,
the remaining series is bounded by

    exp[-(E+Q_B(u))/(2s)] b^(-5/2)
        * z^(L0+1)/(L0+1)! / [1-z/(L0+2)]                (5)

whenever z<L0+2. This records convergence explicitly; no truncation or
numerical Gaussian integral is needed for the accepted sign.

Six remaining points always have affine dimension at most five, regardless
of the full paired rank. Formula (4) therefore covers N-j<=6. More generally,
it covers any number of remaining positions satisfying that affine-rank
condition, as the reviewed source states. The argument does not assign
rank five to seven affinely independent remaining points in R6.

## 2. Replica factors, polarized coefficients and equality

The normalized moment gap obeys

    a_j = (1/(4s)) E[delta_12 integral_0^1
                      (j+2)^(-5/2) exp[-Q_(j+2)(t)/(2s)] dt],

where delta_12 is the nonnegative squared pair-distance loss. I checked
the factor: the exponential derivative contributes 1/(2ms), the pair count
is m(m-1)/2, and a_(m-2) divides the moment by m(m-1). Coupling the extra
replicas then leaves the positive outer factor
(N+1) binom(N,j)/(4s) multiplying the kernel in (4).

Before averaging weights, the polarization identity gives the outer
factor 1/(2s(N+2)) for each distinguished pair and each j-position base
extension. The remaining block has N-j positions. The algebraic identity
in the reviewed equation (14) has the correct binomial normalization;
it also agrees with the reviewer-authored original polarization formula.
Thus positivity is established for the homogeneous coefficients themselves,
not inferred merely from positivity on a weight simplex.

Every kernel in the proved range is strictly positive. Hence a coefficient
is positive if its tuple contains a strictly shortened pair, and its
expectation is positive if the expected pair loss Delta is positive.
If Delta=0, nonnegativity and continuity of the pair loss on the support,
together with the support property of the product law, force every support
pair loss to be zero. Such a map is congruent to an isometry on that support,
so all convolved profile and moment differences vanish. No least weight
is needed. Bounded support justifies the scalar differentiations and finite
expectations; the positive-kernel argument is pointwise and needs no
measurable choice of projection frames. Diffuse laws are covered directly.

## 3. The compact lower bound keeps the correct loss and exponent

I also checked the author's Poisson representation directly. Conditional
on J Poisson with mean beta, the Laplace transform of J independent
rate-p exponentials is [p/(p+ell)]^J. Averaging gives precisely
exp[-beta ell/(p+ell)], with an atom of mass exp(-beta) at Theta=1.
Both its orientation and normalization are correct.

For radius R, write rho=R/sqrt(s), p=j+2 and q=N-j. The reviewed estimates
Q0<=pR^2, beta<=2pR^2/s and |v_i|<=2R follow from the base-centroid
variance and orthogonal nearest-point construction. On the specified R5
box, every complement factor exceeds 1/3 and the normalized volume is
greater than 1/256. Its base Gaussian costs
exp[-p((2rho+2)^2+4)/2]. Combining the three exponential costs gives

    p rho^2/2 + 2p rho^2 + p(4rho^2+8rho+8)/2
       = p(9rho^2+8rho+8)/2.

Multiplying by the replica factor therefore confirms exactly

    b_(N,j) >= [(N+1) binom(N,j)/(1024*3^q*s)]
                   exp[-p(9rho^2+8rho+8)/2] Delta.        (6)

At R=2l,s=1, the exponent becomes p(18l^2+8l+4). The elementary e<4
bound gives the claimed mantissa times 2^[-2p(18l^2+8l+4)]. This is a
direct sign bound on every configuration of K_l. It incurs no localization
or threshold-approximation error, and remains valid when Delta=0.

The independent checker reproduces all seven compressed constants at
l=3,N=429981694 by a falling-product recurrence, and they match the
author's certificate exactly. It never expands the binary denominators.
These tiny positive constants are valid signs, not a claim that they
dominate arbitrary rounding errors or give practical margins for the
remaining columns. The previous weight-cell constants are preserved.

## 4. The first residual classification is complete and still unsigned

For N=7,j=0, remove a distinguished pair of different labels from nine
positions. The remaining block can escape the rank test only if its seven
positions have seven distinct labels. Restoring the pair gives exactly
three cases: both labels already occur, one occurs, or neither occurs.
These give the author's multiplicities (2,2,1,1,1,1,1),
(2,1,1,1,1,1,1,1), and nine singletons, with the stated distinguished pairs.
A pair of identical labels has zero loss and needs no kernel sign.

The independent checker uses canonical set partitions of positions,
instead of the author's integer partitions of multiplicities. It checks
all 21147 set partitions of nine positions and 612252 different-label
pair cases. Exactly 2052 position-pair cases remain: 1512,504,36 in the
three classes respectively. All 610200 other cases have at most six
remaining labels. These are combinatorial counts, not counts of tested
Euclidean geometries or certified negative kernels.

Fraction-free elimination independently reproduces the seven-site paired
determinant -512 and midpoint determinant -64. All 21 endpoint pairs are
contractions; the distinguished loss is 16. Thus the remaining rank-six
case is real. It is not a counterexample and does not raise the minimum
atom count to nine: seven labels with two repeated samples already occur.

## 5. Reproduction and precise trust boundary

[audit.py](audit.py) imports no reviewed code or certificate. It uses exact
orthogonal projection with rational arithmetic and checks (1) for every
subset in five controls: 660 subset identities in total. They include an
actual R3 contraction whose lifted tuple has rank six and whose remaining
affine span has rank five, a nonzero affine correction, a zero correction,
repeated centers and nine remaining positions. Separate checks cover
polarization factors, scaled products and positive-series remainders.
Four invalid inputs or omitted-correction variants are rejected.

Normal and optimized Python reproduce [EXPECTED.json](EXPECTED.json).
The original verifier and its six damaged-certificate controls also passed
in both modes, with the expected author record hash. Those replays are
corroboration, not independent derivations. Reproduction commands and the
independent hash are in [README.md](README.md).

The accepted universal results rest on the written Gaussian integration,
the positive affine correction, replica identities and inequality proof.
The finite code checks neither formalize those arguments nor establish
universality by enumeration. Exact Python integer/Fraction arithmetic
remains a computational premise. No floating-point sign, solver, hidden
input, Gaussian quadrature or large certificate is used.

The useful handoff to R2 and R3 is now an audited pruning and lower-bound
rule on the whole compact frontier: omit N-j<=6 from the unknown signs
and retain the actual distance-loss factor in (6). Every other beta entry
still requires its own argument. This review supplies no new class,
localization theorem, contact-flux sign, or full-question conclusion.
