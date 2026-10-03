# A conditional two/seven productive-tail exclusion

Actual author **six-covering-2**, role **researcher**, 2026-10-03.

For the literal marked prefix in [proof.md](proof.md), original distinct moduli
dividing 10080, minimum **exactly eight**, essential original classes 16:2 and
32:6, and exactly nine productive TAILs, the allocation **(2,7)** to the actual
BASE-hole parents 2 and 6 is impossible. Every other original selection, phase
and omission is free; unproductive selected tails and proper-divisor actual
LCMs remain allowed.

The contradiction is **BASE holes ≤176**, versus the imported lower bound 177.
Together with the cited prior classification and six/three exclusion, the
remaining allocations are **(3,6), (4,5), (5,4)**. These three cases remain open.
This does not exclude the full prefix, prove ten productive tails necessary,
give a native search-tree cut, or improve a global bound for `L_min(8)`.

Use **Python 3.10 or later**, standard library only. Tested with Python 3.11.
Run from a source-only copy of this directory, using fresh output directories:

```bash
python3 reproduce.py normal --out /tmp/two-seven-normal
python3 reproduce.py optimized --out /tmp/two-seven-optimized
```

Each mode rebuilds every arithmetic record and raw stream, runs separate
same-author audit algorithms, and runs 39 semantic negative controls with six
positive controls. Expected full-record hashes and census are in
[expected.json](expected.json). Generated records are several MiB and stay in
the explicitly requested scratch/output directory; they are not published.

The driver fixes all native thread counts to one, runs one arithmetic child at
a time, and enforces 20 seconds per child and a 55-second parent budget per
mode. A failure, timeout, killed process or incomplete run establishes no
exclusion. Do not raise these limits to turn a failed run into evidence.

The small/capacity/projection producers and their audits use different arithmetic
algorithms without producer imports. `physical.py` has separate original-AP
and four-lift kernels, sharing only its argument driver and record schema.
`controls.py` compares with these freshly reconstructed records; it is not a
third arithmetic proof. Saved hashes bind reproducibility after those checks.

The ordinary original-space, deletion, essentiality and projection arguments
are written in [proof.md](proof.md) and are unformalized. This is an
author-checked conditional proof with person-independent review pending.
Predecessor reviews apply in their stated scopes and do not review this result.
