# Three-block entropy reduction for the complete Ramsey43 carrier

Forbidding monochromatic five-sets split **3+1+1 across three non-root four-clique blocks** removes **at least 74.452535% of h4059's remaining global bare carrier**. Every one of its 2,189,178 task carriers shrinks by at least 32.104439%. This is a certified cardinality bound; no complete task is decided and no good43 is produced.

The [proof](PROOF.md) combines three exact centred-triple counts with an explicitly checked entropy projection cover. Unlike an independent-event estimate, the bound accounts for overlapping matrix coordinates. The new events use only ordinary block/block matrices, so they separate from h4059's block/core contact restrictions.

From the repository root, using Python 3.11+ and g++ 12+:

```sh
python3 -B ramsey_r55_three_block_entropy/reproduce.py /tmp/r55-three-block-replay
```

The output directory must not exist. No data download, solver, h4059 replay, or survivor input is needed. Expected status: `REPRODUCED_THREE_BLOCK_GLOBAL_REDUCTION`. Generated binaries, matrix lists, and indexed physical streams stay in the external output directory.

The replay checks the complete census in Python and by a different C++ conditioning order, compares every intermediate profile, verifies all original palette states and transport identities, checks all 18 global covers and exact rational bounds, and runs literal physical controls in normal and `-O` Python modes. C++ release and address/undefined-sanitized output must agree byte-for-byte. `EXPECTED.json` contains the exact totals, rational upper certificate, and compact verification results.

[HANDOFF.md](HANDOFF.md) specifies the physical witness interface and the ownership boundary. The multiplier applies to complete parent carrier classes and unrestricted ordinary-matrix slices; it is not a bound on the teammate's conditioned q10 children.

The exact parent carrier is [h4059](../ramsey_r55_q9_core_contact_domains/README.md), independently accepted in [h4067](../ramsey_r55_q9_core_contact_domains_review1/README.md). The parent assumptions and separate color-orientation queue are recorded in `CONTEXT.json`. `VALIDATION.json` records the complete fresh replay (37.775 seconds) and its expected result SHA-256, `839a83302d2892b99041c41f3f46bbafb53de8fe4708689b5b2bcd98ce5021b0`.
