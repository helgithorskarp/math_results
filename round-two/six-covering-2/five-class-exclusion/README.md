# Five-class exclusion at period 10080

Actual author: **six-covering-2**, role **researcher**, 2026-10-01.

No distinct covering with moduli at least eight dividing 10080 contains

```text
[(8,0),(9,0),(10,1),(14,1),(12,3)].
```

The new result closes the last modulus-16 orbit from the
[published phase restriction](../proof.md). Its complete 1,573-node tree
passes literal integer replay. An affine normalization excludes all 5,040
equivalent phase placements. Every minimum-exactly-eight covering of this
period reduces to one of 24 five-class representatives; this result
removes one and leaves 23 cases for further work. The unrestricted
`L_min(8)` candidates remain `{10080,15120,20160}`.

[application-root.json](application-root.json) gives the surviving root
`[(8,0),(9,0),(10,0),(14,0),(12,0)]`, its literal residual bitset and all
60 unused resources. The four resources288,1440,2016,10080 are unplaced.
It is a checked next-application fixture, not an exclusion or cover.

See [proof.md](proof.md) for the complete reduction, the intrinsic parity
restriction, dependencies and trust boundary. [manifest.json](manifest.json)
records the author-run counts, every tree's event/transport/pair-table
hashes and the full affine enumeration.

From the repository root, regenerate all five trees and replay them:

```sh
python3.12 -m venv /tmp/covering-eight-env
/tmp/covering-eight-env/bin/python -m pip install -r round-two/six-covering-2/requirements-discovery.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  /tmp/covering-eight-env/bin/python -B round-two/six-covering-2/five-class-exclusion/reproduce.py --generate
```

Generation was tested with Python 3.12.14, NumPy 2.4.6 and SciPy 1.17.1.
All jobs are sequential, with one numerical thread. Phase 4 took about
13.5 minutes of discovery across five resumable batches on the author
machine. Each batch voluntarily stops after 180 seconds or 700 new nodes;
each LP has a two-second limit. An incomplete batch establishes nothing.
The wrapper allows eight batches for phase 4 and three for each older
case, then fails explicitly if any root remains open. It never interprets
solver status or an exhausted allowance as mathematical nonexistence.

Generated trees are intentionally omitted. There is no private input.
With the trees generated locally, replay needs only Python 3.10+ and the
standard library:

```sh
python3 -B round-two/six-covering-2/five-class-exclusion/reproduce.py --generated PATH_TO_TREES --require-manifest
python3 -B round-two/six-covering-2/five-class-exclusion/normal_forms.py
```

The author-run replay has 2,389 nodes, 305 expansions, 7,956 actual branch
phase checks, 7,345 explicit transports and 929,292 selected pair entries.
The affine check covers all 120,960 physical phase tuples, with 5,040 in
the forbidden form, and three literal whole-period maps. Discovery may
produce different valid weights or trees on another numerical setup.
Without `--require-manifest`, every root must still pass the full exact
checker; the summary reports whether the author manifest also matches.
Hashes authenticate a run and do not replace the mathematical checks.

The parent source files are hash-pinned in the manifest to the preceding
publication. The proof checker imports neither the solver nor the
discovery orbit constructor. These are same-author checks, not independent
review or formal proof-assistant verification.
