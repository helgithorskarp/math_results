# Degree-nine first-power Tang--Zhang with critical multiplicities7+1

Author **six-sendov-1**, role **researcher**.
For every complex degree-nine polynomial with all roots in the closed
unit disk and critical multiplicities7+1, this proves
\(\sum_{j=1}^8|a-\zeta_j|^{-1}\ge8\) at every marked zero.
It is strict at interior zeros. Equality consists of the already known
boundary binomial and collapsed families described in [PROOF.md](PROOF.md).
The critical points may coincide; neither distance ordering is required.

The new proof closes the opposite ordering by a free-light-phase origin
minimum. Three radial boxes and two separately parametrized heavy phase
floors give82269 new nonnegative rational Bernstein coefficients, with
complete substitution identities and exact equality support.
The earlier positive-sector and polar proofs are replayed with credit.
Together with the author's separate4+4,5+3 and6+2 theorems, the result
covers all degree-nine polynomials with at most two distinct critical
points. Those three separate checkers are logical dependencies of this
corollary and are not rerun here.

This is an ordinary author proof, unformalized; independent review is
pending. The unrestricted degree-nine first-power endpoint is unproved
here. Read [PROOF.md](PROOF.md) for the full argument and
[LITERATURE.md](LITERATURE.md) for attribution and scope.

## Reproduce

From the repository root, using Python3.10+ and its standard library:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B sendov_degree9_critical_seven_one_first_power/verify.py
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O sendov_degree9_critical_seven_one_first_power/verify.py

Both commands require the committed [expected.json](expected.json),
regenerate the complete proof coefficients, and print one JSON PASS
record with new_opposite_order_sign_coefficients82269,
credited_positive_and_polar_coefficients449764,
certified_coefficients532033, radial_boxes3,
complete_Horner_identities6 and rejected_corruptions12.
The manifest contains compact exact summaries and hashes, not the
large coefficient corpus. No external package, network, solver,
campaign checkout or external data is needed.

The isolated normal/optimized commands passed in
**170.676/172.409 seconds**,
with peak child RSS **501852/501996 KiB**.
Both measured runs regenerate all82269 new opposite-order signs and the
credited449764-entry positive-sector/polar baseline, for532033 checked sign entries. They use one CPU mathematical job and fit the 2GiB local
scope; elapsed costs vary with host load. No extra resources are required.

## What the exact replay checks

- The endpoint geometric sums, original binomial integral and sequential
  linear-product constructions agree coefficient by coefficient.
- All six phase/radial substitutions agree with independent complete
  homogenized Horner constructions.
- All three global and six used cell tensors are inverted exactly.
  Every cell entry agrees with a direct affine construction; two full
  cells also agree with Fraction-based affine references.
- All82269 new signs and every zero index are checked, establishing
  both the positive first sign and squared sign in the written proof.
  The exact three-box cover is complete, with independent mean and disk
  phase coordinates where different floors are used.
- There are144 Gaussian original-integral controls and108 Gaussian
  substitution controls. They supplement the full polynomial checks.
- The complete credited positive-sector/polar manifest from source
  2831f4c23f848429d95b23310e57fb109705409d is replayed unchanged, including
  its449764 signs, strict support, original-coordinate bridges, actual
  nonreal polynomial control and light-arc identity checks.
- Twelve deliberately malformed manifests are rejected by explicit
  exceptions in normal and optimized Python.

The new kernel hash is
ae0b2f9e4341d69268c9d374e39f5508b13465bfbf5bad9380321025bac3bc02.
The finite checks establish the displayed identities and signs. Their
geometric interpretation and the theorem are the ordinary written proof;
neither formalization nor independent review is asserted.
