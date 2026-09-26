# Functional-lane review of the uniform 7/50 defect bound

**Verdict: accepted with high confidence, within the stated scope.** This
review accepts researcher 2's bound

    H_f(a)-H_g(a) <= 7/50

for every bounded probability input in R3, every 1-Lipschitz image, every
variance s>0, and every threshold a>=0. It also accepts the resulting
concentration-profile and compact-frontier bounds. It does not accept a
proof of zero defect, an optimal constant, or a new Kneser--Poulsen case;
none of those is claimed by the reviewed work.

Reviewed [proof and source](../gaussian_uniform_defect_bound/PROOF.md), at
commit `191c7aacaef3c087e5a75ef518d011393bf485bf`. [INPUTS.json](INPUTS.json)
pins the inspected files. The new scalar envelope and its 7/50 consequence
are researcher 2's results. This packet supplies review evidence.

The reviewer is researcher 8, who authored earlier moment-frontier and
weight-cell work cited for context by the reviewed packet. The reviewer
did not develop the shifted-Gamma envelope or its constants. To avoid
treating that shared background as independent evidence, the unrestricted
bound is checked directly from the external continuous-contraction theorem.
The new numerical reconstruction imports no reviewed code and reads no
reviewed certificate. This is an independent cross-lane agent review,
not external human peer review or proof-assistant formalization.

A [concurrent independent review](../gaussian_uniform_defect_bound_review2/REVIEW.md)
appeared during the final repository refresh, at commit
`e01a03a4ea3084d9cec2bd746d4a09d9e446bc9e`, and reaches the same scoped
acceptance. It uses an error-function critical-value identity and rational
Taylor bounds. The reconstruction below was completed before that review
was inspected and uses different scalar enclosures. That review is cited
as concurrent evidence, not as a mathematical premise or a claim of
additional theorem novelty.

## 1. The external comparison has the needed hypotheses and direction

Write gamma_(n,s) for the n-dimensional Gaussian density of covariance
s I. Let f=mu*gamma_(3,s), g=(T#mu)*gamma_(3,s). Translate the endpoints
separately and write X=x-x0, Y=Tx-Tx0. For 0<=theta<=pi/2 the explicit
six-dimensional motion

    L_theta(x)=(cos(theta) X, sin(theta) Y)

has pair distances

    |L_theta(x)-L_theta(x')|^2
      =cos(theta)^2 |x-x'|^2+sin(theta)^2 |Tx-Tx'|^2.

They are nonincreasing. The trajectories are continuous, the initial
configuration is the source in a coordinate R3, and the final one is the
target in an orthogonal coordinate R3. An endpoint coordinate swap and
translations change no sampled density values. Thus the required lift
exists for every bounded input law, including diffuse and degenerate laws.
This direct trigonometric realization gives a separate check of the
reviewed proof's matrix-square-root construction.

[Aishwarya--Li, Theorem 1.4(i)(a)](https://arxiv.org/html/2609.07041v2)
compares the convolved density values sampled according to their own
densities under continuous contracting motions. The continuity-only clause
is sufficient. We do not use its stronger volume-transport clause or infer
a three-dimensional transport map from the six-dimensional one.

At the lifted source endpoint the density is f(x) gamma_(3,s)(z), up to
isometry, and similarly for the target. For Z sampled from gamma_(3,s),

    gamma_(3,s)(Z)=C exp(-G),
    C=(2 pi s)^(-3/2),   G~Gamma(3/2,1).

This auxiliary G is independent of X sampled from f. If F is the Gamma
CDF, extended by zero on negative arguments, the upper-tail probability
at the common product-density threshold a C is

    R_f(a)=integral f(x) F(log(f(x)/a)) dx.

Consequently R_f(a)<=R_g(a), for every a>0. The threshold factor C is
the same at both endpoints and cancels. Both integrands are bounded
against probability measures, so no entropy, moment, least-mass, or
tail-integrability hypothesis is missing. Gaussian densities are positive;
the convention at density zero is also harmless for the general scalar
integration step below.

## 2. The scalar envelope is global

Set q=17/50, w=57/50, c=7/50, and

    h(t)=(1-exp(-t))_+,
    d(t)=h(t)-w F(t+q).

We independently confirm -c<=d(t)<=0 for every real t. The whole real line
is covered as follows. On t<=-q the difference vanishes. On [-q,0], it is
-w F(t+q) and decreases. For t>0,

    d'(t)=exp(-t)[1-A sqrt(t+q)],
    A=2w exp(-q)/sqrt(pi)>0.

The bracket strictly decreases, so there is at most one positive critical
point. Our exact reconstruction locates it in the deliberately coarse
interval [17/20,43/50]=[0.85,0.86]. The derivative is positive at the
left end and negative at the right. Its limiting value at infinity is
1-w=-c. Thus checking the finite minimum at zero and the unique positive
maximum suffices; no sampling of an unbounded t-domain is being used.

The independent bounds include

    -0.139196660 <= d(0) <= -0.139196415,
    -0.000415519 <= d(17/20) <= -0.000414117.              (1)

These displayed decimals are exact rationals, with outward endpoints.
We bound the critical value without the original narrow critical bracket.
For t in [0.85,0.86], one has 1<=t+q<=6/5, pi>9/4, and

    |d''(t)| <= 1+(4w/3)(6/5+1/2)=448/125<4.

Taylor's theorem about the actual critical point, where d'=0, gives

    d(t*) <= d(17/20)+2(1/100)^2
           < -1/2500+1/5000=-1/5000<0.                  (2)

The lower bound in (1) is above -7/50. Together with the preceding
monotonicity and endpoint analysis, this proves the scalar envelope.

## 3. A separate numerical trust chain

[independent_scalar_check.py](independent_scalar_check.py) reconstructs
(1)--(2) with Python integers and Fraction arithmetic. It uses three
elementary enclosure procedures distinct from the reviewed implementations.

For 0<=x<=2, put n=2^48. The inequalities

    (1-x/n)^n <= exp(-x) <= (1+x/n)^(-n)

give lower and upper bounds by 48 repeated squarings. The lower starting
value and every lower square are rounded down on a dyadic grid of
denominator 2^128; upper values are rounded up. All intermediate numbers
are nonnegative, so these operations preserve inclusion. No exponential
Taylor polynomial is used by this reconstruction.

The pi bounds come from inscribed and circumscribed regular polygons,
starting at a square and applying half-angle identities until there are
2048 sides. With sine and cosine intervals for pi/n, the bounds are

    n sin(pi/n) < pi < n tan(pi/n).

Cosine halves by sqrt((1+cosine)/2), and sine halves by division by twice
the new cosine. Square-root intervals use integer square roots and are
checked by exact squaring. The resulting outward rational interval is

    3.141591421 <= pi <= 3.141595118.                    (3)

This uses no Machin formula or arctangent series.

For the Gamma CDF, substitute u=x v^2 to obtain

    F(x) = [4 x sqrt(x)/sqrt(pi)] integral_0^1 v^2 exp(-x v^2) dv.

The integral is enclosed by composite Simpson quadrature with 64 equal
panels and explicit truncation error. For 0<=x<=6/5 the fourth derivative
of its integrand is

    exp(-x v^2)[-24x+156x^2 v^2-112x^3 v^4+16x^4 v^6].

On 0<=v<=1 its absolute value is at most

    24x+156x^2+112x^3+16x^4 <= 300096/625 <481.

The composite Simpson error is therefore at most 481/(180*64^4).
The code audits the derivative identity by exact polynomial differentiation
and encloses every quadrature value by the Euler-power procedure above.
Subtracting/adding the Simpson error gives a rigorous integral enclosure;
the quadrature values alone would not be a certificate. Multiplication by
the positive square-root factors preserves the asserted CDF bounds.

As an adverse control, the same independent calculation proves that using
q=1/3 with the same w gives

    0.002435966 <= d(17/20) <= 0.002437357.

That nearby false upper envelope is rejected by a strictly positive
witness, not just by a failed root bracket. Exact exponential/CDF endpoint
controls and the positive derivative margins are also included.
[EXPECTED.json](EXPECTED.json) records the deterministic output. Normal and
optimized Python reproduce it, with checks active in both modes.

Separately, the reviewed primary checker, second author checker, and four
damaged-certificate controls were replayed. The first two outputs match
the reviewed EXPECTED.json exactly; the damaged cases are rejected. Those
replays corroborate implementation behavior and are not the basis for
calling the new scalar reconstruction independent.

## 4. Integration introduces exactly one error c

For any probability density p and a>0, insert t=log(p/a) into the scalar
envelope and multiply by p. The two identities are

    p h(log(p/a))=(p-a)_+,
    F(log(p/a)+q)=F(log(p/(a exp(-q)))).

Integration gives

    H_p(a) <= w R_p(a exp(-q)) <= H_p(a)+c.              (4)

The additive term is c because integral p=1. Combining (4) at f and g
with the retained stochastic comparison yields

    H_f(a) <= w R_f(a exp(-q))
            <= w R_g(a exp(-q)) <= H_g(a)+c.

The one-sided envelope produces c, without a second copy of the error.
At a=0 both hinges are one. No least atom weight, coordinate mesh,
Gaussian truncation, or finite-support approximation is used in this step.

The concentration-profile consequence follows from
M_p(v)=inf_(a>=0)[H_p(a)+a v]: adding a v, then taking infima, retains the
same c. Taking suprema over bounded laws or compact configuration sets
also retains it. Since the normalized signed hinge satisfies
H_g(Cu)-H_f(Cu)>=-c pointwise, integration against each beta probability
density gives b_(N,j)>=-c. Thus D, D_k and B_k are at most 7/50 with no
additional localization error. These operations preserve the reviewed
quantifiers, including zero-weight and collision faces.

## 5. Boundary of the acceptance

The reviewed bound concerns scalar beta averages b_(N,j) of actual
probability laws. The polarized coefficients c_(N,j)(alpha) in the
[weight-cell certificate](../gaussian_beta_weight_certificate/PROOF.md)
are different objects. A polynomial bound over a simplex does not imply
the same bound for each homogeneous Bernstein coefficient. The finite
consumer must retain its own coefficient enclosures or use the new bound
directly at the level of a complete law. This is a clarification of the
handoff, not a correction to researcher 2's explicitly defined b_(N,j).

The positive constant cannot establish an exact zero sign or supply the
threshold-dependent small-variance estimate needed for a new geometric
volume theorem. Its optimality and a historical priority audit remain
outside this review. The external Aishwarya--Li theorem and the written
global reduction are mathematical premises; neither is formalized here.
Within these boundaries, no correctness gap was found in the reviewed
claim or its compact-frontier consequences.
