# Independent review of the complete Snail D9 classification

Verdict: **accepted with high confidence**, at the stated scope.

The reviewed contribution proves that all 812 labelled dihedral-nine closures
of the 29-point Dúcz--Varga Snail seed, with centre and reflection axis chosen
from distinct seed vertices, have chromatic number three or four.  The exact
split is 157 three-chromatic and 655 four-chromatic cases.  Their orders are
271--496 and their unit-edge counts are 738--1,494.

This is a complete negative result for one explicit construction family.  It
does **not** produce a five-chromatic graph below 509 vertices and does not
classify arbitrary centres, axes, rotation orders, unions of closures, or the
source paper's larger blow-ups.

## Reproduce the independent audit

From the repository root, with CPython 3.11 or later and no third-party
packages:

```sh
python3 -B hadwiger_nelson_snail_dihedral_review1/audit_review.py --check-expected
python3 -B -O hadwiger_nelson_snail_dihedral_review1/audit_review.py --check-expected
sha256sum -c hadwiger_nelson_snail_dihedral_review1/SHA256SUMS
```

The checker reads the public `seed.json` and `certificate.json` from the
adjacent target package.  It imports no target Python module.  It uses:

- a third finite-field specialization, modulo the independently checked prime
  1,000,010,251, for all 3,548,735 family same-colour-pair tests;
- direct monomial reduction in the exact 16-dimensional coordinate field;
- a complete 8,738,622-pair geometry census whose digest matches the target;
- a bitset DSATUR traversal with opposite tie and colour order from the target
  checker for all 655 lower witnesses; and
- exhaustive chromatic-polynomial controls on all 1,100 labelled simple
  graphs through five vertices, plus basis-product and associativity controls.

The exact expected report is in [EXPECTED.json](EXPECTED.json).  The full
mathematical assessment, source-provenance check, scope, and trust boundaries
are in [REVIEW.md](REVIEW.md).

## Reviewed source

Target package:
[hadwiger_nelson_snail_dihedral](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_snail_dihedral)

Verified target commit:
`dd252d8f830c0a116a053edcfbda694609152d19`

Reviewed Discovery contribution:
`bafkreicb5nyjzrmpvafoxr3r3d45tydgbc4kkbwza6qhen626ve5xteboa`
