# Reproduce the independent third-boundary/equality-cap audit

Actual six-reviewer-4 / independent mathematical reviewer. Standard-library
Python3.11+ only; discovery execution Python3.11.2. Ordinary uniform analytic
bridges are unformalized; see PROOF.md and REVIEW.md for relative premises.
No native author module or external proof corpus is needed.

Run from this contribution directory:

```bash
python3 -I -B verify.py
python3 -I -B -O verify.py
python3 -I -B verify.py --record
```

The entire canonical record is58074 bytes, SHA256
3b415a4aae8189df9f8322c1fbacba153a4278778b8871726ea0b7c34d153523.
It contains all ten formal parameters/all ten polynomial columns, the
complete normalization/scalar/radial offsets, both entire literal
primitives, both all-nine root and radial jets through fourth order,
both complete FIRST-power objectives, and the full transverse polynomial
cost. MANIFEST.json seals all eight primary files before import.

Optional serial controls (one bounded phase at a time):

```bash
python3 -I -B controls.py --phase positive
python3 -I -B controls.py --phase early
python3 -I -B controls.py --phase late_a
python3 -I -B controls.py --phase late_b
python3 -I -B controls.py --phase fixtures
```

Repeat with --optimized to exercise -O. Each control child has its
initial30s guard; campaign phase wrappers use45s guards. Controls set all
six numerical thread variables to1 and start one mathematical child
at a time. Generated temporary data defaults to this directory's ignored
scratch directory; AUDIT_SCRATCH may select another writable scratch path.
Controls include EMPTY source-only reconstruction, ten semantic wrong
mathematical variants, whole typed-fixture damages and source-byte damage.
No timeout/UNKNOWN is an accepted mathematical control or absence proof.

PROOF.md proves the target's full new relative leaf and two refinements:
an explicit strictly feasible equality-cap family and quantitative
near-third-optimum rigidity. It does not prove a global first-power
endpoint, a sharp fourth infimum coefficient or an effective collar.
