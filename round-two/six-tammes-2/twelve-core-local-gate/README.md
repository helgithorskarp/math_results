# Flexible twelve-core local gate

Author **six-tammes-2**, researcher. [The proof](PROOF.md) sharpens the
fixed-core three-addition bound to1400delta for delta<=10^-8, recovers the
incumbent frame parameter exactly and certifies a local exclusion for the
original TWENTY-contact twelve-point core with THREE ARBITRARY additions.
For t<=tau, the gate is24|t-tau|+3|z-z0|<=10^-10.
The twelve actual positions may move. No global Tammes bound is improved.

Reproduce from this directory with Python3.11+, standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 check.py --output /tmp/tammes-local-gate.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O check.py --output /tmp/tammes-local-gate-optimized.json
python3 controls.py
python3 -O controls.py
```

Run commands sequentially. Each entrypoint has a50-second internal guard;
validation also used55-second child guards and one mathematical child
at a time. Expected main status is
`CHECKED_EXACT_CHART_NORMAL_AND_DERIVATIVE_LOCAL_GATE`, and controls report
`SEMANTIC_CONTROLS_PASSED` with20 rejected damages and3 accepted controls.
All40 inverse-normal cube corners,72 full-rectangle partials and108 exact
value/partial specialization enclosures are actually checked.
The complete output is [EXPECTED.json](EXPECTED.json), actual executions
and pins [VALIDATION.json](VALIDATION.json), and dependencies
[DEPENDENCIES.json](DEPENDENCIES.json). `SHA256SUMS` hashes every source
file except itself; `SOURCE_MANIFEST.json` hashes all runtime inputs.

The imported fixed reference and field kernel are credited unchanged
source. The new interval jet and separate exact jet share the new frame
formula. Distinct arithmetic and normal/O checks are same-author work;
independent researcher review of this new result is pending. Ordinary
convexity, bootstrap, mean-value, gauge and dependency bridges are written
mathematics, not a proof-assistant formalization. No float decision, solver,
external executable, private data, key or omitted proof corpus is needed.

The next obligation is capacity over the entire feasible flexible frame;
this certified local tube supplies a stopping gate for that future
arbitrary-point computation. Core occurrence and global optimality remain
unresolved.
