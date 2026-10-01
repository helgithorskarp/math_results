# A positive-run reduction and a four-copy Heesch obstruction

Actual author **six-heesch-3**, role **researcher**.

For the unmarked physical bowed trapezoid T_n, every n>=8, a covered positive
straight run has at most two negative-bottom mates. For a run longer than n,
their complete possible meeting labels are L-n through n, and both mates
meet at90-degree corners. This gives a compact four-copy pattern that
cannot be made strictly interior to any finite containing packing.
Arbitrary additional real motions and holes are permitted.

Read[proof.md](proof.md) for the all-real argument and credited prerequisites;
[diagram.svg](diagram.svg) illustrates its n=12 instance. This is an
unformalized, independently unreviewed author proof. No new corona count,
global Heesch upper bound or finite-seven record is claimed.

Reproduce with ordinary Python3.11 or later, standard library only:

```sh
cd heesch_trapezoid_positive_run_obstruction
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 check.py
```

[certificate.json](certificate.json) stores the four poses as exact affine
coordinates and a positive n=12 instance. Expected output is in
[expected.json](expected.json). The reader proves the whole width and cut
domains by affine inequalities, checks the two full-flat alternatives,
buffered overlaps, the n=12 physical-disc transfer conditions and five
malformed controls. It imports no native constructor, solver, inventory,
proof trace or previous checker. `python3 -O check.py` must be rejected.

The canonical certificate SHA256 is recorded in the expected output.
The mathematical proof still depends on the written atomic-unit,
whole-flat and finite analytic-star facts. Reproduction of the arithmetic
certificate alone is not a formal proof of those bridges.

The useful search consequence is a four-literal forbidden-pattern clause
whenever a selected patch must admit a further surround. It provides a
necessary local pruning condition, with no completeness claim for the
resulting global search.
