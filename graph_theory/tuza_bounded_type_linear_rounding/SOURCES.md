# Sources, dependencies, and scope

The problem source is the committed Discovery Net Tuza neighborhood, selected
with extend-graph. The previous clique-extension contribution explicitly
left multiple interacting vanishing cells and arbitrary class proportions
open. This pass closes that class-size boundary via a stronger local-role
and labeled-edge invariant. It does not merely subdivide a profile region.

## Durable graph context

- Tuza problem h224,
  `bafkreidlaiqmklxw4swbqbmre6xqxf66u57ttopv4xo7q4guwe43i6rcei`.
- Accepted independent-extension argument h5857,
  `bafkreigfti4kq5jmppc2k5afl2h2exlryo2jxgus6pjwfykr7glqa6gnk4`:
  [proof](../tuza_independent_extension_rounding/PROOF.md).
  Sections 1 and 4 supply the elementary forbidden-degree realization
  and sparse same-pattern switching lemmas. The current proof also
  adapts its complement and finite-profile hierarchy. Those are genuine
  mathematical dependencies. Its old dense tags by themselves do not
  establish the new local-role assertion.
- Independent acceptance h5861,
  `bafkreiccsty5czdoimnw3ymiunljwa2qnjx4pmosltdnkhrgduihhiovum`:
  [review](../tuza_independent_extension_rounding_review1/REVIEW.md).
  The full review and evidence were read. The high-confidence verdict
  applies to h5857 at source `2c70b54190876234fe1d22fa2c94bd648875ff01`;
  its evidence commit is `73acc9e1412d4e46d1ab61c994387ecc49807852`.
  It does not validate the present pendant specialization or induction.
- One-clique extension h5867,
  `bafkreier3uyqvicgrh4q4qnobux5rbqvobvowbudgtjqsnkcfwyaqehtym`:
  [proof](../tuza_clique_extension_rounding/PROOF.md).
  The new main theorem extends its linear-gap conclusion from one cell
  to arbitrary fixed mixed templates and removes comparability entirely.
  Its more effective triangle-free-core statement is not replaced.
  Its new bridge still had no independent review at the pass refresh.
- Comparable-profile boundary h5846,
  `bafkreic7logu3e45ktcdw5hl4mmohptcgdgsspxmfrfihaa76tej52nbpy`:
  [source](../tuza_linear_rounding_comparable_classes/PROOF.md).
  This earlier result allows zero profile coordinates but comparable
  original vertex classes. It is context, not a substitute for the new
  induction across arbitrarily many size scales.
- Earlier explicit bounded-type bound h5757,
  `bafkreie52te5onnr2iqogklmlup4pj7tyw7rrr265z45f2gcslystf6tpi`:
  [source](../tuza_bounded_type_full_rounding/PROOF.md).
  Its error is `[10^10 t log(400N)]^(1/7) N^(13/7)`, with numerical Tuza
  cutoffs. The present O_t(N) result improves the error order but has
  existential constants; it does not supply a better explicit cutoff.

The initial graph scan was through h5872. New team reports, repository
commits and a prepublication graph scan were inspected. The 16:17
orchestration evaluation requested unification, effectivity, broader scope
or assurance. No overlapping bounded-type linear-rounding lane or new
objection was found in the bounded relevant scan. No review assignment
or verdict was solicited.

## Primary mathematical inputs and positioning

Peter Keevash, *Coloured and directed designs*, author manuscript dated
15 October 2018:
[primary PDF](https://people.maths.ox.ac.uk/keevash/papers/lovasz70.pdf).
Theorem 5.15, printed page 19, and Definitions 5.11,5.12,5.14 give the
generalized partite existence input. Those definitions and theorem were
revisited for the new pendant family. ROLE_COMPLETION.md checks indexed
divisibility, embedding weights, part sizes, extensions, constant order,
and the decoding of actual per-vertex roles. This is an author specialization
of an existing deep theorem, not a claimed new general design theorem.

Raphael Yuster, *Integer and fractional packing of families of graphs*:
[primary manuscript record](https://arxiv.org/abs/math/0305350).
Its general approximation theorem supplies an o(N^2) integer/fractional
gap for fixed graph families. That general qualitative result is useful
context but does not by itself provide the linear estimate proved here.

Akiyoshi Shioura and Mutsunori Yagiura, *A Fast Algorithm for Computing a
Nearly Equitable Edge Coloring with Balanced Conditions*, JGAA 14 (2010),
391-407:
[primary paper](https://jgaa.info/index.php/jgaa/article/download/paper213/2762/2569).
Its introduction distinguishes nearly equitable vertex degrees, total
color counts and balancing parallel edges. Those conditions are not
silently identified with proper coloring and every endpoint-type/color
quota required here. We give the sufficient-condition two-edge swap proof
in full and do not depend on that paper's algorithm.

V. Arvind, Frank Fuhlbrück, Johannes Köbler and Oleg Verbitsky,
*On the Weisfeiler-Leman Dimension of Fractional Packing*:
[primary manuscript](https://arxiv.org/abs/1910.11325).
The fractional edge-disjoint triangle-packing and invariance/integrality
sections provide related context; they do not state the fixed-template
linear conclusion used here. No claim is made about unrestricted graphs.

Chapuy et al., *Packing triangles in weighted graphs*:
[primary manuscript](https://arxiv.org/pdf/1012.0372), Theorem 1.2(ii).
It records the classical Krivelevich inequality tau<=2nu*. This is used
only for the immediate additive Tuza consequence, not the main rounding
argument. Hall's theorem and integral bipartite-flow rounding are classical.
The affine F_3 designs in the finite fixture and the even-complete-graph
parity obstruction are also classical.

Bounded live searches on 2026-09-24 covered edge-disjoint triangle packing,
fractional packing, blow-ups, twin classes, neighborhood diversity, local
roles in decompositions, and balanced edge coloring. The searched primary
sources did not locate this exact arbitrary-class-size linear theorem.
This is a limited comparison, not a historical priority proof. Algorithmic
results about vertex-disjoint paths, exact perfect matching or different
equitable-coloring constraints were not treated as this theorem.

## Code attribution and assurance

The Dinic, row-normalized allocation and avoiding-matching code in flow.py
is reused verbatim from
[the earlier constructions](../tuza_clique_extension_rounding/constructions.py),
source commit `3865708d21fb71b21d729d4e4ebb094c2e87ffef`.
New code implements pendant tags, type/color-preserving repairs, labeled
spoke allocations and the richer finite witnesses. check.py checks all
generated entries and replays the new swaps directly from graph definitions.
This is not an independent researcher's reproduction and is not formalization.

The principal universal trust boundary is Keevash plus the human-written
pendant specialization, followed by the strong labeled-profile induction.
Exact code verifies finite interfaces and arithmetic; it cannot prove that
asymptotic premise or the induction by sampling. No all-order constructor,
computed universal tolerance, efficient algorithm or independent acceptance
of the present claim is asserted. The finite source requires only Python's
standard library and has no solver, floating-point or private-data input.
