# Parity alignment and an indecomposable positive control

Complete author proof, 27 September 2026; independent review pending.
The unrestricted dimension-three Gaussian-majorisation question is open.

## 1. Alignment of complete even-sign orbits

Let

    E={(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)}.

For `a=(a1,a2,a3)` with nonnegative coordinates and `sigma in {-1,1}`,
let `nu_(a,sigma)` be the probability assigning mass 1/4 to each labelled
point `sigma e*a`, `e in E`; multiplication is coordinatewise.
Repeated locations when a coordinate vanishes retain their labelled masses.

Let Lambda be any probability on pairs `(a,sigma)` with bounded a, and put

    mu = integral nu_(a,sigma) dLambda(a,sigma),
    mu_plus = integral nu_(a,+1) dLambda(a,sigma).             (1)

Lambda can be atomic or nonatomic, and the sign can depend arbitrarily on
a. The theorem requires uniform weights within each four-point orbit,
but permits arbitrary total masses and three independent axis lengths
between orbits. It is not restricted to regular tetrahedra or two shells.

**Theorem 1.** For every `s>0` and `h>=0`,

    integral (mu*gamma_s-h)_+ <= integral (mu_plus*gamma_s-h)_+.
                                                               (2)

Thus the comparison is full Gaussian majorisation. It does not require
the alignment map to be 1-Lipschitz. In particular the proof does not
insert a noncontracting step into a theorem about contracting paths.

For an intrinsic map description, a law invariant under changing any two
coordinate signs has a representation (1). Off the coordinate planes set

    A(x)=sign(x1*x2*x3) x,

and on the coordinate planes set A(x)=x. Then `A#mu=mu_plus`. On such a
plane the two labelled parity orbits already define the same measure,
so the convention causes no discrepancy. No continuity of A is claimed.

### An explicit doubly stochastic kernel

For `t_j>=0`, define

    c_a(t)=exp(-|a|^2/(2s)) product_j cosh(a_j t_j/s),
    b_a(t)=exp(-|a|^2/(2s)) product_j sinh(a_j t_j/s),
    C(t)=integral c_a(t) dLambda,
    B(t)=integral sigma b_a(t) dLambda,
    D(t)=integral b_a(t) dLambda.

All quantities are finite, `0<=D<=C`, and `|B|<=D`. Expanding the
four sign characters gives exactly

    (1/4) sum_(e in E) exp(sigma sum_j e_j z_j)
          = product_j cosh z_j + sigma product_j sinh z_j. (3)

Write `chi(x)=sign(x1*x2*x3)` away from the coordinate planes and
`t=(|x1|,|x2|,|x3|)`. If `f=mu*gamma_s` and `g=mu_plus*gamma_s`, then

    f(x)=gamma_s(x)[C(t)+chi(x)B(t)],
    g(x)=gamma_s(x)[C(t)+chi(x)D(t)].                        (4)

When `D(t)>0`, put `theta(t)=(1+B(t)/D(t))/2`; otherwise put theta=1/2.
Then `0<=theta<=1`, theta depends only on t, and

    f(x)=theta(t)g(x)+(1-theta(t))g(-x).                    (5)

The same formula at -x has the two coefficients interchanged. Thus on
each antipodal pair the matrix is

    [ theta      1-theta ]
    [ 1-theta      theta ],                               (6)

a nonnegative doubly stochastic matrix. The coordinate planes have zero
Lebesgue measure; (4) also has B=D=0 there. Jensen applied to `(z-h)_+`
and integration prove (2), since `theta(|-x|)=theta(|x|)` and the
reflection x -> -x preserves Lebesgue measure. The same argument applies
to any convex energy for which the integrals are defined. It proves the
whole threshold range at once, including equality cases.

This is the elementary two-value convexity principle applied to (3).
No finite-order moment condition, instantaneous lifted-pair sign,
quadrature, endpoint approximation, or independent review is hidden in it.

## 2. Following alignment by a radial contraction

Let `rho:[0,infinity)->[0,infinity)` be 1-Lipschitz with rho(0)=0, and let

    R_rho(x)=rho(|x|) x/|x|,       R_rho(0)=0.

The accepted [radial/convex-core theorem](../gaussian_radial_contractions/CONVEX_CORES.md)
gives full Gaussian majorisation under R_rho for arbitrary bounded laws,
and both ball-volume comparisons for arbitrary individual radii. Applying
it after Theorem 1 gives

    mu*gamma_s <=_maj (R_rho#mu_plus)*gamma_s                (7)

at every s. The same is true after a further uniform contraction of the
target. This step is a credited positive theorem; we claim no new radial
motion or transfer principle.

When `T=R_rho composed with A` is 1-Lipschitz on the input support, (7)
is a positive class for the named contraction question. This last
Lipschitz condition is a genuine extra hypothesis: it is not inferred
from the factorization, because A can expand distances. Finite instances
can check it exactly; the following existing instance satisfies it.

There is also a direct class on a set with interior. Put

    K={x in R3: 1<=|x_j|<=2 for j=1,2,3},
    T(x)=A(x)/4.                                          (7a)

This map is 1-Lipschitz on the entire union of eight boxes K. For two
points with the same parity it scales their distance by 1/4. For opposite
parities at least one coordinate has opposite sign, so |x-y|^2>=4,
whereas |T(x)-T(y)|^2=|x+y|^2/16<=3. Thus every bounded law on K invariant
under changing two coordinate signs satisfies full Gaussian majorisation
under T. Its absolute-coordinate vector may have any diffuse distribution, with
arbitrary dependence between absolute coordinates and parity. The same construction
gives both volume comparisons below for any finite selection of complete
orbits in K, with independent orbit radii. This supplies a genuine
contraction application of the alignment theorem beyond one fixed input.
No classification of such maps or separate motion obstruction is claimed.
Kirszbraun's extension theorem gives a global 1-Lipschitz extension of
this support map; its values on K determine the asserted pushforward.

## 3. The existing eight-site adversary is a positive control

Use the four vectors v_i in E and the source and target from
[R6's eight-site obstruction](../gaussian_open_eight_site_obstruction/PROOF.md):

    P: a_i=v_i, b_i=-20v_i,
    Q: a_i=v_i, b_i=(58/3)v_i.                            (8)

For every `0<=alpha<=1` give total mass `1-alpha` uniformly to the four
a_i and total mass alpha uniformly to the four b_i. The result is

    mu_alpha*gamma_s <=_maj nu_alpha*gamma_s
        for every s>0 and every alpha in [0,1].            (9)

To prove it, align the outer orbit from -20E to 20E, leaving the core E
unchanged. Now use the nonnegative radial profile, written as
`rho(sqrt(3)t)=sqrt(3)q(t)`, where

    q(t)=t                       for 0<=t<=1,
         1+(55/57)(t-1)          for 1<=t<=20,
         t-2/3                  for t>=20.                 (10)

It is continuous, nonnegative, 1-Lipschitz, and sends 1 to 1 and 20 to 58/3.
Equations (2) and (7) prove (9). Uniformly contracting Q by
`lambda=1-2^-20` also preserves every sign. This is the central strict
pair of R6's open coordinate box; the entire box is not signed here.

For completeness, with r=20 and c=58/3 the exact squared distances are

| Pair | P | Q |
| --- | ---: | ---: |
| a_i,a_j, i!=j | 8 | 8 |
| b_i,a_j, i!=j | 1163 | 1163 |
| b_i,a_i | 1323 | 3025/3 |
| b_i,b_j, i!=j | 3200 | 26912/9 |

Thus the prescribed map really is a contraction. The alignment alone is
not: for i!=j the squared distance from a_j to b_i increases by 80 when
-20v_i is replaced by 20v_i. The density kernel (5), rather than a
contraction-path argument, justifies that intermediate comparison.

### Exact full-interval indecomposability

Fix the four core vertices. In any configuration between P and Q in the
complete squared-distance order, all six core distances and each of the
twelve cross distances `b_i,a_j`, j!=i, remain tight. Three spheres centred
at the corresponding face vertices meet in precisely two points:
`-20v_i` and `(58/3)v_i`. Noncollinearity of the three centres and the
two distinct solutions justify completeness; this is also direct reflection
in their face plane.

Hence the full interval has at most sixteen root-aligned placements.
If one outer point chooses the source position and another the target
position, their squared distance is

    3r^2+3c^2-2rc=1548 < 26912/9.                         (11)

It falls below the target distance. Every proper nonempty subset of
reflections creates such a pair, so only P and Q are feasible. The full
distance interval therefore has exactly two congruence classes. In the
sense of the [existing reduction](../gaussian_indecomposable_contractions/PROOF.md),
(8) is indecomposable among all R3 configurations, not just this displayed
reflection family. The checker examines all sixteen choices independently.

The new sign (9) supplies an actual all-threshold positive control inside
that indecomposable frontier. The four moving points must change together,
yet the two orbit masses may be arbitrary. R6's stronger no-R5-motion
claim is a separate author result and is not required for (9). It concerns
the prescribed labelled map, and must not be used to exclude alternative
weight-preserving rematchings of the two measures.

## 4. Both ball volumes, with radii constant on each orbit

Take finitely many complete labelled orbits `sigma_m E*a_m`, m=1,...,M,
and assign any radius `r_m>=0` to all four labels of orbit m. Align each
orbit to E*a_m, retaining its radius. Then

    volume(union of aligned balls) <= volume(union of source balls),
    volume(intersection of aligned balls)
                    >= volume(intersection of source balls).   (12)

These are comparisons for the alignment itself, which need not contract
centres. Following by R_rho gives the same comparisons for the final
centres, by the cited radial theorem. Whenever the final prescribed map
is a contraction, these are Kneser--Poulsen cases. Radii may vary arbitrarily
between orbits; no claim permits independent radii at the four labels of
one orbit.

Here are direct limiting proofs of both signs, so the intersection is not
silently inferred from the Gaussian union transfer.

### Union

For epsilon>0 form

    F_epsilon(x)=(1/4) sum_(m,e)
       exp((r_m^2-|x-sigma_m e*a_m|^2)/(2epsilon)),

and G_epsilon with all sigma_m=+1. The positive orbit coefficients change
with epsilon, but (3)--(6) apply for each epsilon. Concavity of min(z,1)
therefore gives

    integral min(F_epsilon,1) >= integral min(G_epsilon,1). (13)

Away from the finitely many boundary spheres, these functions converge
to the respective union indicators as epsilon decreases to zero.
If centres have norm at most L and radii at most R, for |x|>=L the sum
is at most `M exp((R^2-(|x|-L)^2)/(2epsilon))`. For epsilon<=1, outside
a sufficiently large fixed ball this is bounded by an integrable Gaussian;
inside it min(F,1)<=1. Dominated convergence proves the first sign in (12).
Radius zero and repeated centres create no problem.

### Intersection

Instead form

    P_epsilon(x)=(1/4) sum_(m,e)
       exp((|x-sigma_m e*a_m|^2-r_m^2)/(2epsilon)),

and Q_epsilon after alignment. The factor `exp(|x|^2/(2epsilon))` is
common on each antipodal pair. The orbit expansion now has `C-chi B`
in place of `C+chi B`, with positive orbit coefficients
`exp((|a_m|^2-r_m^2)/(2epsilon))`. The same doubly stochastic comparison
therefore applies. Convexity of exp(-z) gives

    integral exp(-P_epsilon) <= integral exp(-Q_epsilon). (14)

In the interior of the intersection every exponent tends to minus infinity,
so the integrand tends to one. Outside the intersection at least one
exponent tends to plus infinity, so it tends to zero. Boundary spheres
again have zero volume. For large |x|, retaining any one term gives

    P_epsilon(x)>=(1/4)
        exp(((|x|-L)^2-R^2)/(2epsilon)).

For epsilon<=1 this yields an integrable, superexponentially decreasing
upper bound on exp(-P_epsilon) outside a fixed ball; inside it the bound
one suffices. Dominated convergence proves the second sign in (12).
The sum is assumed nonempty; the empty-family intersection is not used.

For (8), (12) followed by (10) gives both inequalities with two completely
independent radii: one on the four core balls and another on the four
outer balls. The scaled strict target is covered too. Historical novelty
of these geometric comparisons is not established here. In particular,
a labelled motion obstruction alone does not show that their volume signs
escape all radius-preserving alternative rematchings.

## 5. Scope and evidence

The mathematical advance is an exact full-curve sign on a class of bounded
orbit laws, with a useful indecomposable input as an application. It closes
the middle as well as both tails on that class. It does not extend the
closed cap or depth-one classification, enlarge R6's spatial perturbation
box, permit arbitrary weights, or solve the full finite frontier.

The earlier coordinate-height and exposed-edge results remain unchanged.
They alone gave no middle sign. The present two-point kernel supplies such
a sign on the stated balanced inputs, without numerical endpoint overlap.
R8's spherical transfer and R3's loss-proportional cubature are context,
not premises. No signed individual physical pair kernel is assumed.

The standard-library [checker](verify.py) verifies the orbit identity as a
Laurent polynomial, reconstructs finite doubly stochastic witnesses and
all hinge breakpoints exactly, checks the eight-site map and all sixteen
full-interval candidates, and rejects malformed inputs. It uses neither
Gaussian quadrature nor the earlier large audit corpus. The universal
Gaussian and limiting statements rest on the written proof, with the
radial theorem as an explicit credited input. Review and historical
priority remain separate obligations.
