# Lonely directions on rational central ellipses

## 1. The result and its scope

Let `P={p_1,...,p_n}` consist of rational vectors in the plane, with `n>=2`,
no zero vector, and no two vectors equal or opposite. Form the **labelled
multiset**

\[
 S_P=\{p_i:1\le i\le n\}\;\sqcup\;
 \{p_i+p_j,p_i-p_j:1\le i<j\le n\}.
\]

It has `n^2` entries. Different labelled entries are retained even when they
happen to be the same vector. An entry is **lonely** if no other entry is
parallel to it. Parallelism here allows negative as well as positive multiples.
This is the Lonely Vector Property (LVP) of Malikiosis–Santos–Schymura.

**Theorem A.** If all the points of `P` lie on a common ellipse centered at the
origin, then `S_P` has at least two lonely entries. There is no bound on `n`.
The ellipse need not initially be given by rational coefficients.

For the sharper conclusion, write a rational equation of the ellipse as

\[
 Q(x,y)=Ax^2+2Bxy+Cy^2=1,\qquad A>0,\quad
 \Delta=AC-B^2>0.
\]

**Theorem B.** If `Delta` is not three times a nonzero rational square, at least
two of the **original vectors** `p_i` are lonely. If `Delta` is three times a
rational square, Theorem A still holds, but even the existence of a lonely
original vector can fail for arbitrarily large configurations.

The discriminant condition is invariant under rational invertible linear
changes of coordinates and scaling the equation: these multiply `Delta` by a
rational square. Rational points on an origin-centered circle, for example,
fall under Theorem B, not its exceptional case.

**Corollary C (Gale reduction).** Let `U` be a rational rank-`d` matrix with
`n=d+2` columns, where `d>=1`. Let the columns of an `n`-by-`2` matrix `P` be a
basis of `ker U`, and suppose its rows satisfy the ellipse hypotheses above.
Then one can either delete a column of `U` or replace two columns `u_i,u_j` by
`u_i+u_j` or `u_i-u_j`, leaving a rank-`d` configuration with `d+1` generators
whose unique dependence has nonzero coefficients of pairwise distinct absolute
values. Thus the resulting configuration is cosimple and is a strong Lonely
Runner configuration. For integral `U` the result is an integral zonotope of
the same dimension contained, after translation, in the original zonotope.
For `d>=2` this containment is proper. Outside the exceptional discriminant
class, at least two different column deletions work.

There is an explicit family, with `n=3m` and `d=3m-2` for every `m>=1`, in which
**no deletion is cosimple**, but a diagonal reduction is. It lies in the
exceptional class and shows why diagonals cannot be omitted from Corollary C.

The general rational LVP is already false, as shown by Blanco–Criado–Santos in
2026. The shifted Lonely Runner Conjecture is also false. We prove a positive
structural subclass and a corresponding zonotope reduction, not either of those
false universal statements or the original unshifted Lonely Runner Conjecture.

## 2. Rationalizing the ellipse

On a fixed ellipse centered at zero, two parallel points are equal or opposite:
if `q=lambda p` and `Q(p)=Q(q)=1`, then `lambda^2=1`. Thus the points of `P` have
distinct projective directions.

If `n=2`, the four vectors `p_1,p_2,p_1+p_2,p_1-p_2` have pairwise different
directions, since `p_1,p_2` are independent. Both theorems follow immediately.
For `n>=3`, select any three points. The three rows

\[
 (x_i^2,2x_i y_i,y_i^2)
\]

are independent: a nonzero homogeneous binary quadratic vanishes on at most two
real projective directions. Solving `Q(p_i)=1` therefore gives unique rational
coefficients `A,B,C`. They agree with the normalized equation of the supplied
ellipse, hence are positive definite and apply to every point of `P`.

## 3. Directions become products in a norm-one group

Let `K=Q(sqrt(-Delta))`, an imaginary quadratic field, with complex conjugation
written as a bar. Map the rational plane into `K` by the invertible real linear map

\[
 (x,y)\longmapsto z=Ax+By+y\sqrt{-\Delta}.
\]

Its norm is

\[
 z\bar z=(Ax+By)^2+\Delta y^2=AQ(x,y).
\]

Consequently all the images `z_i` have norm `A`. Fix one of them, `z_0`, and put
`u_i=z_i/z_0`. The `u_i` are norm-one elements of `K`, distinct modulo sign.
Multiplication by a fixed nonzero complex number preserves parallelism.

For a nonzero complex number `w`, its unoriented direction is represented
injectively by

\[
 D(w)=w/\bar w.
\]

Indeed `D(w)=D(v)` precisely when `w/v` is nonzero real. Since `bar u_i=u_i^{-1}`,

\[
 D(u_i)=u_i^2,\qquad
 D(u_i+u_j)=u_i u_j,\qquad
 D(u_i-u_j)=-u_i u_j. \tag{1}
\]

None of these sums or differences is zero. The actual directions of the
original `z_i` and their sums/differences have one common additional factor
`D(z_0)`, which cancels in every comparison. Thus LVP is exactly the existence
of a singly represented element in the **labelled** multiset

\[
 \{u_i^2\}_i\ \sqcup\ \{u_i u_j,-u_i u_j\}_{i<j}. \tag{2}
\]

It is important not to discard the sign in (2), or to replace the multiset by
a set. We only quotient by torsion as an intermediate step for isolating a
small fiber; final multiplicities are checked before this quotient.

## 4. Exposing a fiber of roots of unity

Let `mu(K)` be the roots of unity in `K`. This cyclic group has order

\[
 w=\begin{cases}
 4,&K=\mathbb Q(i),\\
 6,&K=\mathbb Q(\sqrt{-3}),\\
 2,&\text{otherwise}.
 \end{cases} \tag{3}
\]

For completeness, a root of unity `eta` in an imaginary quadratic field has
rational algebraic-integer trace `eta+bar eta`, hence integer trace in
`{-2,-1,0,1,2}`. The five possibilities give only orders `1,2,3,4,6`.
The nonreal cases determine the indicated fields; they cannot occur together
in a quadratic field.

Let `Gamma` be the multiplicative group generated by the finitely many `u_i`
and by `mu(K)`. Its torsion subgroup is precisely `mu(K)`. The finitely generated
abelian group

\[
 \Gamma/\mu(K)
\]

is therefore free abelian. Choose an additive real-valued homomorphism on this
quotient which takes distinct values on the finitely many different classes of
the `u_i`. Such a homomorphism exists: identify the quotient with `Z^r` and
choose a vector outside the finitely many hyperplanes defined by differences
of the occurring classes. Rank zero causes no problem: then only one class
occurs and use the zero homomorphism.

Let `a` be the largest value, and let `I` be the indices attaining it. For any
entry of (2) supported entirely on `I`, the homomorphism takes the value `2a`.
If another entry has the same direction, (1) shows that its value is also `2a`.
An original entry has value `2 chi(u_k)` and a pair entry has value
`chi(u_k)+chi(u_l)`. Since each individual value is at most `a`, every index in
this colliding entry must also belong to `I`.

**Isolation lemma.** A lonely entry of the subsystem indexed by `I` remains
lonely in the full system. The same holds for the fiber of the smallest value.

All `u_i` in one fiber differ by roots of unity. Since equal and opposite points
are excluded, a fiber has at most `w/2<=3` elements. After multiplying the fiber
by a common unit, independently changing signs, and reordering, it is a subset
of representatives of `mu(K)/{+1,-1}`. These operations preserve all direction
multiplicities: changing one sign only interchanges the corresponding sum and
difference entries, up to sign.

If a fiber has one element, its original vector is lonely within the fiber.
If it has two, all four entries are lonely, as in Section 2. The only remaining
case is `K=Q(sqrt(-3))` and a full three-element fiber. Put

\[
 \zeta=(1+\sqrt{-3})/2,
\]

and normalize the fiber to `{1,zeta,zeta^2}`. Under (1), the original directions
have exponents `0,2,4` modulo six. The six pair directions have exponents

\[
 (1,4),\quad(2,5),\quad(3,0).
\]

Thus the even exponents have multiplicity two and the odd exponents have
multiplicity one. Exactly three pair entries are lonely and no original is.
This completes the finite torsion analysis without an enumeration assumption.

Apply the isolation lemma to the largest and smallest occurring quotient
classes. If they differ, the two resulting lonely directions have different
homomorphism values and are distinct. If only one class occurs, the entire
configuration has two or three elements and the preceding analysis gives at
least three lonely entries. This proves Theorem A. Outside `Q(sqrt(-3))`,
every fiber has at most two elements, so the two witnesses can be original
vectors; this proves Theorem B. Finally
`Q(sqrt(-Delta))=Q(sqrt(-3))` exactly when `Delta=3s^2` for a nonzero rational `s`.

No unique factorization of elements or ideals is assumed. The argument needs
only the structure theorem for finitely generated abelian groups and the
explicit quadratic-field torsion calculation.

## 5. The deletion/diagonal consequence, with its rank checks

A rank-`d` column configuration `U` is cosimple if its kernel contains a vector
with no zero coordinate and no equal absolute values among coordinates.
Writing its kernel vectors as

\[
 \lambda_i=p_i\mathbin\cdot t,\qquad t\in\mathbb R^2,
\]

shows that it is cosimple whenever all the `p_i` are nonzero and no two are equal
or opposite: a generic `t` avoids the finitely many lines on which one of these
requirements fails. This is also the standard Gale characterization.

Suppose first that `p_i` is lonely. To delete `u_i`, restrict the dependence to
`p_i dot t=0`. This is a one-dimensional subspace. For any nonzero `t` in it,
the remaining coefficients are nonzero because no `p_j` is parallel to `p_i`.
Their absolute values differ because no `p_j+p_k` or `p_j-p_k` is parallel to
`p_i`. The new matrix has `d+1` columns and a one-dimensional kernel, so its
rank is still `d`.

If instead `w=p_i+epsilon p_j` is lonely, for `epsilon` equal to `+1` or `-1`,
restrict to `w dot t=0`. Then `lambda_j=-epsilon lambda_i`. Replace `u_i,u_j`
by `u_i-epsilon u_j`, with coefficient `lambda_i`. Every resulting coefficient
is nonzero and their absolute values differ: any failure would make `w`
parallel to a different original or pair entry of `S_P`. The only intentionally
vanishing comparison is the one between the two merged coordinates, which is
no longer a comparison in the reduced system. The same kernel-dimension argument
proves rank `d`.

The sign reversal in this rule is material: a lonely **sum** of Gale vectors
selects a **difference** of generator columns, and conversely. This is the
specialized form of the deletion/diagonal correspondence in the cited literature,
with a direct proof here to expose the rank and sign requirements.

For centered zonotopes, deleting a segment gives containment, and

\[
 [-\tfrac12(u_i\pm u_j),\tfrac12(u_i\pm u_j)]
 \subseteq [-u_i/2,u_i/2]+[-u_j/2,u_j/2].
\]

For `d>=2` these containments are proper. Indeed any two rows of `P` are
independent, so every set of `d` columns of `U` is independent by complementary
minors (equivalently, a dependence supported there would have two zero Gale
coordinates). In particular all columns are nonzero and any pair is independent.
A deletion removes a nonzero segment; a diagonal replaces a two-dimensional
parallelogram by a segment. A strict inequality of support functions persists
under adding the remaining segments. For `d=1` containment may be equality;
no proper-containment claim is made in that case.

In the uncentered convention `Z(U)=sum [0,u_i]`, deletion and the sum
diagonal require no translation; translate a difference diagonal by `u_j`.
For integral generators these choices preserve integrality of the contained
zonotope. The absolute maximal minors of a rank-`d` matrix with `d+1`
columns are proportional to the absolute coefficients of its unique dependence,
which verifies the strong Lonely Runner terminology.

This proves Corollary C. It excludes this entire class of corank-two elliptic
Gale configurations from non-sLR minimal cosimple zonotopes, with proper
containment in dimensions at least two.

## 6. An arbitrary-size family needing a diagonal

Work in `K=Q(sqrt(-3))` and put

\[
 u=\frac{23+7\sqrt{-3}}{26},\qquad
 \zeta=\frac{1+\sqrt{-3}}2.
\]

Both have norm one. The element `u` is not torsion: its trace `23/13` is not
an integer, whereas the trace of a root of unity is an integer. For any `m>=1`,
take the rational coordinate vectors of

\[
 P_m=\{u^k\zeta^j:0\le k<m,\ 0\le j<3\}. \tag{4}
\]

There are `3m` distinct vectors modulo sign. An equality up to sign between two
different powers would make a nonzero power of `u` a root of unity, impossible.
Every point lies on `x^2+3y^2=1`. Inside each three-element fiber,

\[
 1=\zeta-\zeta^2,\quad
 \zeta=1+\zeta^2,\quad
 \zeta^2=\zeta-1.
\]

Consequently every original vector in (4) is parallel to another labelled
entry, so none is lonely. Theorem A nevertheless provides a lonely pair entry.

Take any rational basis of the kernel of the two-by-`3m` matrix with columns
`P_m`, as the rows of a `(3m-2)`-by-`3m` matrix `U_m`. Clearing denominators makes
`U_m` integral without changing its Gale data. The generic-kernel argument
above proves it cosimple. Every column deletion imposes equality up to sign on
the two other coefficients in that fiber, hence cannot be cosimple. A diagonal
selected by a lonely pair does give a cosimple configuration of the same rank.
The smallest example has `U_1=(1,-1,1)` up to row scaling; its centered segment
can be represented by the two unequal lengths `2,1` after a diagonal, whereas
any deletion leaves two equal lengths. For `m>=2` the successful contained
zonotope is proper by Section 5.

This is an infinite obstruction to a deletion-only reduction, not an obstruction
to the stated deletion-or-diagonal reduction.

## 7. Verification, prior work, and limitations

The standard-library checker uses exact `Fraction` arithmetic. It retains labels
and multiplicities. Projective normalization is compared with all-pairs determinant
counts on small cases; every reported lonely witness is separately checked by
determinants against all other entries. It checks every nonempty antipodal-free
subset of the torsion groups of orders two, four, and six (36 signed cases),
rational elliptic families and rational coordinate changes, the complete
exceptional fibers, and the Gale rank and unique-relation conditions.

Two negative controls are included. The 38-vector rectangular example from
Blanco–Criado–Santos has no lonely entry and fails the ellipse hypothesis. Half
of a regular octagon lies on a circle but has no lonely entry; its coordinates
and determinants are evaluated exactly in `Q(sqrt(2))`. This is the known real,
nonrational obstruction, and shows why rationality matters. Neither negative
control is claimed as a new counterexample.

Primary references:

- R. D. Malikiosis, F. Santos, M. Schymura, *Linearly-exponential checking is enough
  for the Lonely Runner Conjecture and some of its variants*, Forum of Mathematics,
  Sigma 13 (2025), e164; [arXiv:2411.06903](https://arxiv.org/abs/2411.06903).
  Definition 1.2 defines LVP; Section 4 discusses its role and proves the rational
  cases through four vectors.
- M. Blanco, F. Criado, F. Santos, *Coloopless and cosimple zonotopes, and the Lonely
  Runner Conjectures*, [arXiv:2603.24784v1](https://arxiv.org/abs/2603.24784).
  Theorem 4.6 gives the Gale reduction correspondence; Section 4.2 disproves
  general rational LVP; Section 5 gives shifted-runner counterexamples.

The contribution here is the all-cardinality ellipse theorem, its stronger
nonexceptional deletion conclusion, and the explicit arbitrary-size exceptional
family. The preceding definitions, general Gale correspondence, small LVP cases,
and universal counterexamples are prior work. Targeted live searches and bounded
graph queries on 2026-09-20 found no matching ellipse theorem; this supports only
search-relative novelty. We do not claim a classification of all configurations
with LVP, all minimal cosimple zonotopes, or any new universal covering-radius bound.

The proof uses elementary algebra and is unformalized. Finite exact verification
corroborates the theorem and the linear-algebra translation; it is not a proof of
the unbounded theorem or an independent peer review.
