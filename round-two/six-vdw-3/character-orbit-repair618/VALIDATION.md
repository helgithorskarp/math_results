# Reproducible finite checks and the written proof

six-vdw-3, researcher. The result is author-checked, with no external
independent review or formal proof claimed.

The producer uses Euler powers modulo103 and searches actual cyclic
progressions. The checker imports no producer code. It constructs the
51 nonzero squares by multiplication, evaluates all102 orbit APs and
their integer lifts literally, and compares their complete field supports.
The 102 supports are distinct, all have size7, and all102 vertices have
degree7. These facts certify the fractional edge weights1/7 without any
solver. Nine changed certificates are rejected in each Python mode.

The checker covers all64 binary phase rows, all30 start/nonzero-step
phase pairs per row, and literal singleton-column obstructions for the
58 illegal rows. It checks every nonzero multiplicativity input and all
10506 affine field parameter pairs with separately enumerated units and
shift coefficients. Full counts and transcript hashes are in expected.json.
It does not enumerate all possible edited sets or all2^100 orientations.

The ordinary counting proof, the phase classification, the affine
bijection, the interval-lifting argument and the distance corollary are
written in PROOF.md. In particular, the exact fractional cover value uses
the written fact that a legal-phase regular bad AP has seven distinct
field vertices. The full bad-AP hypergraph is not enumerated. Python and
the independent exact checker remain computational trust boundaries.

Run the source-pinned public reconstruction:

```bash
python3 reproduce.py --work /tmp/character-orbit618-check
```

It runs the generator and checker serially in normal and optimized
Python, compares every generated certificate byte with certificate.json,
and compares each complete check result with expected.json. Every child
has a20-second wall-clock guard and one numerical thread. Outputs go to
the chosen work directory; the source directory is not modified.

verification.json records the author's fresh reconstruction, including
runtime and peak child memory. These measurements are operational
receipts, not part of the mathematical proof. No SAT/LP proposal, native
refutation, converter, floating-point computation or bulky certificate
is needed for this lemma. Earlier unsuccessful private searches are not
premises. A timeout while reproducing is an operational failure and must
not be interpreted as a mathematical exclusion.
