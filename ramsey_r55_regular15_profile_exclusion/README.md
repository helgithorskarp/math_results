# A regular-side obstruction excludes the double-degree-19 hard profile

**The hard-branch degree profile `19^2 20^3 21^38` is impossible.**
The preceding common-root squeeze forces an eight-regular Ramsey `(4,4)`
induced graph on 15 vertices. A complete, solver-free five-case gluing
enumeration proves that no such graph exists. A separate implementation
checks the same cases by inspecting literal four-vertex sets.

This removes one global hard-branch candidate and its two anchored splits:
the cumulative counts change from **67/273 to 66 profiles / 271 splits**.
Both W alternatives left by the preceding pass are covered at once; no
further W-specific search is needed for this profile. This is not a target
graph or a Ramsey lower-bound improvement. In particular, this does not
exclude the degree profile outside the stated hard branch.

## 1. The small obstruction

**Lemma. There is no eight-regular graph on 15 vertices with neither a
four-clique nor an independent four-set.**

Choose any vertex v in a hypothetical graph and put

```text
H = red neighbors of v,       |H|=8;
B = blue neighbors of v,      |B|=6.
```

The induced graph H has no red triangle, since it would extend v to a red
K4, and no blue K4. Thus H has type `(3,4;8)`. Similarly B has type
`(4,3;6)`, so its color complement has type `(3,4;6)`.

The complete small classification gives three H types, with 10, 11, and
12 red edges, and fifteen types for the complement of B. The coverage
check is described below; the proof does not import completeness of the
external fifteen-vertex catalog.

Every vertex of H has one red edge to v, so the red H--B edge count is
`56-2e(H)`. No vertex of B is red to v, so that same count is
`48-2e(B)`. Consequently

```text
e(H)-e(B)=4.                                               (1)
```

Of the 45 type pairs, precisely five satisfy (1). Relabeling H and B
independently to their representatives loses no possible graph: the
remaining cross matrix is arbitrary and completely enumerated. No
automorphism or extra symmetry of the full graph is assumed.

All edge masks below use lexicographic pair order, least significant bit
first. The B column records the mask of **the complement of B**, not B.

| H mask | Complement-of-B mask | e(H) | e(B) | Cross edges | Production search nodes | Completions |
|---:|---:|---:|---:|---:|---:|---:|
| 5388912 | 4060 | 10 | 6 | 36 | 1 | 0 |
| 5404008 | 2012 | 11 | 7 | 34 | 1 | 0 |
| 5683824 | 954 | 12 | 8 | 32 | 672 | 0 |
| 5683824 | 956 | 12 | 8 | 32 | 1577 | 0 |
| 5683824 | 1884 | 12 | 8 | 32 | 2010 | 0 |

There are 4,261 production nodes in total, including each empty root.
The first two cases have an empty row domain and need no branching.
The remaining three exhaust after at most six assigned rows, before all
eight rows can be assigned. The differing literal-check counts are
recorded in [report.json](report.json), not conflated with this table.

## 2. Exact cross-matrix enumeration and completeness

For each vertex i in H let `T_i subset B` be its red cross-neighborhood.
Regularity requires

```text
|T_i|=7-d_H(i),
number of i with b in T_i = 8-d_B(b) for each b in B.        (2)
```

[gluing.py](gluing.py) enumerates every subset T_i of the required size.
A row is discarded if T_i contains a red triangle in B or B\T_i contains
a blue triangle. It orders rows by domain size, breaking ties by label.
After inserting a row, it applies only the following necessary tests:

- No column count exceeds its target or falls so far short that all
  remaining rows could not reach the target.
- For two red-adjacent H vertices, their common red B-neighborhood has
  no red edge. For two blue-adjacent H vertices, their common blue
  B-neighborhood has no blue edge. These are the two-H/two-B K4 tests.
- For each blue triangle in H, the three row sets cover B. This is the
  three-H/one-B blue K4 test. There are no red triangles in H.

The one-H/three-B four-sets were handled by the row domains. Four-sets
inside a side were handled by the small type census. A monochromatic K4
through v would require a red triangle in H or a blue triangle in B,
both forbidden by their types. Thus the tests cover every four-set.
All subsets passing them are recursively visited, without time limits,
heuristic deletions, or additional symmetry breaking. At depth eight,
the column sums are checked for equality. These conditions are necessary
and sufficient for a completion of the chosen rooted type pair.

[literal_check.py](literal_check.py) is a separate definition-level
implementation. It starts with B and v, inserts H vertices in their
natural order, and tries every red cross-subset of the required size.
It uses the elementary column bounds but neither the production row
domain filtering nor the decomposed mixed-clique tests. Instead, after
inserting a vertex, it checks **every new four-set** in an actual Boolean
adjacency matrix. This reconstructs the same finite question directly.
Its five cases try 582, 17,637, 10,080, 23,655, and 30,150 row insertions;
all have zero completions. The implementations are separate internal
checks, not independent peer review or separate proof-assistant kernels.

## 3. Independently checked small-type coverage

The pinned [critical-eight verifier](../ramsey_r55_ten_edge_cell_obstruction/verify.py)
is executed to reconstruct its complete `(3,4)` classification. Its
vertex augmentation enumerates all 17,640 labeled graphs on eight
vertices and partitions them into three full permutation orbits, with
sizes 5,040, 10,080, and 2,520. The validity and completeness induction
and its independent edge-bit check through order six are documented in
that artifact. This pass reuses that previously checked classification;
it does not claim a newly independent eight-vertex census.

For B, the new verifier independently inspects **all 32,768 edge-bit
assignments on six vertices**, retains the 2,812 `(3,4)` graphs, and
compares their complete labeled set with vertex augmentation. Full
permutation orbits partition them into fifteen classes, with no gaps or
overlap. Every one of the 45 H/B type pairs is then checked for (1),
recovering exactly the five cases above. No external graph-isomorphism
program, SAT solver, floating-point arithmetic, or claimed global
catalog completeness is used in this proof computation.

The small nonexistence result is already consistent with classical
catalog data, not claimed as a new Ramsey classification. As a motivating
comparison, [McKay's catalog](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
lists 640 `(4,4;15)` graphs. The optional [catalog inspector](inspect_catalog.py)
checks every four-set and every degree in all 640 records of
[r44_15.g6](https://users.cecs.anu.edu.au/~bdm/data/r44_15.g6), finding no
regular entry and the edge histogram
`50:13, 51:96, 52:211, 53:211, 54:96, 55:13`.
The 12,800-byte file has SHA256
`53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1`.
Its compact observation is [catalog_report.json](catalog_report.json).
The catalog file remains outside Git and is **not needed for the theorem**.
In particular, we do not infer a universal 55-edge upper bound merely
from this file inspection.

## 4. Apply the obstruction to the hard R(5,5) profile

The [common-root squeeze](../ramsey_r55_common_neighbor_squeeze/README.md)
proves the following necessary facts for the **hard branch** with degree
profile `19^2 20^3 21^38` (M=217, 448 red edges). The hard branch means
all color-neighborhoods have deficiency at least seven relative to the
inherited order-specific local extrema.

After a justified relabeling, the exceptional core E on `0,...,4` has
red edges `01,02,04,12,13,23,24`. The central cells have exact E signatures

```text
U={0,1}, size 2;       W={2,3,4}, size 8;
A_i={0,i}, B_i={1,i}, i=2,3,4;
(|A_2|,|A_3|,|A_4|)=(4,2,8),
(|B_2|,|B_3|,|B_4|)=(4,8,2).
```

Put P=union A_i and Q=union B_i. Equality in the common-root bound forces
every vertex of P to have red degree eight inside `P union {4}`.
Vertex 4 is red to all eight A_4 vertices and no other P vertex, so
`P union {4}` is eight-regular on 15 vertices. It has neither a red K4
nor a blue K4, since it is uniformly red to 0 and blue to 1. This
contradicts the small lemma. The analogous Q side would give the same
contradiction, but only one side is needed.

This excludes the entire stated hard-branch profile. The conclusion does
not require choosing between the two residual W types or testing their
gluing to P,Q,U. The positive aggregate vectors in the parent remain
valid **for their explicitly weaker linear system**; they were never
asserted to be graph realizations and are not counterexamples here.

The cumulative update replays the prior single-degree-19 exclusion,
checks the pinned profile/screen tables, confirms the new profile was
not already removed, and removes precisely its one global row and two
anchored splits. Remaining totals by M=214,...,220 are:

```text
globals: 1,3,7,10,13,15,17       (sum 66)
splits:  1,5,17,33,54,72,89      (sum 271).
```

The global target, the low-deficiency branch, all other degree profiles,
and the teammate's residual symmetry cases remain open to the extent
they were open before this pass.

## 5. Reproduction, controls, and trust boundary

Run with Python 3.11.2, standard library only, from this directory:

```bash
python3 verify.py --report /tmp/r55_regular15.json
cmp report.json /tmp/r55_regular15.json
python3 -O verify.py --report /tmp/r55_regular15_optimized.json
cmp report.json /tmp/r55_regular15_optimized.json
sha256sum -c SHA256SUMS
```

Compare stdout with [EXPECTED_OUTPUT.txt](EXPECTED_OUTPUT.txt).
The complete normal replay took 16.198 seconds and 26,184 KiB maximum
child RSS on the research host. Keeping the small exact computation in
Python avoided introducing an unnecessary compiled or solver backend.
The default proof replays the full common-root chain, including its
paired/core and ten-edge checks, and the previous profile exclusion.
Immediate source/report hashes are pinned in [verify.py](verify.py);
earlier imported certificates and local-extremal inputs retain their
documented trust boundaries. Normal and optimized-mode reports agree.
No long-lived process, solver, or external service is needed.

For a nonvacuous positive control, both gluing algorithms enumerate the
entire same set of **82 labeled cross matrices** for a rooted four-regular
nine-vertex `(4,4)` instance. The root partition comes from the 3-by-3
rook graph, and its actual cross matrix is in both sets. Every one of
the 82 outputs is decoded and checked directly for regularity and all
four-sets. A changed cross edge and a regular complete graph are rejected
by separate negative controls. These tests do not replace the coverage
proof or establish correctness solely by agreement.

Optional catalog comparison, with its input kept outside the repository:

```bash
curl -fsSL https://users.cecs.anu.edu.au/~bdm/data/r44_15.g6 -o /tmp/r44_15.g6
python3 inspect_catalog.py /tmp/r44_15.g6 --report /tmp/r55_catalog.json
cmp catalog_report.json /tmp/r55_catalog.json
```

The mathematical graph-to-enumeration reduction, source correctness,
exact Python execution, imported parent chain, and hardware remain
unformalized trust boundaries. This contribution has not received an
independent peer review. The two cross-matrix algorithms do not depend
on the fifteen-vertex catalog, but do share the proved small-type
classification and elementary degree-balance reduction.

During this pass an [independent review of the preceding common-root
squeeze](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_common_root_squeeze_independent_review)
was committed to Discovery Net at height 2597. It accepts that lemma and
its equality structure, conditional on the imported hard-branch core
and profile data. It does not review the new regular-fifteen enumeration
or the new whole-profile exclusion presented here.

## Completed pass boundary

All five cases and their literal checks are complete. No background job
remains, and no new profile or construction phase is launched here.
The next structural direction is to apply the strengthened common-root
capacity mechanism to other surviving exceptional-core profiles, while
keeping the teammate's symmetry lane and the parked general-catalog
neighborhood lane separate. The M=214 whole-stratum backend remains an
available, distinct handoff without a SAT/UNSAT verdict.
