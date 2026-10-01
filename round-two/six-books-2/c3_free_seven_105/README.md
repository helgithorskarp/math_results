# Ordinary Book graphs: the 105-edge C3 branch

**six-books-2, researcher.** A complete exact enumeration excludes valid 22-vertex graphs with 105 red edges, maximum red degree ten, an automorphism of cycle type 3^7 1, and fixed red degree nine. Combining this with graph lemmas 7526, 8012 and 8915 gives **at most 102 red edges**, and the prior edge floor 97 leaves **only 99 or 102**, for this cycle type. The other cycle types and the full Ramsey endpoint remain open. Independent peer review is pending; the combinatorial completeness bridge is not formalized.

Read [PROOF.md](PROOF.md) for the exact hypotheses, reduction, coverage, primary literature and directed dependencies. [expected.json](expected.json) is the compact deterministic manifest.

From the repository root, with Python **3.11 or later**:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 round-two/six-books-2/c3_free_seven_105/reproduce.py \
  --work scratch/c3-free-seven-105
```

Use a fresh work directory. `--resume` preserves completed primary root/incidence boundaries and redoes the independent audit. Each bounded incidence, outside-graph or completion phase has a 30-second budget; an incomplete phase aborts the exclusion. Do not increase a limit or interpret incomplete output as nonexistence. Runtime outputs, full incidence tables and checkpoints stay in the selected scratch directory.

The source needs **only the Python standard library**, with no solver, downloads or proof corpus. The only fixed graph input is the 462-byte primary-literature fixture included here. All domain sets and outside graphs are regenerated. Typical total runtime is several minutes on one CPU; peak memory was below one GiB in the author run, within the assigned two-GiB process scope.

Expected final status is `REPRODUCTION_PASS`, with:

- seven degree placements and twenty local classes;
- 2032 incidence representatives and seventeen outside degree profiles;
- all 262144 outside cross words examined;
- 25540320 completions considered and independently rejected;
- zero valid completions;
- 95 graph controls and nine damaged-table rejections under normal Python and `-O`.

`local_roots.py`, `incidence.py` and `complete.py` form the producer. `independent.py` imports none of them: it independently generates degree compositions, local groups, column domains, pair joins and weighted outside graphs, then checks all completions without forced-edge cuts. `blocks.py` and `verify.py` provide two graph constructors and literal positive controls; those helpers and the primary fixture are reused from the preceding 108-edge artifact. Reproducing that earlier result is not part of this new claim.

The published files are compact source, this proof, documentation, a small fixture and expected summaries. Generated tables, profiling output, solver packages, private ledgers, keys and other campaign files are not part of the artifact.
