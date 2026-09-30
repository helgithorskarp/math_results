# 480 extreme-event multisets for the thirteen-input P19 frontier

Author and executing agent: **six-sorting-1, researcher**.

This exact quotient replaces 3,018,600 effective extreme-profile words
by **480 comparator multisets**. There are 135 classes with ten events
and 345 with eleven events. Among the eleven-event classes, 48 repeat
one comparator twice; discarding them would lose admissible cases.

The target is the 158-state eleven-wire Boolean image B11 of the literal
22-comparator prefix in `fixture.json`. Internal ports 0..10 represent
original ports 1..11. The complementary
[P19 minimum reduction](https://github.com/helgithorskarp/math_results/tree/main/sorting13_P19_binary_minimum_reduction)
proves that a 44-comparator thirteen-input sorter beginning with its
literal P19 prefix exists if and only if B11 has a 22-comparator sorter.
The quotient partitions this conditional frontier. The unrestricted
thirteen-input interval remains 44..45; B11 remains 22..23.

Run standard-library Python 3.11+ without `-O`:

```sh
python3 generate.py
python3 verify.py
```

The generator uses forward reduced profiles and dynamic programming.
The checker imports no generator: it reconstructs original thirteen-wire
profiles from distinct scalar ranks and inverse fibers, then explicitly
enumerates every terminal effective word. It compares the entire
480-entry class/count table and parent graph hashes, checks all 8192
original Boolean inputs, and verifies the known 23-comparator control.
No solver, operational cutoff, or proof corpus is needed for these two
commands. The checker is a separate algorithm by the same researcher,
not an external review or a formal proof.

Expected class-table SHA256:
`5ac42c7b2ec5cc5485ea107338ddd20eaf9f8e5a56a6cbb8aa3e87e803799042`.
The compact certificate stores `[decimal multiset code, event count,
number of effective words]`. Each lexicographically ordered active
comparator occupies two bits of the code. Codes are decimal strings
because they exceed ordinary JSON floating-point precision.

`generate.build_class_graph(fixture, code)` constructs the finite quota
graph for any certified class. It retains every permitted effective
event order and every profile self loop. Effective occurrences spend
one unit of their comparator's multiplicity; self loops spend none.
The repeated-gate example class has 158 states and 1402 labelled edges.
Boolean sorting constraints and a 22-comparator word budget must be
supplied by the construction-search caller. The quotient does not
permit freely reordering gates or moving all effective events first.

[PROOF.md](PROOF.md) supplies the repetition lemma, coverage argument,
precise dependencies, and trust boundary. `source-manifest.json` pins
the seven accompanying files. The established pruning bridge, S(11)=35,
and earlier prefix theorems remain explicit mathematical imports.
