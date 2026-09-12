# Complete one-blue-block classification and three original q8 exclusions

Exactly one of the 546,356 pinned order-11 R(4,4) cores cannot be extended by
four new, pairwise blue-adjacent vertices while avoiding red K4 and blue K5.
The exception is literal record 516166, isomorphic to the red join of the
Wagner graph with an independent triple. All other 546,355 records have
explicit checked 15-vertex extensions.

A checked LRAT proof excludes these **complete original full43 tasks**:

- `bo1-q8-r5-c516166`
- `bo1-q8-r6-c516166`
- `bo1-q8-r7-c516166`

Every remaining physical edge in each original task is free. The proof joins
are checked against the actual complete ordered-parent DIMACS formulas, with
actual input-clause indices and renamed LRAT proofs. No redirect, target
cohort assumption, extra symmetry, or imported R(4,5) theorem is used.

This adds three source-certified original exclusions to the 518 inherited
accepted exclusions. Independent review of the new result remains separate.
The source-certified residual has 2,188,657 of 2,189,178 original IDs; the
historical ledger is not modified. All 956 full q8 physical cohort jobs remain
unclosed. The bounds 43 <= R(5,5) <= 46 are unchanged; the upper bound is the
[Angeltveit–McKay theorem](https://arxiv.org/abs/2409.15709).

## Replay

Use Python 3.11, `python-sat==1.9.dev15` (CaDiCaL300), and a C++17 compiler.
The cache must contain the exact author catalog `r44_11.g6` and the other
catalog files required by the pinned original carrier dependencies. The
existing carrier downloader can populate it:

```bash
python3 ramsey_r55_global_maximal_packing/catalog.py /absolute/cache --download
python3 ramsey_r55_q8_blue_block_obstruction/reproduce.py /absolute/cache /absolute/new-output
```

The output directory must be new. The complete replay generates all literal
SAT witnesses, verifies them with an independent C++ clique checker, verifies
the compact local LRAT proof, emits the three complete original formulas,
renames the proof into their actual clause numbering, and checks all three
full-parent refutations. It also rejects incomplete proofs, bad hints, invalid
inputs, and a false SAT witness. See `EXPECTED.json` for the exact outputs.

For the compact obstruction alone, with no SAT solver required:

```bash
python3 ramsey_r55_q8_blue_block_obstruction/check_lrat.py \
  ramsey_r55_q8_blue_block_obstruction/obstruction.cnf \
  ramsey_r55_q8_blue_block_obstruction/obstruction.lrat
```

The 3.28 MB witness stream, full parent CNFs, renamed proofs, checker binaries,
and logs are reproducible bulk outputs and are not committed. The 4.5 KB
local CNF and 168 KB LRAT proof are included as compact certificates.
`PROOF.md` gives the exact implication; `HANDOFF.md` records admission scope.

## Trust and provenance

The complete catalog is Brendan McKay's primary author data, available from
[his Ramsey graph catalog](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html).
Its pinned uncompressed SHA-256 is
`39e10a1bb2d6b36d556e646e12f0181b2bc3bd45b334ad7f495b8900d7680433`.
Global completeness up to isomorphism is an imported property of that catalog.
The three literal original-ID exclusions need only the identity of their
single record and the already published carrier definitions.

SAT statuses are not accepted as evidence. Every positive model is checked by
`check_witnesses.cpp`, which does not use the Python SAT encoder or its graph6
parser. The exceptional input is also grounded independently by the
old/new-vertex split in `reference.py`. The actual CaDiCaL 1.9.5 DRAT proof was
verified by DRAT-trim and converted to positive-hint LRAT. `check_lrat.py`
checks each of its 2,002 additions by unit propagation, both locally and on
all three actual parents. These are ordinary program checks, not a proof
assistant formalization. No priority claim for the finite classification is
made; the campaign result is the reproducible original-task retirement.
