# A conditional period-43200 covering exclusion at phase 72:42

Actual author **six-covering-3**, role **researcher**,2026-10-01.

No distinct covering with moduli at least8 dividing43200 contains the
twenty prescribed classes in [proof.md](proof.md). The minimum is exactly8
because the8 class is prescribed; actual LCM may divide43200. Every other
eligible divisor can be omitted or have any phase, at most once.

The complete tree has30 direct100 leaves and two28-leaf108 splits,86
representative leaves in total. The supplied50 integer weights use462
literal basis boxes and5637 sparse positive terms. The standard-library
checker evaluates every physical phase bucket for each stored vector;
the separate action checker checks full ambient maps and all prescriptions.
All four parts and the written argument are required. Independent review
and formalization are pending. Global L_min(8) bounds remain unchanged.

From this directory, Python>=3.11, standard library only, run sequentially:

```bash
python3 -B check.py --part orbits100
python3 -B check.py --part orbits108
python3 -B check.py --part capacity100 --controls
python3 -B check.py --part capacity108
```

Each prints an exact certificate equal to its entry in
[expected.json](expected.json). Capacity100 additionally rejects16 malformed
fixtures. The action checks reject5 and6 controls, respectively. Each part has a20s
loop cap and explicit exceptions, also effective under Python-O. A
timeout or incomplete run is not an exclusion. The author's outer-job
cap is30s; one CPU-intensive job at a time and all solver/BLAS/OpenMP
threads1. Reproduction itself imports no solver and starts no workers.

Expected prototype census: 2818 resource
instances,7831144 actual phase buckets and
192000 binary union cases. The smallest prototype
gaps are794 at100
and4 at108.
Every86 representative support is explicitly checked.

Fixture SHA256: `876954bf0b89bbf629f0514a876423596130e733690363fa10dd5f9c8d790f74`. Exact source hashes are in
[MANIFEST.md](MANIFEST.md). No private forest, ledger, solver transcript,
large audit corpus or generated cache is needed. Trust consists of exact
Python integer arithmetic, the supplied finite fixture and the written
CRT/completion/binary argument. General-method priority is not claimed.
