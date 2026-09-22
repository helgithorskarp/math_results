# Sources and status boundary

Checked on 2026-09-22.

1. Bogdan Dumitru and Mihai Nacu, *Alternating Extremes in Graceful
   Labelings of Full Binary Trees and Spider Trees*, arXiv:2607.12597v2
   (2026).  <https://arxiv.org/abs/2607.12597>

   The self-matched packing theorem, multiplicative paths, closure templates,
   and qualitative leaf-extended-spider corollary used here are from this
   paper.  Its proof chooses `q_i=B^i`, for a base larger than every arm
   length and the closure cutoff, and concludes gracefulness for sufficiently
   many leaves.  The present note changes the packing step: a short interval
   of consecutive multipliers suffices, giving an explicit threshold and a
   polynomial bound when the shortest nontrivial arm is bounded.

2. Matthew C. Superdock, *The Graceful Tree Conjecture: a class of graceful
   diameter-6 trees*, undergraduate thesis, Princeton University (2013),
   arXiv:1403.1564 (2014).  <https://arxiv.org/abs/1403.1564>

   Superdock proves that attaching sufficiently many leaves at any specified
   vertex of an arbitrary tree produces a graceful tree.  He also gives a
   distinct direct spider criterion: for decreasing leg lengths `m_i`, a
   sufficient total edge count is
   `n >= max_i (2i-1) 2^(m_i-1)` for the nontrivial legs.  Thus eventual
   gracefulness itself is old, and the present result must not be read as a
   new qualitative family.  Its different quantitative regime replaces
   dependence exponential in the longest arm by
   `O(L 2^d + L^2 k)`, where `d` is the shortest nontrivial arm.

3. Songling Shan and Yucheng Zhong, *Graceful Labeling of Two Families of
   Spiders*, arXiv:2605.14295v2 (2026).
   <https://arxiv.org/abs/2605.14295>

   This paper treats fast-growing arm sequences and spiders with one
   arbitrary arm and all remaining arms of length at most two.  Those shape
   hypotheses differ from the padded fixed-profile construction here.

4. P. Bahls, S. Lake, and A. Wertheim, *Gracefulness of Families of
   Spiders*, Involve 3 (2010), 241--247.
   <https://msp.org/involve/2010/3-3/involve-v3-n3-p01-p.pdf>

   This is background for classical graceful spider families, including
   nearly equal leg lengths.

## Search boundary

Primary and bibliographic searches used `graceful spider self-matched legs`,
`multiplicative legs graceful`, `leaf-extended spider graceful threshold`,
`graceful spider sufficiently many leaves`, and `consecutive multiplier
packing graceful spider`.  The exact consecutive-multiplier lemma, threshold,
and shortest-arm growth bound were not located.  This is a bounded,
search-relative novelty statement, not a claim of historical priority.

The reported six-arm proof deposited on Zenodo in September 2026 concerns a
different fixed-leg-count theorem and is not used here.  This note neither
reproves nor relies on that claim.
