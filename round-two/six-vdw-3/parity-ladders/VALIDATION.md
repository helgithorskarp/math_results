# Executed validation

Agent: **six-vdw-3**. Role: **researcher**. Date: 2026-10-01 UTC.

CPython 3.11.2, standard library only, Linux. No solver, floating-point
mathematical result, external witness corpus, or sibling source input is
required. All children ran sequentially with solver/BLAS/OpenMP environment
thread counts set to one.

Executed from the repository root:

```
python3 round-two/six-vdw-3/parity-ladders/reproduce.py \
  --workdir scratch/parity-ladder-validation/reproduction
```

Result: `VERIFIED_PARITY_LADDER_REPRODUCTION`; normal and `python3 -O`
checks both matched the complete [expected output](expected.json).
Wall time 11.153 seconds, maximum child RSS 34720 KiB. Timing is operational
evidence, not a mathematical bound. A prior standalone checker run took
9.091 seconds and 31308 KiB; the final complete run includes both modes.

The regenerated model has 5253 variables, 31110 clauses, and SHA256
`1a0e530403d4ec844d4988ba5e842a8a5582ed09f63a3e7eac6f595762fb659f`.
Each clause matched the separate full-directed-step reconstruction.
The local equivalence exhausts 128 seven-bit words. Both checking modes
compare cyclic products and field ladders word by word on 70720 orientations:

| q | Complement-normalized orientations | Valid products |
|---:|---:|---:|
|7|64|21|
|11|1024|0|
|13|4096|52|
|17|65536|0|

These are exact validation cohorts; no novelty of the small constructions
or exclusions is asserted. Every repeated-residue cyclic step is included.

Both checking modes rejected all six malformed/altered models, checked the
extremal telescoping identity in both derivative-color orientations for
30 admissible q values from 23 through 199, and checked the actual
103-column extremal obstruction at integer start 231, step 305, color 0.
The small positive q23 product was separately checked term by term on all
18906 cyclic start/step pairs. Its 22 nonzero shift distances all equal 12.
The q7 positive control checks the size hypothesis in the extremal lemma.

The established QR617 incumbent was reconstructed from squares, with six
initial zero poles and a final one pole. The independent nonwrapping checker
accepted all 1140833 APs at length 3703; its newline-terminated word hash is
`442f563bc6e1ae75d9666a3417e1246e413c83393777dd22ac0bc730d0f4759a`.

The general derivative cut follows from the written cyclic-run and
telescoping proof for every stated q, word, and unit shift. The 30 numerical
instances support arithmetic validation; they are not its quantifier coverage.
No search verdict is used for q=103. Its separable existence question and
the unrestricted length-3704 target remain unresolved.
