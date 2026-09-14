# No incompatibility between the 84 feasible heptagon pairs

**Completed, 2026-09-14:** in the exact 421-point, 1848-edge heptagon
difference graph, any two of the 84 previously feasible monochromatic
distance-sqrt(3) pairs can be monochromatic simultaneously. Five explicit
four-colourings and exact rotations cover all 3486 requests.

This retires a proposed joint forcing source for the sub-509 campaign.
No smaller subgraph of this source can forbid a tested conjunction either,
because the positive colourings restrict to that subgraph. No useful
composable forcing relation or five-chromatic drawing was obtained.
The shared physical milestone remains unmet.

[PROOF.md](PROOF.md) gives the exact quantifiers, coordinate formulas,
positive certificate argument and limitations.
[certificate.json](certificate.json) contains the 84 pairs and five words
in 5120 bytes. Its SHA-256 is
`e1f3cef665deb8224e2bb6798a5ecc2698726f44681814442166a9660e29474d`.

| Verified quantity | Value |
|---|---:|
| Distinct physical points / all unit edges | 421 / 1848 |
| Selected distance-sqrt(3) pairs | 84 |
| Labelled requests for two simultaneous equalities | 3486 |
| Distinct labelled equality partitions | 3458 |
| Classes of pair-set requests under 14 rotations | 252 |
| Base words / transported words / distinct transported words | 5 / 70 / 63 |
| Direct unit inequalities in the second checker | 129360 |
| Direct request-versus-word checks | 244020 |

The pairs' common colours are not required to differ. This is not a
classification of every proper partition of four terminals. The other
42 distance-sqrt(3) pairs remain outside the theorem; their earlier
unresolved queries have not been resumed.

## Reproduce

Use a full checkout and Python 3.11.2, standard library only. Choose a fresh
external work directory. From this contribution directory:

```bash
python3 -B ../hadwiger_nelson_heptagon_difference_lifts/build.py --work /scratch/fresh-heptagon-joint
python3 -B verify.py --graph-work /scratch/fresh-heptagon-joint
python3 -B audit.py --graph-work /scratch/fresh-heptagon-joint
python3 -B controls.py --graph-work /scratch/fresh-heptagon-joint
sha256sum -c SHA256SUMS
```

The first checker prints `ALL 3486 TWO-PAIR PRESCRIPTIONS EXTEND`.
The second prints `DIRECT LABELLED COVERAGE VERIFIED` after rebuilding
the geometry in the tensor basis Q(zeta_7,omega_6) and checking all labelled
requests without a symmetry quotient. The controls reject an improper word,
five individually proper words with incomplete coverage, and a wrong pair
domain. The primary check also passed with Python `-O`.

The primary and second checks took 6.23 and 12.15 seconds respectively;
[validation.json](validation.json) and [expected.json](expected.json)
record their outputs. No SAT solver or search log is needed to verify the
theorem. The proof trusts the coordinate specification, exact integer
arithmetic and the displayed finite checks. These are author-run checks,
not an independent-author review or a formal proof.

Four retained words were discovered by bounded CaDiCaL195 queries and one
by the previously defined two-step Kempe construction. Their recorded
[provenance](discovery_provenance.json) is descriptive; the proof checks the
actual words directly. Solver timeouts are not evidence. Earlier UNKNOWN
two-pair queries are all resolved positively by the final certificate.
All discovery jobs have ended, and their source and transcripts remain in
campaign scratch storage. Generated graph tables and logs are not published.

## Prior evidence and stopping decision

The exact drawing is inherited from the
[parent difference graph](../hadwiger_nelson_heptagon_difference_lifts/README.md),
source `b42754c605b69877056555955ac7f72a56e824f3`, Discovery Net
`bafkreieymqno3tggkhnxvrwoprgctvvi4mtk3yjvfs7vt6ykfwyje4ywbm`.
Its graph JSON has SHA-256
`54a68876eb8c55d885905482b8373c5542651f7683bf66d4406ce44825563458`.
The selected pair set comes from the
[Kempe result](../hadwiger_nelson_heptagon_kempe/README.md), Discovery Net
`bafkreidsjmeulr6k5hb4ytrgdblspwka5xrh56ntxhp54wfieyzda4ckrm`.
The parent geometry's independent acceptance and canonical recolouring,
`bafkreifchiirmj5gxehu4a3hyvdp6jt4ap25l6xlgtxoudb6asbl2e2x6y`,
were inspected before choosing this joint question. No prior full
ordinary-colouring classification is assumed.

The original motif is from
[Haugland, Section 2](https://arxiv.org/html/2608.04542v4).
The live primary-source refresh on 2026-09-14 still identifies
[Parts' 509-vertex, 2442-edge graph](https://arxiv.org/abs/2010.12665)
as the record. This result does not improve it or establish a global
vertex lower bound. No priority claim is made for the colouring method.

The local Discovery index remains stale at height 4363. Current repository
and team reports were refreshed separately. This lane stayed outside R2's
frozen-centre transfer, R3's triangular patches and R4's H510 repairs.
The declared finite source-selection gate has failed: retire this
two-pair mechanism, with no automatic extension to three pairs, phases,
or a larger heptagon host. The next pass must select a distinct physical
forcing premise after a fresh team refresh.
