# Protected-contact audit

Actual agent **six-reviewer-1**, independent mathematical reviewer.
Read [REVIEW.md](REVIEW.md) for the confirmed scope, all-motion bridges,
independent 8134 prerequisite check and proved rational-grid refinement:
positive-area skeleton overlap forces physical overlap for common translation
denominators \(1\le d\le 88\), using a boundary distance \(1/(18d)\).

From the repository root, with Python 3.11.2 (standard library only):

~~~sh
python 3 -B heesch_protected_contact_review 1/check.py --expected heesch_protected_contact_review 1/expected.json
python 3 -B -O heesch_protected_contact_review 1/check.py --expected heesch_protected_contact_review 1/expected.json
~~~

The commands have identical output; all checks use explicit exceptions.
No solver, campaign executable or original certificate is imported.
The checker derives all-width affine inequalities rather than extrapolating
from sample widths. Its 720-pair intersection regression is separately scoped.
The analytic and topological argument is written, not formally verified.
The original target and prerequisite arithmetic replays are secondary checks;
[provenance.json](provenance.json) identifies their public pinned inputs.

All calculations use one CPU with no native numerical library. Normal and
optimized independent runs each take under two seconds in the reviewed
environment. No generated large corpus or private operational state is included.
The finite-seven target remains unresolved.
