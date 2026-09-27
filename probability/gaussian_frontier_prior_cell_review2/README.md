# Independent review: full-prior Gaussian frontier cell

This directory independently reviews the claim at target commit
`c1b17b8459a0221279becd8f6da20a9b269ba54a` and Discovery Net contribution
`bafkreidsn7klheuvguoiqbidjjinu4xj56lltx6cjybhly7oju45r5fbva`.

Run from this directory with standard-library CPython 3.11 or later:

```sh
python3 -B independent_check.py --check
python3 -B -O independent_check.py --check
sha256sum -c SHA256SUMS
```

The verifier uses exact rational arithmetic.  It neither imports nor executes
the target verifier.  Its main independence boundary is the outer-heavy
vertex: instead of splitting full signed-permutation orbits by the
distinguished coordinate, it enumerates that coordinate explicitly and
quotients only the other two coordinates under signs and interchange.

See `REVIEW.md` for the verdict and scope.
