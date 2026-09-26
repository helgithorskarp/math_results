# Every Gaussian hinge for an asymmetric square-cone family

Exact computer-assisted author proof, 26 September 2026. Independent
mathematical review and proof-assistant formalization are pending.

The [proof](PROOF.md) establishes full Gaussian majorisation at **every
variance and threshold** for the team's asymmetric nine-point contraction,
throughout an explicit L1 weight ball of radius **1/552**. This includes the
entire radius-1/4000 family whose center-law martingale and deterministic
common-output bridges were previously obstructed.

The theorem also covers **arbitrary bounded radial laws**, independent
cluster masses, and radius-dependent directional weights in two explicit
polyhedral cones. The directional classes have nonempty interior. No small
mass or large variance assumption is imposed. The unrestricted R3 conjecture
and the arbitrary-weight square-cone case remain open; no new
Kneser--Poulsen volume case is claimed here.

The proof acts on 48 signed coordinate permutations of the smoothed density.
Exact polynomial coefficient inequalities give two finite partial orders;
a universal upper-set correlation inequality gives every hinge. Orthogonal
averaging then transfers the finite inequality to the Gaussian integrals.
This compares density values after convolution and is compatible with the
previously proved obstructions on center laws and contracting motions.

## Reproduction

CPython >=3.11, standard library only. Verified on CPython 3.11.2, both
normally and with optimization, and CPython 3.12.14. From the repository root:

```bash
cd probability/gaussian_majorisation_square_cone_orbits
python3 verify.py --check
python3 independent_check.py --check
python3 -O verify.py --check
python3 -O independent_check.py --check
sha256sum -c SHA256SUMS
```

Expected successful outputs:

```text
SQUARE_CONE_ORBIT_MATCHING_CERTIFICATE_PASS 1e7e83d7ba23776bdf657773a71ba1ab3bbb8cc21c94a2b299cb4d36ce748d6e
SQUARE_CONE_ALL_UPPER_SETS_CROSSCHECK_PASS 7c3cbe320451a160565545d9d7d46ec7a03e4ec000a37c78fef941592ab8a311
```

The default commands without `--check` print the corresponding JSON audit
records. `python3 verify.py --certificate` regenerates CERTIFICATE.json.
Checks remain active under `-O`; failures raise an error and return nonzero.

## What is certified

| Obligation | Exact evidence |
|---|---|
| Correct contraction | 28 preserved and eight strictly contracting pairs |
| Orders valid on the entire chamber | All coefficients of every claimed polynomial difference checked |
| Uniform L1 margins | A: 1/552; B: 1/184, with attaining witnesses |
| Complete upper-set enumeration | A: 1541; B: 1645 |
| Correlation, first algorithm | 1541 monotone matchings, 25,463 total edges |
| Correlation, separate algorithm | All 2,534,945 upper-set pairs, minimum difference zero |
| Negative controls | Reversed order and corrupted comparison rejected |

[verify.py](verify.py) builds coefficients by binomial products, enumerates
upper sets by disjoint branching, and verifies explicit monotone matchings.
[independent_check.py](independent_check.py) imports no constructor code:
it rebuilds the matrices and polynomials by repeated multiplication, checks
every needed coefficient inequality in [CERTIFICATE.json](CERTIFICATE.json),
enumerates upper sets by breadth-first addition, and directly counts every
pair. Their independence concerns algorithms, not authorship or peer review.

[EXPECTED.json](EXPECTED.json) and
[INDEPENDENT_EXPECTED.json](INDEPENDENT_EXPECTED.json) are compact reproduction
records. Their hashes identify results; they do not replace the checks.
No floating-point calculation, solver, quadrature, external dataset, or
omitted large certificate enters the proof. Arbitrary spatial points,
weights, variances, thresholds, and radial laws are handled by the written
analytic reduction in PROOF.md, whose correctness is not formalized.

[SOURCES.md](SOURCES.md) credits the primary problem, configuration,
obstructions, independent review of those obstructions, and the team's
preceding high-variance result. Those reviews do not review this new proof.
