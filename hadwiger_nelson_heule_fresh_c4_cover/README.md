# An exact fresh-centre four-cycle is four-colourable through order 509

This package closes one concrete non-Parts construction support based on
Heule's exact 510-point unit-distance graph `H510`.  Adjoin the four exact
whole-plane completion centres

```text
1239, 1370, 1522, 1371.
```

They induce precisely the chordless unit four-cycle

```text
1239 -- 1370 -- 1522 -- 1371 -- 1239.
```

After collision checking and complete all-pairs unit-edge reconstruction, the
parent has 514 distinct points and 2,525 strict unit edges.  The four new
points have old-H510 attachment degrees `4,5,4,4` and 13 distinct old
neighbours.

**Exact computer-assisted result.**  For every old H510 vertex `v`, the
certificate gives a proper four-colouring of the parent after deleting `v`.
Consequently every subgraph of this fixed parent on at most **509** vertices
is four-colourable.  Indeed, such a subgraph omits at least five parent
vertices; because only four parent vertices are fresh, at least one omission
is old, and the corresponding singleton word restricts to the subgraph.

In particular, every 508-point exchange retaining the entire four-cycle and
deleting six old points is four-colourable.  This is a fixed-support
exclusion, not a global theorem and not a record improvement.  It says nothing
about other subsets of the 122 fresh centres, points outside that census,
geometric deformations, or unrelated exact forcing cores.  The published
record comparison remains Parts's 509-point five-chromatic strict plane
unit-distance graph.

## Exact physical gate

Coordinates lie in
`Q(sqrt(3),sqrt(5),sqrt(11))`, represented in the ordered basis

```text
1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165).
```

The solver-free checker hash-pins the H510 and fresh-centre source files,
proves all 514 points distinct, and rebuilds the complete unit edge set from
all 131,841 point pairs using rational coefficient arithmetic.  Archived
neighbour lists are checked against the rebuilt graph but are not trusted to
define it.

`certificate.json` contains 510 packed four-colour words, one for each old
singleton deletion.  The checker decodes each word, checks canonical padding
and colour normalization, and tests every retained edge.  The logical order
bound uses only these positive words and restriction; it imports neither an
UNSAT claim nor a completeness assumption about a colouring library.

The 92,042-byte certificate has SHA-256
`474b98e268ef39e3844619350aa526ce160c889849f1b25e90789c05bbfb52f7`.
Its unpacked canonical word stream has SHA-256
`a268d85b9c5c26a03b766a2924ed3371b9a836e7a0e6a8d89b6d5633d01765c6`;
the rebuilt edge stream has SHA-256
`7c7e7385e6fa4dc17aeab11d7df93e0bdfa1ccd66dafe1079753bf152fc6c6a8`.
The verifier checks 1,282,725 retained-edge inequalities.

## Reproduction

CPython 3.11 or later and its standard library suffice for proof replay:

```sh
python3 -B hadwiger_nelson_heule_fresh_c4_cover/verify.py --check-expected
python3 -O -B hadwiger_nelson_heule_fresh_c4_cover/verify.py --check-expected
python3 -B hadwiger_nelson_heule_fresh_c4_cover/controls.py
sha256sum -c hadwiger_nelson_heule_fresh_c4_cover/SHA256SUMS
```

Optional witness regeneration uses `python-sat==1.8.dev17` and CaDiCaL 1.9.5:

```sh
python3 -m venv /tmp/hn-fresh-c4-env
/tmp/hn-fresh-c4-env/bin/pip install -r \
  hadwiger_nelson_heule_fresh_c4_cover/requirements.txt
/tmp/hn-fresh-c4-env/bin/python -B \
  hadwiger_nelson_heule_fresh_c4_cover/produce.py \
  --out /tmp/hn-fresh-c4-certificate.json
cmp /tmp/hn-fresh-c4-certificate.json \
  hadwiger_nelson_heule_fresh_c4_cover/certificate.json
```

The producer uses activated four-colour formulas and normalizes the first
fresh centre to colour zero.  At-most-one clauses are unnecessary: every
active vertex has a nonempty true-colour set, adjacent sets are disjoint, and
choosing the first true colour gives a proper colouring.  The public checker
uses only that explicit selected colour.

The author discovery/production run made 510 SAT calls with a 200,000-conflict
per-query cap, used 1,396,832 conflicts in total, and had no UNSAT or UNKNOWN
outcomes.  A clean second production was byte-for-byte identical.  Those
operational figures are not proof premises.

Remaining trust lies in the hash-pinned coordinate sources, elementary
independence of the radical basis, Python exact arithmetic and complete finite
loops.  This is author-run evidence pending independent review, not a formal
proof-assistant verification.

The previous two fixed fresh-centre supports were independently accepted and
their order bound strengthened to 509 in
[`hadwiger_nelson_heule_fresh_exchange_cover_review1`](../hadwiger_nelson_heule_fresh_exchange_cover_review1/README.md).
