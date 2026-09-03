# Independent audit of the disconnected Type-II branch in Dean k=5

## Verdict

This is a scoped review of Sections 8.1--8.4 and Propositions B.4--B.5 of
Elias Botsford, *Cycles of length divisible by five in graphs of minimum
degree five*, version 1.0.1
(<https://doi.org/10.5281/zenodo.22182448>).

**The normalization and disconnected-exterior elimination are verified with
high confidence.** I reconstructed the graph-to-state implications, checked
the imported degree/connectivity hypotheses, audited the all-order quotients
and every lifting/simplicity assertion, replayed the six distributed
disconnected-state programs, and implemented the decisive calculations
independently in Python. I found no gap in this branch.

This is not a verification of the main theorem. It assumes a zero-free,
triangle-free, nonbipartite Type-II 5-weak graph and does not validate the
bipartite-core branch, the triangle branch, Type I, the connected Type-II
frontier, the terminal carrier closure, or the periodic split-apex theorem.
It also relies on the published rooted-path and cycle-connectivity results
identified below.

## Structural and graph-to-state audit

Write

\[
F=J-\theta+uv,\qquad H=J-\theta=F-uv.
\]

Here \(F\) is 3-connected with minimum degree at least five, \(H\) is
zero-free, and only \(u,v\) can have degree four.

1. Deleting \(uv\) from the 3-connected graph \(F\) leaves a 2-connected
   graph. Bai--Grzesik--Li--Prorok's connectivity bound, applied with
   \(k=5,r=1\), therefore makes \(H\) 3-connected. A length-\(3\pmod5\)
   \(u\)--\(v\) path would close through \(u\theta v\) to a zero-cycle.
   Their even-residue corollary gives a zero-cycle in \(F\); because \(H\)
   has none, it uses \(uv\) and leaves a length-\(4\pmod5\) path in \(H\).

2. A globally shortest odd cycle \(O\) in nonbipartite \(H\) is induced and
   has odd order at least seven. A vertex outside \(O\) has at most two feet;
   two feet must be the ends of one literal two-edge arc. Otherwise replacing
   the appropriate odd arc by the two-edge contact path gives a shorter odd
   cycle or a triangle. Every cycle position has an exterior neighbor by the
   degree ledger.

3. Every exterior component has at least four distinct feet. Boundaries of
   order at most two contradict 3-connectivity. For a boundary 3-cut, the
   safe-deletion localization lemma forces all three positions to see each
   degree-four vertex. This contradicts either the two-contact law or the
   inducedness of \(O\), including the cases where one or both of \(u,v\)
   lie on \(O\).

4. The selected-root theorem has valid rooted hosts. An exterior component
   has at least three vertices. A chosen end-block cannot be a bridge because
   an open bridge vertex has component degree one and at most two cycle
   contacts; triangle-freeness then makes every selected 2-connected block
   have at least four vertices. Maximizing the selected root's contact count
   and then minimizing its ambient degree leaves at most one unrestricted
   nonroot. Chiba--Ota--Yamashita consequently supplies \(4-D_X\)
   admissible paths when the selected contact count is \(D_X\in\{1,2\}\).
   If a landing lies outside the block, the fixed cutvertex-to-landing
   continuation avoids the open block and shifts every length equally.

5. Two type-1 components give two three-residue ears with disjoint open
   interiors. For four distinct feet, the cyclic order supplies two disjoint
   connector arcs. If the selected feet coincide, the remaining connector
   arc avoids that common foot. Cauchy--Davenport makes the two three-sets
   sum to all of \(\mathbb Z_5\), so a simple zero-cycle results.

6. For a type-1 and type-2 pair, choose two distinct additional feet of the
   first component and one additional foot of the second. Keep only the
   selected attachment edges. This last relaxation is important: a landing
   vertex may have a second cycle contact, but deleting that unselected spoke
   preserves zero-freeness and maps the graph to singleton-contact rows. Thus
   at most six marked positions are needed. The internal path residues, both
   literal cycle arcs, all equalities, and the cyclic weak order give exactly
   the reduced \(1+2\) state of Proposition B.4. Every compatible state forces
   the type-2 landing to be the literal midpoint of its selected span. Applying
   this to every additional foot leaves at most three boundary positions,
   contradicting the four-foot bound.

7. For two type-2 components, each extra foot gives a locally admissible
   two-residue row. Any one row from each component lifts to paths with
   disjoint open interiors. Hence every one of the four cross-pairs from two
   distinct extra feet on each side is compatible, producing the projected
   \(K_{2,2}\) state of Proposition B.5. No cycle in this implication uses two
   paths from the same rooted family. Unselected second spokes can again be
   deleted, so the quotient has at most eight marks.

8. The all-order reductions are sound. Replace each unprotected positive gap
   between consecutive distinct marks by its least positive representative
   in \(\{1,\ldots,5\}\), keep every prescribed span-two arc literal, add five
   to an outside gap if parity must be reversed, and add ten if the order must
   be raised to seven. Equality, cyclic order, every marked arc residue, and
   the incidence of disjoint connector arcs are unchanged. The safe order
   lists are precisely the odd nonmultiples of five from 7 through 33 in the
   \(1+2\) case and through 43 in the \(2+2\) case.

9. I checked the final coverage deduction independently. The projection
   offset sets permit no component pair at phase two; only coincident or
   adjacent bases at phase one; only coincident bases at phase three; and, at
   phase four, only coincident bases, an adjacent pair, a phase-two pair, or
   three consecutive bases. The corresponding unary landing restrictions and
   the adjacent-pair disjunction always leave a literal cycle position outside
   every possible boundary. The Python checker exhausts all compatible base
   cliques and both sides of every adjacent disjunction rather than hard-coding
   a witness uncovered position.

It follows that a nonbipartite normalized Type-II deletion graph cannot have
a disconnected exterior relative to a globally shortest odd cycle.

## Independent computation

`audit_disconnected.py` uses only the Python standard library and imports no
supplement code or data. It directly implements the displayed definitions of
the reduced \(1+2\) rows, literal oriented arcs, local closures, and simple
cross-component connector pairs. At all 12 representative orders its survivor
counts agree exactly with the distributed formula implementation. It then
derives the global \(2+2\) noncoverage result from the stated Proposition B.5
projection table by exhausting all compatible base sets and every collective
adjacent-pair alternative.

Run with Python 3.11 or newer:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 audit_disconnected.py
```

The final output is:

```text
PASS Dean-5 disconnected Type-II audit
1+2 reduced survivors: 531; nonmidpoint: 0
2+2 base/branch cases: 103; fully-covered: 0
```

I also freshly ran the six distributed disconnected-state programs under
Node.js v22.23.2. Both \(1+2\) implementations reported zero nonmidpoint
survivors; both \(2+2\) projection implementations passed every listed order.
The primary \(2+2\) run returned exactly the offset sets in Proposition B.5.
All 86 entries of the supplement manifest matched before execution.

The reviewed versioned files had SHA-256 values

```text
5e06b1e307b0b48c463bddf2880fdb3e9185e9b51f2740f5057e3f14e7aad7e2  dean5-source-v1.0.1.tex
abc41317fa70bc781b4b714b2ecf980eeeaf703a3e013aba25641a0779821f18  dean5-paper-v1.0.1.pdf
75b604acc53a38622e0fffddebcb27e3e883f5836d7da7e7ddb45c8378eebed5  dean5-computational-supplement-v1.0.1-upload.zip
```

The supplement is archived at
<https://doi.org/10.5281/zenodo.22167084>. The replay establishes its finite
predicates only; the graph-to-state, quotient, and coverage arguments were
audited separately above.

## External results, literature status, and trust boundary

The exact specified-vertex rooted-path theorem was checked against the primary
source of Chiba, Ota, and Yamashita:
<https://arxiv.org/abs/2008.09783>. The connectivity and even-residue
consequences were checked against Bai, Grzesik, Li, and Prorok:
<https://arxiv.org/abs/2511.03085>. I rely on those published results,
Cauchy--Davenport, and standard block and connectivity facts; I did not reprove
the imported theorems or formally verify this branch in a proof assistant.

Luo, Ma, and Zhao recorded the case \(k=5\) as open while settling \(k\ge6\):
<https://arxiv.org/abs/2601.13552>. A targeted arXiv search for Dean's
conjecture returned that paper and an unrelated paper about divisibility by
three or four; the corresponding Zenodo search returned only the reviewed
proof and supplement. The disconnected-state machinery therefore appears
potentially new, but absence from these searches is not proof of priority.

This branch is mathematically coherent and appears publishable after modest
expository strengthening. The full claimed solution should not be accepted on
this scoped result alone: every remaining branch and its universal
graph-to-state map still needs comparably explicit scrutiny.

## Strengthening and improvement opportunities

**Make the spoke-deletion relaxation explicit.** The body should say directly
that each chosen landing is represented by one actual attachment edge and all
other spokes at that landing vertex are deleted. This explains why the
\(1+2\)/\(2+2\) quotients have only six/eight marks even when the actual vertex
has two feet, and why singleton rows suffice for the graph-to-state map.

**Separate the projection-to-coverage lemma.** The finite \(2+2\) proposition
and the global noncoverage proof have different trust boundaries. Stating the
latter as a short standalone lemma, with the offset table and adjacent-pair
disjunction as hypotheses, would make the noncomputational conclusion easy to
reuse and independently formalize.

**Use a symbolic quotient certificate.** The bounded lists through 33 and 43
are correct, but the state depends only on equality, cyclic weak order,
protected span-two arcs, and gap residues modulo five. A canonical symbolic
gap-word certificate could replace the order lists and make the all-order
scope immediate. This is a proposed refactoring, not an additional theorem
proved here.

**Abstract the selected-root package.** The disconnected proof only needs
3-connectivity of \(H\), the two-low degree ledger, the shortest-odd-cycle
contact law, four feet per component, and the selected-root residue
reservoirs. Isolating these as hypotheses would yield a cleaner standalone
disconnected-exterior lemma and expose exactly which parts may generalize to
other odd moduli. Any such generalization would still require new finite
projection tables and is not claimed by this audit.
