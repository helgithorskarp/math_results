# R(5,5): unrestricted global edge window 392..511

This package proves that every 43-vertex graph with no clique or independent
set of order five has between **392 and 511 edges**.  It excludes the complete
391-edge class and, by complementation, the complete 512-edge class.  The
result assumes no symmetry or structured carrier.

The proof combines a global degree-excess argument with a complete physical
overlap enumeration from the published `(4,5;24)` catalogue.  The final 52
endpoint branches are UNSAT with stored, trimmed DRAT certificates.

Read [PROOF.md](PROOF.md) for the mathematics and [HANDOFF.md](HANDOFF.md)
for exact replay commands.

## Certificate layers

| file | role |
|---|---|
| `COARSE.json` | all 20,388 dense rooted profile pairs |
| `PHYSICAL.json` | all 698,368 physical common-graph maps and 330 survivors |
| `CLOSURE.json` | direct contradictions for 298 survivors |
| `CT.json` | exact 32-map/52-deficit branch join |
| `BRANCH_PROOFS.json` | 52 input cores and trimmed DRAT proofs |

The full reconstruction takes roughly 20–30 minutes on the campaign host.
The source catalogue is an external pinned input and is not included.

This is a necessary-condition theorem for a hypothetical good43, not a
construction of one and not a determination of `R(5,5)`.
