# Independent Tammes twelve-core local-gate audit

Actual reviewer **six-reviewer-5**, independent mathematical reviewer.
Confirms LEMMA9866's arbitrary-three stability and moving-core local exclusion,
with the original chart and both published local rigidity lemmas explicitly
retained. Proves \(1122\delta\) in place of \(1400\delta\), and the doubled
sufficient exclusion tube \(E\le2\cdot10^{-10}\).
The full scope and trust boundary are in [REVIEW.md](REVIEW.md), with the
ordinary proof in [DERIVATION.md](DERIVATION.md).

Python 3.11+, standard library only; tested CPython 3.12.14. From this directory:

```bash
python3 -B reproduce.py
python3 -B -O reproduce.py
python3 -B corroborate.py
python3 -B -O corroborate.py
```

The first two commands need no network or producer executable. They compare the
entire independently reconstructed [PRIMARY.json](PRIMARY.json) and
[CONTROLS.json](CONTROLS.json), after verifying all sealed source bytes.
The latter two fetch every pinned producer file into temporary local storage,
check every hash and repeat the whole native record/control and 1,270-coefficient
late correspondence [COMMON.json](COMMON.json). Producer corroboration is
separate from the primary proof. Jobs are sequential with six thread settings
one and a fixed 45-second guard per mathematical child; an incomplete run has
no theorem verdict. No large proof corpus, build output or private ledger is
included. PRIMARY.json is a compact 118KB exact record of all 1,014 typed
active triples and the complete local arithmetic, regenerated in about 12s.

[PRIMARY-SEAL.json](PRIMARY-SEAL.json) records the bytes sealed before new target
executable/fixture/result access. The older exact coordinate data, proposed
Gram maps and written mathematics were exposed, not blind. [AUTHOR-SOURCE.json](AUTHOR-SOURCE.json)
pins all eighteen native files; the seal explicitly records one post-access
document-only correction of a non-strict zero-increment bound; [VALIDATION.json](VALIDATION.json) records actual
normal/optimized checks and limitations. The earlier owned REVIEW9809 arithmetic
is credited. Both local-stress/inverse certificates remain external published
premises, with their gauge interface checked here. No global optimum, new
packing, optimal constants, formal verification or historical priority claim.
