# A uniform all-threshold certificate for damped Gaussian contractions

**Author proof; independent acceptance pending.** This closes every
threshold for an explicit parameter family at sufficiently large variance.
It does not settle unrestricted dimension-three majorisation.

Let the centered source have radius at most R and covariance at least
`kappa I_3`, with kappa>0. For **every** 1-Lipschitz F and every

```
0 <= c <= kappa/(4 R^2),       s >= 2816 R^4/kappa,
```

`law(X)*gamma_s` is majorised by `law(c F(X))*gamma_s`. The sign holds at
all density thresholds, for any bounded diffuse law or atomic prior.
There is no bound on the number of atoms or minimum positive weight.
The variance bound is essential to the stated conclusion; no new
Kneser--Poulsen consequence is claimed.

The more general [theorem](PROOF.md) takes a coupling with
`E[U|W]=a W`, a>1, between the centered source and target laws. If
`V=E|X-E X|^2>0`, it gives every threshold for
`s >= 4224 a R^4/((a-1)V)`. The explicit product density
`1+a x^T Cov(X)^(-1)y` supplies such a coupling whenever it is nonnegative
on the product of the endpoint supports. This is a law-level coupling;
the dilated prescribed map aT need not contract.

The accepted spherical-gap endpoint supplies the tail/window join. The
new work gives its uniform positive gap and an exact compact witness,
making a known qualitative finite martingale route effective on this
family. Jensen, convex order and that existing endpoint are credited.
No priority claim or new positive classification of the test fixtures
is made. See [SOURCES.md](SOURCES.md) and [HANDOFF.md](HANDOFF.md).

## Reproduce

Use standard-library CPython3.11 or later, from the repository root:

```sh
python3 -B probability/gaussian_dilated_martingale_certificate/verify.py
python3 -B -O probability/gaussian_dilated_martingale_certificate/verify.py
python3 -B probability/gaussian_dilated_martingale_certificate/certificate.py probability/gaussian_dilated_martingale_certificate/FAMILY_INPUT.json
```

Both checks reproduce [EXPECTED.json](EXPECTED.json) and print
`DILATED_MARTINGALE_UNIFORM_FAMILY_PASS` with a canonical record hash.
The last command reproduces [FAMILY_CERTIFICATE.json](FAMILY_CERTIFICATE.json).
From this directory, check that record independently with

```sh
python3 -B verify.py --input FAMILY_INPUT.json --certificate FAMILY_CERTIFICATE.json
sha256sum -c SHA256SUMS
```

Input fields are `sources`, `targets`, `weights`, `variance`, and `dilation`
(default2). Coordinates and numerical parameters are integers or rational
strings. Zero masses are removed; every active pair contraction is checked.
The factored witness stores nine rationals, and verification uses O(n^2)
exact operations and O(n) storage. Input bit size still affects arithmetic cost.

The supplied-record checker imports no producer code. It uses ordered-pair
moments, explicitly expands all coupling masses, checks both marginals and
the dilated conditional means, and verifies the variance cutoff. The
universal analytic argument remains written mathematics.

`SIGNED_ALL_THRESHOLDS` includes the supplied variance.
`UNRESOLVED_AT_REQUESTED_VARIANCE` certifies only the displayed future
variance interval. `UNRESOLVED` makes no sign assertion. `ISOMETRIC_ZERO`
is the exact equality case. A negative coupling entry is a failed
sufficient test, not a Gaussian counterexample.

Controls include the uniform parameter budgets, full paired-rank-six
inputs, zero coupling masses, a mass of order2^-100, an original map whose
dilation expands a pair, rotation/scaling, zero loss and damaged records.
They validate the universal theorem's certificate, not a sample-grid proof.
