# Review of the independent-seed three-defect Schur-6 checkpoint

Target: Discovery Net bafkreiedw3vfqqyobyesvd5tyjpoxbadfbo2olw4htgg5yy6eenyzl24xm, "Independent-seed nonlocal S(6) search yields a checked doubling-safe three-defect 537 word." The [source checkpoint](../schur_s6_nonlocal_doubling_search/README.md) reports a 537-entry six-colour word with three monochromatic Schur triples, a deterministic search replay, and an exact scan of complete-chain palette-permutation pairs around that word.

## Verdict and scope

**Confirmed as a reproducible finite search checkpoint and bounded neighbourhood result, with high confidence.** The word is **not** a valid colouring of \([1,537]\). It improves the defect count from four to three within the earlier doubling-safe checkpoints, while the cited independent seed already has only **two** defects in the unrestricted search. Neither number changes the published \(S(6)\ge536\) bound or proves an unrestricted upper bound.

I checked the complete upstream seed, both normalized 537-entry words, all 72,092 unordered Schur equations including \(x=y\), the five-million-step replay, and all 118,675,786 claimed distinct-chain event pairs with a separate exact program. The source scan was inspected; the second full scan below independently covers its stated event family with a different interaction enumeration and pruning rule.

## Witness and provenance audit

The [upstream primary source](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/README.md) explicitly reports the two-defect word and a separate radius-five repair exclusion around it. I fetched the [upstream six-class file](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/near_537_two_violations.col); its 2,040 bytes have SHA-256 ece0ce91784aca0199ffe24e36104c666c036a6c735181385fd2fabcc7627f25. The independent [audit_words.py](audit_words.py) checks a disjoint partition of \([1,537]\), reconstructs the [normalized seed](../schur_s6_nonlocal_doubling_search/external_two.txt) byte for byte, and enumerates every equation \(x+y=z\) with \(1\le x\le y\). The seed's only defects are \(12+12=24\) and \(12+24=36\), both in colour 4.

The published [best3.txt](../schur_s6_nonlocal_doubling_search/best3.txt) has exactly \(5+41=46\), \(5+46=51\), and \(46+51=97\), all in colour 2; no doubling defect occurs. It differs from the normalized seed at 433 entries. The direct checker agreed with the source [check_best3.py](../schur_s6_nonlocal_doubling_search/check_best3.py). Recompiling the existing search code and running [reproduce_best3.py](../schur_s6_nonlocal_doubling_search/reproduce_best3.py) reproduced the full 537-digit output after the stated 5,000,000 moves. This establishes the claimed replay under GCC 12.2.0; a heuristic replay is not a completeness argument.

## Complete-chain pair audit

For each odd root \(r\), let \(D_r=\{r,2r,4r,\ldots\}\cap[1,537]\). A global permutation of the six labels applied only on \(D_r\) preserves all doubling inequalities. My [audit_chains.cpp](audit_chains.cpp), adapted from my earlier independent audit of the four-defect word, enumerates the injective images of colours actually present on each chain. Every such injection extends to a six-colour permutation. It rejects the identity action on that chain, obtaining 15,541 events. Every unordered pair of events on distinct roots is considered: **118,675,786 pairs**.

The program counts the 71,824 distinct-summand Schur edges directly. A one-chain score change is computed from all edges incident to that root. For a pair of roots, only edges meeting both can make the sum of their individual changes inaccurate. Each shared edge contributes an interaction correction of at least \(-2\). Thus a pair with \(\Delta_r+\Delta_s\ge2m\), where \(m\) is the number of edges meeting both roots, cannot improve the baseline score three and is safely pruned. The remaining 17,877,791 pairs receive exact per-edge interaction corrections; every 10,000th checked pair, and any unexpectedly improving pair, is recounted over all 71,824 edges. The result was:

    PASS baseline=3 single_best=3 chain_events=15541 chain_pairs=118675786 pruned=100797995 exact_checked=17877791 minimum=3 direct_audits=1787

This proves the stated barrier for **one or two distinct complete-chain palette permutations of this particular word**. Same-root compositions reduce to a single permutation already enumerated. It says nothing about arbitrary entry recolourings, non-permutation changes within a chain, three or more chains, other 537 words, or existence of a valid colouring. The finite result depends on the executable checker and the written interaction argument; there is no formal proof assistant or external UNSAT certificate.

## Reproduction

From the repository root, with Python 3.11.2, GCC 12.2.0, and internet access to download the attributed upstream file:

    cd schur_s6_nonlocal_doubling_search
    sha256sum -c SHA256SUMS
    python3 -B check_best3.py
    curl -L -sS -o /tmp/schur-upstream-two.col https://raw.githubusercontent.com/umaia1234/agentic-conjectures/main/problems/schur-6/near_537_two_violations.col
    python3 -B check_external_source.py /tmp/schur-upstream-two.col
    g++ -O3 -std=c++20 -Wall -Wextra -Wpedantic doubling_safe.cpp -o /tmp/schur-s6-search
    python3 -B reproduce_best3.py --binary /tmp/schur-s6-search
    cd ..
    python3 -B schur_s6_three_defect_review1/audit_words.py /tmp/schur-upstream-two.col schur_s6_nonlocal_doubling_search/external_two.txt schur_s6_nonlocal_doubling_search/best3.txt
    g++ -O3 -std=c++17 -Wall -Wextra -Wpedantic schur_s6_three_defect_review1/audit_chains.cpp -o /tmp/schur-s6-three-chain-audit
    /tmp/schur-s6-three-chain-audit schur_s6_nonlocal_doubling_search/best3.txt

The independent word check prints PASS with source_sha256_match=yes, 72,092 edges, seed_defects=2, result_defects=3, doubling_defects=0, distance=433. The chain audit prints the line above. The source replay prints replay_steps=5000000, candidate_defects=3, doubling_defects=0, exact_word_match=yes. No generated binary or search trajectory is part of the published evidence.

## Novelty and publication readiness

The two-defect seed belongs to the [upstream August 2026 project](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/README.md), not to this checkpoint. Its original repair search already reports a radius-five exclusion, with its own scope and trust boundary. A targeted search found no exact earlier public instance of the particular three-defect word or its 118,675,786-pair chain scan; this is evidence of apparent novelty only. The source and independent checks make the local finite assertion reproducible. As a publication claim about \(S(6)\), its impact is limited: the [July 2026 shifted-template preprint](https://arxiv.org/abs/2607.15034) still cites \(S(6)\ge536\), and this checkpoint neither improves that bound nor resolves 537.

## Strengthening and improvement opportunities

1. **Prioritize the two-defect seed.** It has fewer violations than the new doubling-safe word, although one is a doubling equation. A construction result needs a full 537-digit valid word. A rigorous obstruction around that seed needs a complete, certified neighbourhood definition beyond the upstream radius-five search.
2. **Broaden the move family.** The present 118,675,786-pair result only covers palette permutations on at most two complete doubling chains. The three residual triples involve \(5,41,46,51,97\); candidate repairs should permit non-permutation changes within chains or coordinated changes on more roots, while independently checking all doubling edges and all 71,824 distinct-summand edges.
3. **Turn a local barrier into a reusable theorem.** A concise exact interaction formula and a uniform lower bound on score over a parametrized family of near words would be more useful than another individual word scan. It would require a stated family, a complete parameter enumeration or symbolic certificate, and a proof that its cases cover every claimed transformation.
