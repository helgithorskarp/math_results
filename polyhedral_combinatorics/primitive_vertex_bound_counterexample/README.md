# A primitive 12-polytope with 4,352 vertices

The 12-dimensional polytope

```text
y,z,x_0,...,x_9 >= 0,
x_i+(2i+1)y+z <= 100+i(i+1)     (0 <= i < 10)
```

is bounded, simple and **primitive**: deleting any of its 22 facet
inequalities leaves an unbounded intersection. It has exactly 4,352
vertices, exceeding `2^12 = 4,096`.

This refutes the vertex bound in Conjecture 6 of
[Ivanov, arXiv:2607.08944v1](https://arxiv.org/html/2607.08944v1).
It does not refute the illumination conjecture or the paper's illumination
theorem.

More generally, replace 10 by `k>=2` and 100 by `k^2`. The resulting
primitive `(k+2)`-polytope has `2k+2` facets and
`2^(k-2)(k+7)` vertices. The ratio to `2^(k+2)` is unbounded.
At `k=9` it also disproves the conjecture's cube-only equality clause.

- [PROOF.md](PROOF.md): complete proof, explicit facets and deletion rays,
  and the affine-box lifting mechanism.
- [SOURCES.md](SOURCES.md): precise target and attribution of the classical
  facet-wedge construction; search-relative novelty limits.
- [verify.py](verify.py): exact witness checking and separate small-case
  vertex enumeration.
- [expected.json](expected.json): deterministic compact evidence.

From the repository root, with Python 3.11 or newer:

```sh
python3 polyhedral_combinatorics/primitive_vertex_bound_counterexample/verify.py
```

The output must exactly match `expected.json` and report `VERIFIED`.
From this directory, run `sha256sum -c SHA256SUMS`.
Only the Python standard library is needed.

The checker directly tests all vertex inequalities and active-normal ranks,
strict interior and facet points, finite coordinate bounds and deletion
rays for both counterexamples and four small controls. For the four small
cases it separately enumerates every full-rank facet-basis intersection
and compares entire vertex sets. It rejects invalid parameters,
a feasible nonvertex, an infeasible point and incorrect recession rays.
Checks remain enabled under Python `-O`.

The numerical refutation needs only the 4,352 distinct feasible
full-rank vertex witnesses, not an enumeration-completeness assumption.
The exact universal vertex formula follows from the written proof.
No floating-point arithmetic, solver, random input, external dataset or
large certificate is required. This packet has not been independently
peer reviewed or formally verified. No dimension-minimality claim is made.
