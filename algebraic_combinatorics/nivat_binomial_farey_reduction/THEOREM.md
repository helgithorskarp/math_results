# One Farey triangle is the entire unresolved binomial-product frontier

## 1. Definitions

For `u=(a,b)` write `X^u=X^aY^b`.  Let `U=(u_1,...,u_r)` be a nonempty
finite list of nonzero vectors in `Z^2`, and put

\[
 f_U=\prod_{i=1}^r(1+X^{u_i})
 \quad\hbox{in}\quad
 R=\mathbb F_2[X^{\pm1},Y^{\pm1}].
\]

The algebraic subshift `X_f` consists of the binary configurations annihilated
by `f`. It has the **generalized Nivat property (GNP)** if every member `c`
for which `P_c(D)<=|D|` for some finite nonempty `D subset Z^2` has a
nonzero translation period. Vectors on the same rational line have the same
unoriented direction.

Multiplying `f` by a monomial does not change `X_f`. A matrix in `GL_2(Z)`
relabels the lattice, bijects translates of every finite window, and preserves
nonzero periods. Hence GNP is invariant under monomial association and
unimodular coordinate changes.

## 2. Classification reduction

**Theorem (Farey-triangle reduction).** Exactly the following alternatives
cover every binary binomial product `f_U`.

1. If all `u_i` have one direction, then `X_(f_U)` has GNP.
2. Suppose at least two directions occur. If some `u_i` is nonprimitive, if
   a direction is repeated, or if two distinct directions have determinant
   of absolute value greater than one, then `X_(f_U)` does not have GNP.
3. In every remaining two-direction case, there is one factor in each
   direction and their determinant has absolute value one. The polynomial is
   unimodularly equivalent, up to a monomial, to
   `(1+X)(1+Y)`, whose subshift has GNP.
4. In every remaining three-direction case, there is one factor in each
   direction and the polynomial is unimodularly equivalent, up to a
   monomial, to
   \[
   F_\triangle=(1+X)(1+Y)(1+XY).                 \tag{1}
   \]
5. No remaining case has four or more directions.

Consequently, deciding whether (1) has GNP completes the GNP classification
of all products of binary translation binomials. This theorem does **not**
decide that final case.

### The inherited lattice-index obstruction

We use the following two-factor fact. If independent `a,b in Z^2` satisfy
`|det(a,b)|>1`, then

\[
g=(1+X^a)(1+X^b)
\]

has a nonperiodic low-complexity member. Indeed, with
`L=Za+Zb` choose `t notin L` and take, over `F_2`,

\[
c={\bf1}_{Za}+{\bf1}_{t+Zb}.
\]

The two summands have periods `a` and `b`, so `gc=0`. The two support lines
lie in different `L`-cosets, and a two-point test on either line excludes
every proposed nonzero period. On

\[
D=\{ia+jb:0\leq i\leq2,\ 0\leq j\leq1\},
\]

the translated patterns are the zero pattern, the three row indicators, and
the two column indicators. Thus `P_c(D)=6=|D|`. If `g` divides `f_U`, then
`X_g subset X_(f_U)`, so the same configuration disproves GNP for `f_U`.

Now assume at least two directions occur.

- If `u_i=k u` with primitive `u` and `|k|>1`, choose a nonparallel factor
  `v`. Then `|det(u_i,v)|>1`, so the preceding obstruction divides `f_U`.
- If a primitive direction `u` occurs twice, its two binomials are monomial
  associates (the exponents are `u` and possibly `-u`). Up to a monomial,
  characteristic two gives `(1+X^u)^2=1+X^{2u}`. Together with any
  nonparallel factor `v`, this is a bad two-factor divisor because
  `|det(2u,v)|>=2`.
- If two distinct primitive directions have determinant of absolute value
  greater than one, their displayed factors themselves form a bad divisor.

Therefore every surviving factor is primitive, every direction occurs once,
and every two direction representatives have determinant of absolute value
one.

### The Farey clique lemma

**Lemma.** A set of pairwise nonparallel unoriented primitive directions in
`Z^2` whose pairwise determinants all have absolute value one has at most
three elements. If it has three, some choice of signs and a matrix in
`GL_2(Z)` takes it to

\[
\{(1,0),(0,1),(1,1)\}.                            \tag{2}
\]

**Proof.** Choose two representatives `u,v` and orient them so that
`det(u,v)=1`. For any third representative `w`, write `w=a u+b v`.
Then

\[
a=det(w,v),\qquad b=det(u,w),
\]

so `a,b` both belong to `{+1,-1}`. Because directions are unoriented, signs
of `u` and `v` may be changed, and the triple becomes `{u,v,u+v}`.

For a fourth direction `z=c u+d v`, the same argument gives
`c,d in {+1,-1}`. But

\[
|det(u+v,z)|=|d-c|,
\]

which is zero or two, never one. Hence no fourth direction exists. The basis
`u,v` supplies the required unimodular change of coordinates. `square`

With two directions the same basis change produces `(1+X)(1+Y)`. With three,
the lemma produces (1). The positive one-direction and four-dot assertions
are the published Kari--Moutot results cited in [SOURCES.md](SOURCES.md).
This proves the theorem.

The lemma says that the surviving direction sets are precisely edges and
triangles of the Farey graph; it is the reason no undifferentiated
four-factor frontier remains.

## 3. Exact structure of the triangular kernel

Write `Delta_u=1+T_u`, where `T_u` is translation by `u`. Let
`e_1=(1,0)`, `e_2=(0,1)`, and `d=e_1+e_2`.

**Proposition (three-direction decomposition).** A binary configuration `c`
is annihilated by `F_triangle` if and only if

\[
c=h+v+s,
\quad
\Delta_{e_1}h=0,
\quad
\Delta_{e_2}v=0,
\quad
\Delta_d s=0.                                     \tag{3}
\]

Equivalently, for some arbitrary bi-infinite binary sequences `A,B,C`,

\[
c(i,j)=A(j)+B(i)+C(j-i)\pmod2.                    \tag{4}
\]

**Proof.** Every sum in (3) is killed by the product of the three commuting
differences, proving one direction.

Conversely suppose
`Delta_(e_1) Delta_(e_2) Delta_d c=0`, and set
`q=Delta_(e_2) Delta_d c`. Then `Delta_(e_1)q=0`, so
`q(i,j)=Q(j)` for a binary sequence `Q`.

On an `e_1`-periodic configuration `h(i,j)=H(j)`, both `Delta_(e_2)` and
`Delta_d` act as the same one-dimensional difference `1+S`. Hence

\[
\Delta_{e_2}\Delta_d h=(1+S)^2H=(1+S^2)H.
\]

The map `1+S^2` is surjective on bi-infinite binary sequences: choose
`H(0),H(1)` arbitrarily and solve `H(j)+H(j-2)=Q(j)` recursively in both
directions, separately on the even and odd indices. Choose such an `h`.
Then `c+h` is killed by `Delta_(e_2)Delta_d`.

The vectors `e_2,d` are a lattice basis. In their coordinates, every solution
of `Delta_(e_2)Delta_d z=0` satisfies

\[
z(a,b)=z(a,0)+z(0,b)+z(0,0),
\]

as follows directly by iterating the four-dot relation. The first term is
`d`-periodic and the remaining two terms form an `e_2`-periodic
configuration. Thus `c+h=v+s`, proving (3), and (4) is just coordinate
notation. `square`

Over a finite odd `N` by `N` torus, the triangular kernel has dimension
`3N-2` and equals the sum of the three directional kernels. The checker
verifies this for the stated sizes. This finite observation is corroboration,
not the proof of the bi-infinite proposition.

## 4. Boundary of the result

The canonical polynomial expands to the six terms

\[
1+X+Y+X^2Y+XY^2+X^2Y^2.
\]

Its support differences generate the full lattice and every pair of factor
directions is unimodular. It therefore has none of the proper-sublattice
two-factor obstructions used above. A positive proof must exploit the
interaction of all three directional components in (4); a negative proof
must provide a genuinely new low-complexity mechanism.

Nothing here asserts GNP for (1), treats arbitrary line-polynomial factors,
or changes the rectangular Nivat conjecture. The reduction is elementary and
search-relative; no exclusive historical priority is claimed.
