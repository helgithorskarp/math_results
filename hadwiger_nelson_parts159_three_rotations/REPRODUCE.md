# Reproduction and trust boundary

Use a clone of the publication repository, since the exact point input,
field-colouring implementation, and previous component library are reused
from their original directories. `geometry.py` binds all four dependency
files by SHA-256 before importing them. No network access or installed
solver is needed for verification. Python 3.11.2 was used.

From the repository root:

```sh
python3 -B hadwiger_nelson_parts159_three_rotations/verify.py --check-expected
python3 -O -B hadwiger_nelson_parts159_three_rotations/verify.py --check-expected
python3 -B hadwiger_nelson_parts159_three_rotations/controls.py
```

The expected main output is in `EXPECTED.json`; measured checks are in
`VALIDATION.json`. The verifier reconstructs 178 E contact phases, 1,490
outside-E quadratic classes with 2,980 physical roots, and their 52
quadratic extensions. It checks all 118,734 same-field pairs and relies on
the proved degree-four obstruction for the 4,319,976 different-field pairs.
The complete arbitrary-angle reduction is in `PROOF.md`.

The original 4-word library covers 1,428 fixed-field extensions and 37,516
three-copy contact pairs. The certificate checks the remaining 62
extensions and 360 pairs directly. Every component word is checked against
the complete 646-edge graph. Colour agreement at coincident points is
mandatory. Positive witnesses require no proof-producing SAT trust.

`controls.py` uses a second quotient-basis multiplication, with generators
t²=-3, r²=-11 and q²=A-Btr. It checks all 2,980 unit rotations, every
reported outside cross edge, deterministic nonedges in all 52 fields, and
corrupts every additional colouring witness deliberately.

Optional discovery replay requires `python-sat==1.8.dev24` with CaDiCaL
1.9.5. In a separate environment containing that package, choose a new
scratch output path:

```sh
python3 -B hadwiger_nelson_parts159_three_rotations/produce.py --output /tmp/parts159-reproduced.json
python3 -B hadwiger_nelson_parts159_three_rotations/verify.py --certificate /tmp/parts159-reproduced.json
```

Discovery queries have a 500,000-conflict limit. A non-SAT result stops
generation and proves nothing. The distributed certificate is the checked
positive evidence; no UNSAT result is part of this theorem. A regenerated
certificate can have different valid words or indexing, so use
`--check-expected` only with the distributed certificate.

Expanded root catalogues, search logs, exploratory supports, environments,
and temporary solver output are intentionally outside the repository.
