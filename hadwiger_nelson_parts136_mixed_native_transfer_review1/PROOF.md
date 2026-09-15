# Proof and review analysis

## 1. Exact coordinate model

Each real coordinate is represented at denominator 96 in the ordered basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

The three square roots are independent, so the eight coefficient vectors give
exact equality in `Q(sqrt(3),sqrt(5),sqrt(11))`. The review checker multiplies
basis elements by bitmask xor, multiplying by 3, 5 or 11 whenever a radical
factor occurs twice. This is different from the target checker's gcd-based
squarefree-radicand multiplication.

The Parts509 table already uses denominator 96. The archived A159 and B214
tables use denominator 12, so their coefficient rows are multiplied by eight.
The three review inputs are byte-identical to the earlier receiver and donor
source files and are independently hash-pinned.

## 2. Physical support and complete edges

Set

```text
H = {P_0} union {P_374,...,P_508}.
```

Exact tuple intersections give

```text
H intersect A = {P_0},
H intersect B = empty,
A intersect B = empty.
```

Consequently the 136+159+214 formal labels merge to 508 physical points.
The checker squares all `508 choose 2 = 128,778` differences and obtains
2,187 unit pairs. The complete set is exactly the disjoint union of the 564
host edges, 646 A edges and 977 B edges. There is no omitted cross contact.

The independently generated point, edge and full squared-distance stream
hashes agree with the source package entry for entry:

```text
points    1775cb1c53e345070a6260b8cfb5ae7d606dc4e52df527d72b8b974ac2e32710
edges     40e0b2e928656f6c7f0cc27372961732128701d1ac0947491c8cee491284bbd6
distances a13e40a63847a97c1de9c52fe93004665c485f7d1feb63ef44aee95bdf563e61
```

## 3. Universal host extension

Let `c` be any proper four-colouring of `H`. The certificate supplies a proper
four-colouring `a` of `A`. Since colour names have no intrinsic meaning,
compose `a` with a permutation taking its origin colour to `c(P_0)`. This is
still proper and now agrees with `c` at the only shared point. There are no
other `H`--`A` edges. A fixed proper colouring of the disjoint `B` completes a
proper colouring of the whole graph.

Thus every proper host colouring extends. Since `H` is induced, restricting a
whole-graph colouring to `H` proves the reverse containment. Hence the
projection of the whole four-colour relation onto all host vertices equals
the complete host relation.

The 41,025 canonical nineteen-pin patterns are not a premise of this argument.
Their survival is a corollary using the separately independently reviewed
receiver census. This review checks that the source word uses the first saved
receiver fixture and that the fresh word uses the second.

## 4. Exact chromatic number

The fresh 508-symbol word is checked directly on all 2,187 edges. It differs
from the target word on every component, so the reproduction is not merely a
copy of the author's witness.

Seven host vertices induce the 11-edge Moser spindle. Exhausting all 2,187
maps from its vertices to three colours finds no proper word. The complete
union is therefore not three-colourable, while the fresh word makes it
four-colourable. Its chromatic number is exactly four.

## 5. Scope and trust boundary

Completeness applies to the one fixed coordinate union, not to a placement
family. The result proves neither that all A159/B214 placements are neutral
nor that every 372-point replacement of Parts136 is four-colourable. New
private contacts would invalidate the one-vertex-sum argument and require a
new complete physical check.

The proof trusts Python arbitrary-precision integers, the standard
multiquadratic basis fact, the three pinned coordinate files and the compact
review checker. Kissat produces the fresh positive word only; direct checking
removes solver soundness from the theorem. No floating-point predicate or
negative SAT result is used.
