# The directional-rank invariant of the Farey triangle

## 1. Setup

Work over `F_2`.  Let `T_(r,s)` translate a configuration by `(r,s)`, and let

\[
R=\mathbb F_2[X^{\pm1},Y^{\pm1}]
\]

act by `X^rY^s -> T_(r,s)`.  Put

\[
F=(1+X)(1+Y)(1+XY).
\]

The preceding Farey-triangle reduction proves that every `c in X_F` has a
decomposition

\[
c(i,j)=A(j)+B(i)+C(j-i),                         \tag{1}
\]

for binary bi-infinite sequences `A,B,C`.  We first remove the apparent
nonuniqueness of (1).

## 2. The gauge lemma

**Lemma 1 (three-line functional equation).**  If binary sequences `U,V,W`
satisfy

\[
U(x)+V(y)+W(x-y)=0\qquad(x,y\in\mathbb Z),       \tag{2}
\]

then for some `epsilon,u,v,w in F_2`, with `u+v+w=0`,

\[
U(n)=\epsilon n+u,\quad V(n)=\epsilon n+v,
\quad W(n)=\epsilon n+w.                         \tag{3}
\]

Here `epsilon n` means `epsilon` times the parity of `n`.

**Proof.**  Put `y=0` in (2) and eliminate `W`.  Evaluating the resulting
identity also at `x=y` shows that, after adding constants, all three functions
come from one function `f` with `f(0)=0` and

\[
f(x-y)=f(x)+f(y).
\]

Thus `f: Z -> F_2` is a group homomorphism.  It is determined by
`epsilon=f(1)`, and restoring the constants gives (3).  Substitution into (2)
gives `u+v+w=0`. `square`

**Corollary 2 (gauge uniqueness).**  Two triples `(A,B,C)` and
`(A',B',C')` represent the same configuration in (1) if and only if their
componentwise differences have the form (3).  Consequently, whether each of
the three components is periodic is independent of the chosen decomposition.

**Proof.**  Subtract the two representations and apply Lemma 1.  Every
parity-affine sequence has period at most two.  Adding such a sequence
preserves, in both directions, the property of being periodic. `square`

This permits the following definition.

**Definition.**  The **directional rank** `rho(c)` is the number of
nonperiodic sequences among `A,B,C` in any representation (1).

## 3. Exact periods

For a sequence `U`, write

\[
\delta_tU(n)=U(n+t)+U(n).
\]

**Proposition 3 (synchronized-derivative criterion).**  A vector `(p,q)` is a
period of (1) if and only if there are `epsilon,a,b,d in F_2`, with
`a+b+d=0`, such that

\[
\begin{aligned}
\delta_q A(n)&=\epsilon n+a,\\
\delta_p B(n)&=\epsilon n+b,\\
\delta_{q-p}C(n)&=\epsilon n+d.
\end{aligned}                                    \tag{4}
\]

**Proof.**  The difference between `c(i+p,j+q)` and `c(i,j)` is

\[
\delta_qA(j)+\delta_pB(i)+\delta_{q-p}C(j-i).
\]

It vanishes identically exactly when Lemma 1 applies to these three
derivatives. `square`

If `t` is nonzero and `delta_t U(n)=epsilon n+a`, then

\[
\delta_{2t}U(n)=\epsilon t,
\qquad \delta_{4t}U(n)=0.                         \tag{5}
\]

Thus `U` is periodic.  Among `p,q,q-p`, at least two are nonzero whenever
`(p,q)` is nonzero.  Proposition 3 and (5) therefore give one implication of
the next theorem.  Conversely, if at most one component is nonperiodic, move
in its invariant direction and take a common multiple of periods of the other
two components.

**Theorem 4 (periodicity by directional rank).**

\[
c\text{ has a nonzero period}\quad\Longleftrightarrow\quad \rho(c)\leq1.
                                                               \tag{6}
\]

More explicitly, if only `A` may be nonperiodic, a common period `p` of `B`
and `C` makes `(p,0)` a period of `c`.  The other two cases give `(0,q)` and
`(p,p)`, respectively.

## 4. Recovering rank from the annihilator ideal

Let `Ann(c)` be the ideal of Laurent polynomials in `R` annihilating `c`.
It contains `F`.  Hence the common divisor of all its nonzero elements is
well-defined up to a unit and divides the squarefree polynomial `F`.  Denote
this common divisor by `g_c`.

We use one elementary one-dimensional fact: a binary bi-infinite sequence
annihilated by a nonzero Laurent polynomial is periodic.  Indeed, after a
monomial shift the relation is a finite recurrence with nonzero first and last
coefficients.  Its finite state evolves bijectively, so every bi-infinite orbit
is a cycle.

**Theorem 5 (annihilator-gcd formula).**  For a representation (1), set
`epsilon_A=1` when `A` is nonperiodic and `0` otherwise, and define
`epsilon_B,epsilon_C` similarly.  Then

\[
g_c=(1+X)^{\epsilon_A}(1+Y)^{\epsilon_B}
    (1+XY)^{\epsilon_C}                           \tag{7}
\]

up to a Laurent monomial.  In particular,

\[
\rho(c)=\text{the number of irreducible Farey factors of }g_c. \tag{8}
\]

**Proof.**  Take `p in Ann(c)`.  Applying `p` to (1) gives

\[
A_p(j)+B_p(i)+C_p(j-i)=0,                         \tag{9}
\]

where the three terms are obtained by the one-variable substitutions

\[
p(1,Z),\qquad p(Z,1),\qquad p(Z^{-1},Z),           \tag{10}
\]

acting on `A,B,C`, respectively.  By Lemma 1, each output in (9) is
parity-affine and hence two-periodic.

Suppose `A` is nonperiodic.  If `p(1,Z)` were nonzero, multiplying it by
`1+Z^2` would give a nonzero one-dimensional annihilator of `A`, contradicting
the fact above.  Therefore `p(1,Z)=0`, which is equivalent to `1+X` dividing
`p`.  The same argument gives

- nonperiodic `B` implies `1+Y` divides every `p in Ann(c)`;
- nonperiodic `C` implies `1+XY` divides every `p in Ann(c)`.

For the last equivalence, the kernel of the substitution
`X -> Z^{-1}, Y -> Z` is the principal ideal `(1+XY)`.

It remains to show that no factor is mandatory when its component is
periodic.  If `A` has positive period `m`, then

\[
p_A=(1+Y^m)(1+Y)(1+XY)                            \tag{11}
\]

annihilates `c`: its three displayed factors kill `A,B,C`, respectively.
But `p_A(1,Y)=(1+Y^m)(1+Y)^2` is nonzero, so `1+X` does not divide `p_A`.
Similarly, for periods `n` of `B` and `ell` of `C`,

\[
\begin{aligned}
p_B&=(1+X^n)(1+X)(1+XY),\\
p_C&=(1+X^\ell)(1+X)(1+Y)
\end{aligned}                                     \tag{12}
\]

avoid `1+Y` and `1+XY`, respectively.  Because `F` itself belongs to
`Ann(c)` and its three factors are pairwise nonassociate irreducibles in the
Laurent UFD `R`, these forced and avoided factors prove (7). `square`

## 5. Consequence and boundary

The unresolved generalized-Nivat question for `X_F` now has only two
nonperiodic strata:

- `rho(c)=2`: one periodic component acts as a finite phase mask on a
  two-direction nonperiodic core;
- `rho(c)=3`: every binary annihilator of `c` is divisible by all of `F`, so
  `g_c=F`.

This rules out decomposition-dependent case distinctions and makes the three
directions algebraically detectable.  It does **not** show that either stratum
has high complexity for every finite window, and hence does not settle GNP.
