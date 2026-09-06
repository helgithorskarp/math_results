# Full propagation of five local saturated-neighborhood obstructions

Fix a hypothetical Ramsey(5,5;43) graph with order-three action `1^10 3^11`
in the four-red/seven-blue moving-triangle split. Use the accepted full
normalization: internally red triangles C0,...,C3, internally blue triangles
C4,...,C10, and fixed vertices 33,...,42. The first fixed vertex e=33 is
blue to all twelve red-core vertices by the reviewed forced-empty theorem
and existing lexicographic fixed-row order.

Let b count the internally blue moving triangles blue to e, and h its red
neighbors among the other nine fixed vertices. Then

```
d_red(e)=3(7-b)+h,  d_blue(e)=21+3b-h.
```

The inherited degree window 18..24 gives b<=4. When b=4, necessarily h=9:
e's blue neighborhood is exactly 24 moving vertices, on four red and four
blue triangles. It contains no red K5 and no blue K4.

The preceding [local neighborhood theorem](../ramsey_r55_order3_eleven_neighborhood24)
refutes this exact induced-neighborhood condition for cores
**124,155,159,168,180**. The induced local formula covers every choice of
four blue triangles in the full graph by forgetting external incidences
and freely relabeling the four selected blue cycles. It imports no full
normalizer. Its five full DRAT refutations were each replayed twice.
Consequently every full normalized extension of these five cores has b<=3.
During this pass the local premise received an [accepted independent review](../ramsey_r55_order3_eleven_neighborhood24_review1),
source `32775f8609d663966c40c32a4207829421ef9dd9`.

Core194 has an explicit valid 24-vertex local graph, so it receives no such
bound here. The other twelve current full-core classes already have b<=3
from a different, independently accepted maximal-branch result and were
tested in the preceding full-propagation pass. They are not retested.
The present theorem concerns the same first fixed vertex e throughout;
it does not change the normalization or assert a property of every empty
fixed vertex.

## Complete full formulas

For each selected core c, take its unrestricted full base F_c from
[empty-signature propagation](../ramsey_r55_order3_eleven_empty_propagation).
Retain the entire 43-vertex parent, all eighteen core units, the intrinsic
anchor constraints, the forced empty prefix, and all 1,440 sharp
singleton/pair cuts. These are exactly the previously published full bases,
with their exact hashes checked again. All five have two complementary
blue-triangle-free anchors, 34,300 variables and 617,482 clauses.

The seven primary variables 215,...,221 indicate red links from e to the
seven internally blue moving triangles. Append all 35 positive clauses
on four-subsets of these variables:

```
OR_(v in S) v       for every S subset {215,...,221}, |S|=4.
```

They prohibit four simultaneous blue bits, equivalently enforce b<=3 or
at least four red links. All counts four through seven remain allowed
subject to the full base. No fixed edge is newly fixed. There is no new
auxiliary variable, no deleted base clause, and no normalization change.
Each resulting complete formula has **34,300 variables / 617,517 clauses**.

The full local-to-global argument has two alternatives: a normalized full
extension would have b=4, already refuted by its induced neighborhood, or
would model F_c plus the 35-clause tail. An UNSAT certificate for that full
formula therefore excludes the **whole core**. A timeout gives no conclusion.
The same positive-tail bridge was independently accepted for the previous
nineteen-case propagation; this pass supplies five different premises and
five different complete inputs.

Three formula roles must stay distinct:

1. F_c is the unrestricted complete 43-vertex base and is the input here.
2. The old maximal b=4 child fixes exactly three red moving links and nine
   fixed red edges. Adding the new tail to it would create an irrelevant
   contradiction; it is explicitly rejected as a base.
3. The 84-variable local 24-vertex formula has different primary IDs and
   omits the external nineteen vertices. It is used only for the imported
   neighborhood obstruction and is explicitly rejected as a full base.

## Reproduction and verification

The generator pins the local result, fresh verification and boundary,
the unrestricted-base result, and the current full-core boundary. It
selects all and only the five certified local exclusions and matches
index, core bits, labeled multiplicity and anchor data to the full bases.
Both recorded local proof replays must be verified. The source contract
contains the transitive full-base reconstruction chain, the local proof
sources and inputs, the preceding full-propagation evidence, and the six
new production/checking scripts.

Preparation reconstructs all 25 historical unrestricted bases through
an isolated module namespace. It exactly compares the whole preceding
preparation and each complete base identity against the public record.
Only the five selected bases receive the tail and solver test. The other
historical bases are reconstructed for identity checking, not retested.

The new auditor imports no producer. It independently recovers the 320
primary variables from literal edge orbits on 43 vertices, checks every
unrestricted base byte, derives the 35 clauses, and checks header and EOF.
Its complete truth tables inspect all 128 moving patterns and 65,536
moving/fixed incidence assignments. Exactly 64 moving patterns satisfy
the bound; all 17,728 degree-valid complementary incidence assignments
satisfy the tail. Fourteen malformed inputs are rejected, including a
local24 formula, a maximal-branch child and an unproved Core194 case.
Normal and optimized control reports must match.

The bounded run uses two workers, twenty-second Kissat caps, and mandatory
full DRAT replay including any RAT steps. Fresh verification reconstructs
every complete base and all five strengthened formulas again, then
replays every new full refutation a second time. A SAT target claim would
instead require a compact 43-vertex edge list and literal verification of
all five-sets. UNKNOWN is inconclusive, and partial traces are neither
refutations nor resumable solver states. The completed outcome is in
README and the compact reports.

## Scope and imported trust

The full parent, core cover, intrinsic-anchor strengthening, forced-empty
result, Core123 exclusion, nineteen earlier maximal-branch exclusions and
seven preceding whole-core exclusions have accepted independent reviews
at their stated scopes. Older empty-signature-specific whole-core closures
remain the review boundary for cumulative counts. The five local obstructions and their transfer received independent
acceptance during this pass. The review independently reconstructed all
six local formulas, regenerated the five exact proof traces with a
different Kissat binary, fully replayed them, and checked the Core194
witness. The present full propagation and Core159 certificate await review.

The degree window imports R(4,5)=25 through the parent. Ordinary
unformalized reductions, exact source, interpreter/compiler/hardware,
SHA256 identity and the full DRAT checker remain trusted. Internal
independent reconstruction and repeat replay are not peer review or
proof-assistant formalization. Compact hashes are not substitutes for
refutations. No complete eleven-cycle exclusion or Ramsey lower-bound
improvement follows from a partial core closure.
