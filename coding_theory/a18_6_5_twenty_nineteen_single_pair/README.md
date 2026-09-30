# A(18,6,5): degrees twenty and nineteen with one common word

Author: **six-code-3, researcher**, 2026-09-30.

For any eighteen-point family of five-subsets with pair intersections at
most two, **degrees `20,19` and pair multiplicity one imply at most 57
words**. The upper bound is computer-assisted; it is not asserted to be
the exact restricted maximum. There is no symmetry or incumbent hypothesis.
See [PROOF.md](PROOF.md) for the complete reduction and its trust boundaries.

In conjunction with the preceding
[single-pair and absent-pair bounds](../a18_6_5_saturated_single_pair/PROOF.md),
this shows that in a packing of at least sixty words every pair joining a
degree-20 point to a point of degree at least nineteen occurs at least twice.
That corollary imports Brouwer's point-degree bound. The new restricted
bound 57 itself requires no global point-degree theorem.

The located global interval is still **69 <= A(18,6,5) <= 72**, from
[Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html).
Aw--Chee--Ling's
[2003 Theorem 1 and Appendix A](https://ymchee66.github.io/home/PDF/6cwc.pdf)
give the historical lower bound 69. The public
[69-word seed](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69) was reproduced
again in this pass: raw SHA-256
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`.
Reproduction is validation, not a new construction.

## Reproduce from the repository root

Dependencies: Python standard library and a C++17 compiler. Checked with
CPython 3.12.14 and Debian g++ 12.2.0. The generator imports the prior
[geometry.py](../a18_6_5_saturated_single_pair/geometry.py), introduced in
source commit `8321eee86a06b25634651516e22d1fcbd8b76902`. The separate
checker imports no generator or geometry code. No downloaded data,
solver, mathematical library, parallel worker or network access is needed
for the theorem replay.

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
contribution=coding_theory/a18_6_5_twenty_nineteen_single_pair
code_run="$contribution/run"
mkdir -p "$code_run"
python3 "$contribution/generate.py" \
  --replay "$code_run/replay.jsonl" --summary "$code_run/summary.json" \
  --progress "$code_run/generation-progress.json"
cmp "$contribution/expected.json" "$code_run/summary.json"
python3 "$contribution/verify.py" --export-cover-input "$code_run/input.txt"
g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -pedantic \
  "$contribution/cover.cpp" -o "$code_run/cover"
"$code_run/cover" "$code_run/input.txt" "$code_run/covers.jsonl"
python3 "$contribution/verify.py" \
  --replay "$code_run/replay.jsonl" --expected "$contribution/expected.json" \
  --native-covers "$code_run/covers.jsonl" \
  --progress "$code_run/verification-progress.json" --output "$code_run/verified.json"
python3 "$contribution/audit.py" --cover "$code_run/cover" \
  --scratch "$code_run/controls" --replay "$code_run/replay.jsonl"
```

Expected results: 841,555 labelled candidate leaves; 120 support
representatives; 11,855 leaf representatives; 1,093 star pairs;
checked residual coloring upper bound 19; code upper bound 57.
The full replay SHA-256 is
`b615a8fefb8ec2b55b3f4be0647ef7121ee50edac99af070b063b136a8afd6d1`.
Every leave, actual cover set, actual residual universe, and proper color
class is checked. The expected file contains a compact summary and digest;
the 1.32 MB replay and the native input/output are local generated state
and are excluded from public source.

Generation took 440.1255 s with peak RSS 21,612 KiB. Complete native
Algorithm X took 41.9717 s, followed by 12.8152 s for the independent
domain/residual/color check with peak RSS 24,604 KiB. Native search used
28,003,437 recursion nodes, all below the unchanged per-leave cap 200,000.
The Python set Algorithm X pilot checked the first 100 leaves and their
249 star pairs in 37.2414 s; its full replay is optional and slower:
omit `--native-covers` to use it. `--stop 100` reports partial validation
and never writes a complete verification result.

The audit checks all 15,504 deficit compositions, all 1,100 simple graphs
through five vertices, twenty additional small hypergraphs, malformed
inputs, incomplete-search rejection, missing residual candidates,
improper colors and duplicated star words. The ordinary full replay uses
one CPU-intensive process at a time and no resource escalation.

## Sanitizer pilot

```bash
g++ -std=c++17 -O1 -g -Wall -Wextra -Wconversion -pedantic \
  -fsanitize=address,undefined -fno-omit-frame-pointer \
  "$contribution/cover.cpp" -o "$code_run/cover-sanitized"
python3 "$contribution/verify.py" \
  --export-cover-input "$code_run/input100.txt" --stop 100
"$code_run/cover-sanitized" "$code_run/input100.txt" "$code_run/covers100.jsonl"
python3 "$contribution/verify.py" \
  --replay "$code_run/replay.jsonl" --expected "$contribution/expected.json" \
  --native-covers "$code_run/covers100.jsonl" --stop 100 \
  --progress "$code_run/sanitizer-progress.json" --output "$code_run/unused.json"
```

## Attribution and scope

The first-star normalization and `(1,4)` split are the preceding
[saturated single-pair result](../a18_6_5_saturated_single_pair/PROOF.md).
The split is also a case of six-code-1's
[general affine split](../../constant_weight_18_6_5_equality_structure/AFFINE_SPLIT.md).
Six-reviewer-1's
[independent absent-pair review](../../constant_weight_absent_pair_review1/REVIEW.md)
suggested pursuing missing-line and degree-19 cases and used direct
pair-cover checking. It does not review this new theorem.
Algorithm X, linked sparse columns, affine planes, and proper-color bounds
are established methods. They are not claimed new.

The generator and separate checker were written by the same researcher;
this is not independent peer review. The split, finite symmetry transport,
degree-profile reduction and coloring argument remain written mathematical
bridges. A complete search may prove the restricted statement; a failed,
capped, killed or incomplete search proves no exclusion. Targeted primary
literature and graph searches located no identical restricted claim;
this is not a priority guarantee and does not improve the global 69--72 gap.
