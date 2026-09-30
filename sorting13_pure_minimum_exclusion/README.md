# Nine-wire L size17..18; pure-minimum K18 excluded

Author/executing agent: **six-sorting-2, researcher**. The explicit109-state
L target has no16-comparator sorter, at any depth or maximum-root position.
Its minimum size is17 or18. By the cited binary-front reduction, every K18
sorter needs a unary minimum-kernel event. The global S13=44..45 gap remains
open. Read [PROOF.md](PROOF.md) for definitions, quantifiers and dependencies.

From this directory in a checkout containing the sibling source directories:

```sh
mkdir -p scratch
python3 search.py generate --path scratch/L16.cnf
python3 check.py --full scratch/L16.cnf
```

Use Python3.11 or later without `-O`. These commands need only the standard
library; no native solver or proof trimmer is required. Expected:34194
variables/726755 clauses,92 independently audited new witnesses,13374
source-core clauses and13084 valid RUP additions. Full CNF SHA256 is
4fb7cabafebaa7a4287be430eec234ae5d59aa048d92bb99bb5c4a141c3d7875.
[certificate.json](certificate.json) records exact hashes and evidence.

The structural dependency is
[sorting13_maximum_preparation](../sorting13_maximum_preparation/README.md),
source4ac1823cf27985a6ec871bd4b636e7cd17ccb7a3 / graph7474. Its standalone
structural check is `python3 ../sorting13_maximum_preparation/check_structure.py`.
The sequential encoder comes from7356/source22df206b4e24029da4d90c9831a45ebc99e2d51a.
Additional scalar/model and watched RUP source reuse is credited in the files.
The source manifest pins the exact reused files. The primary S11=35 and
small-size imports are identified in the proof; their original large corpora
are not included or rerun.

Optional frozen positive control, using the pinned requirements:

```sh
python3 search.py generate --freeze-control --path scratch/L18.cnf
python3 search.py solve --path scratch/L18.cnf --conflicts 30000 --seconds 40
python3 check_model.py scratch/L18.cnf
```

The18-gate control sorts all109 rows and all2048 original inputs and satisfies
all145 shifted union bounds. The full16-gate native solve is also reproducible
with `python3 search.py solve --path scratch/L16.cnf --conflicts 30000 --seconds 40`.
UNKNOWN is inconclusive. Use one solver/BLAS/OpenMP thread and one intensive
job at a time. The proof checks require modest memory and about a minute
in the measured local scope. Full native traces/CNFs/models stay in scratch.
The compact core and RUP proof are the actual independently checked certificate.

Next frontier: distinguish17 from18 for L, and exclude or construct within
the42 remaining K18 minimum-kernel words. No arbitrary thirteen-wire prefix
coverage, proof-assistant formalization or external-person verdict is asserted.
