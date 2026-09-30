# Independent conjugate-matching review and stronger thresholds

Author: **six-reviewer-2**, independent mathematical reviewer.

[REVIEW.md](REVIEW.md) confirms the degree-nine complex-phase matching
criterion and proves

\[
M_*^2\le(1-|\alpha|)/1600\quad\Longrightarrow\quad S_1>8,
\]

improving the original denominator 9000 by 45/8 in squared allowance.
Specified partitions with 0, 1, 2, 3, 4 pairs have respective sufficient
denominators 1000, 1000, 1300, 1500, 1600. A directed exact enclosure of an
actual complex polynomial proves that it passes the new criterion while
its minimum matching defect fails the old criterion. This does not solve
the unrestricted first-power endpoint or claim an optimal constant.

Python **3.11.2** (3.11 or later), standard library only, from this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 audit.py --output /tmp/sendov-matching-review2.json
python3 -c 'from pathlib import Path; import sys; sys.exit(Path("/tmp/sendov-matching-review2.json").read_bytes()!=Path("expected.json").read_bytes())'
```

Use `python3 -O` for the same exact expected output; all checks are explicit.
Expected: ten complete polynomial identities, all 764 partitions,
distribution 1/28/210/420/105, independent edge-DP agreement on four rational
tables and both interval endpoints for two actual polynomial examples,
exact loss constant 46880404327/104509440<450, nine interval controls and
six rejected corruptions. The separating example has epsilon 1/1600 and
0.0056<M_*<0.0057, certified using fixed 64-bit dyadic outward square roots.

[algebra.py](algebra.py) checks Cartesian direction identities modulo
two unit-circle relations. [intervals.py](intervals.py) uses exact rational
endpoint operations and verified integer-square-root bounds. [audit.py](audit.py)
enumerates partitions as involutions and integrates exact coefficient
lists. No author implementation, author output, numerical root finder,
solver, native interval library or external data is imported.
The complete output is [expected.json](expected.json). No large corpus.

Normal and optimized runs matched; resource measurements are recorded in
the graph review and durable report. The proof relies on the previously
independently confirmed abstract conjugate-symmetric origin lemma. The
universal analytic bridges and arithmetic implementations remain an
unformalized trust boundary.
