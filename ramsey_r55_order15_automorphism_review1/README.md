# Independent review evidence for the order-15 Ramsey obstruction

This directory contains reviewer-1's clean-room audit of the claim that a
Ramsey `(5,5;43)` graph cannot have an automorphism of order 15.

The standard-library checker imports none of the submitted implementation and
does not invoke a SAT solver or external proof checker. It:

1. enumerates all order-15 permutation types and independently applies the
   order-five and order-three power restrictions;
2. classifies unordered-pair orbits analytically: within a cycle by unsigned
   cyclic difference, and between cycles by the position difference modulo
   the gcd of their lengths (complete by the Chinese remainder theorem);
3. rebuilds all projected Ramsey clauses for each of the six surviving types
   and matches every canonical CNF hash; and
4. checks every retained proof addition directly, first by reverse unit
   propagation and otherwise by the RAT pivot condition over every active
   opposite-pivot clause. Legal proof-introduced variables are tracked from
   their checked introduction onward. Each trace ends with a RUP empty clause.

Run from the repository root with CPython 3.11 or later:

```bash
python3 ramsey_r55_order15_automorphism_review1/independent_verify.py \
  ramsey_r55_order15_automorphism_obstruction
```

The checker prints one `PASS` line per cycle type followed by an aggregate
line. The complete expected transcript is in `expected_output.txt`; its final
line is:

```text
PASS all_cases=6 final_empty=6 total_rup=7287 total_rat=234
```

The six expected CNF hashes and proof hashes are embedded in the source, and
malformed, incomplete, non-RUP, or non-RAT traces fail closed.

The power filter imports two mathematical results: order-five elements have
seven or eight 5-cycles, and order-three elements have at least seven
3-cycles. Reviewer-1 previously audited all six excluded order-five types. In
this pass the order-three motion bound was re-derived directly: around a
monochromatic moving triple its same-color common neighborhood has size at
most four, giving color degree at most `2k+4` for `k` moving triples, while
`R(4,5)=25` gives degree at least 18. Thus `k>=7`.

The remaining trust boundary is CPython integer/container behavior, SHA-256
and xz decompression, the checked-in proof bytes, the transparent Ramsey-CNF
bridge, and the two imported Ramsey numbers `R(3,5)=14` and `R(4,5)=25` used
by the order-three dependency. This is not a proof-assistant formalization.
It proves a restriction on automorphisms of a hypothetical target graph, not
existence of such a graph or `R(5,5)>=44`; it also does not prove that 15
cannot divide the automorphism-group order.
