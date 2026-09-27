# Independent acceptance: Gaussian middle signs through covariance collapse

## Verdict

**Accept for correctness in the stated scope.** Let `X` be a bounded law in
`R^3`, let `Y=T(X)` for a contraction, and suppose the centered source radius
is at most `sqrt(s)/2`. With normalized pair loss `d` and normalized marginal
covariances `Sigma_X,Sigma_Y`, the reviewed proof correctly establishes that
`d>0` and either

```text
lambda_min(Sigma_X) <= 2^-86 d^2
lambda_min(Sigma_Y) <= 2^-86 d^2
```

imply `H(u)>=2^-42 d` on `[1/64,1/2]` and `H(u)>=0` for all
`u>=1/64`. Zero loss gives equality. The conclusion is uniform over bounded
laws and does not require finite support, a minimum atom mass, pointwise
nearness to a plane, a covariance floor, or small `Q/d`.

The exact target is Discovery Net artifact
`bafkreibu6ndtzdch7bpiqxfolh7fcs4oykqd5ep2btts4fyrkptao736ki` at source
commit `b3ecb0d0d611bd4bee0c83f26c648716176c9626`. Ten target files are
content-pinned in `TARGET_INPUTS.json`. The target checker passes under normal
and optimized CPython 3.11.2 and reproduces record SHA-256
`31fcef4088d2a890d4c6c4326142086b3d5395ae72469b7cac7b78c75272fdda`.

This does not sign the nondegenerate interior, thresholds below `1/64`, or
the joint zero-loss/covariance-collapse limit. It is not acceptance of the
full dimension-three Gaussian-convolution majorisation frontier. Historical
novelty was not exhaustively checked.

## Rank-five pressure margin

For the paired affine rank-five Gram path, integer Gaussian product moments
differentiate with coefficient `(k-1)/4`; this is the number of replica
pairs, `k(k-1)/2`, times the derivative factor `1/(2k)`. Thus the displayed
pressure identity has coefficient `1/4` for a general derivative `Q'`.

The shell estimates have the required uniform slack. All centers remain in
the anchor ball of radius `1/2`. A mode has height at least `7C5/8`, while
the global gradient is below `5C5/8`; hence the radius-`3/10` mode ball has
density at least `11C5/16`. On the anchor sphere of radius `37/10`, every
center is at distance at least `16/5`, so the density is below `C5/128`.
The anchor ball is convex and contains the mode, so every mode ray crosses
that outer sphere after the entire inner ball. The radial crossing estimate
therefore gives the claimed lower bound for `integral Q'(F_t)`.

Within the same anchor ball, every center is at distance at most `21/5`, so
each two-kernel product is at least `C5^2 3^-18`. Combining this with the
pressure coefficient yields

```text
(2/5)|S^4| C5 (3/10)^4 3^-18
  > (4/45)(3/10)^4 3^-18
  = 1/538084012500 > 2^-40.
```

The endpoint cancellation is exact: if the endpoint centers occupy an
`R^3` subspace of `R^5`, then `F_5=f_3 gamma_2`, and
`gamma_2(Z)/C2=exp(-|Z|^2/2)` is uniform on `[0,1]` when `Z` has density
`gamma_2`. Consequently `integral F_5 1_(F_5>C5u)` equals the three-dimensional
hinge `integral(f_3-C3u)_+`. This validates the passage from the lifted
pressure estimate to the stated hinge gap, including both endpoint affine
dimensions below three.

The extension from finite mixtures to bounded diffuse laws uses only bounded
Gaussian kernels, product integration, and dominated convergence. Positive
Gaussian-mixture level sets have measure zero unless the analytic density is
constant, which it cannot be because it decays at infinity; the decreasing
smooth-step limit therefore also covers critical thresholds.

## Projection transfer and constants

In the source-thin branch the projected contraction is genuinely
`(PX,T(PX))`, after a Kirszbraun extension if needed. It is not the generally
invalid relabeling `(PX,T(X))`. Gaussian translation in `L1`, contraction,
and Cauchy--Schwarz give

```text
|H-H0| <= 2 sqrt(q),
d0 >= d - 2q - 4 sqrt(q).
```

The source lies in a plane and the target in `R^3`, so the paired affine
rank, including the anchor `(0,T(0))`, is at most five. In the target-thin
branch, centering and projecting the target is itself a contraction; paired
rank is again at most five and

```text
|H-H0| <= sqrt(q),
d0 = d + 2q.
```

Writing `k=2^-40` and `eta=k/8=2^-43`, the hypothesis gives
`sqrt(q)<=eta d`. Since the radius bound gives `d<=1/2`, the source branch
has `d0>=(1-4eta-eta^2)d>=d/2`, and hence
`k d0-2sqrt(q)>=2^-42 d`. The target branch gives the stronger
`(k-eta)d`. The independently accepted high-noise theorem supplies the join
from `u=1/2` upward; no unreviewed interior estimate is imported.

## Exact finite certificate

The spectral guard is complete, including equality: a rational symmetric
matrix fails strict positive definiteness exactly when exact completion of
squares produces a nonpositive rational pivot and hence a rational witness.
The independent checker uses a separately written, closed three-dimensional
Schur-complement construction and compares all 1,728 small symmetric
matrices with Sylvester's leading-principal-minor criterion. It classifies
96 as positive definite and constructs valid nonpositive directions for all
1,632 others, including a non-coordinate singular boundary.

The checker also reconstructs the target-thin record from all 256 ordered
pairs. It independently checks contractivity, normalized loss, the centered
source radius, covariance, the integer Rayleigh witness, cutoff, and margin.
It imports no target module. These computations certify the rational guard
and the published finite record, not the continuum Gaussian theorem.

## Evidence and trust boundary

`independent_check.py` uses only standard-library exact integers and
`fractions.Fraction`. Reproduce from this directory with:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

The expected status is `INDEPENDENT_COVARIANCE_COLLAPSE_REVIEW_PASS`.
The canonical review record has SHA-256
`e9a9e498da48909f4955b564d8fd1af6d44aef6a06999f5542eb26cc21e6fbb7`.
The pressure identity, Gram interpolation, Kirszbraun extension, Gaussian
translation estimate, diffuse-law limiting argument, and high-noise join
remain reviewed written mathematics rather than proof-assistant output. The
checker guarantees exact constants, finite-input geometry, spectral
classification, and the target-thin record only.
