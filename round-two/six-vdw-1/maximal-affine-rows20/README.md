# A64-row local family for two-color seven-AP constructions

six-vdw-1, researcher. [PROOF.md](PROOF.md) proves that the specified
dimension-four row cube has a unique maximal locally admissible affine
extension of dimension six, containing64 rows on Z20. Maximality requires
containing this cube. Global field/interval feasibility is unresolved.

The64-row representation supplies300 signed point variables,960 row
membership clauses and179 independent choices after global color exchange
for the proposed31-by20 regular-core construction. No such full field
model or3704-point coloring is supplied.

Use Python3.10 or later on a Unix-like system; this source was checked on
Linux with Python3.12.14. Only the
standard library is used. From this directory run:

```sh
python3 -B reproduce.py /tmp/vdw-local-rows20-check
```

Use an empty output directory. The driver regenerates the compact catalogue
and requires exact byte equality with the frozen fixture. It then runs two
separate checkers normally and with isolated optimized Python, compares
their full expected objects and records a compact verification result in
the output directory. Each child has a35-second guard, with thread variables
set to1. A failure or incomplete check establishes no exclusion.

Expected:1024 difference vectors in64 cosets;580 admissible antiperiodic
rows; three proper one-bit extensions153,277,396; sixty actual AP witnesses
for all other cosets; a unique maximal64-row extension. The maximality
checker verifies24320 local AP pairs,1024 row-membership truth inputs,
1280 point identities and the coefficient decoder. Nine catalogue damages
and seven maximality damages reject in each mode. No field enumeration or
native SAT proof is performed.

Files:

- `generate.py`: deterministic untrusted proposal from actual row APs.
- `catalogue.json`: compact complete coset entries and60 actual bad-row APs.
- `check_catalogue.py`: independent row enumeration and complete input cover.
- `check_maximal.py`: independent maximality witnesses,64 rows and decoder.
- `EXPECTED.json`: frozen exact catalogue hash and full mathematical results.
- `SOURCE_PINS.json`: core source/input hashes fixed before standalone replay.
- `verification.json` and `VALIDATION.md`: concise standalone validation.

No credentials, private ledgers, operational checkpoints, native models,
large proof traces or binary build products belong in this directory.
The native8/16-row experiments remain separate private research; their
status is not a premise or evidence for this local lemma.
