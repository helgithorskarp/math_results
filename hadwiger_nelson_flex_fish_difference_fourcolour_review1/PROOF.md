# Independent proof architecture

## Imported geometric premise

Let `F={p_0,...,p_22}` be the unique exact source realization inside the
rational box in the hash-pinned geometry certificate.  The earlier independent
review proves that these are 23 distinct plane points, that their complete
strict unit graph has the 42 fish edges and contact `(10,21)`, and that its
chromatic number is four.  This review reruns that dependency but does not
repeat its 42-dimensional contraction proof inside the new checker.

The two fixed anchors have exact singleton coordinate intervals.  Each other
source coordinate lies in its certified midpoint interval of radius `10^-25`.
The review constructs these intervals directly.

## Conservative address quotient

There are 529 formal addresses `a=(i,j)`, representing

```text
P_a = p_i-p_j.
```

The checker subtracts the two source-coordinate intervals endpoint by endpoint
to obtain a box for each `P_a`.  Two addresses are joined in the possible-
equality relation exactly when their boxes overlap in both coordinates, and
the review takes connected components.  Any actual equality necessarily
causes direct overlap, so actual collisions cannot cross the resulting 433
components.

For two coordinate intervals, the checker evaluates the exact range of their
difference and then squares it, using zero as the lower square endpoint when
the interval contains zero.  Adding the two squared-coordinate intervals
encloses the squared Euclidean distance.  All 139,656 unordered address pairs
are checked.  The computation proves:

- every pair inside one component has squared distance below `10^-48`, so no
  internal unit edge is possible;
- every pair in different components has squared distance greater than
  `399/1000000`, so different components cannot collide; and
- every excluded possible-unit pair has squared-distance gap from one greater
  than `17/1000000`.

Joining two components whenever any represented address pair has a squared-
distance interval containing one produces a 433-vertex, 1,646-edge
supergraph.  It contains every actual unit edge after collision quotienting.
The literal target word is proper on this independently reconstructed graph
and constant on each component.  It therefore induces a proper four-colouring
of the actual complete strict unit-distance graph.

The review uses interval endpoints rather than the target's midpoint expansion
formula.  The resulting component lists, edge lists, and serialization hash
nevertheless agree exactly with the target certificate.

## Lower bound and physical meaning

For each fixed `j`, the 23 addresses `(i,j)` form the translated set

```text
F-p_j.
```

Translation preserves all 43 exact source unit edges and distinctness.  A
fixed-label exhaustive search independently proves that the 43-edge source is
not three-colourable after 638 recursive calls.  Thus every difference body
contains a four-chromatic fibre, and the actual graph has chromatic number at
least four.  Together with the conservative word, its chromatic number is
exactly four.

All diagonal addresses `(i,i)` are the exact zero point, giving the unconditional
upper order bound `529-22=507`.  Since different conservative components cannot
collide, there are at least 433 physical points.  The boxes do not determine
whether addresses inside a nontrivial component coincide, so no exact physical
order between these endpoints is accepted.

The 23 translated source fibres cover every formal address and all contain
zero.  Since the source is connected, their exact unit edges give a connected
spanning subgraph of the actual quotient.  The source remains connected after
any one edge deletion, so every fibre edge lies on a cycle.  Any additional
actual unit edge also lies on a cycle in this already connected spanning
subgraph.  Hence the actual unit graph is connected and bridgeless.  This
structural strengthening does not affect the four-colour stop.

## Trust boundary

The new proof trusts CPython integer and `Fraction` arithmetic, JSON parsing,
the hash-pinned target word, and the imported source-realization theorem.  It
does not import the target verifier, its error formula, or its SAT producer.
The parent source theorem was itself independently reviewed by interval
Jacobian arithmetic and source reconstruction.

Controls compare the fixed-order colouring engine with brute force on all 512
labelled five-vertex graphs containing the normalizing edge, exercise 8,235
interval sample inclusions, and reject four malformed or improper colouring
words.
