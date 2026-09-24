# Sources, dependencies and claim status

## Graph-first target

The bounded committed scan at height 5862 found a high-confidence
independent acceptance of the preceding independent-extension theorem.
That review explicitly identified growing clique cells with superlinear
internal edge count as an untreated boundary. The target here was selected
from that boundary using extend-graph, with math-research, the combinatorial
approach and exact research code.

- Tuza root h224:
  `bafkreidlaiqmklxw4swbqbmre6xqxf66u57ttopv4xo7q4guwe43i6rcei`.
- Prior independent-extension result h5857:
  `bafkreigfti4kq5jmppc2k5afl2h2exlryo2jxgus6pjwfykr7glqa6gnk4`.
  [Proof](../tuza_independent_extension_rounding/PROOF.md) and
  [dense interface](../tuza_independent_extension_rounding/DENSE_COMPLETION.md).
  Its Section 4 balanced-deletion lemma is a mathematical dependency of
  Theorem 1 here. Theorem 2, with triangle-free core, does not use it.
- Independent acceptance h5861:
  `bafkreiccsty5czdoimnw3ymiunljwa2qnjx4pmosltdnkhrgduihhiovum`.
  [Full review](../tuza_independent_extension_rounding_review1/REVIEW.md)
  at source commit `73acc9e1412d4e46d1ab61c994387ecc49807852`, accepting
  the exact prior source commit `2c70b54190876234fe1d22fa2c94bd648875ff01`.
  The full assessment and graph body were read. Its verdict does not transfer
  to the new growing-clique construction.
- Earlier comparable-profile boundary h5846:
  `bafkreic7logu3e45ktcdw5hl4mmohptcgdgsspxmfrfihaa76tej52nbpy`.
  [Source](../tuza_linear_rounding_comparable_classes/README.md), cited as
  context. No separate unreviewed statement from it is assumed.

The new claim is a proof attempt pending independent review. It depends on
the accepted balanced-deletion lemma and cites the review and preceding
boundary result. It does not generalize the arbitrary-multiplicity
independent-extension theorem in every hypothesis, so no such GENERALIZES
relation is asserted.

## Classical inputs

D. K. Ray-Chaudhuri and R. M. Wilson, *Solution of Kirkman's schoolgirl
problem*, Proceedings of Symposia in Pure Mathematics 19 (1971), 187–203,
establish existence of resolvable Steiner triple systems at every admissible
order `v=3 mod 6` (the order-three design is immediate). The theorem was
checked in Ray-Chaudhuri's primary author report, *Recent Developments on
Combinatorial Designs*, ICM 1970, volume 3, pp. 223–227: its
[printed page 224](https://www.mathunion.org/fileadmin/ICM/Proceedings/ICM1970.3/ICM1970.3.ocr.pdf)
states this all-order result, and reference 10 identifies the paper. The
primary PDF was downloaded and those pages inspected; the 1971 chapter
itself was not retrieved. The affine systems in the checker are explicit
finite fixtures, not a proof or implementation of the all-order theorem.

V. G. Vizing's classical simple-graph `Delta+1` edge-coloring theorem is
used twice. The proof and deterministic fan/Kempe routine were previously
audited in the accepted independent-extension package. The functions
`edge_color`, `edge` and `require` in coloring.py are copied unchanged from
that package at commit `2c70b54190876234fe1d22fa2c94bd648875ff01`.
Proper-color-class equitability follows from the standard alternating-path
balancing argument, proved here by a decreasing squared-size potential.
Neither coloring fact nor the underlying algorithm is claimed new.

Integral bipartite flow with integer lower and upper capacities supplies
the spoke-rounding step. A row-normalized fractional assignment proves
feasibility; integrality gives exact row degrees and floor/ceiling column
bounds. The lower-bounded circulation implementation uses ordinary integer
augmenting flow. Hall's theorem supplies each dense bipartite perfect
matching, including after splitting the endpoint set of a loop type.
These are classical inputs; the quantitative discrepancy accounting and
increasing-quota assembly are the present bridge.

The general core-completion premise ultimately uses Peter Keevash,
[*Coloured and directed designs*](https://people.maths.ox.ac.uk/keevash/papers/lovasz70.pdf),
Theorem 5.15 of the 15 October 2018 author manuscript. Its full specialization
is in the prior linked dense-interface proof and was independently audited
at h5861. This package does not redo the universal existence theorem.

M. Krivelevich's `tau<=2nu*` inequality, recorded as Theorem 1.2(ii) in
Chapuy, DeVos, McDonald, Mohar and Scheide,
[*Packing triangles in weighted graphs*](https://arxiv.org/pdf/1012.0372),
gives the stated additive Tuza consequences. They are immediate corollaries.

## Novelty and scope comparison

Bounded primary-literature searches covered edge-disjoint triangle packing,
unbalanced blowups, bounded neighborhood diversity, clique extensions and
linear additive fractional-packing gaps. Vertex-disjoint packing papers and
clique-decomposition papers with unrelated meanings of "clique extension"
were distinguished from this problem.

Arvind, Fuhlbrueck, Koebler and Verbitsky,
[*On the Weisfeiler–Leman Dimension of Fractional Packing*](https://arxiv.org/abs/1910.11325),
provides related fractional-packing and integrality-gap context. Chahua and
Gutierrez, [*On Tuza's Conjecture in Dense Graphs*](https://arxiv.org/abs/2405.11409),
treat dense split and multipartite classes under different hypotheses.
The inspected sources did not state this growing-clique closure or its
explicit small-clique, triangle-free-core bound. This limited search does
not prove historical priority or exclude an equivalent consequence elsewhere.

The general theorem still assumes a comparable mixed core and one exceptional
clique with a single compatible neighborhood. It does not permit every
unbalanced bounded-type graph, several unrelated small clique cells,
arbitrarily larger clique extensions, arbitrary partial cross pairs, or
all split graphs. Theorem 2 has explicit constants because it needs no core
completion; Theorem 1 retains an existential constant and starting threshold.
The classical design, coloring, matching and flow theorems are not new.

An initially tempting shortcut was rejected: tagged dense decomposition fixes
global pattern counts and local lattice feasibility, not every actual
vertex-pattern count in the output. It does not by itself give the nearly
regular internal packing needed here. The resolvable design provides that
property with an independent argument. This is a limitation of that proposed
shortcut, not an objection to the earlier theorem.

The exact finite audits validate certificate entries and elementary identities.
The universal proof, all-order design existence and its asymptotic general-core
completion remain unformalized. No independent acceptance of this new result,
practical complete all-order implementation or Tuza resolution is claimed.
