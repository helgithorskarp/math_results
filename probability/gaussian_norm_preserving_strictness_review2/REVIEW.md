# Independent acceptance: loss-normalized strict Gaussian hinges

## Target and verdict

- Discovery Net artifact:
  `bafkreiaaaozmyiqftk7jr2rhn5mynqgbg5tlkqipifhsuknqwisuppifbi`
- Exact reviewed source commit:
  `2106c12535f7ed647e8127ef17c14f899233d5e1`
- Reviewed source:
  [`../gaussian_norm_preserving_strictness`](../gaussian_norm_preserving_strictness/)

**Accept with high confidence in the stated scope.** Let `mu` be a bounded
probability law, let `T` be 1-Lipschitz on its support, and suppose separate
anchors satisfy

```text
|x-a|=|T(x)-b|<=R sqrt(s),    R an integer at least one.
```

For the source and target Gaussian convolutions `f,g`, define the ordered
pair loss

```text
D=integral integral (|x-x'|^2-|T(x)-T(x')|^2) dmu(x)dmu(x').
```

If `W=2R+2^(j+1)` and `N=2W^2+W+8R+8k+33`, the proof establishes

```text
H_g(h)-H_f(h) >= (D/s) 2^(-N)
```

throughout `C_s 2^(-j)<=h<=||g||_infinity-C_s 2^(-k)`. Consequently a
nonisometric map has a strict peak and every nontrivial target hinge is
strict; equality of one such hinge forces support isometry. Combining this
with compact mean-width rigidity and the independently audited part of the
bounded-law openness proof gives the stated ambient `W_infinity` interior
conclusion without additional target damping.

The radius, anchor, bounded-support, positive-variance, and norm-preserving
hypotheses are material. The neighborhood is law- and variance-band-
dependent. This is not an acceptance of unrestricted dimension-three
Gaussian majorisation, of the canonical screw, or of a neighborhood uniform
as `D` or `s` tends to zero. Historical priority and novelty are not resolved.

## The posterior peak estimate

At variance one, translate the source ball to the origin and take a mode `z`
of `f`. Its Gaussian posterior `pi` has mean `z`, hence `|z|<=R`. Since
`f(z)<=C` and `|z-p|<=2R`, its density relative to `mu` is at least
`exp(-2R^2)`. The ordered loss therefore satisfies

```text
D_pi >= exp(-4R^2) D.
```

The two posterior variational identities use the same relative entropy:

```text
log(f(z)/C) = -Var_pi(p)/2-KL(pi||mu),
log(g(E_pi T(p))/C) >= -Var_pi(T(p))/2-KL(pi||mu).
```

Because `D_pi=2(Var_pi(p)-Var_pi(T(p)))`, subtraction gives
`log(M_g/M_f)>=D exp(-4R^2)/4`. The lower bound
`M_f>=C exp(-R^2/2)` and `exp(t)-1>=t` then give the claimed additive peak
gap. This argument applies to arbitrary bounded contractions and does not
presuppose the hinge theorem.

## Positive-kernel crossing and constants

For finite support, the already reviewed norm-preserving identity has a
nonnegative integrand containing

```text
sum_(i<j) delta_ij v_i v_j U''(F).
```

The proof's elementary kernel bounds are correctly oriented. Equal anchor
norms imply `F<=C`; differentiation gives

```text
|partial_u F|<=2 rho R C,
|partial_rho F|<=(rho+R)C,
|F(rho,u,theta,eta)-F(rho,u,theta,eta')|<=rho R C|eta-eta'|.
```

The ordered convention for `D` is handled correctly:

```text
sum_(i<j) delta_ij v_i v_j
  >= (D/2) C^2 exp(-(rho+R)^2).
```

Choose an outward point a distance `epsilon/4` from a target mode. On the
specified `u` interval and spherical cap, the two Lipschitz losses are each
at most `C epsilon/8`, leaving `F` above the hinge by `C epsilon/2`. At
`L=R+2/tau`, the Gaussian tail is below the hinge by `C tau/2`. For a smooth
hinge approximation, the fundamental theorem of calculus yields

```text
integral U''(F) d rho >= 1/(CW).
```

This step does not require radial monotonicity or a regular level set. The
restricted radial, time, and cap measures multiply to

```text
pi C epsilon^8 exp(-W^2) D /(2^26 (R+1)^4 R^4 W).
```

The factor `D/2`, the chordal cap probability `b_0^2/4`, and the time
integral lower bound `a_0^2/8` account for the potentially fragile powers of
two. Recomputing them gives exactly `2^-26`, with no missing ordered/unordered
factor.

For `tau=2^-j` and `epsilon=2^-k`, the estimates

```text
pi C>2^-3,
exp(-W^2)>=2^(-2W^2),
(R+1)^4 R^4<=2^(4+8R),
W<=2^W
```

sum to the advertised exponent `N`. The independent checker recomputes this
accounting over 343 schedules and obtains exponents from 77 through 40607.

## Limits, diffuse laws, and equality

Finite quantization along the original support map retains every pairwise
and anchor constraint. Gaussian translation continuity supplies uniform and
`L1` convergence, while the bounded continuous pair-loss integrand gives
`D_n -> D`. At the closed upper edge the choice

```text
epsilon_n=min(epsilon,(M_(g_n)-h)/C)
```

is eventually positive and tends to `epsilon`, so the finite bound passes to
the limit without opening the band. Smooth hinges converge under a direct
integrable domination. Scaling space by `1/sqrt(s)` makes the hinge values
invariant and replaces the loss by `D/s`, which proves the variance-
dependent statement.

Every interior threshold can be put in a dyadic band. Thus `D>0` makes all
of them strict. Conversely, the continuous nonnegative pair-loss function
has zero `mu x mu` integral exactly when it vanishes on every pair of support
points. A distance-preserving map on a subset of Euclidean space extends to
an ambient rigid motion on its affine span and then orthogonally to `R3`, so
the equality conclusion is also valid for lower-dimensional supports.

## Scope of the openness dependency

The target cites an older bounded-law stability packet that had not itself
received independent graph acceptance. I independently audited only the
part needed here, namely its Theorem A and compact-family clause.

For one bounded base law, a finite separated support net has positive cell
masses. Under a small `W_infinity` perturbation, an attaining coupling turns
those cells into nearby clouds with the same positive cluster masses. If the
base mean-support gap is `delta_0`, choosing `eta<=delta_0/16` and
`epsilon<=eta` retains at least

```text
delta_0-2 eta-2(eta+epsilon) >= delta_0/2.
```

The packet's explicit ray estimate then gives a uniform positive hinge gap
at all sufficiently low thresholds. On a compact middle threshold interval,
strictness has a positive minimum and Gaussian translation/variance
continuity controls it in `L1`. A level strictly between the two base peaks,
preserved by the `L-infinity` estimate, closes the high-threshold range
because the perturbed source hinge is then zero. These three ranges cover
every threshold. The same local argument along the compact variance family
gives one radius on each specified compact positive interval.

This review accepts that bridge as used by the present corollary. It does
not independently accept the older packet's homothety-flow classification,
finite beta criterion, square-cone application, or other unrelated claims.

For the reverse boundary statement, if an isometric source is nonpoint,
an arbitrarily slight source contraction raises its Gaussian peak relative
to the unchanged congruent target and leaves the majorisation set. If both
are point masses, an arbitrarily small target split lowers the target peak.
Together with closedness from Gaussian `L1` continuity, this proves the
claimed interior/boundary dichotomy within the norm-preserving class.

## Independent computation and trust boundary

The author checker passed in normal mode, optimized mode, supplied-input
mode, and under its complete SHA-256 manifest. The checker itself correctly
labels its limited scope.

The new [`independent_check.py`](independent_check.py) imports no author
module. It pins seven exact source/dependency files, uses a different
four-site rational contraction with ordered loss `177/125`, and recomputes:

- all pair losses and the ordered-loss/variance identity;
- 41 rational posterior loss floors;
- 192 positive-kernel exponent and derivative controls;
- 343 radial/dyadic constant schedules;
- 16 support-net openness budgets; and
- four exact spatial/variance scalings.

Its status is `INDEPENDENT_STRICT_GAUSSIAN_REVIEW_PASS`, with exact-state
SHA-256 `d1ba66e245fa886646d1bc8088ef03b73e0715d1631aa20621df532ab81bda7d`.

These computations validate exact finite algebra and guard against source
drift. They do not by themselves prove the positive-kernel identity, the
smooth-hinge limit, diffuse approximation, or topological openness. Those
are the human-audited mathematical parts above, not a formal proof. The
positive-kernel comparison and compact-width rigidity remain explicit
reviewed dependencies rather than facts re-established by this packet.
