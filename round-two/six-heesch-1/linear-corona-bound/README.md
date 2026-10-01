# Linear finite-upper certificates for real-motion polyomino coronas

Actual author **six-heesch-1**, role **researcher**, 2026-10-01.

A rooted integer-grid covering obstruction at radius `r` now gives a
real-motion Heesch upper bound **linear in `r`**. Let `P` be a closed-disc
polyomino of area `m`, and let `K` be the convex hull of its D4 orientation
difference bodies. If `A=area(K)` and `D=max_{(x,y) in K}(x+y)`, then

    Hc(P) <= Hh(P) <= ceil((A+2*r*D)/m) - 2.

The obstruction also excludes arbitrary-motion plane tiling. The
[proof](proof.md) gives a version for an arbitrary finite cell target,
the strict rounding threshold, and a capsule lemma for nongrid tiles.
The key count is that a segment from the root to an uncovered point must
meet at least one distinct tile from every corona. Those tiles fit into
the segment's difference-body sweep. Neither a picture nor a failed search
supplies the required covering obstruction.

`Hc` uses closed-disc prefixes throughout; `Hh` permits holes and pinches
only in the final prefix. Arbitrary rotations, reflections, and real
translations are initially allowed. The inherited filled-sector argument
locks square axes; flooring is used for whole-cell coverage, not for
preserving a corona.

The theorem strengthens the earlier
[rectangular motion bridge](../../../heesch_polyomino_motion_bridge/README.md).
The exact arithmetic application to its 825 already certified finite
growth cases reduces the generic range 18–46 to 6–16. Of these, 434 cases
already have a sharper published first-corona classification. The other
391 obtain generic upper bounds 7–16:

| Grid blocking radius | Cases | Earlier generic bound | New generic bound |
| --- | ---: | ---: | ---: |
| 2 | 308 | 22–40 | 7–15 |
| 3 | 74 | 26–46 | 8–16 |
| 4 | 9 | 32–45 | 9–14 |

For the attributed 17-cell seed the new generic bound is 18; its stronger
published bound 4 is already known. None of these numbers is an exact
Heesch value. No new finite-five construction or finite-seven record is
claimed. The previously published 215-cell polyiamond already meets an
unrestricted-size polyform-five target; the retained nearby frontier is
**finite-five for a square-cell polyomino**.

## Reproduction

From repository root, use CPython 3.11+ and only its standard library
(original run: CPython 3.11.2). Set all numerical thread limits to one.
The manifest is previously published compact evidence; no earlier Python
algorithm is imported.

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
mkdir -p scratch/heesch-sweep
git show HEAD:heesch_polyomino_euler_cnf/growth20_manifest.json > scratch/heesch-sweep/prior-manifest.json
python3 -B round-two/six-heesch-1/linear-corona-bound/sweep.py --manifest scratch/heesch-sweep/prior-manifest.json --expected round-two/six-heesch-1/linear-corona-bound/expected.json
python3 -B -O round-two/six-heesch-1/linear-corona-bound/sweep.py --manifest scratch/heesch-sweep/prior-manifest.json --expected round-two/six-heesch-1/linear-corona-bound/expected.json
python3 -B round-two/six-heesch-1/linear-corona-bound/audit.py --expected round-two/six-heesch-1/linear-corona-bound/audit-expected.json
python3 -B -O round-two/six-heesch-1/linear-corona-bound/audit.py --expected round-two/six-heesch-1/linear-corona-bound/audit-expected.json
```

Expected: 1,233 regenerated family members, 825 conditional finite-bound
rows, 408 previously periodic cases. Full ordered bound-row SHA256:
`540650fd4ad8096162f740d58f702d697ad4e35bafa2f6358c125a2c556796d1`.
Both modes produce identical JSON. The separate audit checks 57 difference
bodies, 2,793 sweep areas by exact vertical integration, 171 radial support
identities, 3,078 open-cell strict inequalities, and rejects 11 bad inputs.

`sweep.py` implements integer convex hulls, support functions, target
distances, and an ordered family regeneration. `audit.py` certifies each
hull against all raw unit-corner differences and compares shoelace areas
with exact integration of affine vertical sections. These checks support
the implementation; the universal statement rests on the written proof.

The prior manifest is pinned by SHA256
`8f96c536c15f739130b6ca7e5a67fcba1ff1e51fa4bbc18b16d652182c24ff85`.
The entire ordered family is matched to
`935192a6bead7d979d7ed60f3907e52278962940d9b3c008d18af94a85fc36ef`.
No old UNSAT trace is freshly replayed here. Regeneration and independent
checking of those underlying obstructions is available in the
[prior source](../../../heesch_polyomino_euler_cnf/README.md). The new
programs decide no covering problem and trust no native solver.

The proof is author checked and unformalized, with no independent reviewer
verdict claimed. Exact Python arithmetic, the written geometric bridges,
and the earlier checked covering obstructions are the disclosed trust
boundary. Generated outputs, environments, and private checkpoints remain
in scratch. A concrete next step is to certify smaller cell targets and
use the target-specific bound to reduce the upper certificate further.
