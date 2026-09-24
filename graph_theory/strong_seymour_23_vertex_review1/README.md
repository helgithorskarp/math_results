# Independent review of the 23-vertex strong-Seymour counterexample

This directory records an independent review of Discovery Net contribution
`bafkreigb7tiusrxbfrjqtvrdscbvedykxmi7fevxtpmvztq5z2nt3oq754`,
reviewed at source commit
`84e2cafd6e1733cb7e5aca808a0b248db22c17ec`.

**Verdict: accept, high confidence at the stated scope.** The literal
23-vertex tournament has no strong Seymour vertex. The 13-part construction,
its sufficient parameter chamber, its exact transitive-part classification,
and its selected-certificate-cone minimum are correct. This does not prove
nonexistence at order 22 or unrestricted minimality at order 23.

See [REVIEW.md](REVIEW.md) for the mathematical audit and trust boundaries.

## Independent reproduction

Python 3.11 or later, standard library only. From this directory run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
PYTHONDONTWRITEBYTECODE=1 python3 -O independent_check.py
sha256sum -c SHA256SUMS
```

Both checker runs must reproduce `EXPECTED_OUTPUT.json` byte-for-byte. The
checker imports no target module and reads no target certificate. Its only
target input is the published `tournament23.txt` literal. It:

- computes exact second neighborhoods directly from the 23-by-23 matrix;
- computes maximum matchings by reachable-right-mask dynamic programming;
- exhausts all 62,464 Hall subsets independently;
- derives the 13-part quotient from homogeneous blocks of the literal;
- enumerates all 995 nonempty quotient source subsets and reconstructs the
  universal symbolic deficiency formulas;
- checks the selected dual using fraction-free integer elimination; and
- checks all 1,144,066 positive 13-part compositions of total at most 23,
  finding only the published weight vector feasible for the selected rows.

The expected-output SHA-256 is
`01210bf3c978b5799ed521942147d8b5c7becd487c2d56e2a24bf953398cd540`.
Observed CPython 3.11.2 runtimes were 2.27 seconds normally and 2.33 seconds
with `-O`.

## Trust boundary

The checker uses exact Python integers, filesystem reads, and SHA-256. It
validates the finite and symbolic claims but is not a proof-assistant
formalization. The arbitrary-internal-tournament extension and the chamber
equivalence are also audited in prose. The separate order-at-most-15 SAT
lower bound is not replayed here.
