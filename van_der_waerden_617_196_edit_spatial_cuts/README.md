# Spatial cuts at a 196-edit QR617 seam budget

Author: **six-vdw-3**, role **researcher**. Exact computer-assisted necessary
conditions for arbitrary binary colorings of `[0,3704)` avoiding every
monochromatic nonconstant seven-term arithmetic progression. Adding one to
the coordinates gives the campaign's `[1,3704]` target.

Let `q(r)` be zero on nonzero squares modulo 617, one on nonsquares, and
undefined at zero. At seam `b=1852`, the partial reference is

```
T_s(x) = q(x-b+s)                     for x < b,
         q(x-b+(1-s mod 617)) XOR 1   for x >= b.
```

Poles remain freely colored and are excluded from edit counts. `E_c` is the
set of nonpole positions of **original reference color** `c` where a candidate
differs. Its far edits lie outside `B=[1287,2417)`.

If **one** reference color has at most 196 edits, its far edit count obeys:

| Phase s | Right phase | Required far edits in that color |
|---:|---:|---:|
| 184 | 434 | 55 |
| 201 | 417 | 57 |
| 205 | 413 | 56 |
| 269 | 349 | 60 |

Each statement applies separately to either color under that color's own
budget. The candidate need not have reflection symmetry, affine structure,
periodicity, or a budget in its other color.

The [published 617-phase profile](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_reflection_seam_weights)
has source commit `9a2bb02c0ddf0aabdba44e083d14a89c608b2c64` and graph reference
`bafkreibhwl2tw6yj4f62kc4icradwaq2tpn4z56tox4okqmpy62mn4edma`.
It proves at least 196 edits per color throughout this reflection reference
family, and at least 197 outside the four phases above. **Using that result**,
any candidate with at most 392 nonpole edits relative to any of the 617
references must have exactly 196 in each color, use one of these four
phases, and have at least **110 far edits** (phase-specific totals
110, 114, 112, 120). Its bridge contains at most 282 edits. This directory
checks the four new spatial certificates, not the prior 617-phase theorem.

The same weights give a stronger location reduction at the stated class and
far budgets. Every edit must lie in a high-load eligible set, and the sum of
its capacity defects has a certified upper bound:

| s | Class budget | Far budget | Eligible positions per color | Eligible inner/far | Maximum summed defect |
|---:|---:|---:|---:|---:|---:|
|184|196|55|881|470 / 411|514543 / 1000000|
|201|196|57|911|460 / 451|999926 / 1000000|
|205|196|56|904|465 / 439|589693 / 1000000|
|269|196|60|905|464 / 441|708966 / 1000000|

Each color has 1,849 nonpole reference positions, including 1,285 far
positions. Thus the conditional reduction forbids edits at 968, 938, 945,
and 944 positions respectively. It does not prove that these budgets are
attainable. [PROOF.md](PROOF.md) defines the defects and gives the exact
inequalities, including their complement versions.

Run the complete proof checker with Python 3.11 or later; it needs only the
standard library:

```bash
python3 check_all.py
python3 controls.py
```

Expected: four phases, 6,960 checked APs, 48,720 checked incidences, far
bounds `[55,57,56,60]`, and 20 rejected corruptions/coverage controls.
Canonical certificate manifest SHA-256:

```
216b42f52e2ddcdddb2c370be9deddd07d136ad808b80849746d6219f6e42300
```

For an individual affine tradeoff at additional integer class budgets:

```bash
python3 verify.py certificates/phase-184.json --budgets 196 197 198 200
```

The four compact exact certificates total 63,274 bytes and are included.
`expected.json` preserves entry-level results and eligible-set hashes.
`validation.json` records versions, controls and measured resources.
There is no external numerical premise for the four spatial cuts. Exact
verification uses Euler's criterion, actual integer AP coordinates, and
integer capacity sums; it imports no generator or solver. This is a
same-author independent checker, not an external review or formal proof.

Optional rediscovery uses HiGHS 1.11.0 and NumPy 2.2.6. Keep its generated
state outside this source directory:

```bash
python3 -m venv /path/to/local-venv
/path/to/local-venv/bin/pip install -r requirements.txt
/path/to/local-venv/bin/python reproduce.py --work /path/to/local-work --fresh
```

The runner uses one sequential job and one numerical thread, with a
15-second solver limit per phase. A weaker or incomplete discovery run
establishes no exclusion; the included certificates can still be checked
directly. Floating optimality is not part of the proof. No large outputs,
private campaign state, or credentials are required.

The result constrains four incompatible affine QR617 seams and, through
the cited profile, a conditional regime across 617 such seams. It does
not constrain all 760,761 incompatible seam keys, prove an optimal repair
distance, produce a length-3704 witness, or determine W(2,7).
