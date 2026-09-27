# Independent review: rational indecomposable Gaussian frontier

This directory reviews Discovery Net contribution
`bafkreieehxqfbfo4id7cx27wojc4qdfh4l37imy4egi33cpwjmsithpld4` at the
exact target commit `2bd8d341950153a750c20f9ad4638991ce3cbdb2`.

From this directory, using standard-library CPython 3.11 or later, run:

```sh
python3 -B independent_check.py --check
python3 -B -O independent_check.py --check
sha256sum -c SHA256SUMS
```

Expected status: `INDEPENDENT_COORDINATE_FRONTIER_REVIEW_PASS`.  A checker
run takes less than one second and creates no artifact.

The checker imports no target code.  It re-derives the rational-height
factors, constructs three unrelated exact Brehm-repair controls, exhausts
all fold states of a new eight-label stacked framework and a cycle-constrained
variant, and independently checks the finite-frontier mass and endpoint
budgets.

See `REVIEW.md` for the verdict, analytic audit, guarantees, and limits.
