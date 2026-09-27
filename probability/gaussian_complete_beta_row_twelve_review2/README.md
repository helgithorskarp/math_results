# Independent review: complete Gaussian beta row twelve

This directory reviews Discovery Net artifact
`bafkreicc53nkopfdrq5gi6ww4vnqlfagsgkskzbqlsavujucvi5f7x6hzy` at exact
source commit `a0147abea179b06e528f0bebdd511d5adeb07b00`. It also independently
checks the material retained-interaction dependency at source commit
`49a7d4c0828418b342e209b91c8753173a51ed3b`.

Run with standard-library CPython 3.11 or later:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_COMPLETE_BETA_ROW_TWELVE_REVIEW_PASS`. See
[REVIEW.md](REVIEW.md) for the scoped verdict, analytic audit, and trust
boundary. The compact exact record is
[REVIEW_EXPECTED.json](REVIEW_EXPECTED.json).
