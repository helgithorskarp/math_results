# The automorphism-group order is not divisible by 27

For a hypothetical Ramsey `(5,5;43)` graph, every `C_3 x C_3` subgroup
must act with **one fixed vertex, two orbits of size three and four orbits
of size nine**. Two stabilizer patterns remain open. This is proved by
classifying all 18 actions allowed by the minimum-eleven motion theorem
and certifying 16 exclusions.

The unique fixed point then gives a short group-theoretic contradiction
for any subgroup of order 27. Thus `27` does not divide the automorphism-group
order. Combined with the earlier prime-divisor restrictions, it has form
`2^a 3^b`, **b<=2**. The two open C3-square types each have an order-three
element moving fourteen triangles, so the M=214 branch's upper bound of
twelve excludes them there: **b<=1 in M=214 only**.

Read the full action-cover and group proofs in [PROOF.md](PROOF.md).
No 43-vertex target graph or Ramsey lower-bound improvement is claimed.
No global exclusion of C3-square subgroups is claimed. The teammate's
non-symmetric counts remain 66 profiles / 271 anchored splits.

## Exact finite checkpoint

The action parameters are a global fixed vertices, four sorted
three-orbit multiplicities b, and c regular nine-orbits. The four entries
of b refer to the kernels of x,y,x+y,x+2y, in that order. The full formulas
have only primary edge-orbit variables, all five-set Ramsey clauses and
one complement-normalization unit. They impose no degree profile or
additional graph automorphism.

| case | a | b | c | variables | clauses | status |
|---:|---:|---|---:|---:|---:|---|
| 0 | 1 | 2,3,3,3 | 1 | 135 | 166593 | verified UNSAT |
| 1 | 1 | 0,2,3,3 | 2 | 125 | 197985 | verified UNSAT |
| 2 | 1 | 1,1,3,3 | 2 | 123 | 196805 | verified UNSAT |
| 3 | 1 | 1,2,2,3 | 2 | 121 | 195721 | verified UNSAT |
| 4 | 1 | 2,2,2,2 | 2 | 119 | 194725 | verified UNSAT |
| 5 | 1 | 0,0,2,3 | 3 | 115 | 206775 | verified UNSAT |
| 6 | 1 | 0,1,1,3 | 3 | 113 | 206175 | verified UNSAT |
| 7 | 1 | 0,1,2,2 | 3 | 111 | 205695 | verified UNSAT |
| 8 | 1 | 1,1,1,2 | 3 | 109 | 205199 | verified UNSAT |
| 9 | 1 | 0,0,0,2 | 4 | 105 | 211323 | UNKNOWN (60 s) |
| 10 | 1 | 0,0,1,1 | 4 | 103 | 210907 | UNKNOWN (60 s) |
| 11 | 4 | 1,2,2,2 | 2 | 135 | 197359 | verified UNSAT |
| 12 | 4 | 0,0,2,2 | 3 | 123 | 206971 | verified UNSAT |
| 13 | 4 | 0,1,1,2 | 3 | 121 | 206331 | verified UNSAT |
| 14 | 4 | 1,1,1,1 | 3 | 119 | 205755 | verified UNSAT |
| 15 | 4 | 0,0,0,1 | 4 | 109 | 210785 | verified UNSAT |
| 16 | 7 | 0,1,1,1 | 3 | 135 | 207109 | verified UNSAT |
| 17 | 7 | 0,0,0,0 | 4 | 119 | 210733 | verified UNSAT |

The complete action audit covers 117 ordered multiplicity patterns,
48 invertible matrices and all 24 projective permutations. See
[classification.json](classification.json). The two open types have equal
or distinct stabilizers for their three-orbits, respectively. UNKNOWN is
a timeout status, not a graph realization or a proof of feasibility.

The 18-case run used two workers, 60-second solver limits and 180-second
proof-replay limits, completing in 239.339 seconds. Largest child peak RSS
was 172,776 KiB. All sixteen UNSAT traces passed drat-trim; only cases9,10
reached their search limit. The full run and source/tool hashes are in
[sweep_result.json](sweep_result.json).

The sixteen original binary proofs total 52,949,854 bytes. Extracted cores
and general DRAT proofs total 62,281,845 bytes; these text-format extractions
are not uniformly smaller than the original binary traces. Every one of
166,699 core-clause occurrences was checked against its own complete
formula. Fresh generation, independent full-clause reconstruction and
sixteen further proof replays completed in 130.571 seconds.
[certificate_manifest.json](certificate_manifest.json) records every
core/proof hash; [verification_result.json](verification_result.json)
records the replay and support outcomes. These large generated files and
logs are kept outside Git. Public hashes and reports alone are not
standalone certificates; regeneration is required for independent replay.

## Reproduction

Use Python3.11.2 standard library, GCC12.2.0, Kissat4.0.4 source
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and drat-trim source
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Set KISSAT and DRAT_TRIM
to the corresponding executables. From this directory:

```bash
python3 model.py --report /tmp/c3-square-classification.json
cmp classification.json /tmp/c3-square-classification.json
python3 run.py --work /tmp/c3-square/full --kissat "$KISSAT" \
  --drat-trim "$DRAT_TRIM" --workers 2 --solve-seconds 60 --replay-seconds 180
python3 controls.py --work /tmp/c3-square/controls \
  --cnf /tmp/c3-square/full/case_00.cnf --checker /tmp/c3-square/full/check_formula \
  --report /tmp/c3-square/controls.json
cmp controls_result.json /tmp/c3-square/controls.json
python3 certificates.py extract --sweep /tmp/c3-square/full \
  --output /tmp/c3-square/compact --drat-trim "$DRAT_TRIM" --workers 2
python3 certificates.py verify --work /tmp/c3-square/verification \
  --certificates /tmp/c3-square/compact/certificates \
  --manifest /tmp/c3-square/compact/manifest.json --drat-trim "$DRAT_TRIM"
python3 support_control.py --work /tmp/c3-square/controls \
  --full /tmp/c3-square/full/case_00.cnf \
  --core /tmp/c3-square/compact/certificates/case_00.cnf \
  --report /tmp/c3-square/support.json
cmp support_control_result.json /tmp/c3-square/support.json
sha256sum -c SHA256SUMS
```

Expected exclusions are 0..8 and 11..17, with 9,10 open. Each formula's
canonical hash is deterministic; time-limited solver status and trace bytes
may depend on the host. A new UNKNOWN result contributes no exclusion.
Use a fresh directory with an adequate limit if needed. `--resume` requires
an identical saved contract and rechecks completed exclusions; an existing
OPEN checkpoint is retained. A STOP file prevents starting new cases;
active cases finish their bounded work. Case and summary checkpoints are
written atomically. A SAT result must decode to a literal edge list and
pass every five-set check before the runner reports a target.

[controls.py](controls.py) compares all 128 edge-orbit assignments on a
seven-vertex invariant subgraph against direct five-set tests and the
literal edge-list verifier. Exactly116 are Ramsey and58 satisfy the
complement normalization. It also checks that the complete C++ checker
rejects wrong clause polarity, a missing clause and a wrong header.
Ordinary and optimized Python reports agree. [support_control.py](support_control.py)
adds a well-formed but unsupported empty core axiom; the support checker
rejects it. Cases0,10,11,17 also pass full C++ reconstruction under ASan
and UBSan; commands and outputs are in [sanitizers_result.json](sanitizers_result.json).

## Dependencies and handoff

This action cover imports the minimum-eleven motion result in
[the final ten-cycle artifact](../ramsey_r55_order3_ten_cycle_signature_propagation).
That new closure still awaits independent review. Its older internal-color
split now has an [accepted independent review](../ramsey_r55_order3_ten_cycle_obstruction_review1),
resolving the previously inherited review gap. The separate
[order-nine element theorem](../ramsey_r55_order9_automorphism_obstruction)
and [M=214 upper bound](../ramsey_r55_m214_symmetry_audit) are also reviewed.
The new group-action cover, formulas and certificates have internal checking,
not an independent peer review or formalization. The unformalized arguments,
source, exact runtimes/compiler, hardware, SHA256 and drat-trim remain
explicit trust boundaries.

This completes one C3-square classification milestone and its direct group
corollaries. The two global open formulas are preserved for a later pass.
Their natural next refinement is a justified centralizer normalization of
the four regular F3² orbits and the quotient orbits. Independent changes of
basis on separate regular copies must not be assumed to commute with H.
No further search or separate order-27 computation is launched here.
