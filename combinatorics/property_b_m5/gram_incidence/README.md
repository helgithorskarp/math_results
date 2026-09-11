# Property B: m(5) ≥ 35

Every finite simple 5-uniform hypergraph with at most **34 edges** is two-colorable. The resulting working interval is **35 ≤ m(5) ≤ 51**. See [the proof](proof.md) for the complete reductions, lemmas, attribution, and priority limitations.

The finite proof combines overlap-component constraints, overlap-forest bounds, exact augmented Gram positivity, complete incidence reconstruction, and row inclusion–exclusion. It covers every possible vertex count and every remaining trace class. All 50 stored link bounds are re-proved from complete support and integer-weight enumeration.

## Reproduce

From this directory, with Python 3.11+ and only its standard library:

```sh
python3 verify.py
```

Run without `-O`. The command uses at most two worker processes, recomputes the link bounds and whole-endpoint coverage, runs deterministic controls, and asserts exact agreement with [expected.json](expected.json). Expect several minutes. [reproducibility.json](reproducibility.json) records the measured run and hashes. No solver, external catalogue, large certificate, or unpublished input is required.

The principal files are:

- `realizability.py`: necessary union, forest, and exact Gram tests.
- `graphs.py`: complete graph catalogue with refinement and twin symmetry.
- `envelope.py`: complete integer-box proof of each link bound.
- `exact_union.py`: exact clique-incidence reconstruction and row inclusion–exclusion.
- `coloring.py`, `verify_coverage.py`: every trace branch and structural closure.
- `certificates.json`: 50 compact proposed link bounds, all recomputed.
- `audit.py`: controls using principal minors, another graph canonicalizer, column counting, and direct subsets.

The source imports the existing general-bound modules in the parent directory and its `link_envelopes` and `incidence_forests` subdirectories. Those files are preserved unchanged. The new theorem does not rely on the preceding numerical lower bounds; the proof identifies the reused general lemmas explicitly.

This is an exact computer-assisted proof with written completeness arguments. Controls are not independent peer review or proof-assistant formalization. The exact value of m(5), 35-edge existence, and an improved upper construction remain open here. No novelty is claimed for the classical linear-algebra, inclusion–exclusion, or forest principles individually.
