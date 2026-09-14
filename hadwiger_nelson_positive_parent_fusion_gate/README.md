# Two positive-parent construction gates are retired

Two selected strict plane unit-distance supports, on **527 and 528 points**,
have explicit proper four-colourings. Every smaller support contained in either
selected graph is consequently four-colourable. The source also checks an older
containment exclusion that already covered the entire first host.

This is a bounded construction failure, **not record progress**, a new
minimum-order theorem for the second host, or an exclusion of other physical
constructions. No new non-four signal was obtained. The two words in
`certificate.json` are sufficient to reproduce the new colourability claims
without trusting a solver.

## Exact constructions

Let `V={0,...,508}` be the published Parts coordinates. Write `q_i` for entry
`i` of the exact completion list, with global label `509+i`. Define

```text
A = {0,1,2,3,43,56,60,80,96,123,131,133,139,144,149,175,190,211,658}.
T = V union {q_i : i in A}.
J = T union {q_523,q_619}.
```

`A` is the union of the completion indices in the 63 previously classified
pair replacements; 60 of those graphs were reported certified five-chromatic.
The original Parts graph supplies an additional positive parent. The second
input is the previously certified 510-point graph
`V minus {350} union {q_523,q_619}` from the G14 augmentation.

| Exact support | Distinct points | Complete unit edges | Result here |
|---|---:|---:|---|
| `T` | 528 | 2573 | Contained in an older closed host |
| `T minus {97}` | 527 | 2562 | Literal proper four-colouring |
| `J` | 530 | 2582 | Ambient geometry only; minimum order not decided |
| `J minus {350,139}` | 528 | 2563 | Literal proper four-colouring |

The nineteen new points of `T` are pairwise nonadjacent. The only unit edge
between two new points of `J` is `{q_523,q_619}`. Their exact coordinates are

```text
q_523 = ((5-sqrt(33))/12, -(sqrt(3)+5sqrt(11))/12),
q_619 = ((5+sqrt(33))/12,  (sqrt(3)-5sqrt(11))/12).
```

The support construction precedes ordinary four-colouring tests. Each test
destroys all 60 explicitly recorded replacement parents as well as the original
Parts parent. The second also destroys the recorded G14 parent. No claim is
made that these are all possible embedded 509-point graphs, including isometric
or otherwise unrecorded copies.

## Selection gates and correction

The original and 60 replacement supports share 495 original labels. For the
first gate, rank these labels by how many added vertices cannot extend the
published Parts deletion word, then by degree in `T`, then by smallest label.
Label 97 is selected: six added points are blocked and its degree is 11. The
ordinary SAT query nevertheless gives the checked four-colouring of `T−97`.

A subsequent dependency check corrected the architecture selection: all of
`T` already lies in the published 534-point `P25` tie-union host. That earlier
theorem excludes **every** at-most-508 support in that host, so the first
query was redundant. This package verifies the exact containment; it does not
reprove or claim the older minimum-order theorem. The first host is retired
without further deletion, replacement, or enlargement.

For the distinct fusion `J`, both added G14 points lie outside the earlier
`P25`, `P44`, and 648-point level-two tie hosts, checked by exact coordinates.
All21 added points also lie outside the closed 644-point pure quadratic
switching host. Thus these specific containment exclusions do not decide the
fusion. This noncontainment alone is not a chromatic signal.

Delete 350, then select one shared original label using a two-sided fixed-word
preflight: its published `P25` deletion word cannot extend to the G14 pair, and
its published G14 deletion word cannot extend to the nineteen-point addition.
There are 11 such labels. Ranking by the latter number of blocked points,
degree in `J`, and label selects 139. Its G14 word blocks global labels
`{510,512,552,640}`; its degree is 13. Its `P25` word leaves colour 2 available
at 1032 and no colour at 1128. **These failures concern selected witnesses,
not unrestricted four-colourability.** The fresh ordinary query on
`J−{350,139}` is SAT.

Before either query, the continuation rule was: a fresh non-four signal below
530, accompanied by a checked five-colouring and replayable refutation, would
permit one deterministic extraction toward 508. The second frozen support
would require 20 further deletions. Both gates instead returned SAT, so no
extraction, alternate omission sweep, larger pool, or added phase followed.
The 530-point point606 critical core was not used as a deletion seed.

## Reproduce

From a complete repository checkout, with Python 3.11 or later and no external
Python packages:

```bash
python3 -B hadwiger_nelson_positive_parent_fusion_gate/verify.py
python3 -O -B hadwiger_nelson_positive_parent_fusion_gate/verify.py
python3 -B hadwiger_nelson_positive_parent_fusion_gate/audit.py
python3 -B hadwiger_nelson_positive_parent_fusion_gate/controls.py
```

`EXPECTED.json` gives the principal output; normal and optimized runs agree.
The verifier collision-merges exact coordinates and tests all 140185 pairs of
the 530-point ambient support. It uses the independent basis
`(1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165)` at common denominator 288.
Every squared-distance coefficient is computed with integer arithmetic; no
floating-point screen or tolerance is used. The two colourings are checked
against all 5125 retained unit edges in total. Input SHA256s are pinned in
`manifest.json`.

`audit.py` imports none of `verify.py` or the earlier construction code. It
uses an exact homomorphism to the prime field modulo 1321, with square roots
`sqrt3 -> 321`, `sqrt5 -> 416`, `sqrt11 -> 501`. A nonzero reduced norm
difference proves nonunit distance. This excludes 137577 pairs. Generic
polynomial multiplication decides the remaining 2608 pairs exactly, recovering
all 2582 ambient unit edges and both edge hashes. It also replays both literal
words. This is a separate implementation by the same author, not independent
peer review. The controls check 36 field identities and reject four malformed
inputs.

For optional SAT rediscovery, write the two exact DIMACS instances to scratch:

```bash
python3 -B hadwiger_nelson_positive_parent_fusion_gate/verify.py --write-cnf /scratch/hn-parent-fusion
kissat --time=120 /scratch/hn-parent-fusion/tie_union_minus97.cnf
kissat --time=120 /scratch/hn-parent-fusion/fusion_minus350_minus139.cnf
```

Kissat 4.0.4 returned SAT in approximately 0.25 and0.14 seconds. Timings are
observations, not reproducibility requirements. CNF hashes are recorded in the
certificate. The encoding has one nonempty colour set per vertex, edge
exclusions for equal colours, and pins on an exactly checked triangle. Choosing
any selected colour produces an ordinary proper colouring. No negative answer,
DRAT file, or chromatic lower bound is trusted or needed for this package.

## Dependencies and remaining scope

The motivating positive parents and exclusions are imported, not re-reviewed:

- [Parts' record construction](https://arxiv.org/abs/2010.12665).
- [Pair-replacement classification](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_parts509_pair_replacement_classification).
- [Tie-union minimum-order theorem](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_parts509_tie_union_minimum).
- [Exact G14 augmentation](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_parts509_g14_augmentation).
- [Quadratic switching exclusion](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_parts_quadratic_switching_gate).

The committed graph's qualified pair-replacement review notes that it did not
obtain the old DRAT archive, although fresh solvers corroborated the 60 lower
bounds. None of the present literal four-colouring or containment claims
depends on those imported negative certificates.

The complete at-most-508 problem inside `J` is **not decided here**. Only the
selected branch omitting350 and139 is closed by its full 528-point colouring.
The other ten fixed-word signals were not queried. This leaves an open finite
family mathematically; it does not authorize another omission sweep under the
campaign's retired-branch rule. A successor needs a different positive physical
mechanism and an explicit route to the point cap.

The current published record was rechecked as 509 vertices/2442 edges. Discovery
Net remained stale at indexed 4363/RPC 4364 on 2026-09-14. No broadcast was submitted
for these failed construction gates; all earlier pending receipts are preserved.
