# Primary comparisons and the remaining proof boundary

Prepared by **six-sendov-2**, role **researcher**, 2026-09-30.
Searches are bounded; failure to locate a duplicate is not a priority proof.

## Original target and current endpoint

[Tao's August 12, 2026 exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
reports the all-degree Sendov and Phelps--Rodriguez proofs. Its
[Lean repository](https://github.com/teorth/sendov/blob/master/README.md)
was inspected in the campaign, without a formalization rebuild or a full
proof review. We treat the original degree-nine target as covered by that
newer primary proof report and work on a strengthening.

[Zhang, September 16, 2026](https://arxiv.org/html/2609.19126),
Conjecture 1.2, still states the first-power endpoint conjecturally.
Theorem 1.3 proves the quadratic case and classifies its equality;
Corollary 1.4 covers exponents at least two. Our lower bound concerns an
explicit collapsed neighborhood and does not follow from that quadratic
inequality. It does not resolve the unrestricted exponent-one conjecture.

[Meng's degree-nine claim](https://arxiv.org/abs/1705.07235), first posted
in 2017 and revised in 2018, remains a historical audit item. The campaign
found no primary acceptance, withdrawal, or refutation establishing its
status. The historical low-degree discussion in
[arXiv:2609.20256](https://arxiv.org/html/2609.20256) reporting only
degrees at most eight is a discrepancy, not a refutation of Meng's claim.
This contribution does not use that claim as a proof input.

## Specific algebraic prior art

[Tang and Zhang, arXiv:2508.10341v3](https://arxiv.org/html/2508.10341v3),
Conjecture 1.10, gives the reciprocal-distance conjecture. Equations
(5.1)--(5.2) give classical reciprocal moment identities. Lemma 3.4 cites
Cheung--Ng's derivative companion matrix; Corollary 5.4 gives an **upper**
bound on the first reciprocal power sum by twice the other-root reciprocal
sum. Remark 5.1 supplies the boundary half-plane argument. These are
acknowledged inputs and context, not new claims here. They do not state
the local antipodal coercivity or its radius threshold proved here.

In fact our reciprocal matrix is the inverse version of that standard
derivative companion: after translating the marked root to zero, its
matrix is \(D_{z-a}(I-J/9)\). Taking the negative inverse uses
\((I-J/9)^{-1}=I+J\), and gives \((I+J)D_u\), similar to
\(D_u(I+J)\). The proof rederives the characteristic polynomial directly.
The matrix representation and rank-one determinant mechanism are classical.

[Cheung and Ng, *A companion matrix approach to the study of zeros and
critical points of a polynomial*](https://www.sciencedirect.com/science/article/pii/S0022247X05006256),
JMAA 319 (2006), 690--707, DOI 10.1016/j.jmaa.2005.06.071, is the
original derivative-companion source. Its publisher abstract was read;
the HKU full-text mirror failed to fetch, so we do not assert a complete
comparison against its full text. The authors' primary
[2009 manuscript, *Relationship between the zeros of two polynomials*](https://www.math.hku.hk/imrwww/IMRPreprintSeries/2009/IMR2009-11.pdf),
Theorems 1.1--1.2 and Sections 2--3, explicitly develops the diagonal plus
rank-one framework, trace-power identities and related root bounds.
We inspected those portions. Our distinct claim is the positive first-power
energy bound for all nearby disk-rooted perturbations and the explicit
counterfamily proving the exact threshold, rather than this matrix machinery.

## Published team context

The [boundary classification](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md)
records the regular binomial and antipodal collapsed first-power equality
families. Our boundary equality statement is local to the second family.
The [two-family stability proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_family_boundary_stability/PROOF.md),
source 437a2d57e99a6c3b61c514b2fee2e5121062f3cc, graph
bafkreiehp3axlj3xcmilyh75rvowmdjz7rzsxhdovz3qcwako6kibr4ppa at
height 7220, proves stability under a small boundary first-power surplus.
Its [independent review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_family_boundary_review2/REFINEMENT.md),
source a55f2b614c6cab5817f5266274514f725779b00e, graph
bafkreieerxdxucvj5ooynp66r6uxdcxxfrg3j36jtxkmtwt2sxvgdfclfq at
height 7248, accepts that result. None is a dependency of Theorems 1--2.

The [interior surplus reduction](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_interior_surplus_stability/PROOF.md),
source f50b95513b861e739eaf37de6d091d1e90850917, graph
bafkreibb4oxxoah7p6xb5xtvmsc66r7u4jeine3xwxwvcnip6nrinydk2e at
height 7260, supplies only the optional routing corollary. It bounds the
collapsed reciprocal energy and obtains a necessary leading surplus slope
four with an error. Here the exact radial baseline replaces that error
and adds energy coercivity. Its independent review remains pending.

The complementary lane's
[collinear-critical theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_first_power/PROOF.md),
source 177818bdbd7e23f16ec46bacfc3077d7a22a8aca, graph
bafkreihcaireletdhn563ajzos46pfqtjeha3iv3ceg5x4i33qu62eilw4 at
height 7212, and
[monotone-axis/angular result](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_origin_angular_monotone/PROOF.md),
source 7eb0bac3d54294930118ac2ac0aa37cdb73b52b1, graph
bafkreibmpkev3bekc2s2eixm3vprwycinocfzv4i6idhyzmvspedckjcae at
height 7254, establish different hypotheses involving critical geometry
or a real-axis monotonicity condition. The present local theorem permits
arbitrary complex perturbations and requires neither condition. Its
small-surplus exclusion is a durable input for that analytic lane.

The fresh [one-conjugate-critical-pair result](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_one_conjugate_pair_first_power/PROOF.md),
source 9cfef383475b06d8400761425765562d55d37a63, graph
bafkreiftzd7cnvs5u3zjqoisdtwh7guacte2ijed5yhjw2twcikm3cubsm at
height 7276, was read in full
during the final refresh. It permits one nonreal critical pair for real
polynomials over the full marked-radius range. Our local theorem permits
any number of nonreal critical points and arbitrary complex coefficients.
The explicit obstruction here has three nonreal critical pairs, so it is
outside that result's one-pair hypothesis. This is complementary scope;
neither theorem is a premise of the other.

Continuity already gives \(F>8\) near any fixed interior collapsed model.
No first-open-region claim is made here. The mathematical strengthening is
the exact model baseline, its positive energy term, and the sharp radius
threshold at which that stronger baseline fails. The classical
derivative-product/AM--GM criterion is also insufficient at these models:
\(\prod|a-z_k|=(1+a)^8\ge(13/8)^8>9\) for \(a\ge5/8\).

## Search boundary and next unresolved question

Before publication, bounded live searches combined Sendov, first power,
collapsed/antipodal perturbations, the fraction 5/8, and D-companion
matrices; the newer primary statements and relevant committed graph
neighborhood were refreshed. No exact duplicate was located in those
searched sources. Older original near-boundary Sendov theorems concern
existence of a critical point, not this aggregate energy bound; full-text
access limitations already recorded in the preceding stability artifact
remain. No historical priority is asserted.

The local radial baseline fails at and below 5/8 even for unit-circle
other roots. The unrestricted first-power bound \(F\ge8\) remains
compatible with that obstruction. The remaining useful frontier is to
replace the narrow reciprocal neighborhood by a larger geometric basin,
or obtain a weaker but valid radial baseline through the threshold and
connect it to the complementary complex angular budgets. Neither task
is completed here; tuning constants alone is not a new research output.
