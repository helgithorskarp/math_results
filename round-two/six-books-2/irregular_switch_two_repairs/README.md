# All switches and two edits of the irregular book-Ramsey seed

Author: **six-books-2**, role **researcher**, 2026-10-01.

**Exact computer-assisted theorem:** among every Seidel switch of the
primary 21-vertex (B4,B7) witness and every subsequent set of at most two
pair toggles, only the original host and its two known unswitched
radius-two variants are valid. All three have explicit short
contradiction paths ruling out an arbitrary added vertex.

Consequently every deleted-vertex core of a hypothetical valid 22-vertex
graph has switching edit distance at least three from this seed, under
every labeling. The unrestricted bound remains **22<=R(B4,B7)<=23**.
[PROOF.md](PROOF.md) states the full quantifiers, reductions, prior art and
computational trust boundary. The universal cut classification uses two
independent author algorithms; it is not an analytic-only or formally
verified theorem, and no independent review of this new result is claimed.

## Reproduce

Use CPython 3.11+ and only the standard library. Validated with CPython
3.11.2 on Linux, one process at a time, one CPU thread. From the repository
root, run the following **sequentially**:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 round-two/six-books-2/irregular_switch_two_repairs/forced_scan.py --controls
python3 round-two/six-books-2/irregular_switch_two_repairs/cover_scan.py --controls
python3 round-two/six-books-2/irregular_switch_two_repairs/forced_scan.py \
  --output /tmp/six-books-2-forced-results.json
python3 round-two/six-books-2/irregular_switch_two_repairs/cover_scan.py \
  --output /tmp/six-books-2-cover-results.json
python3 -O round-two/six-books-2/irregular_switch_two_repairs/verify.py \
  --forced /tmp/six-books-2-forced-results.json \
  --cover /tmp/six-books-2-cover-results.json
```

Both full scans examine all **1,048,576** cuts. The common ordered record
list is `[[0,[]],[0,[114,160]],[0,[150,160]]]`, with canonical SHA256
`d9715e8528a5d0e13d64a65666a2e718d044c36a62c3191b382bcecf01c2a599`.
Pair indices use lexicographic order on unordered pairs of {0,...,20}.
The empty-cut records use edits empty, {(6,16),(10,16)}, and
{(9,16),(10,16)} respectively. [expected.json](expected.json) includes
input digests, baseline histograms and the exact coverage counters.

The first algorithm uses bitset neighbors, forced high-page spines,
successive repair intersections and binary cut order. The second uses
switch-invariant triangle parity, covers of original forbidden books,
Gray cut order and literal set reconstruction. It rejects every
nontrivial cut already at the old-book cover stage. Both algorithms are
in separate files and import neither each other nor the verifier.

The included [seed.txt](seed.txt) is a compact fixed input. No external
download is required for reproduction. Optionally download the
[raw primary witness](https://raw.githubusercontent.com/gwen-mckinley/ramsey-books-wheels/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
and add `--primary /path/to/that/file` to the verification command. This
checks its exact raw digest and the off-diagonal zero-to-red conversion.
The original file appends search metadata after its JSON matrix.

The following quick check verifies only baseline identities, eight
literal book-intersection controls, and all 20 attachment-path arrows;
it explicitly makes no cut-domain completeness claim:

```sh
python3 -O round-two/six-books-2/irregular_switch_two_repairs/verify.py --certificates-only
```

`--limit N` on either scan permits a bounded exploratory prefix. Unless
N=1048576, the output is marked partial and the verifier rejects it.
Limits outside 1..1048576 are rejected. The code uses explicit checks,
not Python assertions, so checks remain active under `-O`.

The scan summaries are compact comparison data, not proof objects that
independently certify an unexecuted census. Full coverage follows from
the written reductions plus the full deterministic executions. No
large proof corpus, solver result or external classification is needed.

## Validation

The first scan's reduction agrees with all 22,156 literal edit sets at
each of three control cuts. The second's page formula agrees with 1,260
literal color tests across six cuts. The third checker independently
checks every surviving graph and every attachment implication with
neighbor sets. Damaged records, incomplete cut coverage, wrong input
digests, invalid implication arrows, malformed fixtures and out-of-range
limits are rejected; these checks were exercised with `-O`.

Measured production source runs use about 16 MiB peak memory per process;
the forced-spine scan takes approximately 23 seconds and the cover scan
approximately two minutes on the campaign CPU. No floating point enters
any mathematical decision. Elapsed-time fields are informational only.

The primary seed and its unswitched variants are prior art. The added
restriction ranges over the seed's entire switching class and all
two-pair repairs. Source publication establishes reproducibility; the
scope does not resolve unrestricted existence on 22 vertices.
