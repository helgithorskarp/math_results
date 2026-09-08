# A complete hereditary-core exclusion for good43

**Every 26-vertex induced subgraph of a hypothetical good43 contains an
induced P5 or its complement.** Thus the entire 43-vertex class with a
26-vertex core avoiding both patterns is excluded, with all other edges
unrestricted. No symmetry or fixed neighborhood is assumed.

The proof determines the exact maximum order, **25**, of a graph avoiding
both patterns and having clique and independence numbers at most four.
The unique graph attaining 25 is C5[C5]. More generally, the checked
clique/independence capacity table for caps 1 through 4 is

```text
1  2  3  4
2  5  7 10
3  7 11 16
4 10 16 25
```

See [PROOF.md](PROOF.md) for the complete induction and its imported
Fouquet decomposition and Strong Perfect Graph Theorem premises.
[TABLE.json](TABLE.json) contains every weighted maximizing vector;
[WITNESSES.json](WITNESSES.json) contains literal attaining graphs for all
16 cells. The 25-vertex graph is a boundary witness, not a target candidate.
Its extension to 43 is not attempted or decided.

Two direct consequences for every good43 are a joint P5/complement-P5
vertex-deletion number of at least 18, and four disjoint induced copies
chosen from these two patterns. These are global structural constraints.
There is no solver-runtime estimate or carrier-size comparison.

## Reproduce

CPython 3.11.2, standard library only, from the repository root:

```sh
python3 -B ramsey_r55_path_complement_core_exclusion/reproduce.py
```

This regenerates the table and all graphs, then runs producer-free checks
and physical-interface controls in normal and optimized Python. The
arithmetic checker visits all 59,049 possible weight vectors and compares
every extremal vector. Dense graph verification checks every relevant
subset, including all 53,130 five-sets of C5[C5]. No solver, graph catalog,
external executable or network input is required for replay. The written
global argument and imported theorems are not formally verified by replay.

## Use the physical interface

Provide JSON fields `n:43`, `red_bits_hex`, and a sorted 26-element `core`.
The red edge word has exactly 226 lowercase hex digits, with low bits
assigned to lexicographic pairs `(0,1),(0,2),...,(41,42)`; its unused high
bit must be zero. Every absent red edge is blue.

```sh
python3 -B ramsey_r55_path_complement_core_exclusion/interface.py candidate.json
python3 -B ramsey_r55_path_complement_core_exclusion/verify_certificate.py candidate.json certificate.json
```

Pass the first command's `certificate` field as the second command's
certificate file. An induced-path certificate only shows the supplied
core is outside this excluded class. A monochromatic-five certificate
directly rejects the full graph. The interface does not search all possible
26-sets or produce a full target solver.

This is a complete structural class decision. **No good43 or Ramsey-bound
improvement is established; all 2,189,178 packing tasks remain undecided.**
No claim of historical novelty is made for the classical method or the
iterated-cycle graph. See [VALIDATION.md](VALIDATION.md) for exact checks
and limits and [HANDOFF.md](HANDOFF.md) for integration scope.
