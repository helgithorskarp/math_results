# Independent review: loss-proportional paired Gaussian cubature

This directory reviews Discovery Net contribution
`bafkreicuyedmct5zhkt5cxba2nkvgel3tkursxckgxcryd45ed53khps5e` at the
exact target commit `afacddeb257993b31ee118ff92e7360a7870cbc6`.

From this directory, using standard-library CPython 3.11 or later, run:

```sh
python3 -B independent_check.py --check
python3 -B -O independent_check.py --check
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_LOSS_CUBATURE_REVIEW_PASS`.  A checker run
takes about 40 seconds on one CPU and creates no artifact.

The checker does not import target code.  It independently constructs an
exact common cubature by rational row reduction, enumerates replica scatter
laws from the definitions, and encloses exponentials by reciprocating a
positive series with a geometric tail.  Its three contractions include one
whose loss is about `2.6e-10`, directly exercising the claimed uniformity as
loss tends to zero.

See `REVIEW.md` for the verdict, analytic audit, guarantees, and limits.
