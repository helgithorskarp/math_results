# Two-root parity audit

Actual agent six-reviewer-2, independent mathematical reviewer. See
[REVIEW.md](REVIEW.md) for the full proof, exact imported-premise boundary,
weaker mixed-cap theorem and proved exact-two cuts. This is a review of
LEMMA9199, not a22-host exclusion or a numerical Ramsey improvement.

CPython3.12.14; standard library only. From this directory, run serially:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -B check.py
python3 -B -O check.py
python3 -B compare_author.py
python3 -B -O compare_author.py
python3 -B boundary.py
python3 -B -O boundary.py
```

Each prints a compact `PASS` record. `check.py` regenerates the entire own
record and nine damages; `compare_author.py` reconstructs all credited
author record fields without importing author code; `boundary.py` checks
the matrix identities, equality-cut tables and two damages. Optimized
checks remain active. `--record` prints the complete computed JSON instead
of comparing its frozen counterpart.

`expected.json` is the initial independent record; `AUTHOR-expected.json`
is the original researcher's credited comparison data; `boundary-expected.json`
is the equality-control record. All six `INPUT-controls.json`22-point
graphs are invalid signed identity controls. The141 count profiles are
necessary only. Neither is a valid-host enumeration.

`PRIMARY21.txt` is the authors' known21-point construction. Its leading
matrix's off-diagonal zeros encode red; trailing search metadata is preserved.
There is no runtime network input. Sources, exact measurements, credit and
chronology are in [provenance.json](provenance.json); compact file hashes
are in [manifest.json](manifest.json). No raw logs, graph ledger, keys,
large corpus or private checkpoint is required or published.

The independently frozen original engine preceded author-code inspection.
The record-layout adapter and equality checker were written afterward.
The ordinary proof supplies the universal mathematical bridge. The universal
108-edge conclusion retains9102's imported maximum-ten/rootlessness premises.
