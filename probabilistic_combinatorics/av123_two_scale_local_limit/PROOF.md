# A two-scale local limit for fixed points and excedances in Av(123)

Researcher 4, Discovery Net graph campaign, 22 September 2026.

This is a written analytic proof, not a proof-assistant formalization. Its
enumerative input is the existing two-corner formula of Li, Theorem 3.2,
also extending the ballot-hook distance formula in the source graph.
The known Brownian-excursion distance law is recovered as a normalization
step. The result developed here is the finer joint law and local limit.
See [SOURCES.md](SOURCES.md) for exact versions and the novelty boundary.

## 1. Statements

Let $\pi_n$ be uniform among the $C_n=(n+1)^{-1}\binom{2n}{n}$
permutations of $[n]$ avoiding an increasing subsequence of length three.
Let $A_n$ be the event that it has two fixed points. On $A_n$, write
those fixed points as $a<b$, and put

$$
d=b-a,\qquad e=\#\{i:\pi_n(i)>i\},\qquad
h=a+b-n-1,\qquad k=2e-n+2.
$$

All conditioning below is on events of positive probability. In particular
$A_n$ has positive probability for every $n\ge4$.

**Theorem 1 (joint limit).** As $n\to\infty$, conditional on $A_n$,

$$
\left(\frac d{\sqrt n},\frac h{n^{1/4}},\frac k{n^{1/4}}\right)
\ \Longrightarrow
\left(R,\sqrt{R/2}\,Z_1,\sqrt{R/2}\,Z_2\right),                 \tag{1}
$$

where $Z_1,Z_2$ are independent standard normal variables, jointly
independent of $R$, and

$$
f_R(r)=\frac4{\sqrt\pi}r^2e^{-r^2}\quad(r>0).
$$

The limiting density on $(0,\infty)\times\mathbb R^2$ is

$$
f(r,u,v)=\frac4{\pi^{3/2}}r
 \exp\left(-r^2-\frac{u^2+v^2}{r}\right).                    \tag{2}
$$

Thus the midpoint displacement
$(a+b)/2-(n+1)/2$ and the excedance displacement $e-(n-2)/2$
have scale $n^{1/4}$, each with limiting conditional variance $R/8$
after division by $n^{1/4}$. Their Gaussian limits are independent
*given* $R$; the common random variance generally prevents unconditional
independence. No joint limit with an entire excursion process is asserted.

**Theorem 2 (uniform local limit).** Fix $0<\epsilon<M<\infty$
and $T<\infty$. For integers $(n,d,a,e)$, put

$$
r=d/\sqrt n,\quad u=(2a+d-n-1)/n^{1/4},\quad
v=(2e-n+2)/n^{1/4}.
$$

Uniformly over $\epsilon\le r\le M$, $|u|,|v|\le T$,

$$
\begin{aligned}
&\mathbb P(\operatorname{Fix}(\pi_n)=\{a,a+d\},
                   \operatorname{exc}(\pi_n)=e)\\
&\qquad=\frac{r}{\pi^{3/2}n}
   \exp\left(-r^2-\frac{u^2+v^2}{r}\right)
   \bigl(1+O_{\epsilon,M,T}(n^{-1/2})\bigr).
\end{aligned}                                            \tag{3}
$$

For all sufficiently large $n$ these integer triples are feasible.
Conditional on $A_n$, the right side of (3) is instead

$$
\frac{16r}{\pi^{3/2}n}
   \exp\left(-r^2-\frac{u^2+v^2}{r}\right)(1+o(1)),          \tag{4}
$$

with the same uniformity. The scaled lattice has cell volume $4/n$,
so (4) agrees with (2). Neither (3) nor (4) is a boundary estimate for
$d=o(\sqrt n)$ or $d/\sqrt n\to\infty$.

We also prove the following conditional approximation, which specifies
the mechanism and controls the secondary tails.

**Theorem 3 (parity-binomial approximation).** Put $m=d-1$ and
$L=n-d-1$. Let $X$ count middle values $a<\pi_n(i)<a+d$
at positions $i<a$, and let $Y$ count positions $a<i<a+d$
with values $\pi_n(i)>a+d$. Given $A_n$ and $d$, the law of
$(X,Y)$ is within

$$
C\left(\frac1m+\frac mL\right)                            \tag{5}
$$

in total variation of two independent $\operatorname{Bin}(m,1/2)$
variables conditioned on their sum being congruent to $L\pmod2$,
whenever $m\ge8$ and $L\ge4m$. Here $C$ is universal;
total variation means half the sum of the absolute mass differences.
Consequently the error is $O_{\epsilon,M}(n^{-1/2})$ uniformly on
$\epsilon\sqrt n\le d\le M\sqrt n$.

## 2. Exact enumerative input and lattice

Set

$$
B_L(t)=
\begin{cases}
\binom L{(L-t)/2}-\binom L{(L-t)/2-1},
       &0\le t\le L,\ t\equiv L\pmod2,\\
0,&\text{otherwise}.
\end{cases}                                               \tag{6}
$$

For nonnegative $L$, a binomial coefficient with lower index outside
$[0,L]$ is zero. The exact number with specified $(d,X=x,Y=y)$ is

$$
W_{n,d}(x,y)=\binom mx\binom my B_L(x+y)B_L(2m-x-y),        \tag{7}
$$

where $0\le x,y\le m$. The count is zero if $d>\lfloor n/2\rfloor$.
Moreover

$$
2a=n-d+1+x-y,\qquad 2e=L+x+y,\qquad
h=x-y,\quad k=x+y-m.                                     \tag{8}
$$

Here (7) is **prior work**, not a new enumeration. To translate Li's
Theorem 3.2, replace his middle-position variable $y$ by $m-y$
(his variable counts positions occupied by lower values). His two
interior sizes become $(L-x-y)/2$ and $(L-2m+x+y)/2$.
His forest number $T(j,t)$ equals $B_{2j+t}(t)$. Both ballot
lengths are therefore $L$, proving (7) from the cited formula.
The two-corner cell counts give (8): the upper corner contains exactly
the excedances, and the row and column sums determine $a$.
The supplied literal-permutation auditor independently checks all these
identities and every joint count through size nine.

For fixed $d$, write

$$
s=x+y,\quad g(s)=B_L(s)B_L(2m-s),\quad
F_{n,d}=\sum_{s\equiv L\ (2)}\binom{2m}s g(s).              \tag{9}
$$

Vandermonde's identity justifies (9), with zero terms understood.
The nonzero lattice in $(h,k)$ has

$$
h\equiv L\pmod2,\qquad k\equiv n\pmod2,\qquad
x=(m+k+h)/2,\quad y=(m+k-h)/2.                            \tag{10}
$$

There is no further parity restriction. Its finite support additionally
requires $|h|+|k|\le m$ and $m\pm k\le L$. On the compact
ranges in Theorem 2 these inequalities hold eventually. The two
coordinates $h,k$ each have spacing two. Including spacing one in
$d$, their scaled cell volume is $1/\sqrt n\cdot
2/n^{1/4}\cdot2/n^{1/4}=4/n$. The parity class of $h$ shifts when
$d$ changes, without changing this volume.

## 3. Ballot log-concavity and a quantitative comparison

For an admissible height $t$, (6) gives

$$
B_L(t)=\frac{2(t+1)}{L+t+2}\binom L{(L-t)/2},\qquad
q_L(t):=\frac{B_L(t+2)}{B_L(t)}
 =\frac{t+3}{t+1}\frac{L-t}{L+t+4}.                       \tag{11}
$$

Both positive factors in $q_L(t)$ decrease with $t$. Hence
$B_L$, on its parity lattice, is log-concave. The product $g(s)$
is symmetric about $m$ and has its maximum at
$s_*=m+\delta$, where $\delta\in\{0,1\}$ makes
$m+\delta\equiv L\pmod2$. When $\delta=1$, both
$m-1$ and $m+1$ attain that maximum. Set $G=g(s_*)$.
If $m\ge8,L\ge4m$, every parity-admissible $s\in[0,2m]$
has positive ballot factors and $G>0$.

For completeness, the following discrete curvature bound quantifies the
central plateau. Extend the rational expression $q_L$ to real
$0\le t<L$. Then

$$
-\frac{d}{dt}\log q_L(t)
=\frac2{(t+1)(t+3)}+\frac1{L-t}+\frac1{L+t+4}.             \tag{12}
$$

On $[m/2-2,3m/2]$, under $m\ge8,L\ge4m$, (12) is
bounded by $C_0(m^{-2}+L^{-1})$ for a universal constant $C_0$.
For $u\ge\delta$ on the correct parity lattice,

$$
\frac{g(m+u+2)}{g(m+u)}
=\frac{q_L(m+u)}{q_L(m-u-2)}.                             \tag{13}
$$

For $0\le u\le m/2$, sum the logarithms of (13) from the
maximizer to $u$; all intermediate arguments lie in the interval
used in (12). Symmetry handles negative $u$. We obtain

$$
0\le\log\frac G{g(m+u)}
 \le C_1(u^2+1)(m^{-2}+L^{-1})\quad (|u|\le m/2).          \tag{14}
$$

Let $Q$ be the parity-conditioned independent binomial law in
Theorem 3. Before parity conditioning, $S=X+Y$ is
$\operatorname{Bin}(2m,1/2)$. Each parity has probability $1/2$
for $m\ge1$, so

$$
Q(X=x,Y=y)=2^{1-2m}\binom mx\binom my\,
                 \mathbf1_{x+y\equiv L\ (2)}.             \tag{15}
$$

In particular $\mathbb E_Q(S-m)^2\le m$, by bounding
conditional expectations of nonnegative quantities by twice their
unconditional values. Also

$$
Q(|S-m|>m/2)\le4e^{-m/4}.                                \tag{16}
$$

One elementary justification is
$\mathbb E e^{t(S-m)}=\cosh(t/2)^{2m}\le e^{mt^2/4}$;
Chernoff optimization gives each one-sided unconditional tail at
displacement $z$ at most $e^{-z^2/m}$, and conditioning costs
at most a factor two.

Put $w=g(S)/G$, so $0\le w\le1$. By (14), (16), and
$1-e^{-z}\le z$,

$$
\eta:=\mathbb E_Q(1-w)
 \le C_1(m+1)(m^{-2}+L^{-1})+4e^{-m/4}
 \le C_2(m^{-1}+m/L).                                    \tag{17}
$$

The actual conditional law $P$ in (7) satisfies
$dP/dQ=w/(1-\eta)$. Therefore

$$
\|P-Q\|_{\rm TV}
\le\frac{\eta}{1-\eta}.                                 \tag{18}
$$

If $C_2(m^{-1}+m/L)<1/2$, this proves (5) with constant
$2C_2$; otherwise the trivial bound $\|P-Q\|_{\rm TV}\le1$
proves the same assertion after increasing the constant. This proves
Theorem 3. Notice that a pointwise central approximation alone would
not have justified this total variation statement; the maximum and
tail controls above are essential.

## 4. Uniform asymptotics and a global distance envelope

Stirling's formula with its bounded remainder gives, uniformly for
admissible $0\le t\le A\sqrt L$,

$$
\binom L{(L-t)/2}
=2^L\sqrt{\frac2{\pi L}}\,
 e^{-t^2/(2L)}(1+O_A(L^{-1})).                            \tag{19}
$$

Indeed expansion of the entropy about $1/2$ has leading exponent
$-t^2/(2L)$, next error $O(t^4/L^3)$, and prefactor error
$O(t^2/L^2+L^{-1})$. On this range all are $O_A(L^{-1})$.
This verifies the required uniformity rather than invoking a central
limit estimate outside its stated range.

If $\epsilon\sqrt n\le d\le M\sqrt n$ and $|k|\le Tn^{1/4}$,
apply (11) and (19) to $m+k,m-k$. The exact rational factor is

$$
\frac{4(d^2-k^2)}{n^2-k^2},                              \tag{20}
$$

because $m+1=d$ and $L+m+2=n$. It follows that

$$
g(m+k)=\frac{2^{2L+3}}\pi\frac{d^2}{n^3}e^{-d^2/n}
       (1+O_{\epsilon,M,T}(n^{-1/2})).                    \tag{21}
$$

For clarity, the product of the two binomial approximations in (19)
is $4^L(2/(\pi L))e^{-(m^2+k^2)/L}(1+O(n^{-1}))$.
Inserting (20), replacing $L$ by $n$, and replacing
$m^2/L$ by $d^2/n$ each have relative error
$O_{\epsilon,M,T}(n^{-1/2})$; also $k^2/L=O(n^{-1/2})$.
Thus (21) includes the centering and parity corrections.

At $k=\delta$, (21) estimates $G$. Equations (9), (15), and
(17) give $F_{n,d}=2^{2m-1}G(1-\eta)$. Hence

$$
F_{n,d}=\frac{4^{n-1}}\pi\frac{d^2}{n^3}e^{-d^2/n}
             (1+O_{\epsilon,M}(n^{-1/2})),                \tag{22}
$$

since $L+m=n-2$. Dividing by
$C_n=4^n/(\sqrt\pi n^{3/2})(1+O(n^{-1}))$ gives

$$
\frac{F_{n,d}}{C_n}
=\frac1{\sqrt n}\frac{r^2}{4\sqrt\pi}e^{-r^2}
             (1+O_{\epsilon,M}(n^{-1/2})).                \tag{23}
$$

To normalize (23) without an unjustified exchange of limits, we next
prove a bound valid for all distances. There is an absolute constant
$C_3$ such that

$$
B_L(t)\le C_3\frac{2^L(t+1)}{(L+1)^{3/2}}
                 e^{-t^2/(4(L+1))}.                     \tag{24}
$$

Here inadmissible heights have value zero. To see the bound on the
binomial factor, divide by its central coefficient, which is at most
$C2^L/\sqrt{L+1}$. For even $L=2j,t=2q$, the ratio is
$\prod_{i=1}^q(j-i+1)/(j+i)$. Since $\log(1-z)\le-z$
and $j+i\le L$, it is at most $e^{-q^2/L}$.
For odd $L=2j+1,t=2q+1$, the analogous product is
$\prod_{i=1}^q(j-i+1)/(j+i+1)$, at most
$e^{-q(q+1)/L}$. These estimates imply the Gaussian factor in
(24) with a fixed constant. Multiplication by the first factor of
(11) proves (24). The case $L=0$ is checked directly.

For $n\ge4$, $2\le d\le n/2$, we have $L\ge m$, so a
central admissible pair $m\pm\delta$ exists. Its product is the
maximum of $g$, even if the feasible interval in $s$ is shorter
than $[0,2m]$. Use (24),
$(m+\delta+1)(m-\delta+1)\le d^2$, and
$(m+\delta)^2+(m-\delta)^2\ge2m^2$. As
$n/2\le L+1\le n$ and $m\ge d/2$, (9) is bounded by
$C4^{n-2}d^2n^{-3}e^{-d^2/(8n)}$. A uniform lower bound
$C_n\ge c4^n n^{-3/2}$ follows from Stirling's inequalities.
For $d=1$, (9) is zero for odd $n$; for even $n$, it is
$C_{(n-2)/2}^2$, which satisfies the same bound after adjusting
the constant. We have proved the global envelope

$$
\boxed{\quad \frac{F_{n,d}}{C_n}
 \le C_4\frac{d^2}{n^{3/2}}e^{-d^2/(8n)}\quad}            \tag{25}
$$

for every $n\ge4$, $1\le d\le\lfloor n/2\rfloor$.

Summing (25) below $\epsilon\sqrt n$ gives
$O(\epsilon^3)+o(1)$. Above $M\sqrt n$, its sum is bounded
by a constant times the tail integral of $r^2e^{-r^2/8}$,
plus a term tending to zero. On the intervening compact interval use
(23) as a Riemann sum. Therefore

$$
q_n:=\mathbb P(A_n)\longrightarrow
\int_0^\infty\frac{r^2}{4\sqrt\pi}e^{-r^2}\,dr=\frac1{16}, \tag{26}
$$

and, conditional on $A_n$, $d/\sqrt n\Rightarrow R$.
The envelope proves all truncations used here; no limiting-mass
assumption is needed. Formula (26) and this distance law were already
established by Hoffman--Rizzolo--Slivken through Brownian excursion.
Their result identifies $R$ in law with $\sqrt2\,\mathbb e(1/2)$.

## 5. The secondary Gaussian kernel and joint convergence

Under independent $X,Y\sim\operatorname{Bin}(m,1/2)$, the pair
$((X-m/2)/\sqrt{m/4},(Y-m/2)/\sqrt{m/4})$ tends to two
independent standard normals. This remains true after either parity
conditioning on $X+Y$. Here is an explicit justification. The
conditioned characteristic function is the unconditioned one plus
an alternating term from
$2\mathbf1_{X+Y\equiv p}=1+(-1)^{X+Y-p}$.
The unconditioned function is
$\cos(t/\sqrt m)^m\cos(v/\sqrt m)^m\to
e^{-(t^2+v^2)/2}$. The absolute value of the alternating term is
$|\sin(t/\sqrt m)\sin(v/\sqrt m)|^m\to0$, uniformly for
bounded $t,v$ and for either parity $p$.

Apply the orthogonal change of variables in (8). Under $Q$,

$$
\left(\frac{X-Y}{\sqrt{m/2}},\frac{X+Y-m}{\sqrt{m/2}}\right)
\Longrightarrow (Z_1,Z_2).                              \tag{27}
$$

The convergence is uniform over the two parity choices and over
$m\ge m_0$ as $m_0\to\infty$. Theorem 3 transports (27)
to the actual conditional law, uniformly for
$\epsilon\sqrt n\le d\le M\sqrt n$.

Let $U_n=h/\sqrt{(d-1)/2}$ and
$V_n=k/\sqrt{(d-1)/2}$ when $d\ge2$, assigning arbitrary
values when $d=1$. That exceptional event has conditional
probability tending to zero by (25), (26). For any real $t,v,w$,
condition on $d$, restrict first to a compact distance interval,
and use the uniform characteristic-function convergence (27).
The contribution outside that interval tends to zero as
$\epsilon\downarrow0,M\uparrow\infty$ by (25), (26).
It follows that

$$
\mathbb E\!\left[e^{itd/\sqrt n+ivU_n+iwV_n}\mid A_n\right]
\longrightarrow \mathbb E e^{itR}\,e^{-(v^2+w^2)/2}.
$$

The continuity theorem yields joint convergence to independent
$(R,Z_1,Z_2)$. Since
$h/n^{1/4}=\sqrt{(d-1)/(2\sqrt n)}\,U_n$, and similarly
for $k$, the continuous mapping theorem gives (1). Multiplying
the two conditional normal densities by $f_R$ gives (2).

## 6. Local constants

For the integer triples in Theorem 2, the values in (10) satisfy

$$
x=m/2+(h+k)/2,\qquad y=m/2+(k-h)/2.
$$

Applying the same entropy expansion as in (19) at these two binomial
centers, uniformly on the stated ranges, gives

$$
\binom mx\binom my
=4^m\frac2{\pi m}\exp\left(-\frac{h^2+k^2}{m}\right)
      (1+O_{\epsilon,M,T}(m^{-1})).                       \tag{28}
$$

Multiply (28) by (21) and divide by $C_n$. As $L+m=n-2$,
the powers of two leave

$$
\frac{W_{n,d}(x,y)}{C_n}
=\frac{d^2}{\pi^{3/2}m n^{3/2}}
 e^{-d^2/n-(h^2+k^2)/m}(1+O_{\epsilon,M,T}(n^{-1/2})).
$$

Replacing $m=d-1$ by $d$ in the prefactor and exponent
has relative error $O_{\epsilon,M,T}(n^{-1/2})$.
This is (3). Equation (26) gives (4), completing the proof.

## 7. Evidence and limits

The proof uses the published exact formula, elementary binomial
identities, Stirling's formula, and standard weak-convergence tools.
The normal and local limits are established analytically, with uniform
errors and an explicit global tail envelope. The computational checks
audit the translation to literal permutations, parity, finite ballot
identities, and the constants; they do not prove an asymptotic statement
by testing finitely many sizes.

The approximation constant in (5) is universal but is not optimized or
assigned a numerical value. The conditional local error in (4) is
qualitative because (26) was used without a convergence rate. No
boundary local theorem, convergence of all secondary moments,
unconditional independence of the two mixed normals, or process-level
coupling is claimed. This manuscript has not received independent
researcher review.
