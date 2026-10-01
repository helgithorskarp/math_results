# Independent leaf-neighbor audit

Actual agent six-reviewer-2, independent mathematical reviewer.
Read [REVIEW.md](REVIEW.md) for the complete verdict, inherited premises and
proved refinements of the conditional Book Ramsey lemma 9071.

Python 3.11.2 or compatible standard library; no packages or author modules.
Set solver/BLAS/OpenMP variables to one. Run serially:

```bash
python3 audit.py --check-file EXPECTED.json
python3 -O audit.py --check-file EXPECTED.json
python3 audit.py --self-test
python3 -O audit.py --self-test
```

The frozen record contains all twelve labelled row patterns, physical
contradiction/control counts and all sixteen relaxed low-type margin profiles.
EXPECTED is newly generated, not a pre-existing independent fixture.
VALIDATION records guarded measured jobs and separate author replays.
No relaxed profile is asserted to occur in a valid host; no Ramsey endpoint
or whole 108-edge exclusion is claimed.
