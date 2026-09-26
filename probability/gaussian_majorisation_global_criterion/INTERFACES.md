# Fixed-atom and global-criterion handoff for the eight research lanes

26 September 2026. This consolidates existing author proofs and their
quantifiers; it is **not a new theorem or an independent review**. The full
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
| 1: semigroup/PDE evolution | A signed global profile evolution or endpoint comparison for arbitrary anchored inputs; the [new heat-profile source](../gaussian_majorisation_heat_profiles/PROOF.md) identifies the boundary and integrated-forcing obligation | Its representation is on regular rectangles with positive variance. Coefficient ordering fails even for a strict injective contraction that has full majorisation. Critical levels, boundary data and atomic initial time remain explicit obligations. |
| 2: certified finite-atomic dependencies | Exact contraction data and a rigorously negative integrated hinge or beta test; alternatively all inputs of the existing finite positive certificate | Finite positive moments alone are incomplete. A universal finite orthogonal averaging rule for arbitrary square-cone weights is now excluded by the [finite-rule source](../gaussian_majorisation_finite_orbit_obstruction/PROOF.md). Weight-dependent rules, infinite averaging and radial transport are not excluded. |
| 3: measure localization | For all source sets, the common-set certificate above; or a reduction of priors/sets that preserves a strict negative value with a proved error | The [unique diffuse optimizer](../gaussian_prior_localization/PROOF.md) rules out exact atomic attainment, including for a dominant fixed atom. It does not rule out finite detection of a strict failure. |
| 4: extremal maps/deformation geometry | The [rigid-mesh reduction](../gaussian_majorisation_extremal_maps/PROOF.md) preserves strict failures after support enlargement into a continuous piecewise-isometric tetrahedral map; its anchored finite restriction is extreme and its tight framework rigid | This does not assert an extreme optimizer on the original fixed domain. Mesh complexity is unbounded; the class contains known R5-motion obstructions. The comparison for arbitrary compatible folds remains open. |
| 5: analytic/optimal transport | A zero-failure endpoint density-value coupling, or a fully integrated hinge sign, with arbitrary rare packets retained | The exact reductions are dependencies, not positive assertions. A zero base defect plus the unsigned remote-anchor error does not prove finite-distance adjunction. |
| 6: geometric/internal energy | Certified domain-wide motions and their stated Gaussian and ball consequences, organized in the [geometric review portfolio](../gaussian_axial_cone_rotations/REVIEW_GUIDE.md) | Such motions are sufficient coupling constructions. Failure of the motion mechanism is not a negative endpoint comparison. Review of the original axial/nonlinear core need not depend on the later matrix-path optimization. |
| 7: actual counterexamples | A validated negative integrated hinge or convex energy for a genuine contraction | Negative finite-orbit averages and failed proof mechanisms are different statements. The finite-rule source even has a negative orbit control with identically zero integrated gap. |
| 8: functional inequalities/stability | Its signed endpoint bounds, peak cutoff and strict finite beta margins, or its existing orbit certificates | The [functional handoff](../gaussian_majorisation_open_stability/HANDOFF.md) retains law-dependent neighborhoods and all certificate premises. Arbitrary origin mass on ordered rays does not supply arbitrary rare geometry. |

In the PDE source's notation, `L_p(s,v)=sup_(|A|=v) integral_A p_s` and
`W=L_g-L_f`. Hence `Delta_s=sup_v(-W)_+` by the same concentration/hinge
identity used above. Its regular-rectangle formula is
`W(endpoint)=E W(stopped boundary)+E integral F`, with
`F=(kappa_g-kappa_f)(L_f)_(vv)/2`. The sign of this **sum** would be an
input to the global criterion; a pointwise coefficient sign is not
necessary. Its first-contact proposal remains unproved. For finite atomic
laws, `L_p(s,v)->1` hides the exponential scale
`-2s log(1-L_p(s,v))->rho_support(v)^2`, where `rho_support` is inverse
tube volume. The source's constants depend on the least atom weight.
The flat initial limit gives no signed comparison. The fixed-atom reduction
gives no uniform regular perturbation theorem at a Dirac law.

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
assert that a minimizer is atomic or impose a universal atom bound.
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

## 4. Geometric conclusions and validation boundary

The [existing class map](DEPENDENCIES.md) retains the broad motion classes
with all weights on their domains and the ordered-orbit class with its
ordered weights/radii. Their positive Kneser--Poulsen conclusions are not
claims about the arbitrary packet above. For a general varying-radius
Gaussian transfer, the [geometric annex](GEOMETRIC_LIMIT.md) requires the
normalized small-variance scale `liminf Delta_s/a_s=0`; absolute
`Delta_s->0` does not suffice. Intersections use a separate motion theorem.

All formulas here are sourced identities or direct substitutions in the
linked estimates. The proof files, mathematical programs and certificates
of the global criterion and fixed-atom reduction are unchanged. No new
numerical experiment, program replay, formalization or independent
acceptance is claimed by this documentation update. Validate the compact
source manifest with `sha256sum -c SHA256SUMS`; the existing README retains
the original mathematical reproduction commands and their trust limits.
