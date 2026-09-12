# Exact classification and original-parent implication

Color 1 is red. An R(4,4) core is a graph with neither a red K4 nor a blue K4.
Let H be one of the 546,356 literal order-11 records in the pinned author
catalog. Let B be four new vertices, all six internal B edges blue.
We ask whether the 44 edges from H to B can be colored so that H union B
has no red K4 and no blue K5. All 44 choices are unrestricted.

**Classification.** The answer is yes for every record other than 516166,
and no for record 516166. The latter is the red join W8 + I3: W8 is the
8-cycle together with its four opposite-vertex edges, and I3 is an independent
triple. `reference.wagner_join` supplies and checks a literal permutation
between this definition and the catalog record. The obstruction has 36 red
edges. The all-catalog check also identifies it as the unique maximum-edge
core.

For every positive record, a 44-bit word specifies all cross edges. The
separate C++ checker decodes the input, verifies that the core is R(4,4),
constructs the full graph on 15 vertices, and tests the two forbidden clique
conditions using recursive neighborhood intersections. The six blue edges
of B are set explicitly. The checked witness count is 546,355.

For the negative record there are 285 clauses on 44 physical variables.
They can be derived without the general encoder:

- A red K4 consists of a red triangle in H and one vertex of B: 144 clauses.
- A blue K5 with three vertices in H and two in B: 54 clauses.
- A blue K5 with two vertices in H and three in B: 76 clauses.
- A blue K5 with one vertex in H and four in B: 11 clauses.

Other splits are impossible because H has no monochromatic K4 and B is blue.
The factorized and generic encoders agree clause for clause as multisets.
The exact CNF is `obstruction.cnf`, SHA-256
`6a0b6b23bf7d667da0e199fa7e58ade1b20ae54c430b8afed8ef6d0a5e5f0c81`.
The positive-hint LRAT proof is `obstruction.lrat`, SHA-256
`9022758fae7597f32fe380f75eac537beafce47cf373d26a5c153aff813cde1e`.
Its 2,002 additions derive the empty clause. No RAT step is needed.

**Original-task consequence.** Fix r in {5,6,7}. In the original ordered task
`bo1-q8-r{r}-c516166`, the first r prescribed K4 blocks are red. The next
block, at labels 4r through 4r+3, is blue. The core is labels 32 through 42.
The original red-maximality clauses forbid every red K4 on labels 4r through
42; its global clauses forbid every blue K5 on all 43 vertices.

Take H to be the literal core and B the first prescribed blue block. Thus
any model of the full original task would restrict to an extension forbidden
by the classification. The injection from local labels to original labels is

```
[32,33,34,35,36,37,38,39,40,41,42, 4r,4r+1,4r+2,4r+3].
```

No vertex is duplicated, and every selected vertex lies in the original red
residual. Every core and B edge has exactly the required fixed color.
`bridge.py` checks each of the 285 local clauses against the actual parent's
forbidden-set routine, then finds it in the complete emitted ordered-parent
DIMACS file. Each of the 44 physical variables maps injectively to its actual
parent variable. No additional clause or normalization is appended.

The local LRAT additions and hints are then renamed into actual parent
variable and input-clause numbers. Derived IDs are shifted beyond the last
original clause. Deletions can be omitted because keeping an entailed clause
preserves soundness. The receiving checker scans the full exact parent input
and validates every proof addition through to the empty clause. `ORIGINALS.json`
records all three input hashes and proof hashes; `BRIDGE.json` also records
all embeddings and clause maps. This proves three original-task exclusions,
not merely three physical child decisions.

The same inference does not cover r=8: no prescribed blue block remains.
A SAT witness of the 15-vertex local problem also says nothing about extending
to good43. No q8 physical cohort is closed by this result. The classification
shows that this one-block test has no further exclusions anywhere in the
retained order-11 catalog. This rules out a stream of additional one-block
slices as a useful next step.
