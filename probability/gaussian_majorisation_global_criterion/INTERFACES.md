# Fixed-atom and global-criterion handoff for the eight research lanes

26 September 2026. This consolidates existing author proofs and their
quantifiers, with direct compatibility bounds; it supplies **no new positive
majorisation theorem or independent review**. The full
bounded-law R3 question remains open. The human-assigned lanes below keep
their independent ownership. [DEPENDENCIES.md](DEPENDENCIES.md) contains
the broader class map; [SOURCES.md](SOURCES.md) pins this handoff's inputs.

## 1. One target, three exact descriptions

Let `gamma_s` have covariance `s I_3`, let `T` be 1-Lipschitz, and write
`f=mu*gamma_s`, `g=(T#mu)*gamma_s`. Set

```text
H_p(a) = integral (p-a)_+,
Delta_s(mu,T) = sup_(a>=0) (H_f(a)-H_g(a))_+.
```

For each specified `mu,T,s`, the [global proof](PROOF.md) identifies this
number with both the minimum endpoint density-value coupling failure and
the limit of increasing finite beta defects `D_N`. Explicitly, if `X`
has density `f`, `U` is independent uniform on `(0,1)`, and
`C=(2*pi*s)^(-3/2)`, the scalar law is `Z_f=U f(X)/C`; use `Z_g`
similarly. Then

```text
Delta_s = min_(couplings of Z_f,Z_g) Pr(Z_f>Z_g)
        = lim_(N->infinity) max(0,-min_(0<=k<=N) b_(N,k)).
```

The equivalent spatial coupling uses the probability densities
`f(x)gamma_s^(2)(z)` and `g(y)gamma_s^(2)(w)` in five dimensions and
compares their density values. The coupling may depend on `mu,T,s`.
There is no requirement of a common position noise, a martingale, a
deterministic map, or a continuous motion of the labelled centres.

Now fix **one** `0<epsilon<1`. The [fixed-atom proof](ANCHOR_REDUCTION.md)
reduces the full question to variance **one**, for every law

```text
mu_rho=(1-epsilon)delta_0+epsilon rho,
T(0)=0,   rho an arbitrary bounded probability law.
```

It suffices to consider arbitrary compact rare supports `K` disjoint from
zero, so the input atom has exactly the prescribed mass. The reduction
supplies no common support-radius or atom-count bound, and imposes no
restriction to ordered rays or motion domains. Fixing epsilon and variance
does not remove these quantifiers. The restricted assertion remains unproved.

The measure lane's [common-set dual](../gaussian_prior_localization/PROOF.md),
Sections 1--3, gives the same all-prior target without a prior-dependent
test set. For fixed `K,T,s,epsilon`, put

```text
D_epsilon(K,T;s) = sup_(rho in P(K)) Delta_s(mu_rho,T),
q_(A,B)(x) = integral_B gamma_s(z-Tx) dz
          - integral_A gamma_s(z-x) dz,
m_epsilon(A) = max_(B: |B|=|A|)
    [(1-epsilon)q_(A,B)(0) + epsilon min_(x in K) q_(A,B)(x)].
```

Here `A` ranges over measurable sets of finite positive volume. The exact
identification is

```text
D_epsilon(K,T;s) = sup_A (-m_epsilon(A))_+.
```

This follows from the cited concentration/hinge defect identity and its
anchored minimax formula. Thus the full conjecture is also equivalent to
`m_epsilon(A)>=0` for **every** such `A,K,T` at `s=1`, for the one fixed
epsilon. For each `A`, a maximizing ordinary set `B` exists and can be a
superlevel set of a minimizing target mixture. It may depend on
`A,K,T,s,epsilon`, but must work for every subsequently chosen `rho` on
that `K`. No finite support for the minimizing rare law is implied.

The correct common-set certificate is

```text
q_(A,B)(x) >= -(1-epsilon)q_(A,B)(0)/epsilon   for every x in K.
```

Dropping the anchor term imposes a stronger condition. Conversely,
choosing a different optimizing `B` for each tested prior does not supply
the common-set certificate. The scalar coupling and common-set criteria
are equivalent at their stated levels of quantification; their witnesses
need not have the same dependence on the prior.

## 2. What each lane can return to the shared criterion

These are mathematical interfaces under the existing human assignments,
not new task assignments or assumptions that a proposed method succeeds.

| Owner | Result that the shared criterion can consume | Boundary to preserve |
|---|---|---|
| 1: semigroup/PDE evolution | The [ordered-contact reduction](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md): the full question is equivalent to `J_f>=J_g` where regularized strict-contraction profiles are globally ordered and touch | The reduction now includes critical levels and a transverse first contact. The contact flux sign is still unproved. Its Gaussian-tailed auxiliary input is unbounded; the smoothing and truncation bridges are explicit. The earlier coefficient ordering remains false. |
| 2: certified finite-atomic dependencies | Exact contraction data and a rigorously negative integrated hinge or beta test; alternatively all inputs of the existing finite positive certificate | Finite positive moments alone are incomplete. A universal finite orthogonal averaging rule for arbitrary square-cone weights is now excluded by the [finite-rule source](../gaussian_majorisation_finite_orbit_obstruction/PROOF.md). Weight-dependent rules, infinite averaging and radial transport are not excluded. |
| 3: measure localization | The common-set certificate above; and now the [uniform defect localization](../gaussian_prior_localization/DEFECT_LOCALIZATION.md), giving compact finite maxima within `4/k` of the unrestricted defect | The unique diffuse optimizer rules out exact atomic attainment, not finite detection. Conditioning changes the prior and need not preserve a prescribed dominant atom. Section 4 applies localization **before** a new anchor construction. |
| 4: extremal maps/deformation geometry | The [rigid-mesh reduction](../gaussian_majorisation_extremal_maps/PROOF.md) preserves strict failures after support enlargement into a continuous piecewise-isometric tetrahedral map; its anchored finite restriction is extreme and its tight framework rigid | This does not assert an extreme optimizer on the original fixed domain. Mesh complexity is unbounded; the class contains known R5-motion obstructions. The comparison for arbitrary compatible folds remains open. |
| 5: analytic/optimal transport | A zero-failure endpoint density-value coupling, or a fully integrated hinge sign, with arbitrary rare packets retained | The exact reductions are dependencies, not positive assertions. A zero base defect plus the unsigned remote-anchor error does not prove finite-distance adjunction. |
| 6: geometric/internal energy | Certified domain-wide motions and their stated Gaussian and ball consequences, organized in the [geometric review portfolio](../gaussian_axial_cone_rotations/REVIEW_GUIDE.md) and [eight-lane benchmark handoff](../gaussian_axial_cone_rotations/LANE_HANDOFF.md) | Such motions are sufficient coupling constructions. The known extreme but flexible positive benchmark is not a general rigid-mesh sign theorem. Review of the original axial/nonlinear core need not depend on the later matrix-path optimization. |
| 7: actual counterexamples | A validated negative integrated hinge or convex energy for a genuine contraction | Negative finite-orbit averages and failed proof mechanisms are different statements. The finite-rule source even has a negative orbit control with identically zero integrated gap. |
| 8: functional inequalities/stability | Its [finite-certificate interface](../gaussian_majorisation_open_stability/CERTIFICATE_INTERFACE.md): rigorously enclosed normalized moments, an absolute source-peak bound, signed low-threshold control and strict beta margins | The localized beta error improves on a fixed positive threshold interval. It supplies no uniform degree on the compact frontier, whose equality and zero-weight cases remain. Arbitrary origin mass on ordered rays does not supply arbitrary rare geometry. |

In the PDE source's notation, `L_p(s,v)=sup_(|A|=v) integral_A p_s` and
`W=L_g-L_f`. Hence `Delta_s=sup_v(-W)_+` by the same concentration/hinge
identity used above. Its regular-rectangle formula is
`W(endpoint)=E W(stopped boundary)+E integral F`, with
`F=(kappa_g-kappa_f)(L_f)_(vv)/2`. The sign of this **sum** would be an
input to the global criterion; a pointwise coefficient sign is not
necessary. The subsequent [contact reduction](../gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md)
reaches a stronger equivalent frontier without extending that stopped
representation. Gaussian regularization before applying a strict contraction
gives strict initial order and both volume-end controls. A scalar target
dilation makes a hypothetical first failure transverse. Its bulk flux
`J_u=-integral_(u>a) Delta u` is defined through critical levels. At every
globally ordered contact with equal positive finite volume and density level,
the remaining condition is `J_f>=J_g`. Equivalently, its unweighted integrals
of posterior covariance traces over the two superlevel sets obey `K_f<=K_g`.
This is not a whole-space density-weighted MMSE comparison. The sign remains
open, and no uniform time or volume cutoff is supplied. For finite atomic
laws, `L_p(s,v)->1` hides the exponential scale
`-2s log(1-L_p(s,v))->rho_support(v)^2`, where `rho_support` is inverse
tube volume. The source's constants depend on the least atom weight.
The flat initial limit gives no signed comparison. The new contact reduction
avoids that initial layer by changing to a regularized input, with an explicit
error retaining a hypothetical violation. The fixed-atom reduction itself
still gives no uniform regular perturbation theorem at a Dirac law.

## 3. Error budget for a strict witness

The following is a direct composition of existing estimates, provided to
connect finite certification to the global reduction. It introduces no
new localization theorem or assertion that a negative example exists.

Suppose a base contraction pair has `H_f(a*)-H_g(a*)=delta>0`.
The contractive remote-anchor construction, including its **output
translation**, gives an anchored pair with gap at least
`epsilon delta-beta_R` at threshold `epsilon a*`, where

```text
beta_R <= exp(-(R-M)^2/(8s)).
```

Choose `R` satisfying the construction's contraction conditions and
`beta_R<=epsilon delta/2`. The anchored gap is at least
`epsilon delta/2`. After translating the anchor to zero, restrict its
rare packet to a finite `h`-net inside its own support, using the original
map at the selected sites and leaving the anchor fixed. The map is still
a contraction. The [net estimate](../gaussian_prior_localization/PROOF.md),
Section 5, together with the total-variation hinge bound gives an error
of at most

```text
E_mesh = 2 epsilon h/sqrt(2*pi*s)
```

for the hinge difference at any threshold. Choosing
`E_mesh<=epsilon delta/4` leaves a finite contraction pair with gap at
least `epsilon delta/4`. This approximates a strict witness; it does not
assert that a minimizer is atomic or impose a universal atom bound in this
anchor-first construction. Section 4 instead localizes the base witness
before adding a new anchor.
Independent rational perturbations still need the separate
[strict rational-witness reduction](../gaussian_majorisation_rank_abel/PROOF.md)
and verified pairwise contraction inequalities.

For this finite pair, the global bound
`D_N<=Delta_s<=D_N+K_s(N+2)^(-1/4)` ensures a negative beta test once
`K_s(N+2)^(-1/4)<epsilon delta/4`. Certified upper endpoints for some
`b_(N,k)` must be strictly negative to report a finite witness. This gives
conditional finite detection, with no practical degree claim; the remote
support may make the elementary constant large. The three controls are
different: anchor separation, approximation of the rare law, and moment
localization. None can be replaced by bare finite positivity.

The new map reduction can also retain the **same** prescribed dominant
atom. Include zero among the finite interpolation sites and mesh vertices,
so its piecewise-isometric extension `F` fixes zero. Instead of adding
mass to the whole law, replace only its rare law by

```text
rho_eta=(1-eta)rho+eta nu,
mu_eta=(1-epsilon)delta_0+epsilon rho_eta,
```

where `nu` gives positive mass to every nonzero mesh vertex. The full law
then gives positive mass to every vertex and its anchor mass stays exactly
`1-epsilon`. Each convolved endpoint changes in total variation by at most
`epsilon eta`. The [existing hinge continuity bound](PROOF.md), Section 5,
therefore changes any hinge gap by at most `2 epsilon eta`. A prior gap
`d>0` survives whenever `2 epsilon eta<d`; the remaining margin is the one
to use in the moment bound above. If extra sites are needed to obtain a
full-dimensional source, add their mass inside the rare packet with the
same bound before applying the mesh extension. Only finitely many such
positive-margin steps are needed.

This direct composition of the two published reductions requires neither
an atomic minimizer nor a Jensen argument in map positions. Conditional on
any failure, it gives a fixed-epsilon, variance-one witness on a weighted
rigid mesh with the same anchor. It adds no positive comparison class and
no mesh-size bound. The source's separate uniform-mass normalization is a
different test class and is not imposed simultaneously here. The external
piecewise-isometric extension and rigidity claims remain the map lane's
author-proof dependencies, with independent review pending.

## 4. Compact finite data, moment degree and a prescribed anchor

This section composes the measure lane's new localization theorem with
the existing global and fixed-atom bounds. It does not replace that
theorem's proof or the finite-atomic lane's enclosure work. All three
proof inputs remain author results awaiting independent review.

Let `D` be the supremum of `Delta_s` over every bounded law, contraction
and variance. Scaling permits variance one. Use the compact parameter
set `P_k` from [DEFECT_LOCALIZATION.md](../gaussian_prior_localization/DEFECT_LOCALIZATION.md):
at most `k^6` matched atoms, probability weights, `x_1=y_1=0`, both
supports in `B(0,2k)`, and every pairwise contraction constraint. Zero
weights and collisions are included. Its attained maximum `D_k` satisfies

```text
0 <= D-D_k < 4/k,              D_k increases to D.
```

Keep the localization index `k` distinct from the moment degree `N`.
For a configuration `P` let `d_N(P)=max(0,-min_j b_(N,j)(P))`, the
quantity called `D_N` in the global proof, and put

```text
B_(k,N) = max_(P in P_k) d_N(P),
K_k = K(2k,1).
```

These maxima exist: every replica moment is a continuous finite
exponential sum of the weights and squared distances, also at zero
weights and collisions. The global estimate holds uniformly on `P_k`.
Taking maxima and then applying localization therefore gives

```text
0 <= B_(k,N) <= D_k <= D,
D <= min(1, B_(k,N) + K_k (N+2)^(-1/4) + 4/k).          (A)
```

This is a reusable **uniform** certificate contract. Certified lower
bounds `b_(N,j)(P)>=-eta` for every `P in P_k` and every `0<=j<=N`
give `B_(k,N)<=max(0,eta)`. Testing selected configurations does not give
that bound. Conversely, one certified negative beta value at a feasible
configuration is already a negative convex-energy witness.

For a completely explicit diagonal, the global constant gives, for `k>=1`,

```text
K_k = (16/3)sqrt(2/pi) k^3 + 8sqrt(2) k^2
                         + 16sqrt(2/pi) k + 4sqrt(2)
    < (118/3) k^3 < 40 k^3.
```

Use `sqrt(2/pi)<1`, `sqrt(2)<3/2` and `k,k^2<=k^3`.
Thus `N_k=(40 k^4)^4` and `L_k=B_(k,N_k)` obey

```text
L_k increases to D,          0 <= D-L_k < 5/k.          (B)
```

Monotonicity follows from nesting `P_k` and beta degree elevation. The
full question is equivalent to `L_k=0` for every integer `k>=1`.
This is an explicit accuracy schedule, not a practical enumeration,
an evaluated maximum, or a finite decision procedure for `D=0`.
The maxima still range over all real feasible configurations. No fixed
coordinate denominator or certified optimizer is supplied.

There is also a direct way to retain the prescribed atom while keeping
defect-dependent finite bounds. **Localize first, then adjoin a new atom.**
Fix `0<epsilon<1`, `k>=1`, a unit vector `e`, and set

```text
c_epsilon = sqrt(8 log(1/epsilon)),
L=8k,       R=14k+c_epsilon,       z_R=R e.
```

For any `P in P_k`, translate its rare output sites to `y_i+L e` and
adjoin the common atom `z_R` with mass `1-epsilon`; give the original
pair total mass `epsilon`. The new anchor distances contract because

```text
e.(y_i+L e-x_i) >= 4k,
|y_i+L e|^2-|x_i|^2 <= 100 k^2 < 8Rk.
```

Indeed the difference of squared distances to `z_R` is the second
expression minus `2R` times the first. Every other distance constraint
is inherited. The anchor proof's projection bound is `M<=10k`, so

```text
beta_R <= exp(-(R-10k)^2/8)
        <= epsilon exp(-2k^2) < epsilon/k.              (C)
```

After translating the anchor to zero the rare input is `x_i-R e` and
its image is `y_i+(8k-R)e`. Both supports lie in
`B(0,16k+c_epsilon)`; every rare input has norm at least `12k+c_epsilon`,
so the input atom has **exactly** the prescribed mass. At most `k^6+1`
sites are used. A base gap `d` at a threshold `a` becomes a gap at least
`epsilon(d-exp(-2k^2))` at threshold `epsilon a`.

Consequently any original violation of size `delta>0`, after variance
normalization, has such an anchored witness with gap at least
`epsilon delta/2` whenever `k>=10/delta`: localization costs less than
`4/k` and anchoring costs less than `epsilon/k`. This is a different
conditional witness, not preservation of the original prior or its atom
during conditioning. The support bound depends on the desired defect
resolution and on epsilon; no single bounded test domain settles the
full question. Subsequent rare-only mesh augmentation still costs
`2 epsilon eta`, and no bound for the added mesh vertices is asserted.

The functional lane's [exact certificate](../gaussian_majorisation_open_stability/CERTIFICATE_INTERFACE.md)
has a different purpose from (A)--(B): for one strict finite rational
instance it can prove **zero** defect, given its signed endpoint and
strict localized beta margins. Its full-question equivalence is
`for every such instance, there exists a finite certificate`. Compactness
of `P_k` cannot exchange those quantifiers or supply a uniform strict
degree: `P_k` contains equality and zero-weight cases. Its all-pair
strict test class is also distinct from a rigid mesh with tight edges.
An absolute peak bound needs absolute source moments, not only their
target-minus-source differences. Neither its conditional exact test nor
our uniform defect approximation generates the missing moment enclosures
or establishes their required signs.

## 5. Geometric conclusions and validation boundary

The [existing class map](DEPENDENCIES.md) retains the broad motion classes
with all weights on their domains and the ordered-orbit class with its
ordered weights/radii. Their positive Kneser--Poulsen conclusions are not
claims about the arbitrary packet above. For a general varying-radius
Gaussian transfer, the [geometric annex](GEOMETRIC_LIMIT.md) requires the
normalized small-variance scale `liminf Delta_s/a_s=0`; absolute
`Delta_s->0` does not suffice. Intersections use a separate motion theorem.

All formulas here are sourced identities or direct compositions of the
linked estimates; Section 4 writes out the new constant and anchor-distance
checks. The proof files, mathematical programs and certificates
of the global criterion and fixed-atom reduction are unchanged. No new
numerical experiment, program replay, formalization or independent
acceptance is claimed by this documentation update. Validate the compact
source manifest with `sha256sum -c SHA256SUMS`; the existing README retains
the original mathematical reproduction commands and their trust limits.
