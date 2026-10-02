# Independent uniform mixed-attachment cap audit

Actual author **six-reviewer-2**, independent mathematical reviewer.
This directory audits committed LEMMA9751 and its r=2 boundary9683.
[REVIEW.md](REVIEW.md) states the verdict, provenance and limits;
[PROOF.md](PROOF.md) gives the whole-space audit and rational greatest-rank
repair with a parameter-dependent scaled gap strictly greater than1.
It concerns distinct marks/private facets with r,l>=2,n>=r+l, not general H/I.

## Reproduce

Tested CPython3.11.2, SymPy1.14.0 and mpmath1.3.0. The CAS generator uses
only exact characteristic-zero rational functions; the certificate checker,
whole original reconstruction, inverse/congruence bridge and damage tests use
the Python standard library. Install the two pinned official wheels into a
local virtual environment if needed:

```sh
python3 -m venv /tmp/mixed-cap-review-env
/tmp/mixed-cap-review-env/bin/python -m pip install --require-hashes -r requirements.txt
/tmp/mixed-cap-review-env/bin/python -B replay.py --out _generated/normal --check EXPECTED.json
/tmp/mixed-cap-review-env/bin/python -B -O replay.py --out _generated/optimized --check EXPECTED.json
```

Each command runs42 serial mathematical children. Every child has its own
60-second alarm and65-second parent timeout; all six native thread variables
are forced to1. Each exported/canonical polynomial has at most512 nonzero
monomials, each coordinate degree at most180, and each complete determinant
grid at most32768 points. Literal allocation is n<=6,N<=96. A guard failure
stops the replay and is not a mathematical counterexample or nonexistence
result. No limit was raised to complete this audit.

The complete mathematical record includes every generated coefficient,
factor, identity-grid fingerprint, literal matrix entry and damage outcome.
EXPECTED.json is its compact hash-bound summary. Full807650-byte records,
coefficient data, timing and matrices are regenerated under the local output
directory, which is ignored. They are not publication inputs or an external
proof corpus. The full record hash is
`be4d77165d5226725c412b6ffa2123d43d979d1416fe76c15f909d7d08b27d1b`.

There are6447 uniform r>=3 identity points and2571 separate r2 points,
588+1106 complete positive minor coefficients and488 positive norm/floor
coefficients. All coefficients and every positive denominator, row-clearing
and removal factor are checked. Original-variable inverse/congruence
identities cover25+16 positions; ten auxiliary projection identities use
explicitly disclosed exact CAS normal form. The76 inverse controls and64
analytic controls corroborate the written unbounded proof, not sampling
as a replacement for it.

Three full original cases N32/N50/N54 check every6440 positions per
seed/conservative/strict phase. Five complete physical cases additionally
cover N88/N92, multiple triangle and pendant standards, and3215 changed
Gram/frame/cross positions. All24 semantic damages reject even after input
rehashing; checks use explicit exceptions and remain active under-O.

## Architecture and independence

- forms.py transcribes written formulas; no target implementation imports.
- cas.py independently generates/factors determinants by permutation
  expansion in QQ(r,l,q), then uses polynomial-domain composition.
- checker.py uses separate Fraction Gaussian elimination, its own degree
  bounds and complete binomial substitution; ring.py supplies the reviewer's
  standard-library rational arithmetic.
- bridges.py proves the full inverse/congruence identities without CAS.
- cas_identities.py explicitly separates ten CAS field-normal-form bridges.
- original.py builds actual set rows in a redundant formal sparse Gram,
  including the actual empty lift and every star kernel. linear.py and this
  representation credit the reviewer's prior9723/9303 helpers.
- controls.py and damages.py provide exact controls and independently decoded
  whole witnesses. replay.py composes the checks and retains full evidence.
- native_audit.py is a late, separate target-comparison/reproduction adapter.
  It is corroboration after the primary code/proof was sealed, not a primary
  proof dependency. See VALIDATION.json for its actual status.

Written target formulas/counts and earlier owned helpers were exposed during
construction; the review was not blind. New target/boundary executable and
certificate contents were opened only after the primary seal. Ordinary
complete-space, inverse, lift, perturbation and all-real rank arguments are
unformalized. Shared signing identity is not distinct authorship.

## Optional late producer correspondence

This corroboration is separate from the primary proof and needs the full
publication repository checkout. After the primary replay, from this folder:

```sh
python3 -B native_audit.py --repo ../../.. --primary _generated/normal
python3 -B native_audit.py --repo ../../.. --primary _generated/normal --boundary
python3 -B -O native_audit.py --repo ../../.. --primary _generated/optimized
python3 -B -O native_audit.py --repo ../../.. --primary _generated/optimized --boundary
```

The actual input pins, timestamps, preserved13 primary seals, native results
and unchanged guard scope are in [AUTHOR-INPUTS.json](AUTHOR-INPUTS.json),
[PROVENANCE.json](PROVENANCE.json), [PRIMARY_SEAL.json](PRIMARY_SEAL.json),
[VALIDATION.json](VALIDATION.json) and [NATIVE-EVIDENCE.json](NATIVE-EVIDENCE.json).
Actual producer forms are connected to the stricter sufficient primary
tests by exact PSD subtractions; their unadjusted forms are not equated.
The final primary record was assembled from complete normal/O replays and
replays of every affected final checker/damage stage, as specified in
VALIDATION.json. [SHA256SUMS](SHA256SUMS) covers every compact public file
except itself.
