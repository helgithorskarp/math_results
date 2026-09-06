# Simultaneous gluing of five heptagon–spindle components

**Exact computer-assisted theorem.** For the fixed H and M defined in the [coordinate specification](README.md), put

\[
 \eta=e^{2\pi i/3},\qquad \rho=(5+i\sqrt{11})/6,
\]

and take the following ordered five rotations:

\[
 (r_0,r_1,r_2,r_3,r_4)
   =(1,\eta\overline\rho,\eta,\overline\eta\,\overline\rho,\overline\eta).
\]

Let \(Y_i=H+r_iM\). The complete Euclidean unit-distance graph on

\[
 Z=\bigcup_{i=0}^4Y_i
\]

has **513 distinct vertices, 2,097 edges, and chromatic number four**. One explicit colouring works simultaneously on all five components and extends the previously used fixed colouring of Y_0. Consequently all 31 nonempty unions of these components are exactly four-chromatic, and every vertex- or edge-deleted subgraph of Z is four-colourable. In particular, deleting vertices from this 513-point support cannot produce the target graph on at most 508 vertices.

This is a finite five-orientation theorem. It does not assert colourability for other rotations, translated components, changed factors, or all possible sums. The full graph here is four-chromatic, so it is not a Hadwiger–Nelson record construction.

## Six exact graphs certify the union

The bounded milestone tested all six triple unions

\[
 T_{ij}=Y_0\cup Y_i\cup Y_j,\qquad 1\le i<j\le4.
\]

The four attachments are exactly the prior 252-angle cohort indices 34, 72, 116 and 117, in that order. They were selected because their baseline attachments had the largest observed exclusive cross-edge counts, 19 or 40. That selection is a heuristic choice of the finite cohort, not a completeness claim about promising rotations. Here their algebraic expressions above eliminate any dependence of the theorem statement on enumeration indices. The producer checks those expressions against the inherited indices; the checker constructs the expressions directly in another basis.

No symmetry quotient is used. The six reconstructed full graphs are:

| Attached components i,j | Vertices | Unit edges | Edges outside both baseline pair graphs |
|---|---:|---:|---:|
| 1,2 | 328 | 1,274 | 0 |
| 1,3 | 387 | 1,530 | 40 |
| 1,4 | 387 | 1,530 | 19 |
| 2,3 | 387 | 1,530 | 19 |
| 2,4 | 387 | 1,572 | 40 |
| 3,4 | 328 | 1,274 | 0 |

The last column counts edges belonging to neither G(Y_0 union Y_i) nor G(Y_0 union Y_j). All 118 occurrences are checked. Every triple has at most 387 vertices, as anticipated from the 143-point baseline and the at-most-122 new points contributed by each selected attachment.

**Pair-cover gluing lemma.** Suppose finite point sets Y_0,...,Y_k have prescribed colour functions. If a family of their unions contains each pair Y_i,Y_j, the colour prescriptions agree on every coincidence in each union, and the resulting colouring is proper on each union's complete unit-distance graph, then the prescriptions give a proper colouring of the whole union.

Indeed, two representations of the same point involve at most two components, which occur together in a checked union. Thus their colours agree. The endpoints of any unit edge likewise lie in at most two components, so their edge and its colour inequality occur in a checked union. Internal edges are covered whenever their component occurs. This proves the lemma.

The six triples above cover all ten pairs of the five components. A common component prescription is checked on every triple. Their point and edge sets can therefore be glued exactly to obtain G(Z), without a new distance scan over all pairs of the larger support. The checker compares the glued 513-point support, all 2,097 edges and the colouring entrywise. This is an application of the lemma to the same six checked graphs, not an unverified assumption that arbitrary separately chosen colourings can be combined.

Each nonempty component union contains a translated rotated spindle. The exact spindle edge list and the rejection of all 81 normalized three-colour assignments establish the lower bound four. Restriction of the common colouring gives the upper bound and the subgraph corollary.

## A common certificate and its compatibility structure

Colours are 0,1,2,3 with XOR as addition in F_2 squared. The [227-byte certificate](triples_certificate.json) gives the same H row as the prior baseline theorem,

```
0 1 0 2 0 1 3  1 3 3 0 2 2 0  2 2 1 1 3 0 2
```

and, for components 0 through 4 respectively, the spindle rows

```
0 1 2 3 1 2 0
0 1 2 0 2 3 1
0 2 3 1 1 2 0
0 1 2 0 3 1 2
0 3 1 2 1 2 0
```

On each formal point h_a+r_i m_b prescribe p_a XOR q_i,b. The checker verifies all geometric coincidences, all complete edge lists and every colour inequality. The rows are shared across all six graphs.

The full fixed-p, fixed-baseline XOR compatibility test explains why this cohort does not create a cyclic obstruction. All 96 proper spindle colourings with q(0)=0 are enumerated. The rows that extend the fixed baseline have domain sizes 10,6,10,6 on components 1,2,3,4. For four of the six attachment pairs, every pair of domain rows is compatible. The only restrictive relations are:

- Components 1 and 3: 67 allowed pairs out of 100.
- Components 2 and 4: 27 allowed pairs out of 36.

These relations involve disjoint variable pairs. Thus exactly **67 times 27 = 1,809** choices of the four rows are simultaneously compatible in this restricted class. The certificate selects the lexicographically first choice. This is not a count or a completeness claim for all four-colourings of Z.

[triples_compatibility.json](triples_compatibility.json) records the four domains and all six finite relations in 2,885 bytes. Both implementations compare them entrywise. The restriction graph on the four attachment variables is a matching, so the intended compatibility cycle is absent in this fixed class.

## Computation, independence and reproduction

[triples.py](triples.py) uses the exact 24-coefficient field arithmetic from the preceding construction, with t=e^(pi i/21), s=i sqrt(11), Phi_42(t)=0 and s squared=-11. It generates all six full graphs, all candidate colour relations and the shared witness. It glues the already generated graphs only after checking colour consistency. The local prototype agrees entrywise on every graph and compatibility relation.

[triple_check.py](triple_check.py) imports neither this producer nor its arithmetic. It uses the prior independent [tensor-basis checker](check.py), whose arithmetic is in the basis zeta^a omega^b w^c with zeta a primitive seventh root, omega squared=omega−1, and w squared=w−3. In this basis eta=omega−1, etabar=−omega and rhobar=(3−w)/3. It reconstructs the factors, the five prescribed rotations, all six full supports, all 2,646 formal labels, every edge and every colour inequality. It independently enumerates the 96 normalized spindle rows by recursive propagation and reconstructs the six compatibility relations and all 1,809 completions.

Both implementations scan 406,020 point pairs over the six triples, using different validated finite-field rejection maps. Every modular survivor is checked exactly in characteristic zero. Each obtains 8,710 exact unit edges across the six graphs, with no modular false positives. The checker verifies those 8,710 inequalities, all 118 new attachment-edge occurrences, the ten-pair cover and the glued 2,097-edge certificate. Four controls reject missing or duplicated cover cases, inconsistent component colours and an invalid global colouring.

The new exact claim relies on the injective number-field representation, ordinary Python integer arithmetic, complete finite loops, faithful decoding and the pair-cover lemma. There is no floating-point distance predicate, SAT premise, omitted negative proof or assumption that the original colouring library is complete. The new implementations are independently written and author-run; external review of this simultaneous theorem is pending. The [continuous single-sum theorem has now received independent acceptance](../hadwiger_nelson_heptagon_moser_rotation_family_review1/README.md), but its review explicitly does not cover unions of rotations.

From the repository root, using Python 3.11.2, standard library only, with assertions enabled:

```bash
python3 -B hadwiger_nelson_heptagon_coupled_sums/triples.py --out /tmp/hn-six-triples
python3 -B hadwiger_nelson_heptagon_coupled_sums/triple_check.py --work /tmp/hn-six-triples
```

The output directory must be new. Generation took 2.282 seconds and the audit 2.923 seconds, each using one thread; peak memory was not measured. Full generated graphs, colour-assignment lists and logs stay local and regenerate from source. Compact expected results and provenance are in [triples_expected.json](triples_expected.json) and [triples_validation.json](triples_validation.json).

- Common certificate SHA256: `d0577c3ca9871e7315af66d6a20dc3083b8061f2100a13c2a827b6a86032614a`.
- Compatibility certificate SHA256: `1732ea31f974a5ef22f596008b9e3c5f8fe6fab182fc213ba38c49768a7e0094`.
- Ordered triple-graph stream SHA256: `0f90401cebd4a36046492a59096d605df6ec492d3b8670c699647558875f08c0`.
- Glued graph and colouring SHA256: `44774cc86067756bbccd40d84f9a09d8a2672618bdd382f0d411a74dbeb4ce6f`.

## Decision and shared context

The selected five-orientation support, all its component subsets and all deletion-only refinements are closed. High cross-edge counts did not produce the sought compatibility cycle. This is a no-go result for this construction, not a reason to start another nearby angle cohort automatically. Further work should first justify a different geometric mechanism, such as changed relative translations or a different host, and derive a bounded decisive test before enumeration. No such next construction, background search or unfinished proof is in progress.

The parent 252-angle theorem is at source `0d969bf958f978d156e81fee807e70c6cc51d878`. The new independent single-sum review is at source `274d3df31b172e63f2b766e3c6d352a4a80e3211`, Discovery Net height 3144; it was inspected before this pass. The final shared refresh inspected HN2's [H517 four-large/five-small deletion closure](../hadwiger_nelson_heule517_large4/README.md), source `fe8f1593bcfec80c71adfc55f60b28d58428d70d`, Discovery Net height 3146. It establishes 490 mandatory vertices in that seed and, for obstructions on at most 508 vertices, at least 138 small vertices and five large deletions. Its unrestricted target family remains open. That support and certification lane are separate and supply no premise here.

The record calibration remains [Parts's primary 509-vertex construction](https://arxiv.org/abs/2010.12665), also described as the current record in [Haugland's August 2026 manuscript](https://arxiv.org/html/2608.04542v4). Both were checked live on 2026-09-06. The present result does not improve that record.
