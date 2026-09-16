# Proof outline

## Reviewed finite claim

The target fixes sixteen labelled induced subgraphs of Haugland's 2,131-point
graph.  For each seed `0,...,7` and either orientation, vertices are removed
in increasing order of current induced degree, SHA-256 tie key and label,
subject to the frozen half quota and five protected labels.  Each resulting
support has 508 labels.

`verify.py` does not import the target implementation.  It stores the live
set and every adjacency set as Python integers, scans every currently
eligible label at every deletion, and uses `int.bit_count()` to obtain the
current degrees.  The resulting sixteen label hashes and induced-edge hashes
equal the target certificate.  Direct edge checks validate every target
four-colour word.  The supports are distinct, connected, have 2,105--2,142
edges and minimum degree three, and contain both private-half cross edges.

## Complete physical geometry

The pinned parent edge list was previously obtained by two exact all-pairs
routes.  This review additionally reconstructs the exact coordinates from
the Appendix-A paths through the SymPy representation of
`Q(zeta_84)(sqrt(5))`.  On the 952 labels occurring in at least one support,
evaluation modulo 1009 is used only as a no-false-negative sieve.  All 5,005
survivors are then tested by exact characteristic-zero arithmetic.  Exactly
4,773 unit pairs survive, with global edge hash
`a629f888c136d6ee08a0f5561071202b6efdcd288493b4d6082e769ff00b8c79`;
this equals the restriction of the parent strict edge list pair for pair.
Thus these are actual induced plane unit-distance graphs, not abstract
chromatic graphs or relaxed embeddings.

## Reviewer strengthening

The union of all sixteen labelled supports has 952 vertices and the same
4,773 complete unit edges.  `certificate.json` gives a 952-symbol word over
`0,1,2,3`; direct comparison on every edge proves it is a proper
four-colouring.  Its colour-class sizes are 249, 235, 228 and 240.  Restricting
this one word to any of the sixteen supports gives another proper
four-colouring.  The union is connected and has minimum degree four.

The word was discovered by CaDiCaL 1.9.5 through python-sat 1.9.dev15, but
the solver status is not a proof premise.  Only the literal word and the
solver-free edge checks enter the result.

## Scope

The target and review prove upper bounds only.  They do not show that any
support or the union needs four colours; some could be three-colourable.
They say nothing about other deletion orders, seeds, quotas, subsets or
arbitrary Haugland-derived graphs.  In particular, they do not improve the
509-vertex unrestricted five-chromatic record.

The repository's earlier independent Haugland reproduction did not finish
the parent's endpoint-forcing lower-bound certificate.  Neither this review
nor the target uses that missing lower bound: exact coordinates, complete
unit edges and positive colour words suffice.

