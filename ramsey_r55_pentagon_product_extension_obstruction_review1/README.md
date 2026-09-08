# Independent review of the h3947 pentagon-product extension obstruction

Verdict: **ACCEPT** the claim that no good graph properly contains an induced
`C5[C5]`, and hence that the h3931 pattern-free equality core cannot extend to
a good43 graph.  This is an intermediate structural exclusion, not a
43-vertex Ramsey graph and not a proof of `R(5,5) >= 44`.

The review re-derives the mark-cover proof, reconstructs the 25-vertex core,
checks all 32 inner attachment words and all 243 outer mark assignments,
validates 27,015 selected physical witnesses, and probes the source interface
on fresh full 43-vertex graphs under relabeling and complementation.  It
imports no reviewed Python module.  [REVIEW.md](REVIEW.md) gives the detailed
scope and trust boundary.

From the repository root, with CPython 3.11 or later and a fresh work path
under scratch storage:

```sh
python3 -B ramsey_r55_pentagon_product_extension_obstruction_review1/reproduce.py \
  . /scratch/review-h3947
```

Expected status: `REPRODUCED_ACCEPT_REVIEW_H3947`.  The command extracts the
reviewed source commit, reruns its complete deterministic replay, and runs the
independent checker in normal and assertion-disabled modes.  It uses only the
Python standard library and Git, makes no solver call, and downloads nothing.
