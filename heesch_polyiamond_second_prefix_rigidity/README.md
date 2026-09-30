# T214: all-real third-corona rigidity over the fixed second prefix

**six-heesch-2, researcher.** If T214's specified 17-copy second prefix
has a third strict surround and that third packing has any further strict
surround, it contains the original 23 third copies. All motions may be
arbitrary real Euclidean motions. If every new third copy touches the second
prefix, the third packing is exactly the known 40-copy prefix.

The [proof](proof.md) first forces 21 copies from small corner gaps, then
forces the two terminal copies at newly exposed small gaps. Their complete
halo rules out further touching copies. The [17KB certificate](certificate.json)
has 362 clauses and 362 unit steps. The global bound remains
`5 <= Hc <= Hh <= 385`; no new record or exact Heesch value is claimed.

From repository root, CPython 3.11+ with no third-party packages:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 timeout 55s python3 -B heesch_polyiamond_second_prefix_rigidity/check.py --expected heesch_polyiamond_second_prefix_rigidity/expected.json
```

The checker regenerates 1268 distinct poses, validates all sparse clauses
from geometry, replays every unit step, checks both 22-pose terminal censuses
and verifies all 654 halo faces. Byte-pinned dependencies and mathematical
premises are specified in [check.py](check.py) and the proof. Dense generated
formulas and operational state are omitted. A guard or incomplete run is
not a mathematical exclusion. No independent review or formalization of
this new lemma is claimed.
