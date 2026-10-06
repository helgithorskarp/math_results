# Exact maximum-insertion rule for boxed 2143

Author: Quinn / literature-researcher-3. Date: 2026-10-05.
Status: author derivation awaiting a different researcher's full check. This is groundwork for decision 410, not a solution of its growth question. No novelty claim is made for the algorithmic criterion.

The agreed target asks whether the full boxed-2143 avoidance sequence has a uniform exponential bound, or instead has infinite limsup of nth roots. My lane examines the full class through legal maximum insertions. A transition rule or a census does not itself supply either asymptotic conclusion.

## Conventions

Write a permutation p of [n] as p_1,...,p_n. Its gaps have indices g=0,...,n: gap g lies after the first g entries. Let q be obtained by inserting M=n+1 at gap g. Thus old indices i<=g stay i, old indices i>g become i+1, and M has new index g+1. The implementation uses zero-based entry indices and the same gap indices.

For an old index j, let

- l(j) be the nearest index strictly left of j whose value is greater than p_j, if one exists;
- r(j) be the nearest index strictly right of j whose value is greater than p_j, if one exists.

Call j eligible when both indices exist and p_{l(j)} < p_{r(j)}.

## Claim 1: all newly created occurrences

For an arbitrary parent permutation p, the boxed-2143 occurrences in q that use M are exactly

    (l(j), j, g+1, r(j)+1)

in one-based child indices, for eligible j satisfying j <= g < r(j).

Proof. In any 2143 occurrence, the largest selected value is the third entry. If that value is M, write the other selected values x,y,z in positional order, where y<x<z<M. Let the old indices of x,y,z be l,j,r. Necessarily l<j<=g<r. The bounding rectangle has vertical interior (y,M). Every other old entry has value below M. Rectangle emptiness therefore says that every unselected old entry strictly between l and r has value less than y. It follows that l is the nearest greater entry left of j and r is the nearest greater entry right of j. In particular, j is eligible.

Conversely, for an eligible j with j<=g<r(j), nearest-greater status ensures that all other entries between l(j) and j and between j and r(j) have value below p_j. Inserting M in the indicated interval gives the order p_{l(j)},p_j,M,p_{r(j)} with p_j < p_{l(j)} < p_{r(j)} < M. The remaining entries in its horizontal interior lie below p_j, so none lies in its vertical interior. The rectangle is empty. This proves both directions and enumerates the actual occurrences, rather than only detecting their existence. QED.

## Claim 2: the full legal-gap rule

The old boxed occurrences persist unchanged except for the index shift. Inserting M cannot change their emptiness, because M lies above their upper boundary. Consequently an avoiding parent has an avoiding child at exactly the gaps outside

    union over eligible j of {j,j+1,...,r(j)-1}.

This claim uses avoidance of the parent. A nonavoiding parent cannot become avoiding by insertion of a new maximum. For any avoiding child, deleting its maximum preserves all potential occurrences among its remaining entries: the removed point was outside every vertical bounding interval. Thus the maximum-deletion parent is avoiding. This establishes the exact generating tree of the entire class, with no missing children or duplicate parents. Distinct insertion histories recover by repeatedly recording the maximum's position and deleting it.

In particular, with A_n the set of avoiders and A_0 containing the empty permutation,

    |A_{n+1}| = sum over p in A_n of the number of legal gaps of p.

This is an exact recurrence over the full objects, not a closed scalar recurrence. The decreasing permutation has n+1 legal gaps, so a dimension-independent bound on the number of children of each object is false. An exponential upper bound would require a global encoding or a justified aggregate transition estimate. A lower bound would require a persistent high-branching family; neither is proved here.

## Claim 3: a complete alternative occurrence checker

For each M in {4,...,n}, restrict p to values at most M. In that restriction M is the maximum. Apply Claim 1 to its maximum-deletion parent and translate the indices back into the original p. Collect the resulting occurrences over M.

Every original boxed occurrence has one selected largest value M. Deleting entries larger than M preserves its rectangle because those entries lie above its upper boundary. Conversely, restoring such entries cannot invalidate an occurrence found in the restriction. Claim 1 therefore finds precisely all occurrences with selected largest value M. Their largest selected values partition the occurrence set, proving that the checker finds every occurrence exactly once. This is a different reduction from enumerating all four-index subsequences or all rectangles.

## Algorithm and trust boundary

Nearest greater indices come from monotone-stack scans, each linear in n. The forbidden intervals can be marked by a difference array, making the legal-gap list linear-time. Enumerating newly created occurrences at one specified gap scans all eligible j. The complete checker repeats this for each possible largest selected value and performs quadratic scans; its final canonical ordering additionally costs O(K log K) for K returned occurrences. No floating point, solver, dataset, or external library is required.

kernel.py implements these rules with validated permutations and explicit occurrence indices. verify_kernel.py separately implements the definition by four-index enumeration and interior scanning. Exhaustive agreement on its stated finite range tests implementation and normalization; the written argument above is the justification for arbitrary n. A teammate must check that argument separately before this is reported as an internally checked lemma. Two same-author algorithms are not external or team-independent review.

## Prior context and remaining obligation

Primary sources: Avgustinovich, Kitaev and Valyuzhenich, DAM 161 (2013), Sections 1 and 5, working manuscript https://spider-v.science.strath.ac.uk/sergey.kitaev/Papers/mesh.pdf ; Kitaev, Qiu and Xu, arXiv:2609.13764v1, Sections 1, 3 and 7, https://arxiv.org/html/2609.13764v1 . Extremal deletion, value-interval formulations, and the open growth target are prior context. Specialized containment algorithms exist; I make no priority claim for this derivation.

Next falsifiable structural test: identify a boundary state controlling the kernel and prove its exact update under legal insertion. Check state collisions by comparing child states and all legal-gap profiles, not aggregate counts alone. If a proposed compressed state fails, preserve a smallest pair with the same state and incompatible continuations. Passing finite tests would still require a uniform state/encoding argument for the full target. No completion or stop request is justified by this packet.
