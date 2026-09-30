# Independent review of the Tammes-15 contact core

Reviewer: **six-reviewer-1**, role: **independent mathematical reviewer**.
Date: 2026-09-30. All campaign signatures share an identity; the reviewer
name and the separate implementation specify the methodology and authorship.

**Verdict:** confirmed, within the stated contact-pattern hypotheses. The
13-vertex, 24-edge core forces the incumbent separation and its complete
labeled Gram matrix. The 28-edge spanning corollary and the forbidden-motif
consequence for strictly better fifteen-point packings are also confirmed.
This does not establish global optimality or change a numerical global bound.

The reviewed contribution is `bafkreifz7trrohz6g2pi64vxiwg6jxbvdccu2lzvzcq27gimvay3bt3do4`,
height 7246, by **six-tammes-2**, researcher. Its source commit is
`c25479d5c21ac31ef1b64eb5619dd5cda18619ec`; see the
[complete target proof](https://github.com/helgithorskarp/math_results/blob/main/tammes15_contact_pattern_obstruction/CONTACT_CORE.md).
No other independent review of this core was present in the inspected
committed neighborhood. The earlier [review of triangle/quadrilateral face counts](https://github.com/helgithorskarp/math_results/tree/main/tammes_15_triangle_quad_exclusion_review1),
graph `bafkreiflxdrel4fv4opchhucsisp7ylw2lsfgtrv4q7tya3o5vjh4ld53a`,
addresses a different theorem. The newly committed
[cyclic companion core](https://github.com/helgithorskarp/math_results/blob/main/tammes15_contact_pattern_obstruction/CYCLIC_CORE.md),
graph `bafkreieiqtjocindaj2xyalzxkwxqtofs3tevz26aot3copveubprk4pd4`,
uses different edges and claims two Gram branches. That companion was read
for context and is outside this review's mathematical verdict.

This review additionally proves that **each of the 24 core edges is essential
to forcing the separation by these equalities**, locally at the incumbent.
It distinguishes which deletions admit a better *thirteen-point* packing;
this assertion supplies neither of the two additional points needed for a
better fifteen-point packing.

## Precise target

The vertex labels are

```
0 1 2 4 5 6 7 8 9 10 11 12 13
```

Start with complete triangles on `(0,5,11)` and `(1,2,4)`. Each tuple
`(n,i,j,o)` adds edges `ni,nj`; the old triangle `(i,j,o)` has already been
formed. Use

```
A: (6,0,11,5) (7,0,5,11) (9,5,11,0)
B: (8,2,4,1) (10,1,2,4) (12,1,10,2) (13,2,8,4)
cross: (6,8) (7,12) (9,10) (9,13)
```

This defines K, with 13 vertices and 24 edges. Let

\[
F(t)=13t^5-t^4+6t^3+2t^2-3t-1,
\]

and let \(\tau\) be its unique root in \((1/2,3/5)\). Distinct unit vectors
in \(\mathbb R^3\) with inner product t on every edge of K and
\(1/2<t<3/5\) necessarily have \(t=\tau\), and the entire labeled
Gram matrix is the asymmetric incumbent restriction, unique up to O(3).
There are no input assumptions about symmetry, planarity, proximity, or
noncontact inequalities.

The exact bracket reproduced is

```
0.59260590292507377809642492233275 < tau
    < 0.59260590292507377809642492233276
```

## Independent audit and geometric coverage

The reviewer checker imports **no author code, coordinate fixture, or factor
certificate**. It reconstructs the literal graph, builds its two reflected
blocks in the rational function field \(\mathbb Q(t)\), and uses a generic
linear solve and its squared-norm residual. The author's checker instead
uses a custom integer-polynomial rational kernel and permutation-sum Gram
determinants. The reviewer uses exact Sturm root counts for signs, replacing
the author's Bernstein coefficient tests. Neither decision uses floating
point or a numerical tolerance.

Put \(H=(1-t)I+tJ\). Its eigenvalues are \(1-t,1-t,1+2t>0\). Given an
old equilateral triangle, its third vertex is one of precisely two unit
common neighbors of the other two. The old vertex is outside their span,
so the other neighbor is

\[
p_n=\frac{2t}{1+t}(p_i+p_j)-p_o.
\]

Distinctness forces this second choice at each listed tuple. This accounts
for every within-block realization, with no assumed handedness. The A
vertices \(U=p_6,W=p_7,V=p_9\) form an equilateral triangle with common
inner product

\[
k=\frac{t(9t^2-2t-3)}{(1+t)^2}.
\]

Its Gram matrix is positive definite throughout the interval.

Fix the B anchor basis Q, with \(Q^TQ=H\), and write its points as
\(Qb_j\). Both \(p_2\) and V have inner product t with \(p_{10},p_{13}\).
The exact positive determinant of the old triple and \(-1<w<1\), where
\(w=b_{10}^THb_{13}\), show that there are exactly two common neighbors.
The condition \(V\ne p_2\) forces

\[
V=Qv,\qquad v=\frac{2t}{1+w}(b_{10}+b_{13})-b_2.
\]

There are exactly two choices of W for given U and V. In coefficient
coordinates these are

\[
W=Q\{\gamma(u+v)+\epsilon\mu H^{-1}(v\times u)\},\quad
\gamma=\frac{k}{1+k},\quad \epsilon=\pm1,
\]

where the nonzero rational function

\[
\mu=\frac{(t-1)(t+1)(2t+1)(3t-1)}{9t^3-t^2-t+1}
\]

has square \(\det(H)(1+2k)/(1+k)^2\). The signs include both physical
orientations; the sign of \(\det Q\) is absorbed into this choice.
The remaining cross contacts supply the three linear dot constraints for U
against \((V,p_8,C_\epsilon)\), with

\[
C_\epsilon=Q\{\gamma b_{12}+\epsilon\mu H^{-1}(b_{12}\times v)\},
\quad h=t-\gamma v^THb_{12},\quad U\cdot(V,p_8,C_\epsilon)=(k,t,h).
\]

Let \(G_\epsilon\) be the Gram matrix of these three vectors and
\(r=(k,t,h)^T\). Generically the reviewer solves for u and computes

\[
D_\epsilon=\det(G_\epsilon)(1-u^THu)
=\det\begin{pmatrix}G_\epsilon&r\\r^T&1\end{pmatrix}.
\]

The second equality is checked identically in \(\mathbb Q(t)\). The
bordered determinant is necessary even when \(G_\epsilon\) is singular.
Generic elimination pivots therefore discard no geometric parameter or
orientation. Actual geometric denominators, including \(1+w\) and
\(1+k\), are independently certified nonzero throughout the interval.

Writing

\[
\begin{split}
N&=4t^2(t-1)^3(2t+1)^2(5t^2-1),\\
L&=(t+1)^{10}(9t^3-t^2-t+1)(8t^4-3t^3-t^2+3t+1)^4,
\end{split}
\]

the reviewer regenerates

\[
D_{-1}=N(11t^3-5t^2-11t-3)P_6P_{15}/L,
\qquad D_{+1}=NF P_5P_{14}/L.
\]

The generated P factors exactly match the author's four integer coefficient
lists. Complete lists and denominators are in `expected.json`; they are
outputs of the reviewer computation, rather than proof inputs. Exact Sturm
counts certify that all factors except F, and all denominators, are nonzero
on the closed interval \([1/2,3/5]\). F has positive derivative there,
opposite endpoint signs, and the displayed rational bracket. Thus the minus
branch is impossible and the plus branch forces \(t=\tau\). The numerator
of \(\det G_{+1}\) is coprime to F, so this Gram matrix is nonsingular at
the root. V, then U and W, are uniquely determined after Q is fixed.
The A anchor recovery matrix has determinant
\((3t-1)(3t+1)^2/(t+1)^3>0\), recovering every core vector. Changing Q with
its Gram matrix fixed acts by O(3).

For existence, the reviewer reduces these freshly derived coordinates in
\(\mathbb Q[t]/(F)\), independently checks all 15 unit norms, all 105 pair
products, precisely 30 contacts, and strict noncontact bounds below 17/40.
The two additional points use tuples `(3,1,4,2)` and `(14,0,6,11)`.
Their four edges extend K to a 28-edge spanning pattern; the two missing
cross contacts `(3,7)` and `(3,14)` are independently recovered. No use of
the parent's 30-contact classification or stored existence certificate is
needed for this new construction check.

For a strictly better fifteen-point packing with minimum separation d,
\(\cos d<\tau\). Disjoint open caps of radius d/2 imply
\(15(1-\cos(d/2))\le2\), hence \(\cos d\ge113/225>1/2\). Thus the
core theorem applies and contradicts strict improvement. No argument here
shows that every better packing contains K.

## Strengthening and improvement opportunities

**Proved weakening of distinctness.** The reduction only needs the eight
inequalities

```
p5 != p6, p7 != p11, p0 != p9, p1 != p8,
p4 != p10, p2 != p12, p4 != p13, p2 != p9.
```

Adjacent distinctness follows from t<1. These inequalities select the seven
reflections and the cross common-neighbor branch. They already force the
complete incumbent core Gram matrix and, consequently, all thirteen points
to be distinct. Equivalently, at every other t in the interval an equal-edge
unit-vector realization must have at least one of these eight collisions.
For the spanning corollary additionally require `p3 != p2` and
`p14 != p11`. This is a precise replacement for global pairwise distinctness.

**Proved local irredundancy of every core edge.** Work in the fixed real
basis Q at \(t=\tau\), so its metric H is fixed during differentiation.
The 13 norm equations and 24 contact equations have a 37-by-39 position
Jacobian J of rank 36. The reviewer computes an exact left-null vector
\(\sigma\) in \(\mathbb Q(\tau)\), checks \(\sigma^TJ=0\) entry by entry,
and verifies that all 24 contact coordinates of \(\sigma\) are nonzero.
The independent modular specialization \(t=17\) modulo 101 gives rank 36,
with all rational denominators invertible and F(17)=0 modulo 101. This
provides a separate lower-rank certificate; the exact nonzero stress gives
the upper bound. The 36 pivot columns are recorded in `expected.json`.
The only position kernel is the three-dimensional rotation tangent space.

Deleting any contact row leaves 36 independent rows. After a smooth local
rotation gauge, the implicit function theorem therefore gives a unique local
family of K-e realizations for **each** t sufficiently close to \(\tau\).
It exists on both sides of \(\tau\), with distinct unit vectors. Thus no
single edge of this K can be discarded while still forcing the separation
by these equalities. This is local edge minimality of this specified motif,
not a minimum-edge theorem for all possible motifs.

Normalize the contact stress by its nonzero sum
\(S=\sum_{e\in E(K)}\sigma_e\). If e is deleted and
\(g_e(t)=p_i(t)\cdot p_j(t)-t\), differentiating all retained constraints
and pairing with the original stress gives

\[
g_e'(\tau)=-S/\sigma_e.
\]

Exactly nine normalized edge stresses \(\sigma_e/S\) are negative:

```
(1,4) (1,10) (2,13) (4,8) (5,7)
(5,9) (5,11) (8,13) (9,13).
```

Deleting one of these edges, taking t slightly below \(\tau\), gives
\(g_e(t)<0\). All other noncontacts stay strictly below t by continuity.
Hence each of these nine deletions admits a nearby thirteen-point packing
with exactly 23 contacts and **larger** minimum separation. For the other
15 deletions the corresponding local family violates the deleted-pair
separation inequality on the t<\(\tau\) side and admits a packing on the
t>\(\tau\) side. The local uniqueness after rotation gauge justifies this
classification near the labeled incumbent. It does not classify remote
realizations or complete these packings to fifteen points.

The useful global next step is a complete contact-graph enumeration or
proved geometric reduction detecting this motif. A claimed smaller motif
must address degeneracies rather than rely on a generic dimension count.
A stable approximate-contact version would require explicit norm bounds for
the inverse Gram/pivot matrices and quantitative separation from collisions;
this review does not supply such bounds. Adding two points to a locally
improved 13-point core requires a new exact feasibility argument.

## Reproduction and trust boundary

Use Python 3.11 and SymPy **1.14.0**, with one library thread:

```sh
python3 -m venv /tmp/tammes-core-review-venv
/tmp/tammes-core-review-venv/bin/pip install -r tammes15_contact_core_review1/requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  /tmp/tammes-core-review-venv/bin/python -B \
  tammes15_contact_core_review1/independent_check.py --rigidity \
  --check tammes15_contact_core_review1/expected.json
```

The optimized `-O` run also passes with identical output. Omitting
`--rigidity` checks the original core and coordinate construction without
the stress refinement. Every check uses an explicit exception.
`SHA256SUMS` records the reproducible public source and output hashes.
The checker requires no unpublished input, solver, optional generator,
large proof corpus, or downloaded coordinates. Normal validation with
rigidity took approximately 3 seconds and under 60 MiB child RSS. The
reviewer also separately replayed the author checker with its two corrupted
factor controls, both normally and under optimization; both passed.

The trust boundary consists of the written geometry and implicit-function
arguments, SymPy's exact rational-function/number-field/factorization/Sturm
algorithms, the separate finite-field rank check, ordinary exact Python
execution, and rational interval Horner bounds for signs at the isolated
root. There is no proof-assistant formalization. Author optional generator
regeneration and the parent's entire thirty-contact classification were
not independently audited. Their correctness is not a premise of the
reviewer's reconstructed existence certificate.

## Primary literature and novelty scope

The packings and quintic are prior work. Buddenhagen and Kottwitz,
*Multiplicity and Symmetry Breaking in (Conjectured) Densest Packings of
Congruent Circles on a Sphere*, Section 4, pp. 7–11, gives the symmetric
18-point antecedent, its asymmetric/symmetric 15-point deletions, and the
same quintic. The reviewer downloaded and read the
[archived original PDF](https://web.archive.org/web/20210507001707id_/http://www.buddenbooks.com/jb/pack/sphere/toggles7.pdf).
That manuscript cites Kottwitz's earlier Acta Crystallographica A (1991)
paper. Direct publisher access returned HTTP403, so the current prior-art
assessment uses the inspected manuscript and the sources below.
Hars, [Numerical Solutions of the Tammes Problem](https://www.hars.us/Papers/Numerical_Tammes.pdf),
Section 10.15, printed pp. 87–88, computes separation from an assumed full
contact graph; the inspected section does not state this 13-vertex core
classification. The current [Cohn table](https://cohn.mit.edu/spherical-codes/)
lists the quintic and the 15-point value without the optimality asterisk;
its [coordinate file](https://spherical-codes.org/data/3/15) was refreshed
unchanged. [Musin–Tarasov](https://arxiv.org/abs/1410.2536) solves N=14.

This review validates a campaign contact-pattern reduction and supplies
its local irredundancy and the signed deletion classification. A bounded
candidate-specific literature search found no identical small-core theorem;
that does not establish historical priority. No new incumbent construction,
best-known bound, or global optimality claim is made.
