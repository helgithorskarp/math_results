# R(5,5): rank-four row-triple completion over support sizes 5--8

No good 43-vertex graph occurs in the following fixed-cut family.  Split the
vertices as 20+23 and write the red cross matrix as `U V^T` over `F_2` in
rank four.  The rows of `U` contain one zero, all 15 nonzero vectors, and two
additional copies of each of two distinct nonzero vectors.  Thus those two
labels occur three times.  The 23 rows of `V` are nonzero, span `F_2^4`, use
between five and eight distinct labels, and use every label at most five
times.  All 443 same-side edges are physical Boolean variables.

There is one `GL(4,2)` orbit of the 105 choices for the two tripled labels.
Its inverse-transpose stabilizer action partitions the 20,443 spanning column
supports of sizes 5--8 into 288 orbits.  One symmetry-reduced SAT formula
leaves the support, all allowed column multiplicities, and all 443 internal
edges variable.  CaDiCaL refuted this complete formula, and `drat-trim`
accepted its 125,479,174-byte binary DRAT proof.  This covers
30,213,993,600 row/column factor-multiset pairs before change-of-basis and
vertex-permutation identifications.

The encoding includes the retained contact and equal-row distance conditions,
the same universal distance condition for equal column labels, the good43
degree interval 18--24, and literal red/blue five-set clauses.  These are
necessary conditions; including them can only strengthen an exclusion.

This is a structured family exclusion.  It does not construct a good43,
exclude supports of size 9--15 or other row multiplicity profiles, prove that
a hypothetical good43 has such a cut, or improve `R(5,5) >= 43`.

See [PROOF.md](PROOF.md) for the reduction and [VALIDATION.md](VALIDATION.md)
for the evidence and trust boundary.  Compact verification uses Python 3.11
or newer and the standard library:

```sh
python3 -B reproduce.py
```

Expected status:

```text
VERIFIED_COMPACT_ROW_TRIPLE_SUPPORT_5_8_EXCLUSION
```

Full replay requires CaDiCaL 3.0.1 at commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04` and `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.  Regenerate the 93,795,698-byte
base formula, enumerate supports, then run the aggregate proof in an external scratch
directory:

```sh
mkdir -p /tmp/r55-band
python3 -B build_base.py --orbit 15 --support-maximum 8 --support-symmetry --cnf /tmp/r55-band/base.cnf --metadata /tmp/r55-band/base.json
python3 -B support_representatives.py --orbit 15 --output /tmp/r55-band/supports.json --masks /tmp/r55-band/masks.txt
python3 -B band_proof.py --cnf /tmp/r55-band/base.cnf --metadata /tmp/r55-band/base.json --solver /path/to/cadical --checker /path/to/drat-trim --proof /tmp/r55-band/proof.drat --result /tmp/r55-band/proof.json --seconds 600
```

The 93,795,698-byte formula encodes the correct inverse-transpose support
symmetry and support upper bound.  The committed compact proof record gives
its CNF and proof hashes.  The generated CNF and proof are deliberately
omitted; replay regenerates, checks, hashes, and deletes the proof.
