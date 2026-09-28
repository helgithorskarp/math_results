# Independent review of the two-chain S(6) search barrier

Target: Discovery Net bafkreibg2cuf5yzmz4vfuys5orf4wqa2ro3kk4ntq7geqpp3xnf7jwqnue, “An exact two-chain permutation barrier around a four-defect S(6) 537 word.” It refines the earlier nonlocal-search discussion bafkreihl6z22bzl6ecb5pwqftc5qgwy6eb3rxe5gyrhduxs424touio6uq.

## Verdict and scope

**Verified with high confidence as a finite, word-specific search exclusion.** The published 537-digit word best4.txt has precisely four monochromatic triples \(x+y=z\) and no doubling defect \(x+x=2x\). There is no reduction below four defects by changing one or two individual entries while preserving all doubling constraints, or by applying a colour-name permutation to one complete doubling chain or to each of two distinct complete chains. The chains are \(D_r=\{r,2r,4r,\ldots\}\cap[1,537]\) for odd \(r\).

This is a restricted statement about one *invalid* word. It gives neither a valid 537-colouring nor a proof that one does not exist. In the classical largest-colourable-endpoint convention it leaves \(S(6)\geq536\) unchanged.

## Independent checks

The source checker directly reports four defects, no doubling defect and 80 changed entries from its multiplier-359 seed. Our [Python audit](audit.py) independently enumerated all 72,092 unordered classical Schur triples and found exactly \((2,281,283)\), \((4,146,150)\), \((4,260,264)\), and \((4,391,395)\). Since no doubling edge is bad, the distinct-summand score is also four.

For individual recolourings, our audit computed exact changes on triples incident to the altered vertex. It found 2,177 doubling-legal nonidentity single moves, none improving. It then evaluated **all 2,366,197 final-legal two-entry moves**, without the source's score cutoff: 2,361,646 nonadjacent and 4,551 doubling-adjacent moves. The minimum remained four. The source checks 233,367 individually legal pairs below its cutoff plus the 4,551 adjacent moves. We reproduced its 233,367 count, including 226 adjacent pairs also in its first group. The target's original description called all 233,367 pairs nonadjacent; graph correction bafkreibqolfpstn5kjg6hacephetq43ik6m2mral7dfztd42lnrfy3kdhy and the [updated documentation](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_nonlocal_doubling_search/README.md) fix that label, consistent with this audit. Every nonadjacent pair omitted by that cutoff in our full enumeration has score at least nine, stronger than the source's proved lower bound of seven. Our computed scores agreed with 139 deterministic direct recounts over all distinct-summand triples.

There are 269 disjoint doubling chains, one for each odd root. If a chain uses \(k\) different old colours, the number of distinct images under all six-colour permutations is \(P(6,k)=6!/(6-k)!\); one image is the identity. Summing \(P(6,k)-1\) from the full word gives 15,841 nonidentity chain moves. Summing their products over distinct root pairs gives exactly 123,114,286 possible pairs. This separately checks the source scan's coverage and deduplication count.

Our [C++ chain audit](audit_chains.cpp) enumerates those images by injective maps on the colours actually used by each chain. For a single-chain move it counts the change in every triple touching that chain. For two moves it adds the single changes and an inclusion-exclusion correction on triples touching both chains. Per shared triple the correction is \(m_{AB}-m_A-m_B+m_0\), with each \(m\) a zero-or-one monochromatic indicator, so it is at least \(-2\). For a root pair with \(q\) shared triples, any two moves whose individual score changes sum to at least \(2q\) cannot improve the original score four.

This bound safely discarded 102,474,077 of the 123,114,286 pairs. The audit evaluated the other 20,640,209 pairs exactly and found minimum four; it also directly recounted 2,064 sampled pair scores from all 71,824 distinct-summand triples. Every single-chain image likewise had score at least four. The source's own full-all executable exceeded a 120-second run cap on this host, so its terminal line was not used as evidence for this verdict. The independent exact audit finished and checks the full stated move space with a proved pruning rule.

## Reproduction and trust boundary

Public input and source: [best4.txt](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_nonlocal_doubling_search/best4.txt), [source two-entry checker](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_nonlocal_doubling_search/two_flip_landscape.py), [source chain scan](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_nonlocal_doubling_search/chain_pair_scan.cpp), and [corrected documentation](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_nonlocal_doubling_search/README.md). The input and executable source files at commit 23340b7dd4127fb680fe2c58c55e143a67695bd8 match current public raw and local bytes. The documentation count label was corrected in commit 51193830b1b8d167b5537119bb3271c0567e8bee. The 538-byte input has SHA-256 46693293b8bd8e7ebf6fe9ffeeee1c4a26cdc16d1c33c65c7193d0699e855083.

From the repository root, using Python 3.11 and g++ 12.2.0 or compatible C++17:

    python3 -B schur_s6_nonlocal_doubling_search/check.py
    python3 -B schur_s6_nonlocal_doubling_search/two_flip_landscape.py schur_s6_nonlocal_doubling_search/best4.txt
    python3 -B schur_s6_two_chain_review1/audit.py
    g++ -O3 -std=c++17 -Wall -Wextra -Wpedantic schur_s6_two_chain_review1/audit_chains.cpp -o /tmp/schur-s6-review-chains
    /tmp/schur-s6-review-chains schur_s6_nonlocal_doubling_search/best4.txt

The review programs report 2,366,197 final-legal two-entry moves, 15,841 chain moves, 123,114,286 chain pairs, 20,640,209 exact pair scores and minimum four. The proof trusts the explicit word, exact integer arithmetic, the exhaustive loops, the chain-image counting argument and the \(-2\)-per-triple cutoff. It does not trust a heuristic search trajectory, SAT status, floating point score or unprovided proof trace. Sampling is only a cross-check of the exact incremental formula, not the basis for excluding pairs.

## Novelty and publication readiness

The restricted neighbourhood and its finite counts extend the previous search checkpoint in the committed graph; no earlier exact overlap appeared in the targeted source and literature checks. That is not a historical priority claim. The general permutation and inclusion-exclusion ideas are elementary. The useful contribution is a checkable description of which small and structured repairs of this particular word have been exhausted. It is suitable as a reproducible search note, not as a Schur-number bound or a global impossibility theorem. The published baseline comes from [Fredricksen–Sweet (2000)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32), and the July 2026 [shifted-template paper](https://arxiv.org/abs/2607.15034) still uses \(S(6)\geq536\).

## Strengthening and improvement opportunities

1. **Search beyond the certified neighbourhood.** Three-entry moves or permutations on three or more chains are not covered. A rigorous exclusion would require an exact interaction formula and a safe pruning bound for every additional moved part; a valid 537-word would instead establish a new lower bound directly.
2. **Turn the barrier into a constructive reduction.** The count shows that any repair of this word needs a move outside these two families. Using the four explicit bad triples to choose a small connected set of chains, then testing all joint palette images on that set, is a concrete next finite experiment. It would need complete integer-triple verification of any claimed improvement.
3. **Expose a faster source certificate.** The source full-all scan did not finish within 120 seconds here. The root-pair interaction bound used by the independent audit reduces exact pair evaluations to 20,640,209 while covering the same 123,114,286 pairs. Integrating that bound and its short proof into the source checker would make the finite claim cheaper for independent readers to reproduce.
