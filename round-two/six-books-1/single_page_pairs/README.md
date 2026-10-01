# Single-page pairs at the R(B4,B7) leaf frontier

Actual author six-books-1, researcher,2026-10-01. See [PROOF.md](PROOF.md).

In any ordinary-book valid22 coloring, a red pair of degree-ten points
with a unique common red neighbor a has d(a)<=9. When d(a)=9, three
common blue neighbors are independent, four special neighbors are
independent with two incidences each to that triple, and N_R(a) has
thirteen edges and exactly two possible triangle-free types. All36
labeled special/triple cores are described and verified here. This
improves the edge-one branch of the earlier specified leaf theorem;
full host completions and the Ramsey endpoint remain open.

The theorem has an ordinary proof and requires no total edge count,
maximum degree, outside floor, rootlessness or finite root classification.
The optional thirteen-edge second-neighborhood corollary retains the
specified leaf/root-neighbor degrees and e(G)<=108.

Reproduce with CPython 3.12.14 or a compatible Python 3.11+ standard library,
from this directory. Keep native thread variables one:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 derive.py > /tmp/book-pair-derived.json
cmp /tmp/book-pair-derived.json EXPECTED.json
python3 verify.py
python3 -O derive.py > /tmp/book-pair-derived-O.json
cmp /tmp/book-pair-derived-O.json EXPECTED.json
python3 -O verify.py
python3 verify.py --self-test
python3 -O verify.py --self-test
sha256sum -c SHA256SUMS
```

The producer enumerates 648 missing-word/T-graph cores. The separate
checker starts with 4096 row-subset triples, obtains the same648
candidate cores, checks literal22-point selected-spine pages and
compares all 36 survivors entrywise. The final necessary labeled
forms have sizes 12 and 24. Full matrices used as controls do not
assert host validity. Six deliberately damaged records reject.
No other author's code, catalogue, solver or generated corpus is used.

[EXPECTED.json](EXPECTED.json) is frozen; default verification reads it
and never rewrites it. [provenance.json](provenance.json) records exact
scope, credited results, baseline and actual author measurements.
All six serial runs completed under a fixed 90-second guard in at most
0.316s and 19,932KiB. The proof and its program correspondence remain
unformalized; new independent peer review is pending.
