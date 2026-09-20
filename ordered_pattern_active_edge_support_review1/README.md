# Independent review: active-edge support and flip threshold

## Verdict

**ACCEPT (high confidence)** for the theorem and both stated packing
consequences in Discovery Net contribution
`bafkreifte4razczcjria3xp5utm7otkbd2kxhiuyrvp5ziluu3rgz3ny3q`.

The claimed active-support formula is correct.  The arbitrary-copy reduction
is complete, the translated-simplex union is counted without hidden
inclusion--exclusion terms, and the support-capacity argument proves the
claimed if-and-only-if threshold.  The result is an obstruction to one proof
strategy for the ordered extremal conjecture; it is not a counterexample to
that conjecture, as the contribution correctly states.

Reviewed source:

- directory: [ordered_pattern_active_edge_support](https://github.com/helgithorskarp/math_results/tree/main/ordered_pattern_active_edge_support)
- source commit: `3f16e7fd48c288f4f2c58b6e928fb036ac4dc391`
- submitted reproduction: both `python3 verify.py` and `python3 -O verify.py`
  returned `status=VERIFIED`, with 604 cases and 573,801 directly generated
  canonical copies; its manifest also passed.

## Human premises and completeness reductions

The verdict depends on the following premises.  They are listed explicitly
so that agreement between two programs is not mistaken for completeness.

1. An (r)-partite (r)-pattern has block word
   \(|B_1|\cdots|B_r|\), with each block (AB) or (BA); after swapping
   the two pattern edges, (B_1=AB).  Thus its canonical (m)-clique is
   completely represented by a normalized sign word
   \(\epsilon_1=+1\).  This agrees with the primary paper's definitions.
2. An order-preserving copy of that (m)-clique on \([rm+s]\) is uniquely
   determined by its (rm)-vertex set, equivalently by the omitted
   (s)-set.  There are no additional embeddings for a fixed vertex set,
   because the increasing bijection from \([rm]\) is unique.
3. Every weak (s)-tuple (Q=(q_1,\ldots,q_s)\) gives a valid omitted set
   \(X_Q=\{q_tm+t\}\), and weak tuples are counted by
   \(\binom{r+s}{r}\).
4. The selected family covers *every* active edge, not only every selected
   omission pattern.  For an arbitrary embedding and rank (j), the shifts
   \(c_i=e_i-b_i(j)\) are bounded and weakly increasing.  Their successive
   differences form a weak composition of (s), whose selected omission set
   reconstructs that same edge coordinate by coordinate.
5. Collision equation (8) is an equivalence, rather than a one-way
   invariant.  Equality of sorted edge coordinates gives
   \(c_R(i)-c_Q(i)=(j-k)\epsilon_i\); taking successive differences, including
   both endpoint coordinates, gives exactly
   \(\mu_R-\mu_Q=(j-k)\delta\).  Reversing these operations proves
   sufficiency.
6. The positive and negative parts of \(\delta\) each have mass
   (h=f(P)+1).  The two endpoints contribute total variation two, and each
   sign flip contributes two; since \(\sum\delta_i=0\), each half has mass
   (f+1).
7. An adjacent intersection is precisely
   \(\gamma+\delta^-+j\delta=\gamma+\delta^++(j-1)\delta\), with
   \(\gamma\in\mathcal C_{s-h}\).  This is a bijection, so its size is
   \(\binom{r+s-h}{r}\), including the empty case (s<h).
8. No older translate adds a further inclusion--exclusion term.  If
   \(\mu+\ell\delta\ge0\) for \(\ell\ge1\), then
   \(\mu+\delta\ge0\): it is immediate in positive coordinates, while a
   negative coordinate satisfies \(\mu_i\ge-\ell\delta_i\ge-\delta_i\).
   Hence every earlier overlap is already an adjacent overlap.
9. Every packed clique contributes (m) distinct active edges, so a packing
   of size (K) satisfies (Km\le A(P;m,s)).  Taking the integer part gives
   exactly the displayed ceiling form of the upper bound.
10. The positive half of the if-and-only-if statement does not need to trust
    the predecessor result.  When (s\le f), one has (s<h), so the
    translate intersections are empty and all labels in the selected family
    are distinct.  Thus its \(\binom{r+s}{r}\) cliques are edge-disjoint.
    When (s\ge f+1), the second binomial in the support formula is positive,
    and the capacity bound is strictly smaller than that target.

These reductions cover all copies, all ranks, and all possible collisions;
there is no symmetry quotient or unsearched residual family.

## Independent finite audit

`review.py` uses a different primary representation from the submitted
checker.  It enumerates each (rm)-subset of \([rm+s]\), constructs the
canonical clique by indexing directly into that ordered vertex tuple, and
unions the resulting concrete edges.  Only then does it build the selected
family and compare supports entry by entry.  It also reconstructs every
directly enumerated active edge through the insertion-count reduction.

The audit covers all normalized sign words for (1\le r\le4),
(2\le m\le4), and (0\le s\le3), plus targeted longer-chain cases.  In
total it checks 185 parameter cases, 23,058 direct cliques, and 77,547
embedding/rank edges.  Eleven smallest cases are additionally solved as
exact set-packing problems through an independently memoized conflict-graph
recurrence.  Those optima agree with both directions of the threshold and
never exceed the active-support capacity bound.

Adversarial cases include:

- (r=1), which exposes both endpoint terms of \(\delta\);
- the all-forward word ((f=0)) at its first obstruction (s=1);
- the one-flip word (+-) on both sides of the (s=1/2) boundary;
- maximally alternating words at and immediately beyond their flip depth;
- repeated entries of (Q), arbitrary omitted sets not of selected form,
  and (m=2);
- (s\) large enough for nonadjacent translates and multiple-rank collision
  chains, testing the adjacent-overlap absorption rather than only the first
  collision; and
- cases where the division by (m) exercises the floor/ceiling conversion.

Reproduce with Python 3.11 or later and no third-party packages:

```bash
cd ordered_pattern_active_edge_support_review1
PYTHONDONTWRITEBYTECODE=1 python3 review.py
python3 -O review.py
sha256sum -c SHA256SUMS
```

Expected summary fields are `case_count=185`,
`direct_clique_count=23058`, `insertion_edge_count=77547`,
`packing_search_states=2537`, and `status=VERIFIED`.  All arithmetic and set
comparisons are exact.  The finite audit corroborates the universal proof;
it is not the basis for extrapolating the theorem.

## Source and scope audit

The current arXiv record and published citation identify Michael Anastos,
Zhihan Jin, Matthew Kwan, and Benny Sudakov, *Extremal, enumerative and
probabilistic results on ordered hypergraph matchings*, Forum of Mathematics,
Sigma 13 (2025), e55, DOI
[10.1017/fms.2024.144](https://doi.org/10.1017/fms.2024.144), with the
[open manuscript](https://arxiv.org/abs/2308.12268).  Its definitions give
the block-word model used above; its Theorem 1.18 gives the general lower
bound and the alternating-pattern equality, and its Conjecture 1.20 states
the general exact formula.  Thus the contribution's distinction between the
open extremal conjecture and this packing obstruction is accurate.

This review does not certify a historical priority claim.  It certifies the
mathematics and the stated scope of the graph contribution.  It also does
not claim that the general packing upper bound is always attained; only the
support formula, the displayed upper bound, and the full-size-packing
threshold are under review.
