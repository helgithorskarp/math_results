# The sharp rank boundary for pointwise conditional beta certificates

For a fixed finite contraction in R3, every conditional beta kernel is
nonnegative at all orders and variances **if and only if its paired affine
rank is at most five**. Every rank-six configuration has failing kernels
at an interior lift time and arbitrarily large variances.

The [proof](PROOF.md) supplies a compact exact obstruction: a rational
36-by-36 joint moment matrix and an integer vector with quadratic value
**-1**. It then derives the existence of a negative conditional kernel,
retaining a distinguished pair of positive distance loss. The proof uses
the classical multivariate Bernstein theorem. It does not identify a
negative kernel's order, tuple or variance, or produce a negative beta.
Seven sites are the exact minimum support size for this conditional
failure. The seven-site control itself satisfies full majorisation.

R8's new seven-factor theorem remains compatible with this result.
The obstruction concerns extending pointwise conditional positivity to
**all** orders. The unrestricted majorisation problem remains open; a
proof must preserve more of the averaging or use another sign mechanism.
The earlier instantaneous-lift counterexample already ruled out the global
pointwise strategy. The new statement classifies its boundary for every
finite paired configuration. This is an author proof with exact evidence;
independent review is pending.

From this directory, using Python 3.11+ and its standard library:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Expected status: `EXACT_CONDITIONAL_JOINT_MOMENT_OBSTRUCTION`.
The [certificate](CERTIFICATE.json) contains the physical configuration,
the 21-term integer witness and the matrix hash. The checker reconstructs
all 330 Taylor coefficients through degree four, the entire matrix and
an independent polynomial substitution. Two effective-dimension controls
and three damaged-record rejections check the normalization and interface.
No imported solver, floating sign, numerical integration or omitted corpus
is used. Successful author checks are not independent mathematical review.

[SOURCES.md](SOURCES.md) distinguishes the prior reduction, the concurrent
seven-factor theorem, and the different endpoint-scatter obstruction.
