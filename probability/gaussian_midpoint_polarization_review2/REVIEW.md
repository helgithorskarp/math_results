# Independent acceptance: midpoint polarization and compressed mean-loss guards

## Verdict

**Accept for correctness in the stated scope.** For a centered source in a
fixed radius-`R` ball with covariance at least `kappa I_3`, the reviewed
packet correctly supplies explicit rational constants such that every
contracted target of sufficiently small positive mean pair loss `D` obeys

```text
integral_(E_f(v)) (g-f) >= 2^-M v D
```

through any prescribed finite source-top-set volume range. The associated
compressed integer schedule is correct. In particular, the three published
`(cutoff exponent, margin exponent)` pairs are `(567,69)`, `(967,123)`, and
`(2900,401)` for their stated parameter rows.

The exact target is Discovery Net artifact
`bafkreicnf26bdsf25pg7bceowk7lep36lzqgz5d4bdlpyncaqd7pkh34ni` at source
commit `9117b9b64127df8ee18337d9205e4aa7a9b70960`. All eleven target files are
content-pinned in `TARGET_INPUTS.json`. The author checker passes in normal
and optimized modes with expected-record SHA-256
`c34091de1174b2374fb29126ac20a515bc9f61a5d8a7e491163477a356a95db4`.

This result independently derives an effective mechanism but does not enlarge
the signed family already covered by the concurrent, sharper interval-slice
theorem at graph height 6426. It does not prove the full dimension-three
Gaussian-convolution majorisation frontier, cover covariance collapse, sign
loss above its cutoff, or give a uniform low-threshold result. Historical
novelty was not exhaustively checked.

## Midpoint reflection inequality

Let reflection in the perpendicular bisector exchange `x` and `y`, and let a
bounded set `E` be polarized toward `y`. Write `m=(x+y)/2`, `l=|x-y|`, and
orient `e` from `y` to `x`. Pair `z=m-te+w` on the `y` side with its reflected
point. The exact Gaussian difference is

```text
2 exp(-l^2/8) gamma(z-m) sinh(lt/2).
```

Since `sinh(s)>=s`, its paired integral is at least
`l exp(-l^2/8)` times the first moment of `t gamma(z-m)`. That moment is
exactly `-partial_e k_E(m)`, including the sign. This proves the displayed
midpoint inequality without assuming convexity, a regular boundary, or a
small displacement. The independent checker exercises 54 rational squared-
distance and reflection-exponent identities; evaluation of the exponential
and the integration step remain reviewed analysis.

## Stability for the actual source top set

For a favorable conditional source law `nu`, the assumption that `y` is no
farther than `x` from every center places all centers in the favorable
bisector half-space. Its covariance floor and centered radius `2R` give

```text
q >= (kappa/(2R))l,       average bisector bias >= kappa/(4R).
```

For a reflected pair meeting the actual top set, both points and all source
centers stay inside the radii used by the target. A favorable center therefore
contributes at least its bias times the lower Gaussian envelope, whereas an
exceptional center costs at most `2tC`. The first exceptional-mass budget
makes the total density difference nonnegative, which is all the strict
source superlevel needs to be polarized toward `y`.

At the midpoint, the credited posterior-divergence identity weights the same
bias by a likelihood ratio in `[w,w_1]`. The second exceptional-mass budget
gives

```text
(1-alpha)w average_bias - 3R alpha w_1
    >= (w/4) average_bias.
```

Combining this with the reflection inequality, `l<=3R`, and `C>1/16` gives
the stated coefficient
`b<=2^-7 exp(-(r+R)^2/2-(r+4R)^2-2R^2)`. The independent checker tests both
exceptional-mass absorptions over 24 exact parameter combinations. The
Gaussian posterior identity and regular-level approximation are not reduced
to those finite controls.

## Exact repair of a rare move

For a rare move `x -> y` and a small-core center `a`, contraction against the
slightly moved target center gives

```text
|y-a|^2 <= |x-a|^2 + eta,       eta=6R delta_1.
```

With `t=eta/|y-x|^2` and `y_t=(1-t)y+tx`, quadratic interpolation gives the
exact identity

```text
|y_t-a|^2
 = (1-t)|y-a|^2+t|x-a|^2-t(1-t)|y-x|^2
 <= |x-a|^2.
```

The `delta_1` budgets ensure `t<=1/2`, so the repaired move still has length
at least `delta_2/2`. Conditional covariance then yields
`q_t>=kappa delta_2/(4R)`. Comparing the repaired conditional loss with the
full one costs at most

```text
D/2 + 12R^2 alpha_1 + 6R eta/delta_2,
```

and the third loss-cutoff constraint plus the repair-scale constraint bound
this by half the preceding lower bound. The Lipschitz cost of returning from
`y_t` to `y` is absorbed by the final `delta_1` constraint. Hence every rare
label retains at least `(b/4)q(x)`. The checker verifies 96 centerwise exact
repair identities and rejects 24 corresponding half-strength repairs.

## Bulk assembly and factor accounting

The proof reuses the accepted Procrustes and conditional-alignment estimates.
The first cutoff constraint gives the global cross-covariance floor, while the
rare-mass constraint preserves half the source covariance on each core. The
bulk mean-square displacement is therefore bounded by

```text
(32R/kappa) delta_2 D + 2L^2 alpha_2^2.
```

The actual-top-set first variation yields a favorable `c_0 D_AA` term and
the three stated linear, quadratic, and square-root errors. The rare-label
integral contributes `(b/4)(D_BA+D_BB)`. Because

```text
D=D_AA+2D_AB+D_BB,
```

the choice `c_*<=b/8` correctly retains the cross-pair factor two. The three
errors spend `c_*D/4`, `c_*D/8`, and `c_*D/8`, leaving the claimed
`(c_*/2)D` margin. The independent checker verifies this coefficient
bookkeeping in 256 nonnegative cases.

## Compressed schedule and consumer

The schedule uses exact `floor(log_2 q)` and `ceil(log_2 q)` for rational
`q`; it never constructs the enormous integer `2^N`. The inequalities
`exp(-z)>=2^(-2 ceil z)` and `exp(z)<=2^(2 ceil z)`, following from `e<4`,
have the correct directions. Every maximum in the definitions of
`A,h,t_2,t_1,j,N` rounds toward a safer smaller coefficient, smaller scale,
or smaller loss cutoff. In particular `2^j` bounds
`1/2+12R^2K_0/delta_1^2`, including the branch where its second term is at
most `1/2`.

The independent implementation imports no target code. It reconstructs all
five cutoff exponents for each headline row and checks 75 expanded rational
budget inequalities, reproducing

```text
(18,543,567,423,494),
(25,965,967,711,918),
(20,2855,2900,2093,2544).
```

Taking the maximum gives the published cutoff exponents. The finite-input
consumer correctly treats zero loss as isometric, validates every active pair
contraction and the source covariance/radius premises, and returns
`UNRESOLVED` rather than an adverse verdict outside the guard. Its use of
`ceil(log_2 D)<=-N` is exactly equivalent to `D<=2^-N`.

## Evidence and trust boundary

`independent_check.py` uses only standard-library integers and
`fractions.Fraction`. It pins the source, independently rebuilds schedules,
and checks the algebraic reflection, repair, exceptional-mass, and assembly
interfaces. It does not formalize Gaussian integration, analyticity of
positive mixture level sets, regular-value approximation, the previously
accepted posterior-divergence identity, or the Procrustes theorem. No
numerical quadrature, solver, private dataset, or omitted certificate is used.

Reproduce with standard-library CPython 3.11 or later:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_MIDPOINT_POLARIZATION_REVIEW_PASS`. Expected
record SHA-256:
`6c365fa651cf0e3abd8ae4a38f116209549204233b268d61609afaa925e318cd`.
