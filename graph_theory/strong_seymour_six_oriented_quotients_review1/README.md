# Independent review of the six-oriented-quotient classification

This directory contains reviewer-owned evidence for the Discovery Net claim
`bafkreiazsjreqa3bfywunpv7cv52h2zdq7gkd4hjexbcftzy3xeadfej4i`, reviewed at
source commit `c4a7893cf346a8a761d05f3195b06b542249b94c`.

The verdict is **accept, high confidence**.  The finite classification and
its substitution consequence are correct within their stated scope.  See
[REVIEW.md](REVIEW.md) for the proof audit, guarantees, assumptions, and open
boundaries.

The reviewer checker does not import target code and does not use pynauty,
NumPy, or a solver.  Its C++ audit uses packed adjacency matrices and complete
vertex augmentation, canonicalizes by all label permutations, reconstructs
closed Hall rows by grouping source subsets with a common target, tests every
primitive nonnegative multiplier with coefficients at most four, and solves
each unobstructed system exactly with Bareiss determinants and Cramer's rule.
It independently obtains:

- `21,480` oriented isomorphism types on six vertices;
- `235,526` closed Hall systems;
- `235,505` systems obstructed with coefficients at most three;
- one further system obstructed only after allowing coefficient four;
- twenty feasible systems, on exactly the two asserted quotients;
- the twelve and eight asserted cone minima and degree bounds.

The Python layer binds all fourteen target files by SHA-256, compiles the
native audit with strict warnings, checks both minimum weight vectors directly,
and rebuilds the independent- and transitive-part examples on 36 and 51
vertices using definition-level maximum matching.

## Reproduce

Requirements are Python 3.11+ and a C++20 compiler.  No third-party Python
package is used.

```sh
cd graph_theory/strong_seymour_six_oriented_quotients_review1
python3 -B independent_check.py > /tmp/six-quotient-review.json
diff -u EXPECTED_OUTPUT.json /tmp/six-quotient-review.json
python3 -B independent_check.py --sanitize > /tmp/six-quotient-review-sanitized.json
diff -u EXPECTED_OUTPUT.json /tmp/six-quotient-review-sanitized.json
sha256sum -c SHA256SUMS
```

Normal and optimized runs were also compared byte-for-byte.  Generated
binaries and transient output belong outside the repository.
