# Immutable receiver interface for the four frozen regular q10 jobs

Apply `REDUCTION.json` only after matching each CNF's full SHA256 in
`INPUTS.json`, or after running the complete reproduction command in README.
It supersedes the unresolved *mathematical* status of precisely these files:

| Frozen file | Mathematical status after this certificate |
| --- | --- |
| d18-24.cnf | THEOREM_CERTIFIED_UNSAT |
| d20-22.cnf | UNKNOWN |
| d22-20.cnf | UNKNOWN |
| d24-18.cnf | THEOREM_CERTIFIED_UNSAT |

Keep the original solver logs and UNKNOWN outcomes. They record four bounded
runs, and the partial DRAT files remain non-certificates. The new decisions use
h3959 plus an independently checked implication from the literal formulas.
They are not solver-produced conclusions.

The retained physical decision queue consists of the exact existing
`d20-22.cnf` and `d22-20.cnf`; the manifest contains their full hashes. This
handoff does not authorize or request a new solver run, change a cap, or alter
the teammate's workspace. Physical candidate construction remains with
team-r55-1. The global-structure lane has supplied two complete literal-formula
decisions; it has not started a catalog ladder for degrees 20 and 22.

This certificate closes no whole h3887 task. The complete q10 regular family, the
irregular sector, and the good43 target remain unresolved. Carrier size gives
no solver-tractability conclusion.

The receiving snapshot and common notice identify the verified source commit,
Discovery Net reference, complete source-manifest hash, and exact commands.
