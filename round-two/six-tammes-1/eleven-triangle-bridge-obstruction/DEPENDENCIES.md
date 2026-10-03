# Dependencies and exact scope

Actual author **six-tammes-1**, role **researcher**, pass23.
The local four-bridge obstruction is self-contained: ordinary contact-face
geometry and the compact polynomial certificate establish it. The
fifteen-point corollary additionally depends on9813's forest and cohort
result. All source pins are checked in [PINS.json](PINS.json).

Directed relations intended from this new lemma are:

|relation|destination|reason and scope|
|:---|:---|:---|
|ABOUT|PROBLEM7101|conditional reduction toward Tammes15, with no global bound|
|DEPENDS_ON|[LEMMA9813](../connected-map-filters/PROOF.md)|forest and original necessary size-profile screen used only in the fifteen-point corollary, retaining its entire physical cohort|
|REFINES|[LEMMA9849](../ten-triangle-bridge-obstruction/PROOF.md)|at least twelve faces and four bridging triangles instead of eleven; explicit application to induced selected subtrees on the same full-G20 closed band|
|CITES|[LEMMA9849](../ten-triangle-bridge-obstruction/PROOF.md)|earlier144 two-bridge cases and author-written exact dense/sparse kernels credited and reproduced; no claim that those cases are new|
|REFINES|[LEMMA9813](../connected-map-filters/PROOF.md)|nine necessary profiles under both additional G20 contacts and the narrower interval; its broader eighteen-contact eleven-profile result remains valid|
|CITES|[LEMMA9741](../annulus-rhombus-obstruction/PROOF.md)|origin of the full connected simple-disk convex-hemispheric T11/Q3/P3 physical cohort|
|CITES|[LEMMA9727](../../six-tammes-2/disconnected-core-obstruction/PROOF.md)|specified disjoint twelve-label eighteen-contact motif; neither its occurrence nor extra contacts follow from this citation|
|CITES|[LEMMA9774](../../six-tammes-2/twelve-core-frame/PROOF.md)|exact full twenty-contact interface and variable-frame context; no thirteenth-point G22 assumption or incumbent fixation|
|CITES|[REVIEW9809](../../six-reviewer-5/twelve-core-frame-audit/REVIEW.md)|independent confirmation and positive flexible full-G20 family; its verdict does not transfer to9813,9849 or this new lemma|
|CITES|[LEMMA9828](../../six-tammes-2/twelve-core-completion/PROOF.md)|complementary fixed-incumbent arbitrary-three completion and stability; stronger fixed positions and its additional contact are not assumed here|
|CITES|[LEMMA9866](../../six-tammes-2/twelve-core-local-gate/PROOF.md)|new sharper fixed-core stability and a small moving-frame arbitrary-three exclusion tube; independently unreviewed contextual work, with no tube or closeness premise imported into this tree theorem|

The program [poly.py](poly.py) is a byte-for-byte copy of the own9849 dense
kernel. [audit.py](audit.py)'s sparse arithmetic and Bernstein kernel were
adapted from the own9849 auditor. The new long-path enumeration, core
noncontact coverage, forward/reverse propagation, whole576-case binding,
range validation and semantic controls are supplied in this contribution.
The pins distinguish copied bytes from an adapted predecessor. No code or
unpublished result from another worker's workspace was imported.

The interval is exactly `c in [14/25,593/1000]`, with every pair product at
mostc and all prescribed contacts exactlyc. The selected triangular-face
adjacency is induced and is a tree. This excludes short connecting paths
in that tree, rather than excluding the full positive frame family or a
general cyclic triangle component. The entire9813 cohort is needed to
apply its forest conclusion:15 distinct unit points; complete contact
graph connected with minimum degree at least3; each actual face a simple
disk with3..5 distinct corners; each nontriangle geodesically convex and
individually in an open hemisphere; T11/Q3/P3. Every omitted global
coverage/forcing premise remains a research problem.

The tree-contraction, support, disk, reflection and branch-coverage bridges
are ordinary author-written proofs. Exact computation uses Python3.12
arbitrary-precision integers and `fractions.Fraction`, standard library
only, with the twelve executed entrypoints in [VALIDATION.json](VALIDATION.json).
Separate algorithms and damage controls do not constitute independent
researcher review or formal verification. No solver timeout, numerical
search or incomplete range is interpreted as a mathematical exclusion.
