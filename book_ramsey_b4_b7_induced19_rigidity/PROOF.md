# Proof and completeness bridges

All graphs are simple and finite. A red graph G is valid if every red
edge has at most three red common neighbors and every blue edge has at
most six blue common neighbors. This is equivalent to avoiding ordinary
red B4 and blue B7 subgraphs. Validity is hereditary under vertex deletion.

## 1. General adjacency-domain bound

Fix an induced valid core C with r vertices. Let D(C) contain every
subset P of V(C) for which a new vertex adjacent in red precisely to P
gives a valid (r+1)-vertex graph.

Form a compatibility graph Gamma on D(C). Distinct patterns P,Q are
adjacent if at least one color of the edge between two new vertices with
these patterns makes their (r+2)-vertex graph valid. Record a loop at P
if the same is possible with both vertices having pattern P.

Suppose a valid graph G contains C as an induced subgraph. Every outside
vertex has a pattern in D(C), by deleting all other outside vertices.
Every two outside vertices give a compatible pair by the same hereditary
argument. If Gamma has no loops, those patterns are distinct. They form
a clique in Gamma. Thus

    |V(G)| <= r + omega(Gamma)                         (1)

when Gamma is loop-free. In particular, a loop-free triangle-free Gamma
permits at most two additional vertices. This is only a necessary
compatibility bound: a triangle in Gamma need not itself extend C.
The argument uses absence of triangles, not a sufficiency assumption.

## 2. Exact one-vertex domains

For a new vertex z, write x_u=1 when zu is red and x_u=0 when it is blue.
An old red spine uv with three red common neighbors imposes

    not x_u or not x_v.

An old blue spine uv with six blue common neighbors imposes

    x_u or x_v.

These are exactly the constraints imposed by the old spines: a single
added vertex contributes either zero or one common neighbor, so a
nonsaturated spine cannot exceed its cap. The remaining constraints are
the codegree bounds at the new spines zu. Each complete binary pattern
is checked directly against all spines of the (r+1)-vertex graph.

The generator uses implication-graph reachability to force assignments.
Literal 2u means x_u; literal 2u+1 means not x_u. An assumed true literal
forces every reachable literal. If both polarities of a variable are
forced, that branch has no satisfying extension. Otherwise a not-yet
assigned variable is split into its two values. Consistent complete
assignments are checked against the graph definition.

Every split retains both values. Forced assignments are logical
consequences of the necessary old-spine clauses. Therefore this finite
tree covers every pattern in D(C). No root assignments, symmetry
restrictions, or heuristically selected patterns are imposed.

The separate checker reconstructs the clauses from explicit sets of page
vertices. It propagates by repeated clause scanning, not implication
reachability. At a split it requires the variable to remain unknown,
then checks both children. A conflict leaf must produce a literal
contradiction under these clauses. A complete leaf must have its exact
pattern accepted or rejected by the direct graph checker. No incomplete
assignment may terminate as a valid or invalid complete leaf. These
invariants check the finite coverage argument node by node.

The certificate tree grammar is:

    'C'                         # conflict under necessary clauses
    'I'                         # complete pattern has a forbidden book
    ['V', integer_mask]         # complete valid pattern
    [variable, blue_child, red_child]

At r=19 the mask uses bit u for the u-th smallest original vertex not
deleted. The certificate must contain each of the 210 original deleted
pairs exactly once, in lexicographic order. The checker verifies this
cohort coverage separately from each domain's coverage.

## 3. Exact pairs and computed compatibility graphs

For each core the generator tests every pattern pair P,Q, allowing P=Q,
and both colors of the joining edge. Only the order of the two new
vertices is quotiented: exchanging them exchanges P,Q without changing
the core or validity. Every unordered pair with repetition is present.
The independent checker reconstructs and checks every such graph from
explicit edge sets, then compares its complete compatible-pair list
entry by entry with the certificate.

Write H for the precise primary fixture in h21.json, and

    A = H symmetric-difference {(6,16),(10,16)},
    B = H symmetric-difference {(9,16),(10,16)}.

All three 21-vertex graphs are directly checked to be valid. For each
deleted pair S, the checker restricts each of H,A,B to the retained
19 labels. A template is eligible only if this restriction equals H-S
exactly. It reconstructs the two remaining vertex patterns and joining
color and compares their predicted set to the full checked pair list.
There are no additional pair completions.

Template A is eligible precisely when 16 belongs to S or S={6,10}.
Template B is eligible precisely when 16 belongs to S or S={9,10}.
This follows immediately by asking whether S meets both of their two
toggled pairs. H is always eligible.

The independent checked compatibility graphs, after removing isolated
patterns, have shapes:

    188 copies of K2;
    20 copies of K1,3 (exactly the S containing 16);
    2 copies of 2K2 (S={6,10} or S={9,10}).

The checker verifies no compatible loops and no triangles directly,
as well as these shapes and the exact template equality. There are
18,246 tree nodes, 9,055 consistent necessary-kernel assignments, and
1,308 valid domain patterns across the complete cohort. These counts
are reproducible diagnostics; coverage is established by the tree and
pair checks, not by matching counts alone.

## 4. Maximum order and rigidity

Apply (1) with r=19. Each checked compatibility graph has clique number
two. Every valid graph containing any H-S as an induced subgraph has
order at most 21. The graph H itself supplies a valid order21 host for
every S, so the maximum is exactly 21 in each of the 210 cases.

The exact pair list also proves the claimed 21-vertex rigidity: with
the old core labels fixed, every completion is one of the eligible
H,A,B templates after possibly swapping its two new vertices. This
classifies fixed-core completions; it does not assert that the three
templates are pairwise nonisomorphic.

No graph automorphism assumption is used. If a core merely occurs via
an isomorphism, transport its labels along that isomorphism to apply
the same result. Thus the exclusion concerns every induced copy of
every core, not just a chosen placement of its vertex labels.

## 5. Consequence for repairs

Take any hypothetical valid G on 22 vertices, delete any one vertex,
and label the remaining vertices by 0,...,20. Let F be the set of pairs
on which this 21-vertex graph differs from H. If a set S of at most
two original vertices meets every pair of F, enlarge it to size two.
The other 19 original vertices induce exactly H-S in G. This contradicts
the maximum-order result above. Therefore the edit graph F has vertex
cover number at least three under every such deletion and labeling.

In particular, changing arbitrary numbers of edges incident to only
one or two chosen original vertices, and adding one new vertex with
arbitrary incident colors, can never extend H to a valid graph on 22
vertices. This is a restricted repair obstruction, not a resolution
of whether other 22-vertex graphs exist.

## Trust boundary

The finite certificate is generated locally and is not a required
external input. The checker is self-contained and does not import
generator code. Exact integer masks and set operations are used;
there is no solver verdict, floating-point inference, large imported
enumeration, timeout, or memory-kill interpretation. The graph-domain
bound and tree coverage bridges are the displayed elementary arguments,
not proof-assistant formalizations. An independent literal sweep of
all 2^19 patterns for S={6,18} reproduces its largest (24-pattern)
domain entry by entry. That control is not substituted for checking
the full 210-case certificate.
