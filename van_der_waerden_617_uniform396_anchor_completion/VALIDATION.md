# Exact validation and measured resources

Actual author: **six-vdw-3**, role **researcher**. These are author checks.
Independent review of this extension is pending; neither completed
external review nor proof-assistant formalization is claimed.

The supplied verify.py imports no native numerical library or proposer.
It replays19 old root chains, nine new root packings and all four actual
seven-point anchors, using only the opposite class197 cap. Old rigidity
and stage-domain deductions are rechecked before reuse. It reconstructs
all617 references, pole pairing and class sizes. The earlier other-phase
profile is explicitly imported; its full proofs are not reexecuted here.

The complete frozen result is expected.json, SHA256
`142578449837532e9a154c00681287983a3a83c94c96a6938ea60c7c460f0e93`.
Frozen CPython3.11.2 checking and controls passed. A source-only
CPython3.12.14 run completed **15 serial jobs**: frozen replay and controls
in normal/optimized modes; regeneration of all nine new certificates;
fresh complete replay in both modes. Fresh normal and optimized results
are identical and have the frozen combined profile. Coefficient bytes
may differ, because any checked positive packing proves the same root
exclusion. The smallest new frozen gap is56434/1000000; the corresponding
fresh root19 gap is49371/1000000. The smallest terminal gap across all
frozen old/new roots is the inherited7490/1000000.

Both modes reject **49 corruptions**, including an extra opposite-class
cap, wrong cap/class/phase, noninteger values, poles, invalid geometry or
colours, duplicate/nonpositive weights, point overloads, missing essential
triples, triples with a one-point transversal, a zero rather than strict
gap, each missing new root, each missing phase, malformed complete
coverage, an omitted old chain and an unproved old domain restriction.
All substantive checks use exceptions and survive Python `-O`.

Separate small assignment enumerations check64 activation assignments,
512 anchor assignments across the four phases (508 nonempty subsets),
255 empty-intersection triple families,1529 weighted hitting models,
3337 defect models and32328 strict remaining-edit screen models. These
audit the written local rules; they do not enumerate length3704 words.

The full fresh run completed in46.9552 seconds, longest child11.3798s;
peak parent RSS16824KiB and maximum child RSS56500KiB. Pinned proposer
versions are highspy1.11.0/numpy2.2.6. Every actual native LP was limited
to15s, threads1 and parallel off. Each child had a30s external guard.
Triple selection was bounded at8s/2million candidates/20000 rows, with
at most four cut rounds. The existing1CPU/2GiB scope was unchanged;
there was at most one CPU-intensive job at any time.

The compact measured evidence is evidence.json. Generated guides,
journals, damaged copies, caches and private explorations are excluded.
Missing packages, unavailable guides, UNKNOWN, unchecked negative solver
statuses, timeout, memory kill and no witness found establish no
mathematical exclusion. No resource limit is escalated after failure.
