# Exact correction of the ACD `D(10,9)` Lagrange-cover data

## Result

The public ACD Repo dataset `partial_orders_on_lattice_paths_10x9` does not
encode Lagrange-order covers as claimed.  Its matching-order portion is valid,
but its Lagrange portion was generated after sorting Lagrange-value classes by
their stored path lists rather than by their Lagrange values.

An exact reconstruction gives the following complete audit:

* `D(10,9)` has 4,862 paths, 4,859 matching-number levels, and 2,494
  Lagrange-number levels.
* The true orders have 4,864 matching covers and 9,481 Lagrange covers, of
  which 122 are covers in both orders.  Removing just those common pairs gives
  4,742 matching-only and 9,359 Lagrange-only examples.
* All 4,843 published matching-labelled rows are genuine matching covers, but
  121 are also genuine Lagrange covers and hence are not exclusive as claimed.
* Of 9,453 published Lagrange-labelled rows, only 55 are genuine Lagrange
  covers.  The other 9,398 are not covers: 6,003 point from a larger Lagrange
  value to a smaller one, while 3,395 point upward but skip at least one value
  level.  Among the reversed rows, 631 become exact covers when reversed.
* The incorrect notebook ordering of the 2,494 Lagrange levels has 1,578
  adjacent descents in the true numerical order.

The exact cover-pair SHA-256 records are in `certificate.json`.  No corrected
bulk dataset is committed: the short source regenerates it exactly.

## Root cause

In the source notebook, `D_l.items()` consists of pairs

```text
((D,q), [(path, floating_L), ...]).
```

It is ordered by

```python
sorted(D_l_items_list, key=operator.itemgetter(1, 0, -1))
```

Python therefore compares item `1` first: the value list beginning with the
first stored path.  Distinct value classes have distinct first paths, so this
is a lexicographic path ordering, not a Lagrange-number ordering.  The next
function treats consecutive classes in this list as cover levels.

There is a second, smaller mismatch between the code and description.  The
description says common cover *pairs* are removed.  The code instead removes
every cover above a lower path whenever that path has any cover common to the
two computed relations.  The corrected exclusive counts above implement the
stated pairwise removal.

The independent reconstruction of this exact notebook logic reproduces all
14,296 published train/test rows, including every label.  This rules out an
unmodeled Sage sorting convention or a later hidden generation step.

## Exact mathematics

Write a path as a word in `R=1,U=0`.  Replace each equal adjacent pair by
`1,1` and each unequal adjacent pair by `2`, obtaining a finite continued
fraction word `C`.  Its numerator is the matching number.

For the Lagrange number, put `A=(2,C)` and consider every cyclic shift.  If

```text
product([[a,1],[1,0]] for a in A_shift) = [[p,r],[q,s]],
```

then the difference of the two quadratic conjugates for that shift is

```text
sqrt((p-s)^2 + 4*r*q) / q.
```

Thus all ordering and equality decisions are made exactly by comparing the
rational squares

```text
((p-s)^2 + 4*r*q) / q^2.
```

No floating point is used.  Since each order is induced by one scalar, its
cover pairs are exactly all cross-products of consecutive distinct value
levels.  `test_exact_covers.py` independently recomputes the Lagrange squares
from four continuants rather than the production running-matrix algorithm.
It checks every path through `D(8,7)`.  The example
`RRRUURURU, RRRUURRUU` from Apruzzese--Cong is also reproduced exactly:

```text
M = 1115, 1177
L^2 = 11390621/1055^2, 17^2*48893/1177^2,
```

with the Lagrange inequality opposite to the matching inequality.

## Reproduction

Requirements: CPython 3.11 or later; no third-party packages.

From this directory run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -I exact_covers.py
PYTHONDONTWRITEBYTECODE=1 python3 -I audit_published.py \
  --scratch-dir /scratch/acd_lagrange_cover_correction
PYTHONDONTWRITEBYTECODE=1 python3 -I test_exact_covers.py
sha256sum -c SHA256SUMS
```

The audit downloads the two published JSONL files into the specified scratch
directory and rejects them unless their pinned SHA-256 values match.  Expected
terminal markers are `EXACT COVER CERTIFICATE VERIFIED`,
`PUBLISHED DATA AUDIT VERIFIED`, and five passing tests.

## Sources, scope, and trust boundary

* Open problem and definitions: Apruzzese and Cong,
  [On Two Orderings of Lattice Paths](https://arxiv.org/abs/2310.16963).
* ACD dataset paper: Chau et al.,
  [Machine Learning meets Algebraic Combinatorics](https://arxiv.org/abs/2503.06366).
* Audited generation notebook:
  [PNNL/ML4AlgComb](https://github.com/pnnl/ML4AlgComb/blob/master/lattice_path_posets/lattice_path_data_generation_with_sage.ipynb),
  inspected at upstream commit `85512421547ccb066318b08ae0205ba8c68a722f`.
* Published data:
  [ACDRepo `10x9` dataset](https://huggingface.co/datasets/ACDRepo/partial_orders_on_lattice_paths_10x9).

The enumeration is exhaustive for `D(10,9)`, and the arithmetic is exact.
The trust boundary is the displayed reduction, readable standard-library
Python, CPython integer semantics, SHA-256, operating system, and hardware.
The external JSONL files are used only to audit the publication; the corrected
cover counts are regenerated from definitions.  This contribution does not
classify cover relations for general `D(a,b)`, assess the paper's model
experiments, or claim that analogous published files at other sizes were
audited.  Targeted web, repository-issue, and committed-graph searches on
2026-09-03 found no earlier report of this dataset defect or exact correction;
that is search-relative novelty, not a priority claim.
