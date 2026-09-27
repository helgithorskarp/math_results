# An exposed-edge certificate for the Gaussian tail of a tight contraction

Complete author proof, 27 September 2026; independent review pending.
The unrestricted dimension-three majorisation question remains open.

Strict mean-width decrease under a noncongruent contraction is classical,
and its qualitative Gaussian low-tail consequence is already in the team's
work. The new statement here is an explicit rational geometric certificate
for the margin. It applies directly to maps with preserved distances,
including the indecomposable test class, and requires no mean-width
quadrature. Its cutoff can be extremely small.

## 1. The certificate and quantitative statement

Let `x_i -> y_i`, `1<=i<=N`, be a finite contraction in R3, so

    d_ij = |x_i-x_j|^2-|y_i-y_j|^2 >= 0.

Translate the two endpoint configurations separately if desired and choose
`R>0` with `|x_i|,|y_i|<=R`. Write `w_i=(x_i,y_i)` in R6. A certificate
consists of labels i,j, a vector g in R6, and a number eta such that

    d=d_ij>0,       ||g||_1<=1,       0<eta<=R,
    g.(w_i-w_j)=0,                                         (1)

and, for every k, one of the following is true:

    w_k belongs to the closed segment [w_i,w_j], or
    g.(w_i-w_k)>=eta.                                     (2)

Thus the maximizing face is exactly the segment, with a certified gap to
every point off it. Labels in its relative interior, or coincident labels,
are allowed. The entire paired hull may itself be a segment, in which case
g=0 is permitted. Every condition is an exact rational comparison for
rational data.

For a finite configuration X define

    hbar(X)=integral_(S^2) max_i theta.x_i d sigma(theta),

where sigma has total mass one. This is half the usual mean width.

**Theorem 1.** A certificate (1)--(2) implies

    hbar(X)-hbar(Y) >= Delta,
    Delta = d eta^5 / (2^40 N^2 R^6) > 0.                  (3)

Every noncongruent finite contraction has such a certificate. If its
coordinates are rational, g,eta,R and Delta can all be rational. No
strictness is required for any pair other than the certified edge.
The numerical constant is deliberately coarse.

## 2. Why a strictly shortened exposed edge always exists

On R6 put `q(a,b)=|a|^2-|b|^2`, with symmetric bilinear form B. Thus
`q(w_i-w_j)=d_ij>=0`. Let K be the convex hull of the paired points.

Suppose, for contradiction, that q vanishes on every edge direction of K.
At a vertex v, write its incident edge vectors as e_1,...,e_l. Their other
endpoints are vertices of K, hence among the paired points. Therefore

    q(e_a)=0,       q(e_a-e_b)>=0,
    B(e_a,e_b)=-q(e_a-e_b)/2<=0.

Every vector from v to another vertex lies in the tangent cone at v, which
is the nonnegative span of the incident edge vectors. For such a vector
`z=sum alpha_a e_a`, `alpha_a>=0`, these inequalities give `q(z)<=0`.
The contraction condition gives the reverse inequality, so every distance
loss between vertices is zero. Fixing one vertex as origin, polarization
then shows that B vanishes on the span of all vertex differences. Every
paired point belongs to their affine span, so all d_ij vanish. This
contradicts noncongruence.

There is consequently an edge with endpoint labels i,j and d_ij>0.
An exposing functional for this edge is constant on its segment and
strictly smaller at every paired point outside it. Normalize its L1 norm
to at most one and decrease its positive finite gap if necessary so that
eta<=R. If K is a segment there are no off-segment constraints.

For rational paired points, the equality and strict inequalities defining
such a functional have rational coefficients. Their feasible relative
open set contains a rational point: its equality subspace is rational,
and rational points are dense there. Normalize and choose a smaller positive
rational eta. This also describes a finite exact producer: try the finitely
many distinct label pairs, identify segment membership by rational linear
algebra, and test feasibility of

    g.(w_i-w_j)=0,   g.(w_i-w_k)>=1 for every off-segment k.

Any feasible rational solution can be normalized to (1)--(2). Standard
exact rational linear feasibility suffices; the compact checker below
verifies supplied certificates and does not implement this general search.
The elementary tangent-cone fact is the usual edge-generator description
of a polytope's tangent cone. No three-dimensional rigidity assumption is
being silently imposed on the six-dimensional paired hull.

### A bound using only rational input size

Suppose `D w_i` has integer coordinates of absolute value at most `M`,
where D,M are positive integers, and choose a rational support radius
`R>=1`. Then the exposing certificate can be chosen with

    eta >= eta_0 = 1/[6 D 7! (2M)^6].                    (2a)

Consequently every noncongruent contraction with these input bounds has

    hbar(X)-hbar(Y) >= Delta_0,
    Delta_0 = 1/[2^40 N^2 R^6 D^7 (6*7!)^5 (2M)^30].    (2b)

This bound does not require producing the exposing vector. To prove it,
take the strictly shortened exposed edge from the preceding argument, and
write `A_k=D w_k`. If there are no off-segment labels, take g=0 and eta=R.
Otherwise maximize u over seven real variables `(h_1,...,h_6,u)` subject to

    -1<=h_l<=1,        u>=0,
    h.(A_i-A_j)=0,
    h.(A_i-A_k)>=u    for every off-segment label k.

This is a nonempty compact polytope: the cube bounds h, and any off-segment
constraint bounds `u<=12M`. An exposing functional gives a feasible u>0,
so a maximizing vertex has u>0. At that vertex select seven linearly
independent active constraints, including the equality as needed. Their
coefficient matrix has integer entries; each of the first six columns has
absolute entries at most 2M and the final column at most one. Right-hand
sides are integers. Its nonzero determinant is at most `7!(2M)^6` in
absolute value by expansion over permutations. Cramer's rule therefore
gives `u>=1/[7!(2M)^6]`.

Taking g=h/6 gives `||g||_1<=1` and an original-coordinate gap at least
eta_0. Choose eta=eta_0; it is at most 1<=R. A positive d_ij is an integer
multiple of `D^(-2)`, so d_ij>=D^(-2). Formula (3) now gives (2b).
The integer D may be the least common multiple of the supplied coordinate
denominators; no common denominator for the probability weights is needed.

The bit length of this certified Delta_0 is bounded by the bit lengths of
N,R,D,M with fixed coefficients. This is a statement for a **given rational
map**. The earlier rational indecomposable reduction did not bound the bit
length of its constructed coordinates in terms of the original loss scale;
that separate complexity gap is not filled here.

## 3. A positive Gaussian prism around the exposed edge

Let A,B be independent standard Gaussian vectors in R3, and put

    z_k(t)=(sqrt(1-t)x_k,sqrt(t)y_k),
    V_k(t)=G.z_k(t),       G=(A,B) ~ N(0,I_6).

For beta>0, let

    F_beta(t)=E log(sum_k exp(beta V_k(t)))/beta,
    p_k(t,G)=exp(beta V_k(t))/sum_l exp(beta V_l(t)).

Gaussian integration by parts gives the standard comparison identity

    -F_beta'(t)=(beta/2) sum_(k<l) d_kl E[p_k p_l].       (4)

For completeness, if C(t) is the covariance matrix of V(t), its derivative
is constant, and the Hessian of log-sum-exp divided by beta is
`beta[diag(p)-pp^T]`. The Gaussian derivative is half its contraction with
C'. Using `sum p_k=1` rewrites it as one quarter of the ordered pair sum
of the increment-variance derivatives, which are `-d_kl`; this is (4).
The identity and its endpoint integral also hold for singular covariances
by Gaussian integration by parts, or by adding vanishing independent noise.
All finite-beta derivatives are bounded and integrable. Every term on the
right is nonnegative.

Write g=(g_x,g_y). For `1/4<=t<=3/4`, define

    g_t=(g_x/sqrt(1-t),g_y/sqrt(t)),
    h_t=z_i(t)-z_j(t),       e_t=h_t/|h_t|,
    r=eta/(8R).

Then `|g_t|<=2`, `g_t.h_t=0`, and `|h_t|<=2R`. Also
`|h_t|>=sqrt(d)/2`, uniformly on this t interval. The exposed gaps in (2)
are unchanged by this transformation.

For all sufficiently large beta, uniformly in t, consider the prism

    G=g_t+v+alpha e_t,
    v orthogonal to e_t, |v|<=r,
    |alpha|<=1/(beta |h_t|).                              (5)

Choose beta so that the last upper bound is at most r. Each perturbation
then has norm at most `2r=eta/(4R)`. Since `|z_i-z_k|<=2R`, every
off-segment gap remains at least eta/2. The values from segment labels
lie between the two endpoint values for every G. On (5) the endpoints
differ by at most 1/beta, so

    p_i p_j >= e^(-2)/N^2.                               (6)

Moreover `r<=1/8` and `|G|<=2+2r<3`. The six-dimensional Gaussian density
is therefore at least `(2pi)^(-3)e^(-9/2)` throughout the prism. Its volume
is `2 omega_5 r^5/(beta |h_t|)`, where `omega_5=8pi^2/15`. Thus

    beta E[p_i p_j]
      >= e^(-13/2) omega_5 r^5 / [(2pi)^3 N^2 R].       (7)

Retain this one pair in (4) and integrate over the t interval of length
1/2. For every sufficiently large beta this gives

    F_beta(0)-F_beta(1)
      >= d eta^5 e^(-13/2) / (1966080 pi N^2 R^6).      (8)

The error between log-sum-exp/beta and the maximum is at most
`log(N)/beta`. Let beta tend to infinity. If
`W(X)=E max_i A.x_i`, the left side tends to W(X)-W(Y). Gaussian polar
decomposition gives `W(X)=E|A| hbar(X)` and
`E|A|=2sqrt(2/pi)<2`. Consequently

    hbar(X)-hbar(Y)
      >= d eta^5 e^(-13/2)/(3932160 pi N^2 R^6).

Finally `3932160*pi<2^24` and `e^(13/2)<4^(13/2)=2^13`.
The denominator is less than 2^37, so (3) follows with ample slack.
This proves Theorem 1.

This positive pair contribution belongs to a Gaussian **maximum**
comparison. It is not an individual posterior pair action for the physical
three-dimensional mixture hinge. The accepted obstruction to the latter
termwise sign remains intact.

## 4. Explicit signed endpoints for the original tight map

Give the N labels probability weights `a_k>=m>0`. Put
`f=sum a_k gamma_s(.-x_k)`, `g=sum a_k gamma_s(.-y_k)`,
`C_s=(2pi s)^(-3/2)`, and use the positive sign convention

    H(u)=H_g(C_s u)-H_f(C_s u).

Choose any integer `ell>=log(1/m)`, for example
`ell=ceil(log2(1/m))`. With the margin Delta from (3), or Delta_0 from
(2b), set

    B0=6R^2+2s ell,       Q=4B0/Delta,
    E=ceil(Q^2/s),        tau=2^(-E),
    b=1-m |x_i-x_j|^2/(8s+|x_i-x_j|^2).                  (9)

**Corollary 2.** For every `s>0`,

    H(u)>0           for 0<u<=tau,
    H(u)>=0          for u>=b.                           (10)

All remaining thresholds lie in the explicit finite interval `[tau,b]`.
For rational coordinates, positive rational weights and rational variance,
E is an exactly computable integer and b is rational. The dyadic cutoff is
stored by its exponent; the denominator `2^E` is not constructed.
Colliding images and zero losses on arbitrarily many pairs are allowed.
One first removes zero-weight labels if the input law contains them.
When using Delta_0, any strictly shortened pair can supply b: finding the
exposed edge or its normal is unnecessary for computing the endpoints.

Here is the analytic input, credited to the existing
[geometric low-threshold lemma](../gaussian_majorisation_open_stability/PROOF.md#2-low-thresholds-with-a-positive-geometric-margin).
For supports in B(0,R), atom masses at least m, and a mean-support gap at
least Delta, it gives, with `B0>=6R^2+2s log(1/m)` and `Q=4B0/Delta`,

    H_g(a)-H_f(a)
       >=4pi Delta s a [log(C_s/a)+1]>0
       whenever 0<a<=C_s exp[-Q^2/(2s)].                 (11)

Its finite, non-asymptotic argument is recalled to fix the parameters.
Write `a=C_s exp[-q^2/(2s)]`, and
`K=R^2+2s log(1/m)`. The maximum term in the mixture and the mass floor
put the radial superlevel boundary within K/q of `q+h_X(theta)` once
`q>=4R`, `q^2>=2K` and `q>=K/R`. Cubing and integrating gives

    |V_f(a)-(4pi/3)q^3-4pi q^2 hbar(X)|
       <=4pi (K+5R^2)q.

The same bound holds at Y. For `q>=4B0/Delta`, using `Delta<=2R` and
`K>=R^2`, all the conditions hold and subtraction gives
`V_f(a)-V_g(a)>=2pi Delta q^2`. Integrating this inequality from 0 to a
and using `H_f(a)=1-integral_0^a V_f(t)dt` proves (11). It is the prior
tail estimate, not a new Gaussian asymptotic or transfer theorem.

Since `log 2>1/2`, the choice E in (9) makes tau no larger than
`exp[-Q^2/(2s)]`; this proves the first part of (10). For the second,
every spatial point is at distance at least `|x_i-x_j|/2` from one of
the two selected source sites. Hence

    ||f||_infinity/C_s
      <=1-m[1-exp(-|x_i-x_j|^2/(8s))]<=b,

where `exp(-t)<=1/(1+t)`. The source hinge vanishes at and above b,
while the target hinge is nonnegative. This proves the corollary.

## 5. Scope, exact evidence, and open obligation

The [indecomposable reduction](../gaussian_indecomposable_contractions/PROOF.md)
and its rational effective construction produce finite maps with many tight
edges and positive weights. The present certificate supplies their signed
endpoints directly. It neither changes those maps by a homothety nor claims
they belong to the strict rational grid used in the separate measure lane.
The new [linear chain bound](../gaussian_indecomposable_contractions/LINEAR_HEIGHT.md)
retains a larger hypothetical negative gap, but does not itself supply an
exposing vector or a middle sign. The two improvements are complementary.

Strict mean-width monotonicity is Gorbovickis's Theorem 1.5 in
[Strict Kneser--Poulsen conjecture for large radii](https://arxiv.org/html/1006.0531v2).
The comparison identity (4) is classical Gaussian interpolation. We claim
neither result as new. The contribution is the explicit one-edge lower
bound, its rational input-size bound, and its exact certificate-to-endpoint
conversion for tight maps.
No exhaustive priority claim is made for this quantitative formulation.

The [checker](verify.py) uses rational arithmetic to validate the certificate
on the already published seven-site positive indecomposable control and on
a segment with an interior label and collapsed target. It checks a scaled
copy, damaged-certificate rejection, and the rational endpoint budgets.
It does not integrate a Gaussian, estimate mean width numerically, solve
a general hull problem, or infer the universal theorem from the examples.

The preserved seven-site control is already known to satisfy every hinge;
it is a positive control, not a candidate counterexample or new map family.
Its displayed conservative exponent E is enormous. No practical certificate
search at that resolution was run. The sign on `[tau,b]`, and therefore
the unrestricted dimension-three problem, remains unresolved.
