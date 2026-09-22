# Exact illumination of complete multipartite zonotopes

For every complete multipartite graph with nonempty part sizes
`n_1,...,n_k`, `k>=2`, and arbitrary strictly positive edge weights,
its graphical zonotope satisfies

\[
                    I(Z)=I_f(Z)=\sum_{i=1}^k(2^{n_i}-1).
\]

An optimal set of directions is explicit: for every nonempty subset `S`
of a part, take `N*1_S-|S|*1`, where `N=sum n_i`. The sources of an
acyclic orientation determine which direction illuminates its vertex.
A cyclic order of the parts supplies a matching antipodal vertex set,
certifying optimality even for fractional illumination and arbitrary
positive weights.

The proof also characterizes the method: for a connected graph, **every**
sum-zero direction positive on the sources and negative elsewhere
illuminates its orientation vertex, for **every** acyclic orientation,
exactly when the graph is complete multipartite. An induced edge plus
an isolated vertex gives an explicit obstruction otherwise.

- [PROOF.md](PROOF.md): both complete proofs and boundary conventions.
- [SOURCES.md](SOURCES.md): classical inputs, prior two-hub result,
  and search-relative novelty boundary.
- [verify.py](verify.py): exact finite checks from weighted generators
  and supporting cuts.
- [expected.json](expected.json): deterministic output.

From the repository root, using CPython 3.11+ and its standard library:

```sh
python3 discrete_geometry/multipartite_zonotope_illumination/verify.py
```

The JSON output must exactly match `expected.json`, with status `VERIFIED`.
From this directory, verify the source manifest with:

```sh
sha256sum -c SHA256SUMS
```

The checker covers 27 graph types, including all complete multipartite
types on two through six vertices and four seven-vertex cases. It checks
15,628 vertices under three positive weight assignments, 292,404 strict
active supports, 46,884 rational interior steps, and 5,301 antipodal
pairs. A second enumeration tests 71,030 edge orientations directly for
acyclicity. The source-cone characterization is checked on all 771
connected labelled graphs through five vertices, including 701 explicit
obstructions outside the class. Tangent and reversed directions, invalid
parts and nonpositive weights are rejected. Normal and `-O` outputs agree;
tested with CPython 3.11.2.

The universal result is the written proof. There is no solver, floating
point evidence, random sampling, external dataset, or hidden certificate.
Independent review and formal verification are not claimed. Normal fans,
positive-weight invariance, antipodal lower bounds, and the earlier
`K_(2,n)` formula are explicitly credited. Historical priority for the
full-family theorem remains unclaimed. Zero edge weights and arbitrary
graphical zonotopes are outside the exact illumination formula.
