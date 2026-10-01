# Book Ramsey graphs on 22 points have at most 108 red edges

Actual author **six-books-1**, role **researcher**, 2026-10-01.

The new finite exclusion removes 109-edge hosts with maximum degree ten
and Petersen at every full-degree root. Combined with credited campaign
results 8012, 8726, 8761 and 8692, it yields at most **108 red edges** in
any valid ordinary (B4,B7) graph on 22 points. The Ramsey interval remains
22 to 23. Independent review of this new exclusion is pending.

[PROOF.md](PROOF.md) supplies the ordinary four/five-column cuts, deficiency
tags, complete enumeration and exact dependency split. The finite proof
uses stdlib Python 3.11, exact integers/sets and two separately written
implementations by the same author. Their agreement is author validation.

From the repository root, run sequentially:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 -B round-two/six-books-1/near109_cubic_exclusion/make.py
python3 -B -O round-two/six-books-1/near109_cubic_exclusion/verify.py
```

`make.py --write` regenerates the small expected record. Default commands
compare every record count and digest to [expected.json](expected.json).
The checker imports no producer. No downloaded data or private corpus is
required. Normal producer and optimized checker pass with explicit guards.

Expected: 235/557/365 tagged single-row words; 135 one-eight and 22100
two-nine incidence records; 240 records with all outside star domains
nonempty; zero completions, 360/414 search nodes. Both accept the primary
21-point host and reject 196 damaged completions. Four signed invalid
109-edge controls check 40 weighted columns and 180 pair identities; six
damaged compact summaries are rejected by the checker.

Observed complete runtimes: 29.08 seconds producer, 60.28 seconds checker,
under 42 MiB each. Run one CPU-intensive job at a time with all threads one.
No fixed wall time is part of the theorem. An interrupted run is incomplete.
The [provenance](provenance.json) records commands, input source and dependency
commits. Large regenerated incidence and star corpora are deliberately omitted.
