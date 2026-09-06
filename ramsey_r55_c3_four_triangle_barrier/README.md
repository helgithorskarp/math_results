# A four-triangle repair barrier for the score-123 C3 graph

The saved [43-vertex graph](baseline.edges) is the **unique minimum of
score 123** under all the recolorings specified below. Every nontrivial
recoloring in this family has **at least 126 monochromatic five-sets**.
There are exactly **4,183,743,579 distinct labeled graphs** in the family.
The value 126 is a lower bound; attainment is not asserted.

This is an exact local repair obstruction for one defective graph. The
graph still has 72 blue K5s and 51 red K5s. There is no improved graph,
Ramsey coloring, whole-action exclusion, or Ramsey-number bound change.
The useful consequence is that any score improvement retaining the same
C3 action and internal triangle colors must change pairs involving **at
least five moving triangles**. No five-triangle phase has started here.

## Exact family and coverage

Let `G0` be the [previously published construction](../ramsey_r55_c3_fourteen_construction),
with action `g=(0 1 2)...(39 40 41)` fixing vertex 42. Triangles 0 through
6 are internally red, and 7 through 13 internally blue. Its edge-list
SHA-256 is
`36c4a4ff6359e56ece7c9a6b41e35fae02cb04d72e56d832dc1a4dc056c6e88e`.
Files start with the order `43`, then sorted red pairs `u v` on labels
0 through 42; all omitted pairs are blue.

For every four-element subset `Q` of the fourteen moving triangles,
freely recolor all three phase orbits between each pair of its triangles,
and each triangle's contact to vertex 42. The four internal triangles
and every other pair retain their colors in `G0`. This gives

`3*binom(4,2)+4 = 22`

independent bits, changing 66 of the 78 pairs on the selected thirteen
vertices. All 1,001 blocks use the same original `G0`; they are not
successively based on intermediate results. The union covers exactly
all C3-preserving recolorings with the same internal colors whose changed
pairs involve at most four moving triangles. In particular it covers
changes involving fewer triangles, by extending their support to four.

This is not a family of arbitrary thirteen-vertex recolorings, arbitrary
C3 graphs, switches of `G0`, or arbitrary graphs after relabeling. The
labels, action and internal colors are fixed. The earlier separation of
`G0` from completed switching families is context, not a premise here;
no separation claim is made for every member of this new repair family.

The run exhausts `1001*2^22 = 4,198,498,304` block-assignment slots.
Blocks overlap, so this number is **not** a distinct-graph count.
[blocks.tsv](blocks.tsv) records all 1,001 block minima, first argmin
masks, multiplicities, maxima, score sums and projected-event counts.
Every row has minimum 123, first mask zero, and multiplicity one.
Thus `G0` is the unique minimum in the union as well.

Every five-set orbit under `g` has size three: an invariant five-set
would have to be a union of three-cycles and possibly the one fixed
vertex, which cannot have order five. Monochromatic five-sets consequently
occur in triples. A nontrivial recoloring has score strictly above 123,
hence at least 126.

## Exact number of distinct graphs

For a recoloring, its support is the set of moving triangles containing
an endpoint of a changed pair; vertex 42 is not counted. On a specified
set of `r` triangles there are `3*binom(r,2)+r` free orbit bits. Let `a_r`
count toggle words whose support is that whole specified set. Excluding
each missing triangle by inclusion-exclusion gives

`a_r = sum_(j=0)^r (-1)^j binom(r,j) 2^(3*binom(r-j,2)+r-j)`.

Equivalently, `2^(3*binom(r,2)+r) = sum_(s=0)^r binom(r,s) a_s`, by
partitioning words according to their exact support. Each physical graph
has a unique toggle word and exact support, so summing over supports of
size at most four counts the union without duplication.

| Support size | Words on a specified support | Distinct labeled graphs |
| ---: | ---: | ---: |
| 0 | 1 | 1 |
| 1 | 1 | 14 |
| 2 | 29 | 2,639 |
| 3 | 4,005 | 1,457,820 |
| 4 | 4,178,105 | 4,182,283,105 |
| Total | | **4,183,743,579** |

[count.py](count.py) evaluates both formulas with exact Python integers
and checks the support partition by literal enumeration of all 4,131
words on zero through three triangles. [count.json](count.json) records
the complete result. This post-run cardinality calculation is not an
input, pruning rule, or symmetry assumption in the native computation.
No count modulo graph isomorphism is asserted.

## Exact evaluation by a subset transform

The objective counts all 962,598 physical five-sets of the full graph,
including five-sets extending outside the chosen thirteen vertices.
For each color, a frozen pair of the other color makes that event
impossible. Otherwise its free variables require certain toggle bits
`y_i=1` on a set `P`, and `y_i=0` on a disjoint set `Q`. Repeated orbit
indices are collapsed. A merged event of physical multiplicity `w`
contributes the Boolean polynomial

`w * product_(i in P) y_i * product_(i in Q) (1-y_i)`.

Expanding the second product contributes `(-1)^|T| w` to the coefficient
indexed by `P union T`, for each `T subset Q`. The subset zeta transform
replaces each coefficient array entry at `S` by the sum over `T subset S`,
which evaluates the polynomial at the assignment with ones exactly in
`S`. Summing event polynomials therefore gives the exact global physical
score at every one of the `2^22` assignments. Scanning that table proves
its minimum and the number of assignments attaining it.

[block.cpp](block.cpp) implements this derivation. Only its physical
weighted-clause generator and original orbit-index function come from
the prior construction's `search.cpp`; it uses none of the heuristic
optimizer. Every identical event retains its physical multiplicity.
[imports.json](imports.json) records this reuse explicitly.

All table arithmetic is signed 64-bit integer arithmetic. A coefficient
has absolute value at most `2*962598`; a partial transform entry sums at
most `2^22` coefficients. Their product is below `2^63`. Final scores
are in `[0,962598]`. The expected first moment is bounded by the same
loose product. Subset indices are unsigned, with shifts below 22. No
floating arithmetic affects a decision; elapsed time is metadata only.

Each block checks the unchanged score 123, nonnegative bounded scores,
and divisibility by three. It compares the sum of the entire table with
the separate conjunction-cardinality sum

`sum_events w * 2^(22-|P union Q|)`.

The first argmin is also evaluated directly in the weighted model,
without the transform. All these checks passed in every block. Source
and scope were frozen before the single full production run; see
[PROTOCOL.md](PROTOCOL.md) and [result.json](result.json).

## Verification and trust boundaries

[audit.py](audit.py) discovers the free physical pair orbits under `g`
and derives each block from its actual thirteen vertices. It imports no
native model, native orbit-index formula, or subset-transform code.
It verifies the canonical coverage of all 1,001 blocks and reconstructs
every recorded argmin, with direct red/blue clique counts. All argmins
are the same graph `G0`; the audit caches identical words rather than
calling them 1,001 independent graph checks. Literal enumeration of all
962,598 winner five-sets and separate clique recursion give identical
complete lists of the 123 defects.

The physical routines in [physical.py](physical.py) are copied byte for
byte from the prior published verifier, with provenance in `imports.json`.
This is disclosed reuse. It provides an algorithm different from the
polynomial objective, not external peer review or a newly rewritten
physical checker.

Controls compare all 256 entries of one eight-bit restricted block with
actual graph clique counts. All 1,093 ternary event patterns through six
variables are compared with literal Boolean conjunctions. Three full
22-bit blocks give byte-identical rows and graphs in release and address/
undefined-behavior sanitizer builds. Eight malformed graph, range, score
or output-directory cases are rejected. Calibration overlaps production
and is not additional family coverage. Normal and optimized Python
audits and cardinality reports agree byte for byte.

**The physical audit alone does not prove all production minima or their
uniqueness.** Those negative assertions rest on the complete native
transform and table scan, with the derivation, controls and explicit
arithmetic bounds above. This is a deterministic exhaustive computation,
not a SAT proof checked by a separate proof kernel. It has author checking,
not external review or formalization at publication. Its trust boundary
includes the generator, projection, transform, compiler, input identities
and platform. No solver, timeout verdict, catalog completeness, earlier
exclusion theorem or omitted large certificate is a premise.

## Run and reproduction

The one full run completed all 1,001 blocks in **188.653 seconds**, with
reported peak child RSS **139,944 KiB**. All 4,198,498,304 assignment slots
were scanned; no STOP, early target, or partial-range condition occurred.
The three-block release/sanitizer calibrations took 1.091 and 11.410
seconds. No follow-up block size or reanchored sweep was started.

Tested with CPython 3.11.2 standard library, GCC 12.2.0, C++20. From the
repository root with a new output path:

```sh
bash ramsey_r55_c3_four_triangle_barrier/reproduce.sh /tmp/r55-four-triangle-check
```

The default reruns the complete native transform, compares every row of
`blocks.tsv` and the graph bytes, and runs the physical and arithmetic
checks. Expect all 1,001 minima to be uniquely attained by mask zero at
score 123, and distinct-family count 4,183,743,579. Allow approximately
three minutes for the full native computation on the production host.

For a shorter integrity, physical-witness and control check, use:

```sh
bash ramsey_r55_c3_four_triangle_barrier/reproduce.sh /tmp/r55-four-triangle-audit --audit-only
```

That mode **does not re-evaluate the production minima**. It was run from
the assembled public package; the original complete native run used the
same hash-frozen source. No second full sweep was performed merely to
repackage it. Both modes need only the bundled files, compiler and Python.
Full tables, binaries, native logs and operational state remain outside
Git; the small eight-bit control table and all block summary rows are public.

To run the native computation directly from this directory:

```sh
g++ -std=c++20 -O3 -Wall -Wextra -Wpedantic -Werror block.cpp -o /tmp/r55-block
/tmp/r55-block baseline.edges /tmp/r55-block-run 0 1001 22 123
```

Replace `-O3` by `-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer`
for the checking build. The range is explicit; smaller ranges or smaller
bit counts are not the whole family. A `STOP` file in the run directory
is honored before another block, and completion flags distinguish partial
coverage. Source and final checkpoint preserve the exact completed scope.

The constructive improvement gate was not met. This complete local barrier
is the bounded pass's negative evidence and stopping point; it is not
presented as a new global symmetry restriction. Reassess the next method
after coordination rather than automatically extending this census.
