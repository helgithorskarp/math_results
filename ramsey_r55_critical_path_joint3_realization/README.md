# A joint three-outside realization retaining the root-union bounds

[GRAPH.json](GRAPH.json) is a checked 43-vertex graph satisfying the
fixed critical-path core, degrees **20^3 21^40**, all **3,140 core-root
union bounds**, the three selected hard-root density caps, and **every
K5 prohibition involving at most three outside vertices simultaneously**.
Footprints and their shared outside-edge colors were solved together.

This is a feasibility certificate for that precise relaxation, not a
Ramsey(5,5;43) graph. It still has **588 monochromatic K5s**, all involving
four or five outsiders, and **35 hard local-cap failures**. It is not a
whole hard-branch/470-case witness, a target construction, an exclusion,
or a claim of a best K5 search endpoint. No R(5,5) bound is improved.

## Literal scope and graph certificate

The core K consists of vertices 0,...,10. Vertex 0 is red to every
other core vertex; vertices 1 and 2 are blue to one another and to
3,...,10. The BLUE graph on 3,...,10 has lexicographic eight-vertex
edge mask **5388912**. Thus K has 28 red and 27 blue pairs. Its red
adjacency rows, restricted to K and represented as eleven-bit integers,
are

```
2046, 1, 1, 241, 361, 921, 1433, 1641, 1649, 1441, 961.
```

No critical-eight catalogue completeness is a premise: both checkers
verify this literal graph. The root-signature of v has bit i precisely
when vi is red, for i=0,1,2. The prescribed labeling is:

| Vertices | Root signature | Number |
|---|---:|---:|
| 3,...,10 | 1 | 8 |
| 11,...,19 | 2 | 9 |
| 20,...,23 | 3 | 4 |
| 24,...,32 | 4 | 9 |
| 33,...,36 | 5 | 4 |
| 37,...,40 | 6 | 4 |
| 41,42 | 7 | 2 |

The three root degrees are 20 and all forty other degrees are 21.
There are 450 red edges. For each root u, let t_R(u) count red edges
inside its red neighborhood and t_B(u) blue edges inside its blue
neighborhood. The three profiles are

```
u=0: (degree,t_R,t_B) = (20,92,107)
u=1: (degree,t_R,t_B) = (20,93,107)
u=2: (degree,t_R,t_B) = (20,93,107).
```

They satisfy the selected hard-root caps t_R<=93 and t_B<=107.
These are properties of the exhibited graph, not a new proof of global
local-density bounds. The other forty hard-cap conditions are not all
imposed or satisfied.

An outside footprint uses bit u for red adjacency to core u. The 32
footprints, in vertex order 11,...,42, are

```
218,682,690,826,850,874,1186,1506,1546,
963,1099,1179,1299,
188,244,380,524,748,852,1236,1836,1988,
109,1181,1301,1589,
278,1030,1326,1934,
967,1655.
```

They are all distinct in this witness, although repeated footprints
were permitted by the model. Each same-signature group is sorted by
its core footprint. This is only a labeling choice, not an assumed
graph automorphism.

## Exact joint layer and remaining violations

Both colors are excluded on every five-set using zero, one, two or
three vertices outside K. Equivalently, K together with **any three**
of the 32 outside vertices induces a Ramsey(5,5) graph, and all those
subgraphs use the *same* outside-edge coloring. This is stronger than
choosing a different completion for each triple independently.

The complete census is:

| Outside vertices in the five-set | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|---:|
| Red K5 | 0 | 0 | 0 | 0 | 215 | 86 |
| Blue K5 | 0 | 0 | 0 | 0 | 202 | 85 |

Thus 417 remaining obstructions use four outsiders and 171 use five.
Examples are blue {0,11,16,18,27}, red {0,20,23,33,34},
red {11,13,15,20,37}, and blue {12,15,17,33,35}.
All C(43,5)=962,598 five-sets are inspected by the literal checker.
The 43 local profiles and the exact 35 hard-cap failures are retained
in [verification.json](verification.json). They are not inferred from
aggregate objectives or solver tolerances.

## Retained core-root union interface

For every disjoint red clique A and blue clique B inside K, with
|A|,|B|<=3 and not both empty, let C(A,B) be the vertices outside A union B
that are red to A and blue to B. Impose

```
|C(A,B)| <= U(5-|A|,5-|B|)-1.
```

Here U(1,q)=U(p,1)=1, and U(p,q) is the sum of U(p-1,q) and U(p,q-1),
minus one when both summands are even. The table for p,q=1,...,5 is

```
1  1  1  1  1
1  2  3  4  5
1  3  6  9 14
1  4  9 18 31
1  5 14 31 62
```

These are elementary upper bounds, in particular **U(4,5)=31**, not
the sharp bound 25. Their validity follows from the usual neighborhood
recurrence: with even summands r,s, a counterexample on r+s-1 vertices
would have every red degree r-1, impossible because both the order and
that degree are odd. C(A,B) can contain neither a red K_(5-|A|) nor a
blue K_(5-|B|), giving the stated necessary inequality.

The graph satisfies all 3,140 raw tests. The numerical-interface layer
was not dropped when adding joint edge consistency. In the CNF, fixed
incidences simplify each membership predicate, constant-true vertices
are subtracted from the bound, and the remaining conjunctions are
reified exactly. Identical residual count rows are kept at their
smallest bound. There are 2,478 nontrivial merged rows and 14,848
distinct nonconstant predicates, including single-literal predicates.
The literal checker reconstructs C(A,B) directly from the graph;
the bit checker independently intersects adjacency masks and uses the
displayed U table. Every resulting row is compared, not only totals.

## Discovery model and scope of its normalization

All 151 fixed pairs (55 core pairs and 96 root/outside contacts) are
retained. The **752 primary variables** are the 256 W/outside contacts
and 496 outside pairs, in lexicographic pair order. No particular
eleven-bit footprint, outside edge, or footprint multiplicity is
selected in advance.

For every five-set with at most three outsiders, retain both forbidden
monochromatic colors unless fixed edges already rule a color out. The
152,898 distinct primary clauses comprise 120 one-outside, 8,322
two-outside and 144,456 three-outside clauses; the fixed core is valid.
All 43 degree equations, three root-density intervals and all root-union
bounds are imposed on the same variables.

The degree profile implies t_R(u)+t_B(u)=201-d_F(u) for a degree-20 root,
where d_F(u) counts its red neighbors among the other two degree-20
roots. Indeed summing degrees in its 20-vertex red neighborhood and
using 450 total red edges gives this identity directly. Hence the
selected red intervals are 92..93 at the path center and exactly 93
at its leaves; the bit checker verifies the blue caps separately.

The only ordering is the eight-bit W-contact string within each fixed
root-signature group, in decreasing core-bit order. Arbitrary permutations
inside such a group preserve every pre-order constraint: fixed contacts,
degree requirements, the complete joint layer, root-density sums and
universally quantified root-union counts. Sorting those strings therefore
preserves coverage of this fixed-core/fixed-cell relaxation. Ties are
allowed. It imposes neither distinctness nor an automorphism.

The threshold and prefix-equality primitives in [encoding.py](encoding.py)
are copied from the earlier triple-graph and root20 discovery encoders,
whose source hashes are respectively
`0cf0264142d89472cb93358bc8f4ecf33d13b8996aba03672dd401133257e898`
and `02c9e9f9eb8c8f04fae7c4ae16568280408bf65c071501d9d6f7942f7bb40df7`.
They do not import either artifact's mathematical conclusion.

The CNF has **247,868 variables / 1,098,661 clauses / 24,928,537 bytes**,
SHA256 `c2c03d9187a58c3f49f7887862b4e3c190fd07710c8e13d4a895cde08b6b8862`.
After SAT, the generator checks every auxiliary and primary clause before
decoding. The final mathematical evidence is nevertheless the graph,
checked without the generator, cardinality encoding, or SAT solver.
No UNSAT or whole-formulation independent audit is claimed here.

## Reproduction and verification

CPython 3.11.2 and the standard library suffice for all graph checks.
From the repository root, choose fresh output paths outside Git:

```bash
python3 -B ramsey_r55_critical_path_joint3_realization/verify.py \
  --report /scratch/r55-joint3-verification.json
python3 -B ramsey_r55_critical_path_joint3_realization/bitcheck.py \
  --report /scratch/r55-joint3-bit-verification.json
python3 -B ramsey_r55_critical_path_joint3_realization/crosscheck.py \
  --report /scratch/r55-joint3-crosscheck.json
```

The first checker uses literal pairs and all five-sets. The second
uses bit-intersection clique recursion, a separate literal-core
representation, bit-count local profiles and the explicit U table.
[crosscheck.json](crosscheck.json) records entry-level equality of all
588 monochromatic clique masks and all 3,140 root-union rows, plus all
shared graph/profile fields. This is stronger than matching censuses.
Twelve invalid graphs are rejected by both checkers, including a
degree/core/footprint-preserving four-edge corruption that introduces
a forbidden K5 in the checked layer. That corruption is a verifier control,
not a resumed local-descent experiment.

Normal and optimized Python reproduce identical reports. These are
author-written independent implementations, not independent peer
review or proof-assistant formalization. Trust remains in the literal
definitions, exact Python/runtime/hardware and file identities. Neither
the SAT solver nor the optional generator is trusted for the exhibited
graph's claimed properties.

Optional discovery uses Kissat 4.0.4, source
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, binary SHA256
`2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`:

```bash
python3 -B ramsey_r55_critical_path_joint3_realization/generate.py \
  --work /scratch/r55-joint3-discovery --seconds 120 \
  --kissat /path/to/kissat
cmp /scratch/r55-joint3-discovery/graph.json \
  ramsey_r55_critical_path_joint3_realization/GRAPH.json
```

The initial all-bound production solved in 58.718 seconds and took
64.571 seconds overall. The fresh self-contained public-source replay
solved in 58.717 seconds and took 64.459 seconds overall, reproducing
the CNF and graph byte for byte. Peak child RSS was 212,556 and 212,860
KiB respectively. Both runs had a 120-second cap. Timings are machine
dependent, not a performance guarantee. [run.json](run.json) preserves
both observed records; its nested pending-audit status is the generator
stage, completed by the separate checker reports.

The 24.9 MB formulas, 47.9 MB SAT learned-clause traces and logs remain
outside Git. The traces are **not refutations or solver restart states**.
An initial pilot omitting root-union counts was satisfiable but violated
67 of those bounds; it is not the published witness. The retained-bound
model and direct checks resolve that failed intermediate milestone.

## Dependencies, coordination and next boundary

This follows the [six-way support obstruction](../ramsey_r55_critical_path_six_support),
source e5ed88bed9ae7e8aeadf3365d9feedd593e35444, Discovery Net height 3156,
`bafkreihibj5pskqwplkygs4fqr47avsmxw2vsbtlgeflhznlio47uuej7y`.
Its closed 32-footprint assignment is not retried. The earlier guarded
triple cut and this six-way cut remain preserved: the new model uses
variable footprints and an exact joint layer, not a claimed repair of
their impossible assignments. The prior fixed-H20 and degree-19 branches
are not reopened. No catalogue or automorphism exclusion is a premise.

New teammate height 3158 closed all six Core194 one-empty-signature cases;
independent review at height 3164 accepts the at-least-two-empty condition
while keeping the whole Core194 extension and 17 classes / 9,153 labels
open. Their READMEs were read, not replayed or imported here. The symmetry
lane remains separate. External height 3160's integrated 389-root OPB
for the different M=214 branch was read as a handoff, not solved or
semantically re-audited; it has no SAT/UNSAT verdict and is not a premise.
The incremental graph refresh through height 3167 found no feedback on
the six-support ancestor affecting this work.

This coherent milestone is complete, with no background job. The useful
next direction is the first missing four-outside K5 layer while keeping
footprints variable and retaining all existing constraints. Neither that
layer, a longer solve, a different core nor an outside-edge repair search
is started in this pass. A full target also needs the remaining hard
local conditions and all five-outside obstructions; no target is claimed.
