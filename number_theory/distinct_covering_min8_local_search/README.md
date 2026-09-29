# An explicit minimum-eight covering at LCM 30240

Author: **six-covering-1**, role **researcher**, 2026-09-29.

The 85 congruences in [cover.json](cover.json) cover every integer, have
pairwise distinct moduli and minimum **exactly eight**, and have LCM
`30240 = 2^5*3^3*5*7`. Consequently `L_min(8) <= 30240`. This improves
the campaign's previously certified upper bound of 70560. Together with
six-covering-2's [10080 lower bound](../distinct_covering_min8_lower_bound),
the current campaign interval is `10080 <= L_min(8) <= 30240`.

The [proof](proof.md) reduces coverage to a literal check of all 30240
integer representatives. Two standard-library checks use different
algorithms: marking arithmetic progressions and testing every point's
congruence predicates. Both are by the author; no external review or
optimality claim is asserted.

From the repository root, Python >=3.10:

```sh
python3 number_theory/distinct_covering_min8_local_search/verify.py --check-expected
python3 number_theory/distinct_covering_min8_local_search/audit.py
python3 number_theory/distinct_covering_min8_local_search/controls.py
```

Expected: 85 classes, minimum 8, LCM 30240, zero uncovered residues;
coverage multiplicities `{1:18862, 2:10466, 3:909, 4:3}`. Every class
has at least two points covered by that class alone. The ordered byte
sequence of coverage multiplicities has SHA-256:

    97b16fb2a89d0b54acfc03790e83afa45934edb570e57d1b6d54825c7def3994

Verification was tested with CPython 3.11.2. The proof needs no solver,
floating arithmetic, compiler, claimed minimum-seven lower bound or
external enumeration data. [expected.json](expected.json) records the
complete compact verification summary; `SHA256SUMS` records file hashes.
The cover JSON has SHA-256
`aae0d039be18688848632813671fa6e24e0b14aef1a2f06e76cdfd1fa6584bfa`.
Progression verification took 0.123 seconds and the separate point audit
0.403 seconds, each using less than 16 MiB peak child RSS and one thread.

Optional deterministic discovery replay, tested with GCC 12.2.0:

```sh
g++ -std=c++20 -O3 -Wall -Wextra -Wconversion -Wshadow number_theory/distinct_covering_min8_local_search/search.cpp -o /tmp/min8-walk
/tmp/min8-walk 30240 5 20260929 number_theory/distinct_covering_min8_local_search/seed.tsv /tmp/min8-walk.tsv
python3 number_theory/distinct_covering_min8_local_search/prepare.py /tmp/min8-walk.tsv /tmp/min8-regenerated.json
python3 number_theory/distinct_covering_min8_local_search/verify.py --cover /tmp/min8-regenerated.json --check-expected
```

The initializer [seed.tsv](seed.tsv) is the explicit 66-class covering in
[Zhang–Zhang, Section 7](https://arxiv.org/html/2607.19029#S7). The search
changes its phases freely and uses every eligible divisor once. It found
an 89-class covering; `prepare.py` deleted four redundant classes. The
stored final cover retains 29 of the 65 designated classes left after
deleting modulus seven. Controls check that initializer and provenance.

Search is one thread and bounded by time and 200000 iterations. An
inconclusive run exits with code 2; its output is rejected by `prepare.py`.
Bounded failures establish no nonexistence. Sanitizer checks and exact
reconstruction are described in the proof. Verification of the stored
certificate remains available when discovery does not finish in time.
