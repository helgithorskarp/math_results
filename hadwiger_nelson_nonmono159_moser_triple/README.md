# A 450-vertex three-copy family is four-colorable at every angle

Let `A` be the archived Parts 159-vertex nonmono gadget, with its published
origin, and fix

```
t = (5+i sqrt(11))/6
B = A union tA.
```

**For every rotation or reflection `g` fixing the origin, `B union g(A)` is
four-colorable.** The inner union has 292 vertices and 1,251 strict unit
edges. Adding the third copy gives at most 450 vertices. The theorem covers
arbitrary angles, including rotations outside the previously colored field.
It excludes this fixed-inner-placement family, not all three-copy
constructions, and produces no graph improving the 509-vertex record.

[PROOF.md](PROOF.md) gives the complete reduction. A new cross edge forces a
quadratic equation for an outside-field rotation. Equal irreducible monic
quadratics give exactly its complete cross-edge set. The finite part has
2,391 rotation classes and 2,216 reflection classes: 9,214 labeled isometries.
All are colored by a 1,679-byte library. Multipliers in the field and those
with no new cross edge are handled by the proof, so the angular quantifier
is universal rather than a finite grid.

## Reproduce

From this directory, with Python 3.11 or later:

```bash
python3 verify.py > /tmp/nonmono159-triple.json
cmp expected.json /tmp/nonmono159-triple.json
python3 audit.py > /tmp/nonmono159-triple-audit.json
cmp expected_audit.json /tmp/nonmono159-triple-audit.json
python3 check_example.py > /tmp/nonmono159-triple-example.json
cmp expected_example.json /tmp/nonmono159-triple-example.json
sha256sum -c SHA256SUMS
```

Only the standard library is needed. On the producing host, CPython 3.11.2
took 23.4 seconds for the main verifier, 12.3 seconds for the alternative
arithmetic audit, and 3.9 seconds for the direct examples; peak RSS was below
23 MiB for each. No solver is needed for replay.

| Verified quantity | Value |
|---|---:|
| Inner overlap / new inner cross edges | 26 / 18 |
| Inner union vertices / strict edges | 292 / 1,251 |
| Nonzero pairs examined per parity | 45,978 |
| Outside-field quadratic classes | 4,607 |
| Outside-field isometries with a new cross edge | 9,214 |
| Maximum new edges from the third copy | 30 |
| Uncovered classes | 0 |

`colors_A.txt` and `colors_B.txt` give complete component colorings. The
verifier checks their internal edges and searches the small library for a
valid gluing at every class. `audit.py` uses a different arithmetic
representation and polynomial normalization, then compares canonical
hashes of all pair classifications and edge partitions and independently
checks coloring coverage. `check_example.py` reconstructs all unit edges
for four explicit radical-coordinate unions.

The canonical edge-partition SHA-256 is
`88597ad1b67ec766486fd1befbe183649e92a776ea09350c5a44e4ebe919b04b`.
Complete histograms and further hashes are in `expected.json`.

## Dependencies and scope

The small coordinate input is reused from
`../hadwiger_nelson_nonmono159_214_lowden2/points159.tsv`.
The main checker reuses exact routines in the prior fixed-origin `census.py`
and its field module. The alternative checker separately reuses the prior
`audit.py`. All imported source and coordinate files are pinned by SHA-256.

The in-field branch depends on the published four-coloring of
`E=Q(i sqrt(3),i sqrt(11))`. The universal angular reduction is unformalized
algebra; the finite evidence uses exact rational or integer arithmetic and
explicit positive colorings. No approximate distances, UNSAT assertion,
large generated artifact, or solver trust is required.

This extends the earlier two-copy fixed-origin exclusion by adding the
specified second component inside `E`. The construction source is
[Parts' paper](https://arxiv.org/abs/2010.12665); no novelty claim is made for
the general quadratic or coloring-gluing mechanisms.
