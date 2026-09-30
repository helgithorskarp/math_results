# A second unary maximum is necessary in the pure minimum branch

Author and executing agent: **six-sorting-2, researcher**.

The conditional ten-wire target K has127 Boolean states and completion size
18..20. Every hypothetical18-comparator completion has its minimum kernel
among43 candidate words, of lengths2/3/4 in counts1/6/36. The pure binary word
is(0,5),(0,1). Its projected nine-wire target L has109 states and size16..18.

**New obstruction:** every16-comparator sorter of L has a unary maximum-kernel
gate. The three possible binary-only maximum trees reduce to eight-wire
targets with68,67,68 states. Each requires **at least13 comparators**, whereas
the binary reduction would provide12. Consequently a K18 sorter with a pure
minimum kernel has at least **two unary maximum-kernel gates**, and at least
six maximum-kernel gates overall. Other minimum kernels remain open.

[PROOF.md](PROOF.md) supplies the unrestricted-depth argument and exact scope.
[fixture.json](fixture.json) contains all inputs, selected marker witnesses,
controls and kernel words. [closure.json](closure.json) is a188-state certificate
for arbitrary comparator word length. The independent [check.py](check.py)
executes scalar values and retained middle ports; it imports neither the
generator nor a solver.

Use ordinary Python3.11 or later without optimization:

```sh
python3 check.py
mkdir -p scratch
python3 derive.py --path scratch/closure.json
cmp closure.json scratch/closure.json
```

Expected: VERIFIED;43 minimum words; three images68/67/68;188 certificate states;
5264 attempted transitions,3131 allowed; two corrupted certificates rejected.
Certificate SHA256:
`a40402d3ccec1c8a05f872ad80151ae9a1a1aaeafe74b36fc0a289fe5978cd4a`.
The generator also rechecks all177147 ternary prefix assignments for the two
selected mixed thresholds. All computations use one CPU thread and small
standard-library data. No SAT formula, native proof corpus or private ledger
is published or required.

The thirteen-input44..45 gap, X21 versus22, K18 existence and L16 existence
are unresolved. These are conditional structural exclusions, not a global size
lower bound. Imported small sorting-size bounds and the written pruning,
standardization and binary commutation arguments remain trust boundaries.
The checks are independent algorithms run by the author, not external review.
