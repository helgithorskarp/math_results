# Coupled unit shifts in the P192 corona template

six-heesch-1, researcher. Author-checked exact finite lemma; ordinary geometric
bridges remain unformalized and independent review is pending.

The [proof](proof.md) classifies all common prototypes between a fixed35-cell
core and105-cell domain, while each of six first-corona placements independently
chooses one of nine fine-grid unit shifts. An admissible disc first corona
forces the unchanged68-cell prototype or one67-cell exception. The exception
has one such layout, and an empty90-degree corner prevents its extension even
under arbitrary rigid motions. Thus an edited prototype in this template
cannot have a second corona beginning with these placements.

This closes a specific route to a high-corona construction. Other first
placements are outside the theorem. The exception's global Heesch number and
plane-tiling status remain unknown; no record or finite-five tile is claimed.

Run with Python3.11.2, standard library only, from the repository root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 round-two/six-heesch-1/p192-coupled-template/verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -O round-two/six-heesch-1/p192-coupled-template/verify.py
```

Both commands emit [expected.json](expected.json):1252 variables/11409 clauses,
3160 checked residual RUP additions, one67-cell exception, a54-variable/
456-clause unique-layout certificate, and a536-placement empty-corner check.
Five damaged inputs are rejected. The reader reconstructs every formula and
physical footprint; no native solver, status, heuristic or external catalogue
is trusted. Its sole code dependency is the byte-pinned public
[RUP reader](../finite-contact-types/rup.py). [dependencies.json](dependencies.json)
also pins the literal input. All proof data needed for replay are included.

The [literature note](literature-note.md) corrects the earlier hexapillar baseline description using Mann's primary source.
