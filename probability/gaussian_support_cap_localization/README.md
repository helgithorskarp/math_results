# Support caps give uniform eventual Gaussian majorisation

Every bounded contraction in R3 with a **positive support mean-width gap**
has full Gaussian majorisation at every sufficiently large variance.
The law may be diffuse, and the map may preserve nonzero pair distances.
A quantitative cap-mass bound makes the variance cutoff explicit and
uniform over a whole family.

For a radius bound `R`, mean squared pair-loss floor `d>0`, support
half-mean-width gap at least `delta_0>a>0`, and source mass at least
`2^-k` in every exposed cap of depth `a`, set

```
N = max(1,ceil(R(k+1)/(delta_0-a))).
```

Then every density threshold is signed for every

```
s >= (2112 R^4/d) 2^(8N).
```

[PROOF.md](PROOF.md) joins the independently accepted universal spherical
comparison to a growing cap bound and the accepted all-threshold endpoint.
Its finite-cover version replaces the cap hypothesis with rational
reference sites, cloud radii, and aggregate cell-mass bounds. An exact
six-chart quadrature certifies the support width. Every strict-width
bounded contraction admits such a finite certificate at the level of
verified support/mass data. No martingale witness or covariance floor is
required. [HANDOFF.md](HANDOFF.md) states the consumer interface and limits.

**Status:** author proof; independent review of this contribution pending.
The unrestricted all-variance R3 problem remains open. No universal
strict-width claim for infinite supports, useful small cutoff, or new
Kneser--Poulsen volume theorem is asserted. The radius, loss, and cap-mass
hypotheses are quantitative data; boundedness alone supplies no uniform
schedule. The published control was already positive by a contracting
straight motion and is not offered as new geometric coverage.

Reproduce with CPython3.11, standard library only:

```sh
python3 -B certificate.py INPUT.json > /tmp/support-cap-certificate.json
cmp /tmp/support-cap-certificate.json CERTIFICATE.json
python3 -B verify.py --input INPUT.json --certificate CERTIFICATE.json
python3 -B verify.py > /tmp/support-cap-check.json
cmp /tmp/support-cap-check.json EXPECTED.json
python3 -B -O verify.py > /tmp/support-cap-check-opt.json
cmp /tmp/support-cap-check-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

Expected audit status: `SUPPORT_CAP_LOCALIZATION_PASS`. The supplied-record
mode imports no producer code and reconstructs the weighted loss using
marginal covariances and the integral through paired antipodal charts.
The test suite additionally compares coarse cells to direct rational
evaluation, exercises negative rounding, tests exact zero reserves and
invalid inputs, and checks scale/translation symmetry. The manuscript,
not finite testing, supplies the continuum proof. Dependencies are pinned
in [INPUTS.json](INPUTS.json), with attribution in [SOURCES.md](SOURCES.md).
Normal and optimized CPython3.11.2 audits took about21 and23 seconds on the
development host, with peak child-process RSS below22MiB. Canonical output
SHA256: `d13b9bf05bccbb2f3651f14f8bb6100da28ea554df311ed13b48a6a5aa78578a`.

The example [certificate](CERTIFICATE.json) has mesh256, 393216 cells,
`N=64`, and variance cutoff
`(38051054201746882593/3373851463450616) * 2^512`.
This large value is deliberately recorded without decimal approximation
or expansion. It signs all contractive clouds of radius`1/16384` around
the paired eight-site reference, with common-label relative prior error
at most`1/4096`. It does not verify the actual-cloud contraction premise.

No floating point, solver, external data, or large certificate is used.
Producer arithmetic is `O(n M^2)` with `O(n)` storage; rational bit lengths
also affect runtime. The dyadic grid error vanishes with the mesh, so
strictly positive finite width will eventually be certified.
