# Two Tammes-15 contact patterns force the incumbent quintic and coordinates

Authoring agent: **six-tammes-2**, role: **researcher**. Date: 2026-09-29.

This package proves a conditional, global classification of the two known
thirty-contact patterns. Every realization by fifteen **distinct** unit vectors
whose indicated edges have a common inner product in \((1/2,3/5)\) has the
incumbent separation and the indicated incumbent coordinates, up to an
orthogonal transformation. No symmetry, proximity, planarity, or noncontact
inequality is assumed in this necessary-direction theorem. Other contact
patterns remain unclassified, and the global Tammes-15 bounds are unchanged.

The two packings, their quintic, and their exact construction are prior work:
Kottwitz (1991) and Buddenhagen–Kottwitz, Section 4, pp. 7–11. The latter
derives the quintic using a symmetric eighteen-point antecedent and removes
three toggle points. Here the explicit edge equations are treated without
imposing that antecedent or a symmetry ansatz. The contribution is a small
independently checkable classification certificate for arbitrary realizations
of the two patterns. No historical-priority claim is made.

The [13-vertex, 24-contact core theorem](CONTACT_CORE.md) now forces the
incumbent separation and the core Gram matrix using only a subconfiguration.
A strictly better fifteen-point packing cannot contain that contact motif;
the other two points are arbitrary. Its spanning corollary removes both
asymmetric cross edges `(3,7)` and `(3,14)`, giving a 28-edge completion theorem.

The [29-edge completion extension](DELETED_CONTACT.md) deletes the asymmetric
pattern's edge `(3,7)` and proves that every realization in the same interval
automatically restores it. Its separate certificate and checker strengthen
the asymmetric spanning-pattern exclusion without changing the global bounds.

## Statement and precise graph models

Let

\[
 F(t)=13t^5-t^4+6t^3+2t^2-3t-1.
\]

It has exactly one root \(t_0\) in \((1/2,3/5)\), bracketed by

```
0.59260590292507377809642492233275
0.59260590292507377809642492233276
```

Both graphs have vertex set \(\{0,\ldots,14\}\). Begin with complete
triangles on \((0,5,11)\) and \((1,2,4)\). A tuple \((n,i,j,o)\)
below adds the edges \(ni,nj\). The edges \(ij,io,jo\) are already
present; the old point \(o\) specifies the forced reflection. Add the
following six tuples in both graphs:

```
A: (6,0,11,5) (7,0,5,11) (9,5,11,0)
B: (3,1,4,2) (8,2,4,1) (10,1,2,4)
```

Then add the tuples and cross edges in the appropriate row:

| Pattern | Additional tuples | Cross edges |
|---|---|---|
| Asymmetric | A: `(14,0,6,11)`; B: `(12,1,10,2) (13,2,8,4)` | `(7,3) (14,3) (6,8) (7,12) (9,10) (9,13)` |
| Cyclic | A: `(14,0,6,11) (12,5,7,0) (13,11,9,5)` | `(7,3) (14,3) (6,8) (13,8) (9,10) (12,10)` |

These definitions give exactly 30 edges per pattern. The cyclic name describes
the resulting incumbent; it imposes no restriction on an input realization.

**Theorem.** Suppose \(p_0,\ldots,p_{14}\in\mathbb R^3\) are distinct unit
vectors, \(1/2<t<3/5\), and \(p_i\cdot p_j=t\) on every edge of either
specified graph. Then \(t=t_0\). Moreover their entire labeled Gram matrix is
forced: it equals the explicit realization below for the chosen pattern.
Consequently the realization is unique up to an element of \(O(3)\).

**Tammes consequence.** A strictly better fifteen-point packing cannot have
either graph as a spanning subgraph of its contact graph, under any relabeling.
Additional contacts do not evade the exclusion. Indeed the known packing gives
\(\cos d<t_0<3/5\) for a strict improvement, while the disjoint cap-area bound
\(d\le2\arccos(13/15)\) gives \(\cos d\ge113/225>1/2\). The theorem then
forces equality with \(t_0\), a contradiction. This does not enumerate or
exclude all other contact graphs.

## Proof of the reduction

Put \(H=(1-t)I+tJ\). Its eigenvalues are \(1-t,1-t,1+2t\), all positive
on the stated interval. Thus each anchor triangle is a basis of \(\mathbb R^3\).

For an equilateral triangle \((i,j,o)\), the intersection of the unit sphere
with \(x\cdot p_i=x\cdot p_j=t\) consists of exactly two points. One is
\(p_o\). Its orthogonal reflection through \(\operatorname{span}(p_i,p_j)\)
is the other, because its projection on that plane is
\(t(p_i+p_j)/(1+t)\). Distinctness of the fifteen points therefore forces

\[
 p_n=\frac{2t}{1+t}(p_i+p_j)-p_o
\]

at each tuple. This argument covers every geometric branch; no choice of signs
or orientation is suppressed.

Let \(P=(p_0\ p_5\ p_{11})\), \(Q=(p_1\ p_2\ p_4)\), and
\(M=P^TQ\). The two blocks have coefficient vectors \(a_i,b_j\) obtained
from their anchor basis vectors by those reflections. The six cross contacts
are linear equations

\[
 a_i^T M b_j=t.
\]

They solve the first six row-major entries of \(M\) in terms of its bottom
row \((x,y,z)\). The checker proves the chosen six-by-six pivot determinant
does not vanish anywhere on \([1/2,3/5]\), so the solution loses no input.
Write \(\beta=(1,x,y,z)^T\). The certificate's `linear` table gives the
nine entries of \(M\) as \(U(t)\beta/d_M(t)\).

Since \(Q=PH^{-1}M\), the necessary metric compatibility condition is

\[
 M^T H^{-1}M=H.
\]

Write \(H^{-1}=G/h\), where \(h=(1-t)(1+2t)\), and \(G\) has
diagonal \(1+t\) and off-diagonal \(-t\). Substitution and multiplication
by \(h d_M^2\) give six polynomial equations

\[
 C(t)\mu+L(t)\beta=0,\qquad
 \mu=(x^2,xy,xz,y^2,yz,z^2)^T.
\]

The checker computes the determinant of \(C\), proves it nonzero on the
same interval, and verifies the exact identity \(C N+d_Q L=0\) for the
certificate's `quadratic` table. Hence necessarily

\[
 \mu=\mathcal Q(t)\beta,\qquad \mathcal Q=N/d_Q.
\]

## Multiplication obstruction and coordinate uniqueness

Let \(e_x,e_y,e_z\) be the second, third, and fourth standard basis vectors
of \(\mathbb R^4\), and let \(q_1,\ldots,q_6\) be the rows of
\(\mathcal Q\). Form the four-by-four matrices with the specified columns:

\[
 X=[e_x\ q_1^T\ q_2^T\ q_3^T],\quad
 Y=[e_y\ q_2^T\ q_4^T\ q_5^T],\quad
 Z=[e_z\ q_3^T\ q_5^T\ q_6^T].
\]

Any common zero satisfies
\(\beta^T X=x\beta^T\), \(\beta^T Y=y\beta^T\), and
\(\beta^T Z=z\beta^T\). Therefore the nonzero row \(\beta^T\) annihilates
both commutators \([X,Y]\) and \([X,Z]\).

Concatenate these as a four-by-eight matrix \(W\). Its four-by-four minors
using zero-based columns \((1,2,3,5)\) and \((1,2,3,6)\) must both vanish.
The checker constructs these matrices from the verified normal forms, clears
denominators, and computes both determinants exactly. After removing factors
certified nonzero on the interval, the two polynomials have degrees:

| Pattern | First minor | Second minor | Primitive common divisor |
|---|---:|---:|---|
| Asymmetric | 46 | 44 | \(F\) |
| Cyclic | 32 | 28 | \(F\) |

Their primitive polynomial gcd, computed by a rationally sound integer
pseudoremainder algorithm, is exactly \(F\). Thus \(F(t)=0\).
The checker proves \(F'>0\) on \([1/2,3/5]\) by positive Bernstein
coefficients and verifies opposite endpoint signs. This proves \(t=t_0\).

At any root of \(F\), the three-by-three minor of \([X,Y]\) in rows and
columns \((1,2,3)\) is nonzero: its numerator has gcd one with \(F\).
Exact polynomial identities modulo \(F\) show that

\[
 (1,b,c,a)[X,Y]=(1,b,c,a)[X,Z]=0,
\]

where

\[
\begin{aligned}
 a&=(117t^4-48t^3+70t^2-6t-27)/2,\\
 b&=(195t^4-106t^3+136t^2-38t-31)/4,\\
 c&=(-429t^4+202t^3-276t^2+42t+81)/4.
\end{aligned}
\]

The rank is therefore exactly three, and the left kernel has a unique vector
whose first entry is one. Hence \((x,y,z)=(b,c,a)\). Substitution in the
verified linear table forces, in both patterns,

\[
 M=\begin{pmatrix}a&b&c\\c&a&b\\b&c&a\end{pmatrix}.
\]

Together with the forced reflections and the common anchor Gram matrix \(H\),
this fixes every inner product. Equal full Gram matrices with spanning anchor
bases give an orthogonal transformation taking one realization to the other.

For existence, choose any real basis \(P\) with \(P^TP=H(t_0)\), set
\(Q=PH^{-1}M\), and carry out the chosen reflection list. The checker
verifies \(M^TH^{-1}M=H\) modulo \(F\), all fifteen unit norms, all thirty
contact equalities, and every noncontact inner product strictly below \(17/40\)
by exact rational intervals at the bracketed root. Since \(17/40<t_0<1\),
the points are distinct and the contacts are exactly the declared edges.
These are the known asymmetric and cyclic incumbent packings, not new codes.

## Divisors, certificate, and trust boundary

Every denominator and each of the two pivot determinants is checked to be a
nonzero rational constant times a product of members of this list:

```
t; t-1; t+1; 2t+1; 3t+1; 3t-1; 5t^2-1;
9t^2-2t-3; 9t^3-t^2-t+1; 8t^4-3t^3-t^2+3t+1;
t^2-2t-1; 13t^3-7t-2; 11t^3-5t^2-11t-3.
```

Every member has Bernstein coefficients of a single strict sign on
\([1/2,3/5]\); the checker computes and checks these coefficients using
`Fraction`. Polynomial identities, Bareiss determinants, divisibility, and
gcds use only integer arithmetic. The certificate contains two sets of affine
linear and quadratic-normal-form tables, in ascending coefficient order, with
a common integer polynomial denominator per table. It contains no search log,
floating-point witness, or large external certificate.

The independently executable checker does not call SymPy or a solver and does
not trust generator output without checking the defining identities. The
reduction from geometry to the equations and the multiplication argument above
are a hand proof, not a proof-assistant formalization. Arithmetic checks cannot
replace that reduction. Independent review is pending.

## Reproduction

Python **3.11 or newer**, standard library only:

```sh
python3 -B tammes15_contact_pattern_obstruction/verify.py
python3 -B tammes15_contact_pattern_obstruction/verify.py --selftest
python3 -B -O tammes15_contact_pattern_obstruction/verify.py
```

Expected: `VERIFIED`, both patterns have 15 points and 30 edges, common
obstruction `[-1,-3,2,6,-1,13]`, unique cross Gram at the root, all divisors
nonzero, and noncontacts below `17/40`. Controls reject separately corrupted
linear and quadratic tables and distinguish a genuine gcd obstruction from an
extra common factor. A run on CPython 3.11.2 used under one second and under
20 MiB RSS. No costly enumeration or numeric solver is involved.

Full table regeneration requires **SymPy 1.14.0** and one CPU thread:

```sh
python3 tammes15_contact_pattern_obstruction/generate_certificate.py
python3 -B tammes15_contact_pattern_obstruction/verify.py --selftest
sha256sum tammes15_contact_pattern_obstruction/certificate.json
```

The fully regenerated certificate has SHA-256
`825cd708d864ffdf73922395081d6201a2e54a920324bf47d60309e934402b35`.
The source commit is recorded in the graph contribution and durable campaign
checkpoint after remote verification.

## Literature and complementary work

- D. A. Kottwitz, *The densest packing of equal circles on a sphere*,
  Acta Cryst. A **47** (1991), 158–165,
  [DOI](https://doi.org/10.1107/S0108767390011370).
- J. Buddenhagen and D. A. Kottwitz, *Multiplicity and Symmetry Breaking in
  (Conjectured) Densest Packings of Congruent Circles on a Sphere*, Section 4,
  pp. 7–11. [Archived author PDF](https://web.archive.org/web/20210507001707/http://www.buddenbooks.com/jb/pack/sphere/toggles7.pdf).
  Wang's bibliography dates the preprint to 1994; the PDF inspected has no
  explicit date on its title page. Its exact constructions and quintic are
  acknowledged as prior work.
- J. Wang, *Finding and investigating exact spherical codes*,
  [arXiv:0805.0776](https://arxiv.org/abs/0805.0776), Introduction and Section 4.
  It explicitly credits those prior exact fifteen-point descriptions.
- [Current Cohn table](https://cohn.mit.edu/spherical-codes/),
  [coordinate data](https://spherical-codes.org/data/3/15), and
  [archived data](https://hdl.handle.net/1721.1/153543).
- Musin–Tarasov, [arXiv:1410.2536](https://arxiv.org/abs/1410.2536), solves
  the fourteen-point problem; it does not prove fifteen-point optimality.
- six-tammes-2's [exact incumbent and local stress certificate](https://github.com/helgithorskarp/math_results/tree/main/tammes15_exact_local_certificate)
  verifies the asymmetric packing and a quantified neighborhood exclusion.
  The present proof covers arbitrary realizations of both specified graphs.
- six-tammes-1's [triangle–quadrilateral exclusion](https://github.com/helgithorskarp/math_results/blob/main/tammes_15_triangle_quad_exclusion/PROOF.md)
  closes a complementary face branch. It is cited for coordination and is not
  a premise of the present classification.
