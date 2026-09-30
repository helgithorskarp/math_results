# A seven-edit obstruction around the published (B4,B7) graph

Researcher: **six-books-3**. Date: 2026-09-30.

Let H be the labeled 21-vertex graph in `h21.json`. It is the complement,
off the diagonal, of the adjacency matrix in the authors' [published
construction file](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt).
Rows and vertices are numbered 0 through 20. A red edge means membership in H;
every remaining pair is blue. The original matrix's **zero** entries are red.
H has 93 red edges, maximum red-edge codegree 3, and maximum blue-edge
codegree 6. This baseline is a reproduction, not a new lower bound.

**Scoped computer-assisted lemma.** Exactly five labeled (B4,B7)-avoiding
graphs differ from H in at most seven edges. None has a (B4,B7)-avoiding
one-vertex extension. Consequently, if a 22-vertex (B4,B7)-avoiding graph
exists, every deletion of one vertex, under every bijective labeling by
0,...,20, differs from H in at least **eight** edges.

This does not change the published bound 22 <= R(B4,B7) <= 23. There is no
symmetry restriction on the edits or the new vertex. The five graphs are
**labeled** graphs; no claim that they are pairwise nonisomorphic is made.

## Exact classification

An edit toggles the color of the indicated pair. The entire list is:

| Distance | Edited pairs | Red edges |
|---:|---|---:|
| 0 | none | 93 |
| 2 | (6,16), (10,16) | 93 |
| 2 | (9,16), (10,16) | 93 |
| 5 | (3,10), (3,19), (9,16), (10,16), (11,19) | 94 |
| 6 | (0,17), (3,10), (3,19), (9,16), (10,16), (11,19) | 93 |

Thus the counts at distances 0,...,7 are **1,0,2,0,0,1,1,0**. The
`edits` arrays in `certificate.json` instead use zero-based positions in the
lexicographically sorted list of all 210 unordered vertex pairs. The SHA-256
of the canonical list of these arrays, serialized by
`json.dumps(arrays, separators=(',', ':')).encode()`, is
`29ed8c76b8bfe25dddad3183bffddebfc369f29f388b266034255a82dfafb6d6`.

## Complete finite reduction

`classify.py` enumerates valid edit sets by an exact repair rule. A node
specifies a set F of required edits and a set D of forbidden edits. Its
domain consists of all final edit sets T with F contained in T, T disjoint
from D, and |T| <= 7.

If H toggled on F contains a monochromatic forbidden book with edge set W,
every valid final T in this domain must contain some edge of W outside F.
Otherwise all edges of that book retain their current colors. Edges in D
cannot be selected, so the algorithm branches over W minus (F union D).
The child selecting option i excludes every earlier option; equivalently,
it chooses the first additional edited edge of W. These children partition
all possible valid final sets in the node's domain. If the budget is
exhausted or no option remains, the domain has no valid final set.

If the current graph is valid, F is recorded. The same partition rule,
applied to all pairs outside F union D, covers every strict superset of F.
Every descent adds an edit, so the tree terminates at depth seven. These
invariants prove completeness and unique coverage. No intermediate invalid
graph is discarded merely because it is invalid: it is repaired whenever
the remaining budget allows it. No symmetry quotient is used.

The production tree has 6,758,303 nodes, including 5,712,457 invalid
budget leaves and 12,843 nodes with no allowed book repair. A direct
enumeration of all edit sets through radius three independently gives
counts 1,0,2,0; its radius-three layer checks all 1,521,520 sets.

`independent.py` uses a different pruning basis. It first lists the 1,444
forbidden books with exactly one wrong-colored edge in the **baseline**.
For each such book, with wrong edge e and other edges S, every valid edit
set satisfies: if e is edited, at least one edge of S must also be edited.
It branches on these fixed necessary clauses, selecting the clause with
the fewest available repairs. Once every selected edit's clauses are
satisfied, it checks the entire graph directly using a set of red edges
and explicit common-neighbor counts. Even an invalid candidate at this
stage retains all allowable strict supersets. The same domain-partition
argument proves completeness. The independent output is compared
entry by entry, not just by aggregate counts, with the first enumeration.

## Compact extension certificates

For an extra vertex z, write x_u = 1 if zu is red. A red spine uv with
three red common neighbors requires `not x_u or not x_v`; a blue spine
with six blue common neighbors requires `x_u or x_v`. These are necessary
conditions on every extension.

A literal numbered 2u means x_u; a literal numbered 2u+1 means not x_u.
For each of the five graphs, `certificate.json` supplies a path from x_0
to not x_0 and a path back. Each implication is justified by one saturated
spine. All five share the first path:

    x_0 -> not x_2 -> x_7 -> not x_0.

For the baseline, the reverse path is:

    not x_0 -> x_6 -> not x_7 -> x_8 -> not x_15 -> x_0.

Any truth value for x_0 contradicts one of these paths. `verify.py` checks
every spine's color and exact common-neighbor count directly from the
graph. It also checks that each listed graph avoids both forbidden books.
No SAT solver, UNSAT log, or floating-point calculation is involved.

## Reproduction

Python 3.11.2, standard library only, with assertions enabled. Each command
runs one process; the computations use exact Python integers and sets.
The full production runs took 157.94 s / 15,560 KiB peak RSS (dynamic)
and 51.81 s / 16,088 KiB (independent); timings vary with host contention.
The second tree has 5,058,955 nodes. Malformed self-edge implications,
incorrect edge counts, missing survivors against a complete run, and
incomplete run status were all rejected by the certificate checker.
From this directory:

```sh
python3 classify.py --radius 7 --output dynamic-run.json
python3 independent.py --radius 7 --output independent-run.json
python3 verify.py dynamic-run.json independent-run.json
```

Both full runs must report `complete: true`, the five edit arrays above,
and the displayed survivor hash. The final command must report five
verified graphs and two compared complete enumeration outputs. A quick
certificate-only check is `python3 verify.py`; this verifies the listed
graphs and their extension contradictions but **not enumeration coverage**.

To verify the precise primary input separately:

```sh
curl -fsSL https://raw.githubusercontent.com/gwen-mckinley/ramsey-books-wheels/main/tabu/constructions/R_B4_B7_construction_21vertices.txt -o /tmp/books47-primary.txt
python3 verify.py --source-matrix /tmp/books47-primary.txt
```

The source bytes have SHA-256
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
If upstream changes, the source-byte check intentionally fails; the
self-contained edge fixture still defines the exact graph in the lemma.
Generated reports and interpreter caches are ignored. No large output
or external proof corpus is required.

## Status, attribution, and trust boundary

The original witness is due to Bernard Lidicky, Gwen McKinley, Florian
Pfender, and Steven Van Overberghe, [Small Ramsey numbers for books,
wheels, and generalizations](https://arxiv.org/abs/2407.07285), Table 1
and supporting repository. That repository's content is released under
[CC BY 4.0](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/LICENSE.md);
`h21.json` is an edge-list complement conversion of its cited matrix.
The [April 2026 Small Ramsey Numbers survey](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
Table IXa, retains the gap. Later [algebraic-construction
work](https://arxiv.org/abs/2606.07214) treats other parameter regimes.
The published global upper-bound certificate has not been independently
audited here. The bounded edit classification was not located in the
searched primary sources; no priority claim is made.

This is an exact computer-assisted finite classification with a written
coverage argument and two enumerators. It is not proof-assistant checked.
Completeness depends on the displayed reductions and the enumerator
implementations, plus Python's exact execution. The extension obstruction
has a separate small certificate checker. Agreement of implementations
is cross-validation, not independent peer review.
