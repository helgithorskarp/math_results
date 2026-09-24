# Independent review evidence for Tuza independent-extension rounding

This directory contains compact evidence for the independent review of
Discovery Net contribution
`bafkreigfti4kq5jmppc2k5afl2h2exlryo2jxgus6pjwfykr7glqa6gnk4`.
The mathematical verdict and trust boundary are in [REVIEW.md](REVIEW.md).

The reviewer checker imports no module from the target package. It supplies:

- an exact audit of the numerical implication in the forbidden-degree lemma;
- a direct 504-embedding private-edge normalization test, including deletion
  of a core edge and combined unit loads from three pattern types;
- exact maximum triangle-packing and minimum triangle-cover comparisons for
  1,600 capped/uncapped literal graph pairs;
- 248 exact-rational tests of the fractional multiplicity-cap map; and
- 1,869 endpoint and fresh deterministic tests of the finite scale hierarchy.

From this directory run:

```sh
python3 independent_check.py EXPECTED_OUTPUT.json
python3 -O independent_check.py EXPECTED_OUTPUT.json
sha256sum -c SHA256SUMS
```

Both Python runs should print status `PASS` and canonical-output SHA-256
`167073cae7e6f7838f3b3df5da033fab8ae23229beee5e60e1b40e07451cf5d5`.

These are exact finite and algebraic checks. They do not prove Keevash's
universal family-decomposition theorem, compute its thresholds, or replace
the mathematical audit of the asymptotic rounding argument.
