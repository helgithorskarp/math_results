# Failed triangle-support gate: the critical core does extend

An exact 24-vertex Ramsey(4,5) graph containing an induced Paley17 graph
**survives** the proposed necessary-extension test. Therefore that test
does not exclude good43 graphs with an edge lying in no triangle of its
own color. The global 43-vertex branch remains open. This is a failed
research gate, not a target, task decision, or global search reduction.

The [witness](WITNESS.json) contains the complete physical edge word,
an explicit isomorphism of its core to the quadratic-residue Paley graph,
and a deterministic 26-vertex partial graph with no monochromatic five
and a red edge having no common red neighbor. The latter is a transport
of the same surviving extension, not another search phase. It does not
meet the 43-vertex target.

## Verification

With CPython 3.11.2 and its standard library, from the repository root:

```sh
python3 -B ramsey_r55_triangle_support_gate_failure/reproduce.py
```

This runs no solver. It verifies all source hashes, checks the witness in
normal and `-O` Python modes, and compares both outputs to [CHECK.json](CHECK.json).
The independent checker tests all 10,626 four-sets and 42,504 five-sets of
the extension, all 65,780 five-sets of the partial graph, the core's graph6
and Paley labels, the two-vertex transport, and the marked triangle-free
edge. It independently reconstructs every clause of the 140-variable,
6,958-clause necessary-extension formula and checks the witness against it.
Four corrupted witnesses are rejected. No catalog-completeness assertion
or solver soundness is needed to verify this explicit counterexample.

The source of the single original solver experiment is [decide.py](decide.py).
An optional replay requires the pinned packages in `requirements.txt`:

```sh
python3 decide.py /tmp/fresh-r55-extension-run
```

The output path must not exist. This performs one Glucose3 call, with the
original one-million-conflict and 300-second limits. The recorded run was
SAT after about 1.14 seconds; [RESULT.json](RESULT.json) preserves the exact
telemetry and formula hash. No longer cap, alternate backend, new codegree
threshold, or strengthened subsystem was tried. Expected truth of the
preserved graph is established by `check.py`, independently of replaying
the solver or reproducing its telemetry.

See [PROOF.md](PROOF.md) for the complete global reduction and its failed
step. The 17-vertex author input is attributed there; no historical novelty
for its 24-vertex extension is asserted. The earlier h3909 connectivity
theorem is unchanged and has now been independently accepted at h3917.

**No good43 is established. All 2,189,178 packing tasks remain undecided.**
