# Independent Book Ramsey degree-eleven audit

Reviewer: **six-reviewer-5**, independent mathematical reviewer.

The [review](REVIEW.md) confirms the universal degree-eleven neighborhood
histogram `(0,0,1,10)` and all148 forbidden induced12-vertex leaf cores.
The Ramsey number remains in the located22..23 interval. The review also
proves a direct four-case scalar reduction and necessary localized cuts
for the surviving histogram. Ordinary proofs establish the universal
exclusions; complete exact enumeration classifies the local cores.

Run from the repository root with CPython3.11.2+, standard library only,
one job at a time:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_degree11_review5/audit.py > /tmp/book-review5.json
diff -u book_ramsey_degree11_review5/expected.json /tmp/book-review5.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O book_ramsey_degree11_review5/audit.py > /tmp/book-review5-O.json
diff -u /tmp/book-review5.json /tmp/book-review5-O.json
```

Expected:133105 normalized labeled graphs,148 orbits,9768 local spine
checks;457 residual,25135 mixed-spine and5027 row-identity controls.
A fresh adaptive vertex sweep and a nonenumerating degree-class recurrence
agree. No researcher executable, manifest or graph corpus is imported.
All148 representatives are independently regenerated in [expected.json](expected.json).
No full22-host enumeration or proof-assistant result is claimed.

Complete summary SHA256:
`bc3a8801c2ba57f1cff2ad9cb0082b0f920af81e1c549b8fc9b7a9f9855d7f66`.
Domain sorted-decimal-mask stream SHA256:
`d2acc97a6865cfb95f6800ee07ddad815f426799f85a7265365ad11dbeb0ec85`.

The small [primary21 matrix](primary21.txt) is the known public construction
by the authors of arXiv:2407.07285, with source URL and hash recorded in
[provenance](provenance.json). Its metadata is never executed.
Generated graph corpora and private operational logs are omitted.
Trust boundaries and candidate-specific primary literature are in the review.
