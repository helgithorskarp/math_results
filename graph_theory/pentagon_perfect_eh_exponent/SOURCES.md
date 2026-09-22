# Sources and status boundary

Checked on 2026-09-22.

1. V. Chvátal, *On certain polytopes associated with graphs*, Journal of
   Combinatorial Theory, Series B 18 (1975), 138--154.
   <https://doi.org/10.1016/0095-8956(75)90041-6>

   Chvátal characterizes perfect graphs by the equality between the stable-set
   polytope and the nonnegative clique-inequality polytope.  This is exactly
   the imported result used for perfect outer quotients.

2. N. Alon, J. Pach, and J. Solymosi, *Ramsey-type Theorems with Forbidden
   Subgraphs*, Combinatorica 21 (2001), 155--170.
   <https://doi.org/10.1007/s004930100016>

   They prove that the collection of forbidden patterns having the
   Erdős--Hajnal property is closed under substitution.  Their theorem varies
   the forbidden pattern `H`; the result in this directory instead gives an
   exact exponent for a recursively defined class of host graphs `G`.

3. M. Chudnovsky, A. Scott, P. Seymour, and S. Spirkl, *Erdős--Hajnal for
   graphs with no 5-hole*, Proceedings of the London Mathematical Society 126
   (2023), 997--1014. <https://doi.org/10.1112/plms.12504>

   This proves the Erdős--Hajnal property for all hosts with no induced
   `C_5`.  The present class deliberately contains `C_5` and all its
   lexicographic powers, so neither theorem contains the other.

4. T. Gallai, *Transitiv orientierbare Graphen*, Acta Mathematica Academiae
   Scientiarum Hungaricae 18 (1967), 25--66.
   <https://doi.org/10.1007/BF02020961>

   Gallai's decomposition supplies the standard equivalence between recursive
   substitutions and the prime-quotient description.  The proof here can also
   be read purely from the recursive definition and does not require
   uniqueness of the decomposition.

## Search boundary

Primary and bibliographic searches used the combinations `substitution
closure C5 Erdős-Hajnal exponent`, `alpha omega C5 substitution`, `log_5 4
graph clique independence`, `modular decomposition prime quotients perfect or
C5`, and `perfect graphs C5 substitution closure`.  The searches located the
qualitative Alon--Pach--Solymosi substitution theorem, the exact perfect-graph
polytope input, and the distinct `C_5`-free host theorem, but no source stating
the product exponent

```text
alpha(G)omega(G) >= |V(G)|^(log_5 4)
```

for the perfect-or-pentagon modular class, nor its weighted outer-graph lemma.
Novelty is therefore search-relative; no historical-priority claim is made.
