# Releasing cell quotas while preserving exceptional local profiles

An exact signature criterion broadens the permitted four-edge switches
and escapes the previously certified 384-K5 local trap. Eleven strictly
improving moves produce a verified **358-K5 graph** (172 red, 186 blue),
while retaining degrees, exceptional local profiles, mixed-K5 absence,
and all 884 pointwise root inequalities. **This is not a Ramsey graph
or a lower-bound improvement.**

For an alternating switch removing ac,bd and adding ad,bc, with X_v
the adjacency bitmask to the exceptional roots, the exact criterion is

```text
((X_a XOR X_b) AND (X_c XOR X_d)) == 0.
```

The former cell-quota restriction required an entire opposite pair
to have equal signatures. [PROOF.md](PROOF.md) proves the broader
criterion and its completeness, identifies the affected-row lifting
gate, and describes the concrete escape. Only the first move changes
cell quotas; it unlocks ten more strict improvements.

| Full one-switch census | 384-K5 seed | 358-K5 endpoint |
|---|---:|---:|
| Exceptional-profile-preserving supports | 17256 | 17276 |
| Quota-changing supports | 5837 | 5786 |
| Pointwise lifting failures | 3359 | 3032 |
| Further mixed-K5 failures | 13709 | 14052 |
| Admissible supports | 188 | 192 |
| Admissible quota-changing supports | 3 | 2 |
| Strictly K5-decreasing supports | 1 | 0 |
| K5-neutral supports | 0 | 3 |

The three endpoint neutral switches are recorded, not expanded. Thus
the endpoint census is not a neutral-component or whole-fiber barrier.
The endpoint still violates 34 central local caps and has Phi=86;
the actual K5 objective, not Phi, was minimized along the recorded path.

## Reproduce

Use a complete repository checkout: sibling source and seed dependencies
are SHA-256 pinned. CPython **3.11.2**, standard library only; no solver,
catalog, or group software is used in this calculation. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B verify.py --report /scratch/new-r55-profile-verify.json
cmp report.json /scratch/new-r55-profile-verify.json
python3 -B -O verify.py --report /scratch/new-r55-profile-verify-O.json
cmp report.json /scratch/new-r55-profile-verify-O.json
python3 -B controls.py --report /scratch/new-r55-profile-controls.json
cmp controls_report.json /scratch/new-r55-profile-controls.json
python3 -B -O controls.py --report /scratch/new-r55-profile-controls-O.json
cmp controls_report.json /scratch/new-r55-profile-controls-O.json
python3 -B search.py --work /scratch/new-r55-profile-search --max-steps 128
cmp GRAPH.json /scratch/new-r55-profile-search/GRAPH.json
cmp PATH.json /scratch/new-r55-profile-search/PATH.json
```

The search requires a fresh work directory. It saves the current graph,
path and scan records after each completed step, and terminates on the
first full scan with no strictly decreasing admissible switch, the step
bound, or zero K5s requiring a full audit. It does not expand neutral
components. The reference search stopped after 11 accepted moves and
a complete twelfth scan, in 5.953873 seconds, peak RSS 66248 KiB.
Discovery timing/RSS are informational, not reproducible byte-for-byte.
`discovery_report.json` records that run; no process remains active.

The independent verifier imports no search code. It uses perfect
matchings rather than the production opposite-pair generator, literal
root-edge changes rather than the bitmask criterion, unmerged named
pointwise inequalities rather than the compressed gate, and full K5
enumeration rather than the incremental update. It replays every path
graph through the original full five-set audit. Reference normal/-O
runs took 42.990955/42.912024 seconds and produced byte-identical reports.

The controls exhaust 131072 seven-vertex completions (4096 signature
assignments times 32 free-edge completions). They additionally compare
all 34532 seed/endpoint support entries, every feasibility classification,
all four-row versus all-row gates, and full color counts for all 380
admissible endpoint incidences. A first-pair-only lifting shortcut is
explicitly falsified; nonpreserving-switch and malformed-loop controls
are detected. Final normal/-O runs took 31.582405/31.850688 seconds and produced
byte-identical reports. Peak checker RSS was under 68 MiB.

Compact exact output hashes:

```text
GRAPH.json
122ed044228839122d6dba6d0f1cb87480818a6a8e8b277b6e5504d2da2e2cbc
PATH.json
ea432066b51fd7037f20d547ddeda892eee2d915255f0b210a7ac9474c0b3213
report.json
3bb8832a848abeb288f6aba3e019a1512df6e9b245d2253db42dc66f3142b677
controls_report.json
bdbe63ceeac0e67128ea61eb39f3ec55aa2922b9f305438fc0831ca049fdb166
```

## Dependencies and coordination boundary

The seed and exact K5 update come from
[actual-K5 obstruction repair](../ramsey_r55_k5_obstruction_repair),
substantive commit `bbe1323e94aa829a12c39c915a0c9c578e1c9028`, Discovery Net
`bafkreiguvijqgcwke3fxpb7osksrylohxr2wic7kpahkwu42xdu6mrv3su` (height 2821).
Retained gate and independent literal sources come from
[cell-preserving repair](../ramsey_r55_cell_preserving_repair);
the full graph inspector comes from
[triple graph realization](../ramsey_r55_triple_graph_realization).
Their exact source pins are in the scripts. The original realization's
aggregate retained-case certificate and elementary Ramsey-recursion
root bounds remain inherited inputs; actual cell quotas are released.

This is the non-symmetric graph-realization lane, not a restart of the
catalog neighborhood sweep or the order-three structured lane. The
prepublication refresh through graph height 2832 read the external
codegree-13 common-core footprint contribution (height 2823) and the
teammate's sharp empty-pair lemma/four UNKNOWN extensions (height 2829).
Neither supplies a constraint assumed here. The external guarded
local-deletion cuts (height 2751) likewise are not claimed to be imposed
or independently reviewed. The new switch result relies on none of
those unreviewed additions and does not contradict their scope.

The exact sources and finite checks are inspectable, but ordinary code,
proof alignment and hardware trust remain. There is no independent
external review of this new contribution and no historical-priority claim.
The coherent milestone ends here. A possible next bounded step is to
inspect the three actual-K5-neutral exits from the 358-K5 endpoint;
that is not part of the present computation.
