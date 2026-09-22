# Review of the all-dimensional symmetric Firey Rogers--Shephard claim

Date: 2026-09-22  
Target commit: `4aa5cc4b489368b2ec99c14c71e36b66081180cb`  
Target graph reference: `bafkreicok4at2jp5mpke247wikmyboaswwgrdvhvf2ofj3vsqssh2kpuze`

## Verdict

**Accept.**  I found no mathematical defect in the claimed inequality or its
equality classification.  The proof closes the smooth, nonsmooth, and
boundary-origin cases, and the stated constant agrees with the current
primary source.  This verdict is conditional on the standard support-volume,
mixed-volume, approximation, and surface-area-measure facts itemized below;
those facts are cited rather than reproved from first principles.

The theorem reviewed is the following.  If `d>=2`, `1<p<infinity`,
`q=p/(p-1)`, and the full-dimensional convex body `K` contains zero and has a
center of symmetry, then

    |K +_p (-K)| <= kappa(d,p)|K|,
    kappa(d,p) = sum_i binom(d,i)/binom(d/q,i/q).

Writing `K=C+x`, `C=-C`, equality is equivalent both to
`|x.n|=h_C(n)` for `S_C`-almost every `n` and to

    C polar = conv(F union -F),
    F = C polar intersect {u : x.u=1}.

## Independent proof audit

### 1. Translation and rank-one curvature

Since `0 in K=C+x`, symmetry gives `x in C`.  Thus
`|x.n|<=h_C(n)`.  With `h=h_C`, `l=x.n`, `t=l/h`, and

    f(t)=((1+t)^p+(1-t)^p)^(1/p),

the Firey support is `H=h f(t)`.  Spherical differentiation of `l=ht`, using
`Hess_S l=-l I`, gives independently

    Q_H=(f-t f')Q_h+h f'' grad(t) tensor grad(t).

The scalar factors are

    a=f-t f'=( (1+t)^(p-1)+(1-t)^(p-1) )/f^(p-1)>0,
    f''=4(p-1)(1-t^2)^(p-2)f^(1-2p)>0.

For `1<p<2`, the endpoint singularity has exponent `p-2>-1`, so it is
integrable.  This is the point at which an incautious endpoint
differentiation could have lost the boundary-origin cases; the target instead
uses an interior calculation followed by a limit.

In tangent dimension `d-1`, the determinant lemma gives exactly the two terms
and powers printed in the target.  If `U=cof Q_h`, then the Cheng--Yau
identity and `h^2 grad t=h grad l-l grad h` give

    div(h^2 U grad t)=-(d-1)t h det(Q_h).

The sign, the factor `d-1`, and the power `a^(d-2)` all agree.  Integrating
the divergence with multiplier

    R(t)=integral_0^t f a^(d-2) f''

therefore yields the claimed exact volume kernel

    Psi=f a^(d-1)+(d-1)tR.

### 2. Scalar maximum and normalization

Using `a'=-t f''`, direct differentiation gives

    Psi'=f'a^(d-1)+(d-1)R,
    Psi''=d f''a^(d-1)>0.

Because `Psi` is even, this proves strict increase as a function of `|t|`.
No inequality is hidden in the integration-by-parts step; the only inequality
is the pointwise comparison `Psi(t)<=Psi(1)`.

For `s=f'/a`, one has `ds/dt=f f''/a^2` and

    (a+f')^q+(a-f')^q=2^q.

Consequently `R(1)=integral_0^1 a(s)^d ds`.  The substitution
`u=(1-s)/(1+s)`, reflection of the tail by `u -> 1/u`, and the beta integral
give

    R(1)=(1/q) sum_(i=1)^(d-1)
             binom(d-2,i-1) B(i/q,(d-i)/q).

The gamma recurrence converts `(d-1)R(1)` to the interior terms of the stated
binomial sum, while `f(1)=2` supplies its two endpoint terms.  This reproduces
`kappa(d,p)` with no missing factor of `d` or `2`.

### 3. Completion for arbitrary bodies

The smooth calculation requires positive curvature and an interior
translation.  The two completion steps cover the full claim:

1. Smooth symmetric positive-curvature approximants converge in Hausdorff
   distance.  For fixed `x in int C`, their support ratios remain uniformly
   inside `(-1,1)`, their surface-area measures converge weakly, and the
   integrands converge uniformly.
2. For `x in boundary C`, replace it by `rx`, `r<1`, and let `r` increase to
   one.  Continuity of `Psi` on `[-1,1]`, uniform convergence of Firey
   supports, and finiteness of `S_C` suffice.  No endpoint `C^2` regularity is
   used.

These reductions cover every real `p>1`, every `d>=2`, every full-dimensional
centrally symmetric `C`, and every allowed placement `x in C`.

### 4. Equality and the polar-face reduction

The deficit is an integral of the continuous nonnegative function
`h[Psi(1)-Psi(t)]`.  It vanishes exactly when `|x.n|=h(n)` on the support of
`S_C`; almost-everywhere vanishing extends to that support by its definition.

The key completeness statement is

    conv{n/h(n): n in supp S_C}=C polar.

The target proves it rather than assuming that arbitrary polar extreme points
carry surface area.  Indeed, a point satisfying the corresponding supporting
halfspaces but lying outside `C` would enlarge `C` to `D`; the mixed-volume
formula would give `V(C[d-1],D)=|C|`, contradicting the first Minkowski
inequality because `|D|>|C|`.

Thus equality forces all generators into the opposite exposed faces
`F` and `-F`, proving necessity.  Conversely, polytopes approximating `F`
inside its fixed affine hyperplane have polar facets all containing `x` or
`-x`; the already established volume formula gives equality for their
polars, and Hausdorff continuity passes it to the limit.  This is a complete
reduction, not an assumption that surface area lives on all polar extreme
points.  Full dimension of `C polar` forces `dim F=d-1`.

## Human premises and trust boundary

The verdict depends on these standard human-checked premises:

1. The smooth support-volume identity
   `|L|=(1/d) integral h_L det(Hess_S h_L+h_L I)`.
2. The Cheng--Yau divergence-free cofactor identity for
   `Hess_S h+hI`.
3. Existence of smooth symmetric positive-curvature approximants, weak
   convergence of surface-area measures, and Hausdorff continuity of volume,
   polarity (when zero stays interior), and Firey addition.
4. The mixed-volume representation and first Minkowski inequality, including
   strict volume increase under proper containment of full-dimensional convex
   bodies.
5. Euler's beta integral and the gamma recurrence in positive arguments.

The cited Colesanti--Livshyts--Marsiglietti paper explicitly records the
support-volume formula and Cheng--Yau lemma.  The remaining items are standard
convex-geometry facts.  I checked that the hypotheses used here (positive
support, full dimension, interior point during smoothing, and positive beta
arguments) match their applications.  I did not formalize these premises in a
proof assistant.

## Adversarial smallest examples

The finite checker and hand calculations test the reductions at their weak
points:

- **Square, vertex translation, `d=2,p=2`.**  For
  `C=[-1,1]^2`, `x=(1,1)`, the Firey support equals `2(cos+sin)` on two
  opposite quadrant sectors and the constant `2` on the other two.  The
  support-area formula gives area `8+2*pi`, hence ratio `2+pi/2`, exactly the
  sharp constant.  This is a definition-level calculation independent of the
  target's `Psi` program.
- **Square, edge midpoint.**  Taking `x=(1,0)` puts zero on the boundary of
  `C+x`, but the top and bottom facets contain neither `x` nor `-x`; equality
  must fail.  At `p=infinity`, exact convex hull arithmetic gives ratio `2<3`.
- **Centrally symmetric hexagon, vertex translation.**  The hexagon with
  vertices `(1,0),(1,1),(0,1),(-1,0),(-1,-1),(0,-1)` and `x=(1,1)` makes zero
  a vertex of `C+x`, but two facets miss both special points.  The exact
  `p=infinity` ratio is `7/3<3`.  Thus "zero is a vertex" is not a sufficient
  higher-facet argument even in the plane.
- **Tangent Euclidean disk.**  For the unit disk and `|x|=1`, the `p=2`
  Firey sum is the ellipsoid with support squared
  `2(1+(x.n)^2)`, giving ratio `2 sqrt(2)<2+pi/2`; boundary placement alone is
  insufficient, and smooth bodies are strict.
- **Three-dimensional crosspolytope.**  For `C` the `l_1` unit ball and
  `x=e_1`, `C polar` is the cube, the convex hull of its two opposite facets
  `u_1=+/-1`.  This is an equality case but not a parallelotope, guarding
  against an incorrect carryover of the planar classification.
- **Endpoint singularity.**  The exponent `p-2` was checked explicitly: it is
  negative but greater than `-1` for every `1<p<2`, so the limiting argument
  covers the smallest problematic range.

## Source and scope check

The live arXiv record for Fradelizi--Manui--Meyer--Ndiaye,
arXiv:2607.03582, still listed only v1 on 2026-09-22.  Its Conjecture 4 states
the same all-dimensional symmetric-body inequality and constant.  The paper
proves the asymmetric `L_1`-zonoid case (hence the planar inequality) and only
states parallelotopes as equality examples; it does not contain the reviewed
general proof or higher-dimensional classification.  Bounded searches for
the exact identifier, title, and conjecture found no later primary proof.
This supports the target's claim boundary but is not a guarantee of priority.

The theorem does not resolve the nonsymmetric conjectures in that paper,
`p<=1`, stability, or formal verification.  The producer's exact checker
reproduces its manifest under normal and optimized Python, but it is finite
corroboration only.

## Strengthening and improvement opportunities

1. Add a named theorem-level citation for the smoothing and weak
   surface-area-measure convergence step, which is correct but currently
   summarized as standard.
2. State explicitly at the first occurrence that `0 in C+x` implies
   `x in C`; this makes the domain `|t|<=1` immediate to a reader.
3. Include the direct `p=2` square computation above as a normalization test
   in the proof text, not only the displayed value of the constant.
4. In the polar-face approximation, say "relative `(d-1)`-dimensional
   polytopes in `aff F`" to prevent "full-dimensional" from being read as
   full-dimensional in `R^d`.
5. A proof-assistant formalization of the smooth rank-one calculation would
   materially reduce the remaining human trust surface; it is not required
   for this acceptance.

