# Validation and trust boundary

## Exact public replay

`generate.py` builds all four group tables, inversion orbits, and complete
rooted-five formulas. `audit.py` imports no producer code. It rebuilds the
four presentations, checks all `4*44^3=340,736` associativity instances,
reconstructs every clause, compares the complete formula sets, and verifies
that every committed core clause is physical.

`controls.py` compares `dpll_check.py` with literal enumeration of all eight
assignments on 12,291 three-variable formulas. It includes explicit empty-
clause and complete-assignment-blocker UNSAT cases. The core replay reports:

| group | DPLL states | branches | contradiction leaves | unit assignments |
|---|---:|---:|---:|---:|
| `C11 x C4` | 3,085 | 1,542 | 1,543 | 10,658 |
| `C11 x V4` | 3,229 | 1,614 | 1,615 | 11,793 |
| `C11 semidirect C4` | 2,621 | 1,310 | 1,311 | 9,548 |
| `C11 semidirect V4` | 58,721 | 29,360 | 29,361 | 320,839 |

No random sampling, floating-point arithmetic, external graph catalog, or
unpublished input enters the public replay.

## Production provenance

The initial formulas were solved sequentially by Kissat 4.0.4 with
`--unsat` and a fixed 300-second wall limit per group. All four returned
UNSAT in 0.165, 0.265, 0.115, and 4.129 seconds. Their binary DRAT streams
were checked by `drat-trim -i`. Kissat's binary SHA-256 was
`2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`;
drat-trim's was
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

Those operational proofs are not published and are not proof premises. They
were used to extract smaller input-clause cores. The public DPLL replay
decides those cores independently, while `audit.py` binds every core clause
back to a literal Cayley five-set.

## Trust boundary

The mathematical trust boundary consists of the written Sylow and translation
arguments, the finite group/formula reduction, the producer-independent
auditor, the DPLL algorithm and its controls, CPython integer/file semantics,
SHA-256, the operating system, and hardware. The computations are not
formally verified. No historical novelty claim is made for the group
classification or Cayley obstruction.
