# A 23-vertex tournament with no strong Seymour vertex

An explicit tournament improves the preceding graph upper bound from
24 to **23**. It belongs to a 13-part family of order `9a+b+3c` with
no strong vertex whenever

    a < b < 3a,       c > max(3a,a+b).

These conditions work with arbitrary internal tournaments and are
necessary and sufficient when all parts are transitive. The unique
smallest triple is `(a,b,c)=(1,2,4)`. A vertex is strong when arcs from
its out-neighborhood to its **exact** second out-neighborhood admit a
matching covering the first neighborhood.

[PROOF.md](PROOF.md) gives the quotient, all thirteen Hall witnesses,
the exact deficiency formulas, a rational certificate for the selected
Hall cone's minimum, and the five-arc surgery from the preceding example.
[SOURCES.md](SOURCES.md) credits the original nine-vertex quotient and
prior results. The current graph-supported interval is **16≤m≤23**;
the exact unrestricted minimum and the regular-tournament question remain open.

## Reproduce

Python 3.11 or later; standard library only. Tested with CPython 3.11.2.
Reference runs took about 0.13 and 2.04 seconds respectively, with peak
child RSS about 21 MiB. Outputs were byte-identical under Python `-O`.
From this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py
python3 construction.py
sha256sum -c SHA256SUMS
```

The first two commands print the checked-in `EXPECTED_PRIMARY.json` and
`EXPECTED_INDEPENDENT.json` respectively. The third prints the literal
matrix, with bit/column `j` equal to one precisely for the arc `i→j`.

* `verify.py` checks every quotient edge, all thirteen strict Hall rows,
  995 source subsets and 110 closed rows, the determinant-40 dual identity,
  207 expanded-vertex Hall witnesses across three internal rules and two
  scales, and six rejected invalid fixtures.
* `independent_check.py` imports none of the other source files. It reads
  the literal matrix, exhausts 62,464 Hall subsets, computes matchings
  from exact-distance neighborhoods, and reconstructs the family from
  the separate cyclic surgery rule. All 216 triples `1≤a,b,c≤6`, covering
  9,828 vertices, satisfy the stated full deficiency formula.

The two literal-graph checks use different representations and algorithms.
They are checks written by the author, not an external peer review.
The universal classification follows from the complete symbolic table,
not the finite parameter audit. No search solver, numerical tolerance,
external data, or unrecorded generated artifact is needed.

Literal matrix SHA-256:

`97d505a5fe2b68bdcc704c6ace82ffd0a4a387da6a94ac032b13ea24762c062e`

Independent parameter-audit SHA-256:

`baacc9e8262698c4a56ecde012498d7b895fb261cbff70d5a9dda7cb676d62f3`

The selected thirteen-row cone has unique total-weight minimum 23.
This is not a minimum over all Hall choices on this quotient or over all
tournaments. The accepted lower bound through order 15 is imported and
its separate SAT certificates are not replayed here.
