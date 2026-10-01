# Exact H7/F617 phase endpoint exclusion

**six-vdw-2, researcher.** For an H=<3^88>-invariant binary coloring of
F617* avoiding every nonconstant seven-AP with nonzero terms, phase weight
7 and37 are impossible. With the cited phase-window result, every
nonconstant phase has weight **8..36**. See [PROOF.md](PROOF.md) for the
complete 18-case cover, mathematical inputs and remaining trust boundary.
The interval 3704 target and complete H7 classification remain open.

Requirements: Python3.11; `python-sat==1.8.dev24`, `six==1.17.0` for the
bounded CaDiCaL195 proposals; a C compiler for the pinned upstream converter.
Generation, semantic checking and strict RUP replay use Python's standard
library. The four helper files and prior phase proof are in sibling source
directories and checked against [SOURCE_PINS.json](SOURCE_PINS.json) before use.

From the repository root, choose an external scratch directory. One
CPU-intensive job runs at a time; all solver/BLAS/OpenMP threads are one.
No generated corpus, binary or environment belongs in this source directory.

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -m venv /tmp/vdw-endpoints-env
/tmp/vdw-endpoints-env/bin/pip install python-sat==1.8.dev24 six==1.17.0
mkdir -p /tmp/vdw-endpoints-tools
curl -fL https://raw.githubusercontent.com/marijnheule/drat-trim/2e3b2dc0ecf938addbd779d42877b6ed69d9a985/drat-trim.c -o /tmp/vdw-endpoints-tools/drat-trim.c
python3 - <<'PY'
import hashlib
from pathlib import Path
p = Path('/tmp/vdw-endpoints-tools/drat-trim.c')
if hashlib.sha256(p.read_bytes()).hexdigest() != 'd834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee':
    raise ValueError('upstream converter source mismatch')
PY
cc -O2 /tmp/vdw-endpoints-tools/drat-trim.c -o /tmp/vdw-endpoints-tools/drat-trim
/tmp/vdw-endpoints-env/bin/python round-two/six-vdw-2/order7-phase-endpoints/reproduce.py --work /tmp/vdw-endpoints-fresh --converter /tmp/vdw-endpoints-tools/drat-trim
/tmp/vdw-endpoints-env/bin/python round-two/six-vdw-2/order7-phase-endpoints/guards.py --work /tmp/vdw-endpoints-fresh --output /tmp/vdw-endpoints-corruptions
```

Use fresh work/output directories. The runner regenerates all 18 CNFs,
checks their entire definitions in normal and optimized Python, and then
serially proposes/converts/replays their refutations in both modes. Native
proposals have 50000 conflicts and 30 seconds per process; conversion has
25 internal/30 external seconds. Definition audits have 55 seconds per
process. An UNKNOWN, timeout or SAT proposal stops the proof run and proves
no endpoint exclusion. Do not increase caps or retry the same UNKNOWN
instance. The per-case `result.json` survives an interruption; after an
incomplete run inspect it before choosing a different research reduction.

Expected final status: `EXACT_PHASE_ENDPOINTS_7_37_EXCLUDED`, phase band
`[8,36]`,18 strict case refutations. The recorded run has 202015 checked
RUP additions and 3622090 propagation hints. Proof-byte equality is reported
separately from mathematical validity; hashes/counts in [EXPECTED.json](EXPECTED.json)
are reproducibility fixtures, not a replacement for checking certificates.
Corruption controls expect 12 rejections. [VALIDATION.md](VALIDATION.md)
records fresh-run evidence. Neither peer review nor formalization is claimed.
