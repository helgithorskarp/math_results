# Exact classification of Hamming-invariant 208-edge square-saturated subgraphs of Q7

## Result

Let

$$
\sigma(x)=\bigoplus_{i:x_i=1}(i+1)\in\mathbb F_2^3,
\qquad H=\ker\sigma,
$$

where the seven coordinate labels are the nonzero vectors of $\mathbb F_2^3$.
The earlier construction in
[`hypercube_square_saturation_q7`](../hypercube_square_saturation_q7/README.md)
proved that the minimum size of an $H$-translation-invariant square-saturated
subgraph of $Q_7$ is 208.  This directory gives the exact structure at equality.

**Classification theorem (finite exhaustive component).** There are exactly 224
$H$-translation-invariant square-saturated subgraphs of $Q_7$ with 208 edges.
They form one orbit under the normalizer of $H$ in $\operatorname{Aut}(Q_7)$.
Equivalently, the induced action of $\operatorname{AGL}(3,2)$ on the syndrome
quotient is transitive on the optima, and the stabilizer of an optimum has order
6.  Thus the 208-edge optimum is unique up to a cube automorphism preserving the
Hamming translation subgroup.

The quotient graph of every optimum has degree sequence

$$
(7,4,4,4,2,2,2,1)
$$

and is abstractly $K_1\vee(K_1\sqcup N_6)$, where $N_6$ is the *net graph*: a
triangle with one pendant leaf at each triangle vertex.  Across the 14 affine
planes of $\mathbb F_2^3$, its selected-edge counts have profile

$$
(n_0,n_1,n_2,n_3,n_4)=(3,0,0,5,6).
$$

No claim is made here about unrestricted square-saturated subgraphs of $Q_7$.

## Quotient reduction

Map the $Q_7$ edge $\{x,x+e_i\}$ to

$$
\{\sigma(x),\sigma(x)+(i+1)\}.
$$

This is a bijection from the 28 $H$-translation orbits of hypercube edges to
$E(K_8)$ on the syndrome space $\mathbb F_2^3$.  The 672 square faces split
into 42 free $H$-orbits.  Their quotient images are precisely the three
Hamilton 4-cycles in each of the 14 affine planes.

Consequently, an invariant hypercube subgraph is square-saturated exactly when
its quotient edge set contains no affine-plane 4-cycle and every omitted
quotient edge completes such a cycle.  Each selected quotient edge lifts to 16
hypercube edges.

There is also a short non-computational bound reducing optimality to weights 12
and 13.  If a square-free quotient has $m$ edges and an affine plane contains
$j$ selected edges, that plane can witness at most zero, one, or two omitted
edges according as $j\leq2$, $j=3$, or $j=4$.  It cannot have $j>4$.  Thus its
witness capacity is at most $j/2$.  Every quotient edge lies in three affine
planes, so

$$
28-m\leq \frac12\sum_P |E(P)|=\frac{3m}{2},
$$

and hence $m\geq12$.

The self-contained C++20 census checks all
$\binom{28}{12}=30{,}421{,}755$ weight-12 subsets and all
$\binom{28}{13}=37{,}442{,}160$ weight-13 subsets.  It finds no saturated set
at weight 12 and exactly 224 at weight 13.  As a stronger diagnostic, no
square-free weight-12 set witnesses more than 13 of its 16 missing edges.

## Explicit family

The census output has a compact parameterization.  Choose distinct
$p,u\in\mathbb F_2^3$ and an unordered basis $\{b_1,b_2,b_3\}$ satisfying

$$
b_1+b_2+b_3=p+u.
$$

Make $u$ universal.  Put a triangle on the three vertices $u+b_i$, and add the
matching

$$
p+b_i\;\mathord{-}\;(u+b_i),\qquad i=1,2,3.
$$

These are all the selected edges beyond the seven incident with $u$.  There are
four admissible unordered bases for each ordered pair $(p,u)$, giving
$8\cdot7\cdot4=224$ members.  The classifier proves that this explicit family
equals the exhaustive set of optima.  The canonical certificate takes
$p=0$, $u=7$, and basis $\{1,2,4\}$.

## Reproduction

Only a C++20 compiler and Python 3.11 or later are required:

```bash
g++ -std=c++20 -O3 -march=native -Wall -Wextra -Wconversion -pedantic \
  classify_affine_quotient.cpp -o /scratch/q7_affine_classify
/scratch/q7_affine_classify

python3 verify_canonical_family.py
```

On the recorded machine the exhaustive run took about 5.5 seconds.  Its main
output is:

```text
weight_12_examined: 30421755
weight_12_square_free: 9207240
weight_12_saturated: 0
weight_12_maximum_witnessed_missing_edges: 13
weight_13_examined: 37442160
weight_13_square_free: 6124832
weight_13_saturated: 224
explicit_family_size: 224
single_agl_orbit_size: 224
affine_stabilizer_order: 6
status: VERIFIED
```

The independent Python checker does not import or invoke the classifier.  It
reconstructs the explicit 224-member family and its affine orbit, expands the
canonical quotient to 208 edges of $Q_7$, enumerates all 448 host edges and 672
square faces, and checks square-freeness, saturation, and $H$-invariance directly.

## Hashes and trust boundary

```text
classify_affine_quotient.cpp:
  bce10769eaebcf761d73813cad834fc0866350586192a4dcf357d5f40a0f1a3d
verify_canonical_family.py:
  18f76c592e60bc87b375ff345687577da8d581c30d1e55fc0beaad7e057b0ce1
canonical_affine_quotient.json:
  842359f09591222feeef0d37ed0ef007890facac351ff7c0e330514fbf32a0c6
canonical expanded Q7 edge list:
  0b82210c5d616253d9291d35d5ef117213462b27c09810b7647a73ff6904db57
```

- The quotient bijection and the capacity bound above are mathematical arguments.
- The exclusion at quotient weight 12 and completeness at weight 13 depend on
  the auditable exhaustive C++ enumeration.  No SAT solver or proof log is used
  for this new census.
- The independent Python checker verifies the entire explicit family, affine
  orbit statement, and canonical upper-bound construction, but it does not
  independently repeat the 68-million-subset census.
- The previous checked-DRAT certificate independently excludes 12 or fewer
  quotient orbits; this package adds a direct census and the equality classification.
- No Lean formalization is claimed.

## Literature and novelty assessment

The underlying hypercube saturation problem was introduced by Choi and Guan,
and the Hamming-code method was developed in later asymptotic work:

- S.-Y. Choi and P. Guan, “Minimum critical squarefree subgraph of a hypercube,”
  *Congressus Numerantium* 189 (2008), 57–64.
  <https://combinatorialpress.com/cn/vol189/>
- J. R. Johnson and T. Pinto, “Saturated Subgraphs of the Hypercube,”
  *Combinatorics, Probability and Computing* 26 (2017), 52–67.
  <https://arxiv.org/abs/1406.1766>
- N. Morrison, J. A. Noel, and A. Scott, “Saturation in the Hypercube and
  Bootstrap Percolation,” *Combinatorics, Probability and Computing* 26 (2017),
  78–98. <https://arxiv.org/abs/1408.5488>

Concept and exact-phrase searches on 2026-09-01 found no prior quotient
classification, count of 224 optima, or uniqueness theorem under
$\operatorname{AGL}(3,2)$.  The classification is therefore apparently new to
the searched sources, not a priority claim.
