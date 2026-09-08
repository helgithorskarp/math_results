# Global connectivity constraint for complete good43 branches

The completed gate proves kappa = delta in both colors for every
hypothetical good43. It rules out all separators of size k below the
same-color minimum degree, including the previously unresolved global
cases k = 19,20,21,22,23. It does not classify all minimum cuts or
force minimum degree at least 19.

For disjoint nonempty physical vertex sets A,B, put
k = 43-|A|-|B|. If every vertex has degree at least k+1 in color c,
at least one A--B edge must have color c. For red variables x_uv this
is a disjunction of 43 negated degree guards and the positive cross
edges; for blue it uses blue-degree guards and negative cross edges.

Example from the contribution directory:

```sh
python3 -B guarded_cut.py 0,1,2,3,4,5,6,7,8,9,10 11,12,13,14,15,16,17,18,19,20,21,22,23 --color red
```

This outputs the k=19 cut with guards degree >=20 and 143 crossing
edge literals. The contract is symbolic JSON, not numeric CNF. A
consumer must give each degree predicate its actual counting semantics
or derive it from existing constraints. A claimed lower bound alone is
not evidence that a guard is true. The output is a valid implication
under complete good43 constraints, not a contradiction certificate for
an arbitrary partial coloring.

The theorem applies to every labeling of all 2,189,178 h3887 packing
tasks. It changes neither task IDs nor their decision status, and makes
no timing, carrier-size, or search-tractability claim. A physical solver
integration or decision is a separate phase owned by team-r55-1.

For concrete decision leverage, the supplied `UNEXTENDABLE_CORE.json`
is a good23 that cannot accept even one new vertex. Its literal induced
core excludes all completions on twenty further vertices, leaving 650
otherwise unrestricted edge variables. It does not purport to cover
every good43 or to coincide with a complete packing task. The complete
side-word obstruction is replayed by `verify_core.py`.

Reproduce the full result using `reproduce.py`. The sibling dependency
`ramsey_r55_separator18_classification` is pinned to source commit
`4b6455643c0dba1222231b66c1dedca699cf03e9`; its 19-entry source manifest
has SHA256
`1f3d9a3b32f5c5574846fb1c0a6a753922e2391445e6e06934d0be1e4d69580b`.
The delivery snapshot must preserve both sibling directories. Exact
source commit, graph reference, snapshot hashes, and receiving replay
receipt are recorded in the external immutable delivery record after
publication, so this source does not contain a self-referential commit.

The prior h3897 and h3887 immutable handoffs are preserved. No good43
is established. Independent algorithms here mean separate enumeration
routes, not independent researchers or peer review.
