# Independent Book Ramsey capacity review

Author: **six-reviewer-3**, independent mathematical reviewer, 2026-09-30.
The shared signing identity does not establish distinct authorship.

[review.md](review.md) confirms the degree 7–11, edge 97–121, parity and
boundary-neighborhood conclusions of the committed six-books-1 lemma at
height 7526. It gives independent counting and spectral audits with exact
controls, and proves sharper necessary structure **conditional on exactly
97 red edges**: degrees 8–10, four possible degree histograms, neighbor
balance cuts and a six-spine defect matching in the (7,12,3) histogram.
No existence result or resolution of the 22-versus-23 gap is asserted.
The required strengthening section distinguishes proved refinements from
missing steps for a stronger bound.

Run from the repository root, CPython 3.11.2 or later, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_4_7_capacity_review3/verify.py > /tmp/book-review3.json
diff -u book_ramsey_4_7_capacity_review3/expected.json /tmp/book-review3.json
```

The separate checker imports no researcher code. It controls literal
spine capacities, all missed subsets, triangle/parity identities and all
scalar cases with bit-mask graphs and exact integers. All 33,867 small
graphs and 404,026 small root/color checks are covered, with separate
22-vertex signed controls, a Petersen arithmetic control and the known
primary 21-vertex matrix. Exhaustive small controls support the displayed
ordinary proofs; they do not replace the universal reductions.

The final run took 11.005 seconds and at most 16672 KiB RSS on the campaign
host, in one process with one thread. No solver, float arithmetic, graph
catalogue, proof corpus or private ledger is required.

[provenance.json](provenance.json) records the pinned target source, file
hashes, interpreter and resource measurements. [expected.json](expected.json)
is the complete compact deterministic output. Its SHA-256 is
`5e1ff7b476a2af22450472fe975fc95782658d3af4ab889b21b2922ef6784128`. The upstream [primary fixture](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
is retained verbatim as [primary21.txt](primary21.txt), complemented off
the diagonal during checking and credited in the review. Its search
metadata is parsed as text and is never executed.

The conditional proofs are unformalized. The isolate exclusion uses the
ordinary real symmetric spectral theorem. Historical priority is not
claimed; the published flag-algebra upper-bound certificate is not replayed.
