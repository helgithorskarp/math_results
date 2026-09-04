# Two non-killing deletion triples in the Parts sealed pool

**Claim status: exact computer-assisted lemma, with regenerated and checked
DRAT proofs.** This is a certificate-semantics audit. It gives no graph below
509 vertices and does not close the six-addition replacement problem.

Use the exact indexing and sealed pool from the committed
[shape reduction](../hadwiger_nelson_parts509_pool_shape_closure). Write
`L = {0,...,373}`, let `S = {374,...,508}`, let `Q5` be its 168 specified
completion points, and put `U = S union Q5`. A set `D subset U` is a
*killing set* if `L union (U minus D)` is four-colourable.

> Neither `D1 = {374,375,383}` nor `D2 = {396,412,479}` is a killing set.

The exact induced graphs after these deletions have:

| deleted set | vertices | unit edges | SAT variables | clauses |
|---|---:|---:|---:|---:|
| D1 | 674 | 3,363 | 620 | 6,589 |
| D2 | 674 | 3,359 | 620 | 6,573 |

Both formulas are UNSAT with checked DRAT proofs.

## Why this matters for the unfinished certificate

These triples occurred with empty addition-side repair sets in an unpublished
six-addition master. That draft treated every such row as a direct killing
set and requested a full-pool colouring witness. The lemma proves that these
two requested witnesses cannot exist.

A different argument can still justify a deletion constraint under a budget
of six additions. For example, if the union of the single-deletion repair
families for the triple has transversal number at least seven, its deletion
constraint follows at that budget. That auxiliary statement is a separate
proof obligation. The present lemma does not assert that the budgeted
constraints are invalid, nor certify those transversal bounds.

More generally, a direct killing-set witness proves four-colourability with
*all* completion points outside the killing set present. A bounded-addition
constraint may have a different justification. A certificate must preserve
that distinction when importing constraints. No priority claim is made for
the two induced-graph observations.

## Encoding and proof

The existing [interface lemma](../hadwiger_nelson_parts509_interface_lemma)
classifies the restrictions of all proper four-colourings of `L` to its
19 interface vertices into 20 classes, up to colour permutation. Each class
has a published full colouring witness for `L`. All 36 edges from `L` to
`U` end at this interface.

For each deletion triple, use two Boolean bits for the colour of each of
the 300 retained pool vertices. For each internal unit edge and each of the
four colours, a four-literal clause forbids both endpoints having that
colour. Add 20 interface selectors and one clause requiring at least one
selector. For each cross edge and each selector, a three-literal clause
conditionally forbids the pool endpoint from taking the colour of its
fixed `L` neighbour.

A satisfying assignment extends at least one published `L` colouring.
Conversely, by interface completeness, a four-colouring of the full graph
can be globally permuted to extend one of the 20 representatives, and
therefore satisfies the formula. Requiring exactly one selector is
unnecessary: any true selector supplies a valid extension witness.
Thus the two checked UNSAT formulas prove the lemma.

## Reproduction

From a checkout of this repository, install Python 3.11 and
`sympy==1.14.0`, Kissat 4.0.4, and `drat-trim`. GNU `timeout` bounds each
solver/checker invocation to 180 seconds, with a five-second kill grace.

```sh
python3 hadwiger_nelson_parts509_non_killing_triples/verify.py \
  --work /tmp/parts-non-killing \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

The script reconstructs exact coordinates and all unit edges, checks the
published `L` witnesses, generates both formulas, regenerates both proofs,
and requires successful `drat-trim` verification. It compares each case
with the compact dimensions and hashes in `expected.json`. Run without
Python optimization flags. The generated `result.json` records proof hashes,
sizes, and times. Generation and checking took about 1.6 seconds per formula
on the producing host, after geometry reconstruction.

As a positive control, the published colouring for the genuine killing set
`{486}` is checked both against the graph and as a satisfying assignment of
the new encoding. The script rejects a formula that excludes this witness.

The retained local proofs had sizes 910,108 and 802,599 bytes. CNFs, proofs,
and logs are omitted from git; the source regenerates them in the requested
work directory. `toolchain.json` records the producing binary hashes.

## Trust boundary and source

The new two-bit encoding and DRAT replay supply the SAT evidence. The script
uses the committed shape contribution's exact geometry parser, whose
arithmetic is in `Q(sqrt(3),sqrt(5),sqrt(11))`, with denominators cleared
before unit-distance tests. Its source inputs are the published Parts
coordinates, the committed exact completion coordinates, and the committed
pool list. The source construction is described in
[Parts's paper](https://arxiv.org/abs/2010.12665).

The full-graph conclusion inherits completeness of the 20-class interface
classification; this script checks its explicit witnesses and interface
boundary but does not re-enumerate that classification. The bridge from
colourings to SAT and the exact arithmetic implementation are ordinary
reviewable mathematics and code, rather than proof-assistant formalizations.
