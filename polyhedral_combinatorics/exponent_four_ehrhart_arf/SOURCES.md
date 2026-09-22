# Sources and claim boundary

Checked 2026-09-22 after graph-first selection.

## Analytic and algebraic inputs

1. N. Berline and M. Vergne, *Local Euler--Maclaurin formula for
   polytopes*, Moscow Mathematical Journal 7(3) (2007), 355--386.
   [Primary full text](https://arxiv.org/pdf/math/0507256).
   In the inspected 41-page version, Theorem 19(d) and Theorem 20(a,e)
   give the cone identity and lattice-translation invariance. Corollary
   30(a,b) supplies the dimension-specific Ehrhart coefficient sum and
   the affine-span period bound. These analytic results are imported,
   not reproved by our code. The proof retains induced quotient lattices
   and a fixed rational scalar product.

2. R. Miranda and D. R. Morrison, *Embeddings of Integral Quadratic
   Forms*, authors' manuscript (2009).
   [Author-hosted text](https://web.math.ucsb.edu/~drm/manuscripts/eiqf.pdf).
   Chapter III, Section 1, gives classical Gauss-sum multiplication,
   radical reduction and vanishing (including Corollary 1.4 and Lemma
   1.5, printed pp. 78--79). Only that section was used here. Our proof
   includes the elementary binary specialization, including the sign
   convention for the Arf invariant. The quadratic-form classification,
   symplectic elimination and Gauss-sum evaluation are prior art.

3. T. B. McAllister and K. M. Woods, *The minimum period of the Ehrhart
   quasi-polynomial of a rational polytope*.
   [Primary manuscript](https://arxiv.org/abs/math/0310255).
   Theorem 2.2 contains the classical denominator-two collapsing
   triangle. Existing collapse examples and their standard constructions
   are not novelty claims of this package. The source distinguishes
   denominator from minimum quasiperiod.

4. M. Bohnert, *Quasi-period collapse in half-integral polygons*.
   [Primary manuscript](https://arxiv.org/abs/2405.13404).
   This is contemporary context for classification of half-integral
   polygon collapse; our theorem concerns local active cokernels in
   arbitrary dimension, under explicit local simplicity assumptions.

## Committed graph inputs

The direct precursor is **Cyclic active cokernels give an exact Ehrhart
parity formula and index-four phase classification**, graph
`bafkreifl35gwaspdsy3ecdxnrz4rbfgn7kqa6xibu23tnlpqo6m34gwmy4`.
[Proof and source](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/cyclic_four_local_period).
It explicitly leaves noncyclic cokernels unresolved. We reuse its geometric
local character reduction, now with a general finite abelian character
filter, and credit its all-profile simplex construction. Our theorem
extends its order-four phase classification, but does not contain its
all-even-order cyclic result.

The earlier accepted index-two criterion is **Simple bimodular polytopes
have full Ehrhart period via an index-two face criterion**, graph
`bafkreihboua67mygd4hpxhywaenqv77rdugidlhjwfrfkztmveg4k3mtka`.
[Source](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/bimodular_ehrhart_period).
Its [independent review](https://github.com/helgithorskarp/math_results/tree/main/polyhedral_combinatorics/bimodular_ehrhart_period_review1),
graph `bafkreigwy65qn5dokstadtxgjrf73wuza6ffepega3klzjszjrmtfzangi`,
names a dual-code/Walsh sign-control bridge for higher two-power index.
Our group obstruction shows why a noncyclic elementary-two active quotient
cannot itself occur at a locally simple minimum bad face. Exponent four
admits noncyclic quotients and leads to the binary quadratic invariant.
These prior acceptances do not review the present theorem.

## Scope of the contribution

The potentially new claims are the geometric exponent-four group
restriction and the resulting uniform radical/Arf criterion for exact local
Ehrhart parity, with its all-profile simplex collapse consequence. Abstract
finite-group character filtering, weight enumerators, binary quadratic
forms, Arf invariants, and the underlying Euler--Maclaurin machinery are
not new. The implementation supplies a compact binary certificate for this
application, not a new general quadratic-form algorithm or a polynomial-time
algorithm for finding all minimum bad faces.

The live search combined Ehrhart parity/period collapse, noncyclic active
cokernels, exponent four, binary codes, quadratic Gauss sums and Arf
invariants, and checked the cited primary sources. No matching complete
local criterion was located. This is a bounded-search observation and does
not certify historical priority. The arbitrary-exponent, nonsimple and
lower-coefficient cancellation problems remain outside the claim.
