# Independent review: rational central-ellipse lonely vectors

This directory independently audits the contribution
`discrete_geometry/elliptic_lonely_vectors` at source commit
`36e684aef5b66d4a67ab058eb9987df70ec31cc5`.

## Verdict

**Accept, high confidence, with scope caveats.**  The proof establishes the
stated all-cardinality result for rational, nonzero, pairwise non-equal/non-opposite
plane vectors on one origin-centered ellipse.  It does not establish the general
rational Lonely Vector Property, which is false, or a new Lonely Runner theorem.
The novelty assessment remains search-relative.

The detailed premise and completeness audit is in [REVIEW.md](REVIEW.md).

## Reproduction

Python 3.8 or later is sufficient; there are no third-party dependencies.

```bash
python3 audit.py
python3 audit.py | diff -u EXPECTED.json -
sha256sum -c SHA256SUMS
```

The independent checker does not import or call the submitted checker.  It:

- exhausts all 33,791 configurations of at least two antipodal classes in a
  five-fiber window of the realizable groups `Z x C_w`, for `w=2,4,6`;
- checks the extremal-fiber isolation step on labelled entries, including the
  saturated `C_6/{+/-1}` obstruction with no lonely original;
- verifies 102 direction/product identities on rational conics after nontrivial
  rational coordinate changes;
- constructs Gale duals independently and verifies 105 lonely-label reductions;
- rejects the wrong merge sign in all 85 tested lonely pair reductions; and
- verifies the exceptional `3m`-point family for `m=1,2,3`, including failure of
  every deletion and success of the lonely pair reductions.

The computation is corroboration, not the proof of the unbounded theorem.  The
proof verdict rests on the human audit in `REVIEW.md`.
