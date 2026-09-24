# Independent review evidence for bounded-type triangle rounding

This directory supports the independent review of Discovery Net contribution
`bafkreienkkf63nylhemuybw7f6qfcbkgfehhwcvjmoaj265dqnbuuchve4`.
The verdict, proof audit, exact scope, and residual trust boundary are in
[REVIEW.md](REVIEW.md).

The checker imports no target module. It independently performs exact finite
checks of the new pendant-role, row-normalized-flow, color-repair, ordered
Hall-matching, size-hierarchy, filler-edge, and parity interfaces. These are
supporting checks; the universal Keevash specialization and induction are
human-audited mathematics rather than finite computations.

From this directory run:

```sh
python3 independent_check.py \
  ../tuza_bounded_type_linear_rounding/AUDIT.json \
  EXPECTED_OUTPUT.json
python3 -O independent_check.py \
  ../tuza_bounded_type_linear_rounding/AUDIT.json \
  EXPECTED_OUTPUT.json
sha256sum -c SHA256SUMS
```

Both Python commands should print status `PASS`. Only the Python 3.11 standard
library is required.
