# Failed intake for fresh defect-support repair families

**The intake gate failed: 0 of 32 fresh graphs met the required score of
at most 16 monochromatic five-sets.** Their verified scores range from 146
to 180. The required eight-candidate registry was never sealed, and no SAT
instance was generated or solved. This checkpoint does not satisfy the
declared complete-family output gate and establishes no Ramsey exclusion.

The proposed next family would free every edge belonging to any current
monochromatic five-set of a qualifying graph, while fixing its other edges.
All assignments of those free edges would then require a target or checked
UNSAT proof. The preregistered intake threshold prevented applying that
experiment to this much poorer cohort. Neither the threshold, temperature
schedule, proposal count nor number of starts was enlarged after observing
the failure. See [DECLARED_GATE.md](DECLARED_GATE.md).

## Reproduce the evidence

Python 3.11+ standard library; no solver, catalog or network dependency.
Use a fresh output directory outside this source package:

```bash
python3 -B ramsey_r55_fresh_defect_support_intake_checkpoint/reproduce.py /tmp/r55-fresh-intake-check
```

Expected: `VERIFIED_FAILED_FRESH_INTAKE_GATE`. The command independently
checks all stored graphs in normal and optimized Python. It does not repeat
the failed generation schedule. To reproduce that specific schedule manually:

```bash
python3 -B ramsey_r55_fresh_defect_support_intake_checkpoint/generate.py /tmp/r55-fresh-intake-regenerated.jsonl
```

There are exactly 32 starts, seed 202609090000+i for i=0..31. Each starts
from 903 fresh pseudorandom edge bits, then makes 524288 annealing proposals
in eight cycles. The temperature in each cycle decreases in 64 stages from
1.25 to 0.1. A cycle after the first starts at the best graph so far. Metropolis
moves accept nonpositive objective changes and accept a positive change d
with probability exp(-d/T). Final strict improving descent ends at a
single-edge local minimum. No degree or symmetry constraint is imposed.

The fixed schedule made 16,777,216 annealing proposals in approximately 257
seconds on the recorded machine, plus the final descent evaluations.
Elapsed times are diagnostic and are not deterministic evidence. Generation
uses CPython's seeded Random and math.exp; exact graph replay across other
interpreter/libm versions is not promised. Every published graph is explicitly
pinned, so checking the failure does not trust reproducibility of the search.

## Independent audit and limits

The producer calculates a flip's exact change using triangle counts in the
two common neighborhoods. It cross-checks the objective after every cycle
with a separate recursive clique count. Before the run, 664 small literal
single-flip controls checked this implementation. A measured Python reference
runtime was short enough that no native rewrite was needed.

The independent checker imports no producer. It literally inspects all
962,598 five-subsets of each complete 43 graph, for 30,803,136 subsets total.
It also calculates all 28,896 single-edge objective derivatives: every current
monochromatic five-set contributes -1 to its ten edges, and every five-set
with exactly one minority-colored edge contributes +1 to that edge. All other
five-sets contribute zero. This verifies both the recorded objective and that
strict single-edge descent has terminated. Normal/-O replays agree and
reject corrupted objective and graph-padding inputs.

These are 32 finite, poor-quality endpoints of one heuristic schedule. They
do not bound the best achievable objective, show a multi-edge repair barrier,
exclude a complete 43-vertex target family, or disprove unconstrained search.
No defect-support family was instantiated. Publishing the failed intake and
its fixed parameters is intended to prevent an unrecorded repeat or silent
relaxation of this gate. No Discovery Net theorem is claimed for the failure.

The accepted h4009/h4015 structural base, h4021 interface, h4029 (now
independently accepted at h4037), and completed h4035 remain unchanged.
There are no new whole-task or q10-child verdicts. team-r55-1 retains h4021
integration and all 161 q10 survivors. No historical graph or teammate input
was used. A next pass must choose a distinct milestone rather than append
more starts, temperatures, looser thresholds or larger supports to this one.
