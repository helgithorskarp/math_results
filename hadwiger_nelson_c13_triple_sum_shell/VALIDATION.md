# Validation record

Validated on 2026-09-08 UTC with CPython 3.11.2.

Both of the following pairs produced byte-identical output under ordinary and
assertion-disabled Python:

```bash
python3 -B verify.py
python3 -O -B verify.py
python3 -B controls.py
python3 -O -B controls.py
```

The verifier independently checks the SAT-produced colour word against the
complete exact strict graph. No SAT solver, floating-point operation, imported
coordinate file, or large external artifact is used during verification.

The negative controls reject a monochromatic-edge word, a truncated word, a
corrupt coordinate receipt, and a nonunit vector whose squared norm has
rational coefficient one but nonzero `sqrt(5)` coefficient. Reconstructing the
shell with minimum contact count three gives 832 points, which checks that the
published 2,940-point count is tied to the stated threshold two.
