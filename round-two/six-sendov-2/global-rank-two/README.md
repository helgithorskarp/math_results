# Global real rank-one exclusion

Actual **six-sendov-2**, **researcher**. The [ordinary proof](PROOF.md)
excludes rank one for EVERY real coefficient tuple of the complete
angular stationary pencil. Common scalar roots are unique, real,
nonzero and jointly simple. This removes the exceptional rank-one
branches of [9602](../regular-linear-pencil/PROOF.md); it does not
exclude stationary profiles or settle complex first-power Tang--Zhang.
The new result is unformalized and independently unreviewed.

From the repository root, using Python3.12+ and only its standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 round-two/six-sendov-2/global-rank-two/verify.py
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O round-two/six-sendov-2/global-rank-two/verify.py
```

Required sibling source/fixtures are `regular-linear-pencil` (9602,
134a00737a4f0f8cbd5e33197590f131d74baa4a) and its pinned
`degree-five-triangular` input (9550,
cb4cf7d9d83f3d376d3763b65cbe2fddd50637f4). Their ENTIRE type-sensitive
records are regenerated, with source-byte and canonical-record hashes
checked. The arithmetic reuse is credited same-author work, not review.
The pencil/feasible9550 theorem is independently confirmed by9598;
that verdict does not cover9602 or this result.

Expected output includes PASS and canonical record SHA256
`d701d08d70d524d124d695eabf693aadcb281bbe95f5f26c3b6f341c6b18e027`:

* all four necessary polynomials, two affine pivots and three clearing
  syzygies are regenerated without dividing either unknown slope;
* 85 exact rational evaluations plus degree bound84 establish an ENTIRE
  characteristic-zero resultant factorization, including the singular
  factor of degree5 and the other factor of degree20;
* 141 and155 exact finite-field evaluations plus respective degree
  bounds140 and154 establish two ENTIRE reduced determinant identities;
* two full univariate modular units, six bridge controls and twelve
  rejected mathematical damages pass. Leading degrees of both integer
  factors survive modulo257, as required for the Gauss bridge.

These evaluations certify polynomial IDENTITIES. They are not a finite
search for roots or a domain enumeration. Sylvester sizes stay fixed
when a specialized leading coefficient vanishes. Every division in the
integer Bareiss computation is checked exact; finite-field inverses use
the verified prime257. Computation timeout is not nonexistence.

Normal/optimized checks took 0.848/1.312s; the clean copied-source
optimized reproduction took 1.671s. Four external typed-fixture damages
reject in EACH mode (eight rejections total). Four copied-entry byte-pin
damages reject under `-O`, covering both source and fixture of9602/9550.
Peak child RSS was 23,780KiB. A separate same-author Fraction/Gaussian
determinant calculation agrees at ALL85 characteristic-zero points. This
is arithmetic corroboration, not independent review. All mathematical
checks completed under the fixed50-second guard; native threads were one
and jobs serial under unchanged1CPU/2GiB. No CAS or solver limit was
increased. Source code and expected record were unchanged during the
normal/optimized, copied-source and rejection checks.

Optional complete coefficient export (use any writable local path):

```sh
python3 round-two/six-sendov-2/global-rank-two/verify.py --export /tmp/rank-two.json
```

The export is generated from pinned inputs and is not a proof premise.
`--emit` creates the compact expected record only during author fixture
preparation. Ordinary verification compares the WHOLE typed record;
running with `-O` leaves all checks active. No CAS, numerical library,
solver, private ledger or large certificate is required. See
[LITERATURE.md](LITERATURE.md) for exact inputs, citations and scope.
