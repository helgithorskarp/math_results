# Tammes 15: exact exclusion of an eight-point core

Author: **six-tammes-2**, role: **researcher**.

On the closed cosine interval `[29/50,593/1000]`, the explicit eight-point
core in [PROOF.md](PROOF.md) permits at most six arbitrary additional
separated unit points. Hence no fifteen-point packing in this interval
contains its thirteen-contact pattern. No facial or pentagon/bridge
hypothesis is needed. Global numerical bounds remain unchanged, and
independent peer review and formalization are pending.

The production verifier is standard-library-only CPython >=3.11, tested
on 3.11.2. The separate native algebra audit and definition-level controls
also require SymPy 1.14.0. From this directory:

```sh
python3 -B check.py > replay.json
cmp replay.json EXPECTED.json
python3 -B -O check.py > replay-optimized.json
cmp replay-optimized.json EXPECTED.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B audit_sympy.py > replay-audit.json
cmp replay-audit.json AUDIT_EXPECTED.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B controls.py > replay-controls.json
cmp replay-controls.json CONTROLS_EXPECTED.json
sha256sum -c SHA256SUMS
```

Run commands sequentially with one CPU-intensive job and all native
threads set to one. The author's checks use the existing 1 CPU/2 GiB
scope. Any error, incomplete search or timeout leaves verification
unfinished and is not a nonexistence result.

`certificate.json` is a compact exact tree/pair/multiplier/deletion
certificate. Its discovery history is unnecessary for verification.
`check.py` verifies the complete cover, capacity, pair exclusions,
deletion transcript and complete no-seven-clique search. The expected
graph has 1210 vertices and 486009 edges, reducing to 230 vertices;
production searches 43133 states. `audit_sympy.py` independently rebuilds
the exact algebra, cover, rectangle bounds and graph, checks the same
deletions by sets, and uses a different 19995-state complete search.
Both algorithms are by the same author.

There is no solver, floating-point acceptance test, downloaded input,
private graph dependency or omitted large artifact. See PROOF.md for
the exact contact-pattern implication, chart completeness, trust
boundary, primary literature and correctly scoped predecessors.
