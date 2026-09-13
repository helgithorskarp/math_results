# Reproduction
Python 3.11 or later and the standard library suffice for verification.  From
this directory run:

```bash
python3 -B verify.py --certificate certificate.json
python3 -B -O verify.py --certificate certificate.json
python3 -B verify.py --certificate certificate.json --controls
```

Each verifier run reconstructs 2,073 canonical closure points in total and
all strict pair distances exactly.  The reference runs take about one minute
each on the research host.  Expected output has `status=VERIFIED` and rows
`(302,1341)`, `(700,3531)`, `(971,5092)`.

Optional regeneration requires a DIMACS SAT solver that returns code 10 and a
standard `v` model, for example CaDiCaL 1.9.5:

```bash
python3 -B produce.py --solver /path/to/cadical --output certificate.generated.json
cmp certificate.generated.json certificate.json
```

The SAT solver is only a positive-certificate finder.  The solver-free
verifier checks the generated colour words directly against exact geometry.
There is no UNSAT or proof-trace trust boundary.
