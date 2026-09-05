# Independent review of the ten-cycle anchor sweep

This directory contains reviewer-1's independent audit of the lemma
"Ten moving 3-cycles force a minority matching and four anchor profiles."
The reviewed contribution is a necessary restriction on a hypothetical
Ramsey `(5,5;43)` graph with cycle type `1^13 3^10`; it is **not** a graph
construction, an exclusion of that cycle type, or a new Ramsey lower bound.

`review.py` imports none of the submitted Python modules. It independently:

* reconstructs the 353 unordered-pair orbits of the order-three action;
* enumerates the 98 sorted anchor profiles and obtains 5,599 labeled profiles
  by orbit multiplicities rather than the submission's `4^9` scan;
* checks the four public survivor rows and the degree ranges;
* exhausts all symmetric weight assignments on four minority triangles and
  confirms that the row condition `(1,2,2)` gives exactly the three labeled
  perfect matchings; and
* with `--sweep`, checks every regenerated cube as the exact parent plus its
  27 independently reconstructed units and requires successful DRAT replay
  for every claimed exclusion.

Run the compact public-source audit from the repository root:

```sh
python3 ramsey_r55_order3_ten_cycle_anchor_sweep_review1/review.py \
  --source ramsey_r55_order3_ten_cycle_anchor_sweep
```

For the full review, first run the submitted bounded sweep with one worker in
scratch space and then supply its `sweep` directory:

```sh
python3 ramsey_r55_order3_ten_cycle_anchor_sweep_review1/review.py \
  --source ramsey_r55_order3_ten_cycle_anchor_sweep \
  --sweep /scratch/path/to/sweep --output /scratch/path/to/review_report.json
```

The generated CNFs and DRAT files occupy several gigabytes and are deliberately
not committed. [report.json](report.json) records the completed serial run:
all 98 cube formulas matched their expected construction, 94 were UNSAT with
successful DRAT replay, and precisely indices 64, 65, 67, and 69 reached the
30-second limit. All 94 formula hashes and all 94 regenerated proof hashes
also matched the submitted references. The run used one worker, took 1020.4
seconds, and had maximum child RSS 495,712 KiB.

## Review verdict and boundary

**Accepted for the new refinement, conditional on the preceding four-versus-six
internal-color lemma.** The fresh certificate run verifies the 94 exclusions,
and the independent combinatorial audit verifies that their four survivors
force the stated perfect matching and degree restrictions at every minority
triangle. No survivor is asserted feasible. The reviewed result remains an
intermediate necessary restriction: it neither excludes cycle type `1^13 3^10`
nor constructs a 43-vertex graph or improves the lower bound for `R(5,5)`.

The review rebuilt and completely audited the `r=4` parent formula used by the
94 cubes, but did not rerun the five older DRAT exclusions for internal red
counts 0, 1, 2, 3, and 5. Those are an explicit imported dependency. The
remaining trust boundary includes that preceding result, the unformalized
graph-to-CNF and normalization arguments, CPython, the C++ compiler/runtime,
ordinary hardware, SHA-256, and the external drat-trim checker. The omitted
gigabyte-scale traces, CNFs, and logs remain reviewer scratch state; their
hashes in the compact report are provenance, not standalone proof evidence.
