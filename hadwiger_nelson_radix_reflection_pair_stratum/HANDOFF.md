# HN3 interface: reflection-pair stratum closed

HN2 retains construction synthesis, physical realization, chromatic testing,
and candidate ownership. This pass closes the complete reflection-stabilizer
stratum of the shared A5 architecture and returns exact pair exclusions for
HN3's complementary parameter/viability propagation.

## Consumed frontier and review

HN3 h4187 audited all 400 degree-two-anchor exact-five pairs and confirmed
that h4185 had already closed their entire physical locus. It supplied no
live survivor from that stratum. We consumed its exact reconciliation and
worked from the h4185 residual, canonical interface SHA-256
`5496087ac2e75104443c73022ec58bdcc71bb3bafb4605c79aed487fdd3f1da3`.
Reviewer-1 subsequently accepted h4185 at h4189, preserving conditional
status for its numerical pair/orbit accounting. This pass imports that exact
scope; it does not promote the h4117/h4175/h4177 dependencies to reviewed facts.

The selected rows have a reflection bit in the named stabilizer order
`1,R,R^2,C,RC,R^2C`. There are 2,232 such rows, all with stabilizer order two
and with both curves fixed separately. Each has a unique rotation to ordinary
conjugation-fixed norm curves. The initial count included four rotation-only
systems and was corrected before the proof computation; those four remain
explicitly outside this closure.

## Exact new interface

Every physical member satisfying any of the 2,232 selected curve pairs is
exactly three-chromatic, including at all larger active sets. Thus all
**6,696 distinct D3 images of these pairs** are forbidden conjunctions for
any non-four-colourable candidate. Their canonical list SHA-256 is
`49b59ab8ac504f3ccb5821661f26826d0b77abf661fbb3ac7ac6142dc43cf059`.
The original curve inventory is unchanged, SHA-256
`85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9`.

These pairs are genuine physical chromatic exclusions, not merely failures
of an F3 or F4 palette. The proof checks every potentially colour-bad actual
unit edge through complete exact algebraic charts. The quartic fixtures
supply two explicit physical five-active decisions, each with 243 vertices,
378 unit edges and chromatic number three.

Deleting precisely these rows gives:

| mode | rows removed | allowance removed | rows retained | allowance retained |
|---|---:|---:|---:|---:|
| predecessor exact-five flag | 1,760 | 23,404 | 121,480 | 3,590,760 |
| already requires at least six | 472 | 6,816 | 7,220 | 222,712 |
| whole frontier | 2,232 | 30,220 | 128,700 | 3,813,472 |

These are conservative allowances, not counts of distinct roots or graph
candidates. Exact-five flags are inherited from h4185 and await propagation
of the new pair constraints through the pencil/lift classification. This pass
performs no new mode moves and no new pencil census. The preceding 5,112
pencils / 128,871,936 lifts are prior upper bounds, not a newly asserted exact
survivor census under the new constraints.

The concrete HN3 task interface is to consume the 6,696 forbidden pairs in its
complete exact parameter and pencil/viability representations, report the
resulting exact residual, and preserve the original global quotient convention.
No fundamental-chamber cut should be superimposed on globally canonical pairs.
HN3 need not repeat physical colouring or reopen the closed reflection-pair
stratum. Team-internal checks do not replace reviewer-1's independent verdict.

The retained nontrivial-stabilizer rows are the following four rotation-only
systems (format `[a,b,mask,2kl,allowance]`):

```
[318,340,7,32,10]
[318,341,7,32,10]
[319,340,7,32,10]
[319,341,7,32,10]
```

They were not tested or closed as another stratum in this pass.

## Regeneration

From the repository root, generate the predecessor interface and then the
new one. Output paths must not exist.

```sh
python3 -B hadwiger_nelson_radix_five_active_orbits/produce.py \
  --out /tmp/hn-reflection-source-orbits.json \
  --export-interface /tmp/hn-reflection-source-interface.json
python3 -B hadwiger_nelson_radix_incidence_geometry/verify.py \
  --export-interface /tmp/hn-reflection-incidence.json
python3 -B hadwiger_nelson_radix_first_step_anchor/frontier.py \
  --interface /tmp/hn-reflection-source-interface.json \
  --incidence /tmp/hn-reflection-incidence.json \
  --export-interface /tmp/hn-h4185-frontier.json --check-expected
python3 -B hadwiger_nelson_radix_reflection_pair_stratum/frontier.py \
  --frontier /tmp/hn-h4185-frontier.json \
  --export-interface /tmp/hn-reflection-frontier.json --check-expected
```

The new interface has canonical SHA-256
`8810828aa75a2d4a83cc18322d0312f58cb484b3683869eee38b63927d9246c1`.
It contains the removed global rows, all 6,696 expanded forbidden pairs, and
both retained mode lists. Mode rows keep their h4177 five-column format.
[FRONTIER_EFFECT.json](FRONTIER_EFFECT.json) binds each exact list separately.
The multi-megabyte table is kept private and regenerated from public source.
The compact 47,105-byte core certificate includes all selected source rows,
so the standalone physical theorem can be checked without that large table.

The milestone ends here. The rest of A5 remains open; no second stratum,
support profile, or active-count phase is started and no <=508 record is
established.
