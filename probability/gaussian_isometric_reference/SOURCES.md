# Attribution and dependency boundary

The sole problem source is Aishwarya--Li's full Gaussian-majorisation
question in dimension three. This packet gives an analytic dependency
toward its common-set formulation. It is not a resolution of that question
or a new Kneser--Poulsen class. All new arguments are author proofs awaiting
independent review. No historical priority claim is made.

## Primary literature

* Gautam Aishwarya and Dongbin Li,
  [Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
  Conjecture, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
  The full majorisation question, density-value coupling, and geometric
  consequences motivate the campaign. The present proof uses no asserted
  three-dimensional sign from that paper.
* Gautam Aishwarya, Irfan Alam, Dongbin Li, Sergii Myroshnychenko and
  Oscar Zatarain-Vera,
  [Entropic exercises around the Kneser--Poulsen conjecture,
  arXiv:2210.12842v2](https://arxiv.org/pdf/2210.12842).
  Theorem 2.4 and its proof on page 10 already give pointwise transfer for
  centered balls under arbitrary contractions, using radial monotonicity
  of ball probabilities. Thus the singleton-reference transfer in this
  packet is a known case. Our issue is a general isometric reference and
  the complete zero-minimizer classification, including zero pointwise
  slack. No priority is claimed for Gaussian radial monotonicity.
* Alexander Yu. Solynin,
  [Continuous symmetrization via polarization,
  arXiv:1102.1004](https://arxiv.org/pdf/1102.1004).
  Section 3, Definition 3.2 gives the classical two-point polarization
  operation for an affine halfspace. The background includes Brock--Solynin,
  Trans. Amer. Math. Soc. 352 (2000), 1759--1796. Reflection pairing is a
  classical tool; equations (5)--(6) in our proof are proved directly.
  We do not use a continuous-symmetrization theorem.

These primary sources and the relevant committed graph neighborhood were
checked on 26 September 2026. The ball case, the polarization method,
stationarity under translations, and zero pair-distortion rigidity are
credited ingredients, not independently claimed inventions.

## Durable team inputs

| Source | Precise use | Verified input commit |
|---|---|---|
| [Common-set minimax theorem](../gaussian_prior_localization/PROOF.md) | Supplies the full-question formulation and its arbitrary-set quantifier. Our special value and dual maximizer are proved directly, without a minimax interchange. | `541d4b7de3d73b41444e5350378a8ecc43d914ea` |
| [Isometric faces](../gaussian_majorisation_minimax_faces/PROOF.md) | Theorem 1 is the incoming positive transfer mechanism. We remove its dual-cone and orthogonal-splitting restrictions and add the full zero-minimizer classification. Its finite face enumeration and sharp reserve are neither repeated nor claimed here. | `e53ad777d2aaa0556e646d4db44a2afc7235c7d0` |
| [Global coupling and moment criterion](../gaussian_majorisation_global_criterion/PROOF.md) | Full-question context: the zero endpoint defect remains unproved for arbitrary contraction data. This packet supplies special common-set signs, not that coupling. | `713e542a0bd389681a3fb4ee0c0b61a4f272f104` |
| [Fixed-atom reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md) | A reference satisfying a specified atom mass remains an admissible zero minimizer. This fact does not establish the comparison for every actual prior with that atom mass. | `138993ba3ec2efde720c789a2a3d887c9c417c69` |
| [Gaussian contraction rigidity](../gaussian_contraction_rigidity/PROOF.md) | Earlier use of weighted zero distance loss and Euclidean extension. The present weighted argument is reproved in equations (13)--(16); no entropy bound or claimed entropy-to-hinge inference is used. | `33bb5788b6ecf84a706fbd3eea99cf336f23e25b` |
| [Gaussian Markov intertwining](../gaussian_markov_intertwining/PROOF.md) | Concurrent boundary: a positive channel taking a fixed-covariance Gaussian location family on an open convex mean set to Gaussians of fixed covariance has affine means. Our reference-dependent target set is not such a channel. This is context, not a proof premise. | `b001598e004ba85c0934a5070f031d56c550a717` |
| [Indecomposable finite contractions](../gaussian_indecomposable_contractions/PROOF.md) | Concurrent full-question reduction fixing a tetrahedron. A reference positive on those four fixed vertices has q(x)=0 exactly at fixed points, giving a strict reference-test boundary when the actual prior charges moved sites. The arbitrary-set sign and all-weights comparison remain open. | `4518e569424cbac04083e6cb9497cc97991cf301` |

Relevant committed identifiers are common-set `6122`, isometric faces `6142`,
global criterion `6088`, fixed-atom reduction `6112`, and early rigidity
`5610`. These heights locate the inputs; acceptance of the present proof
is not inferred from acceptance or publication of an earlier result.

The direct consumer obligation is now precise: an arbitrary-set sign proof
must extend beyond isometric-reference superlevel tests. Within those tests,
an exact zero minimizer must be jointly isometric with its reference and
share its maximizing source set. A first variation that only checks q=0
misses the translation condition. The finite and measure lanes can use
this distinction for equality controls without assuming atomic minimizers.

The current geometric classes retain their own domain, weight and motion
hypotheses. They are not premises here and are not expanded by this result.
The functional lane's uniform moment budget, the evolution lane's contact
sign, and the counterexample lane's integrated numerical sign have separate
owners. No rate, finite-degree certificate or new numerical search is added.

## Review and reproduction

Read [PROOF.md](PROOF.md). The central review obligations are strictness of
the affine-bisector transfer at every positive level; positivity of the
transverse coefficient including r=0 and dim(V)=1; the sign in translation
stationarity; and the use of the same positive weight at both endpoints
in (16). The cases V={0}, singleton references, diffuse laws, and coincident
target points are explicitly included.

There is no program claimed to verify the universal theorem. The only
command, `sha256sum -c SHA256SUMS`, checks the three text sources. No runtime
dependency, dataset, certificate, or large output is omitted. A clean manual
audit of equations (6), (10), (14) and (16) is still an author audit, not
independent mathematical acceptance.
