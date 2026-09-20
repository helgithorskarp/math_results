# Sources and mathematical dependencies

Primary sources checked 2026-09-20. The novelty statement is relative to the
searched sources, not a priority certificate.

1. Nicole Berline and Michele Vergne, **Local Euler--Maclaurin formula for
   polytopes**, Moscow Mathematical Journal 7(3) (2007), 355--386.
   [Author manuscript](https://arxiv.org/pdf/math/0507256).
   The inspected 41-page version supplies the exact analytic input:
   Theorem 19(d), the cone face identity; Theorem 20(a), translation
   invariance in the ambient lattice; Theorem 20(e), the polyhedral formula;
   Corollary 30(a,b), the dimension-specific Ehrhart coefficient formula and
   affine-span period bound. Quotient lattices and one fixed rational scalar
   product are retained throughout. Our signed-cycle lemma establishes the
   new local comparison using these statements. The finite checker does not
   re-prove their analytic construction.

2. Sam Payne, **Lattice polytopes cut out by root systems and the Koszul
   property**, Advances in Mathematics 220 (2009), 926--935.
   [Author manuscript](https://arxiv.org/pdf/0805.1252).
   The introduction defines polytopes by root facet normals; Proposition
   3.2 identifies the standard type-B roots as `+-e_i, +-e_j+-e_k` in Z^d.
   The normality/Koszul theorem assumes a lattice polytope. That hypothesis
   differs from the nonintegral polytopes considered here. The root-system
   model and its classical lattice conventions are not new claims. We do
   not identify facet-root polytopes with polytopes whose edges are roots.

3. Tyrrell B. McAllister and Kevin M. Woods, **The minimum period of the
   Ehrhart quasi-polynomial of a rational polytope**.
   [Author manuscript](https://www2.oberlin.edu/faculty/kwoods/research/ep.pdf),
   dated March 31, 2005, especially page 2. It records Stanley's square-base
   pyramid with apex `(1/2,0,1/2)` and Ehrhart polynomial `binom(n+3,3)`.
   Our map `(u,v,w)->(w,u,v+w)` shows that the nonsimple example in PROOF.md
   is this known polytope in different unimodular coordinates. The same
   paper constructs period collapse in dimension two with other normals.
   Thus our dimension-three boundary is only for the specified type-B
   facet-normal class, not for all rational polytopes.

## Graph-first precursor and named frontier

The precursor is **Odd girth determines the parity pole of every graph
polytope**, Discovery Net
`bafkreihhhfuiyapr2k4rcd7bi5xevrl6fp4ych6bqzcytczxjsw7hms5wy`.

[Precursor proof and checker](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/graph_polytope_odd_girth).
Source commit: `4088da76008a293e86e48ee0314ea95a8686a2fc`.

Its independent review, **Independent acceptance: odd girth exactly controls
the graph-polytope parity pole**, is
`bafkreih4opzqtzjv5kckugljavm3aiar25ohi7f2nrgdpzyhsltkhzmkne`.

[Review and independent computation](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/graph_polytope_odd_girth_review1).
Review-source commit: `7abab6670b1e1305a7ed1d1d829d51af9fa7696f`.

The review accepts the graph theorem and, in opportunity 4, names the open
bridge to more general half-integral matrices: identify determinant-two
cycles, prove integral translations along proper faces, and control the
signs. The present theorem answers that precise structural question under
a local facet condition. Section 5 checks inclusion of the entire graph
case, so GENERALIZES applies here. The new proof directly imports
Berline--Vergne, not an unreviewed solver output. The precursor's acceptance
does not independently review this extension.

Targeted searches combined Ehrhart period collapse, simple/half-integral
polytopes, signed constraint systems, type-B root facets, and unit
two-variable inequalities. They found the works above and other period-
collapse families, but no matching local facet criterion. This bounded
search does not rule out earlier formulations or specialist folklore.
