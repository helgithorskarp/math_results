# Attribution and literature audit

Checked 2026-09-21.

1. Jineon Baek and Martin Balko, *The Erdős--Szekeres Conjecture Revisited*,
   SoCG 2025, LIPIcs 332, 13:1--13:15,
   [publisher record](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2025.13),
   [full text](https://drops.dagstuhl.de/storage/00lipics/lipics-vol332-socg2025/html/LIPIcs.SoCG.2025.13/LIPIcs.SoCG.2025.13.html).
   Definition13 and Lemma14 supply the general nonuniform construction,
   its feasibility constraints, polygon avoidance, and size formula.
   Section6.1 includes an equality construction at factor k=N+1 for
   arbitrary seeds. Those ingredients are theirs. Our contribution is
   the convex-interval certificate, unconditional convex-seed upper bound,
   and classification of all active equality parameters for that family.
   The prior decomposable-set theorem does not itself assert closure under
   the almost-vertical blow-up operation; we make no such closure claim.

2. Baek and Balko, journal version, *Journal of Combinatorial Theory,
   Series A* 222 (August2026), 106195, DOI 10.1016/j.jcta.2026.106195.
   The publisher's search-indexed abstract was inspected and still calls
   the general conjecture open. A direct full-text request returned403,
   and the DOI resolver failed through the browsing tool. The accessible
   author/project pages did not supply a newer full manuscript. Therefore
   the journal version has **not** been fully audited for this theorem.
   No global priority claim is made. This explicit access limitation also
   applied to the earlier uniform-blow-up note.

3. Earlier campaign result,
   [Uniform-blow-up hereditary obstruction](https://github.com/helgithorskarp/math_results/tree/main/discrete_geometry/erdos_szekeres_uniform_blowup_obstruction),
   source commit 0b4c5b98f2727f39fa87f50f5d1cb01e444eb973,
   committed graph lemma
   `bafkreifch5tgknmrjs24csg2flivk5smfmiz57h4y5jtmel3ovnquinvjy`.
   Its independent accepted review is graph artifact
   `bafkreifwcrgm567fxgzp7vsovjp5cflpvcebh7qigj6p7l3x6bqowuwica`.
   That theorem extracts a smaller ES counterexample from a profitable
   uniform blow-up. It explicitly leaves nonuniform profiles outside
   scope. The present theorem is unconditional on its smaller geometric
   family and does not depend on that hereditary theorem.

The bounded primary-source search included the paper title with
“blow-up”, “convex”, “equality”, “monotone”, and “convex seed”. No identical
certificate or equality classification was found in the accessible
material. This supports a carefully scoped research note, not an assertion
that every relevant paper or the inaccessible journal text was checked.
