# An effective Gaussian mean-loss margin

An author proof gives an explicit cutoff at every fixed centered source
radius, positive covariance floor, and positive lower threshold. It makes
R8's qualitative zero-loss margin effective using a Gaussian comparison
on each interval component of a source top set. Independent review of
the new argument is pending; full three-dimensional majorisation is open.

In a concrete normalization, centered radius<=sqrt(s)/2,
Cov(X)/s>=2^-15 I, and mean normalized pair loss d<=2^-360 imply
H(u)>=2^-40 d on all [1/64,1/2] and H(u)>=0 for u>=1/64.
There is no second-loss-moment restriction, minimum atom mass, atom-count
bound, or finite-support requirement. No sign below 1/64 is claimed.

- [Proof and explicit seven-part cutoff](PROOF.md)
- [Consumer contract and 19-pair guard reduction](HANDOFF.md)
- [Exact finite guard and all-radius schedule](certificate.py)
- [Finite controls](verify.py) and [expected record](EXPECTED.json)
- [Attribution and dependencies](SOURCES.md)

Run from this directory, with standard-library CPython 3.11 or later:

```sh
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
```

Both Python runs must print `EFFECTIVE_MEAN_LOSS_PASS` and match the fixed
record exactly. Ten written inputs are pinned in INPUTS.json. There is
no external package, numerical integration, solver, private data, or
omitted large certificate. The analytic proof is not formalized; author
checks are not an independent review. The finite controls take about one
second and under 20 MiB on CPython 3.11.2.

The numeric cutoff is deliberately conservative. It removes the zero-loss
boundary effectively, but is not a claim that the remaining cover is
computationally feasible. The method does not settle covariance collapse,
arbitrarily low thresholds, or general positive loss outside the cutoff.
