# Nonpotential colourings and 84 monochromatic heptagon pairs

**Completed result:** ordinary four-colourings of the 421-point heptagon
difference graph need not have potential form. Swapping a single vertex
in one published potential colouring makes the previously unresolved
pair [0,332] monochromatic. Both old UNKNOWN SAT inputs now have an
explicit, directly checked satisfying assignment.

The complete one-component Kempe test from all 42 published seeds gives
1260 different normalized colourings, 1218 outside the potential class.
Of these, 1008 break antipodal symmetry and 210 preserve it. Six compact
witness recipes and rotation show that **84 of 126 sqrt(3) pairs are not
forced nonmonochromatic**. The remaining 42 pairs are unresolved.
No five-chromatic graph or record improvement is established.

[PROOF.md](PROOF.md) gives the singleton witness, general Kempe criterion,
enumeration scope and six orbit representatives.
[witnesses.json](witnesses.json) contains all six short recipes, including
the underlying 21-potential rows. [expected.json](expected.json) records
the complete counts, the 84 covered and 42 residual pairs, and the
residual 14 equilateral triangles on the unit circle.

| Quantity | Exact value |
|---|---:|
| Seed colourings / tested colour pairs per seed | 42 / 6 |
| Single-component swaps / distinct normalized outcomes | 1260 / 1260 |
| Potential / nonpotential outcomes | 42 / 1218 |
| Swaps producing a monochromatic sqrt(3) pair | 756 |
| Covered pairs / covered rotation orbits | 84 / 6 |
| Unresolved pairs / residual rotation orbits | 42 / 3 |
| Direct post-swap unit-edge checks | 2328480 |
| Direct post-swap designated-pair checks | 158760 |

For two initially different-coloured vertices, swapping an arbitrary
union of components for one chosen colour pair can equate them exactly
when they have the two chosen colours and lie in different components.
One component then suffices. Thus unions do not extend this one-step
pair coverage. Sequences of swaps and other ordinary colourings are
outside the completed test.

## Reproduce

Use a full checkout and Python 3.11.2 (tested), standard library only,
with assertions enabled. From this directory choose two fresh external
directories. The first three commands replay the inherited geometry and
seed classification, including its alternative-basis audit:

```bash
python3 -B ../hadwiger_nelson_heptagon_difference_lifts/build.py --work /scratch/fresh-heptagon-geometry
python3 -B ../hadwiger_nelson_heptagon_difference_lifts/classify.py --work /scratch/fresh-heptagon-geometry
python3 -B ../hadwiger_nelson_heptagon_difference_lifts/audit.py --work /scratch/fresh-heptagon-geometry
python3 -B run.py --graph-work /scratch/fresh-heptagon-geometry --out /scratch/fresh-heptagon-kempe
python3 -B audit.py --graph-work /scratch/fresh-heptagon-geometry --out /scratch/fresh-heptagon-kempe
python3 -B controls.py
sha256sum -c SHA256SUMS
```

Expected audit status:
`ALL 1260 SWAPS AND SIX ORBIT WITNESSES VERIFIED`.
It also prints `EXPLICIT MODEL VERIFIED` for both old CNFs and reports
42 unresolved pairs. Generated graph/colour transcripts stay outside
the repository. No native solver or proof trace is needed.

The graph identity is SHA256
`54a68876eb8c55d885905482b8373c5542651f7683bf66d4406ce44825563458`.
The sorted concatenation of 1260 normalized rows, each 421 bytes with
values 0 through 3 and no delimiter, has SHA256
`052ad900425d2c64b8cf8b17d07fe858687f90232f315b9cc033f45dbc53b852`.
The audit compares every component and outcome record entrywise, checks
all edges directly, and independently reconstructs potential form.

The geometry replay took 6.48 seconds to build, 0.10 seconds to classify,
and 13.56 seconds for the alternative-basis audit. The complete swap
census and disjoint-set audit each took under one second. Peak memory
was not measured. [validation.json](validation.json) records the exact
timings and source identities. Small exhaustive controls check 5184 pair
cases and 5508 union-swap colourings; three invalid large colourings are
rejected. These are author-run checks, not an external review.

## Dependencies and stopping decision

The mathematical input is the
[parent heptagon package](../hadwiger_nelson_heptagon_difference_lifts/README.md),
source `b42754c605b69877056555955ac7f72a56e824f3`, Discovery Net
`bafkreieymqno3tggkhnxvrwoprgctvvi4mtk3yjvfs7vt6ykfwyje4ywbm`
at height 2971. Its geometry derives from the 21-point motif in
[Haugland, Section 2](https://arxiv.org/html/2608.04542v4).
This result refines the parent's unresolved ordinary-colouring question;
it does not contradict the correctly restricted 42-potential theorem.
No priority claim is made for Kempe swaps or colour normalization.

The primary-source calibration checked live on 2026-09-05 remains the
509-vertex graph of [Parts](https://arxiv.org/abs/2010.12665), also cited
as the record by Haugland's August 2026 paper. This pass supplies no
improved five-chromatic graph.

New HN-2 evidence was inspected through its
[fixed-partner compatibility audit](../hadwiger_nelson_parts509_partner_compatibility/README.md),
source `30b7abf9c070dd07bdc86d78c5c32485a7935233`, Discovery Net height
2977. Its eleven additional blocked pattern orbits and unsolved exact
composition formula concern a separate Parts lane and are not premises
here. The initial graph scan reached height 2982; final relevant refresh
and publication identities are recorded in the campaign checkpoint.

**Subsequent bounded checkpoint:** the
[complete two-step follow-up](TWO_STEP.md) now tests all 37968 second
swaps from these 1260 first-step rows. None makes a residual pair
monochromatic; all 42 remain unresolved. A separate disjoint-set audit
constructs and directly checks every second-step colouring. This does
not prove ordinary forcing or close a full Kempe equivalence class.

**Stopping decision:** reassess the residual terminal mechanism before
another swap layer. No third depth, enlarged graph, native runtime
extension or other construction phase has started. No job remains
running; external review is pending.
