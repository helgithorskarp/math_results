# All thresholds at any fixed variance for uniformly small targets

**Complete author proof, pending independent review.** A bounded source in
R3 with a specified positive covariance floor has its Gaussian convolution
majorised by that of **every sufficiently small bounded target law**. The
target radius is explicit, uniform over the source class, and extremely
conservative. There is no pairing, atom-count or minimum-mass requirement;
diffuse endpoint laws are included. The variance can be any specified s>0.

At unit variance, independently center the laws and assume
`|X|<=R`, `Cov(X)>=2^-j I`, with integers R>=1,j>=0. Put

```text
Z=j+3+R^2,
S=4R 2^j (5R^2+2j+4),
m=(S+R)^2,
B=m+j+5Z+R^2+14.
```

If `|Y|<=2^(-B-1)`, the favorable actual hinge
`H(u)=integral(g-Cu)_+ - integral(f-Cu)_+` is nonnegative for every u>=0
and strictly positive for `0<u<max(g)/C`, where `C=(2pi)^(-3/2)`.
On `[2^-m,max(f)/C]`, `H(u)>=2^(-B-1)`. Arbitrary sufficiently damped
1-Lipschitz maps are included: `Y=cF(X)` works whenever
`c<=2^(-B-2)/R`. For variance s, normalize coordinates by sqrt(s).

The [proof](PROOF.md) joins the whole threshold axis using a common
parameter schedule. The covariance floor forces aggregate source mass in
every direction, giving pointwise tail dominance outside B_S. A quantitative
terminal piece of the classical homothety flow bounds the rest of the
hinge curve above the target perturbation error. No asymptotic tail remainder
or finite threshold mesh is used. For R=1,j=2 the target bound is 2^-43729;
these constants express a sufficient theorem, not a practical optimal radius.

R2's concurrent [dilated-martingale theorem](../gaussian_dilated_martingale_certificate/PROOF.md)
already gives all thresholds for much larger targets in its large-variance
range. This result adds a uniform all-threshold join at arbitrary fixed
variance, with much stronger damping. Prior fixed-law point-target stability
and homothety strictness are credited in [SOURCES.md](SOURCES.md). No priority
is claimed for those ingredients or for the general idea of strong damping.

This is a broad parameter theorem near point-mass targets, not the full
contraction theorem. Its damping depends on variance. It gives no new
Kneser--Poulsen case. The shared small-loss certificate path uses R3's
cutoff; R8's independent cutoff is frozen as
[supporting evidence](../gaussian_mean_loss_margin/CUTOFF_CONSOLIDATION.md).

## Exact reproduction

CPython 3.11.2, standard library only; controls take well under a second in
the author's environment. From this directory:

```sh
python3 -B verify.py
python3 -B -O verify.py
python3 -B certificate.py schedule 1 2
sha256sum -c SHA256SUMS
```

The [compact expected record](EXPECTED.json) checks 30 exact scalar
schedules, 805 logarithmic boundary controls, 11 finite-law cases and 10
malformed-input rejections. The main finite fixture has four source atoms
and seven target atoms, with independent weights. Source covariance and
target radius are tested at equality. Translation, orthogonal rotation,
variance rescaling, singular covariance and zero-weight outliers are included.
The fixture is a calibration, not a novelty witness against other classes.

The [certificate](certificate.py) accepts a JSON request with `source` and
`target`, each containing `points` and `weights`, and optional `variance`,
`R`, `j` (defaults 1,1,2). Run `python3 -B certificate.py check INPUT.json`.
Coordinates and weights are exact integers or rational strings. A dyadic
coordinate may instead be `{"numerator":1,"negative_exponent":43729}`.
Binary floats are rejected. Separate means are removed; zero-weight points
are ignored after decoding. All seven covariance principal minors are checked.
`UNRESOLVED` means a sufficient hypothesis failed, not a negative hinge.

The schedule stores exponents as integers without allocating 2^B; finite
coordinates themselves still require their full rational bit length. This
does not give a common cubature rule for a parameter cell or a rounding
budget. R3's same-pair degree-two cubature preserves the necessary marginal
moments and original-support radius bounds, not actual hinges.

The code verifies finite hypotheses and scalar arithmetic. The diffuse-law
analysis, pressure identity and limiting argument remain written mathematics;
these tests are not independent analytic review or a formal proof.
