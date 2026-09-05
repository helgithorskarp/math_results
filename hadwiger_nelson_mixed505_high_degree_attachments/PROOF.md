# High-degree attachments in the fixed mixed505 family

Let `A=v159e646` and `V=v214e977` be the hash-pinned archived Parts point
sets. Put `t=(5+i sqrt(11))/6` and `B=A union tA`, retaining the original `A`
labels followed by previously unseen `tA` points in source order.

**Theorem.** If a Euclidean isometry `g` satisfies

\[
g(V)\cap\{b\in B:\deg_B(b)\ge22\}\ne\varnothing,
\]

then the strict unit-distance graph on `B union g(V)` is four-colorable.
Its order is at most 505.

The fixed graph `B` has 292 vertices and 1,251 strict unit edges, and `V`
has 214 vertices and 977 strict edges. Exact reconstruction shows that the
qualifying vertices are precisely

\[
B_0=0,\quad \deg_B(B_0)=41;\qquad
B_{28}=i\sqrt3/3,\quad
B_{185}=(-\sqrt{33}+5i\sqrt3)/18,
\]

with both latter degrees equal to 22. The integer verifier and the rational
geometry auditors each reconstruct this degree set. The case `B_0` is the
[previously proved all-gadget-anchor theorem](../hadwiger_nelson_mixed505_all_gadget_anchors/PROOF.md).
The new computation handles the other two vertices without re-enumerating
the origin case.

## 1. Translation preserves the complete angular reduction

Fix `p=B_28` or `B_185`, and write `B'=B-p`. Give `B'` label 0 at `p-p`,
then retain all other original `B` labels in their previous order. For an
anchor `q in V`, an orientation-preserving placement centered at `p` has,
after translating the entire union by `-p`, point set

\[
B'\cup u(V-q),\qquad |u|=1.
\]

The checked equality `conjugate(V)=V` also covers every reflection by
replacing `q` with `conjugate(q)`. Thus all 214 gadget anchors in the rotation
parameterization suffice for both orientation parities.

All untranslated and translated component points belong to
`E=Q(i sqrt(3),i sqrt(11))`, with real subfield `R=Q(sqrt(33))`.
For `u in E`, the previously proved [whole-field coloring](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
applies. For `u not in E`, any nonzero coincidence
`b'=u(v-q)` would put `u` back in `E`. The sole overlap is therefore the
shared origin; the graph has exactly 505 vertices and 2,228 internal edges.
All edges incident to the origin are already internal. If no new cross
edge exists, component colorings glue directly.

For a new cross edge, set `d=v-q`, `c=conjugate(b')d`,
`S=|b'|^2+|d|^2-1` and `Delta=4|b'|^2|d|^2-S^2`. Then

\[
cu^2-Su+\overline c=0.
\]

Negative `Delta` gives no unit root. For nonnegative `Delta`, both roots
are unit and lie in `E` exactly when `Delta/3` is a square in `R`, including
the double-root case. Every other pair defines an irreducible monic
quadratic over `E`. Equal such quadratics are precisely the complete
cross-edge classes at both roots, by uniqueness of the minimal polynomial.

As in the previous theorem, enumerate distinct nonzero displacements in
`D=V-V` once. The exact table of all incidences `d=v-q` projects every
ambient class to its complete edge set at every anchor `q`. This remains
valid after translating `B` and uses the same integer scale 72 for `B'`
and scale 12 for `D`. There is no angle grid, denominator cutoff, or
partial-edge relaxation.

## 2. Exact finite geometry

There are 4,418 distinct nonzero vectors in `D`, hence 1,285,638 nonzero
`B'`-vertex/displacement pairs for each new inner anchor. Their census is:

| Inner anchor | Negative discriminant | Roots in `E` | Roots outside `E` | Ambient classes |
|---|---:|---:|---:|---:|
| 28 | 529,462 | 109,166 | 647,010 | 407,356 |
| 185 | 533,592 | 108,902 | 643,144 | 403,220 |

Projection gives 6,094,992 nonempty gadget-anchor/class cases for inner
anchor 28 and 6,064,198 for inner anchor 185, totaling 12,159,190 new cases.
Counts refer to the specified labels and parameterizations; they are not
counts of graph isomorphism types or distinct point sets. Each ambient
class has two distinct unit roots, and roots from different ambient classes
are distinct for a fixed inner anchor.

The maximum new cross-edge counts outside `E` are respectively 18 and 19.
These bounds do not cover the separate in-field branch. Nor are they the
maximum for the imported origin family, whose bound is 26.

The rational auditors use a separate four-dimensional field representation
and the monic normalization. They match every pair classification, the
full canonical ambient edge partition, and every projected anchor histogram.
The main program uses the previously published integer sign/square tests
and projective normalization. These checks agree at the level of the full
partition, not merely aggregate totals.

## 3. Repair of the positive coloring library

Start with the earlier three proper `B` colorings and two proper `V`
colorings. At the new inner anchor `p`, a `B` row `f` becomes
`f(b) XOR f(p)` in the translated label order. At gadget anchor `q`, a `V`
row `h` becomes `h(v) XOR h(q)`. Each normalization is a bijection of the
four color labels and sends the common point to 0.

The original rows, together with all six permutations of the right colors
fixing 0, fail to cover 6,922 cases at inner anchor 28 and 7,826 at inner
anchor 185. These were only library residuals. Five satisfiable graph-coloring
queries supplied five additional rows for each component. Every returned
505-vertex coloring was checked directly before its component restrictions
were normalized back to original label 0 and added to the libraries.

The repaired library has eight `B` rows and seven `V` rows. It occupies
3,849 bytes, including 1,309 reused bytes and 2,540 new bytes. The verifier
checks every internal edge for every row. For each projected class it tries
one row from each library and one of the six origin-fixing permutations,
then directly checks the chosen coloring on all projected cross edges.
Every one of the 12,159,190 cases succeeds. The data are sufficient positive
certificates; no minimality or necessity of individual rows is asserted.

Combining internal-edge validity, agreement at the common point, and
validity on the complete cross-edge set gives a proper union coloring.
Together with the in-field and cross-edge-free branches, this proves the
new two-anchor exclusions. The imported origin theorem completes the
stated degree-threshold theorem.

## 4. Mask calculation and a direct formerly uncovered graph

The witness choices are indexed by `(i,j,k)`, meaning a left row, a right
row, and a permutation. For each pair of right-component color signatures
at `q,v`, the optimized checker records four masks: mask `c` contains
exactly the right-row/permutation choices that color `v` with `c` after
anchor normalization. For each left row, the mask of its color at the left
endpoint is shifted into that row's block. The union of these shifted masks
is precisely the set of forbidden choices for that edge. Complementing it
within the full finite choice set gives the allowed mask.

Intersect these allowed masks along all cross edges. A zero mask can stop
that intersection because later constraints cannot restore a choice. A
nonzero mask supplies a witness, whose actual colors are separately checked
on every cross edge. The optimized calculation reproduced both complete
baseline witness-stream hashes, residual counts and projected histograms
before it was used for the repaired libraries. It avoids an expensive cache
of full left/right signature combinations as more rows are added.

A former residual at inner anchor `p=B_28` and gadget anchor `q=V[46]` has
four new cross edges. Its polynomial is

\[
U^2-\left(\frac78+\frac{7i\sqrt3}{24}\right)U
+\frac{1+i\sqrt3}{2}=0.
\]

Both roots are

\[
u_\varepsilon=\frac{21-\varepsilon\sqrt{429}
+i(7\sqrt3+3\varepsilon\sqrt{143})}{48},\qquad\varepsilon=\pm1.
\]

The standalone checker verifies the unit norm and quadratic identities
and constructs `B-p union u_epsilon(V-q)` directly in the eight-element
real radical basis of `Q(sqrt(3),sqrt(11),sqrt(13))`, at integer scale 576.
The nonzero real `sqrt(429)` coefficient also shows these roots are outside
`E`, by basis independence. Every one of the 127,260 point pairs is tested
for each root. Both realizations have 505 distinct vertices, 1,251 plus
977 internal edges, and exactly the four new edges in
`first_repair_example.json`, hence 2,232 strict unit edges.

All 36 original gluing choices fail on this graph, whereas a repaired
choice gives an actual proper coloring. In fact the first successful choice
in the direct checker uses an original `B` row and the first new `V` row.
This illustrates why a library residual is not a non-four-colorability
certificate, even when the geometry and complete edge set are exact.

## 5. Trust and scope

These are author cross-checks, not an independent peer review. The whole-
field theorem and continuous-to-finite algebra remain unformalized. Finite
trust lies in exact Python arithmetic, pinned coordinates and source,
the checked positive rows, and ordinary software/hardware execution.
No SAT verdict is used without checking its positive coloring. No UNSAT
verdict, approximate unit-distance decision, or omitted large certificate
is required.

The original data [provenance](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md)
is Parts' archive accompanying [the graph-minimization paper](https://arxiv.org/abs/2010.12665).
[Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4),
checked on 2026-09-05, retains the 509-vertex benchmark. The present theorem
excludes another bounded construction family; it produces no record graph
and makes no priority claim for the elementary gluing or quadratic methods.
