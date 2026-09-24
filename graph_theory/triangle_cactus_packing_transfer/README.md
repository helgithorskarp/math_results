# Linear fractional-packing loss for triangle-cactus families

For every fixed finite family F of graphs whose nontrivial blocks are
edges or triangles, and every fixed neighborhood-diversity bound t,

```text
nu*_F(G) - nu_F(G) <= K(t,F) |V(G)|.
```

Class sizes may be arbitrary. Patterns may have bridges, branching trees
of triangles, disconnected components, and isolated vertices; each pattern
must have an edge. Copies are non-induced and packing is by edges.
Every feasible fractional packing rounds with this loss, with separately
below-input counts for each vertex-class-typed pattern.

The [proof](PROOF.md) transfers the accepted
[balanced triangle-and-edge theorem](../tuza_bounded_type_linear_rounding/PROOF.md)
to a whole class of patterns. A partition-constrained rounding step labels
and orients its base cliques. Greedy assembly then charges losses to missing
blocks and collisions at articulation vertices. Surviving partial copies
need not remain balanced: their demands are dominated by original parent
role counts.

If C(t,1), D(t,1) are the base theorem's constants, q is the largest pattern
order, and B=sum_F b(F)t^|V(F)|, a valid coefficient is

```text
K(t,F) = C(t,1) + B [2D(t,1) + 80 + q].
```

The proof also states a conditional transfer for larger clique blocks.
Its required base theorem is **not** asserted beyond triangles here.

The [independent review](../triangle_cactus_packing_transfer_review1/REVIEW.md)
accepted the proof at source commit
`bd5c50a327e21ab32193da113e55012f5b23c5d2`, with one wording correction:
the sharpness example uses complete graphs of **even order**. That correction
is incorporated here; the theorem and audit are unchanged. The base
constants remain existential through Keevash's design theorem. The package
implements the new elementary steps, not a universal design constructor or
a practical algorithm for all hosts. Longer cycles, two-vertex gluing, K4
blocks, and growing t or F remain outside the unconditional result.
See [dependencies and novelty limits](SOURCES.md).

## Reproduce

Python 3.11.2, standard library only. From this directory:

```sh
python3 check.py > /tmp/triangle-cactus-audit.json
cmp /tmp/triangle-cactus-audit.json AUDIT.json
PYTHONHASHSEED=271828 python3 -O check.py > /tmp/triangle-cactus-audit-optimized.json
cmp /tmp/triangle-cactus-audit-optimized.json AUDIT.json
sha256sum -c SHA256SUMS
```

Expected audit SHA-256:

```text
b7ca4ff56c74e2bcd1a27818f2e8637e7092c8f69793342ef8a3a9f9de56d62a
```

[RUN.json](RUN.json) records measured time and memory. The normal run takes
about 14 seconds and 25 MiB on the research host. Exact rational arithmetic
and ordinary Python integers are used throughout; no solver or dataset is
needed. Checks remain enabled under optimized Python.

The finite audit includes:

- 2,304 exhaustive small rounding inputs, 27 retained-row stress inputs,
  and 7,320 replayed floating-variable moves across all rounding fixtures.
- Eight labeling/orientation cases, including repeated classes, unequal
  classes, zero counts, nonintegral targets, actual trimming, and slack.
- Six assembly fixtures and an end-to-end two-pattern fixture: 8,199
  assembled copies and 76,008 checked edges **across separate fixtures**.
- Four explicit orbit-averaging checks totaling 1,008 labeled embeddings.
- Ten rejection controls, including invalid one-hot constraints, a corrupted
  rounding trace, two-vertex gluing, cyclic block incidence, reused edges,
  impossible isolated roles, and noninjective output.

Four larger fixtures on 243-vertex hosts each assemble 1,944 patterns.
The chain-with-bridge fixture has 324 incompatible request/candidate pairs;
the disconnected fixture has 230,850. A fixture with unequal block deficits
returns 390 of target 486 copies, exercising actual request deletion.
The separate-class fixture has class sizes 3,5,8,13,21,34,55,89.

The end-to-end family fixture starts with a full, exactly balanced base
profile on K27: 54 triangles and 189 slack edges. It has fractional targets
18 bowties and 18 triangles, rounds labels/roles, and outputs six bowties
plus 18 triangles with 90 distinct edges. This is a valid illustrative
rounding, not an optimum or an efficiency guarantee.

[rounding.py](rounding.py) constructs exact option-rounding traces;
[assembly.py](assembly.py) constructs injective pattern copies;
[fixtures.py](fixtures.py) generates compact affine inputs; and
[check.py](check.py) replays moves without the constructor's linear algebra,
then verifies every output edge from the pattern definition. These are
finite author checks, not independent peer review or a computational proof
of the imported all-order design theorem.
