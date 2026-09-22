# Sources and status boundary

1. V. Chvátal, *On certain polytopes associated with graphs*, Journal of
   Combinatorial Theory, Series B 18 (1975), 138--154,
   DOI: https://doi.org/10.1016/0095-8956(75)90041-6.
   This supplies the vertex-packing polytope framework and the perfect-graph
   characterization used for perfect quotients and induced paths.  The
   odd-hole/antihole specialization is made explicit in `THEOREM.md`.

2. N. Alon, J. Pach, and J. Solymosi, *Ramsey-type theorems with forbidden
   subgraphs*, Combinatorica 21 (2001), 155--170,
   DOI: https://doi.org/10.1007/s004930100016.
   This is the primary substitution reference in Erdős--Hajnal theory.  The
   present result has different quantifiers: it gives an exact exponent and
   leading constant on a specified modular host class.

3. T. Gallai, *Transitiv orientierbare Graphen*, Acta Mathematica Academiae
   Scientiarum Hungaricae 18 (1967), 25--66.  Gallai's modular decomposition
   theorem justifies the equivalent prime-quotient description.  The proof
   itself may instead take the recursive definition of `M_h` as primary.

4. M. Bonamy, N. Bousquet, and S. Thomassé,
   *The Erdős--Hajnal Conjecture for Long Holes and Anti-holes*,
   arXiv:1408.1964 (and subsequent journal versions/results in this line),
   https://arxiv.org/abs/1408.1964.
   This concerns fixed forbidden induced holes/antiholes.  It neither states
   nor implies the sharp modular length hierarchy proved here.

5. The immediately preceding reviewed source is
   `graph_theory/pentagon_perfect_eh_exponent` in this repository.  It proves
   the `h=2` result when the only imperfect prime quotient allowed is `C_5`.
   The present theorem strictly enlarges the prime-quotient class to every
   sufficiently long odd hole and odd antihole and gives a sharp theorem for
   each length threshold.

Targeted live searches (odd hole/antihole, modular decomposition,
substitution, weighted stable-set inequality, exact Erdős--Hajnal exponent)
did not locate the weighted cycle lemma or this length-sensitive modular
classification.  This is a bounded status check, not an exhaustive priority
claim.
