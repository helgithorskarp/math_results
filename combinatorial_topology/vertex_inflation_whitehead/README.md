# Vertex inflation cannot create a new Whitehead counterexample

For a finite simplicial complex K of dimension at most two, replace each
vertex v by m_v>=1 independent copies, lifting every face in all choices.
Let I be the resulting vertex inflation and S the vertices with m_v>1.

The following local conditions are equivalent to a collapse of I,
preserving the original K, onto K together with a graph:

1. Every link of a vertex in S is a forest.
2. Every edge with both endpoints in S lies in at most one triangle.
3. No triangle has all three vertices in S.

The same collapse sequence restricts to **every subcomplex** Y of I,
leaving Y intersect K together with a graph. Consequently, if I is
aspherical, every nonaspherical subcomplex Y already has a nonaspherical
component in Y intersect K. In particular, an aspherical inflation has
the Whitehead subcomplex property exactly when its base does.

A failed condition gives an explicit spherical obstruction: a suspended
link cycle or an octahedral sphere. Thus I is aspherical exactly when K
is aspherical and the three conditions hold. All disconnected statements
are componentwise; arbitrary positive multiplicities are covered.

The absolute asphericity criterion also follows from the classical
Björner--Wachs--Welker inflation formula. The contribution here is the
relative collapse, its restriction to arbitrary subcomplexes, and
Whitehead inheritance. This is a modest structural refinement, with no
claim to solve Whitehead's general conjecture or decide base asphericity.
No independent review of this note is yet available.

See [PROOF.md](PROOF.md) for the complete elementary proof and
[SOURCES.md](SOURCES.md) for prior art and the novelty boundary.

## Reproduce the finite checks

Python 3.11+; standard library only. From the repository root:

```sh
python3 combinatorial_topology/vertex_inflation_whitehead/verify.py
```

From this directory:

```sh
python3 -O verify.py
sha256sum -c MANIFEST.sha256
```

Both Python commands must match [expected.json](expected.json) exactly.
The script works from any directory. `--emit` prints fresh evidence
without comparison; it does not modify the reference file.

The deterministic validation covers all complexes on one through four
labelled vertices with multiplicities in {1,2,3}, and all five-vertex
2-complexes with complete 1-skeleton and multiplicities in {1,2}:

- 42,185 cases, with 18,378 admissible inflations;
- 56,328 elementary collapse pairs checked by generic replay;
- 23,807 signed integral spherical obstruction certificates;
- a separate boundary-matrix rank computation over F_2 in every case;
- all 403 and 697 subcomplexes of two admissible inflated disks;
- three examples separating the local conditions, eight rejection
  controls, and identity, empty-complex and torus checks.

Evidence payload SHA-256:

```text
43aa2156df34d01030fca06adaca12119a720395e7e0f2138fefee3400a29ae7
```

The universal theorem rests on the written proof. Computation validates
finite instances and certificate handling; it does not test arbitrary
base asphericity. The code uses integer arithmetic, no solver, random
search, floating-point inference or external data. Certificates are
generated and checked in memory and hashed entry by entry, avoiding a
large enumeration dump. The independent boundary method is an additional
check by the same author, not independent peer review.
