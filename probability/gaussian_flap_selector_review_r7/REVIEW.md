# Independent check of the full orthocentric-flap exclusion

**Verdict: accept the theorem at its stated scope.** Researcher 4's
[selector-motion proof](../gaussian_flap_selector_motion/PROOF.md), source
commit `19d42da48e5262580c4178c47a5937cbfe39f1ff`, proves full Gaussian
majorisation for every interior-orthocenter, depth-one tetrahedral flap,
for all nonnegative atom weights and all positive variances. It also proves
both arbitrary-radius Kneser--Poulsen volume inequalities on the full
sixteen labels. The unrestricted dimension-three question remains open.

This is an independent team-agent review of the new motion, not external
human peer review or a formal proof. I authored the earlier tournament
reduction and simplicial-basis motion on which the paper builds. Before
reading the new source I had obtained a weaker two-exceptional-pair motion
covering a proper shape region. That unpublished work is subsumed and has
been kept out of the public packet. I did not develop the author's new
one-exceptional-pair motion. I read its proof and source notes, but did not
read, import or execute its checker or expected output. The exact checks
here reconstruct the critical algebra and coordinate geometry separately.

## 1. Precisely what is accepted

Let v_0,...,v_3 be affinely independent in R3 and

    v_i.v_j=-c<0 (i!=j),       h_i=|v_i|^2+c.

Keep the anchors v_i fixed and send the twelve flaps v_j-v_i to v_j+v_i.
The accepted assertions are:

* Every ten-site tournament selector, with one directed flap per unordered
  vertex pair, has an analytic contracting motion in R5.
* For the full sixteen-site map, every probability mass vector satisfies
  H_(mu*gamma_s)(a)<=H_(nu*gamma_s)(a) for every s>0 and a>=0.
* Every independently assigned list of sixteen nonnegative radii satisfies
  union-volume decrease and intersection-volume increase.

The Gram kernel gives sum c/h_i=1 and sum v_i/h_i=0. Its strictly positive
kernel implies that every three normals are independent. The original
endpoint map contracts by the exact loss identities in the earlier
[tournament reduction](../gaussian_flap_tournament_reduction/PROOF.md).
The target collisions v_i+v_j=v_j+v_i are essential to the last two claims.

This does not cover arbitrary tetrahedra, other flap depths, arbitrary
bounded laws, or all R3 contractions. No motion of the full sixteen-label
configuration is asserted. The classical obstruction to that simultaneous
motion is not contradicted.

## 2. Why there is exactly one free Gram entry

A sinkless tournament on four vertices has an outdegree-one vertex i.
Let i->k be its unique outgoing edge, with r,l the remaining vertices.
For a pair of selected flaps with tails i,k, the flaps must be i->k
and k->b, with b!=i. Thus their squared distance has the form

    constant - 2[G_ik + h_k lambda_k],                    (1)

where G_ik is the moving inner product of the normal vectors. There is
no tight selected pair with these tails that forces G_ik to be constant.
All other moving Gram entries may be kept constant. Anchors require only
that the individual physical coefficients lambda_a be nondecreasing.

I checked this incidence obligation for every sinkless tournament and
every possible outdegree-one choice, without using the author's enumeration.
The complete counts are 32 sink, eight source-and-cycle and 24 strong
tournaments, with 72 eligible tail choices. The sink selectors use the
already-proved three-basis motion. No symmetry reduction of an asymmetric
shape is hidden here.

## 3. Projection geometry and the opposite shifts

Let P=span(v_r,v_l). Orthogonal projection of v_i and v_k onto P gives
the same vector p: both have inner products -c with the two independent
spanning vectors. Write L=|p|^2. It is strictly positive because p.v_r=-c.
The components perpendicular to P have opposite signs by the positive
Gram dependence, so for a unit normal n one can write

    v_i=p+A n,       v_k=p-B n,       A,B>0.

Taking inner products gives

    AB=L+c,         h_i=A(A+B),       h_k=B(A+B).          (2)

Put U=asinh(A/sqrt(L)), V=asinh(B/sqrt(L)), d=U+V>0.
Use shifts u_i=U, u_k=-V and u_r=u_l=0. In an auxiliary copy of P
choose E_i=cosh(U)p, E_k=cosh(V)p, E_r=v_r and E_l=v_l.
An isometry J identifies this plane with R2. Then

    R_a(w)=(tanh(w+u_a) v_a, sech(w+u_a) J E_a).           (3)

All normal lengths are constant. Except for {i,k}, the identity
E_a.E_b=-c cosh(u_a-u_b) and the hyperbolic addition identity give
R_a.R_b=-c. The exceptional entry is

    R_i.R_k=-c+delta sech(w+U)sech(w-V),
    delta=AB(cosh(d)-1)>0.                               (4)

The amplitude identity is exact. If Q=sqrt((L+A^2)(L+B^2)), then
E_i.E_k=Q and cosh(d)=(Q+AB)/L; substituting c=AB-L proves (4).
There is no omitted shape inequality or sign choice in this calculation.

## 4. An independent factored certificate for the only distance sign

For (1), set

    t=tanh(w-V),       q=tanh(d),       epsilon=exp(-d).

Then -1<t<1, 0<q,epsilon<1 and
sqrt(1-q^2)=epsilon(1+q). Define

    F(t)=sqrt(1-q^2)(1-t^2)/(1+q t).

The bracket in (1), apart from an additive constant, is
delta F(t)+h_k t. Instead of bounding F' by concavity, direct polynomial
factorization gives the exact identity

    F'(t)+2 epsilon
      = epsilon(1-q)(1-t)[2+q(1+t)]/(1+q t)^2.            (5)

Every factor on the right is nonnegative on the entire closed interval;
the denominator is positive. Also (2) and (4) give

    h_k-2 delta epsilon
      = B^2+AB epsilon(2-epsilon)>B^2>0.                  (6)

Combining them produces a positive expression for the complete derivative:

    [delta F(t)+h_k t]'
      = B^2+AB epsilon(2-epsilon)
        +delta epsilon(1-q)(1-t)[2+q(1+t)]/(1+q t)^2
      > B^2 > 0.                                        (7)

This is a universal sign certificate, not a sample of positive path values.
It verifies the author's exceptional-distance argument and its margin
without importing the author's F'' calculation or numerical code.

All remaining flap distances follow from constant normal norms and Gram
entries and the exact derivative formula

    (|z_ab-z_ef|^2)'
      = -2[(R_a.R_e)' + h_a lambda_a' 1_(f=a)
                               +h_e lambda_e' 1_(b=e)].  (8)

Equal tails give constant distances. Anchor distances have derivative
-2h_a lambda_a' 1_(anchor=a). Thus every pair is accounted for, including
all equality constraints. Equations (5)-(7) settle the sole exceptional case.

## 5. Endpoints and the analytic transfers

The parameter w in (3) can be compactified without losing regularity.
Put tau=-cos(pi u), theta_a=tanh(u_a), 0<=u<=1. Then the physical
coefficient is (tau+theta_a)/(1+theta_a tau), and the auxiliary component
is sin(pi u) sech(u_a) J E_a/(1+theta_a tau). Since |theta_a|<1,
every denominator is bounded away from zero. These paths extend analytically
through both endpoints, with values (-v_a,0) and (v_a,0). The auxiliary
vectors all lie in a single plane; exactly two additional dimensions suffice.

The Gaussian inference correctly uses
[Aishwarya--Li, Theorem 1.4(i)(a)](https://arxiv.org/html/2609.07041v2),
which orders density values sampled from their own endpoint laws in R5.
For an independent planar Gaussian Z, gamma_s^(2)(Z)/(2 pi s)^(-1)
is uniform on (0,1). Consequently the probability of the product density
exceeding a(2 pi s)^(-1) equals H_f(a) in R3. This proves every selector
hinge comparison, including arbitrary zero atom weights.

For the full map, choose each edge's direction with probability proportional
to its two flap masses and place their sum on the selected source. All
selector laws have exactly the same target law. Their mixture is the
original source. Convexity of (x-a)_+ gives the correct inequality direction
and proves the full comparison at every variance. Zero edge masses can
use either orientation without changing this argument.

The volume proof correctly applies
[Bezdek--Connelly, Theorem 1](https://arxiv.org/pdf/math/0108098)
to each reversed R5 selector motion. To recover the full union, select
the larger-radius flap in each coincident-target pair: the target union
stays equal and the source union becomes a subset. For the intersection,
select the smaller-radius flap: the target intersection stays equal and
the source intersection becomes a superset. These give both inequalities
with the stated directions, independently of mass balances. The intersection
assertion is not inferred from Gaussian majorisation. Zero radii are allowed.

## 6. Independent exact checks and rejection controls

[verify.py](verify.py) uses standard-library rational arithmetic and the
quotient ring Q[u,v]/(u^2-U2,v^2-V2) to reconstruct the motion. The two
positive radicals are theta_i and -theta_k. It computes the common projection
by solving a two-by-two system from actual rational R3 coordinates, and
checks the opposite normal components and the two reserve identities.
At each fixture it uses the equivalent formulas

    theta_i=A/|v_i|, theta_k=-B/|v_k|,
    sech(U)E_i=sech(V)E_k=p,

so no transcendental evaluation, float or sign tolerance is present.
The residual coordinates are represented in R3 for exact dot products,
and their common two-dimensional span is checked explicitly.

The finite checks cover five polynomial identities, every eligible
tournament incidence, three rational geometries and three selector/tail
choices per geometry. At five rational compactified times, including
both endpoints, they check every moving Gram entry and every one of the
45 squared-distance derivatives directly from coordinates. They also
reject applying the same motion to the full family: the omitted common-head
pair i->r,k->r has equal endpoint distances and a strict interior dip.
Such a path cannot be a continuous contraction of that tight pair.

The [expected record](EXPECTED.json) contains the exact projection data,
counts and controls. The universal inequalities (5)-(8), the cited analytic
theorems and the mixture/radius transfers remain written mathematics.
Finite time checks do not prove an all-time sign. This is not a Lean
formalization, an independent proof of the cited external theorems, or
an independent authorship claim for the preceding R7 basis/reduction work.

## 7. Consequence for the counterexample lane

The entire interior-orthocenter, depth-one family is now excluded as a
Gaussian counterexample at the reviewed theorem's scope. Neither its two
ten-site templates nor a more asymmetric shape nor higher-order weights
can yield a failure. The eight residual selectors in my unpublished
partial construction are also closed; that partial packet was not published.

The exact finite beta certificates near this family retain their quantitative
margins and their scope for nearby ten-site contractions which need not
be flaps. They should not be treated as superseded in those directions.
The full comparison theorem removes only searches on the exact flap family.
Other depths and nonorthocentric geometries remain outside this theorem;
the separate shallow-depth result must still be respected there. Further
adversarial work needs an actual weighted hinge or convex-energy target
outside these closed classes, rather than another negative search here.
