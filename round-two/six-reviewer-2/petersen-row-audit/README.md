# Independent audit of Petersen miss-row lemma8871

Actual reviewer: six-reviewer-2, independent mathematical reviewer.
See [REVIEW.md](REVIEW.md) for the exact verdict, ordinary proof,
conditional108 import, stronger geometric hypothesis, credit, and limits.
The Ramsey endpoint remains unresolved in the located primary literature.

Run from the repository root, sequentially, CPython3.11 or later,
standard library only:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-reviewer-2/petersen-row-audit/audit.py
python3 -B -O round-two/six-reviewer-2/petersen-row-audit/audit.py
python3 -B round-two/six-reviewer-2/petersen-row-audit/controls.py
```

Expected:30 nine-row incidences from2520 initial choices;31744 physical
large-point stars, no nine-row domains, one complete ten-row star;
45 forced-blue small pairs, ten root spines with nine blue pages;
180 missing-edge controls,14784 arbitrary physical-spine comparisons,
4928 signed identities and the known21-point93/117-edge fixture;
ten damaged-data rejections. [EXPECTED.json](EXPECTED.json) contains
the complete summary. [VALIDATION.json](VALIDATION.json) records
sequential timings, source replays and all60 entrywise author comparisons.

The ordinary proof does not enumerate arbitrary22-point graphs.
All generated controls except the known21-point fixture are deliberately
invalid; no host witness is supplied. No author algorithms are imported.
Author-format record hashes are obtained by independently derived data
and a verified local point map. Exact written coverage arguments remain
an unformalized trust boundary.

Optional `--records /tmp/row-records.json` regenerates the small comparison
inventory locally. `--derive` only omits comparison with EXPECTED.json;
mathematical guards remain active. Generated records are not published.
The known primary input is credited and checked byte-for-byte in the review.
