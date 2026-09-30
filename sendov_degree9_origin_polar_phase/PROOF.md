# A sharp communication comparison on the coalesced unit phase face

Author: **six-sendov-1**, role **researcher**. Date: 2026-09-30.
Status: complete ordinary proof with a finite exact polynomial certificate;
independent review is pending. The written bridges are unformalized.

This is a functional lemma and a precise obstruction to two proposed
certificate classes. It does not establish a new unconditional polynomial
case or the general first-power Tang--Zhang conjecture.

## 1. The two-value frontier and classical communication identities

Let a monic degree-nine polynomial have all original zeros in the closed
unit disk and a simple marked zero. Rotate the variable so the marked
zero is $a\in(0,1)$. Write $b=1-a^2$, and put
$q_j=(a-\zeta_j)^{-1}$ for the eight derivative zeros, with multiplicity.
The critical-disk condition and radial lower bound are

$$f_a(q_j):=b|q_j|^2+2a\Re q_j-1\ge0,
\qquad |q_j|\ge(1+a)^{-1}. \tag{1}$$

If $z_i$ are the other eight original zeros, integrating the derivative
from $a$ to $0$ and to $1/a$ gives, respectively,

$$O=9\int_0^1\prod_j(1-atq_j)\,dt
  =\prod_i z_i\prod_jq_j, \tag{2}$$

$$C=\int_0^1\prod_j(a+btq_j)\,dt
  =\prod_i\frac{1-az_i}{a-z_i}. \tag{3}$$

For (3), $p(1/a)=b a^{-9}\prod_i(1-az_i)$, while direct integration gives
$9b a^{-9}\prod_j(a-\zeta_j)C$. Use
$p'(a)=\prod_i(a-z_i)=9\prod_j(a-\zeta_j)$.
The marked root is simple, so these denominators are nonzero.
Moreover

$$|1-az_i|^2-|a-z_i|^2=b(1-|z_i|^2)\ge0.$$

Consequently an actual disk-root polynomial satisfies

$$|O|\le\rho:=\prod_j|q_j|,\qquad
|C|\ge1,\qquad
I:=\int_0^1\prod_j|a+btq_j|\,dt\ge|C|. \tag{4}$$

These are classical communication identities, credited to
[Zhang, Lemma 3.1](https://arxiv.org/html/2609.19126) and
[Tao, Lemma 6](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/).
Keeping the complex integral in (3) avoids the triangle-inequality loss
in the weaker condition $I\ge1$. We claim no novelty for these identities.

Our unresolved reduction restricts to $q_1=\cdots=q_4=U$ and
$q_5=\cdots=q_8=V$, with arbitrary complex $U,V$. Its abstract domain is

$$0<a<1,\quad r=|U|,\ s=|V|,\ r,s\ge(1+a)^{-1},\quad
r+s\le2,\quad f_a(U),f_a(V)\ge0. \tag{5}$$

Here $
ho=r^4s^4$. Any hypothetical first-power failure in this critical
multiplicity class must obey (5), $|O|\le\rho$ and $|C|\ge1$.
The results below concern a face and certificate limitations; they do
not prove incompatibility of this full system.

## 2. The sharp comparison

On the coalesced unit face set $U=V=q$, $|q|=1$ and $x=\Re q$.
Condition (1) is exactly $x\ge a/2$. Define

$$O_a(q)=9\int_0^1(1-atq)^8\,dt,\qquad
C_a(q)=\int_0^1(a+btq)^8\,dt.$$

**Phase lemma.** For $0<a<1$, $|q|=1$ and $a/2\le\Re q\le1$,

$$\boxed{|C_a(q)|<1+\frac43(1-a^2)(|O_a(q)|^2-1).} \tag{6}$$

Equivalently,

$$J_{3/4}^{\rm norm}
 :=|O_a(q)|^2-1+\frac{3}{4b}(1-|C_a(q)|)>0. \tag{7}$$

The weight $3/4$ is the largest real constant for which the corresponding
nonnegative comparison can hold on this entire face. Equation (6)
excludes $|O_a|\le1$, $|C_a|\ge1$ there. The actual one-critical-point
polynomial family is a regular nine-gon and is already understood;
this exclusion is not presented as a new polynomial theorem.

### Exact reduction to two real polynomials

Let $T_k$ be the Chebyshev polynomials, defined by
$T_0=1$, $T_1=x$, $T_{k+1}=2xT_k-T_{k-1}$. For unit $q$,
$\Re(q^k)=T_k(x)$. Set

$$o_k=\frac{9\binom8k(-a)^k}{k+1},\qquad
c_k=\frac{\binom8k a^{8-k}b^k}{k+1}.$$

The exact norm polynomials are

$$N_o=\sum_k o_k^2+2\sum_{j>k}o_jo_kT_{j-k}(x)=|O_a(q)|^2,$$

$$N_c=\sum_k c_k^2+2\sum_{j>k}c_jc_kT_{j-k}(x)=|C_a(q)|^2. \tag{8}$$

Define $R=1+(4/3)b(N_o-1)$ and $D=R^2-N_c$, and substitute

$$x=\frac a2+\left(1-\frac a2\right)y,\qquad 0\le y\le1. \tag{9}$$

This parametrizes every allowed phase, including both imaginary signs.
After substitution the degree bounds in $(a,y)$ are $(18,8)$ for $R$
and $(36,16)$ for $D$. The included checker constructs their complete
power-basis coefficients from (8), not from sampled values.

### Finite certificate and strictness

Use tensor Bernstein bases on each $a$ interval and $y\in[0,1]$.
The following covers are exact:

| Polynomial | Intervals in $a$ | Coefficients per interval |
|---|---|---:|
| $R$ | $[0,1/2],[1/2,3/4],[3/4,7/8],[7/8,1]$ | $19\cdot9=171$ |
| $D$ | $[0,1/2],[1/2,5/8],[5/8,3/4],[3/4,7/8],[7/8,1]$ | $37\cdot17=629$ |

All **3,829** coefficients are checked, including zero entries.
Every $R$ coefficient is strictly positive. Every $D$ coefficient is
strictly positive except on the last interval, where all coefficients
are nonnegative, the row at $a$ index zero is strictly positive, and
the row at $a$ index 36 consists of 17 zeros.

Bernstein basis functions are nonnegative and sum to one. Thus $R>0$.
On the last interval put $a=7/8+t/8$. If $t<1$, its index-zero basis
factor $(1-t)^{36}$ is strictly positive; the positive row therefore
gives $D>0$ for every $y$, including $y=0,1$. Other intervals have
strictly positive coefficients throughout. Hence $D>0$ for $a<1$,
and $|C_a|=\sqrt{N_c}<R$, proving (6).

[algebra.py](algebra.py) additionally reconstructs both norm polynomials
by an independent quotient-ring calculation
$\mathbb Q[a,x,q]/(q^2-2xq+1)$, where $\overline q=2x-q$.
It compares every power coefficient. For each of the nine cells the
checker applies the complete inverse Bernstein transform and compares
the original local power polynomial. Thus neither a degree extent nor
a coefficient list is accepted from an external positivity oracle.
[expected.json](expected.json) records compact minima, zero counts,
complete coefficient hashes and exact obstruction data; it is not an
external proof corpus. Removing a cell, duplicating a cell, introducing
a negative coefficient, changing a coefficient, or exceeding the
stated degree is detected by the included mutation controls.

## 3. Sharp weight and two impossible fixed-weight alternatives

For the positive-real family $q=1$, put $\delta=1-a$. Then

$$O_a(1)=\frac{1-\delta^9}{a},\qquad
C_a(1)=I_a(1)=\int_0^1(a+bt)^8\,dt>0.$$

Exact polynomial expansion gives

$$|O_a(1)|^2-1=2\delta+O(\delta^2),\qquad
I_a(1)-1=\frac{16}{3}\delta^2+O(\delta^3). \tag{10}$$

Therefore, for any fixed real weight $\lambda$,

$$J_\lambda^{\rm norm}
 =\delta\left(2-\frac83\lambda\right)+O_\lambda(\delta^2). \tag{11}$$

If $\lambda>3/4$, this is negative for all sufficiently small positive
$\delta$. Together with (7), this proves the asserted sharpness.
At $\lambda=3/4$ the next term is $(11/2)\delta^2>0$.
The checker verifies the exact low-order coefficients, so this limit
argument does not depend on numerical extrapolation.

On the larger domain (5), define two different candidates:

$$J_\lambda^{\rm triangle}
=\frac{|O|^2}{\rho^2}-1+\lambda\frac{1-I}{b},\qquad
J_\lambda^{\rm square}
=\frac{|O|^2}{\rho^2}-1+\lambda\frac{1-|C|^2}{b}. \tag{12}$$

For $\lambda\ge0$, positivity of either would exclude the relevant
necessary conditions from (4). The square candidate retains the complex
polar integral, but squares its modulus. This differs from (7).

**Fixed-weight obstruction.** No real constant $\lambda$ makes either
candidate in (12) nonnegative on all of (5). This remains true if
$U\ne V$, $r+s<2$ and both disk inequalities are required to be strict.
This statement concerns exactly the normalizations in (12); it is not
an obstruction to every possible combination of communication identities.

First, the family $U=V=1$ in (10) forces
$\lambda\le3/4$ for the triangle candidate and $\lambda\le3/8$ for
the square candidate. Indeed $|C|^2-1=(32/3)\delta^2+O(\delta^3)$,
so their leading terms are, respectively,
$\delta(2-8\lambda/3)$ and $\delta(2-16\lambda/3)$.

Second, take the explicit Gaussian-rational point

$$a=\frac{102}{149},\qquad
U=V=q=\frac{51+140i}{149},\qquad r=s=1. \tag{13}$$

It satisfies $|q|=1$, $f_a(q)=0$, the radial lower bounds and the budget.
The exact checker gives

$$|O|^2=
\frac{3165887550005216675137055729601}
 {59017430136820283047307224487697601}<\frac1{1000},$$

$$I=
\frac{157108497345077507655296710971200971}
 {531156871231382547425765020389278409}<1,$$

$$J_{3/4}^{\rm triangle}=
-\frac{2121189943792465155184957524301973}
 {354104580820921698283843346926185606}<0. \tag{14}$$

Thus every $\lambda\le3/4$ fails at (13), because $1-I>0$.
For the square candidate, $b>1/2$ and $|C|^2\ge0$ imply

$$J_{3/8}^{\rm square}\le |O|^2-1+\frac{3}{8b}
<\frac1{1000}-1+\frac34=-\frac{249}{1000}<0.$$

Also $|C|\le I<1$, so every $\lambda\le3/8$ fails there.
Weights above these thresholds have already been excluded by the family
approaching $a=1$. This proves both assertions for all real constants.
The exact point requires triangle weight greater than approximately
$0.754520$ and square weight greater than approximately $0.555679$;
these decimals are explanatory, while the exact lower fractions are
in the fixed manifest.

To obtain strict distinct-value witnesses, use continuity at the strict
negative values of $J$. Near (13), move each unit phase slightly toward
the positive axis to make both disk inequalities strict, using distinct
phase changes. Then decrease their radii by sufficiently small positive
amounts: strict disk feasibility and negativity persist, the budget
becomes slack, and the radial lower bounds remain strict. Near $U=V=1$
the disk inequalities are already strict; distinct small radial/phase
perturbations with slack budget preserve the negative value. This is
an existence argument for each fixed weight, not an assertion that the
same perturbation works uniformly for all weights.

The point (13) violates the actual-polynomial requirement $I\ge1$.
It is an abstract method witness, never a counterexample to the first-power
conjecture or to ordinary Sendov.

## 4. Reproducibility, literature boundary and remaining work

From the repository root, with Python 3.11 standard library:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B sendov_degree9_origin_polar_phase/verify.py
~~~

Expected: 3,829 exact Bernstein coefficients, two complete norm identities,
nine complete inverse basis identities, both fixed-weight obstructions,
sharp weight $3/4$, and five rejected mutations. No floating-point,
root-solving, solver or external data enters this proof computation.
The arithmetic trust boundary is Python integer/Fraction arithmetic and
the published algorithms. The written identity, phase parametrization,
strictness, asymptotic sign and continuity arguments remain unformalized.

[LITERATURE.md](LITERATURE.md) positions this functional claim against the
quadratic theorem, the conjectural first-power endpoint, the independently
reviewed reflection-symmetric theorem, and the previous conjugate-matching
criterion. No exhaustive historical-priority claim is made.

The concrete next target is an analogue of (6) for arbitrary $U,V$ in
(5), with the normalization $|O|^2/\rho^2$. Bounded floating-point
experiments motivated that target but do not prove it. Unequal radii,
noncoalesced phases and unsaturated budgets have not been reduced to
the present face. Alternatively, an exact coexistence witness would
delimit the joint-identity route. Neither conclusion is asserted here.
