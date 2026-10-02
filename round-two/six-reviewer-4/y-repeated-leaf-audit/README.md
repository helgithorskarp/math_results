# Reproduce the independent Y-repeated leaf audit

Actual author six-reviewer-4, independent mathematical reviewer,2026-10-02.
Read [REVIEW.md](REVIEW.md) for hypotheses, proof, verdict and limitations.
This independently checks9327's six interfaces and allows165 initial outside
low placements without its earlier T0-degree or selected-cycle filters.

Python3.12 standard library and a C++17 g++ compiler are sufficient. From this
directory run serially, with a writable scratch output directory:

```bash
python3 check.py --out /tmp/six-reviewer-4-Y-normal
python3 -O check.py --out /tmp/six-reviewer-4-Y-optimized
cmp /tmp/six-reviewer-4-Y-normal/mathematics.json /tmp/six-reviewer-4-Y-optimized/mathematics.json
```

The driver checks the whole native census, every naturally disjoint set-enumeration
stratum, literal endpoint/rank/transport/corruption controls, and full native
ASan/UBSan output. Every direct CPU child has a fixed60-second guard, with
owned process-group termination on timeout. A failed/incomplete run is not
a mathematical exclusion. All native numerical thread variables are1 and
all children run serially. No solver, network, external mathematical data,
author fixture or private corpus is needed by these independent commands.

Expected full1058-byte record:

```text
35c0eebf3c599ffae9a55cb33c532463b479cfddc05be8f4cc54fc34f9777321
```

Expected mathematical aggregate:

```text
1e26ec5a98141f64fcdf93f0eff50f4604a5a29be25dbc8262ce11751224aa14
```

[RESULTS.json](RESULTS.json) contains every surviving interface and all stratum
counts. [evidence.json](evidence.json) records the successful normal/optimized
runs and later unmodified author corroboration, including actual source versions,
resource reporting and the two corrected non-mathematical/control edits.
The ordinary-to-finite proof remains unformalized.

Optional author corroboration is separate. Obtain exactly the seven public files
at commit53299fce3d1533600741841940a4a625db2fdb70 listed in
[AUTHOR_SOURCE.json](AUTHOR_SOURCE.json), place them together in a directory,
and run:

```bash
python3 corroborate.py --author /path/to/pinned-caseI_tagged_leaf --out /tmp/six-reviewer-4-Y-author
```

This verifies all source hashes before running the unmodified author row and
column programs in normal/optimized modes and both damage modes. Every2497-byte
record must equal the entire pinned EXPECTED.json; every decoded interface and
all11 author flag-survivor counts must match the independent six-interface domain.
This optional replay is corroboration, not an independent proof input.

Generated binaries, logs, scratch output and Python caches are excluded from
publication. This directory carries compact source and complete small evidence only.
