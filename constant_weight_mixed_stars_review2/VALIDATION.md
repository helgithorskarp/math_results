# Independent validation record

**six-reviewer-2, independent mathematical reviewer**, 2026-10-01.
All entries below are complete exact checks, with explicit exceptions rather
than Python assertions. CPython 3.11.2; g++ 12.2.0, C++17,
`-O2 -Wall -Wextra -Wpedantic`; standard libraries only. Every numerical
thread setting was one, and intensive jobs ran sequentially within the
unchanged 1 CPU / 2 GiB scope.

## Complete mathematical evidence

| Component | Exhaustive domain | Result |
| --- | --- | --- |
| First incidence graphs | 408 path, 24 cubic bipartite, 2,408 triangle graphs | 8 + 8 + 1 + 612 orbit cases |
| First-star covers | All 629 cases, independent native and literal implementations | Complete covers 2, 2, 2, 0 by marked shape; native 2,885 states, literal 36,267 |
| Mixed shape 0 | 110 C-orbits, 353,831 cover fibers | 20 covers, 120 actual second stars, 20 joint orbits |
| Mixed shape 2 | 161 C-orbits, 530,198 cover fibers | 15 covers, 60 actual second stars, 15 joint orbits |
| Double-row coupling | All 240 ordered markings per template, 85,995 fibers | 148 second stars, 31 joint orbits |
| Common residual ceilings | All 31 double, 20 mixed-0 and 15 mixed-2 cases | Reject residual sizes 22, 22 and 21; 20,154 nodes, maximum 1,649 in one case |
| Sharp fixtures | All words and word pairs in supplied attaining examples | Restricted totals 58, 58, 57, with exact hypotheses |
| Historical baseline | All 69 words and pairs | A single saturated (2,2,1) row occurs at coordinate 3; known construction |

Each mixed census retains all 560 labeled C choices through explicit orbit
weights and 2,118,918 weighted labeled leaves. Independently regenerated
inputs and every complete output batch, including every empty fiber, agree
with authenticated author reference summaries. Those summaries are optional
comparison data, were read without mutation, and are not needed for public
reproduction or exclusion. No target-author executable code was run.

The common bounds and attaining fixtures are audited. Smaller individual
residual maxima and mixed shape 1 are outside this verdict. Imported global
degree/support/remaining-row results are identified in [REVIEW.md](REVIEW.md).
The unrestricted interval remains 69--72.

## Cold computation and packaging checks

| Run | Seconds | Peak Python RSS, KiB | Native states | Maximum states per native fiber |
| --- | ---: | ---: | ---: | ---: |
| Complete cold mixed shape 0 | 82.2624 | 58,156 | 138,466,231 | 1,500 |
| Complete cold mixed shape 2 | 110.1347 | 57,920 | 179,043,162 | 1,088 |
| Complete double degree carrier | 19.4115 | 21,868 | 10,744,350 | 590 |
| Normal complete stable-record packaging | 34.8056 | 25,216 | First/double/residual rerun; source-bound mixed resume | Same mathematical record |
| Optimized Python stable-record check | 38.1233 | 27,560 | First/double/residual rerun; source-bound mixed resume | Same mathematical record |

The normal packaging command used `--record` to write the expected baseline.
The optimized command omitted `--record` and compared every byte of that
complete stable mathematical record. Neither packaging run is presented as
a second cold mixed census. The original cold censuses completed before the
resume metadata check was added; the exhaustive algorithms and kernel did
not change, and their completed outputs had already been compared entrywise
before binding them to the source hashes.

All generator roots and native/residual searches retained the original
200,000-state and ten-second guards. Maximum carrier-root states were 42,181;
maximum first-incidence root states were 10,491. No timeout, UNKNOWN,
incomplete branch or resource failure supplied any exclusion.

## Controls and trust boundary

- The actual residual threshold engine agrees with exhaustive subset truth
  at the optimum and optimum plus one for all 1,024 five-vertex compatibility
  graphs, realized by literal sets: 2,048 comparisons.
- Six additional literal threshold controls pass. A zero residual guard
  reports INCOMPLETE visibly.
- The native kernel returns the genuine one-quadruple cover on four points,
  rejects four malformed inputs, and reports INCOMPLETE for a zero guard.
- Every first-star cover agrees between the native point-partition kernel
  and a separately written literal pair-set recursion.
- All actual point permutations, orbit coverage and positive packings are
  checked explicitly. All external runtime inputs and prior reviewer reuse
  are hash-pinned in [INPUT.json](INPUT.json).

This is an ordinary computer-assisted proof, not proof-assistant verification.
The native kernel and exact primitives are openly reused from this reviewer's
previous sources. The residual binary/color-bound algorithm is also used by
the target's replay; the independent degree carriers and point-partition
cover search supply the principal algorithmic separation. Written reductions,
the compiler/interpreter and exhaustive code remain trust boundaries.

For an independent proof run, use a fresh work directory. Source-bound caches
are a resume convenience and do not authenticate arbitrary user-supplied
results. Public reproduction regenerates all bulky data locally; only source,
small manifests and this compact expected record are published.

Complete [expected.json](expected.json) SHA256:
`b78f7d5cd879c5f4b475084fc892d5f5655e7ac6ea31f7138b83a2dedcbf7a68`.

The final publication-path normal check used the default repository inputs,
matched their historical pins, and compared the complete stable record in
39.5829 seconds, peak Python RSS 25424 KiB. It
reran first/double/residual work and controls and reused the source-bound
completed mixed censuses, exactly as disclosed above.
