# One missing contact is forced in the asymmetric Tammes-15 pattern

Authoring agent: **six-tammes-2**, role: **researcher**. Date: 2026-09-29.

Delete edge `(3,7)` from the asymmetric 30-edge graph in
[README.md](README.md), giving a labeled graph \(G_{29}\). Every realization
of \(G_{29}\) by fifteen distinct unit vectors, with a common edge inner
product in \((1/2,3/5)\), automatically restores that missing edge. The
existing 30-edge classification then identifies the full Gram matrix.

The packing and its quintic are prior work, as documented in README.md.
This is a smaller independently checkable contact-pattern reduction. It does
not improve the global numerical bounds or prove Tammes-15 optimality.
No symmetry, proximity, planarity, or noncontact inequalities are assumed.
Independent review is pending; no historical-priority claim is made.

The primary literature comparison also includes L. Hars,
[*Numerical Solutions of the Tammes Problem*, Section 10.15, p. 87](https://www.hars.us/Papers/Numerical_Tammes.pdf).
That section computes the incumbent distance assuming its displayed contact
graph, using a bisection equation. It does not establish the 29-edge completion
proved here. The exact construction and quintic references remain those in
README.md, including Kottwitz and Buddenhagen–Kottwitz.

Complementary work by **six-tammes-1, researcher**, gives a
[31-edge bound in the triangle/quadrilateral branch](https://github.com/helgithorskarp/math_results/blob/main/tammes15_seven_rhombus_exclusion/PROOF.md).
It assumes a complete, connected, strictly convex cellular contact graph
with degrees 3 through 5 and only those two face types. It is relevant
context rather than a logical premise of this prescribed-edge theorem.

## Statement and graph

The graph has vertex set \(\{0,\ldots,14\}\). Its anchor triangles are
`(0,5,11)` and `(1,2,4)`. Each reflection tuple `(n,i,j,o)` adds edges
`ni,nj`, with old equilateral triangle `(i,j,o)` already present:

```
A: (6,0,11,5) (7,0,5,11) (9,5,11,0) (14,0,6,11)
B: (3,1,4,2) (8,2,4,1) (10,1,2,4) (12,1,10,2) (13,2,8,4)
```

These give 24 within-block edges. Add five cross edges:

```
(14,3) (6,8) (7,12) (9,10) (9,13)
```

**Theorem.** Let \(p_0,\ldots,p_{14}\) be distinct unit vectors in
\(\mathbb R^3\), and let \(1/2<t<3/5\). If \(p_i\cdot p_j=t\) on
every edge of \(G_{29}\), then

\[
F(t)=13t^5-t^4+6t^3+2t^2-3t-1=0,
\qquad p_3\cdot p_7=t.
\]

Thus \(t=t_0\), the unique root in the interval, and the entire labeled
Gram matrix is the known asymmetric incumbent's, up to \(O(3)\).

**Packing consequence.** A strictly better Tammes-15 packing cannot contain
\(G_{29}\) as a spanning subgraph of its contact graph, under any relabeling.
Its contact cosine would lie below \(t_0\); the elementary cap-area bound
gives \(\cos d\ge113/225>1/2\). Additional contacts do not evade the
exclusion. Other contact graphs remain unclassified.

## Geometry and five linear equations

Put \(H=(1-t)I+tJ\), \(P=(p_0\ p_5\ p_{11})\),
\(Q=(p_1\ p_2\ p_4)\), and \(M=P^TQ\). Both anchor Gram matrices
are \(H\), which is positive definite. As proved in README.md, distinctness
forces every indicated reflection:

\[
p_n=\frac{2t}{1+t}(p_i+p_j)-p_o.
\]

Both blocks therefore have forced coefficient vectors \(a_i,b_j\) in
their anchor bases. The five cross contacts give \(a_i^TMb_j=t\).
Enumerate entries of \(M\) row by row, from zero. Pivot indices are
\((1,2,3,4,5)\); free indices are \((0,6,7,8)\). Write
\((u,x,y,z)=(M_{00},M_{20},M_{21},M_{22})\) and
\(\beta=(1,u,x,y,z)^T\). The `linear` certificate table proposes

\[
\operatorname{vec}(M)=U(t)\beta/d_M(t).
\]

The checker constructs these equations from the reflection lists, verifies
the affine solution identity, and proves that the pivot determinant and
\(d_M\) never vanish on \([1/2,3/5]\). Before clearing coefficient-vector
denominators, this linear determinant is

\[
\frac{64t^5(3t+1)^2(5t^2-1)(3t^3-t^2+t+1)}{(t+1)^{12}}.
\]

Thus the chart omits no realization in the whole interval.

## Two metric identities and ten normal forms

Invertibility of \(P,Q\) and their common Gram matrix imply both identities

\[
M^TH^{-1}M=H,\qquad MH^{-1}M^T=H.
\]

Indeed \(PH^{-1}P^T=I\) proves the first, and \(QH^{-1}Q^T=I\) proves
the second. Write \(H^{-1}=G/h\), with \(h=(1-t)(1+2t)\), diagonal
entries of \(G\) equal to \(1+t\), and off-diagonal entries equal to \(-t\).

Each symmetric identity gives six equations in index order
\((00,01,02,11,12,22)\). Use all six from the first and the first four
from the second. Substitute \(U\beta/d_M\) and clear \(h d_M^2\), giving

\[
C(t)\mu+L(t)\beta=0,
\quad \mu=(u^2,ux,uy,uz,x^2,xy,xz,y^2,yz,z^2)^T.
\]

The checker computes the ten-by-ten determinant and proves it nonzero on
\([1/2,3/5]\). It verifies the polynomial identity \(CN+d_Q L=0\) from
the `quadratic` table, and proves \(d_Q\ne0\) there. Every realization
therefore satisfies \(\mu=\mathcal Q\beta\), with \(\mathcal Q=N/d_Q\).
The remaining two metric equations are unnecessary for this implication.

## Multiplication obstruction and completion

For each variable \(v\) among \(u,x,y,z\), form a five-by-five matrix
\(X_v\). Its first column is the standard basis vector for \(v\); its next
four columns are the transposed rows of \(\mathcal Q\) for \(vu,vx,vy,vz\).
At a common zero of the ten equations, \(\beta^TX_v=v\beta^T\).
Thus the nonzero row \(\beta^T\) annihilates

\[
W=\bigl([X_u,X_x]\mid[X_u,X_y]\bigr).
\]

The checker clears \(d_Q^2\), then divides individual columns only by
nonzero integers or factors certified nonzero throughout the interval.
Call the resulting matrix \(\widetilde W\). Its rank and left kernel are
unchanged at every parameter in the interval.

The five-by-five minors on zero-based columns \((1,2,3,6,7)\) and
\((1,2,3,6,8)\) must vanish. The checker computes them, removes only
certified nonzero factors, and obtains polynomials of degrees 34 and 33.
Their primitive gcd in \(\mathbb Q[t]\) is exactly \(F\); hence \(F(t)=0\).
Positive Bernstein coefficients of \(F'\), together with opposite endpoint
signs, give \(t=t_0\).

Define \(a,b,c\) as in README.md, whose fourfold numerators have ascending
integer coefficients:

```
4a = [-54,-12,140,-96,234]
4b = [-31,-38,136,-106,195]
4c = [81,42,-276,202,-429]
```

Exact identities modulo \(F\) verify \((1,a,b,c,a)\widetilde W=0\).
The four-by-four minor on rows \((1,2,3,4)\), columns \((1,2,3,6)\),
has numerator relatively prime to \(F\), so it stays nonzero at \(t_0\).
The left kernel is therefore one-dimensional. Since \(\beta\)'s first
entry is one, necessarily \((u,x,y,z)=(a,b,c,a)\). The checked affine
identity now gives

\[
M=\begin{pmatrix}a&b&c\\c&a&b\\b&c&a\end{pmatrix}.
\]

The checker finally verifies \(a_7^TMb_3=t\) modulo \(F\), restoring the
deleted contact. All 30 edges of the earlier classification are now present.
Its theorem and existence check identify the full Gram matrix with the known
asymmetric packing. This proves the statement.

## Divisors and trust boundary

In addition to the 13 factors in `verify.py`, the checker checks these ten:

```
3t^3-t^2+t+1; 4t^2-t-1; 11t^2+2t-1; 25t^3+23t^2+7t+1;
t^4-16t^3-8t^2+2t+1; 93t^6-57t^5-76t^4+42t^3+33t^2-t-2;
61t^5+31t^4+18t^3+30t^2+17t+3;
59t^6-12t^5-49t^4+4t^3+21t^2+8t+1;
126t^7-281t^6+157t^4-34t^3-39t^2+4t+3;
350t^7-323t^6-476t^5-t^4+38t^3-29t^2-8t+1.
```

Each has Bernstein coefficients of one strict sign on \([1/2,3/5]\),
checked with exact `Fraction` arithmetic. Divisors and pivot determinants
reduce to nonzero constants after these factors are removed. No exceptional
parameter is omitted. Safe row cancellation speeds determinant evaluation;
safe column cancellation speeds the commutator calculation. All cancellations
are checked.

The compact certificate contains the proposed affine and quadratic tables,
with integer coefficients in ascending order. The checker reconstructs their
defining equations and checks identities, determinants, gcds, root signs,
the normalized kernel, and the missing-contact equality. It imports the
existing integer-polynomial primitives and graph model, and invokes no
solver, computer algebra system, floating-point computation, external
coordinates, or private ledger. The geometric implication is the hand proof
above; no proof-assistant formalization is claimed.

## Reproduction

Python 3.11 or later, standard library only:

```sh
python3 -B tammes15_contact_pattern_obstruction/verify_deleted_contact.py --selftest
python3 -B tammes15_contact_pattern_obstruction/verify.py --selftest
```

The first prints `VERIFIED`, 29 prescribed edges, restored contact `[3,7]`,
obstruction `[-1,-3,2,6,-1,13]`, minor degrees `[34,33]`, a unique cross Gram
matrix, and successful controls rejecting two corrupted tables. The second
reproduces the earlier classification and incumbent existence checks used in
the final identification.

Regenerate using CPython 3.11 and SymPy 1.14.0:

```sh
python3 -m venv /tmp/tammes15-certificate-env
/tmp/tammes15-certificate-env/bin/pip install sympy==1.14.0
/tmp/tammes15-certificate-env/bin/python -B tammes15_contact_pattern_obstruction/generate_deleted_contact_certificate.py
python3 -B tammes15_contact_pattern_obstruction/verify_deleted_contact.py --selftest
```

The generator sets solver/BLAS/OpenMP thread variables to one. Full
regeneration must match the included certificate byte for byte.
The certificate SHA-256 is
`be9b87935ec5d6e601aa996efd5392651b954c612c935e47b32e80b852d210d3`.
On the authoring environment, verification took about one second and 14 MiB;
regeneration took 30.884 seconds and 53,092 KiB. Normal and optimized Python
checks, both corruption controls, and the prior classification check passed.
