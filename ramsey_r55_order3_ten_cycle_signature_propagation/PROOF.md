# Excluding the remaining ten-cycle branch with twelve units

**Computer-assisted result.** All four full-extension formulas described
below are UNSAT with independently replayed DRAT proofs. Subject to the
inherited internal-color, matching and phase reductions, no Ramsey
`(5,5;43)` graph has an order-three automorphism of type `1^13 3^10`.
Combining with the preceding minimum-ten theorem raises the minimum to
eleven moving cycles. The principal unreviewed inherited boundary is
specified at the end; the new closure itself has internal checking only.

The scope is the surviving four-versus-six internal-color branch of an
order-three action of type `1^13 3^10` on a hypothetical Ramsey `(5,5;43)`
graph. Triangles `C_i={3i,3i+1,3i+2}`, `0<=i<10`, move; vertices 30..42
are fixed. The first four triangles are internally red and the last six
internally blue. A primary Boolean variable is true precisely for a red
edge orbit under this action.

The inherited matching and phase reductions put the first twelve vertices
in the unique core H: red cross differences are `{0}` on pairs 01 and 23,
and `{0,1}` on pairs 02,03,12,13. The four remaining anchor profiles,
indexed 64,65,67,69 in the original list, have phase triple `(0,0,0)`.
This is the full four-case parent cover, not an additional selection.

For a fixed vertex f, let its minority signature be the set of triangles
`C_i`, `i<4`, to which it is red. The
[fixed-signature lemma](../ramsey_r55_order3_fixed_signature_bound/PROOF.md)
proves that at most ten fixed vertices have a nonempty signature. There
are thirteen fixed vertices, so at least three are blue to all of H.
That lemma and its equality case have an
[accepted independent review](../ramsey_r55_order3_fixed_signature_bound_review1).

The parent formula sorts the thirteen ten-bit fixed incidence rows in
ascending lexicographic order, with minority coordinates first. Every row
whose first four bits are zero precedes every row with a nonzero prefix,
regardless of the final six bits. Consequently positions 30,31,32 are
blue to H. The audit checks all `64 * 15 * 64 = 61,440` comparisons.

There are 135 moving-to-moving primary variables and 78 fixed-to-fixed
variables. The remaining 130 primary variables, indexed in fixed-vertex
then moving-triangle order, have indices

```
variable(f,i) = 214 + 10*(f-30) + i.
```

The necessary blue assignments are exactly

```
-214 -215 -216 -217
-224 -225 -226 -227
-234 -235 -236 -237
```

Each displayed literal is a separate unit clause. Each represents three
literal edges, giving exactly the 36 edges from 30..32 to H. The checker
reconstructs the actual permutation's unordered-pair orbits independently
of this indexing expression. It checks both the selected 36 edges and
that these variables represent no other edges.

These units impose neither an ordering among equal complete incidence
rows nor any mutual edge colors on the fixed vertices. No M=214 degree
profile, extra automorphism, or equality assumption `z=3` is imposed.
The units permit more than three empty minority signatures.

## Preservation of the parent encoding

The full base has 28,950 variables and 927,000 clauses. Every base clause
is preserved byte for byte after the DIMACS header. The 334-clause phase
layer is unchanged: 298 simultaneous matching/mixed-row constraints,
27 anchor units and nine phase units. Adding twelve units gives
28,974 variables and 927,346 clauses per case. Repeated-edge degree
counters at fixed vertices, all five-set constraints, and all inherited
auxiliary gates remain in place.

Production regenerates the base from source and reconstructs it using
the sibling C++ checker, then checks each full extended formula. The
layer checker compares the base bytes and the entire additional clause
multiset against the parent's independently reconstructed phase semantics
plus the literal-orbit units. Five deliberately malformed formulas must
be rejected by this same checker.

Any hypothetical target in the parent branch has a normalized labeling
satisfying these units. The four verified UNSAT results therefore exclude
every case in the cover. There were no timeouts. A SAT model would have
had to decode to a literal 43-vertex edge list and pass every five-set
check; a time-limited UNKNOWN result would have supplied no exclusion.

## Inherited trust boundary

The normalization, source semantics, Python/C++ execution, SHA256 and
hardware are unformalized trust boundaries. The signature bound and
unique-core reduction have accepted independent reviews, but those
ten-cycle applications still import the older
[four-versus-six internal-color split](../ramsey_r55_order3_ten_cycle_obstruction).
Its five exclusions were internally reconstructed and their proofs
replayed; the cited reviews do not independently recheck those five
exclusions. This checkpoint does not close that review boundary.

No solver status is promoted to a theorem without its appropriate
certificate. The deterministic formula hashes are reproducible;
wall-clock-bounded solver paths and their partial trace hashes can vary
with scheduling and hardware.
