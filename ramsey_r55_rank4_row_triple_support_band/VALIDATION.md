# Validation and trust boundary

The production orbit enumerator builds `GL(4,2)` from adjacent basis swaps and
one transvection.  It finds 16 row-full multiplicity orbits in total and fixes
row orbit 15.  Its stabilizer partitions all 30,392 spanning nonzero supports
of size at least five into 475 orbits.  The completed theorem uses all 288
orbits at sizes 5--8, covering 20,443 supports.

The single 93,795,698-byte CNF encodes all 288 canonical supports at once.  Its
SHA-256 is checked before solving.  CaDiCaL 3.0.1 emitted a 125,479,174-byte
binary DRAT proof, and `drat-trim` accepted it before its hash was recorded.

`audit.py` imports no production module.  It independently:

- constructs all 20,160 invertible linear maps from ordered bases;
- verifies the 105-member row-pair orbit and stabilizer order 192;
- reconstructs all 475 support orbits and compares every representative and
  orbit size with `support_orbits.json`;
- checks the exact 288-orbit and 20,443-support coverage of the formula;
- derives every variable and clause block analytically, including all
  1,817,142 literal five-set clauses; and
- recomputes multiplicity counts and every aggregate in `RESULT.json`.

`encoding_controls.py` exhaustively checks the production sequential-counter
semantics with and without gates.  It separately tests repeated literals,
which represent distinct physical incident edges forced to share a color by
equal factor labels.  Normal and assertion-disabled runs must agree exactly.

The large CNF and DRAT files are omitted under the repository size boundary.
Their identities, sizes, solve/check times and accepted status are retained in
`proof_result.json`; `build_base.py` and `band_proof.py` regenerate and check
them.  A fresh proof must independently pass the checker.

Trust remaining: the written mathematical reduction, Python 3.11 integer and
file semantics, CaDiCaL 3.0.1, standard DRAT soundness, the pinned
`drat-trim` C checker, SHA-256, ordinary hardware, and the imported reviewed
Ramsey structural results listed in [PROOF.md](PROOF.md).  The compact audit
checks recorded proof metadata; a full independent proof replay uses the
documented external tools and omitted generated files.

The teammate's later rank-four projection witness has zero and a broader
column multiplicity pattern.  It is a local necessary-projection witness, not
a physical good43 and not a contradiction to this full completion exclusion.
