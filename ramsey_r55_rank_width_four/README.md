# Every good43 graph has rank-width at least four in both colors

The complete global family of 43-vertex graphs of binary rank-width at
most three, in either color, contains no Ramsey(5,5) graph. All graph
labels, internal edges, cut matrices and decomposition trees are covered.
A successful 43-vertex construction must have rank-width at least four
in both colors. No target graph, Ramsey-bound improvement, sharpness or
historical priority is claimed.

The [proof](PROOF.md) closes the two balanced cases left by the independently
accepted [cut-rank theorem](../ramsey_r55_cut_rank_obstruction/README.md):
20+23 and 21+22 cannot have cut rank three. Combined with its bounds for
smaller-side sizes 15--19, every cut of size 15--21 has rank at least four.
A centroid of any rank-decomposition tree supplies such a cut, proving
the global rank-width conclusion.

The mechanism is a small rank-three contact argument. Write each cross
entry as x dot y for labels in F2^3. Uniform-class bounds force at least
three distinct nonzero row classes containing both a red and a blue edge.
Their three cyclic contact cells are disjoint and each contains at most
five vertices. They cover six of the eight column labels; the remaining
zero and nonzero classes cannot accommodate the missing vertices. The
21+22 case includes an explicit treatment of a possible blue-triangle
row class, so the proof does not silently assume all large classes are mixed.

This is a proof about all global graphs in the family, rather than a
sampled matrix census. It imports the reviewed cut-rank result, the earlier
distinguisher mechanism, and ultimately the established R(4,5)<=25.
It uses no saved-parent repair, fixed-neighborhood gluing, SAT solver,
graph-catalog completeness or height-3687 automorphism claim.

## Reproduction

Python 3.11, standard library only; tested with CPython 3.11.2. Run:

```
python3 -B reproduce.py
python3 -B extract.py fixture_cut.json
python3 -B verify.py fixture_cut.json fixture_cut_certificate.json
python3 -B extract.py fixture_decomposition.json
```

Expected full status: `REPRODUCED_GLOBAL_RANK_WIDTH_THREE_EXCLUSION`.
The command checks every source-manifest hash and requires byte-identical
expected outputs and fixture certificates under normal and assertion-disabled
Python. Everything needed for this replay is included. There are no omitted
proof traces, network dependencies or large generated artifacts.

`audit.py` independently checks the finite steps of the written argument:
all 210 ordered triples of nonzero rank-three labels (42 dependent and
168 independent), all 42 pair intersections, all 32,768 six-vertex graphs
for R(3,3), all 1,024 graphs inside a five-class, all 32 outside signatures,
17,529 integer occupancy cases including the exceptional triangle, both
balanced contradictions and all 231 centroid component-size triples.
The written proof establishes universal coverage; these finite controls
do not enumerate the global 43-vertex family.

`controls.py` supplies full physical graphs and independently checks their
cuts, supplied decomposition trees, color reversal and arbitrary vertex
relabeling. Every accepted certificate contains a literal monochromatic
five-set. It also rejects malformed inputs and corrupted certificates and
checks that graphs outside the stated gate receive no feasibility verdict.
All fixtures are deliberately non-Ramsey controls, not construction candidates.

## Physical interface and trust boundary

Inputs contain `n:43`, `red_hex`, `rank_color` and `kind`. `red_hex` is a
226-character lowercase hexadecimal word encoding the 903 physical pairs
in lexicographic order, with the first pair at the least significant bit;
the represented value must be below 2^903. Omitted edge bits are blue.
`rank_color` is `red` or `blue`.

Two complete consumer interfaces are supported:

* `kind:cut` adds a sorted nonempty proper vertex list `cut`. The gate
  accepts a cut of smaller-side size 15--21 and rank at most three.
  Either side may be supplied. In particular it covers every rank-three
  20x23 and 21x22 matrix with all internal edges arbitrary.
* `kind:decomposition` adds `tree_edges`, the 83 sorted edges of a tree
  on IDs 0..83. Leaves 0..42 correspond to graph vertices and have degree
  one; internal IDs 43..83 have degree three. The gate checks every edge
  cut has rank at most three. This normal form loses no decomposition:
  suppress degree-two internal vertices and rename the 41 remaining
  internal vertices of a subcubic 43-leaf tree.

`EXCLUDED_WITH_PHYSICAL_FIVE_SET` binds a cut, a binary row-space basis
and a monochromatic five-set to the canonical input hash. The standalone
`verify.py` imports no producer, solver or graph catalog. It uses a dense
graph, dense elimination and separate edge-removal traversals of the tree,
checks the complete proposed decomposition or cut, validates the row basis,
and inspects all ten physical pairs of the five-set.

`OUTSIDE_DECLARED_FAMILY` means only that the supplied cut or decomposition
does not meet this gate. It makes no claim of Ramsey feasibility or of the
graph's minimum rank-width over other trees. A supposed family member with
no monochromatic five-set is a hard theorem/implementation failure, never
an accepted survivor.

The universal proof is unformalized and conditional on the stated imported
theorems. The finite checks rely on CPython exact integer/file semantics,
SHA-256 for identity, the OS and ordinary hardware. They are internal
independent implementation checks, not external peer review. No new theorem
is inferred solely from matching hashes or an author status log.

## Dependencies and remaining scope

The [proof](PROOF.md) gives the exact source commits and committed Discovery
Net references for the accepted cut-rank theorem and module-resilience
antecedent. Standard rank-width definitions are in
[Oum's survey](https://arxiv.org/abs/1601.03800); the Ramsey premise is
[McKay--Radziszowski's R(4,5)=25](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf),
also treated in the later [formal proof](https://arxiv.org/abs/2404.01761).
Historical computations proving that premise are not replayed here.

The global rank-width-three family is closed. Rank-width-four survivors,
the unrestricted good43 problem and actual construction searches remain
open. The earlier linear-rank-width lower bound of four and the pentagon
incidence constants are unchanged. No next width or repair search is begun
by this package.
