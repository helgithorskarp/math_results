# An exponential survivor bound for one Bell-leaf encoding

This directory contains a complete hand proof and a different researcher's
internal check of an obstruction to one proposed construction of many
boxed-2143 avoiders. It does not decide the full growth question.

For a permutation sigma of {1,...,k}, form the doubled-label word

    S = (1,k+sigma_1,k+sigma_1,1, ..., k,k+sigma_k,k+sigma_k,k).

Make E by listing the two one-based positions of each label in descending
label order 2k,...,1. E is a permutation of length 4k. The Bell inputs are
set partitions of {1,...,k}: list each block decreasingly, ordering blocks
by their minima, to obtain sigma. This entire input-to-output map is injective.

Let T_k count Bell inputs whose E has no boxed-2143 occurrence. Here a boxed
occurrence means indices i1<i2<i3<i4 with
E[i2]<E[i1]<E[i4]<E[i3], with no unselected j strictly between i1 and i4
whose value is strictly between E[i2] and E[i3].

The proved bound is

    T_1 <= 1,
    T_k <= (k-1) 2^(k-2) + 1                 for every k >= 2,
    limsup T_k^(1/(4k)) <= 2^(1/4).

Every internal ascent of sigma in an avoiding image must start at a prefix
minimum; the final possible ascent is excluded because a needed root is
absent. For a Bell input, applying this to its second block boundary leaves
at most two blocks, or three with a final singleton. Counting these necessary
shapes proves the bound. Necessary shapes need not actually survive. Even
optimal pruning of this specific length-4k encoding therefore cannot give
unbounded output roots. Other encodings and the full avoiding population
are outside the theorem.

The source consists of:

* `BIPARTITE_BELL_LEAF_EXPONENTIAL_SURVIVOR_UPPER_HAND_V1.md`: complete author
  argument, preserved at its original pre-review bytes.
* `BELL888_ENTIRE_INDEPENDENT_HAND_PROOF_V1.md`: independent inverse-position
  and exhaustive leaf/root reconstruction, including the exact block count.
* The method, review and actual author acceptance: the full internal exchange.
* The original literal k4 input and its complete manual certificate: all
  sixteen entries, eight labelled position pairs, selected points and every
  unselected point in the horizontal interval.
* `SOURCE_MANIFEST.json`: exact compact source sizes and SHA256 hashes.

To reproduce the literal witness by hand, list the first/second positions
of labels8 down to1 in S. This gives
E=(14,15,10,11,6,7,2,3,13,16,9,12,5,8,1,4). The selected one-based indices
(6,8,9,11) have values(7,3,13,9). The only unselected horizontal points
(7,2) and(10,16) lie outside the open vertical band(3,13). For arbitrary
k, follow the exhaustive cases and anchored-block count in the two proofs;
the single example does not supply their infinite quantifiers.

No native mathematical executable or exhaustive enumeration was used for
this theorem or its review. The finite certificate was reconstructed by
hand. Original pending-stage labels in preserved documents are historical;
the actual whole author exchange accepted the complete scoped theorem.
This is internal team checking, not external peer review, formal verification
or a novelty claim. Administrative receipts are retained in the campaign;
they are not mathematical premises and are excluded from this compact source.

The campaign's full target asks whether all boxed-2143 avoiders satisfy
a_n<=C^n for some finite C. It remains unsolved. Literature context:
[original author manuscript](https://spider-v.science.strath.ac.uk/sergey.kitaev/Papers/mesh.pdf)
and [2026 manuscript, Theorem4.4](https://arxiv.org/html/2609.13764v1).
The latter still lists the growth question as open; this limited obstruction
does not resolve it.

The previous k5 necessary-shape counterexample is included as a compact
literal from the separately checked five-case exchange. Its historical
selection fields are ZERO BASED. Equivalently, one-based indices(2,4,5,7)
have values(11,3,18,14), with unselected(3,2),(6,19) outside(3,18).
This case is supporting context; the all-size upper needs no old experiment.
