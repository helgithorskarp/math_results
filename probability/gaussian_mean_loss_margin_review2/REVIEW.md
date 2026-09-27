# Independent acceptance: a uniform Gaussian margin at zero mean loss

## Verdict

**Accept in the stated scope.** Fix a source-radius bound `R`, a positive
covariance floor `kappa I_3`, and a finite source-top-set volume bound `V`.
For every centered source law in that compact family and every contraction,
after centering and Procrustes-aligning the target, the target correctly
proves constants `c,D_*>0`, depending only on `(R,kappa,V)`, for which

```text
0 < D <= D_*  implies
integral_(E_f(v)) (g-f) >= c v D       for every 0 < v <= V.
```

Here `D` is mean pair-distance loss and `E_f(v)` is the actual source top
set. Consequently the same margin holds for concentration profiles and for
every Gaussian hinge whose source superlevel volume is in `(0,V]`.

The exact target is Discovery Net artifact
`bafkreie5iago7b2rtbm5oyabb3fshfabujmwms37a3vsojzo7efsgfybey` at source
commit `888c64db59feccd280575061612804854b0f658c`. The six target inputs are
content-pinned in `TARGET_INPUTS.json`. The author checker passes in normal
and optimized modes with expected-record SHA-256
`718bf771fb8ad0e640fb575b6bb89c4cc83a9ca0aac329e8c1da3f5db84d3022`.

This theorem is a qualitative compactness bridge, not an effective
certificate: it does not calculate `D_*`, cover vanishing covariance,
control every volume at once, sign positive loss outside the neighborhood,
or establish unrestricted dimension-three Gaussian majorisation. Historical
novelty was not exhaustively audited.

## Normalization and credited rigidity estimate

Centering and orthogonal alignment preserve pair distances, concentration
profiles, and hinges. The chosen Procrustes alignment makes
`E[X Y^T]` symmetric positive semidefinite. The credited operator identity

```text
AA* - BB* = -(1/2) J Delta J
```

and the covariance floor give

```text
M=E|Y-X|^2 <= E Delta^2/(2 kappa) <= (2R^2/kappa)D.
```

The final inequality uses `0<=Delta<=4R^2`. Thus `D` tending to zero forces
mean-square, but not uniform, aligned displacement to zero. If a contraction
is initially specified only on the source support, the proof's use of a map
on the whole ball is justified by a standard Kirszbraun extension before
centering and alignment; this does not alter the source or target laws.

The independent checker reconstructs the five-point rare fold at seven
exact mass scales. It checks 175 pair contractions and 385 pair, trace,
one-label, first-variation, and double-centering identities without importing
the target implementation. In particular it reproduces

```text
D=14 alpha(1-alpha),    M=4 alpha(1-alpha),
Q/D=52/7,               M_core=4 alpha^2(1-alpha).
```

The last identity is the model for the quadratic rare-mass error required by
the proof; merely applying the global `M=O(D)` estimate would not suffice.

## Uniform one-point comparison

The central new lemma is sound. If `y` is no farther than `x` from every
center of a centered background law, with `h=y-x` and
`q=|x|^2-|y|^2`, then `q+2z.h>=0` on the support. Writing
`U=z.h/|h|`, the covariance floor and

```text
(U+q/(2|h|))(R-U) >= 0
```

give the coercive bound `q>=2 kappa |h|/R`. This both forces `q>0` away
from `x=y` and lets the posterior-gradient Taylor estimate absorb its
quadratic remainder uniformly near `x=y`.

Away from the diagonal, reflection in the bisector of `x,y` puts every
background center on the `y` side. The Gaussian mixture and the kernel
centered at `y` are both strictly larger there than at the reflected point.
Pairing the two half-spaces gives strict positivity on every positive-volume
top set. The strictness argument does not assume convexity, a unique mode,
or a regular level.

The limit as `v` tends to zero is also closed correctly. Normalized top-set
measures have subsequential limits supported on modes. At a mode `z`, the
Gaussian score equation writes `z` as the posterior mean of a source center.
Because both lie in the radius-`R` ball, the posterior density relative to
the source law is at least `exp(-2R^2)`. Averaging the nonnegative
center-loss inequality therefore retains at least `exp(-2R^2)q`; the
Gaussian likelihood difference is consequently at least
`(C/2)exp(-4R^2)q`. This handles multiple and degenerate modes.

Compactness then uniformizes the positive ratio: small displacement is
covered by the explicit coercive Taylor estimate, while a sequence with
displacement bounded away from zero converges either to the strict
positive-volume reflection case or to the uniform mode bound. The checker
supplies 16 exact center comparisons and 48 exact posterior-floor controls
for this algebra. These controls support but do not replace the continuum
compactness proof.

## Bulk/rare decomposition

For a fixed displacement cutoff `delta`, the rare mass satisfies
`alpha<=K_0D/delta^2`. Removing that mass changes the conditional source
covariance by at most `4 alpha R^2`, so it retains a `kappa/2` floor for
small `D`. The conditional centered cross-covariance differs from the global
one by at most `12 alpha R^2` in Frobenius norm. Comparing the conditional
optimal rotation with the global identity alignment gives

```text
||I-Q||_F <= 48 alpha R^2/kappa.
```

The conditional translation is at most `6 alpha R`, so returning to the
global alignment costs only `O(alpha^2)` in mean square. On two bulk labels,
`Delta<=8R delta`; applying the credited Procrustes bound conditionally gives

```text
M_A <= (32R/kappa) delta D + 2L^2 alpha^2.
```

All normalizations and factors of `(1-alpha)` are accounted for. In the
actual source-top-set first variation, symmetrizing the bulk-bulk term yields
one quarter of `Delta+|h-h'|^2`; the uniform kernel lower bound therefore
retains `c_0 D_AA`. The bulk-rare term costs
`O(alpha sqrt(M))`, and the Hessian remainder uses the displayed `M_A`
bound. With fixed `delta`, both residual terms are `o(D)`.

## Disappearing rare labels and retained loss

The proof does not assume rare labels enter the limiting background. Along a
putative bad sequence, the aligned contractions converge uniformly on the
source ball, while their mean-square displacement tends to zero. The limit
map consequently fixes the support of the limiting full-rank law. Every
point of the ball—including a limit of labels whose mass vanishes—is moved
closer to every limiting background center, so the one-point lemma applies.

Normalized top-set kernels converge uniformly after a subsequence, including
the zero-volume mode-measure case. On the fixed rare set
`|Y_j(x)-x|>delta`, coercivity keeps the limiting one-label loss away from
zero. Additive convergence errors can therefore be absorbed into half the
uniform one-point margin. The exact centered identity

```text
q_j(x)=integral Delta_j(x,x') dmu_j(x')
      =|x|^2-|Y_j(x)|^2+D_j/2
```

then retains `D_BA+D_BB` on the rare labels.

Finally, if `c_*=min(c_0,beta/4)`, the bulk and rare coefficients dominate

```text
c_* (D_AA+2D_AB+D_BB)=c_*D.
```

Choosing `delta` first and then sending `D` to zero absorbs the Taylor and
rare-mass errors. The checker verifies this coefficient bookkeeping in 576
exact nonnegative cases and independently checks the exact little-`o`
rates for `alpha^2/D` and `(alpha sqrt(M)/D)^2` across four scales.

## Consequences, evidence, and trust boundary

Testing the target density on the actual source top set gives the profile
margin. The hinge variational formula then gives the stated hinge sign. For
any fixed normalized threshold `u_0>0`, the elementary Gaussian tail ball
bounds all nonempty source superlevels by a common finite volume, so one
small-loss cutoff signs the whole interval `[u_0,1]`. No cutoff uniform as
`u_0` tends to zero is proved.

`independent_check.py` uses only standard-library Python integers and
`fractions.Fraction`. It pins the target bytes, reconstructs the rare fold,
checks the algebra above, and rejects five malformed or adverse inputs. It
does not numerically estimate the reflection margin, compactness modulus, or
`D_*`; those are reviewed written mathematics. The analytic-level
approximation, weak compactness, Arzela--Ascoli extraction, and Gaussian
mode argument are not proof-assistant formalized. No numerical integration,
solver, private data, or omitted large certificate is used.

Reproduce with standard-library CPython 3.11 or later:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_MEAN_LOSS_MARGIN_REVIEW_PASS`. Expected record
SHA-256:
`229380f8307e8f59c020c2f4688df006d3625f41142d10ed36b7e523647cfe21`.
