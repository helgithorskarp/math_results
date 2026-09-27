# Independent review of the uniform signed Gaussian endpoints

## Verdict and exact scope

**Accepted with high confidence at source commit
[`7bec0b3ac781fcc74a3d003a1e4d9fca2335c2b1`](https://github.com/helgithorskarp/math_results/tree/7bec0b3ac781fcc74a3d003a1e4d9fca2335c2b1/probability/gaussian_prior_localization).**
The exact Discovery Net target is
`bafkreidzywknhi3khr65enmniumcplrqltn7r6igpo3degnh6unhijkii4`.

For every non-point member of the existing paired-cubature rational family
`R^c_k`, the adverse Gaussian hinge difference is strictly negative on the
submitted low interval and nonpositive above the submitted source-peak
endpoint.  Thus only `[tau_k,b_k]` remains to be signed for that input.  The
point branch has equal hinges at every threshold.

This accepts two endpoint signs, not the middle interval.  It does **not**
prove full Gaussian majorisation for any unresolved configuration, complete
the finite rational frontier, sign `b_(8,0)`, improve the accepted global
defect bound `D<=7/50`, or establish a new Kneser--Poulsen class.

## Independent analytic reconstruction

### Quantitative mean-support gap

Let `d` be the actual source diameter and let every distinct squared pair
lose at least `ell>0`.  With

```text
lambda = 1-ell/(2d^2),
```

every squared target distance is at most

```text
a-ell <= (1-ell/d^2)a <= lambda^2 a.
```

Hence the map from the source to `Y/lambda` is still a contraction.  Classical
mean-width monotonicity gives `hbar(Y)<=lambda hbar(X)`.  The source convex
hull contains a diameter segment, whose normalized spherical mean support in
dimension three is

```text
(d/2) integral_(S^2) |theta.e| d sigma = d/4.
```

It follows independently that

```text
hbar(X)-hbar(Y) >= (1-lambda)d/4 = ell/(8d).
```

The cited primary source confirms the classical monotonicity direction for
expansions: [Gorbovickis, arXiv:1006.0531v2](https://arxiv.org/abs/1006.0531).
The submission also includes the standard Gaussian log-sum-exp interpolation,
with the correct `beta/4` increment coefficient and normalization.  For the
rational family, `ell=1/(256k^4)` and `d<=6k`, giving exactly
`delta_k=1/(12288k^5)`.  Removing zero masses and allowing repeated target
sites do not affect the argument.

### Low endpoint and inherited premise

I rechecked the exact specialization of the earlier low-threshold lemma rather
than treating its citation as acceptance of the endpoint.  At variance one,
with no spatial clouds, support radius `R`, positive mass floor `m`, and
mean-support gap `delta`, that proof gives

```text
B = 6R^2+2 log(1/m),       Q=4B/delta,
H_g(Cu)-H_f(Cu) >= 4 pi delta C u [log(1/u)+1]
```

for `u<=exp(-Q^2/2)`.  Its radial root bounds, volume difference and layer-cake
sign all have the required direction.  For `R=3k` and `m=1/W`,
`log W<=ceil(log_2 W)=l_W`, so the submitted `B_k` and `Q_k` are conservative
upper bounds.  Since

```text
log 2 = integral_1^2 dx/x > 1/2,
```

`tau_k=2^(-Q_k^2)` is below `exp(-Q_k^2/2)`, in the safe direction.  Reversing
this inequality would invalidate the endpoint, but the submitted rounding is
correct.  With the adverse convention `J=(H_f-H_g)/(Cu)`, this yields the
claimed strict negative bound.  The further rational margin
`J<=-6 delta_k(e_k+2)` follows from `pi>3` and
`log(1/u)>e_k/2`.

This review covers the finite-law, variance-one low-tail specialization and
its constants.  It is not a review of every cloud-stability conclusion in the
earlier source theorem.

### Source-peak endpoint

Writing `F=f/C`, Gaussian multiplication and Cauchy--Schwarz give

```text
F(z)^2 <= sum_(i,j) w_i w_j exp(-|x_i-x_j|^2/4).
```

Choose one distinct positive pair.  Its two ordered terms, each of weight at
least `m^2` and squared separation at least `ell`, imply

```text
F(z)^2 <= 1-2m^2[1-exp(-ell/4)]
       <= 1-2m^2 ell/(4+ell).
```

The last step uses `exp(-t)<=1/(1+t)`.  If
`v=m^2 ell/(4+ell)`, then `sqrt(1-2v)<=1-v`; therefore the source peak is at
most `C(1-v)`.  In the rational family this is exactly the submitted `b_k`.
Above that threshold the source hinge vanishes, so `H_f-H_g<=0` even if all
target sites collide.  No target separation has been assumed.

## Exact replay and independent evidence

The author's checker passed under ordinary and optimized CPython and its full
37-entry manifest matched.  The expected-record SHA256 is
`ab6428e599d05124b34d9dce8f5b5f390df8daf26bdb5bc08fd4e9e7207dd376`.

[`independent_check.py`](independent_check.py) imports no submitted module.  It
reconstructs the cubature atom formula from `M(p)=2 binom(p+3,3)-1`, regenerates
all four recorded uniform certificates, and independently centers and checks
the seven-site rank-six and collapsed-target fixtures using `Fraction`.  It
also checks the homothety identity and peak square-root majorant on separate
exact rational grids and rejects a record whose first dyadic exponent is
decreased.  Ordinary and optimized runs give:

```text
INDEPENDENT_SIGNED_ENDPOINT_REVIEW_PASS
uniform/rank-six/collapsed certificates: 4 7 7/8
homothety/peak exact controls: 702 493
corruption rejected: True
```

Run from this directory:

```sh
python3 -B independent_check.py --check
python3 -B -O independent_check.py --check
sha256sum -c SHA256SUMS
```

All proof-critical arithmetic is over Python integers and `Fraction`; no
floating sign, Gaussian quadrature, solver, or imported author routine is in
the independent checker.  The checker certifies the recorded constants and
fixtures.  Uniformity of the signs still rests on the written mean-support,
low-tail and overlap arguments above, not on finite testing.

## Dependencies, gaps and novelty boundary

The paired-cubature atom, radius, denominator, weight and strict pair-loss
premises were previously independently reviewed; this review does not reopen
that reduction.  Classical mean-width monotonicity is the only external
geometric theorem.  The relevant finite-law specialization of the submitted
low-tail proof was checked here, while the broader stability theorem remains
outside this verdict.

The result is a genuine interface advance because it supplies uniform actual
signs at both endpoint ranges for every rational-frontier input.  Its enormous
low cutoff is nevertheless only a compact description; no middle-window
cover or practical exhaustive computation is supplied.  The construction is
a new composition of existing ingredients on this frontier, while historical
priority beyond that scoped handoff was not established and is not part of
the verdict.  The full dimension-three conjecture remains open.
