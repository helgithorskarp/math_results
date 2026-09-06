# Universal propagation of four local neighborhood obstructions

Let G be a hypothetical Ramsey(5,5;43) graph admitting the order-three
action `1^10 3^11`. In the four-red/seven-blue internal triangle split,
write C0,...,C3 for the red moving triangles and C4,...,C10 for the blue
ones. Fix the red core in one of these canonical representatives:

| Core | Cross words in pair order 01,02,03,12,13,23 | Labeled cores |
|---|---|---:|
| 124 | 000110110011101110 | 324 |
| 155 | 100100110001101110 | 648 |
| 168 | 100100110011110110 | 324 |
| 180 | 100100110101100110 | 648 |

The [accepted local obstructions](../ramsey_r55_order3_eleven_neighborhood24)
exclude an invariant 24-vertex graph on four red and four blue triangles,
with that same red core, no red K5, and no blue K4. Their formulas impose
no fixed vertices, degree constraints, phases, row order, or other full
normalizers. Their [independent review](../ramsey_r55_order3_eleven_neighborhood24_review1)
reconstructs the formulas and regenerates and checks the refutations.

## The distinguished empty vertex can be any fixed vertex

Choose any fixed vertex e blue to all four red moving triangles. Let b be
the number of blue moving triangles blue to e, and let h be its number
of red neighbors among the other nine fixed vertices. Invariance makes
each fixed-to-cycle incidence uniform, so

```
d_red(e) = 3(7-b)+h,     d_blue(e) = 21+3b-h.
```

The inherited degree window 18..24 and h<=9 imply b<=4. If b=4, the
lower bound on d_red forces h=9. Then N_blue(e) consists of precisely
the four red moving triangles and four selected blue moving triangles,
with no fixed vertices. Its induced graph H has no red K5 by heredity.
It has no blue K4 because such a set together with e would be a blue K5.

Keep vertices 0,...,11 of the red core exactly labeled. Relabel only
the four selected blue cycles as local C4,...,C7, preserving the direction
of the order-three action. Forget all other vertices and external edges.
The resulting H satisfies the refuted local formula. This contradiction
holds for all 35 choices of blue cycles and for every choice of fixed e.
Consequently **b<=3 at every empty-signature fixed vertex** in each of
the four full core classes.

The previous local report introduced e using the first normalized row.
The argument here establishes the stronger quantifier directly from the
unrestricted local formula. It does not relabel fixed rows in a normalized
full formula, and it does not assume that a second fixed vertex is empty.
Core159 satisfies the same local argument but its whole extension is
already excluded; it is not tested again. No universal transfer is asserted
for the other historical first-row bounds whose proof had extra hypotheses.

## Exact full clauses and completeness

Let L(f,i) denote a red incidence from fixed f to moving cycle i. In the
inherited primary numbering,

```
L(f,i) = 211 + 11*(f-33) + i,    f=33,...,42, i=0,...,10.
```

For each f and every four-subset S of {4,...,10}, append

```
L(f,0) OR L(f,1) OR L(f,2) OR L(f,3) OR OR_(j in S) L(f,j).
```

A nonempty red-core signature satisfies these clauses automatically.
For an empty signature they prohibit four simultaneous blue links to
blue cycles, equivalently requiring at least four red links among those
seven cycles. Thus the clauses encode exactly the proved implication.
There are 350 positive eight-literal clauses, adding 11,900 bytes and
no new variables, fixed-edge units, or normalizers. The first row's
existing empty-prefix units simply make its four guard literals false.

For each core, the complete unrestricted base F is rebuilt from
[empty-signature propagation](../ramsey_r55_order3_eleven_empty_propagation).
It contains the complete parent, eighteen core units, the two intrinsic
anchor constraints, the first empty prefix, and the sharp pair cuts.
All its clauses are retained: 34,300 variables / 617,482 clauses become
34,300 variables / 617,832 clauses. The old maximal b=4 child would be
an invalid base, since it assumes the very branch now excluded. Neither
an 84-variable local formula nor a previous first-row-strengthened child
is substituted for F. The base identities are pinned in cases.json.

Every hypothetical graph in the full core class has a normalized
representation satisfying F, by the imported completeness reductions,
and satisfies the new clauses by the universal argument above. A checked
refutation therefore excludes its whole extension class. UNKNOWN excludes
nothing. A SAT target must be decoded and checked literally for every
five-set, as well as order-three invariance and the intended core.

## Verification and trust boundaries

The isolated reconstruction rebuilds the complete parent and preparation,
matches the earlier preparation entry by entry, and reconstructs only
the four selected unrestricted bases. An auditor importing no producer
recovers the full primary numbering from physical edge orbits, verifies
every base byte, every new clause, the header and EOF.

It also constructs all 350 physical neighborhood restriction maps. Each
keeps the twelve red vertices pointwise, commutes with the cyclic action,
preserves the 84 local cross-edge orbits and internal colors, and forgets
exactly nineteen vertices including the distinguished fixed vertex.
There are zero red-core or fixed-row relabelings. This finite audit checks
the representation map; the hereditary clique argument above supplies
the logical implication.

Truth tables exhaust 20,480 row assignments, retaining per row all 1,920
nonempty-signature patterns and precisely 64 empty-signature patterns.
The degree bridge checks 65,536 empty-vertex moving/fixed incidence
patterns, including all 17,728 admissible complementary patterns.
Sixteen malformed cases or formulas must be rejected under normal and
optimized Python. Fresh verification independently rebuilds all four
complete formulas, repeats these controls, and requires a second full
DRAT replay for any exclusion. RAT steps must be checked.

The local refutations, parent, core cover, anchor and forced-empty
theorems have accepted reviews at their stated scopes. The new universal
transfer and full test have author checking and await independent review.
Older empty-signature-specific whole-core exclusions retain their
cumulative-count review boundary. The separately accepted Core194
maximal-branch review changes historical review coverage but is not a
premise for any of these four local obstructions.

The degree theorem imports R(4,5)=25 through the parent. Unformalized
reductions, exact source, interpreter/compiler/hardware and hash identity
remain trusted; any refutation additionally relies on the full DRAT
checker. Internal reconstruction is not independent peer review or
proof-assistant formalization. No new Ramsey lower bound follows here.
