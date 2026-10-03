# Entire three-original Q obstructions for supplemental covering tails

**six-covering-1 / researcher.** In the five-copy F160 model defined in
[proof.md](proof.md), with one possible supplemental modulo9 row, an UNMARKED
copy with ENTIRE original inventory

- `{d3,8,720}`, `d3 in{3,6,12}`, has common support at most110;
- `{d3,8,d5}`, `d3 in{3,6,12}`, `d5 in{5,10,20}`, has common support at most106.

All other originals, owners, phases and omissions are free. Projected aliases
retain separate original resources. No binary-core ownership condition is
imposed. These are ordinary, unformalized conditional proofs, accompanied by
exact local audits. Independent external review is pending. Neither bound is
claimed sharp, and neither changes global minimum-EXACTLY8 LCM bounds.

Python3.10+ standard library only. From this directory:

```sh
python3 verify.py
python3 -O verify.py
```

Each command runs six independent child processes sequentially, each with a
14-second timeout and numerical thread variables set to1. Typical total time
is approximately26 seconds; no private input, native builder or solver is used.
Individual partitions can also be checked:

```sh
python3 verify.py --part parity
python3 verify.py --part column-0
```

The five column partitions are `column-0` through `column-4`; all are required
for the complete column audit. `verify.py` compares complete mathematical
records with [expected.json](expected.json), including source hashes and
complete local entry-stream digests. Optimized Python retains explicit checks.

[audit_parity.py](audit_parity.py) verifies all200 singleton-Q targets, all
three original inventory types,308400 phase entries and the complete local
column/fine-row obstruction. [audit_column.py](audit_column.py) verifies all30
whole-Q phase tuples, all nine original types,186030 phase entries and every
budget20 local equality case. Both compare every original progression residue
on period5040 with its projected support. The ordinary proof handles arbitrary
common-support subsets and all allocations within the stated inventories;
the audits do not enumerate those whole allocations or subsets.

No full covering, new universal nonexistence result, sharpness certificate,
formal proof, independent review verdict or higher-minimum record is supplied.
Primary literature, previous model context and the scope of the construction
consequence are stated in the proof.
