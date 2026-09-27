# Covariance-boundary signs at arbitrary radius and threshold

The [author proof](PROOF.md) gives an explicit uniform neighborhood of the
covariance-degenerate boundary of either marginal on every bounded positive-loss and
positive-threshold slab of the dimension-three Gaussian frontier.
Independent review is pending; full majorisation remains open.

At unit variance, take integer radius bound `R>=1`, mean pair loss
`D>=2^-k`, and thresholds `u>=2^-m`, with `k>=0,m>=1`. Set

```
q=ceil(sqrt(2(m+1))),
B=31+47R^2+2(2R+q)^2+5k.
```

If either marginal's variance in any unit direction is at most `2^(-2B-4)`,
then **all these hinges are nonnegative**. Through the actual source peak,
their favorable gap is at least `2^(-B-1)`. The law may be diffuse or have
arbitrarily small masses. There is no lower covariance or minimum-mass condition.

Equivalently, any adverse input on this slab has the explicit covariance
floors `Cov(X)>2^(-2B-4)I` and `Cov(Y)>2^(-2B-4)I`. This removes an entire boundary of
each positive-loss compact search. It does not sign the remaining interior,
the joint zero-loss/covariance corner, or arbitrarily small thresholds.

R2's concurrent [covariance guard](../gaussian_covariance_collapse_guard/README.md)
already supplies plane projection and the sharper cutoff `2^-86 D^2` at
radius at most `1/2` and threshold floor `1/64`. Use that bound where it
applies. The present estimate removes those radius/threshold restrictions
with a weaker covariance cutoff; it does not imply or improve R2's bound.

The proof uses the existing R5 motion margin for a projected reference
and bounds Gaussian hinge and peak errors. A retained target-peak
gap makes the comparison uniform through every possibly adverse upper
threshold. The geometric comparison and quantitative motion margin are
credited in [SOURCES.md](SOURCES.md); they are not new claims here.

From the repository root, using standard-library CPython 3.11 or later:

```sh
python3 -B probability/gaussian_covariance_boundary/certificate.py --radius 1 --threshold-bits 6 --loss-floor-bits 1
python3 -B probability/gaussian_covariance_boundary/verify.py
python3 -B -O probability/gaussian_covariance_boundary/verify.py
```

The first command returns covariance exponent `314` and hinge-margin
exponent `156`, valid when `D>=1/2` and `u>=1/64`. These conservative
constants are not optimized. The checker prints
`COVARIANCE_BOUNDARY_EXACT_CONTROLS_PASS` and reproduces
[EXPECTED.json](EXPECTED.json), SHA-256
`aa538a5a2eb95362e2a8c524945d8d926e2befcadb03d3a7e49a87d91219a916`.

Append `--input file.json` to the first command for exact finite data.
Fields are `sources`, `targets`, `weights`, `direction`, optional
positive `variance`, and optional `side` (`source` by default or `target`).
Numerical entries must be rational strings or integers.
The direction can have any nonzero norm. The checker centers the source,
checks its normalized radius and all active pair contractions, and tests
the exact normalized loss and the selected marginal's directional covariance. Failed sufficient
guards return `UNRESOLVED`. Planar and zero-loss branches are separately
credited known full comparisons. The implementation computes no eigenvector,
extension map, Gaussian integral, or large dyadic denominator.

The exact controls include two seven-label configurations of paired affine
rank six, both projection branches, loss/variance normalization, equality
at the sufficient cutoffs, expanded budgets and rejected inputs. The target
control uses radius `3` and threshold floor `2^-19`. They support the algebra and code;
they are not independent verification of the continuum proof or a new
Kneser--Poulsen case. No large artifact or external dataset is required.
