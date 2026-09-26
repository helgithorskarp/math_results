# Sources, dependencies, and review boundary for the effective supplement

The sole named problem is Aishwarya--Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2),
Conjecture 1.1 in dimension three. The present supplement does not prove
the missing sign or add a positive Kneser--Poulsen class.

## Classical geometric sources

- U. Brehm, [Extensions of distance reducing mappings to piecewise congruent
  mappings on R^m](https://link.springer.com/article/10.1007/BF01917587),
  Journal of Geometry 16 (1981), 187--193. The extension theorem and repair
  mechanism are classical, not discoveries of this packet.
- A. Petrunin and A. Yashinski,
  [Lectures on piecewise distance-preserving maps](https://arxiv.org/pdf/1405.6606),
  Lecture 2, especially the proof of Theorem 2.1 on printed pages 21--24;
  final remarks on printed page 47 state the all-dimensional extension.
  The star-shaped repair and the boundary blind zone are explicit there.
  Our bounded folding seed removes that boundary case before counting
  three-dimensional convex pieces. The universal count is written out
  in EFFECTIVE_BOUND.md instead of being attributed to the lectures.
- P. Osinenko, [A note on Brehm's extension theorem](https://arxiv.org/pdf/1609.00965),
  2016, treats constructive rational input in the planar case. This is
  relevant prior constructive work. Our rational three-dimensional cell
  and interval bookkeeping uses the explicit bisector reflection formula;
  no claim of first constructive extension is made.

The plane-arrangement recurrence, Euler edge bound, barycentric
subdivision, and rational polyhedral operations are elementary classical
ingredients proved or explained in the supplement. A bounded live search
for quantitative Brehm complexity, number of pieces, and rational extension
found the above related sources but no identical stated Gaussian
complexity-and-gap formula. This does not establish historical priority.

## Direct mathematical dependencies

- [Indecomposable reduction](PROOF.md), source commit
  `4518e569424cbac04083e6cb9497cc97991cf301`, graph
  `bafkreihtkvrmyjs4cswetyjge4rpwvppjunbtmd4tnrw3o65cwvfa5wyey`
  at height 6164. Its finite interval and saturated-chain argument turn
  the new mesh count into a witness count and gap bound. Original proof
  SHA256: `bc4eed76242de833971fa79bb28da984ed9e021262f852e2a3d24e320c0aa5ad`.
  [Review 2](../gaussian_indecomposable_contractions_review2/REVIEW.md),
  source commit `d853d267d429b0f502ccf9989d93a724f3b027d6`, accepts that
  qualitative theorem, not this supplement.
- [R3 paired-cubature frontier](../gaussian_prior_localization/CUBATURE_FRONTIER.md),
  reviewed source commit `cc561805eaf1e28f7138b5f71c8b37dbc9ce2a1a`, graph
  `bafkreia425hkp6pibvmb4dqein5ybdlxy4kkeywfmuqd3gd6mkptjll4rq`.
  Its [independent review](../gaussian_paired_cubature_review2/REVIEW.md)
  accepts the near-cubic atom bound and defect error. It is a premise
  only of the support-independent composition in EFFECTIVE_HANDOFF.md,
  not of the N-point geometric bound itself.

## Coordination context, not new sign premises

The current refresh read the seven other researchers' latest completed
reports and new repository source. R7 accepts the
[orthocentric depth-one flap theorem](../gaussian_flap_selector_review_r7/REVIEW.md);
both finite templates are closed at that scope. R6 independently recovered
the motion and retained its controls privately without duplicate publication.
The present effective count does not reopen or extend the flap family.

R2's [endpoint scatter obstruction](../gaussian_beta_endpoint_scatter_obstruction/PROOF.md)
rules out one positive Laplace representation on an actually positive
two-point contraction. R3's [direct hinge oracle](../gaussian_prior_localization/DIRECT_HINGE.md)
can certify a supplied rational finite instance but cannot inherit its
small-frontier budget on our enlarged configurations. The final refresh
also found R8's new [universal seven-factor author proof](../gaussian_seven_factor_kernel/PROOF.md):
b_(7,0) is no longer an unsigned obligation at author-proof level, while
independent review is pending. R1's local theorem and R5's fixed-atom/remainder
boundary retain their separate scope. None is a premise of this count or
is invoked to supply the full hinge sign.

## Evidence status

The supplement is an unformalized author proof with exact standard-library
Python controls. `effective_bound.py` uses Fraction/integer arithmetic and
does not import the earlier checker, any teammate's code, a solver, or
numerical quadrature. It reconstructs its local cone maps from four vertex
images and then compares them to the reflection formula. Matching those
controls is not independent mathematical review of the universal proof.

The original PROOF.md, verify.py, EXPECTED.json and SOURCES.md are unchanged.
No large artifact, external dataset, private state, or credential is needed.
