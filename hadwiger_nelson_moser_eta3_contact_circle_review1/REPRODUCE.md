# Reproduction notes

From this directory, run:

```sh
./reproduce.sh
```

The script creates a temporary directory, compiles the independent
alternate-basis metric twice, runs the complete checker twice, compares both
outputs to `EXPECTED.json`, and checks the source manifest. The first build is
optimized. The second enables undefined-behaviour sanitization and disables
Python assertions so correctness checks cannot accidentally depend on
`assert` statements.

The checker takes four explicit inputs from sibling directories:

- the target `certificate.json`, as untrusted positive-witness data;
- the target `expected.json`, for claimed census/hash comparisons;
- the prior review's `independent_audit.py`, pinned internally to SHA-256
  `b9a8dcb...28fd4`; and
- the newly compiled `geometry_check.cpp` shared object.

It imports no Python or native code from the reviewed eta-cubed package. No
network, SAT solver, floating-point distance calculation, or omitted generated
inventory is needed.
