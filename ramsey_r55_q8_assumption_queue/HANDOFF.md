# Non-q10 operational handoff

Scope: all original `bo1-q8-r{5,6,7,8}-c000000..c546355` tasks. No q7, q9
or q10 worker is admitted by this interface. The existing h4001 global
registry and the separate 161-child q10 ledger are unchanged.

Prepared queue: 239 exact core guards per r, hence 956 pending jobs. Each
guard covers 1953--4095 original IDs. All IDs remain UNKNOWN. The guard tree
also partitions every assignment of the 55 variable core edges, so each
worker is a complete physical43 job, not a local residual search.

## Worker and certificate contract

1. Select a published cohort using `cohorts.py RUN --r R --leaf T`. Its output
   is a JSON job with `r`, `core_assumptions`, `edge_cube` (initially empty).
   Core literals are restricted to 802..856; physical branch literals to
   2..801. All 48 fixed block edges remain in the same full43 graph.
2. `worker.py materialize RUN JOB.json NEW.cnf` writes M_r plus the listed
   units, records its exact SHA-256 and refuses an existing output path.
   A solver or proof-producing decomposition must use that exact input.
3. `worker.py import-lrat RUN JOB.json PROOF.lrat OUT.json` normalizes
   positive-hint RUP LRAT, then checks its original and discharged proofs.
   It rejects unsupported RAT steps. It never launches or restarts a solver.
4. If a physical edge is split, both children retain the same core guard and
   preceding physical cube, ending respectively in +x and -x. Use
   `worker.py join RUN POSITIVE.json NEGATIVE.json OUT.json` to obtain a
   checked parent proof. An unresolved child leaves the parent unresolved.
5. Only a worker whose edge cube is empty can become a task cover:
   `worker.py cover RUN WORKER.json COVER.json`. The cover is checked against
   the audited base and the exact catalog stream. Its guard may match many
   original IDs; empty matches are explicitly reported as empty covers.
6. `task_queue.py request ID RUN --certificate COVER.json` returns
   CERTIFIED_UNSAT and suppresses dispatch only if the checked cover matches
   that ID. Otherwise the original task remains UNKNOWN. Certificate scope
   is qualified by r and the exact base hash; no cross-r reuse is implied.
7. `worker.py target RUN JOB.json MODEL.out OUT.json` requires a complete
   SAT assignment satisfying the exact base and all job units, reconstructs
   every physical edge and checks all 962598 five-sets. A partial-core worker
   may produce an unlisted core; a verified good43 still settles the target.

For a larger adaptive tree, retain unresolved jobs and their exact inputs.
The provided proof joins supply a finite complete path to a parent verdict;
they do not predict how many branches will be needed. Workers can share
clauses only when they have been established as consequences of the common
base, using the guarded proof mechanism. An unverified assumption core, a
local witness or a partial DRAT trace never changes a whole-task status.

## Concrete next verdict gate, outside this completed mechanism pass

The prepared r=5, leaf=0 job contains 2184 original task IDs and has eight
core assumptions. Its full input is 931 variables and 1488142 clauses,
SHA-256 `345f980b276beeb8a5abf7303ef4e080f03662ac1823f5bcf199c7aac74677a7`.
Its cohort guard is the eight negative literals
`810 819 824 832 833 836 842 856`.

A subsequent bounded computation using this mechanism should predeclare a
specific nonempty cohort or physical subtree, resource-accounted branching
policy and one measurable verdict gate. A checked complete cohort exclusion
would retire its full member set; a physical good43 is checked independently.
The mechanism does not justify another isolated capped monolithic solve.
No such target computation was begun in this pass.

The initial proof-plumbing controls used an impossible core K4 pattern and
matched zero original IDs. Their verified branch joins are control evidence,
not the verdict gate. The new bases have roughly 1.49--1.50 million clauses
each and can be harder than a fully conditioned task. Speed and positive
cohort exclusions remain unmeasured. Independent reviewer-1 review is pending.
