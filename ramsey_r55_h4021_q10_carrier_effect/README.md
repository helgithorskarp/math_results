# h4021 on the complete h3987 UNKNOWN fixed-prefix carrier

The h4021 interface gives **zero direct `CONFLICT` embeddings and zero task
closures** on all 161 h3987 q10 tasks currently marked `UNKNOWN`.  This is an
exact negative integration result, not a decision of a survivor.

The obstruction is decisive at the fixed-prefix level.  Every h4021 conflict
embedding contains an 18-edge monochromatic star at its root.  Reconstructing
all 161 q10 prefixes gives maximum fixed red degree 6 and maximum fixed blue
degree 6.  Thus none of the 13,846 task/root/color triples can begin a direct
conflict embedding.  This covers all
194,747,098,693,790,360,516,198,400,000 ordered interface embeddings without
enumerating their irrelevant module positions.

Run from the repository root into a fresh directory:

```bash
python3 -B ramsey_r55_h4021_q10_carrier_effect/reproduce.py \
  /tmp/r55-h4021-q10-carrier-replay
```

Expected status:
`REPRODUCED_H4021_Q10_ZERO_DIRECT_CARRIER_EFFECT`.
The replay uses Python 3.11+ standard library only, invokes no solver, checks
normal and assertion-disabled Python, independently reconstructs the S4 x S3
word quotient and all 260 task records, exercises the actual h4021 receiver,
and rejects altered numerical claims.

The scope is deliberately narrow.  A partially substituted h4021 instance
may still return a valid nonempty `CLAUSE`, and such clauses could help a later
SAT mechanism.  This result does not count that possible search pruning and
does not say that free edges cannot later complete the template.  It produces
no good43 graph and leaves the h3987 ledger at 99 certified UNSAT / 161
UNKNOWN.  See [PROOF.md](PROOF.md) and [HANDOFF.md](HANDOFF.md).
