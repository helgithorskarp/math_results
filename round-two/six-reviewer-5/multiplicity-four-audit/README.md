# Multiplicity-four independent audit

Actual agent: **six-reviewer-5**, independent mathematical reviewer.

This bundle independently proves the conditional multiplicity-four exclusion in
71-word `(16,19,20^16)` packings. It validates six existing exact duals, closes
three shared-isolated-hub lemmas, corrects a faulty heavy-edge sentence by a
row-sum proof, and removes the final scalar enumeration. The zero-through-three
exclusion remains an explicit older premise of the multiplicity-five corollary.
Read [REVIEW.md](REVIEW.md) for hypotheses, reductions, attribution and trust.

From repository root, CPython 3.11.2+ standard library, sequentially:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-reviewer-5/multiplicity-four-audit/audit.py
python3 -B -O round-two/six-reviewer-5/multiplicity-four-audit/audit.py
python3 -B round-two/six-reviewer-5/multiplicity-four-audit/local_pair.py
python3 -B -O round-two/six-reviewer-5/multiplicity-four-audit/local_pair.py
```

The first checker reconstructs all 388 raw marks of the already reviewed
nineteen-star census, both original 62/40 inventory streams and the new six-case
screen, all six duals with 1,219 columns each, and 49 isolated-hub pair carriers.
Its stable exact record SHA256 is
`b841641fe298f00ae24f9759de6b3972416063dabab058af67e0edf3b4b65e0e`.
The isolated pair carrier excludes all 3,048,192 full maps, with 129,759 visited
prefixes and maximum 3,135 per case. It also accepts two known positive controls,
including a degree-19 multiplicity-four pair. The complete carrier proof uses
weighted collision prefixes, never missing branches or author automorphisms.

The second checker cold-replays this reviewer's earlier **standalone local**
component: 448 raw cases, 6,967,296 full maps, 413,196 visited prefixes, maximum
1,611 per case. Its unchanged exact stream SHA256 is
`c2fa107a505b44e21f83e99415a4dde3af4d3061b1e735554eb4e4250b619dbb`.
Only a fixed digest of its redundant case summary is retained here; all actual
proof checks execute, and the full earlier summary remains in its original
published contribution. No whole-result implication from that earlier review
is imported.

Inputs are credited in INPUTS.json. The census is a mathematical premise, not
reproved here. Dual columns are evaluated by subset aggregation, independently
of the author's dense row construction. No author modules or solvers execute.
EXPECTED.json contains compact case summaries and the full tiny inventory
streams; VALIDATION.json records measured runs. Generated full maps remain
private. Thirteen malformed-dual controls, two positive carriers and explicit
fixed-limit guard controls are included. No raised resource setting is needed.
