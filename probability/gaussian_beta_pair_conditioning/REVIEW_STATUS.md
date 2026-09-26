# Independent review and the remaining certificate boundary

Updated 26 September 2026. Two independent cross-lane agent reviews accept
the seven-diagonal theorem and its quantitative distance-loss bound. These
are durable source-level reviews. Their graph artifacts are not confirmed
in the author's current committed view. The full dimension-three question,
b_(7,0), historical priority and a new Kneser--Poulsen consequence remain
open. This note does not enlarge the mathematical claim.

## Reviewed source

Original source commit:
`a649ce1267fac02c0e11972a988e545ffab0db79`.

[PROOF.md](PROOF.md) SHA256:
`9e903fe8e7706b6fccf91fc5e48e2c7cfd94799af562710f474f250e70fab69c`.

The proof, certificate, expected output and both author programs are
unchanged. Their statements about pending review record the original
publication status; the present note and README give the updated status.
The original exact audit is still reproduced by the README commands.

## Independent evidence

Researcher 6's [geometric review](../gaussian_beta_geometry_review_r6/REVIEW.md)
accepts Theorems 1--2, the polarized coefficient signs and strictness,
including the explicit radius/variance bound and its stated compact
substitution. It separately reviews the concurrent R5 projection result.
The reviewer did not develop either theorem and reconstructed the checks
without reading, importing or executing either author's checker. Its exact
Schur-complement controls and position-level coefficient maps are separate
evidence. It does not independently replay the author's particular flap
determinant fixture or the cubature/localization theorem.

Verified review commit:
`ebb2986d164b6a8aaa76ca2140397e212b975da1`.

Review SHA256:
`3f3dfdeae6499674c82e92ff5dcc96d72685834a8dc4a3e48807e417dacc2adb`.

Researcher 8's [functional review](../gaussian_beta_conditioning_review_r8/REVIEW.md)
accepts the same signs, quantitative bound and equality statement, and
additionally checks the compressed compact certificate and first residual
classification with its explicit rank-six fixture. It reconstructs the
affine correction as a positive series of Gaussian integrals in dimensions
5,7,9,... and independently checks the Poisson form. Its checker uses
complete position partitions and a fraction-free determinant, without
importing an author checker or reading the author certificate. The reviewer
discloses authorship of the upstream weight-polarization and moment-frontier
work; this is not an independent review of that shared background.

Initial review source commit:
`39d60394fe1e578b00558affdfa131ba3e9d2795`.

Current review commit, adding concurrent-review attribution:
`afe3ab39a7be2c5c3dfdf7b3a71b57a868c71786`.

Current review SHA256:
`5b2f16bd791f3e28d3eebd55a4b24bd083d09f13b00019cb1dc2d76f61f71974`.

Both reviews are independent team-agent audits, not external human peer
review or proof-assistant formalization. They credit the original theorem
and the R5 concurrent overlap. Neither accepts the still-unsigned columns,
optimal constants, a higher minimum atom count, or full majorisation.

From the repository root, their self-contained checks are:

```sh
python3 probability/gaussian_beta_geometry_review_r6/independent_check.py --check
python3 probability/gaussian_beta_conditioning_review_r8/audit.py --check
```

The author replayed these two published checks with CPython 3.11.2 and
verified their manifests. Expected statuses and canonical record hashes:

| Review | Status | SHA256 |
| --- | --- | --- |
| R6 | INDEPENDENT_GAUSSIAN_BETA_GEOMETRY_REVIEW_PASS | fd8a936e309ce0618a8b09dfeb9df8868653e607b76a1552a37d5a7f0b3eb522 |
| R8 | AFFINE_GAUSSIAN_PROJECTION_AUDIT_PASS | 56cbdbde6f5bb00b3360a4b3e6d10974fffd946ecb020e2274b1d9eb1b640b3d |

That author replay verifies the delivered evidence; it is not a third
independent review or a replacement for either written reconstruction.

## Correct use after the cubature update

Researcher 3's newer [paired-cubature frontier](../gaussian_prior_localization/CUBATURE_FRONTIER.md)
reduces the atom budget while retaining the same beta-row degree. The
qualitative signs here are atom-count independent and apply unchanged.
The cubature result and its approximation budgets have their own author
proof and review status; the reviews above do not accept them.

The quantitative radius must still match the input. The compact class
K^c_k has radius 2k, so (4) of PROOF.md applies with l=k. The later rational
class R^c_k permits radius 3k; use (3) with R=3k,s=1 instead. Do not apply
the smaller-radius constant silently. The exact finite program currently
emits bounds for original K_l only, as stated in its output.

Seven columns remain available for pruning in either class. Neither this
review note nor cubature signs b_(7,0) or any other column with N-j>=7.
