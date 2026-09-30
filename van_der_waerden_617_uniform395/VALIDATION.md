# Actual validation

Author: six-vdw-3, researcher. These are successful local checks by the
author; external independent review is not asserted.

The complete frozen result matches `expected.json`, SHA256
`eb5a74e2baf4bd4d767bc97c52836976df10c9270e9dc2ab853ddd066a0ca558`.

| Run | Python | Optimization | Seconds | Self peak RSS KiB | Child peak RSS KiB |
| --- | --- | ---: | ---: | ---: | ---: |
|stdlib|3.11.2|0|4.225|24020|0|
|optimized|3.11.2|1|4.434|25340|0|
|isolated-fresh|3.12.14|0|119.588|39712|55964|

Every run replays13 new joint197 box exclusions:41 root cases,50 exact
stages, both zero-loss trees in both actual colours, all base capacities,
all inherited full domains and complete anchor coverage. It combines the
new proof with four explicit byte-pinned prior result summaries, without
replaying the old602 or201/269 proofs.

Every run rejects73 malformed, corrupted, restricted or incomplete proof
inputs. These include hidden screens and forced edits, omitted anchor roots,
omitted refinement stages, wrong actual APs, invalid cover2 triples, capacity
violations, a nonpositive final packing, missing old-tree children, missing
zero-loss premises and incomplete global phase coverage. One damaged old
leaf still proves its original cap196 case but cannot justify the stronger
removed-zero conclusion; the new checker rejects it.

Definition-level controls exhaust64 sole-root activation assignments,
160 edit subsets on the13 actual anchors,8500 clipped-capacity models and
26682 removed-zero triple models. Python optimization does not disable
these checks; no proof guard depends on `assert`.

The isolated Python3.12.14 run also regenerated all50 numerical proposals
with highspy1.11.0/numpy2.2.6. Each was checked exactly on its full domain
independently derived from the frozen predecessor proof. All41 terminal
exclusions passed, all50 freshly derived screens recovered the frozen
screen, and all50 certificate files matched the frozen bytes. This includes
the smallest final margin, phase184 root1408: `7490/1000000`.

Native jobs ran serially with one thread and a15-second limit. The largest
native elapsed time was2.731 seconds and largest native peak RSS was55964 KiB. These limits were not raised.
The default standard-library route needs no solver or network access.

The fresh route deliberately uses proved frozen predecessor domains. Its
successful regeneration is additional evidence; the frozen integer route
is the complete primary proof. Neither solver noncompletion nor lack of
an AP-free witness is used to infer nonexistence.
