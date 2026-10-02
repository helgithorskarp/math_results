# H7/F617 selected adjacency at phase weights10 and34

six-vdw-2, researcher. The [proof](PROOF.md) establishes that a phase value
occurring exactly ten times has adjacent occurrences. Both values are
covered. This excludes only the no-adjacency subclass, not either endpoint
or all H7 colorings. It does not improve the unrestricted W(2,7) bound.

Use a checkout of `helgithorskarp/math_results` containing this directory
and the sibling sources listed in `SOURCE_PINS.json`. Python3.11.2,
python-sat1.8.dev24, six1.17.0, CaDiCaL195 and a C compiler were used.
Keep all generated files under a scratch/build directory outside tracked
source. Set solver/BLAS/OpenMP thread counts to one.

From this directory, with `PYTHON` naming the ACTUAL solver virtual-
environment interpreter (do not resolve its symlink to the system Python):

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
mkdir -p build
curl -fL https://raw.githubusercontent.com/marijnheule/drat-trim/2e3b2dc0ecf938addbd779d42877b6ed69d9a985/drat-trim.c -o build/drat-trim.c
sha256sum build/drat-trim.c
cc -O2 build/drat-trim.c -o build/drat-trim
"$PYTHON" reproduce.py --work build/fresh --converter build/drat-trim
"$PYTHON" guards.py --checked-work build/fresh --work build/guards
```

Expected converter-source SHA256:
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.
Final status is `EXACT_H7_PHASE10_SELECTED_ADJACENCY_LEMMA`:14 complete
cases,141044 strict additions and2260110 checked hints per Python mode.
`EXPECTED.csv` records every model/proof hash and count. Guards reject16
damages and accept two positive tiny RUP controls.

Each model is generated and independently audited normally and under
Python `-O` before any native proposal. Native guards are50000 conflicts/
30 seconds; converter25 seconds internal/30 external; strict replay30
seconds per mode; definition audits55 seconds. Stop at first incomplete
case. UNKNOWN, timeout, missing proof or incomplete coverage establishes
no exclusion. Optional `--certificate-cache PATH` expects `PATH/head/`
with byte-matching CNF/LRAT candidates; every candidate is strictly replayed.
`--resume` replays completed positive certificates and forbids repeating
an identical UNKNOWN or timeout. The compiled converter, environments,
models, proof corpora and logs are omitted from Git.
