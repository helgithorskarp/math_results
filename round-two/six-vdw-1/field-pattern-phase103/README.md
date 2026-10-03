# F103 independent phase-table repair obstruction

six-vdw-1, researcher. See [PROOF.md](PROOF.md) for the precise theorem.
For roots p+u,p+2u,p+4u and a free physical pole p, arbitrary independent
Boolean truth tables at every phase need at least five additional edited
field columns. This holds for any phase modulus m coprime103 on cyclic103m
or [1,N] with N>=408m+1. On cyclic103m or N>=409m, at least5m individual
nonroot/nonpole positions must change. All original roots remain freely
colored, including ignored inputs; these values may be nonperiodic.

For m6 the cuts are five columns at2449 and30 positions at2454. There
is no new W(2,7) lower bound, repair optimum or sufficiency claim.

With standard-library CPython3.12 (tested3.12.14):

```sh
python reproduce.py
```

The runner checks its source manifest, regenerates the whole3735-byte
positive certificate, and runs the independent checker and real controls
normally and with `-O`. Every source/evidence byte and complete result
must match; children are serial, threads1, each guarded at20 seconds.
There is no native solver, converter, graph SDK, network or external
data dependency. Generated files live in a temporary directory.

[EXPECTED.json](EXPECTED.json) holds the complete deterministic records,
and [VALIDATION.json](VALIDATION.json) describes the trust boundary.
[four-APs.json](four-APs.json) gives the elementary unedited obstruction;
[five-packs.csv](five-packs.csv) gives five disjoint actual field APs
for each of128 gauged truth tables. A failed generator/search never
establishes absence. The independent checker validates successful
positive witnesses directly against the mathematical definition.
