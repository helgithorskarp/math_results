# q8,r8: a certified negative branch and a constrained physical queue

The entire h4149 q8,r8 formula forces physical edge **{3,4}=red**, variable
119. A 240-step checked normalization derivation and the published bound
R(4,5)<=25 exclude its complementary physical branch for every core.
See [PROOF.md](PROOF.md) for the proof and external-premise boundary.

The complete routing run certified 239 negative cohort branches, refused
their materialization, and materialized and byte-checked all 239 positive
full43 inputs. It transported all 546,356 original q8,r8 task identities
with the forced edge, while leaving the other 717 q8 cohorts unchanged.

**Original-task outcome: UNKNOWN.** Zero original tasks were newly
excluded, zero candidates were found, and no target solver ran. The
positive siblings are still undecided. This is an operational consequence
of a proved branch exclusion; it does not meet the principal's requested
original-task or good43 verdict gate. Independent reviewer-1 review is
pending. All parked routes and the q10 queue remain untouched.

## Reproduction

Use Python 3.11 standard libraries, from the repository root. The sibling
directory `ramsey_r55_q8_assumption_queue` must match the source manifest
pinned in DEPENDENCIES.json. The full parent source and input audits are
documented in its README. If its verified run directory is already
available, use it directly. Otherwise generate it in fresh scratch paths:

```sh
python3 -O -B ramsey_r55_q8_assumption_queue/reproduce.py \
  /tmp/r55-q8-catalog /tmp/r55-q8-parent --download --sanitizers
python3 -O -B ramsey_r55_q8_root_unit/reproduce.py \
  /tmp/r55-q8-parent /tmp/r55-q8-unit
```

The second command generates and checks the theorem certificate, tests
malformed proofs and scopes, executes all 239 full materializations,
independently audits the resulting queue, and tests original-ID requests.
Existing output directories are refused. Its queue stage took 250.4792
seconds and 450,896 KiB peak RSS in the recorded run. It wrote and checked
16,345,885,302 bytes of transient worker inputs, retaining only the first
and last CNFs. This I/O is validation work, not measured search savings.

The preserved compact certificate can also be checked alone:

```sh
python3 -O -B ramsey_r55_q8_root_unit/bridge.py verify \
  /tmp/r55-q8-parent ramsey_r55_q8_root_unit/branch-certificate.json
python3 -O -B ramsey_r55_q8_root_unit/independent_check.py \
  /tmp/r55-q8-parent ramsey_r55_q8_root_unit/branch-certificate.json
```

After full reproduction, an original task is consumed by the active stream:

```sh
python3 -O -B ramsey_r55_q8_root_unit/bridge.py request \
  /tmp/r55-q8-parent ramsey_r55_q8_root_unit/branch-certificate.json \
  --stream /tmp/r55-q8-unit/run/q8r8-dispatch.records \
  --task bo1-q8-r8-c000000
```

The result remains UNKNOWN and returns an h4149-compatible worker job
with all 55 original core assumptions and physical `edge_cube: [119]`.
Use the parent `worker.py materialize` and `worker.py target` interfaces
for its full formula and any future candidate. No q7/q9/q10 task is
admitted by this stream. No proof of a positive sibling was produced here.

QUEUE_RESULT.json contains the actual 239 input hashes and timings.
VALIDATION.json distinguishes the full routing run from the later small
request/serialization checks; the one-command wrapper was assembled from
those exercised components rather than rerunning the 16 GB I/O stage.
CNFs, full streams, external paper bytes, and the immutable checkpoint
remain outside Git. Source and the compact certificate are public.
