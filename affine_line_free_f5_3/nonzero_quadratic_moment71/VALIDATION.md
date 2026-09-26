# Author validation

The complete verifier passed on 2026-09-26 with:

* Python 3.11.2, ordinary execution;
* Python 3.11.2 with `-O`;
* Python 3.12.14;
* GCC 12.2.0 with both address and undefined-behavior sanitizers,
  using the command in [README.md](README.md).

All runs include the full 1,081,575-subset planar census and all
14,348,907 quartic information words. The canonical JSON outputs
agree exactly with [EXPECTED.json](EXPECTED.json), whose SHA-256 is
`1950d1be2e67d416eef35b43e092dda342afe2bae16e55e120a26e122fadfaf7`.
No sanitizer failure was reported.

The distinct checks address the following boundaries:

1. The projective quartic evaluation minor and its exact inverse are
   checked, so the information words cover all potentially square-valued
   quartics with no orbit-identification assumption.
2. Full labeled catalogue equality with explicit quadratic squares and
   binary cones is checked, not merely its cardinality or spectrum.
3. A direct coefficient-reconstruction evaluator checks a 19,683-word
   slice, giving the same 73 retained words.
4. All 3,125 binary forms are evaluated independently to check the
   six-point sum-zero parameterization used for the cone family.
5. All 125 affine points satisfy the conic identity pointwise; the
   six possible five-arc completions and all 930 required quartic
   collinearity assertions are checked.
6. All 715 deficit compositions are examined, producing the 27 profiles
   in the written proof. The integer reductions in both cubic branches
   are separately enumerated and leave zero unexcluded cases.

Negative controls reject an empty matrix, a matrix with an extra
entry, an out-of-field entry, a missing completion marker, an incorrect
enumeration counter, and deletion of the zero quartic from the
catalogue/family comparison. These checks use explicit exceptions,
not Python `assert` statements.

The proof's finite inputs are regenerated locally; the compact expected
output is a regression check, not an externally supplied classification.
The written geometric and moment reductions remain part of the trust
boundary. These are author-run checks, not an independent accepting
review or a proof-assistant verification.
