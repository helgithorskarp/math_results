# A degree barrier before Gaussian moment enumeration

The supplied Gaussian moment certificate cannot pass its first Bernstein
cell when K>=1 and N+2<=2/tau, even with exact moments. Combining that
necessary condition with the interface's supplied signed-tail cutoff forces
N+2>2 exp(288R^2/s).

For the classical sixteen-site simplex-flap pair at variance at most one,
both automatic moduli have K>1 and the minimum source radius is sqrt(8).
The required degree therefore exceeds **10^1000**. The bound persists under
every additional target homothety, including the known-positive point
target. It is a limitation of these particular certificate ingredients,
not a Gaussian counterexample or an impossibility theorem for other methods.

The [proof](PROOF.md) isolates the exact inputs that must change before a
moment producer is useful here. The [exact audit](verify.py) checks the
universal polynomial identity, all 120 geometric pairs, the optimal-radius
witness, boundary selection and a rational exponential lower bound.

**Status:** complete author argument; independent correctness review pending.
The unrestricted dimension-three question and the simplex-flap Gaussian
sign at arbitrary weights remain open. No new positive class is claimed.

Run from this directory with standard-library CPython 3.11 or later:

```sh
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

Expected status: `GAUSSIAN_CERTIFICATE_DEGREE_BARRIER_PASS`.
The output must match [EXPECTED.json](EXPECTED.json), with canonical record
SHA256 `44cfb6ef12ba10e090e95910dc44bb07f4a4f00fd4953830a8ba5f94ddfe9b77`.
CPython 3.11.2 and 3.12.14 passed. Each run takes less than one second.
No external dataset, solver or numerical library is used.
The audit corroborates the written reduction; it is not independent peer
review or an all-law integral calculation. [SOURCES.md](SOURCES.md) records
the exact interface and benchmark provenance.
