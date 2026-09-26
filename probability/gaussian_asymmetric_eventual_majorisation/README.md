# A positive Gaussian endpoint on the asymmetric nine-atom frontier

Every density hinge has the desired sign for the team's asymmetric
nine-point square-cone example at Gaussian variance **s >= 13200**.
The conclusion holds uniformly for probability weights within L1-distance
**1/25000** of the displayed weights once **s >= 16896**.

This is a complete author proof with a validated numerical certificate;
independent review is pending. The same weight neighborhood is already known
to exclude the position-martingale and deterministic common-output R5-motion
routes. The present result uses a spherical log-MGF comparison instead.
The lower-variance question, unrestricted three-dimensional conjecture, and
any new Kneser--Poulsen consequence remain unresolved.

In the listed order, the source and target centers and central weights are

```text
A = ((1,0,1), (0,1,1), (-1,0,1), (0,-1,1))
B = ((1,1,1), (-1,1,1), (-1,-1,1), (1,-1,1))
X = (0,A,-B), Y = (0,A,B)
p = (8,12,7,15,44,21,11,23,43)/184.
```

[PROOF.md](PROOF.md) establishes the continuum bounds, including all
thresholds and the infinite spherical-parameter tail.
[EXPECTED.json](EXPECTED.json) contains 26 rational lower bounds.
[verify.py](verify.py) validates them with outward Arb balls, checks the
25 connecting parameter intervals exactly, and verifies the weight and
variance constants. [SOURCES.md](SOURCES.md) records dependencies and scope.

## Reproduce

From this directory, using CPython 3.11 or later:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python verify.py
.venv/bin/python -O verify.py
.venv/bin/python verify.py --precision 192 --equal-z-grid
sha256sum -c SHA256SUMS
```

Each checker run begins with

```text
ASYMMETRIC_EVENTUAL_MAJORISATION_CERTIFICATE_PASS
certificate_sha256=fb297e46742dfd051089d0198e0d992f658523fd47afc025bee61ee837cb2897
```

The default proof uses 128-bit balls on 1024 sphere cells. The supplementary
run uses 192-bit balls and a different 4096-cell equal-height partition.
Both certify the same rational bounds, with exact interval minimum
1290469/128000000 > 1/100. Validation used CPython 3.11.2 and
python-flint 0.8.0. Runtime is about one second for the default check and a
few seconds for the alternative geometry. An intentionally false lower
bound is rejected, including when Python optimization disables assertions.

The trust boundary is Arb's enclosure arithmetic, Python exact rational
arithmetic, the written analytic error estimates, and the independently
reviewed eventual-endpoint theorem. No finite-degree moment inference,
unvalidated quadrature, or generic entropy-stability bridge is used.
