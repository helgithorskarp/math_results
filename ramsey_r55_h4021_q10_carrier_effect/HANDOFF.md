# Mechanism boundary and ledger handoff

The h4021 fixed-prefix integration gate is complete on the entire owned h3987
UNKNOWN carrier.

Exact effect:

- tasks inspected: 161 of 161 UNKNOWN children;
- fixed edges per task: 76 in 132 tasks, 77 in 29 tasks;
- maximum fixed same-color degree: 6, versus 18 required by h4021;
- direct h4021 `CONFLICT` embeddings: 0;
- new task verdicts: 0;
- operative ledger after this result: 99 certified UNSAT / 161 UNKNOWN.

This retires h4021 as a direct fixed-prefix closure mechanism for these q10
children.  It does not retire the cut as a possible nonempty learned clause in
a genuinely different exact search mechanism.  No such SAT integration,
sibling formula, embedding sweep, local-pair enumeration, or two-switch
extension was started here.

h4001 remains a separate q7-r5 ledger with 518 excluded and 122 UNKNOWN; its
counts are not combined with h3987.  h4035 changes q8/q9 global-carrier
accounting and has no q10 constraint.  No good43 candidate was found.
