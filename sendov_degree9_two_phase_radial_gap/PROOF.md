# Two unit phases and a quantitative radial obstruction

Author: **six-sendov-1**, role **researcher**. Date: 2026-09-30.
Status: ordinary written proof with a complete exact polynomial certificate;
independent review is pending. The written analytic bridges are unformalized.

The main result extends the earlier coalesced-unit functional comparison to
two independent unit directions, with an explicit margin. It then gives a
necessary radial gap for an abstract four-plus-four critical-reciprocal system.
The unrestricted two-value case and general first-power Tang--Zhang conjecture
remain unproved. The displayed polynomial consequence is a sufficient
criterion, without a claim that its very small region supplies new nonempty
polynomial examples or improves every earlier near-boundary estimate.

## 1. The two-phase functional theorem

Let $0<a<1$, $b=1-a^2$, and let $u,v$ be complex numbers such that

$$|u|=|v|=1,\qquad \Re(u+v)\ge a.$$

Define

$$O_0=9\int_0^1(1-at u)^4(1-at v)^4\,dt,\qquad
C_0=\int_0^1(a+bt u)^4(a+bt v)^4\,dt,$$

$$R=1+\frac43 b(|O_0|^2-1),\qquad
\theta=1-\frac{\Re(u+v)}2\in[0,1].$$

**Theorem 1.** We have $R>0$ and

$$\boxed{R^2-|C_0|^2\ \ge\ b\left(\frac{(1-a)^2}{100}
                      +\frac{\theta}{1000}\right)>0.} \tag{1}$$

In particular,

$$|C_0|<1+\frac43 b(|O_0|^2-1). \tag{2}$$

The phases need not coincide, be conjugate, or separately satisfy
$\Re u,\Re v\ge a/2$. Only their mean real part is constrained.
The coefficient $4/3$ in (2) is the same as in the
[previous coalesced-unit lemma](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_origin_polar_phase/PROOF.md).
This contribution proves a larger phase domain and the quantitative margin;
it does not reclassify that earlier theorem's fixed-weight obstructions.

### A common phase with an independent separation parameter

Put $S=u+v$. Since $\Re S\ge a>0$, $S\ne0$. Define

$$c=\frac{|S|}{2},\qquad w=\frac{S}{|S|},\qquad x=\Re w.$$

Then $0<c\le1$, $|w|=1$, and $u+v=2cw$. The identity
$S=uv\overline S$ shows $uv=w^2$. Hence

$$c x=\frac{\Re(u+v)}2\ge\frac a2,
\qquad \frac a2\le c\le1,\quad \frac a2\le x\le1. \tag{3}$$

No choice of a square-root branch or angle is needed; both imaginary
orientations are included. The two pair products become

$$ (1-at u)(1-at v)=1-2acwt+a^2w^2t^2,$$
$$ (a+bt u)(a+bt v)=a^2+2abcwt+b^2w^2t^2. \tag{4}$$

Let $h_k(c)$ be the coefficients of

$$ (1-2ct+t^2)^4=\sum_{k=0}^8 h_k(c)t^k.$$

In order, these are

$$1,\ -8c,\ 4+24c^2,\ -24c-32c^3,\ 6+48c^2+16c^4,
\ -24c-32c^3,\ 4+24c^2,\ -8c,\ 1.$$

Therefore $O_0=\sum_k o_k w^k$ and $C_0=\sum_k d_k w^k$, where

$$o_k=\frac{9h_k(c)a^k}{k+1},\qquad
d_k=\frac{(-1)^k h_k(c)a^{8-k}b^k}{k+1}. \tag{5}$$

For $T_0(x)=1$, $T_1(x)=x$, $T_{j+1}=2xT_j-T_{j-1}$, define

$$N_o=\sum_k o_k^2+2\sum_{j>k}o_jo_kT_{j-k}(x),\qquad
N_c=\sum_k d_k^2+2\sum_{j>k}d_jd_kT_{j-k}(x). \tag{6}$$

Since $\Re(w^j)=T_j(x)$, these are the complete norm polynomials
$|O_0|^2$ and $|C_0|^2$. Now construct, in $\mathbb Q[a,c,x]$,

$$R=1+\frac43 b(N_o-1),\qquad
H=\frac{R^2-N_c}{b},$$

$$K=H-\frac{(1-a)^2}{100}-\frac{1-cx}{1000}. \tag{7}$$

The numerator in $H$ is exactly divisible by $b$ as a polynomial;
the checker reconstructs the quotient and verifies every coefficient of
the identity $bH=R^2-N_c$, including the zero remainder.

### Complete rational Bernstein certificate

We prove $R>0$ and $K\ge0$ on the larger rectangle
$c,x\in[a/2,1]$. This contains (3); it does not assert that every point
of the rectangle satisfies the stronger product constraint $cx\ge a/2$.
Use independent cube coordinates $y,z\in[0,1]$:

$$c=\frac a2+\left(1-\frac a2\right)y,\qquad
x=\frac a2+\left(1-\frac a2\right)z. \tag{8}$$

After (8), the complete degree extents in $(a,y,z)$ are $(22,8,8)$
for $R$ and $(42,16,16)$ for $K$. For each polynomial use these five
exact intervals in $a$:

$$[0,1/2],\quad[1/2,5/8],\quad[5/8,3/4],\quad
[3/4,7/8],\quad[7/8,1]. \tag{9}$$

Writing $a=L+(U-L)t$ on a cell, a power polynomial of degrees
$(n_0,n_1,n_2)$ has tensor Bernstein coefficients

$$\beta_{i,j,k}=\sum_{p\le i,q\le j,r\le k}\alpha_{p,q,r}
\frac{\binom{i}{p}}{\binom{n_0}{p}}
\frac{\binom{j}{q}}{\binom{n_1}{q}}
\frac{\binom{k}{r}}{\binom{n_2}{r}}. \tag{10}$$

All **71,450** entries are regenerated and checked, including zeros:

| Polynomial | Degree extent | Cells | Entries per cell | Sign result |
|---|---|---:|---:|---|
| $R$ | $(22,8,8)$ | 5 | $23\cdot9\cdot9=1,863$ | all strictly positive |
| $K$ | $(42,16,16)$ | 5 | $43\cdot17\cdot17=12,427$ | all nonnegative |

The first four $K$ cells have strictly positive coefficients. The last
has exactly two zeros. Their indices, each cell's exact minimum, and
hashes of the complete ordered rational arrays are recorded in
[expected.json](expected.json); the arrays themselves are generated locally.

For completeness, the checker also:

- compares the nine $h_k$ polynomials against a separate multinomial formula;
- compares both full norm polynomials against reduction in
  $\mathbb Q[a,c,x,w]/(w^2-2xw+1)$, using $\overline w=2x-w$;
- compares both complete substitutions (8) against grouped Horner evaluation;
- reconstructs every local power polynomial by the inverse tensor transform
  $\alpha_j=\binom n j\sum_{i\le j}(-1)^{j-i}\binom j i\beta_i$
  on each of its three axes, giving ten full inverse identities;
- rejects five deliberate coverage, coefficient-sign, degree and inverse
  mutations, and checks the radial constants and the cleared identity below.

These are separate reconstruction algorithms in the author's checker,
not an independent peer-review verdict. The fixed manifest is compared only
after all identities and sign checks have passed.

Bernstein basis functions are nonnegative and sum to one on the unit cube.
Thus $R>0$ and $K\ge0$ on all cells. Since $b>0$ and $(1-a)^2>0$,
(7) gives (1), and $R>0$ justifies the square-root comparison (2).
No strictness inference from a sampled interior point is used.

## 2. Disk geometry projects unequal radii into the certified phase domain

Let $U=r u$ and $V=s v$, with $r,s>0$, $|u|=|v|=1$, and assume

$$r+s\le2,\qquad
b|U|^2+2a\Re U-1\ge0,\qquad
b|V|^2+2a\Re V-1\ge0. \tag{11}$$

Dividing the last two inequalities by $r,s$ and adding gives

$$2a\Re(u+v)\ge\frac1r+\frac1s-b(r+s).$$

Writing $\sigma=2-r-s\ge0$, the exact identity is

$$\frac1r+\frac1s-b(r+s)
=2a^2+(2-a^2)\sigma+\frac{(r-1)^2}{r}+\frac{(s-1)^2}{s}. \tag{12}$$

In particular $\Re(u+v)\ge a$. Thus the unit projections of every
pair obeying (11) lie in Theorem 1's domain, even when one projected
direction separately has real part below $a/2$. Identity (12) also
retains both the budget slack and the radial quadratic loss. It is a
classical elementary harmonic-mean refinement, not claimed as a new
general inequality. The checker verifies the full identity after
multiplication by $rs$.

## 3. A quantitative obstruction to the joint communication conditions

For the same $U,V$ define

$$O=9\int_0^1(1-atU)^4(1-atV)^4\,dt,\qquad
C=\int_0^1(a+btU)^4(a+btV)^4\,dt,$$

$$\rho=r^4s^4,\qquad \varepsilon=\max\{|r-1|,|s-1|\}.$$

**Theorem 2.** If (11) holds and both communication conditions

$$|O|\le\rho,\qquad |C|\ge1 \tag{13}$$

hold, then the following necessary radial gap holds:

$$\boxed{\varepsilon\ \ge\ \frac{(1-a)^2}{12\,010\,000}
                 +\frac{1-\Re(u+v)/2}{120\,100\,000}.} \tag{14}$$

No optimality of these constants is claimed. This is an obstruction
in the abstract reciprocal system, not a proof that arbitrary unequal
radii cannot satisfy it.

### Uniform radial transport estimates

First suppose $\varepsilon\le1/40\,000$. In particular
$\varepsilon\le1/100$ and $r,s\ge1-\varepsilon>0$. Normalize the
origin integral before perturbing the radii:

$$\widetilde O=\frac{O}{U^4V^4}
=9\int_0^1(U^{-1}-at)^4(V^{-1}-at)^4\,dt.$$

Its unit-radius counterpart $\widetilde O_0=O_0/(u^4v^4)$ has
modulus $|O_0|$. For each factor, inverse-radius displacement is at
most $\varepsilon/(1-\varepsilon)\le(100/99)\varepsilon$, and
all actual and unit factor moduli are bounded by
$1+a+1/99\le199/99$. Telescoping the product of eight factors,
then integrating and multiplying by nine, gives

$$|\widetilde O-\widetilde O_0|
\le72\left(\frac{199}{99}\right)^7\frac{100}{99}\varepsilon
\le10000\varepsilon. \tag{15}$$

For the polar factors, the displacement is at most $b\varepsilon$.
Using $a+b\le5/4$ gives
$a+b(1+\varepsilon)\le63/50$. Hence

$$|C-C_0|\le8\left(\frac{63}{50}\right)^7 b\varepsilon
\le50b\varepsilon. \tag{16}$$

The two leading rational constants in (15),(16) are strictly less than
$10000,50$, respectively; those rational comparisons are checked.
The weak inequalities displayed here suffice for (14).

Under (13), (15),(16) imply

$$|O_0|\le1+10000\varepsilon,\qquad
|C_0|\ge1-50b\varepsilon>0.$$

With $z=10000\varepsilon\le1$, $2z+z^2\le3z$, so

$$0<R\le1+40000b\varepsilon.$$

As $40000b\varepsilon\le1$, the elementary bound
$(1+h)^2\le1+3h$ for $0\le h\le1$ yields

$$\begin{aligned}
R^2-|C_0|^2
&\le(1+40000b\varepsilon)^2-(1-50b\varepsilon)^2\\
&\le120100b\varepsilon. \tag{17}
\end{aligned}$$

Identity (12) supplies the hypothesis of Theorem 1. Combining (1)
with (17) and cancelling $b>0$ gives (14) in the small-radius window.
If instead $\varepsilon>1/40000$, the right side of (14) is at most

$$\frac{1/100+1/1000}{120100}
=\frac{11}{120100000}<\frac1{40000},$$

because $0<(1-a)^2<1$ and $0\le\theta\le1$. Thus (14) also holds
outside that window. This completes the proof without an assumption
that the radii are close to one.

## 4. Consequence and exact remaining boundary for degree nine

For a monic degree-nine polynomial with all original zeros in the
closed unit disk, rotate a simple marked zero to $a\in(0,1)$, and put
$q_j=(a-\zeta_j)^{-1}$ for the eight derivative zeros. Gauss--Lucas
gives $\zeta_j$ in the closed disk and hence

$$b|q_j|^2+2a\Re q_j-1\ge0.$$

If $z_i$ are the other eight original zeros, derivative integration gives
the classical communication identities

$$O=9\int_0^1\prod_{j=1}^8(1-atq_j)\,dt
 =\prod_{i=1}^8z_i\prod_{j=1}^8q_j,$$

$$C=\int_0^1\prod_{j=1}^8(a+btq_j)\,dt
 =\prod_{i=1}^8\frac{1-az_i}{a-z_i}. \tag{18}$$

For the second identity, integrate from $a$ to $1/a$ and use
$p'(a)=\prod_i(a-z_i)=9\prod_j(a-\zeta_j)$.
These are prior communication machinery, credited to
[Zhang, Lemma 3.1](https://arxiv.org/html/2609.19126) and
[Tao, Lemma 6](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/).
Indeed $|1-az_i|^2-|a-z_i|^2=b(1-|z_i|^2)\ge0$, so an actual
polynomial satisfies $|O|\le\prod_j|q_j|$ and $|C|\ge1$.

Restrict to the critical multiset $q_1=\cdots=q_4=U$,
$q_5=\cdots=q_8=V$, allowing $U=V$. Any hypothetical failure

$$S_1=\sum_{j=1}^8|a-\zeta_j|^{-1}=4(r+s)\le8$$

therefore satisfies (11),(13) and must obey (14). In particular,

$$\max\{|r-1|,|s-1|\}<\frac{(1-a)^2}{12010000}
\quad\Longrightarrow\quad S_1>8. \tag{19}$$

This implication is a derived sufficient criterion. We do not claim
that the narrow radial window contains a new nontrivial polynomial
family, or that it is stronger than all known quantitative versions of
ordinary Sendov. The new reusable object is the phase comparison with
margin and the consequent abstract joint-identity obstruction.
The central marked root, unit-circle marked root, and repeated marked
root are outside (19)'s stated hypotheses; no claim about their status
is needed for this proof.

Theorem 2 allows substantial radial displacement. It does not eliminate
all such tuples, certify the full four-plus-four first-power case, or
classify all disk-root polynomials with those critical multiplicities.
Identity (12)'s slack and radial losses offer the next concrete route:
control the full radial transport against the available phase margin,
or find an exact coexistence witness to delimit that route.

## 5. Reproduction and trust boundary

From the repository root, Python 3.11 standard library:

~~~sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B sendov_degree9_two_phase_radial_gap/verify.py
~~~

Expected: 71,450 exact rational Bernstein entries, two complete norm
identities, ten complete inverse basis identities, two independent
phase substitutions, the radial constants and identity, and five
rejected mutations. Generated arrays are held locally and not required
as an external corpus. No floating-point arithmetic, root solve,
solver, external library or downloaded certificate enters the proof
computation. The arithmetic trust boundary is Python unbounded
integer/Fraction arithmetic and the published algorithms. The written
phase geometry, Bernstein positivity, analytic transport, classical
polynomial identities and inequalities remain unformalized.

[LITERATURE.md](LITERATURE.md) records the exact literature boundary
and earlier complementary contributions. Independent review is pending.
