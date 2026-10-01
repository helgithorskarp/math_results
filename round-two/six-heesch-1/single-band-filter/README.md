Actual agent **six-heesch-1**, role **researcher**.

This directory checks all37 distinct P192 single-band stretches defined in
the [proof](proof.md). Exactly three admit three complete integer disc coronas;
each is an explicit periodic plane tiler. For the other34, the reader proves
an integer-prefix obstruction at depth2 or3. It also excludes integer-grid
plane tilings for those34. Their unrestricted Heesch numbers are not determined.
This is a bounded construction-family filter, not a new Heesch record.

Run with standard-library CPython3.11 or later, one process:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O check.py
```

No solver or network is required. The output must match [expected.json](expected.json).
The checker reconstructs the family, all admitted first surrounds, the remaining
second rejection, all2240 literal corner certificates, three periodic quotient
tilings, their three disc coronas and seven damaged controls. Enumeration guards
raise exceptions and never return a mathematical negative.

[upper.py](upper.py) is byte-identical to the same-author independent geometry
and cover reader published with the [P192 exact-three proof](../p192-exact-three/proof.md)
at commit37e77d6c9e113673356b0c3a96cae5021a7811a2. Its SHA256 is pinned
in [input.json](input.json). The new classification uses integer enumeration;
it does not import that tile's real-phase reduction or numeric contact atlas.
The signed-permutation lower checker uses direct whole cells and a lattice quotient.
Same-author algorithm independence is separate from independent peer review.

Discovery used PySAT1.8.dev24/Glucose4 assumption cores to choose a small subset
of already checked exclusions. Those cores are hints, not proof premises:
the reader independently replays every retained corner certificate and verifies
each negative by complete solver-free enumeration. Partial pair-atlas searches
only omit exclusions and weaken the necessary model.

Proof status: exact computer-assisted author proof, unformalized;
independent review pending. The finite-five square-polyomino frontier remains open.
