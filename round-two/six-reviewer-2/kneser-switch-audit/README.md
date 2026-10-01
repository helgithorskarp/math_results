# Independent KG(7,2) switching audit

Author: **six-reviewer-2**, role **independent mathematical reviewer**.

[REVIEW.md](REVIEW.md) confirms committed lemma8528 and its analytic
seven-shape coverage. It records the complete red-B4-free switch
classification (309 labeled colorings), the seven sharp ten-page star
switches, and the sharp eight-page unswitched attachment gap with
full-star equality. This does not determine the unrestricted Ramsey
endpoint, and historical priority is unestablished.

CPython3.11+ standard library only. From the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -O round-two/six-reviewer-2/kneser-switch-audit/audit.py
python3 -O round-two/six-reviewer-2/kneser-switch-audit/controls.py
```

The full audit tests all 1,048,576 normalized root graphs against the
root-degree condition. Its 554 surviving cuts equal the complete seven
root-shape domain. Literal book checks leave exactly 309 red-B4-free cuts,
with maximum blue histogram 5:1, 10:7, 11:175, 12:126. It checks all 456
intersecting-family attachments as whole 22-vertex colored graphs.
[EXPECTED.json](EXPECTED.json) is checked automatically in a full run.
The full audit takes about four seconds on one CPU, below 21MiB peak RSS.

Optional entrywise author comparison, with generated records in scratch:

```sh
python3 round-two/six-books-2/kneser_seidel_switching/enumerate.py \
  --records /tmp/kneser-author-census.json
python3 -O round-two/six-reviewer-2/kneser-switch-audit/audit.py \
  --author-records /tmp/kneser-author-census.json
python3 -O round-two/six-reviewer-2/kneser-switch-audit/controls.py \
  --author-records /tmp/kneser-author-census.json
```

All 309 records agree entrywise with the author. Their canonical SHA256
is `51a051f7ca69ed37a8a199289c00a76b2336a863c9e3189f8f4edec3034aaedb`.
Five damaged comparison inputs are rejected under `-O`. The controls
alone run only small fixtures and explicitly report that scope.
`--skip-domain` is similarly a fixture-only option; it cannot be reported
as a completed full census.

The reviewer imports no author's implementation. Computational trust is
exact source, Python execution and the written finite reduction. No
solver, numerical tolerance, external corpus or graph catalogue is used.
Generated record lists and operational files are not published. Compact
source provenance, measurements and a file manifest are included.
