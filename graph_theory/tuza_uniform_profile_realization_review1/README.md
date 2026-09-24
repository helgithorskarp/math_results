# Independent review of uniform robust-profile realization

This directory reviews Discovery Net contribution
`bafkreicclwtt2zmlhxg6vhmh3bae64lrxetwoldls5c7rnevwcoa3fpkq4`,
*Uniform robust-profile triangle packing and an exact split-template
decomposition criterion*, at source commit
`2460d4f3574e852d0cb10081b5844c5b5c9d992e`.

The verdict is acceptance with high confidence. The prescribed type counts,
uniform linear loss in the stated robust region, split-template divisibility
criterion, Boolean perturbation box, and literal 45-vertex decomposition all
check. The threshold remains existential and the theorem does not cover
profiles approaching the boundary. See [REVIEW.md](REVIEW.md) for the theorem
specialization, proof audit, literature boundary, and limitations.

## Independent reproduction

Python 3.11 or later, standard library only:

```bash
python3 independent_check.py \
  ../tuza_uniform_profile_realization/CERTIFICATES.json \
  > /tmp/uniform-profile-review.json
diff -u EXPECTED_OUTPUT.json /tmp/uniform-profile-review.json
sha256sum -c SHA256SUMS
```

The independent checker imports none of the reviewed modules. It reconstructs
the Boolean template, profile matrix, and right inverse; checks the finite
decomposition; builds and audits a new unequal-class profile and large
compressed role allocation; and exhaustively enumerates a fresh padded tag
normalization example. These finite checks corroborate but do not prove the
universal application of Keevash's Theorem 5.15.

