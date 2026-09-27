# Sources, dependencies and scope

Primary sources and the relevant team neighborhoods were inspected on
27 September 2026. Aishwarya--Li is the sole problem source. This is a
complete author proof with exact supplementary checks; independent
correctness and historical-priority review are pending.

## Primary inputs

- G. Aishwarya and D. Li, *Gaussian Convolution, Internal Energies, and the
  Kneser--Poulsen Conjecture*,
  [arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2), revised
  13 September 2026. Theorem 1.4(i)(a) gives sampled-density order for a
  continuous contraction on a subset. Its discussion explicitly identifies
  at most two auxiliary dimensions as sufficient for full majorisation.
  We use that established transfer, with the two-coordinate cancellation
  written out in PROOF.md. Theorem 1.3 alone does not give the full R3
  conclusion sought here.
- K. Bezdek and R. Connelly, *Pushing disks apart--the Kneser--Poulsen
  conjecture in the plane*, J. reine angew. Math. 553 (2002), 221--236,
  [arXiv:math/0108098](https://arxiv.org/pdf/math/0108098).
  Theorem 1 transfers a piecewise-smooth motion in dimension n+2 to
  arbitrary-radius union and intersection inequalities in dimension n.
  Corollary 5 treats partial dilation by one common factor using the
  classical norm-displacement lift. Neither transfer nor that older lift
  is claimed here. PROOF.md gives an admissible two-ray pair on which the
  older displayed lift fails, while the fractional-linear motion works.
- K. Bezdek and M. Naszodi, *The Kneser--Poulsen conjecture for special
  contractions*, [arXiv:1701.05074v4](https://arxiv.org/html/1701.05074v4).
  The strong-coordinate condition and Theorem 1.3 are compared with the
  global angular example. The separate uniform-contraction condition
  compares all source distances with all target distances; it is not the
  hypothesis of our theorem.

The contribution under review is the uniform fractional-linear raise for
all nonexpansive nonnegative homogeneous ray maps, its exact full-cone
criterion, and the resulting broad Gaussian/Kneser--Poulsen class.
Targeted primary-source searches did not locate this complete class or
motion. This is a bounded literature assessment, not a claim that priority
has been established. A prior statement of the same class would change
the novelty assessment without changing the proof obligations.

## Relationship to durable team work

| Source | Role and boundary |
|---|---|
| [Common radial profiles](../gaussian_radial_contractions/PROOF.md), graph 6317, `bafkreiequbwj2ms2eev5sydi5exukocl3ycgaryq5bcywqxypf367hgoui` | One common function of radius, independent of direction. The new theorem instead allows one factor per direction, independent of radius. Composing the two positive maps gives the additional closure examples stated in Section 6; only that observation invokes this predecessor. |
| [Convex normal profiles](../gaussian_radial_contractions/CONVEX_CORES.md), graph 6331, `bafkreifktf3exjltqmj5gnt5wvhpqe2za3cbb7rkdnlt3ha774is52k2j4` | The accepted arbitrary-convex-core package is preserved. No strict containment or general separation from all choices of convex core is asserted. |
| [Scalar transport defect](../gaussian_majorisation_scalar_defect/PROOF.md), graph 6066, `bafkreidpgtehewdn2wn72hfi4c6aoq5bohkdss6dv36o37rjyxg6ndzxlq` | Existing sufficient criterion and Gaussian cancellation. Our global example fails this direct criterion for every pair of independent axes; its proof is included. No failure of majorisation follows from failure of the criterion. |
| [Paired-rank reduction](../gaussian_majorisation_rank_abel/PROOF.md), graph 5964, `bafkreidnqtxulerp64z7i2syzjymc3beilgovd4gyfcu5h2mzmim5l5ytu` | The rational calibration has paired affine rank six. This checks a scope distinction, not a claim that the finite fixture escapes all prior positive classes. |
| [Axial cone and matrix-path portfolio](../gaussian_axial_cone_rotations/REVIEW_GUIDE.md), original graphs 6062 and 6118 | Preserved flagships. The angular theorem is a full-cone factor principle, without their cluster-axis or matrix-path assumptions. No internal audit or extension of their constants is undertaken. |

The accepted cap and depth-one flap families remain closed checkpoints.
This contribution does not classify extremal maps or run an adversarial
search. R4's deformation/classification ownership and R7's counterexample
ownership are preserved. The full R3 sign problem remains open: angular
remapping, signed factors, arbitrary direction-and-radius dependence, and
merely finite-sample contraction are not covered.

The main proof uses no unresolved team conjecture, numerical sign, or
finite atomic reduction. Its external theorem dependencies are exactly the
two named primary transfer results. Earlier team sources above supply
comparisons, credit and the explicitly marked composition observation.

The final refresh also incorporated R4's
[parity alignment](../gaussian_parity_alignment/PROOF.md), graph 6396,
`bafkreicuhkfttm4ixgn55hupyfhfj6tqvfsxjy6qnkjc7zb5umisbfnke4`.
That all-variance result requires equal weights within each even-sign orbit
and allows one radius per orbit for the ball statements. It signs balanced
laws on the earlier eight-site obstruction; it does not remove the
arbitrary-prior problem there. Our nonnegative ray theorem instead makes
no orbit or weight assumption and permits individual radii. Neither
theorem is claimed to contain the other. R3's extended prior cell,
R7's accepted finite-atomic low-noise exclusion, R1's equality-contact
observation and R8's Jackson reconstruction were also inspected; none is
a sign premise of this proof.

## Reproduction and trust boundary

Run, from the repository root, with standard-library CPython 3.11.2:

```sh
python3 probability/gaussian_angular_ray_contractions/check.py --check
python3 -O probability/gaussian_angular_ray_contractions/check.py --check
```

Both print:

```text
AUTHOR_CHECKS_PASS: identities, angular example, rational motions, rejected invalid inputs
```

Without `--check`, the canonical JSON output must match EXPECTED.json.
The exact sparse-polynomial calculation checks the generic derivative
factorization, norm identity, lowering derivative, shear determinant, and
opposite one-sided scalar-defect sum. It rejects a changed derivative sign.
Fractions also verify every pair of the eight-site control, its rank-six
determinant, the differential Lipschitz reserve, 97 admissible rational
motion cases (including zero and unit factors), the invalid full-cone
control, and the comparison with the classical interpolation.

The continuum quantifiers, geometric regularity, Gaussian cancellation,
ball-volume transfer and global scope comparisons rest on the written
proof and the cited theorems. A finite rational grid is not a proof of the
continuum motion. This is author verification, not an independent checker
or proof-assistant formalization. There is no floating-point sign, external
dataset, solver, omitted large certificate or private input. SHA256SUMS
records all other files in this directory.
