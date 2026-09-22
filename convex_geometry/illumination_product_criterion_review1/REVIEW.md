# Review: fractional criterion for universal illumination multiplicativity

## Verdict

**Accept, high confidence.** I independently checked the proof and the
source package at target commit
`1963aec794ff832654ed89c5ff1f12e507f1ea48`. The theorem is correct in its
stated domain: `P` is a full-dimensional, positive-dimensional polytope;
partners in the all-partner statement are positive-dimensional convex
bodies; and the power-limit assertion is only made for `P`.

The target does not claim a solution of the general illumination conjecture,
a classification of all zero-gap polytopes, a nonpolytopal power theorem, or
priority for the pentagon product failure. Its novelty statement is expressly
search-relative. Those scope restrictions are material to this verdict.

## Claim alignment

The proof establishes all of the following claims actually stated by the
target:

1. `I_f(P)=I(P)` if and only if `P` multiplies ordinary illumination with
   every positive-dimensional convex-body partner.
2. It is equivalent to multiplication with every polytope, to equality on
   every Cartesian power, and to equality on arbitrarily large powers.
3. For `tau=I_f(P)` and `v=|V(P)|`,
   `tau^r <= I(P^r) <= floor(tau^r r log v)+1` and
   `I(P^r)^(1/r) -> tau`.
4. The wholly rational upper bound
   `ceil(tau^r)(1+r ceil(log_2 v))` eventually certifies a strict power when
   `tau<I(P)`.
5. `I(P x K) >= ceil(I_f(P)I(K))` for arbitrary convex bodies `K`, and
   `I_f(P x Q)=I_f(P)I_f(Q)` for polytopes.
6. The displayed rational pentagon has `I=3`, `I_f=5/2`, and square
   illumination number eight.

## Human premises and completeness reductions

I treated the following as separate proof obligations rather than relying on
agreement between programs.

1. **Definitions and domain.** Illumination uses a nonzero direction and a
   positive time entering the interior. Full dimensionality makes the strict
   facet test valid in the ambient factor spaces.
2. **Vertex test.** At a vertex, a direction illuminates exactly when it has
   negative dot product with every active outer facet normal. Inactive
   inequalities remain strict for a sufficiently small step.
3. **Boundary-to-vertex completeness.** A vertex of the minimal face of a
   boundary point has every facet active at that point. Hence a direction
   illuminating that vertex also illuminates the point. Vertex coverage is
   therefore neither an undercount nor merely a necessary condition.
4. **Finite incidence completeness.** Only finitely many illuminated subsets
   of the finite vertex set occur. Selecting one direction per nonempty class
   preserves integral coverage.
5. **Measure reduction.** Each incidence class is Borel because it is defined
   by finitely many strict linear inequalities. Moving all measure in a class
   to a representative preserves every vertex load, so no infinite-dimensional
   LP assertion is smuggled in.
6. **Finite LP premise.** The fractional optimum is attained and rational;
   ordinary finite LP duality supplies a rational vertex-weight certificate
   with the same objective.
7. **Nondegenerate rounding domain.** Two generic opposite extreme vertices
   cannot share an illuminating direction, giving `tau>=2`; thus the later
   estimates using `T>1` apply.
8. **Common product time.** If the two components enter their interiors at
   possibly different times, convexity makes every sufficiently small positive
   time work in both. Product illumination is therefore componentwise.
9. **Product boundary upper bound.** Factor covers illuminate every product
   boundary point, including the cases where one coordinate is interior;
   openness keeps that coordinate interior for a small common time.
10. **Arbitrary-partner fiber bound.** For a fixed vertex `p` of `P`, the
    second components paired with directions illuminating `p` illuminate all
    of `K`. There must be at least `I(K)` such indices. Rescaling their first
    components gives a valid fractional cover of `P` and proves the mixed
    lower bound without assuming `K` is a polytope.
11. **Product-class completeness for polytopes.** At vertex pairs, every
    nonempty incidence class is the rectangle `E x F`; zero components create
    no useful additional class.
12. **Fractional product equality.** Tensoring optimal primal weights gives
    the upper bound and tensoring optimal dual vertex weights gives the same
    lower bound. This proves equality, not just submultiplicativity.
13. **Power lower bound.** Iterating the exact fractional product formula and
    using integer cover number at least fractional cover number yields
    `I(P^r)>=tau^r`.
14. **Greedy completeness.** Weighted double counting guarantees a set
    covering at least a `1/T` fraction of the currently uncovered elements.
    The recurrence leaves fewer than one after more than `T log N` choices,
    hence leaves none.
15. **Power substitution.** The product model has `N=v^r` ground elements and
    a tensor fractional cover of mass `T=tau^r`, yielding the stated integer
    upper bound.
16. **Limit passage.** The lower and upper bounds have the same `r`th-root
    limit. The polynomial factor in `r` contributes a root tending to one.
17. **Rational block estimate.** With `q=ceil(T)`, Bernoulli's inequality makes
    each `q`-step block reduce the remaining bound by strictly more than a
    factor of two. The stated number of blocks beats `v^r`.
18. **Finite failure exponent.** Because `tau/I(P)<1`, the rational bound
    divided by `I(P)^r` tends to zero; an integer search must eventually halt.
19. **Equivalence chain.** The all-body statement implies the all-polytope
    statement; induction gives all powers; an unbounded equality subsequence,
    combined with the full root limit, forces `tau=I(P)`.
20. **Failure-pair qualification.** An arbitrary strict power need not make
    its final successive factorization strict. The target correctly uses the
    least strict exponent when identifying a particular failing partner.
21. **Rational input certificate.** A rational perturbation can preserve all
    already strict negative inequalities and possibly add coverage. This is
    enough to dominate the original incidence class in optimization and
    greedy certificates.
22. **Pentagon completeness.** Exact facet inequalities show that the maximal
    illuminated vertex subsets are precisely the five adjacent pairs. Three
    cover the cycle, half-weighting all five is primal-dual optimal, and the
    eight displayed product rectangles cover all 25 vertex pairs.
23. **Literature boundary.** Fractional illumination, product failure, the
    regular-pentagon square value, finite LP duality, and greedy set-cover
    rounding are treated as prior ingredients. The unavailable 2007 full text
    prevents a definitive historical-priority verdict for the precise
    all-partner equivalence.

All mathematical premises above were checked directly in the written proof.
The only imported mathematical result that does real logical work is standard
finite-dimensional LP duality; the greedy estimate is proved in the note.

## Independent adversarial computation

The independent checker imports no target code or output and uses exact
`Fraction` arithmetic throughout. It performs the following tests:

- It enumerates all `2^15-1` nonempty families of nonempty subsets of four
  labelled points, retaining exactly 32,297 covering families and reducing
  them to all 114 distinct maximal covering clutters.
- It solves both primal and dual fractional-cover LPs by independent exact
  vertex enumeration and solves integral cover by a branch-on-an-uncovered-
  element recurrence. All 114 primal and dual objectives agree.
- It builds and checks all ordered pairs of the 114 clutters, i.e. 12,996
  product clutters on 16 points. Tensor certificates are checked constraint by
  constraint. Every one of the 12,635 products having at least one zero-gap
  factor has the predicted multiplicative integer value; 225 products are
  strictly submultiplicative.
- The smallest boundary/adversarial systems include a one-class cover
  (`tau=I=1`, confirming why the geometric `tau>=2` premise matters), four
  disjoint singletons (`tau=I=4`), the even cycle `C4` (`tau=I=2`), the odd
  cycle `C5` (`tau=5/2<I=3`), and the Fano lines (`tau=7/3<I=3`, exercising
  denominator three rather than just half-integrality).
- Six exact block-decay cases include `T=2`, the pentagon and Fano values,
  their powers, and `T=2001/1000`, which probes a value barely above the
  `T>1` boundary. Every claimed strict halving and coverage inequality holds.
- For the rational pentagon, the checker derives outer normals from the
  vertices and solves every pair and triple of vertex constraints through
  four exact `L1`-normalized quadrant intervals. Exactly the five adjacent
  pairs are feasible and no triple is feasible. It independently checks the
  five representative directions, all 25 product vertices, the eight-set
  cover, and a nonempty hole after deleting each displayed rectangle.

Normal and `python3 -O` runs produce identical output. The manifest and
frozen result file make later source drift detectable. This computation
strongly corroborates premises 6, 11, 12, 14, 17, and 22, but it does not by
itself prove the geometric completeness premises 2--5 or the unrestricted
fiber argument in premise 10.

## Source and integrity audit

The target's seven files match its recorded manifest and both its ordinary and
optimized verification runs pass with result digest
`5f29ec7df3a23b7045798c39aa50d5de284515d70fec69403dea07c177d90d3d`.
Its code uses only the Python standard library and exact rational/integer
arithmetic. The independent checker intentionally uses a larger finite test
space and a different geometric feasibility method.

The official 2006 Baladze--Boltyanski PDF resolves and is consistent with the
target's attribution of direct-sum multiplicativity conditions and the
pentagon mechanism. Naszódi's publisher record confirms the 2009 fractional-
illumination paper. The current Rotem--Schejter--Slomka paper and arXiv source
resolve and provide contemporary product/fractional context. The target
plainly records that the 2007 Boltyanski--Martini full text was unavailable;
the review therefore makes no independent novelty claim.

## Strengthening and improvement opportunities

1. In the paragraph on rational input, replace “has a rational representative
   as far as its illuminated set is concerned” with “has a rational direction
   whose illuminated set contains it.” The following sentence already admits
   that perturbation may add coverage, and domination is exactly what the
   optimization argument needs. This is a wording improvement, not a gap.
2. It would help readers to isolate the common-small-time observation in a
   named lemma because it supports both product-class factorization and the
   boundary-cover upper bound.
3. Say explicitly that `log` in the analytic bound is the natural logarithm.
   The proof via `exp(-m/T)` makes this clear, but an upfront convention would
   remove a minor ambiguity.
4. Historical priority of the exact all-partner criterion should remain
   qualified until the 2007 direct-vector-sums paper is audited in full. This
   caveat affects novelty assessment, not correctness.

No requested change is corrective, and none lowers the verdict.
