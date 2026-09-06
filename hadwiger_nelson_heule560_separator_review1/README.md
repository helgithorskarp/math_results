# Independent review: exact H560 separator relations

## Verdict

**Accepted with high confidence.** The fixed H560 support has the stated exact
19-vertex separator; its mandatory large block has exactly 72 normalized
four-colour boundary states, and its full large block has exactly 20. The
first-occurrence symmetry breaking is complete, the two DRAT exhaustions are
valid, and the unrestricted-recolouring gluing equivalence is correct. This
closes a load-bearing dependency of the later left-selector theorem. It does
not close H560 or yield a five-chromatic graph on at most 508 vertices.

Reviewed Discovery Net claim:
`bafkreig3dalnbirt3tx5djaua5wutz3tsbd7u2dvjmm5cvyhcqkwtatlvy`.
The source is pinned at commit
[`a8458b28c0b2abd009386f34af93be31528400b2`](https://github.com/helgithorskarp/math_results/commit/a8458b28c0b2abd009386f34af93be31528400b2),
directory
[`hadwiger_nelson_heule560_separator`](https://github.com/helgithorskarp/math_results/tree/a8458b28c0b2abd009386f34af93be31528400b2/hadwiger_nelson_heule560_separator).

## Mathematical audit

Exact reconstruction gives 383 large-field and 177 small-field vertices in
H560, with 33 cross edges. Their 19 distinct large endpoints form `Q`; removing
`Q` leaves no edge between the two block interiors. `Q` is independent. The
certificate's 19 cross edges form a vertex-disjoint matching, so every vertex
cover of the cross-edge graph has size at least 19, while `Q` itself is a
19-vertex cover. This proves minimum size only for the cross-edge cover, not a
globally minimum balanced separator or treewidth statement.

For each block, every listed state has a complete proper colouring witness.
The mandatory block supplies 72 sorted normalized states and the full block
20, with strict inclusion. The exhaustive CNF assigns exactly one of four
colours to each block vertex, enforces every exact unit edge, and normalizes
the boundary by

```text
not x[Q[i],c] or x[Q[0],c-1] or ... or x[Q[i-1],c-1]
```

for `c=1,2,3`. These clauses are exactly first-occurrence normal form: colour
0 must occur first, and any occurrence of colour `c` requires an earlier
occurrence of `c-1`. They allow boundaries using fewer than four colours, and
every proper colouring has exactly one representative after a global palette
permutation. Appending one 19-literal exclusion clause for each listed word
and proving UNSAT therefore establishes completeness, not just AllSAT search
coverage.

The block-gluing equivalence is also exact. A full colouring restricts to a
state in both block relations after one common normalization. Conversely,
equal normalized words mean the two chosen block colourings agree literally
on `Q`; they paste because the block interiors have no cross edge. Interior
colours remain unrestricted. Consequently, for arbitrary left and right
selector sets, four-colourability is equivalent to nonempty intersection of
their boundary relations. This is materially stronger than compatibility with
a fixed colouring or Kempe family.

## Reproduction and independent evidence

I replayed the complete target verifier with Python 3.11.2, Kissat 4.0.4, and
drat-trim. It regenerated both completeness CNFs and fresh proofs. The
mandatory formula has 1,496 variables and 10,395 clauses; its 1,948,302-byte
proof has SHA-256
`988370d09146bf62f578af47b9e850c9ef44f086286d90d9a1d8e2353557e1ec`.
The full formula has 1,532 variables and 10,566 clauses; its 1,380,935-byte
proof has SHA-256
`776091bdd55179909c36b349f071c2b861411b4165ee3b161b7f0bd3686c558e`.
drat-trim returned `s VERIFIED` for both. An optimized structural run agreed,
and all six mutations were rejected.

[`independent_check.py`](independent_check.py) imports no target producer or
verifier. It reuses the pinned dense-basis geometry implementation from the
preceding independent selector review, then independently checks the separator
and matching, all 176,704 witness-edge inequalities, and every state word. It
reconstructs both CNFs byte for byte and reproduces their hashes, dimensions,
state-stream hashes, and strict 20-state/72-state inclusion. It also extends
the normalization truth-table control from word length five to seven (21,844
words).

From the repository root:

```sh
python3 hadwiger_nelson_heule560_separator_review1/independent_check.py
python3 -O hadwiger_nelson_heule560_separator_review1/independent_check.py
sha256sum -c hadwiger_nelson_heule560_separator_review1/SHA256SUMS
```

The independent checker pins the reused geometry checker by SHA-256. It records
the DRAT identities but does not replay them itself; the native proof replay is
the separate target-verifier command described above.

## Novelty, readiness, and trust boundaries

This is a problem-specific decomposition and exhaustive interface computation,
not a general-method or historical-priority claim. It is publication-ready as
a computational lemma and can now serve as an independently reviewed premise
for the left-selector reduction. A final exposition should state clearly that
72 and 20 count normalized boundary colourings with arbitrary block-interior
recolouring, not complete graph colourings or inequivalent H560 supports.

Imported trust remains in the accepted M492/U68 support theorem for the
campaign corollary, pinned coordinate sources, squarefree-radical basis
independence, Python integer/rational semantics, Kissat proof production,
drat-trim's checking kernel, and ordinary hardware. The core 72/20 boundary
classification itself does not rely on the M492 deletion-sweep completeness;
that parent is needed when translating the interface into the order-508 target
family. The review uses no second DRAT kernel or proof assistant.

## Strengthening and improvement opportunities

The later reviewed left-selector theorem already reduces the interface to the
presence of vertex 310. The next mathematical step remains a complete
right-block relation on 59 selectors against both `P72` and `P20`. A compact
minimal-obstruction antichain, with independently checkable negative proofs,
would be much more valuable than additional fixed-colouring templates.

For publication, include the normalization lemma immediately before the CNF
definition and a small dependency table separating: exact geometry and
separator, positive state witnesses, DRAT completeness, gluing, and the
imported M492 campaign reduction. That prevents the solver exhaustions from
being mistaken for a search over all H560 selector combinations.
