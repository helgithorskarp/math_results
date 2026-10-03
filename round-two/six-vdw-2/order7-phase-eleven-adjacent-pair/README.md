# Adjacent minority phases at H7 weights11/33

Actual author six-vdw-2, researcher. See [PROOF.md](PROOF.md) for the precise
field-coloring domain,72-case lossless cover, certificates and limits. The
isolated branch is excluded; the phase endpoints and3704 target remain open.

Run from this directory in a full repository checkout using CPython3.11.2,
PySAT1.8.dev24 with CaDiCaL1.9.5, and the pinned upstream `drat-trim` source:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 reproduce.py --work work --converter /absolute/path/to/drat-trim
```

The converter and sibling `drat-trim.c` must have the source provenance in
SOURCE_PINS.json. That file also pins145 whole public ancestor/helper files.
The driver reconstructs all72 canonical models, nine disjoint eight-case
literal audits per mode, all coverage/count/gauge controls and79 meaningful
damages per mode before certificate access. Every full normal/O definition,
damage and strict RUP record must match; EXPECTED.csv gives all72 input and
proof hashes and counts. No partial result is a complete exclusion.
The driver writes `stage-ledger.json` before each child and records completion
after it returns. An interrupted running stage remains explicitly incomplete;
the driver still requires a fresh workspace and never resumes a failed input.

An externally supplied LRAT directory can replace new native proposals:

```sh
python3 reproduce.py --work fresh-proof-replay --converter /absolute/path/to/drat-trim \
  --certificate-cache /absolute/path/to/untrusted-lrat-directory
```

Each candidate is untrusted and checked independently against the freshly
reconstructed whole physical CNF in both modes. The public source copy was
checked this way using the completed private72 proofs; the default command
regenerates candidates. The native solver/converter are discovery layers.
The strict checker and ordinary reductions supply the negative proof.

Expected complete status: `EXACT_H7_ELEVEN_ADJACENT_MINORITY_PAIR`.
Each mode checks873538 additions,4655556 deletions and14140470 positive hints.
Ordinary phase controls cover55110 normalized words/background and84510
shortest-pair markings; these do not count feasible field colorings.

All numerical threads are one and children are serial. Existing guards are
55s for each definition/control/damage child,30s native at50000 conflicts,
25s internal/30s external conversion and30s strict replay/case/mode.
UNKNOWN, timeout, memory failure or incomplete results prove no exclusion.
Stop at the first incomplete case and preserve it; do not retry identical
failed inputs or raise resource settings. Ten old failed inputs remain
frozen and are absent from this new72-case family.

Generated models, proofs, caches and logs stay local and are ignored. No
large proof corpus or private graph/signing/account data is published.
This is author-checked and unformalized; external-person review is pending.
