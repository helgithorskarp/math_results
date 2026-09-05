# Ten moving 3-cycles force one twelve-vertex minority core

In a hypothetical Ramsey `(5,5;43)` graph with an order-three
automorphism of type `1^13 3^10`, the four minority-color moving triangles
must induce the explicit graph in [minority_core.edges](minority_core.edges).
It is 7-regular in their internal color, and its complement is
triangle-free. A fixed vertex can be adjacent in that color to at most
two of the four whole triangles.

The proof refines the previous
[minority matching](../ramsey_r55_order3_ten_cycle_anchor_sweep): 27
normalized phase patterns form six classes, and **20 checked exclusions
eliminate all five nonzero phase classes**, across all four anchor
profiles. The single phase `(0,0,0)` remains. Its four full-extension
formulas timed out and remain **open**. No target graph, exclusion of
the ten-cycle type, or improved Ramsey bound is claimed.

Read [PROOF.md](PROOF.md) for the complete normalization, encoding,
certificate and dependency arguments. The twelve-vertex edge list is
a forced-core fixture, not a 43-vertex candidate.

## Reproduce the proof without a SAT solver

Use Python 3.11.2, GCC 12.2.0 and drat-trim. From this directory:

```bash
python3 audit.py --output /tmp/r55_phase_audit.json
cmp audit_result.json /tmp/r55_phase_audit.json
python3 certificates.py verify --work /tmp/r55_phase_verify \
  --certificates certificates --manifest certificate_manifest.json \
  --drat-trim /path/to/drat-trim
python3 controls.py --base /tmp/r55_phase_verify/base.cnf \
  --work /tmp/r55_phase_controls --output /tmp/r55_phase_controls.json
cmp controls_result.json /tmp/r55_phase_controls.json
python3 inspect_core.py > /tmp/r55_phase_core.json
cmp core_result.json /tmp/r55_phase_core.json
sha256sum -c SHA256SUMS
```

The expected proof output verifies indices 4 through 23, checks 4,992
core-clause occurrences / 992 distinct parent obligations, and reports
indices 0,1,2,3 open. [verification_result.json](verification_result.json)
records the reference replay, which took 31.134 seconds. Elapsed time
is machine-dependent. `audit.py` reports six phase classes, 24 cases,
432 literal core relabelings and 688 local truth assignments per tail.
`controls.py` additionally checks 96 whole-graph normalizations and six
adversarial conditions. Checks remain active with `python3 -O`.

The [forty published certificate files](certificates) total 310,309 bytes;
the largest is 25,354 bytes. The verifier rebuilds the full parent CNF
outside Git, checks every used core clause against that parent or its
own independently audited extension clauses, and replays general DRAT.
Case 20 has three RAT core lemmas. No SAT solver is needed to replay
these twenty new certificates. Earlier mathematical dependencies retain
their own certificate/reproduction boundaries.

The parent directory must remain beside this one in the repository.
[dependencies.json](dependencies.json) pins the required parent sources
and the preceding matching theorem, surviving profiles and graph checker.
The parent formula includes all five-sets and all thirteen fixed-vertex
degree counters; no weaker pilot formula is used.

## Reproduce the bounded search

The reference tools were Kissat 4.0.4, source commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and drat-trim, source commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Tool-binary hashes and Python
version are recorded in [sweep_result.json](sweep_result.json).

```bash
python3 run.py --work /tmp/r55_phase_sweep \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
python3 certificates.py extract --sweep /tmp/r55_phase_sweep \
  --output /tmp/r55_phase_extracted --drat-trim /path/to/drat-trim
```

The default is two workers, 30 seconds per SAT case and 120 seconds
per proof check. A case is marked excluded only after successful DRAT
replay. A SAT result must decode to a compact edge list and pass the
literal all-five-sets graph verifier. Timeouts are explicitly open.
The reference bounded sweep took 155.037 seconds, with largest-child
peak RSS 495,708 KiB. Its twenty original excluded traces totaled
214,430,938 bytes and are omitted, along with full CNFs, incomplete
traces, binaries and logs. Fresh bounded runs can have different timeout
outcomes; the published certificates give the durable twenty exclusions.

Each completed case and the cumulative result are written atomically.
Creating `WORK/STOP` prevents new cases from starting after active
cases and proof checks finish. `--resume` requires unchanged source,
tools, worker count and limits; it replays cached exclusions and retains
the recorded open outcomes. A changed formula or budget requires a new
work directory. This makes the 24-case unit stoppable without treating
unfinished work as a completed proof.

The exploratory matching-only four-case run left every case open at
30 seconds. A small extension pilot found each core class admits a
single majority triangle. Those pilots motivated the full phase split;
their outputs are not theorem evidence and are not needed for verification.

## Scope and next checkpoint

There is no M=214 or selected-exceptional-core assumption. The result
applies to every hypothetical 43-vertex target with this exact cycle
type. Other moving-cycle counts are not decided. The matching refinement
now has an [accepted independent review](../ramsey_r55_order3_ten_cycle_anchor_sweep_review1),
explicitly conditional on the older internal-color split. That split and
this new phase refinement have no recorded independent peer review;
internal cross-checking is not such a review.

The next frontier consists of the four extensions of the forced core,
with anchor profiles 64,65,67,69 and mixed weight-one counts 4,3,2,1.
The preserved source can regenerate those exact formulas. Exploit the
fixed core's extension constraints before a larger solver budget or
another symmetry stratum. This pass finishes and yields at the completed
phase classification and certification milestone.
