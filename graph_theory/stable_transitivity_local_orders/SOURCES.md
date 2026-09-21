# Sources and status audit

Status was checked before technical development on 2026-09-21.

## Primary literature

1. Matthew Davis and Michael W. Schroeder,
   [*Relating tournaments and permutations with xrays*](https://arxiv.org/abs/2606.21532v1),
   arXiv:2606.21532v1 (2026).

   This paper introduces transitive tournament decompositions, stable
   transitivity, `m(T)`, and `m(n,k)`.  The arXiv history still lists only v1,
   submitted 2026-06-19.  Targeted inspection and searches found no result on
   stable transitivity of locally transitive tournaments or local orders.

2. L. Babai and P. J. Cameron,
   [*Automorphisms and Enumeration of Switching Classes of Tournaments*](https://doi.org/10.37236/1516),
   Electronic Journal of Combinatorics 7 (2000), R38.

   This paper calls tournaments switching-equivalent to linear orders
   `local orders`, identifies them with the class also known as locally
   transitive tournaments, and develops their switching classes.  The
   switching characterization used here is classical; `THEOREM.md` includes
   a direct rooted proof specialized to the present application.

3. Leonardo Nagami Coregliano,
   [*Quasi-Carousel Tournaments*](https://arxiv.org/abs/1503.04124),
   arXiv:1503.04124 (2015).

   This source records the standard neighborhood definition of locally
   transitive tournaments, their equivalent `W_4,L_4` forbidden-subtournament
   characterization, and the odd carousel family.

Targeted web searches combined `stable transitivity` with `locally
transitive tournament`, `local order`, `switching`, and `carousel`.  The only
stable-transitivity primary source located was Davis--Schroeder.  The
apparent-newness statement in this directory is relative to this search.

## Discovery Net dependency and collision check

The graph was refreshed through indexed height 5341.  No graph contribution
matching the local-order theorem was found.  Corollary 3 uses the earlier
Discovery Net result *Stable transitivity is exact under tournament
substitution and localizes to strong components* and its public source:

- [`../stable_transitivity_substitution`](../stable_transitivity_substitution)

The local-order theorem, its explicit witness, and the carousel formula are
independent of that result.
