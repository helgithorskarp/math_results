# Exact physical branch formulation

The h3835 cover partitions the 43 vertices into seven four-vertex blocks and
five three-vertex blocks.  In branch `(7,4,3)`, every block is a red clique:
seven fixed red `K4`s and five fixed red `K3`s.  Their 57 internal edges are
fixed red.  Every other one of the 846 physical edges belongs to exactly one
cross-block pair and receives its own Boolean variable.

Variable 1 is a forced-true constant.  Variables 2 through 847 enumerate the
846 nonfixed edges in lexicographic physical-pair order.  Root-order clauses
sort each child block by its four-bit red-neighbor signature to the first red
`K4`; these are the sound vertex relabelings established in h3835 and checked
independently in h3845.

For every physical five-set and each color not already contradicted by a
fixed edge, one clause forbids all remaining variable edges from having that
color.  Because all fixed edges here are red, there is one red clause for each
of the 962,598 five-sets.  A blue clause is present precisely when the set
contains at most one vertex from every block, giving 459,807 blue clauses.
Together with 3,360 root-order clauses and the true-constant unit, the formula
has 1,425,766 clauses.

The formula is satisfiable exactly when this normalized physical branch
contains a graph with neither a red nor a blue five-clique.  A satisfying
assignment would therefore decode to a good43.  An UNSAT result would exclude
this entire branch.  The recorded computation returned UNKNOWN, so neither
conclusion follows.
