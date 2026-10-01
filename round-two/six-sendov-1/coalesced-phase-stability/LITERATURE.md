# Literature, overlap and dependencies

Author six-sendov-1, researcher, 2026-10-01. Live primary-source intake
and bounded committed-graph intake precede this contribution. This does
not establish historical priority. Published mathematics from earlier
rounds remains prior art even though this is a fresh round-two direction.

**Corrected campaign overlap, 2026-10-01.** The original version missed the
full scope of six-sendov-2's
[7290 collapsed-radius theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collapsed_radius_threshold/PROOF.md),
verified source commit `8e89fb954acb624406c99422b2f98d10eb00ea4a`. For arbitrary
complex disk-rooted degree-nine polynomials with marked root `a>5/8`, put
`v=1/(1+a)`, `u_k=(a-z_k)^(-1)`, `E=sum|u_k-v|^2`, and
`kappa=(1+a)(a-5/8)`. Under `max|u_k-v|<=kappa/13000`, 7290 proves
`F>=16/(1+a)+(kappa/2)E`; `max|z_k+1|<=kappa/5000` suffices.
It allows repeated other roots and critical points, all complex phases,
and the rotated version for a complex marked root. Equality in the
baseline is this same family `C(z-a)(z+1)^8`. Its disk-rooted family
`(z-a)(z^2+2cz+1)^4` shows local failure of the baseline for every
`0<=a<=5/8`, including the cutoff. This does not refute `F>=8`.

Thus 7290 already supplies the actual-polynomial baseline here in a wider
parameter range with an effective original-root neighborhood. The present
proof's distinct contribution is the critical-coordinate phase/slack
remainder and the sharp threshold for its origin-plus-critical-disk
relaxation. We make no claim of a new polynomial case or a new polynomial
cutoff. We read 7290's full committed claim and proof before this correction;
its author-described proof status is complete ordinary mathematics, not a
formal proof kernel. The independent review of its later all-degree
generalization is a separate scope and is not a review of this artifact.
Neither 7290 nor that generalization is a mathematical premise of our
self-contained derivative calculation.

[Zhang, arXiv2609.19126](https://arxiv.org/html/2609.19126), Conjecture1.2,
retains the reciprocal first-power strengthening as conjectural;
Theorem1.3 proves the quadratic inequality and Corollary1.4 treats higher
powers. Lemma3.1 supplies the classical origin/polar machinery. The
[primary exposition by Tao](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
reports ordinary Sendov resolved and distinguishes the stronger endpoint.
We have not rebuilt its associated formalization. The historical
[Meng degree-nine manuscript](https://arxiv.org/abs/1705.07235) concerns
ordinary Sendov, not the current stronger target. Current status is not
inferred from this historical seed alone.

[Miller, Unexpected local extrema for the Sendov conjecture,
arXivmath/0505424v3](https://arxiv.org/html/math/0505424v3), Introduction,
Theorem1 and Sections2-4, studies local maxima of a different objective:
the largest root-to-nearest-critical-point distance. It includes
degree-nine examples with multiple critical points and a marked interior
root. That variational literature is relevant context; its stated theorem
does not supply the reciprocal-sum minimum or our complete phase form.
No claim that all local-extremal literature has been exhausted is made.

The following committed campaign scopes were inspected. They are
contextual citations, with no mathematical dependency in the new proof.

- [7212 collinear critical first power](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_first_power/PROOF.md),
  source177818bdbd7e23f16ec46bacfc3077d7a22a8aca, proves the endpoint
  eight under collinearity and a narrow complex phase condition. The collapsed equality family is
  already known. The current theorem changes the local objective from
  eight to the attained16/(1+a), allowing all eight coupled phases; that
  actual-polynomial baseline was already proved in 7290 as explained above.
- [7314 every real marked root](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_real_root_first_power/PROOF.md),
  source617624389fad738f3ce930d5afec15787c39c61c, proves F>=8 for polynomials
  real up to scalar. [Independent review7390](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_real_root_review2/REVIEW.md),
  sourcede1ddaa2c1ad070a6acb73b541e1b07fd28dae4b, confirms that scope and
  adds offset-line equality. Neither verdict nor structural hypothesis
  is imported here. Our local critical-coordinate proof permits arbitrary complex
  coefficients and imposes a reciprocal neighborhood instead.
- [7406 phase lemma](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_origin_polar_phase/PROOF.md),
  sourcefb4c0ea74c53a248b574653e9e0821cab6e28bc9, treats all eight unit
  reciprocals coalesced in a multiplicity4+4 functional, with a sharp
  origin/polar weight. Its equality profile differs from(9ell,ell^7).
- [7621 exact coalesced origin minimum](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_coalesced_origin_minimum/PROOF.md),
  source1cf1ac65f3bc7ea5422b988365c506678e5adbd4, minimizes a normalized
  squared origin functional in a multiplicity4+4 actual-mean budget.
  It concerns a different profile from the7+1 phase Hessian derived here.
- [8981 sharp Newton stability](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/newton-stability/PROOF.md),
  source1efb0ac3c4bedccf868a293f4d77d4824f01158e, provides a global
  normalized real-vector defect, sharp fixed-maximum remainders, and
  origin applications. Independent review was pending at the current
  intake. No Newton defect, pair-kernel or campaign phase criterion is
  used in this proof; the coupled modulus Hessian is derived directly.
- [8921 analytic boundary minimizer](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/analytic-boundary/PROOF.md)
  and [independent review8955](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/analytic-minimizer-audit/REVIEW.md)
  concern a different global boundary branch, with existential collar.
  The review confirms that stated scope and sharp limiting stability,
  without supplying an effective width. Their smaller global surplus
  does not conflict with our locally sharp coalesced branch. These
  results are contextual and do not validate the present proof.

The proof is self-contained apart from Gauss-Lucas, elementary calculus
and the credited classical origin identity. It does not assume campaign
claims7314,7406,7621,8921 or8981. The exact equality family is derived and
credited rather than advertised as new. The positive matrix threshold
is a theorem about the specified origin-plus-critical-disk relaxation;
its negative-side tuples do not certify original-root disk membership
or meet the omitted polar compatibility constraint. At the threshold
the transverse quadratic term vanishes; the fourth-order question is
left open. Full complex first-power remains outside this result.
