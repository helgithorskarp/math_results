# Validation of the six new outside-parent bounds

Author: **six-covering-3, researcher**. Python 3.11.2 on Linux,
standard library only. No native solver, random choice, phase heuristic or
floating-point arithmetic is used.

The documented new-case reproduction command passed on the exact published
Python sources. It ran 26 sequential children: producer and independent
literal-AP checker for each of six parents, in normal and optimized modes,
then the scope/transport controls in both modes. Every child exited zero
with empty stderr. Maximum child runtime was 4.117378s,
and maximum child RSS was 21976 KiB, within the unchanged
20s guard and 1CPU/2GiB scope. Numerical thread settings were all one.

All 1,620 raw-pair records were compared entry by entry, including all
55,080 original marginals, in each mode. Each complete calculation maximized
over 14,978,520 phase intersections. Deficits by parent1,2,3,5,6,7 were
2,40,2,2,40,2. The six required-point hashes are distinct, even though the
bounds have the four-unit CRT symmetry explained in proof.md. The code
still checked each of the six cases separately.

Both modes rejected the same 27 intentional damages. Four numeric damages
ran the complete independent case checker; stream damages detect omitted,
duplicated, reordered and damaged raw rows. Frame controls reject the
wrong literal14/12 phase, an omitted prefix class, original21 omission,
original16 aliasing, pooled original18 singleton phases, canonical rather
than raw pairs, missing parents and inflated deficits. Definition-level
worst-row checks recover 222+982=1204 and 210+973=1183.

A genuine distinct period12 toy cover survives all partial-prefix marginal
bounds16,14,13,12,12,12. Other controls check the four CRT multipliers,
all original phase permutations and required-set transports, the exhaustive
41/24/65 original BASE/TAIL split, 362,880 BASE lift incidences and
241,920 TAIL parent incidences.

Certificate SHA256:

```
cad6c3bb40a2ed28316c821b04e1ce9bc4f7ab7744adaccf6bc9e1dccfa7f8ca
```

`verification.json` records exact checked source hashes and compact child
summaries. Every 270-record binary stream (20,520 bytes) and generated
operational receipt remains in workspace/scratch and is reproduced locally,
not staged. No private ledger, key, credentials, corpus, binary or logs are
part of the public contribution.

For the combined two-parent conclusion, the already published parent4
lemma9709 is a separate mathematical dependency. Its source and reproduction
command are stated explicitly in README and dependencies.json. The new
command does not claim to replay that older 288-map/four-stage certificate.
The six new deficits are unconditional for the literal P/36-original-BASE
inventory; the old parent4 conclusion used here is at least one hole only.

The checks are by different algorithms from the same author. Source
publication does not itself prove the lemma. Python execution, finite
completeness, the cited dependency and the ordinary completion/marginal/
CRT/lifting arguments are the trust boundary; no external independent
review, formalization, fullP exclusion or global L_min(8) improvement is
claimed. A guard failure or incomplete record would certify no exclusion.
