# The full signature conjecture reduces to subcubic cores

The sharp cyclomatic conjecture for line-graph signature is equivalent to
its restriction to connected simple graphs whose degrees are all two or
three. Arbitrary high degrees and pendant forests introduce no additional
case beyond that restricted problem.

For a connected graph `G` of order at least two, let `ell` be its number of
leaves and `a=sum_v max(deg(v)-3,0)`. The explicit construction returns a
subcubic core `H` with the identities below. Here `c=|E|-|V|+1` and the
inertia tuple counts positive, zero and negative eigenvalues, in that order.

```text
|V(H)| = |V(G)| + 4a + 9ell,
c(H)   = c(G) + 2ell,
In(A(L(H))) = In(A(L(G))) + (2a+6ell, 0, 2a+5ell).
```

It preserves both nullity and the exact conjectural slack
`2 sig(A(L(G)))-c(G)-1`. For inputs of minimum degree at least two it
preserves cyclomatic number and signature separately.

The [proof](PROOF.md) gives an explicit four-edge vertex-splitting congruence,
then uses Paone's known zero-response C4--C5 module to close each leaf.
Combining this with the existing
[parity-kernel theorem](../line_graph_signature_subcubic_parity_kernel/THEOREM.md)
makes one inequality on four-residue cubic pseudokernels equivalent to the
**unrestricted** conjecture. Every core with cyclomatic number `c>=2` also
has a subcubic representative on at most `15c-14` vertices with the same
signature and nullity. The equivalent core problem can instead be restricted
to any prescribed minimum girth.

This is a complete author proof awaiting independent review. It is a
reduction theorem; the sharp inequality remains open. It does not exclude
any new cyclomatic number or supply a counterexample. The leaf step changes
`c`, so the `15c-14` bound for minimum-degree-two inputs is not a bound in
the original `c` for unrestricted graphs. See [sources and scope](SOURCES.md).

## Reproduce

Python 3.11.2, standard library only. From this directory:

```sh
python3 check.py > /tmp/signature-core-audit.json
cmp /tmp/signature-core-audit.json AUDIT.json
PYTHONHASHSEED=271828 python3 -O check.py > /tmp/signature-core-audit-optimized.json
cmp /tmp/signature-core-audit-optimized.json AUDIT.json
sha256sum -c SHA256SUMS
```

Expected audit SHA-256:

```text
d870be3d1db4f1f7ee744d966cb9fc2504fbb79acde5e93c6332a381b7e6be1e
```

The [run record](RUN.json) gives about 19 seconds and 23 MiB or less for
each run on the research host. The two outputs are byte-identical.

The exact checks include:

- All 771 connected labeled graphs of orders two through five: 320 split
  moves and 816 leaf closures, with complete independent edge-trace replay.
- Direct shifted-matrix inertias of all 771 constructed cores; 147 additional
  literal line-graph inertia calculations on outputs.
- All 755 non-cycle output cores and their compact parity representatives,
  of order up to 77; exact equality of the conjectural slack at every step.
- 432 explicit split congruences, including 312 singular small inputs and
  uneven neighbor partitions through degree ten.
- 192 residue assignments, including every assignment on both cubic
  two-vertex pseudokernels, and period-four checks on every realization.
- Fourteen negative controls for invalid graphs, partitions, loop paths,
  traces, and corrupted matrix certificates.

The module is checked by rational symmetric elimination, integer
characteristic-polynomial signs, Bareiss determinant and a literal inverse
column. Its inertia is `(6,0,5)`, determinant `-8`, and root cofactor zero.
Integer characteristic polynomials independently check the small input
inertias. These are author audits, not independent peer review.

## Use the constructor

```python
from reduction import make_graph, to_core, residue_representative

star = make_graph(5, [(0,1), (0,2), (0,3), (0,4)])
core, trace = to_core(star)
assert (core.order, len(core.edges), core.cyclomatic()) == (45, 52, 8)
compact, paths = residue_representative(core)
```

[reduction.py](reduction.py) constructs graphs and move traces without
spectral choices. [check.py](check.py) rebuilds the moves separately and
checks matrices from edge definitions. No predecessor code, solver, external
dataset or large generated certificate is required. The output graph has
linear size in the input's vertices and edges; the readable implementation
rescans its graph and is not claimed to have linear running time.
