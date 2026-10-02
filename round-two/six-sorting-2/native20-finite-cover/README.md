# Native thirteen-input P20 exclusion

Agent **six-sorting-2**, role **researcher**, 2026-10-02.

Every standard sorting network beginning with the native46 word's first20
comparators requires at least45 total comparators. The proof covers
arbitrary suffix order/depth and preparation length. This prefix starts
(0,11) and ends(3,8); it differs from the historical twenty-prefix theorem
for the45-gate incumbent. The global13-input gap remains44..45.

[PROOF.md](PROOF.md) gives the argument. [fixture.json](fixture.json) pins
the exact20-gate word, known46 control and81 original selected domains.
The complete finite normal form has23006 nine-wire images;22241 semantic
and765 nested class certificates exclude them all. The expected root
image/budget hash and counts are in [expected.json](expected.json).

From the repository root with Python3.11.2 and stdlib, run:

~~~sh
python3 -B round-two/six-sorting-2/native20-finite-cover/run.py --output-dir scratch/native20-normal
python3 -O -B round-two/six-sorting-2/native20-finite-cover/run.py --output-dir scratch/native20-optimized
~~~

Each command regenerates all data and runs all independent checks,
serially, with threads1 and a55-second stage guard. Expected final status:
NATIVE20_COMPLETE_SIZE44_EXCLUSION_VERIFIED,45 lower bound,23006 roots,
22241+765 exclusions and zero remaining. Finite output fields agree
between normal and optimized modes; timing, progress elapsed time and RSS are excluded from
that comparison. Generated arrays/certificates/logs remain in scratch.
The compact public evidence contains only inputs, source and summaries.

The [source manifest](source-manifest.json) pins reused public production
and intake modules. Later standalone numeric/DNF, balanced-tree/bulk-image,
numeric-set and scalar-carrier checkers import no producer or solver.
Algorithmic independence is same-author; no external review or formal
verification is claimed. Imported9207/8539/8604/9007, S11/S7/S6/S5 and
unformalized pruning/commutation/zero-one/category-collapse are explicit.

[checks.json](checks.json) records normal/optimized agreement, exact checker summaries and resource use. To repeat the nine damaged-certificate checks after a successful normal run, use:

~~~sh
python3 -B round-two/six-sorting-2/native20-finite-cover/damage_check.py --evidence-dir scratch/native20-normal --output-dir scratch/native20-damages
~~~

All nine cases reject with explicit errors in both modes. The script refuses an existing overlay directory and leaves original evidence intact.
