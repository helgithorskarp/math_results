# Independent review: bounded H560 global decision

## Verdict

**Accepted with high confidence at its stated scope, conditional on the
already reviewed M492/U68 and exact 72/20-state separator theorems.** The 35
positive covers do force selectors 310, 393, and 578 in every obstruction and
close the whole 310-absent family. The combined checked refutation establishes
all 80 negative supports; the specified 516-vertex support is five-chromatic
and vertex-critical. The displayed cylinder really gives 194,580 exact
508-vertex supports outside the published positive and negative cones.

The last statement means **unclassified by these certificates only**. None of
those 194,580 graphs is proved non-four-colourable. The complete H560 family
is not closed, no graph on at most 508 vertices is produced, and the
five-chromatic record remains 509 vertices. “NO GO” is a sound workflow
recommendation for the unchanged bounded pilot, not a mathematical
impossibility theorem about further certificates or other methods.

Reviewed Discovery Net claim:
`bafkreihataf6q7i32e5ehv5sooyyqc7hoyl3vzi4ohjsei3cl3szxrk2gm`.
The source is pinned at commit
[`bff36887d06f5fdbf017380148419da5ce8f0935`](https://github.com/helgithorskarp/math_results/commit/bff36887d06f5fdbf017380148419da5ce8f0935),
directory
[`hadwiger_nelson_heule560_global_decision`](https://github.com/helgithorskarp/math_results/tree/bff36887d06f5fdbf017380148419da5ce8f0935/hadwiger_nelson_heule560_global_decision).

## Mathematical audit

Let `M` be the reviewed 492-vertex mandatory set and let the 60 surviving
selectors index `G552`. By the reviewed left-selector theorem, a selected
support is four-colourable exactly when its right-block boundary relation
meets `P72` if 310 is absent or `P20` if 310 is present. This is an imported
arbitrary-interior-colouring equivalence, not a template restriction.

Each positive row supplies a proper right colouring with an allowed boundary
word. Pasting the corresponding parent left witness gives a proper colouring
of the entire selected support. Restriction therefore colours every subset of
that row. Three verified size-59 covers omit exactly 310, 393, and 578. Any
obstruction must contain the omitted vertex from each cover; in particular,
the size-59 cover omitting 310 colours every 310-absent support. The earlier
eight-selector erasure equivalence transfers this conclusion from G552 back
to H560. Enlarging the mandatory set to 495 vertices and leaving at most 13
of the other 57 selectors at target size is valid.

The four-colour oracle has one-hot variables for all 196 right vertices and
60 selector variables. Every edge-colour inequality is guarded by the
negative selector literals of its optional endpoints, so the clause is active
exactly when both endpoints are present. Its 72 boundary gates pin the 19
separator colours, with at least one gate active. A boundary word outside
`P20` receives the clause

```text
not selector[310] or not gate[word].
```

Thus all `P72` words are available when 310 is absent and only `P20` words
when it is present. No right-interior colouring is fixed. The resulting oracle
has 916 variables, 6,017 clauses, and SHA-256
`4682363b5c0afd715b028e2214191f2710260a5c74c29cf89934ad538df6465e`.

For the 80 negative rows, an added case gate implies every selector in its
mask and at least one case gate must be true. Selectors outside a chosen mask
need not be false. This does not weaken the conclusion: a model colours a
supergraph of some negative support and restricts to that support; conversely,
a colouring of any negative support extends to the CNF by selecting exactly
that mask. Hence UNSAT is equivalent to all 80 asserted lower bounds. The
combined formula has 996 variables, 8,226 clauses, and SHA-256
`bde148aa4dc1d8e1ce8a378f2168a79f19fe84d028cb4b9fd8a9cf49649ef832`.

The checked inherited five-colouring gives an upper bound of five for every
negative support, so all 80 are exactly five-chromatic. Negative row 52 has
the claimed 24 optional vertices and hence 516 total vertices. Its 24 supplied
single-optional-deletion colourings are proper. Deleting any of the other 492
vertices is four-colourable by restricting the already reviewed parent
colouring of `H560-v`. These cases exhaust its vertices and prove
vertex-criticality. No edge-criticality or minimum-order assertion follows.

For the residual certificate, put

```text
F = {310,361,362,393,406,407,409,434,500,505,578,604}.
```

Direct containment checks show that no new positive cover and no earlier
Kempe cover contains F. Every exact-16 superset of F is therefore outside
their downward cones. There are exactly
`C(48,4)=194,580`. Since every certified negative support has at least 24
selectors, none lies inside an exact-16 support. This proves only that these
194,580 supports evade the published two-sided cone certificate.

## Independent computation and proof

[`independent_check.py`](independent_check.py) imports no target producer or
verifier. It pins the target source and reuses the earlier reviewer’s pinned
quadratic-tower geometry checker, which reconstructs all 199,396 H632
point-pair norms independently of the target’s sparse-radical implementation.
It then derives the 196-vertex right block, 806 right edges, 19-vertex
separator, and 60-selector domain.

The checker independently performs:

- exact full-graph validation of all 35 positive rows, totaling 27,529 right
  and 94,721 glued whole-graph edge inequalities;
- exact five-colour validation of all 80 negative supports, totaling 204,629
  edge inequalities;
- validation of all 24 optional-deletion witnesses, totaling 14,676 right
  and 60,748 whole-graph edge inequalities;
- a third byte-for-byte reconstruction of both CNFs, plus truth-table controls
  for guarded edges, `P20` gates, and negative case gates;
- validation of all ten older Kempe covers on 27,346 edge inequalities; and
- explicit enumeration of all 194,580 exact-16 supersets of F, checking every
  one against every published positive and negative cone.

Normal and optimized structural runs reproduce
[`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt). The target verifier was also
replayed in full: its seed-zero 1,596,382-byte DRAT proof regenerated with the
published hash and drat-trim returned `s VERIFIED`.

For a genuinely separate negative proof, reviewer-built Kissat 4.0.4 at
commit `8af8e56f174b778aef3aa45af9f739b2a5f492c2` was run with seed 29. It
produced a different 1,423,523-byte DRAT trace with SHA-256
`fe8a5848cbae349ec1909195872b74df5dddd9f0bc7e744996e30103f2668624`.
Reviewer-built drat-trim accepted it and emitted a 6,181,615-byte LRAT trace,
SHA-256
`72c5e9294117a823c402165ef7ab1c70bfcaba98eecf3b8224b1aefbf82e8b87`.
The separate lrat-check executable returned `c VERIFIED`. Binary identities
are recorded in [`NATIVE_PROOF.json`](NATIVE_PROOF.json). The large CNF and
proof traces remain reproducible scratch artifacts rather than Git objects.

From the repository root, reproduce the deterministic structural checks with
Python 3.10 or later:

```sh
python3 -B hadwiger_nelson_heule560_global_decision_review1/independent_check.py > actual.txt
diff -u hadwiger_nelson_heule560_global_decision_review1/EXPECTED_OUTPUT.txt actual.txt
python3 -O -B hadwiger_nelson_heule560_global_decision_review1/independent_check.py > actual-optimized.txt
diff -u hadwiger_nelson_heule560_global_decision_review1/EXPECTED_OUTPUT.txt actual-optimized.txt
sha256sum -c hadwiger_nelson_heule560_global_decision_review1/SHA256SUMS
```

Add `--prove --work NEW_DIRECTORY --kissat PATH --drat-trim PATH
--lrat-check PATH` to regenerate the independent seed-29 proof chain.

## Search-history boundary, readiness, and trust

I did not replay the 300-second MARCO pilot. Its raw query log and capped
terminal masks are intentionally absent from Git, so the reported 4,249
queries, 115 completed rows, and 4,097 terminal masks remain author-run
operational provenance. They are not premises of the positive covers,
negative proof, critical graph, forced-selector theorem, or explicit
194,580-support lower bound reviewed here.

The mathematical certificate is publication-ready as a computational
checkpoint. A paper should separate the accepted exact claims into positive
cones, negative supports, one critical graph, and residual lower bound, and
label the time-limited search statistics as nonreproducible provenance. This
is problem-specific computation rather than a general method or priority
claim.

Imported trust remains in the reviewed M492/U68 mandatory theorem, the
reviewed 72/20-state separator and gluing theorem, and the reviewed erasure
equivalence; pinned coordinate inputs; exact Python arithmetic; independence
of the quadratic basis; CNF encoding; the two native proof-checker kernels;
SHA-256 collision resistance; and ordinary hardware. The DRAT-to-LRAT route
reduces but does not eliminate native-checker trust. No proof-assistant
formalization is present.

## Strengthening and improvement opportunities

The decisive next object is a compact complete frontier for the remaining
exact-16 selector family, or a new family of large positive covers that cuts
through the explicit F-cylinder. Simply extending the same wall-limited
MARCO schedule has poor evidenced marginal value. The three forced selectors
should be treated as mandatory in any successor encoding, leaving 57 selector
variables and target cardinality at most 13; only the `P20` left relation is
then needed.

For publication, retain a small dependency table naming which conclusions use
the parent deletion theorem, separator completeness, fresh DRAT proof, and
positive witnesses. That will prevent the 516-vertex example from being
mistaken for a record and the 194,580 residual supports from being mistaken
for obstructions.
