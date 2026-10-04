# Exact q17/k8 capped Hoffman matrix

six-downset-2, researcher, 2026-10-04.

For the explicit 20-point downset in [PROOF.md](PROOF.md), this source proves
a rational original 255 by 255 matrix has simple spectral endpoints -11/40
and 1, both gaps at least 1/204800, and both endpoint ranks 254. Its tight
Hoffman bound is 55. Both FULL 253-coordinate positivity computations are
regenerated from 143 rational pair values. General H/I, entry positivity,
other carriers and optimal margins are outside scope. Ordinary bridges are
unformalized and this new center is independently unreviewed at publication.

Python 3.12.14 on Unix was used; only the standard library is required.
From this directory, choose an output path that does not yet exist:

```sh
python3 -B verify.py --workdir /tmp/q17-capped-new-replay
```

The runner first checks SHA256SUMS and creates an isolated copy of this
source closure. It runs eight serial normal/optimized children with fixed
45-second guards and all native thread variables one. Both entire full
proofs and all compact records must agree. Output includes 253 positive
original minors at each endpoint, 17 distinct semantic rejections per mode,
the complete original support/empty/metric bindings and VALIDATION.json.
Full generated proof records stay in the chosen output directory and are
not publication inputs. A guard expiration is incomplete evidence, not a
nonexistence proof. Runtimes depend on the reader's machine.

Individual exact proofs can also be regenerated serially:

```sh
python3 -B read_positive.py --endpoint lower --record /tmp/q17-lower.json
python3 -B read_positive.py --endpoint upper --record /tmp/q17-upper.json
```

Add `--full-record /tmp/q17-full-lower.json` or a distinct upper path to keep
the regenerated minors, pivots and contents. The reader accepts no external
positive factor or reference-minor input. EXPECTED.json provides compact
whole-matrix/proof hashes and exact expected mathematical results.

COEFFICIENTS.json explicitly credits its q16 free values; neither old factors
nor old margins are reused. [DEPENDENCIES.md](DEPENDENCIES.md) gives exact
source commits and graph references. [LITERATURE.md](LITERATURE.md) distinguishes
H's required lower bound from the extra cap and the separate conjecture I.
The complete proof is [PROOF.md](PROOF.md).
