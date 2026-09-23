# Six two-intersection links cannot extend by eight blocks

Let `A` be twelve five-subsets on twelve points, with point degree five,
covering every pair, and with pairwise block intersections at most two.
There are exactly **six** isomorphism classes of `A`. For every class,
**at least nine additional six-subsets are needed** to cover the missing
triples. No upper bound of nine is asserted.

The classification uses two cycle deficit graphs and a forced row recurrence.
After exact symmetry normalization only twenty-six row sets remain.
Nonnegative integer weights on missing triples exclude eight additional
blocks in each class. The proof check uses only the Python standard library.

For a hypothetical twenty-block `(13,6,3)` covering with degree profile
`(12,9^12)`, this excludes maximum intersection two between the twelve
five-point residues at the degree-twelve point. Two of those residues must
intersect in at least three points. This removes the entire `k=2` row of the
earlier nine-class frontier; it does not settle `C(13,6,3)`.

## Reproduce

From this directory, using CPython 3.11 or newer:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > /tmp/c1363-check.json
diff -u EXPECTED.json /tmp/c1363-check.json
PYTHONDONTWRITEBYTECODE=1 python3 audit.py
sha256sum -c SHA256SUMS
```

Expected final verification status:
`VERIFIED_SIX_CLASSES_AND_EIGHT_BLOCK_EXCLUSION`.
The check exhausts all nine cycle partitions, six representative orbits,
and all 924 six-subsets for each of six weight certificates. Run time and
the interpreter used for validation are recorded in `VALIDATION.json`.

`classify.py` contains the complete enumeration; `verify.py` checks its
coverage by six explicitly generated isomorphism orbits and checks the
integer inequalities. `certificate.json` holds the six representatives and
weights. Its bit-mask convention is: bit `j` denotes point `j`, for
`0<=j<12`. `audit.py` imports neither proof program and checks the spectral
data by exact matrix determinants and the weights using ordinary sets.
It does not repeat the classification enumeration.

The full mathematical reduction and trust boundary are in `PROOF.md`.
No installed optimizer, solver, graph package, or external input is required.
The classical `4C_3` designs include the known R145 parameter set; no
historical priority is claimed for their existence or for cycle/Gram methods.
See `SOURCES.md` for prior literature and graph dependencies.
