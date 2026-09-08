# Physical decision handoff: K4 expansion interface

Append this interface to any h3887 task before another physical decision.
For every prescribed block Q it enforces that at least 19 of the 39 outside
vertices have a same-color neighbor in Q. The rule is valid for red and blue
blocks and for all 18 macro classes. It preserves the physical model set and
the existing task identity.

`augment.py CACHE --task TASK [--triangles] --cnf PATH` writes the complete
augmented formula. It refuses an existing output path. For the previously
attempted ordered triangle task:

```sh
python3 -B augment.py /tmp/k4e-data \
  --task bo1-q7-r7-c000000 --triangles --cnf /tmp/k4e.cnf
python3 -B audit.py --cache /tmp/k4e-data \
  --task bo1-q7-r7-c000000 --triangles --cnf /tmp/k4e.cnf
```

Expected full audit values are in `FORMULA_AUDIT.json`. A receiving solver
must treat variables 1 through 6,332 exactly as in h3887 and variables 6,333
through 10,868 as the new unique contact/counter extension. The full formula
has 923,269 clauses and SHA-256
`755dbcd5677bbc57a0865637dbce19fa72084c4846b3996b8697bf1485070178`.

`interface.py --q Q --r R --base-variables V --cnf PATH` writes only the
standalone suffix when integration into another compatible physical engine
is desired. Its header counts the V pre-existing variables although their
base clauses are intentionally absent. Preserve the exact h3873 physical
edge numbering and choose V as the total variable count of the receiving
base formula. `audit.py` can read this suffix independently.

The practical boundary is exact: 21 fully opposite-color stars into a block
produce a unit-propagation conflict; 20 such stars force every remaining
star to include the block color. This compactly represents more than 62
billion minimal h3897 cut clauses per block. A future physical decision can
therefore use ordinary CNF propagation or expose the same recurrence as a
native cardinality propagator.

For a SAT result, pass the solver model back through the same command with
`--sat MODEL` in place of `--cnf PATH`. The decoder requires a complete exact
assignment satisfying every augmented clause, strips only the uniquely
determined interface variables, and invokes h3887's complete physical-model
decoder and independent five-set verifier.

This handoff authorizes no inference from the earlier 1,800-second UNKNOWN
run. No new solver call, speedup measurement, task decision, or candidate is
contained here. An UNSAT result still requires a checked proof for the exact
augmented CNF. All 2,189,178 tasks remain undecided and no good43 is
established.
