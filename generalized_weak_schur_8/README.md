# WS₈(2) = 365

Every two-coloring of **[1,365]** contains eight distinct positive integers
whose sum is also in [1,365] and has their color. The published avoiding
coloring of [1,364] makes the bound exact. Eight is the number of summands;
two is the number of colors. We use the least forcing integer convention.

This package gives a **computer-assisted proof** of the upper bound. Read
[the mathematical proof and literature context](proof.md) for the complete
reduction, the prior lower-bound construction, and the scope of trust.
No assumptions on the shape or sizes of the two color classes are imposed.

The unrestricted instance has 629,905 variables and 1,059,130 clauses.
Glucose 3 returned UNSAT; the independent `drat-trim` checker returned
**VERIFIED** with RUP additions only (`-U`). An arithmetic auditor checks
every input clause without importing the generator. See
[the certificate manifest](expected.json), [arithmetic audit](evidence/audit.json),
[checker transcript](evidence/check.txt), and [validation](evidence/validation.json).

## Reproduce

Requirements: Python 3.11, Git, a C compiler, and the pinned Python-SAT packages.
Run these commands from this directory. Keep generated data in an external work
directory. The original solve and check took about 12 minutes total on one CPU
core; times depend on hardware. The generated CNF is about 19.3 MB and its proof
about 3.6 MB. Neither generated file is committed.

```sh
WS8_WORK=/tmp/ws8-replay
mkdir -p "$WS8_WORK"
python3 -m venv "$WS8_WORK/venv"
"$WS8_WORK/venv/bin/python" -m pip install -r requirements.txt
git clone https://github.com/marijnheule/drat-trim.git "$WS8_WORK/drat-trim"
git -C "$WS8_WORK/drat-trim" checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
cc -O2 "$WS8_WORK/drat-trim/drat-trim.c" -o "$WS8_WORK/drat-trim/drat-trim"
"$WS8_WORK/venv/bin/python" validate.py
"$WS8_WORK/venv/bin/python" replay.py --out "$WS8_WORK/run365" --drat-trim "$WS8_WORK/drat-trim/drat-trim"
```

Expected final status: `VERIFIED_WS8_2_EQUALS_365`. The replay regenerates the
CNF, requires the published input hash, solves it, audits each arithmetic
clause, and invokes the separate proof checker. A solver budget exhaustion
or failed proof check exits with an error and does not report verification.
The proof hash is recorded but need not match if a different valid proof is
generated. The proof must always verify against the audited CNF.

To audit an existing instance without solver dependencies:

```sh
python3 audit.py /path/to/input.cnf --n 365 --k 8 --r 171
```

To regenerate only the exact deterministic input:

```sh
python3 encode.py --n 365 --r 171 --out "$WS8_WORK/input-only" --generate-only
```

`validate.py` exhaustively compares the encoding to direct distinct-summand
enumeration on 8,448 small colorings. It also checks the entire published
[364] coloring with a separate integer-set subset-sum algorithm and verifies
its canonical auxiliary assignment against all clauses at N=364.

## Files and provenance

- `encode.py`: subset-sum implication generator and proof-producing solver call.
- `audit.py`: independent arithmetic interpretation of every input clause.
- `validate.py`: exhaustive definition-level controls and the published lower bound.
- `replay.py`: complete solve, audit, and proof-check pipeline.
- `proof.md`: self-contained mathematical argument and primary-source trail.
- `expected.json`, `evidence/`: compact recorded evidence and external-artifact hashes.

The lower bound is due to Ahmed, Boza, Revuelta and Sanz,
[Ramanujan Journal 62 (2023), Lemma 2.1 and Table 4](https://doi.org/10.1007/s11139-023-00760-y).
The matching upper bound was obtained in the autonomous general-researcher-2
campaign on 2026-09-11 and is new to the primary literature searched on that date.
The result has not yet received independent researcher review or proof-assistant
formalization. Solver answers alone are not used as proof.
