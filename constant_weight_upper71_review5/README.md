# Independent saturated-point audit by six-reviewer-5

This directory independently audits reviewer 1's sharp nineteen-block theorem,
reconstructs the upper bound `A(18,6,5) <= 71`, and proves an exact accounting
identity for any hypothetical 71-word code. Read [REVIEW.md](REVIEW.md) for the
complete mathematical reduction, verdict, attribution and trust boundary.
No attainment result at 70 or 71 is claimed.

Requirements: CPython 3.11 standard library and g++ with C++17 and GNU
128-bit unsigned integers. Tested with CPython 3.11.2 and g++ 12.2.0.
Run from the repository root, using a fresh work directory outside this source
directory:

```bash
python3 -B constant_weight_upper71_review5/audit.py --work /tmp/upper71-review5-normal
python3 -O -B constant_weight_upper71_review5/audit.py --work /tmp/upper71-review5-optimized
python3 -B constant_weight_upper71_review5/audit.py --sanitize --work /tmp/upper71-review5-sanitized
```

The audit compiles and runs the native search, reconstructs both complete
compatibility graphs, checks all 4,672 target certificate nodes, reruns four
clique decisions and 66 native graph controls, restores sharp packings, and
checks all seven twenty-star profiles. It separately validates the established
69-word code, all eight three-vertex graph types and the ordinary deficit
identity on subcodes of sizes 0, 1, 5, 30, 68 and 69. The written counting
argument, rather than these finite controls, proves the identity universally.

Each run must reproduce the entire compact [expected.json](expected.json)
record. Canonical stable output is 6,180 bytes with SHA256
`3aeb886b677dba31c75816cc07d558a4f29f479c02bb0245c9da4e5008559c5a`.
Ten-clique exclusions take 525 and 1,018 search nodes; fresh nine-cliques take
ten nodes each. Normal, optimized and sanitized outputs are identical.
[validation.json](validation.json) records versions, guards, timings and memory.
The cold normal audit took 1.83 seconds; the sanitized audit took 4.71 seconds,
with peak child/compiler RSS 152,484 KiB. One intensive job runs at a time,
and all numerical-library thread settings are one.

The two external data files in [INPUT.json](INPUT.json) are the target's
36,056-byte certificate and the established 1,311-byte lower-bound word list.
If present under the repository root, they are checked for exact size and
SHA256. If missing, only those two pinned data files are downloaded from their
verified source commits and checked before use. `--repo-root PATH` selects
another local checkout; `--offline` prohibits downloads. Altered local data
are rejected. No target or original author executable is run or imported.

All generated inputs, binaries, results and run records stay under `--work`.
It must be a new directory. A timeout, guard, diagnostic, malformed certificate
or incomplete output aborts the audit and supplies no exclusion verdict.
The native guard is 200,000 nodes and ten seconds per case, with a thirty-second
outer timeout; resource settings are not increased on failure.

Source layout: [anchors.py](anchors.py) reconstructs the exact finite universe;
[clique.cpp](clique.cpp) makes fresh decisions;
[clique_audit.py](clique_audit.py) independently checks literal certificates,
adjacency and restored packings; [ordinary.py](ordinary.py) validates counting
controls and the known lower construction; [common.py](common.py) provides
explicit exception checks and serialization. No Python assertion is a proof
check. The ordinary normal form, pruning induction and global accounting
remain unformalized mathematical bridges.
