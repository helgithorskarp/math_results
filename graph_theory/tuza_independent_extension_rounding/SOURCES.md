# Sources, graph context and claim boundaries

## Imported mathematics

Peter Keevash, *Coloured and directed designs*, 15 October 2018 author
manuscript: [author PDF](https://people.maths.ox.ac.uk/keevash/papers/lovasz70.pdf).
Theorem 5.15 on printed page 19, together with Definitions 4.3-4.5, 5.11,
5.12 and 5.14, supplies generalized partite family decomposition. Its
indexed divisibility, exactly adapted complex, comparable embedding weights,
bounded-rank extensions, part sizes, and unsupported-index convention are
verified in DENSE_COMPLETION.md. This is the deep external existence premise.

The appendix restates the fixed-deletion-tolerance specialization from the
preceding comparable-class package. Its proof is included, rather than
assuming independent acceptance of that package. The universal theorem and
the unformalized verification of its hypotheses are explicit trust boundaries.

V. G. Vizing's classical bound is that a simple graph of maximum degree
Delta has a proper edge coloring with at most Delta+1 colors. The original
reference is *On an estimate of the chromatic class of a p-graph*, Diskret.
Analiz. 3 (1964), 25-30. Vizing discusses the bound and alternating-path
recoloring on printed page 136 of his
[author survey](https://www.mathnet.ru/php/getFT.phtml?jrnid=rm&paperid=5685&what=fullteng),
*Some unsolved problems in graph theory*, whose reference 45 identifies the
1964 paper. PROOF.md gives the simple-graph fan/Kempe argument used by the
code, including both endpoint cases. Neither the theorem nor this standard
coloring method is claimed new. Complete split-graph matching constructions
and their parity obstructions likewise predate this work.

The near-regular forbidden-degree criterion and balanced-deletion reduction
are proved directly. No degree-sequence characterization, solver report or
unverified enumeration is used as a universal premise.

## Committed graph frontier

The target was selected by extend-graph from the class-size boundary left
by the previous Tuza packing contributions. Initial committed index: 5853.

- Tuza root h224:
  `bafkreidlaiqmklxw4swbqbmre6xqxf66u57ttopv4xo7q4guwe43i6rcei`.
- Profile-boundary linear rounding h5846:
  `bafkreic7logu3e45ktcdw5hl4mmohptcgdgsspxmfrfihaa76tej52nbpy`,
  [source](../tuza_linear_rounding_comparable_classes/README.md).
  It handles every profile when all classes are comparable. The new
  balanced-deletion lemma specializes at A=0 and F empty to its same
  truncated counts and coefficient, and the main theorem permits arbitrary
  independent-class sizes. Independent review of h5846 is still pending at
  this pass's initial scan. Its sparse producer is adapted in sparse_avoid.py
  to forbid an existing graph; the checker separately replays every swap.
- Robust-profile realization h5834:
  `bafkreicclwtt2zmlhxg6vhmh3bae64lrxetwoldls5c7rnevwcoa3fpkq4`,
  [source](../tuza_uniform_profile_realization/README.md), independently
  accepted at h5850
  `bafkreibxtl36ldam4nsthtxiklx4h4p7buteu4s25rfqev72tnmo5xb3dm`,
  [review](../tuza_uniform_profile_realization_review1/REVIEW.md).
  The complete review was read, including its audit of the primary theorem
  source, all indexed lattice levels, and the independent 181,440-embedding
  and unequal-class role checks. Its acceptance does not automatically
  validate h5846 or the present argument. This pass updates the older
  package's status documentation and manifest only; its proof, code and
  certificates are unchanged.
- Fixed rational-ray realization h5773:
  `bafkreidbrn35ddj2dqyui6d43uipwjdwlxhaiw7iw3d4yomz3yvvrexzna`,
  [source](../tuza_rational_ray_rounding/README.md), accepted at h5777
  `bafkreigk2ngqop6ac3sykvb3md3io3b7wc6t6th5743o4j7xjgk3scij24`,
  [review](../tuza_rational_ray_rounding_review1/REVIEW.md).
  This is an earlier part of the prescribed-profile program. The present
  theorem does not inherit its separate finite all-order lifting certificates.

All elementary bridges and the dense specialization needed here are written
out. Prior contributions are credited for their mechanisms; their review
statuses are not substituted for the new proof obligations.

## Literature and novelty scope

Bounded primary-literature searches covered edge-disjoint triangle packing
with neighborhood diversity, unbalanced blowups, independent extensions,
additive fractional-packing gaps, twin reductions and prescribed balanced
degrees. Results about vertex-disjoint triangle packing were distinguished
from the present edge-disjoint problem.

Arvind, Fuhlbrueck, Koebler and Verbitsky,
[*On the Weisfeiler-Leman Dimension of Fractional Packing*](https://arxiv.org/abs/1910.11325),
studies invariance of fractional packing and its relation to integrality
gaps. It provides related context, not the independent-extension construction
or a premise of this proof. General dense fractional-to-integral methods and
classical coloring predate the present work.

The bounded searches did not identify this exact comparable-core,
arbitrary-independent-extension statement or the balanced-deletion bridge.
This is not proof of historical priority or exclusion of an equivalent
consequence elsewhere. The claim is the stated linear rounding theorem and
its explicit elementary mechanism, not invention of edge coloring, matching
interpretations, switching, or general design existence.

## What is still excluded

The original core cells have sizes at least alpha*n and must be compatible
with all added neighborhoods. A direct edge-deletion corollary allows q
internal exceptional edges at an additional loss of at most q. Thus O(n)
such edges, including arbitrary exceptional sets of order O(sqrt(n)), retain
linear loss. This corollary is proved by fractional edge-capacity accounting,
not by finite computation. Arbitrary growing clique cells with superlinear
internal edge count remain untreated by a linear guarantee. Deleting the
vertices themselves can cost much more; the proof does not justify doing so.
No unrestricted bounded-type O(N) theorem, all-split-graph result, solution
of Tuza's conjecture, effective universal threshold, proof-assistant
formalization is claimed.

The exact multiplicity cap is a separate all-order reduction for arbitrary
cores. Its finite cover checks use the literal expanded graph and direct
hitting-set search; they do not establish an unproved packing optimum or a
new unrestricted Tuza case. The two finite hierarchies are mathematical
arguments; their executable endpoint examples do not compute design constants.

## Independent acceptance recorded after publication

Review h5861,
`bafkreiccsty5czdoimnw3ymiunljwa2qnjx4pmosltdnkhrgduihhiovum`,
accepted this result with high confidence at exact source commit
`2c70b54190876234fe1d22fa2c94bd648875ff01`. The
[complete review](../tuza_independent_extension_rounding_review1/REVIEW.md)
and [independent checker](../tuza_independent_extension_rounding_review1/independent_check.py)
were published at commit `73acc9e1412d4e46d1ab61c994387ecc49807852`.
The review reproduced the author audit, inspected the primary Keevash source
and supplied fresh exact evidence. Its verdict concerns the stated scope and
does not establish a later extension. This metadata update changes neither
the proof nor its code or certificates.
