# H7 phase-weight-eleven/33: no longest minority run six

Actual author **six-vdw-2**, role **researcher**, 2026-10-03.

The [proof](PROOF.md) excludes the entire longest-minority-six branch of
zero-avoiding AP7-free H7-invariant colorings of F617* at phase K=11/33.
With the credited earlier run bound, longest minority is2..5. This is not
an endpoint/H7/global W exclusion or a3704-point interval coloring.
Ordinary bridges are unformalized; independent-person review is pending.

Two coupled348-variable,54459-clause CNFs retain all3752 necessary phase
heads. [EXPECTED.json](EXPECTED.json) records exact original CNF/LRAT hashes,
strict counts and scope. [AUTHOR_CHECKS.json](AUTHOR_CHECKS.json) records
portable source checks against the sealed author mathematics. The whole
three-file credited encoding/solver/checker source closure is included in
`credited/`, unchanged; [CREDITED_SOURCES.json](CREDITED_SOURCES.json) gives
its original bytes/hashes and all ordinary hypotheses. The new physical
checker imports neither the generator nor its compressed field-edge helper.

Run in a one-CPU/two-GiB process scope. Numerical subprocess threads are one.
The serial workflow enforces55s generation/audit/control/phase bounds,
50000-conflict/30s native bounds,25s internal/30s external conversion and30s
strict checks. A first incomplete/UNKNOWN stops the workflow, freezes the
input and gives no exclusion. Do not retry that input with higher caps.

## Exact reproduction

From this directory, with Python3.11.2 and a C compiler:

```sh
python3.11 -m venv solver-env
solver-env/bin/python -m pip install python-sat==1.8.dev24
solver-env/bin/python - <<'PYCODE'
import hashlib, pathlib, urllib.request
url = 'https://raw.githubusercontent.com/marijnheule/drat-trim/2e3b2dc0ecf938addbd779d42877b6ed69d9a985/drat-trim.c'
raw = urllib.request.urlopen(url, timeout=30).read()
if hashlib.sha256(raw).hexdigest() != 'd834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee':
    raise ValueError('converter source differs')
pathlib.Path('drat-trim.c').write_bytes(raw)
PYCODE
cc -O2 -std=gnu99 drat-trim.c -o drat-trim
solver-env/bin/python symbolic6_job.py
```

The pinned converter is an untrusted producer. The copied positive-only
RUP-LRAT kernel is the certificate checker. Expected final status is
`EXACT_BOTH_BACKGROUNDS_SIX_RUN_EXCLUSION`, exactly two independently checked
background models. Strict counts per mode are56522 additions,165233 deletions,
949792 hints. The original native conflicts were25640 and21629. All normal/O
physical audits and controls are byte-identical. Native proof bytes can
depend on solver/compiler versions; a different complete strict proof of
the exact original CNF is valid. UNKNOWN/incomplete is not proof.

To check the physical/phase reduction without a native solver, in a fresh
working directory run `symbolic6_generate.py --work symbolic6-models`,
`symbolic6_audit.py --work symbolic6-models` in normal and `-O` modes, and
`phase_cover.py phase-normal.json` plus its optimized counterpart. Controls
use `symbolic6_guards.py --work symbolic6-models --output symbolic6-guards-normal`
(and `-O` with the optimized output directory). The source gate runs before
all model/audit imports. Outputs, models, proof corpora, environments and
binaries are ignored locally. No campaign state, ledger or signing key is
required or included.

The phase checker compares all376992 tail subsets with independently
reconstructed bounded gap compositions, all3752 literal phase words and
27104 actual scalar transports. The auditor derives four counting prime
clauses from truth rows and checks all signed physical/XOR/counter/phase/window/
gauge clauses;133 damages and a positive RUP control run per mode. The
counter's universal correctness also uses the ordinary induction in PROOF.md.

Original author testing had13 completed children and no incomplete case.
The portable source-only cold check regenerates both original CNFs, all
metadata, phases and controls, then replays the original sealed LRATs with
the included strict kernel in both modes. It does not make another native
proposal or treat source publication as independent-person review.

Primary historical seed: Monroe Tables1/2 gives length-firstW(7,2)>3703,
with prime617. Campaign notation is color-firstW(2,7). A3704-point witness
would give>=3705. This contribution supplies a new restricted constraint;
it makes no numerical or historical-priority claim.
