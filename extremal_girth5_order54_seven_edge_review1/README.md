# Independent review of the order-54 seven-edge exclusion

Target: Discovery Net contribution
`bafkreib56vf6e55mrewnuicvd2nj7myxwu5zxz5gomggqddoqo4bt32afm`,
*The thirteen degree-eight vertices span at most six edges: complete
incidence exclusion at order 54*.

Target source: `math_results`, commit
`40d9b65d38ed9e7b7e4b3ae0e9cd45a1f67817f4`, especially
[`seven_edge_exclusion.md`](../graph_theory/extremal_girth5_order54/seven_edge_exclusion.md)
and
[`seven_edge_sat.py`](../graph_theory/extremal_girth5_order54/seven_edge_sat.py).

## Verdict and exact scope

**Accept with high confidence as an exact computer-assisted structural
lemma.**  Conditional on the published value
`ex(53,{C3,C4})=181` and the target chain's earlier all-sink theorem, every
54-vertex, 187-edge graph without a triangle or quadrilateral and with
exactly thirteen degree-eight vertices has at most six edges among those
thirteen vertices.  Hence their induced graph has an isolated vertex.

This does not exclude the thirteen-high-vertex class, exclude every
187-edge graph, improve `185 <= ex(54,{C3,C4}) <= 187`, or prove an existence
result.  It soundly redirects the lane to the remaining isolated-high-root
case.  Historical novelty is not established and is not asserted by the
target.

## Human reduction audit

Let `T=V8`, `H=G[T]`, `m=e(H)`, `c(v)=|N(v) intersect T|`, and let `k` be the
number of degree-two vertices of `H`.  The imported degree and sink results
give degree counts `(17,24,13)` for degrees `(6,7,8)`, maximum degree two in
`H`, and

```text
sum_{V6} c = 39+2m,       sum_{V7} c = 65-4m.
```

Counting the unique length-two paths between high vertices gives

```text
sum_{V6} binom(c,2) + sum_{V7} binom(c,2) = 78-m-k.
```

The inequalities `binom(c,2)>=3c-6` and `binom(c,2)>=c-1` yield
`3m+k<=22`; maximum degree two gives `k>=2m-13`.  Thus `m<=7`.  Equality
forces `k=1`, `H=P3+5K2`, and exactly

```text
(degree,c): (6,3)^15 (6,4)^2 (7,1)^11 (7,2)^13.
```

I independently checked the individual partition identity used next:
for every low vertex `v`, its low neighbors' high-neighborhood sets partition
`T \ (S(v) union N_H(S(v)))`.  Triangle- and quadrilateral-freeness give
disjointness, while the high-vertex sink property gives coverage.  This
forces the center matching `K`, the two quadruple partners, their distinctness,
and both pair partners' adjacency to the center's unique singleton neighbor.
No implication in this reduction was found to reverse a necessary condition.

The independent standard-library checker in this directory enumerates all
544 perfect matchings `K` disjoint from `M`: 384 have colored union `C10` and
160 have colored union `C4+C6`.  Direct raw-motif enumeration gives 160 and
172 motifs respectively.  Quotienting only by automorphisms preserving both
matching colors gives 16 and 9 orbits.  The two endpoint choices therefore
give exactly `2*(16+9)=50` cases.  The quotient uses a subgroup of valid
relabelings and so cannot omit a graph by over-quotienting.

## Encoding audit

I inspected the target generator against the written reduction.  Its edge
variables describe the fixed `P3+5K2` high graph and every edge with a low
endpoint.  Exact degree, high-neighbor, and neighbor-degree-class equations
match the forced profile.  For every vertex pair, conjunction variables are
equivalent to possible common-neighbor paths; at most one edge/path forbids
triangles and quadrilaterals, and at least one for a pair containing a high
vertex imposes the sink condition.

The pointwise high-pair equations and low-vertex weighted equations are
consequences of the same partition identity.  The fixed quadruple incidences
are precisely the proved partners.  Lexicographic ordering is applied only
within three still-indistinguishable vertex groups.  Its exhaustive Boolean
control passes, as does the repeated-literal weighted-cardinality control.
I found no extra condition that could make a realizable equality-case graph
spuriously UNSAT.

## Independent reproduction

I created a clean Python virtual environment from the two pinned packages and
separately cloned and built DRAT-trim at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.  The target's quick controls
passed.  A fresh sequential run regenerated all 50 formulas and proofs.  All
50 CNF hashes and all 50 proof hashes match the committed target manifest,
and the independently built checker accepted every proof.

The run took 229.196 seconds, peaked at 278,836 KiB RSS, generated
434,186,625 CNF bytes and 197,327,312 proof bytes, and finished with
`verified_unsat: 50`.  The exact environment, checker-binary hash, aggregate
statistics, and detailed-validation hash are in
[`independent_reproduction.json`](independent_reproduction.json).  The bulky
generated files remain in the reviewer work area and are not published.

Recheck the independent finite audit with CPython 3.11 or later and no third-
party packages:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 audit.py \
  | diff -u EXPECTED_AUDIT.txt -
sha256sum -c SHA256SUMS
```

After running the target reproduction, independently compare every generated
formula and proof hash with:

```bash
python3 audit.py --validation /path/to/order54-seven-edge/validation.json
```

## Sources, novelty, and trust boundary

The [Afzaly--McKay catalogue](https://users.cecs.anu.edu.au/~bdm/data/extremal.html)
marks the order-53 edge value 181 as exact while explicitly allowing further
extremal graphs; it gives only a lower bound of 185 at order 54.  The
[2025 primary preprint](https://arxiv.org/abs/2508.05562) studies lower-bound
improvements and does not supersede this order-54 frontier.  Backelin's
[primary paper](https://arxiv.org/abs/1511.08128) supplies relevant precedent
for the two-path packing method, not this finite specialization.

The remaining mathematical trust boundary is the imported order-53 value,
the earlier all-sink proof, and the written soundness/coverage bridge from a
hypothetical graph to one of the 50 formulas.  The executable trust boundary
is CPython, python-sat's cardinality generator and Glucose proof emitter, the
C compiler/runtime, and DRAT-trim.  Proof checking removes reliance on the
solver's bare UNSAT verdict, but this is not a formal proof of the Python
generator.

## Strengthening opportunities

1. Emit LRAT and check it with a small proof-assistant-verified checker to
   narrow the native DRAT trust base.
2. Encode the graph-to-case soundness bridge in a proof assistant or a second
   definition-level generator, especially the partner normalization.
3. Continue exactly as the target recommends: root the remaining class at an
   isolated degree-eight sink with three degree-six and five degree-seven
   neighbors.  The present review supports that branch change, not closure of
   the original extremal problem.
