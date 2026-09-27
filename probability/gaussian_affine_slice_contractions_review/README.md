# Independent review: affine-slice prism contractions

This directory independently reviews Discovery Net artifact
`bafkreia4ivwxrdzlhqa6ywpddshfzqk5p6s2n7fzz67tqedsnnfk7uq6xa`.
The proof content is from commit `9c1feb8cf43d8726c7fddc540dd6a8b143749f47`;
the exact graph-cited publishing state is
`80d676cbbd5ccb0c7fa6f9303e05cf9e8251dfea`.

Use standard-library CPython 3.11+:

```sh
python3 -B independent_check.py
python3 -B -O independent_check.py
sha256sum -c SHA256SUMS
```

Both Python modes must report `INDEPENDENT_AFFINE_SLICE_ACCEPT`. The checker
imports no author module. See [REVIEW.md](REVIEW.md) for the verdict and the
boundary between exact controls, primary-source transfers, and the written
continuum/ODE argument.

