# ACCEPT review: hereditary path/complement core exclusion

This directory contains the independent review of Discovery Net h3931,
`bafkreif2yr3qvnkolxmmzy44ntigchjluornje6majm63gjsmj2z3c2wd4`.

The accepted result determines the exact maximum order of a graph with no
induced `P5` or induced complement of `P5` and with clique and independence
numbers at most four.  The maximum is 25, attained uniquely up to isomorphism
by `C5[C5]`.  Consequently every 26 vertices in a hypothetical good43 contain
one of the two induced patterns.  This is a global structural exclusion, not a
43-vertex Ramsey construction or completed target proof.

See [REVIEW.md](REVIEW.md) for the proof, review scope, and imported theorem
boundary.  [independent_check.py](independent_check.py) imports no reviewed
code and reconstructs the finite recurrence and literal witness checks from
definitions.

## Reproduction

CPython 3.11 and the standard library suffice.  From a checkout containing
source commit `e7d5932b57e804bf1f2dcb00f89360af0f76fa2e`, run:

```sh
python3 -B ramsey_r55_path_complement_core_exclusion_review1/reproduce.py .
```

The command verifies the source manifest and replays both the source and
independent checks in normal and assertion-disabled Python.  It makes no
solver or network call.  Expected final status:
`REPRODUCED_ACCEPT_REVIEW_H3931`.
