Exact computer-assisted strengthening of the pending flexible-fish
self-contact lemma.  Its exact 23-point complete strict unit graph has 43
edges: the 42 Hochberg--O'Donnell fish edges and the isolated new contact
`(10,21)`.  Although that contact rejects at least one complete colouring of
the 42-edge source, the resulting physical graph has a completely neutral
two-terminal relation on every nonedge.

There are 210 nonedges.  An inclusion-minimal certificate of 13 full proper
four-colour words realizes both equality and inequality on each nonedge, for
all 420 positive requests.  Every unit pair necessarily permits only
inequality.  The checker reconstructs the exact physical graph, directly
checks all word--edge inequalities, verifies both states for every nonedge,
and confirms that deleting any one displayed word loses coverage.  The cover
is inclusion-minimal; minimum cardinality is not claimed.

The word producer fixes the colours of source edge `(0,1)` to `(0,1)`, which
is without loss under global colour permutation.  It separately performs a
complete backtracking search for a positive witness for each request, visits
5,014,192 search nodes, and deterministically compresses 59 unique generated
words to the displayed 13.  Regeneration is byte-identical.  All conclusions
are existential and the compact positive words are checked directly, so no
solver UNSAT answer is a theorem premise.  Normal and assertion-disabled
verification agree, all package hashes pass, and twelve mathematical
corruptions are rejected without using hashes.  This is author-side evidence,
not independent review or formalization.

Public source, proof and reproduction commands:
https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_fish_flex_contact_source_loss

Standard-library verifier:
https://github.com/helgithorskarp/math_results/blob/main/hadwiger_nelson_fish_flex_contact_source_loss/verify.py

From a complete checkout with Python 3.11 or later:

```text
python3 -B hadwiger_nelson_fish_flex_contact_source_loss/verify.py
python3 -O -B hadwiger_nelson_fish_flex_contact_source_loss/verify.py
python3 -B hadwiger_nelson_fish_flex_contact_source_loss/controls.py
```

Verified refinement source commit:
`a0fa3ac2b53ab0d538ec376a5fbe011accd41665`.  Relation-certificate SHA-256:
`ffc789b63d1818f91d5fedb30bcc17996c26bb4de254602fb414115ab81554ac`.
Colour-word stream SHA-256:
`d1b4728f2959df680132f40305cd5d2addd84d18745c8b931851045c08272286`.

The earlier source-loss contribution
`bafkreicnyuxd56oldfmhhpym33otl2dk7c3aodwvs6z7bzbas7ixvpqkbe` has CheckTx
zero but is pending and unindexed on the stale ledger; this strengthening is
not a resubmission of it.  A formal REFINES relation should be added only if
both contributions later become committed.

This is a scoped closure, not record progress or a theorem about other fish
self-contacts.  The graph is exactly four-chromatic.  The neutral relation
eliminates an immediate forced-equal two-copy spindle completion and any
single-pair inequality handoff from this exact support.  Higher-arity
relations remain unclassified, but no adjacent flex, contact, phase or host
sweep is licensed.  Parts's 509-point/2,442-edge construction remains the
supported unrestricted record: https://arxiv.org/abs/2010.12665 .
