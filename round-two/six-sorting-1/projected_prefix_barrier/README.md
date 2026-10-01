# A 24-gate prefix barrier for the projected construction family

Author and executing agent: **six-sorting-1, researcher**, 2026-10-01.

Of the 869 canonical thirteen-input projected words in the earlier
[projection family](../projection_deletion_barrier/README.md), **867 have
24-gate prefixes that cannot start any sorter with at most 44 comparators**.
The suffix may use arbitrary comparator choices, orientations, interleavings
and depth. This strengthens the earlier deletion-only obstruction for this
specified family. It does not change the global `44 <= S(13) <= 45` interval.

The two prefixes passing this necessary check come from the original
`N13L46D9` and `N13L45D10` thirteen-input table words. Passing gives no
completion. The incumbent 45-gate word's first 20 gates already have a
published completion exclusion; the present construction target is the
native 46-gate word's first 24 gates followed by any 20 comparators.

| Prefix length | Distinct seed words passing both anchor bounds |
|---:|---:|
| 8 | 869 |
| 12 | 869 |
| 16 | 869 |
| 20 | 356 |
| 24 | 2 |

The 24-gate prefixes are all distinct. Canonical survivor indices are
396 (`N13L46D9`) and 591 (`N13L45D10`), counting from zero. Both have
normalized low/high anchor masses `(512,512)`. The other 867 have maximum
mass 576 (341 cases) or 640 (526 cases), above the size-44 ceiling 512.

The theorem is an exact application of six-sorting-2's
[semantic anchor Huffman lemma](../../six-sorting-2/semantic-pruning/ANCHORS.md),
source commit `b49096c7b4af0920e93e78c489d69bd7105363cb`, graph
`bafkreidfuz2cnbkhgd7urqenzmv7iiy5tjvj5ghbmxlyhcbxhdkqdoalle` (8604).
The producer is an incremental C++ transport of every original marked
truth-table family. The checker reconstructs projections by a different
algorithm, then recomputes all 4,345 prefix values with the pinned Python
profile and anchor implementations. It imports neither new C++ program.
The existing independent scalar/Huffman certificate was also rerun here:
4,473,152 free assignments, all checks passed in 39.861 seconds / 22 MiB.
Algorithmic checking is not an external-person review or formalization.

From the repository root, Python 3.11+, GCC 12.2+, one CPU job/thread:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-sorting-1/projected_prefix_barrier/generate.py
python3 -B round-two/six-sorting-1/projected_prefix_barrier/verify.py
python3 -B round-two/six-sorting-1/projected_prefix_barrier/check_examples.py
```

The checker took 140.350 seconds and 22,344 KiB peak RSS. The C++ screen
took 2.096 seconds. The 68,759-byte certificate has SHA256
`73d746988f6fa5150a39ab02874ec6601be1b4db04fde1f9c03e18ff3c1cc594`.
Default output goes to workspace `scratch`; alternate work/dependency
directories are supported. Dependencies are checked by exact byte hashes.

Two optional fixed construction fixtures illustrate the surviving native
prefix. Both 44-gate words pass the anchor bounds but fail Boolean sorting:
403 inputs for distinct-image fitness and 366 for original-input fitness.
They were produced by an incomplete width-32 beam, with no fixed-depth
restriction. Complete failure lists and exact gates are in
`construction-examples.json`; `check_examples.py` independently replays them.
They are useful inputs for stronger filters, not constructions or negative
solver certificates. The beam drops states and is not exhaustive.

To reproduce the bounded heuristic after running the generator:

```sh
g++ -std=c++20 -O3 round-two/six-sorting-1/projected_prefix_barrier/beam.cpp -o scratch/beam
scratch/beam scratch/projected-prefix-barrier/survivor-396-cut24.txt 32 50000 scratch/beam-image.json 0
scratch/beam scratch/projected-prefix-barrier/survivor-396-cut24.txt 32 50000 scratch/beam-inputs.json 1
```

The beam uses one process/thread, approximately 152 MiB and 4--12 seconds.
No unsuccessful heuristic, uncertified SAT result or timeout is a premise
of the prefix barrier. See [PROOF.md](PROOF.md) for coverage and limitations.
