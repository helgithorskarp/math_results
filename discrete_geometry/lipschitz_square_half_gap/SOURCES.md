# Sources, alignment and novelty boundary

Primary literature checked on 2026-09-22 after graph-first selection.

1. **Ludovic Rifford**, *A quantitative version of Tao's result on the
   Toeplitz Square Peg Problem*, arXiv:2106.01914v2.
   [Full primary manuscript](https://arxiv.org/pdf/2106.01914).
   Theorem 1.1 gives a universal constant times the maximum branch gap;
   the discussion on PDF page 5 records 0.018 from the proof and suggests
   the optimal value 0.5. Footnote 5 observes that a larger constant is
   impossible. We attribute both the quantitative target and this prior
   sharpness observation to Rifford. Our explicit exact witness is not a
   claim that the upper restriction on the optimal constant was unknown.
   Lemma 4.1, equations (4.3)--(4.4), at delta=0, already proves the
   two-sided local integral bound used here: subtracting (a²−b²)/2
   gives exactly b²≤J≤a². Equation (4.5) is the chord envelope used in
   our rederivation. None of those inequalities is claimed new.

2. **Joshua Evan Greene and Andrew Lobb**, *Square pegs between two
   graphs*, [arXiv:2407.07798v1](https://arxiv.org/html/2407.07798v1).
   Exact dependencies: Theorem 1.1 (spectrality and spectral properties),
   Proposition 1.3 (nested elegant PL comparison), Section 3.4
   (Definitions 3.8–3.12, Lemma 3.13 and Proposition 3.14 for PL curves
   and continuity), and Lemma 4.1 (elegance for the two-graph class).
   The proof of Proposition 1.3 explicitly uses action spectrality for
   PL curves, including nonisolated inscription components. Proposition
   4.2 and its following no-shrinkout argument explain the nondegenerate
   limit when both endpoints of the action interval are avoided.
   Their Lemma 4.3 uses an interior diamond and expanding graph domains
   for qualitative existence. That geometric comparison strategy is
   also prior art. Our proof checks the same construction for a prescribed
   strictly interior diamond, uses the maximum-gap scale, and identifies
   Rifford's integral with the correctly normalized spectral action.

   The [publisher's current record](https://ems.press/journals/cmh/articles/14299791)
   reports *Commentarii Mathematici Helvetici*, online 2026-06-02,
   DOI 10.4171/CMH/619. Its abstract was checked; the ordinary PDF
   download redirects to the subscription-required article page.
   Mathematical alignment is with the complete accessible arXiv
   version, not an uninspected journal revision. No priority claim is
   inferred from that access limitation. The [author-hosted manuscript](https://maths.dur.ac.uk/users/andrew.lobb/union_of_two_curves.pdf)
   was also inspected: its 28-page version has the same comparison
   construction and states the qualitative existence theorem. It was
   not represented as a verified copy of the final journal version.

3. **Joshua Evan Greene and Andrew Lobb**, *Floer homology and square
   pegs*, [arXiv:2404.05179v2](https://arxiv.org/html/2404.05179v2).
   Sections 2.2 and 3 define the preferred diagonal-avoiding capping,
   Hamiltonian H(z,w)=|z−w|²/4, and action. Section 3's elegant-rectangle
   calculation is the underlying geometric interpretation. Our proof
   derives the exact alternating-arc formula, including its additive
   constant, for the labeling needed here.

4. **Terence Tao**, *An integration approach to the Toeplitz square peg
   problem*, [arXiv:1611.07441](https://arxiv.org/abs/1611.07441),
   *Forum of Mathematics, Sigma* 5 (2017), e30.
   Square existence for two graphs of Lipschitz constant below one and
   the conserved square-area identity are prior. The present proof
   does not claim a new existence theorem without a metric conclusion.

## Graph and source predecessors

The graph source is the Toeplitz problem
`bafkreihwlwx62hnzcang2ct3mncgdomlao32kblxqmgqimxjvtgwwe6mhy`.
The inspected local predecessors are:

- [Sharp affine-branch bound](https://github.com/helgithorskarp/math_results/tree/main/discrete_geometry/affine_branch_square_size),
  graph `bafkreigr753i3nrnnsnvddpteqv3ddszncrwrx4y23ojwkudrel5rdq2dm`,
  source commit `2538cb79365caa81520e3fb7345dc7dc2a16330d`.
  Its stronger restricted constant 2/3 remains valid.
- [Maximum-gap localization obstruction](https://github.com/helgithorskarp/math_results/tree/main/discrete_geometry/square_peak_localization_obstruction),
  graph `bafkreibbzd4tmyuscmzj3wfw23zsu5ulqv7tlnev2w3oukyvvfm2s5rf3a`,
  source commit `0304625ef7389aea66942690ed14d7befdf6b22b`.
  Its independent accepted review at committed height 5434 was read.
  Our action proof does not require its disproved localization property.
  The self-contained rational elimination/polytope kernel is reused from
  this source, with attribution. Three old squares are normalization
  controls, not new findings.

## Claim boundary

The substantive conclusion is the full M/2 lower bound and its explicit
sharpness certificate. The spectral theory, diamond comparison
construction, Rifford's local integral inequalities, polygon enumeration
method, and original
half-gap question are prior. The proposed advance is their synthesis:
identify that integral as the local Floer action, start the established
comparison at the maximum-gap diamond scale, and deduce the full sharp
metric bound. Normalization and the prescribed-diamond hypotheses are
spelled out.

Bounded searches covered the primary Rifford and Greene–Lobb papers,
their current records, and quantitative square-size/half-gap terms.
No accessible source inspected stated the full sharp lower bound.
This is a search-relative novelty statement, not a historical-priority
certificate. The unavailable final journal version remains a comparison
limitation. The written universal proof is unformalized and has not
received independent review. The finite certificate trusts exact rational
arithmetic, Python, and the completeness reduction in PROOF.md Section 7.
