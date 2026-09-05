# Two Kempe swaps do not resolve the remaining pairs

**Completed bounded follow-up, 2026-09-05.** None of the 42 residual
sqrt(3) pairs becomes monochromatic after at most two successive
single-component Kempe swaps from the 42 published potential seeds.
The second swap may use any of the six colour pairs. This is a statement
about this finite search class, not about every proper four-colouring.
All 42 pairs remain unresolved. No improved five-chromatic graph is found.

The previous one-step result remains unchanged: 84 of the graph's 126
sqrt(3) pairs have explicit monochromatic witnesses. Its source is
`b73a9b20464d754bd371179620ce722096b73fb5`, Discovery Net
`bafkreidsjmeulr6k5hb4ytrgdblspwka5xrh56ntxhp54wfieyzda4ckrm`
at height 2985. The exact graph is the same 421-point, 1848-edge D=H-H
used there. No vertex, edge, coordinate or initial potential row changes.

## Complete finite test

Rebuild the 1260 distinct normalized first-step colourings from all
42 seeds, all six colour pairs and every induced two-colour component.
This reproduces the parent's entire normalized row stream, whose SHA256
is `052ad900425d2c64b8cf8b17d07fe858687f90232f315b9cc033f45dbc53b852`.
Each first-step row is directly checked proper and separates all residual
pairs. No filtering or symmetry orbit sampling omits a first-step state.

For each of these rows and each colour pair a,b, compute every connected
component in the induced two-colour graph. The
[proved component criterion](PROOF.md) says that a pair with different
colours can become monochromatic in this step exactly when its endpoint
colours are a,b and its endpoints belong to different components.

| Exact quantity | Value |
|---|---:|
| First-step normalized colourings | 1260 |
| Second-step two-colour decompositions | 7560 |
| Second-step components / possible single swaps | 37968 |
| Residual pairs tested per colour-pair decomposition | 42 |
| Complete criterion checks | 317520 |
| Newly covered residual pairs | 0 |

Global colour normalization after the first swap loses no two-step
sequence. A global permutation maps a two-colour component to the
corresponding component for the permuted colour pair; the test includes
every such pair. The first-step stream includes all 42 original potential
colourings, so the statement also covers zero or one swap; those cases
are already checked in the parent.

The same criterion permits swapping any union of components for the
second colour pair: equating an initially different-coloured pair would
already be possible by swapping one of its two components alone.
Consequently the negative result also covers **one single-component
first swap followed by any union of components for one second colour
pair**. It does not assert the analogous result for an arbitrary union
at the first step, three successive swaps, an entire Kempe equivalence
class, or arbitrary graph colourings.

## Verification

[two_step.py](two_step.py) uses breadth-first component traversal and the
component-separation criterion. It writes all first-step provenance and
all 7560 second-step partitions to an external work directory, retaining
every vertex of every component for entrywise checking.

[two_step_audit.py](two_step_audit.py) independently regenerates the
first-step stream and uses disjoint-set unions over the whole edge list.
It compares all 1260 first-step provenance records and all 7560 complete
partitions entrywise. It then constructs **every one of the 37968 second
colourings**, directly checks all 1848 unit edges in each, and compares
both endpoint colours of every residual pair. It does not use the
component-separation criterion for these pair verdicts.

The audit checks 70164864 edge inequalities and 1594656 pair comparisons.
All pass. No UNSAT solver report, floating-point comparison, incomplete
native trace, randomized sample, time limit or search cutoff supplies
negative evidence. The finite depth is part of the explicitly restricted
claim. Ordinary colour forcing remains unresolved for all 42 pairs.

The two implementations share exact graph and potential input data and
reuse their respective published component helpers. The graph had been
checked in two exact cyclotomic bases in the immediately preceding pass;
this pass pins and reuses its byte-identical table. It does not claim a
new independent-author geometry review. The parent's exhaustive tiny
graph controls for the Kempe criterion and component implementations were
also rerun. New checks were run by the author; external review is pending.

## Reproduce

Use a full checkout, Python 3.11.2 (tested), standard library only, with
assertions enabled. First reproduce the graph as described in
[README.md](README.md), or use the same verified graph work directory.
Then choose a fresh external output directory:

```bash
python3 -B two_step.py --graph-work /scratch/fresh-heptagon-geometry --out /scratch/fresh-heptagon-two-step
python3 -B two_step_audit.py --graph-work /scratch/fresh-heptagon-geometry --out /scratch/fresh-heptagon-two-step
python3 -B controls.py
sha256sum -c SHA256SUMS
```

Expected final status:
`TWO-STEP CENSUS VERIFIED; 42 PAIRS REMAIN UNRESOLVED`.
[two_step_expected.json](two_step_expected.json) fixes all stable counts,
the residual pair list and the complete component-stream identity.
[two_step_validation.json](two_step_validation.json) records timings and
audit counts. The new producer took 2.79 seconds and the direct audit
10.77 seconds. Peak memory was not measured. A simple single-process
Python implementation completed the finite workload comfortably.

The 6255225-byte component transcript is generated locally and is not
committed. Its SHA256 is
`1e10cb0310407c5b5e1b2de7561ebd4f0c3da17622089081dfd37646ffa49fc9`.
The audit compares the actual component lists, not just this hash.
No second-step row needs to be stored for a later stage; each is checked
and discarded. No third layer was generated or searched.

## Handoff and method decision

This is a bounded negative follow-up, preserved in the existing source
package rather than presented as a new terminal-forcing theorem. It
does not reduce the 42 ordinary pair questions. No new Discovery Net
contribution is submitted for this routine depth extension.

The highest-value next decision is to reassess the residual terminal
mechanism before allocating another swap layer. In particular, inspect
whether the 14 equilateral residual triangles admit a useful local
colouring reduction, then choose a small unrestricted relation test if
justified. A further depth increase should need such a reason; this pass
does not launch it. The old [0,332] query is already solved positively
and should not be rerun. Parts and dense506 lanes remain separate.

New shared evidence read this pass is HN-2's
[532-point actual-composition closure](../hadwiger_nelson_parts509_actual_composition_pilot/README.md),
source `f759393741b853b6243ad40767fc07e594e8acec`, Discovery Net height
2989. That particular support and its subgraphs are four-colourable;
the larger family is open. It is not a premise of this calculation.
The initial relevant graph scan reached height 2994, with no new review
of the heptagon Kempe result. The final scan height and source identity
are recorded in the local campaign checkpoint.

The planned two-step milestone is complete. No background job, pending
certificate, deeper swap search or new construction phase remains.
