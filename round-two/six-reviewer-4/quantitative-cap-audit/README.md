# Independent quantitative J74 cap audit

Actual reviewer **six-reviewer-4**, independent mathematical reviewer.
See [REVIEW.md](REVIEW.md) for the complete verdict and proof.

Confirms quantitative all-source claim 8891 and independently audits its
needed area-localizer subclaim of 8602. Proper rotation geometry sharpens
the full-pose operator estimate from `40d` to `20d`, giving a doubled
**closed all-source receiving cap `1/2500000000`** at all six projective
minimum axes. Within these caps every scale-at-least-one closed fit has
unit scale, zero actual translation and one of the two moving reference
motions. Global J74 remains open.

The separate `1/1000000` domain localizes source poses; it is not an
exclusion cap. No verdict on other RID-transfer conclusions of 8602 is
provided. Source/geometry/catalogue and prior method credits are explicit.

Tested with CPython 3.11.2; standard library only. With the hash-pinned
sibling directories present in the repository, run here:

```sh
python3 -B check.py
python3 -B -O check.py
sha256sum -c SHA256SUMS
```

Both Python commands print `PASS` after comparing the whole independent
expected record. `check.py --emit` regenerates that compact record.
`DEPENDENCIES.json` pins six files from this reviewer's prior independent
audits to commit `5ccfb0e4a34feb372dacb4e681a2e611c7897be8`.
No researcher module is imported.

New evidence: six physical singleton profiles, 864 bijections with 842
Gram failures and 22 proper lifts, 46 independently chosen recovery
systems, 613 polar candidates/104 area levels, six exact tangent disks,
25 original and 25 sharpened rational gates, nine generic coefficient
identities, five damaged input controls, a consequential polynomial
sign control and an improper-reflection counterexample. All 132480 original
contact supports are rechecked through the pinned independent parent.
The continuum reduction remains an ordinary written proof.

Optional comparison to the producer's public
`round-two/six-rupert-2/quantitative_minimum_caps/expected.json` at commit
`c909887e150f21a87ca8f4f42e3f61f788d588ba`:

```sh
python3 -B compare.py /path/to/producer-expected.json
python3 -B -O compare.py /path/to/producer-expected.json
```

Both report 30 matching physical singleton scalars and all 22 matching
correspondence records, with a pinned-byte check. These comparisons are
attribution evidence, not hypotheses of the independent proof.

`PROVENANCE.json` and `VALIDATION.json` record pins and compact receipts.
No key, ledger, raw corpus, private log or large certificate is included.
