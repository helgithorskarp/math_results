# Only cross four-cycles survive outside the source field

Put

\[
R=\mathbb Q(\sqrt{33}),\qquad
E=\mathbb Q(i\sqrt3,i\sqrt{11})=R+\alpha R,
\qquad \alpha=i\sqrt3.
\]

These are the specified real and complex embeddings. `E` is the restricted
complex field, not a Cartesian product of larger real coordinate fields.
Write `N(z)=z conjugate(z)` and `Tr(z)=z+conjugate(z)`.

**Theorem.** Let `P,Q subset E` and let `g` be a Euclidean isometry with
`g(E)!=E`. Every finite alternating unit cycle in `P union g(Q)` on
distinct plane points has length four. Equivalently, an alternating unit
cycle of any even length at least six forces `g(E)=E`.

No connectedness, cardinality or denominator restriction is needed for
this geometric theorem. Cycles need not be induced, and additional
overlaps outside the selected cycle are allowed. The distinctness is of
plane points, not merely of labels from two source copies.

**Colouring corollary.** If the unit-distance graphs of `P` and `Q` are
connected and their isometric union has any such alternating cycle, its
entire strict unit-distance graph is four-colourable. For a cycle of
length at least six apply the theorem and the prior
[whole-field colouring](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md).
For a four-cycle apply the prior
[cross-four-cycle gluing theorem](../hadwiger_nelson_cross_four_cycle_gluing/PROOF.md).

In particular, any non-four-colourable **disjoint** placement of the fixed
`B292/V214` alternative gadgets must have a cross graph that is a forest.
The [single-hub theorem](../hadwiger_nelson_mixed506_single_hub_reduction/PROOF.md)
then leaves at most one cross-degree-at-least-three vertex, of degree at
most ten. Its nontrivial cross components are paths, except possibly one
tree with one branch vertex and at most ten arms. This is a necessary
condition, not a proof that such forests always glue to four colours.
No five-chromatic graph is produced.

## 1. A cycle puts the isometry in one quadratic extension

We extend the geometric mechanism of the
[six-cycle theorem](../hadwiger_nelson_cross_six_cycle/PROOF.md), repeating
the needed argument to expose the longer-cycle and zero-vertex cases.
Conjugating `Q` absorbs reflection, so write `g(z)=u z+h`, `|u|=1`.
Suppose there is a cycle of length `2k`, with `k>=3`, on distinct points.
Its fixed vertices are `p_0,...,p_(k-1)` and its moving vertices are
`z_j=g(q_j)`, where `z_j` is unit distance from `p_j,p_(j+1)`; indices
are modulo `k`.

A point unit distance from three distinct `E`-points belongs to `E`.
Indeed, three distinct points on a circle are noncollinear. Subtracting
their squared-distance equations in the coordinates `x+alpha y` gives
a nonsingular linear system over `R` for the centre.

For distinct `a,b in E`, let `d=b-a`, `n=N(d)` and `m=(a+b)/2`.
Their unit-circle intersections, when present, are

\[
m\pm\frac{\alpha d}{2}\sqrt{D},\qquad
D=\frac{4-n}{3n}\in R,\quad D\geq0. \tag{1}
\]

Tangency has `D=0` and centre `m in E`. Otherwise a centre outside `E`
generates a quadratic field `E(sqrt(D))`, with a positive real square
root. A real square root in `E` would be in its real subfield `R`.

If two neighbour pairs share exactly one fixed point, their midpoints
are different. For chosen outside-field centres
`z_i=m_i+b_i sqrt(D_i)`, where `b_i!=0`, suppose their squared separation
is in `R`. Different quadratic fields would make
`1,sqrt(D_1),sqrt(D_2),sqrt(D_1 D_2)` independent over `E`. Expanding the
norm difference and equating its three nonconstant coefficients gives

\[
\operatorname{Tr}(\overline{m_1-m_2}b_1)=
\operatorname{Tr}(\overline{m_1-m_2}b_2)=
\operatorname{Tr}(\overline{b_1}b_2)=0.
\]

The two nonzero offsets are perpendicular; the midpoint difference is
perpendicular to both. Thus the midpoints are equal, a contradiction.
The two outside-field centres consequently generate the same quadratic
extension.

In the selected cycle, all moving squared separations are in `R`, since
they equal the corresponding source squared separations. If two moving
vertices belong to `E`, their differences give `u,h in E`, contrary to
`g(E)!=E`. Hence at most one moving vertex is in `E`. The remaining
outside-field moving vertices form a connected chain of successive
neighbour pairs around the cycle, after deleting that one vertex if
necessary. Since `k>=3`, there are at least two of them. The preceding
argument puts them all in a common quadratic extension `L/E`, and any
remaining moving vertex is in `E subset L`. Taking two moving differences
and then a translation gives `u,h in L`.

If `u in E` but `h not in E`, each cross edge yields an offset
`v=p-uq in E` satisfying `|h-v|=1`. There are at most two different offsets,
by the three-centre fact above. Incident cycle edges have distinct offsets,
so they must alternate two values `v_1,v_2`. Summing alternate equations
around the `2k`-cycle gives `k(v_1-v_2)=0`, impossible in characteristic
zero. This branch has no finite simple cross cycle.

## 2. The non-base rotation puts the cycle on two lines

We may now assume `u not in E`, so `L=E(u)`. Write uniquely

\[
h=m-u n,\qquad m,n\in E,
\qquad u^2-Tu+J=0,\quad T,J\in E.
\]

For a cross edge let `x=p-m`, `y=q-n`, `c=conjugate(x)y` and
`S=N(x)+N(y)-1`. Multiplying the unit-distance equation by `u` gives
`c u^2-Su+conjugate(c)=0`. Independence of `1,u` yields

\[
cT=S,\qquad \overline c=Jc. \tag{2}
\]

Any two nonzero cross values of `c` have real ratio. Two edges sharing
a nonzero centred vertex therefore have opposite centred endpoints on
one real line. Propagating along a path with no zero centred vertex puts
its fixed vertices on one line through `m` and its moving vertices on
another. Among the selected distinct plane vertices, at most one is `m`.
Delete it if present and propagate along the remaining `2k-1` vertex
path. A deleted vertex belongs to both lines. This proves the two-line
reduction without dividing by zero, and also covers `T=0`.

Coincident lines cannot contain a finite simple unit cycle: the largest
coordinate of a selected point has at most one unit neighbour among the
other selected points. Thus the two lines are distinct.

Choose a nonzero fixed centred point `a in E` and a nonzero moving source
centred point `b in E` as line directions. Every fixed centred cycle point
is `a r_i` and every moving source centred point is `b s_i`, with
`r_i,s_i in R`: the ratios lie in `E` and are real. The actual moving
points are `m+u b s_i`. Define

\[
A=N(a)>0,\qquad B=N(b)>0,\qquad
H=\operatorname{Re}(\overline a u b).
\]

There is a cross cycle edge with both centred endpoints nonzero. Its unit
equation expresses `H` as an element of `R`. Distinct lines give
`H^2<AB`. The cycle edges satisfy the positive definite conic equation

\[
F(r,s):=Ar^2+Bs^2-2Hrs=1. \tag{3}
\]

## 3. The cycle gives a finite-order matrix over R

At a fixed `s`, the two distinct neighbouring `r` coordinates are the
two roots of (3), so the other root is `r'=2Hs/A-r`. At that next `r'`,
the other moving coordinate is `s'=2Hr'/B-s`. Two steps around the cycle
therefore act by

\[
\begin{pmatrix}r'\\s'\end{pmatrix}
=M\begin{pmatrix}r\\s\end{pmatrix},\qquad
M=\begin{pmatrix}
-1&2H/A\\
-2H/B&4H^2/(AB)-1
\end{pmatrix}\in\operatorname{SL}_2(R). \tag{4}
\]

The matrix preserves the positive definite form `F`. If `H=0`, it is
`-I` and has order two. Otherwise its trace is strictly between `-2` and
`2`, and it has two distinct complex conjugate eigenvalues. Returning
to the starting edge gives `M^k(r,s)=(r,s)` for a nonzero state. Thus an
eigenvalue of `M^k` is one; the conjugate eigenvalue is also one, so
diagonalizability gives `M^k=I`. Its order is exactly `k`: a smaller order
would repeat the starting edge before the simple cycle finished.
This also shows directly why tangency, which has only one neighbour
along a line, cannot be used as a step of the cycle.

## 4. Finite-order traces in Q(sqrt(33)) are rational integers

**Trace lemma.** A finite-order determinant-one matrix over `R` has trace
in `{-2,-1,0,1,2}`.

Write its trace as `tau=a+b sqrt(33)`, with rational `a,b`. Its eigenvalues
are roots of unity, so `tau` is an algebraic integer. Applying the other
real embedding of `R` to the matrix preserves finite order and determinant
one. Both `tau` and `tau'=a-b sqrt(33)` consequently lie in `[-2,2]`.

If `b!=0`, the algebraic trace and norm of `tau` give
`2a in Z` and `a^2-33b^2 in Z`. Hence `132b^2 in Z`. Writing `b=c/d` in
lowest terms shows `d^2` divides `132=4*3*11`, so `d` is one or two.
Therefore `|b|>=1/2`, which gives

\[
|\tau-\tau'|=2|b|\sqrt{33}\geq\sqrt{33}>4,
\]

contradicting the interval bounds. Thus `b=0`; a rational algebraic
integer is an integer, proving the lemma. No bound on the possible
cycle length was used.

For (4) put

\[
\tau=\operatorname{tr}(M)=\frac{4H^2}{AB}-2.
\]

Since `H^2<AB`, `tau!=2`. The possible traces and exact orders are

| Trace | Order of M | Possible cycle length |
|---|---:|---:|
| `-2` | 2 | 4 |
| `-1` | 3 | 6 |
| `0` | 4 | 8 |
| `1` | 6 | 12 |

For trace `-2`, (4) is `-I`. For the other traces the orders follow from
the characteristic polynomials `X^2+X+1`, `X^2+1`, and `X^2-X+1`.
This table is a uniform finite-order reduction, not a scan up to length
twelve. All other finite lengths have already been excluded.

## 5. The three remaining traces contradict a non-base isometry

The trace `-2` case has order two, contrary to `k>=3`. In each remaining
case `H!=0`. Write `Z=conjugate(a)u b`. It has real part `H` and
norm `AB`.

If `tau=-1`, then `AB=4H^2` and
`Z=H(1+/-alpha) in E`. If `tau=1`, then `AB=4H^2/3` and
`Z=H(1+/-alpha/3) in E`. Either expression puts
`u=Z/(conjugate(a)b)` in `E`, a contradiction.

If `tau=0`, then `AB=2H^2`. Multiplicativity of the norm would give

\[
N(ab/H)=2,\qquad ab/H\in E. \tag{5}
\]

But two is not a norm from this `E`. The prior field theorem supplies a
conjugation-compatible embedding `E -> Q_2(omega)`,
`omega^2+omega+1=0`. For `z` mapping to `x+y omega`,

\[
v_2(N(z))=v_2(x^2-xy+y^2)
=2\min(v_2(x),v_2(y)).
\]

The last equality follows by extracting the common power of two and
checking the three nonzero residue pairs. Norm valuations are even,
whereas `v_2(2)=1`. This contradicts (5). All cases for `k>=3` are now
excluded, proving the theorem and the stated colouring corollary.

## 6. Exact boundary examples and computational role

Cross four-cycles outside `E` do exist. The small example
`P={+/-alpha/4}`, `Q={+/-(1+2alpha)/4}` with
`u=(1-2alpha)/sqrt(13)` has `u outside E` and all four cross distances one.
Thus the geometric theorem cannot replace "length four" by "no cycle".
Four-colourability of a cyclic union uses the separate gluing theorem.

The norm-two obstruction is specific to the source field. Put
`K'=E(sqrt(2))` and take

\[
P=\{7/5,1/5,-7/5,-1/5\},\qquad
Q=\frac{\sqrt2}{5}\{4,-3,-4,3\},\qquad
g(z)=\frac{1+i}{\sqrt2}z.
\]

These are subsets of `K'`, and all eight placed points are distinct.
The complete cross graph is an eight-cycle, while `g(K')!=K'`.
Here `N(sqrt(2))=2`, so (5) is possible. This is a counterexample to
extending the cycle classification to that larger field, not a
five-chromatic graph. The matrix with rows `(0,-1),(1,sqrt(2))` likewise
has order eight over `Q(sqrt(2))`, showing that the rational-trace lemma
cannot simply be transferred to every real quadratic field.

The source includes exact field-preserving six-, eight-, and twelve-cycle
examples and an outside-field quadratic path. Thus the theorem excludes
long cycles only in the non-field-preserving branch; it does not assert
that unit cycles themselves are impossible in `E`. The path explicitly
retains an acyclic case outside the closed family.

`verify.py` expands the matrix, root-exchange, invariant-form and order
identities and checks the finite arithmetic used in the trace and norm
arguments. `examples.py` constructs the geometries by exact complex
multiquadratic arithmetic. A separate rational Gram-matrix audit compares
every squared distance, strict edge and colouring, and checks the cross
components independently. These are author checks of identities and
examples. The arbitrary-cycle, algebraic-integrality and local-field
bridges are the unformalized proof above, not deductions from samples.

The archived [gadget provenance](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md)
and [fixed inner construction](../hadwiger_nelson_nonmono159_moser_triple/PROOF.md)
are unchanged. Primary construction source: Parts,
[Graph minimization](https://arxiv.org/abs/2010.12665).
[Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4),
checked on 2026-09-05, retains the 509-vertex benchmark. No record
improvement or novelty priority is claimed. Neither the sealed Parts pool
nor the parked Parts L/S overlap family is enumerated here.
