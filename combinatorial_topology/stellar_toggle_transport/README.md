# Stellar transport of optimal toggle words

A stellar subdivision of any finite simplicial complex preserves winnability
of its augmented face-lattice toggle game. It also preserves the existence of
a word attaining every face's Mobius multiplicity lower bound, hence a word
optimal for all nonnegative move costs.

If the subdivided face has s vertices, replace each affected move by a
2^s-1 move local word. For an optimal input the new minimum length is

    ell(K') = ell(K) + (2^s-2) sum_{H superset sigma} |mu_K(H)|.

The compiler applies without purity or shellability. Explicit optimal words
for the projective-plane and torus seeds give **every forward stellar refinement
of those seeds** an optimum of 2E+1 moves. Arbitrary surface triangulations
and reverse stellar moves remain outside this result.

- [Full proof and barycentric consequence](PROOF.md).
- [Compiler](transport.py) and [independent exact verifier](verify.py).
- [Surface certificates](seeds.json) and [expected evidence](expected.json).
- [Primary sources and novelty limits](REFERENCES.md).

From the repository root, with CPython 3.11+ and only its standard library:

```sh
python3 combinatorial_topology/stellar_toggle_transport/verify.py
python3 -O combinatorial_topology/stellar_toggle_transport/verify.py
```

Both commands must print the identical JSON in expected.json with status pass.
The verifier uses explicit checks that remain active under `-O`. The proof of
the all-complex theorem is mathematical; the bounded checks validate the
implementation, certificates, and failure controls, not an inference from samples.

The suite covers all 167 nonvoid complexes on four available labels (ghost
labels allowed), unrestricted game BFS on 228 small instances, 2564 stellar
transports including 1264 nonoptimal input words, and 170 barycentric cases.
It checks 35100 Mobius values, 976432 carrier-state entries, 54422 legal moves,
36 stages of mixed subdivisions, and nine deliberately invalid inputs/words.
The producer uses integer masks and the upper Mobius recurrence; replay uses
sets of faces and alternating coface sums. Barycentric output is independently
compared with the complex of strict chains. Runtime is recorded in the campaign
report; no external data, solver, floating point, or hidden dependencies are used.

`seeds.json` encodes each face as a list of vertex labels, with `[]` the empty
face. The compiler encodes it as a nonnegative integer bit mask. The new lattice
top is always implicit, including when the input is a simplex.

Manifest verification, from this directory:

```sh
sha256sum -c MANIFEST.sha256
```

The exploratory greedy rules failed and are not part of the compiler. No
independent peer review or proof-assistant formalization is claimed.
