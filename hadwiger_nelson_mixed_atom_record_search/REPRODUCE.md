# Reproduce

Use a complete checkout of this repository. Python 3.11.2 and g++ 12.2.0 were
used. The complete search additionally used `python-sat==1.8.dev24` with
CaDiCaL195. No SAT dependency is required for the two fixture replays.
All generated data belongs outside the repository.

From this directory, choose a fresh output directory:

```sh
export HN_MIXED_RUN_DIR=/tmp/hn-mixed-replay
mkdir -p "$HN_MIXED_RUN_DIR"
g++ -O1 -fsanitize=undefined -fno-sanitize-recover=undefined -shared -fPIC geometry.cpp -o "$HN_MIXED_RUN_DIR/geometry.so"
python3 -O shell_search.py fixture main_0_44 0
python3 -O shell_search.py fixture field_5_GMM_0 0
```

Expected final lines report SAT on 847 vertices/5,024 edges and 518
vertices/2,567 edges. Here SAT means the supplied four-colouring passed exact
checking; the fixture path never invokes a solver. Each replay reconstructs
every circle intersection and the entire physical graph, checks both metrics,
and compares point/edge hashes. The optional final `0` is an unused fixture
argument retained to share the search command interface. About 2--4 minutes
for both cases is a representative runtime; hardware affects this.

To rerun the full finite search in a separate directory with the stated PySAT
version installed:

```sh
export HN_MIXED_RUN_DIR=/tmp/hn-mixed-search
python3 search.py
```

The driver first builds the exact E-phase inventory and the 106 coefficient
sources. It then uses at most four solver processes for the main and fixed-field
searches. A final structural census must match EXPECTED.json. Solver colour
words and statistics need not be identical on other solver versions.
The expected result is 99,080 retained quadratic cases and 6,738 fixed-field
phase choices, with zero UNSAT and zero UNKNOWN.

The raw outputs, process logs and generated graphs remain in the selected
output directory. Do not commit them. Use a new directory for independent
replays: the batch can resume existing results, and its STOP file deliberately
prevents continuing blindly after an UNSAT candidate. Candidate files are
preserved, but a solver's UNSAT result alone is not a record certificate.

`geometry.cpp` uses guarded integer arithmetic in `__int128`; it rejects
coordinates outside its range instead of approximating them. Coefficient,
radicand and denominator bounds are at most 10^9. Even the larger real-metric
intermediates stay below 10^33, below 2^127. The vertex bound affects allocation,
not these arithmetic bounds. The two published fixtures fit the guards.

```sh
sha256sum -c SHA256SUMS
```
