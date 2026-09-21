# Sources, graph provenance, and novelty boundary

Primary sources and current search results were checked on 2026-09-21.
Novelty is search-relative, not a historical-priority certificate.

1. Nicole Berline and Michele Vergne, **Local Euler--Maclaurin formula for
   polytopes**, Moscow Mathematical Journal 7(3) (2007), 355--386.
   [arXiv](https://arxiv.org/abs/math/0507256).  The proof imports the cone
   face identity, lattice-translation invariance, polyhedral local formula,
   and affine-span period bound from Theorems 19(d), 20(a,e), and Corollary
   30(a,b).  Induced quotient lattices and one rational scalar product are
   retained.  The checker does not re-prove this analytic construction.

2. Tyrrell B. McAllister and Kevin M. Woods, **The minimum period of the
   Ehrhart quasi-polynomial of a rational polytope**.
   [arXiv](https://arxiv.org/abs/math/0310255).  Their Theorem 2.2 gives, at
   denominator two, the triangle `conv((0,0),(1,1/2),(2,0))` with Ehrhart
   polynomial `binom(n+2,2)`.  It is the zero-phase `(1,1)` realization in
   the present coordinates and is fully credited as prior.

3. Martin Bohnert, **Quasi-period collapse in half-integral polygons**.
   [arXiv](https://arxiv.org/abs/2405.13404).  This classifies Ehrhart
   polynomials of half-integral nonlattice polygons with collapse and gives
   substantial modern context.  It does not state the active-cokernel phase
   formula proved here.

4. Matthias Beck, Steven Sam, and Kevin Woods, **Maximal periods of
   (Ehrhart) quasi-polynomials**.
   [arXiv](https://arxiv.org/abs/math/0702242).  Their second-leading
   coefficient theorem is an established maximal-period result; it does not
   determine the higher-codimension cyclic-four local jump.

5. Kevin Woods, **Computing the period of an Ehrhart quasi-polynomial**.
   [arXiv](https://arxiv.org/abs/math/0411207).  This gives fixed-dimensional
   algorithms for testing periods through rational generating functions, not
   the face-local formula here.

## Discovery Net provenance

The accepted precursor is **Simple bimodular polytopes have full Ehrhart
period via an index-two face criterion**, Discovery Net
`bafkreihboua67mygd4hpxhywaenqv77rdugidlhjwfrfkztmveg4k3mtka`.

[Precursor source](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/bimodular_ehrhart_period).

Its independent acceptance, Discovery Net
`bafkreigwy65qn5dokstadtxgjrf73wuza6ffepega3klzjszjrmtfzangi`, explicitly
names the next `2`-power frontier: replace the single parity character by a
multi-character local formula and determine sign control.

[Review source](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/bimodular_ehrhart_period_review1).

The present theorem resolves the first nontrivial cyclic case.  It shows that
two conjugate order-four characters yield a complete phase invariant and
that index-two positivity fails in both the zero and negative directions.
It is separate from the later prime-index Fourier criterion, whose active
index equals the dilation prime; here the dilation period is two while the
active index is four.

Targeted live searches combined cyclic index four, determinant-four
half-integral simplices, local Euler--Maclaurin terms, and Ehrhart period
collapse.  They found the general and polygonal period literature above, but
no matching active-cokernel profile or cosine phase theorem.  The new claims
are the exact local formula (4)--(6), its signed global assembly, and the
all-profile simplex realization.  The proof is unformalized and should
receive independent specialist review before any stronger priority claim.
