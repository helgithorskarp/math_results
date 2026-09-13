# Induced-path/module coexistence: first-gate boundary

**The first whole-good43 gate is missed.** No good43, class exclusion, or
finishable structural reduction was obtained. One final contracted pass
remains, with an approach correction required.

The unchanged published seven-defect graph in `control43.edges` satisfies
the full simultaneous system below:

- Every induced subgraph on at least 36 vertices is prime.
- Every induced subgraph on at least 28 vertices has no proper module of
  size at least three.
- Every 26-set contains an induced P5 or complement-P5.
- Every 18-subset of every colour neighbourhood contains an induced P5
  of that colour.

This proves consistency of those accepted necessary conclusions on a
physical order-43 graph. It does **not** refute any accepted theorem or
decide good43 existence. The graph still has its seven monochromatic
five-sets and violates an omitted same-colour triangle-common-neighbour
bound. [PROOF.md](PROOF.md) defines the precise necessary system Q and
proves the complete coverage joins. It is not the full Ramsey system.

The predeclared disconnected/spanning path-component partition remains
unclosed. The control has a connected spanning path hypergraph, so it does
not disprove a future theorem excluding the disconnected class. No claim
of a new graph, construction basin, Ramsey bound or paper-scale advance is
made. [DEPENDENCIES.md](DEPENDENCIES.md) preserves all imported boundaries,
including the critical-graph classification behind the neighbourhood input.

## Reproduction

Use CPython 3.11.2 and g++ 12.2.0 with C++17, no external packages or solver:

```sh
python3 -B ramsey_r55_path_module_coexistence_boundary/reproduce.py /tmp/new-path-module-replay
```

The output path must be new and outside the source directory. Expected:
`REPRODUCED_PATH_MODULE_COEXISTENCE_BOUNDARY`, with `first_gate_met=false`
and `new_good43_decisions=0`. All checked JSON bytes must match
[EXPECTED.json](EXPECTED.json).

The C++ program exhausts all 196,081,820 rooted module-subset occurrences.
The separate Python checker uses a different complete intersection
algorithm, with 135,790 extents, to verify the full deletion statements.
It checks all 710,315 literal path-cover records and scans every five-set
independently of the producer's path-recognition method. This is same-author
algorithmic separation, not independent peer review or formalization.

The regenerated binary coverage certificate has 5,682,520 bytes and SHA-256
`cbbc3cb64905648f5ec05960b08ac1b1f67c3d1af0a509d9ae7531306a971801`.
It and all binaries remain outside Git. The exact graph, source, compact
expected results and hashes suffice for offline replay. No prior campaign
computation is restarted and no Discovery Net claim is submitted.
