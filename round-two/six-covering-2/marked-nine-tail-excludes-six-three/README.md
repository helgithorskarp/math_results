# Exact nine-tail six/three exclusion

Author: **six-covering-2**, researcher. Conditional ordinary proof;
unformalized and independently unreviewed.

[proof.md](proof.md) excludes productive TAIL counts(6,3) for distinct ORIGINAL
moduli dividing10080, minimum EXACTLY8, literal
`8:0,9:0,10:1,14:0,12:10,16:2,28:4,32:6`, with essential16/32.
All other original selections, phases and omissions are free; unproductive
selected tails and proper-divisor actual LCMs are allowed. BASE means selected
originals dividing2520; productivity refers to its ACTUAL holes.

Imported published premises: BASE holes>=177 (9934), productive tails>=9
(10022), and the two-parent theorem10054 for the resulting four-pair frontier
(2,7),(3,6),(4,5),(5,4). This does not establish ten productive tails, a
full-prefix exclusion, a covering construction or a new global L_min(8) bound.
Review10066 confirms10022 relative to the old eight-tail result; its scoped
weaker16 variant and verdict are not transported to this proof.

Python3.11+; standard library only. From this directory:

```sh
python3 -I -B verify.py --mode normal --out-dir repro-normal
python3 -I -B -O verify.py --mode optimized --out-dir repro-optimized
```

Use fresh output directories. Each run rebuilds all records and streams from
source only, with ten serial20-second children and native threads1. Failure,
interruption or timeout does not prove nonexistence. The recorded campaign
cold replay also applies55 seconds per mode and its unchanged1CPU/2GiB scope.
A slower machine may report INCOMPLETE; do not treat that as an exclusion.

The complete producer and same-author independent-method checker records and
raw streams must agree. [expected.json](expected.json) pins all eight whole
files and compact expected census. Expected results:137963 canonical phase
rows covering17393805 raw tuples,113 repair sets;1045363 final BASE phase rows,
all excluded with deficits18..63. Per mode73 semantic record damages and nine
raw damages must be rejected AFTER full fresh independent arithmetic.
The scripts need no graph, network, solver, private pilot or other source tree.
Large generated evidence and histories are omitted from publication.

Read proof.md for the complete lossless symmetry reduction, actual-hole and
original-label semantics, free BASE/omission bridge, imports and trust boundary.
Source publication is not an independent reviewer verdict.
