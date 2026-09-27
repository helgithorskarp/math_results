# Independent review: meridian contractions

This directory reviews Discovery Net artifact
`bafkreiabngjrclqthd36unxe7cjzyqw3uhmgbr5it62si6yjca6l6dnqf4` at exact
source commit `a1013f169d8dd6d32ae76cf9817a47dccd3f100f`.

Run with standard-library CPython 3.11 or later:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_MERIDIAN_CONTRACTION_REVIEW_PASS`. See
[REVIEW.md](REVIEW.md) for the verdict, primary-source audit, and trust
boundary. The compact record is [REVIEW_EXPECTED.json](REVIEW_EXPECTED.json).
