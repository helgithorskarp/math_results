# An explicit equal-light annulus for degree-nine first power

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.
This is an exact computer-assisted ordinary author proof, with the
mathematical reductions written below. It is unformalized and independent
review of this new result is pending. Its imported campaign lemmas and
their scoped reviews are credited in [LITERATURE.md](LITERATURE.md).

## 1. Actual-polynomial statement

Let $p$ have degree nine and all its roots in the closed unit disk.
Suppose its critical multiset is ${H^6,L_1,L_2}$, allowing coincidences
and counting multiplicities. Let $a$ be a marked root and suppose

$$
 |a-L_1|=|a-L_2|,\qquad
 \rho=|a|\ge\frac{43750}{46643}.
$$

Then

$$
 S_1(a)=\frac6{|a-H|}+\frac1{|a-L_1|}+\frac1{|a-L_2|}\ge8.
 \tag{1}
$$

It is strict when $\rho<1$. Equality holds exactly when

$$
 |a|=1,\qquad p(z)=C(z^9-a^9),\qquad C\ne0.
$$

A critical collision contributes infinity. There is no heavy phase,
radial order, light reflection or nonzero-center hypothesis in (1).
The annulus radius is conservative; no optimality is claimed.
The unrestricted degree-nine first-power inequality remains outside
this theorem.

[STABILITY.md](STABILITY.md) derives the stronger uniform origin margin
$|I|^2-R\ge10^{-32}(1-b)^2$ from these same complete coefficient supports.
It extends the actual annulus theorem to unequal light distances whose
reciprocal magnitudes differ by at most $10^{-40}(1-\rho)^2$.
That extension explicitly uses the original quantitative1/128 component
of the credited full complex polar lemma8148.

Earlier campaign results give a qualitative annulus for every degree-nine
polynomial and an explicit universal annulus starting at $1-10^{-18}$.
The new part is this substantially wider explicit annulus within the
specified critical multiplicity and equal-distance class, together with
the uniform origin certificate below. It does not replace those results'
more general hypotheses or their quantitative boundary slopes.

## 2. The uniform normalized origin statement

Take

$$
 \frac78\le b\le1,\quad r,s>0,\quad 3r+s=4,\quad
 r,s\ge\frac1{1+b},\quad U=x+iY,\quad |U|=r.
 \tag{2}
$$

Let $v,w$ be arbitrary unit complex numbers and assume the **actual**
real reciprocal mean condition

$$
 \mu=\frac{6x+s\operatorname{Re}(v+w)}8\ge b.
 \tag{3}
$$

Define the integral and positive denominator

$$
 I=9\int_0^1(1-b\tau U)^6(1-b\tau sv)(1-b\tau sw)\,d\tau,
 \qquad R=r^{12}s^4.
 \tag{4}
$$

The certified conclusion is

$$
 |I|^2\ge R,
 \tag{5}
$$

strict when $b<1$. At $b=1$, equality is possible exactly for

$$
 U=sv=sw=1.
 \tag{6}
$$

No individual critical disk is required for (5). The radius floors and
actual mean in (2)--(3) are essential to the proved domain.

For an antipodal pair $v+w=0$, put $t=0$, without assigning it a
center. Otherwise put

$$
 q=\frac{v+w}{|v+w|},\qquad c=\frac{|v+w|}{2},\qquad
 t=sc\operatorname{Re}q.
$$

The budget and the floor for $s$ give

$$
 t\ge4b-3r=s-4(1-b)
 \ge\frac{4b^2-3}{1+b}\ge\frac1{32}>0.
 \tag{7}
$$

Thus an antipodal pair cannot satisfy these hypotheses, and every pair
in this proof has $\operatorname{Re}q>0$. Also $t\le s$.
Write

$$
 q=\frac{1+ik}{\sqrt{1+k^2}},\quad k\in\mathbb R,\quad
 \kappa=k^2,\quad K=\frac{s^2}{t^2}-1\ge0.
$$

Since $c=t\sqrt{1+\kappa}/s$, the condition $c\le1$ is precisely

$$
 0\le\kappa\le K.
 \tag{8}
$$

For two unit phases with positive sum, $v+w=2cq$ and $vw=q^2$.
This includes coincident lights $c=1$.

## 3. Exact center identities and a Gram reduction

Use the complex moments

$$
 A=9\int_0^1(1-b\tau U)^6\,d\tau,\quad
 B=9b\int_0^1\tau(1-b\tau U)^6\,d\tau,\quad
 C=9b^2\int_0^1\tau^2(1-b\tau U)^6\,d\tau.
$$

Then $I=A-2scqB+s^2q^2C$, and exactly

$$
 (1+k^2)I=J_0+ikJ_1+k^2J_2+ik^3J_3,
 \tag{9}
$$

where

$$
 J_0=A-2tB+s^2C,\quad J_1=-2tB+2s^2C,\quad
 J_2=A-2tB-s^2C,\quad J_3=-2tB.
$$

Write $J_j=a_j+iYb_j$, with rational polynomials in $b,r,x,t$,
and reduce $Y^2=r^2-x^2$. For such pairs put

$$
 \operatorname{dot}(P,Q)=a_Pa_Q+Y^2b_Pb_Q,\qquad
 \operatorname{cr}(P,Q)=2(b_Pa_Q-a_Pb_Q).
$$

The complete norm identity is

$$
 |(1+k^2)I|^2-R(1+k^2)^2=E(\kappa)+YkO(\kappa),
 \tag{10}
$$

where $E=\sum_{j=0}^3E_j\kappa^j$, $O=\sum_{j=0}^2O_j\kappa^j$, and

$$
 \begin{aligned}
 E_0&=|J_0|^2-R,&
 E_1&=2\operatorname{dot}(J_0,J_2)+|J_1|^2-2R,\\
 E_2&=|J_2|^2+2\operatorname{dot}(J_1,J_3)-R,&
 E_3&=|J_3|^2,\\
 O_0&=\operatorname{cr}(J_0,J_1),&
 O_1&=\operatorname{cr}(J_0,J_3)+\operatorname{cr}(J_2,J_1),\\
 O_2&=\operatorname{cr}(J_2,J_3).
 \end{aligned}
$$

Define the degree-six Gram polynomial

$$
 G(\kappa)=E(\kappa)^2-(r^2-x^2)\kappa O(\kappa)^2.
 \tag{11}
$$

For real $Y,k$, $E\ge0$ and $G\ge0$ imply $E\ge|YkO|$.
When both are strict, (10) is strictly positive for either sign of $k$.

[kernel.py](kernel.py) constructs all moment, numerator, even/skew and
Gram polynomials directly. It compares **entire coefficient dictionaries**
for the binomial versus endpoint moment formulas, the full eight-factor
numerator and the separate real/imaginary norm convolution. It also
checks $G_0=E_0^2$ and $G_6=E_3^2$. The seven Gram coefficient term
counts are $3381,3381,3299,3373,3381,1024,91$, totaling (17930).
These identities alone do not establish positivity.

## 4. Angular Bernstein controls

Put $D=s^2-t^2\ge0$. If $D=0$, (8) gives $k=0,c=q=1$, and the
credited reflected-origin lemma applies directly. Suppose $D>0$ and
put $h=\kappa/K\in[0,1]$. Then

$$
 t^6E(Kh)=\sum_{j=0}^3E_jt^{6-2j}D^jh^j,
 \qquad
 t^{12}G(Kh)=\sum_{j=0}^6G_jt^{12-2j}D^jh^j.
 \tag{12}
$$

For degree $n=3$ or (6), let $C_j=E_j$ or $G_j$, respectively.
The $i$-th Bernstein coefficient of the corresponding cleared polynomial
is $t^{2n-2i}P_i$, where

$$
 P_i=\sum_{j=0}^i\frac{\binom ij}{\binom nj}
              C_jt^{2(i-j)}D^j.
 \tag{13}
$$

The zeroth coefficient uses an existing lemma, rather than a new tensor.
In $J_0=A-2tB+s^2C$, the reflected opening is $t/s\in(0,1]$ and
its real mean is exactly the same $(3x+t)/4\ge b$. The full-radius
reflected-origin surplus/equality result, graph8291, therefore gives

$$
 E_0\ge1-b,\qquad G_0=E_0^2.
 \tag{14}
$$

It has been independently confirmed in graph8344. Its stronger reviewer
surplus and wider center tube are not imported here.

For the remaining nine controls $E1,E2,E3,G1,\ldots,G6$, only the
actual common $t$-monomial is removed: $t^2$ from E3 and G5, and
$t^4$ from G6. No $b,r,x$ powers are removed. Equation (7) proves
the removed monomials and every other cleared denominator positive.
The source reconstructs the entire inverse angular basis identities for
all four even and seven Gram power coefficients, not sampled values.

## 5. Complete mean-loss cubes and certificate soundness

Put $\varepsilon=1-b$. The radius floors and $3r+s=4$ give

$$
 \frac1{1+b}\le r\le1+\frac{b}{3(1+b)}.
$$

Two closed charts cover this interval:

$$
 r=1+\frac{by}{3(1+b)}\quad\text{(nearer)},\qquad
 r=1-\frac{by}{1+b}\quad\text{(farther)},\qquad 0\le y\le1.
$$

Since $x\le r$ and $t\le s$, the actual mean condition is the
nonnegative loss budget

$$
 3(r-x)+(s-t)\le4\varepsilon.
$$

For $b<1$ choose

$$
 x=r-\frac43\varepsilon v,\qquad
 t=s-4\varepsilon(1-v)w,\qquad 0\le v,w\le1.
 \tag{15}
$$

Indeed, $v=3(r-x)/(4\varepsilon)\in[0,1]$; for $v<1$ the budget
gives $w=(s-t)/(4\varepsilon(1-v))\in[0,1]$. If $v=1$, the budget
forces $t=s$ and any $w$ works. At $b=1$, saturation gives $x=r$
and $t=s$ directly, without division by $\varepsilon$.

On both **whole** cubes, $r,s$ satisfy the floors, $t\ge1/32$,
$t\le s$, and $Y^2=r^2-x^2\ge0$. For the last assertion use
$(4/3)(1-b)\le2/(1+b)\le2r$. Finally put $b=(7+u)/8$, with
$u\in[0,1]$. Thus these cubes cover every allowed case of (2)--(3).

[certificate.py](certificate.py) composes each reduced $P_i$ with
these maps in integers. Homogeneous composition clears powers of
positive $3,8,1+b$; primitive normalization divides only by positive
integer gcds. Its returned positive scale $f$, radius power $d$ and
primitive polynomial $P$ satisfy

$$
 \frac{P(u,y,v,w)}f=(1+b)^d\,P_i^{\rm reduced}(b,r,x,t).
 \tag{16}
$$

The tensor-product Bernstein basis on the four-dimensional unit cube
is nonnegative and sums to one. For a power polynomial with separate
degrees $n_j$, its coefficient at multi-index $i$ is

$$
 \beta_i=\sum_{e\le i} a_e\prod_{j=1}^4
                \frac{\binom{i_j}{e_j}}{\binom{n_j}{e_j}}.
$$

The checker computes **every** coefficient with shared integer
denominators. It separately verifies the entire inverse identity,
using

$$
 a_e=\left(\prod_j\binom{n_j}{e_j}\right)
       \sum_{i\le e}(-1)^{\sum_j(e_j-i_j)}
             \left(\prod_j\binom{e_j}{i_j}\right)\beta_i.
$$

The tensor values alone are not trusted. Each full inverse equals
the complete regenerated mapped polynomial dictionary, including its
support. Missing cases, timeouts or negative coefficients cause failure.
Hashes in the mandatory compact fixture are additional regression
checks; they do not replace the identities or sign checks.

The full cover has eighteen tensors, nine per chart. Both charts have
the following dimensions and counts; their actual coefficients and
hashes differ.

|Control|Degree $(u,y,v,w)$|Entries per chart|Zeros per chart|
|---|---|---:|---:|
|E1|$36,18,9,3$|28120|80|
|E2|$38,20,10,4$|45045|110|
|E3|$36,20,8,2$|20979|54|
|G1|$68,34,17,5$|260820|648|
|G2|$72,36,18,6$|359233|798|
|G3|$74,38,19,7$|468000|960|
|G4|$76,40,20,8$|596673|1134|
|G5|$74,40,18,6$|408975|798|
|G6|$72,40,16,4$|254405|510|

Each chart checks (2442250) signs; the union checks **4884500**.
Every entry is nonnegative and every whole inverse identity holds.

## 6. Strictness and equality

Nonnegative controls in (12)--(13) give $E\ge0,G\ge0$ on the full
angular interval. If $b<1$ and $h<1$, the zeroth coefficient (14)
has positive Bernstein weight, so $E>0,G>0$.

At $h=1$, only the top angular controls remain. In both E3 tensors
**all zero entries have $u$-index36**, the endpoint degree. Hence
the entire $u$-index0 slice is strictly positive, and its positive
weight $(1-u)^{36}$ proves E3 positive at every $u<1$, including
all vertices of the other three coordinates. Both G6 tensors have
degree72 in $u$, and **every $u$-index0 coefficient is strictly
positive**. Its weight $(1-u)^{72}$, and the partition of unity in
the other axes, likewise prove the Gram endpoint positive at every
$u<1$. The minimum zero $u$-index is71. The source checks the full
support predicates needed here; zero counts alone would not suffice.

All prefactors from (12)--(13) are positive. Therefore $E>0,G>0$
also at $h=1,b<1$, proving $E>|YkO|$ and the strict form of (5)
for both signs of $k$. If $D=0$, strictness follows already from
(14). No previously published merged-light origin theorem is needed
for this endpoint argument.

At $b=1$, the budget gives $x=r,t=s$. Since $t=sc\operatorname{Re}q$
and $c\le1$, this forces $c=q=1$ and $k=0$. The reflected-origin
equality result in graph8291 gives (5), with equality exactly $r=s=1$.
Thus (6) is the complete equality set. There is no division by $K$
or $1-b$ at this boundary.

## 7. Passage to an actual polynomial

Rotate $a=\rho>0$ and normalize $p$ monic. A collision is already
settled, so suppose $S_1(a)\le8$ and put

$$
 m=\frac{S_1(a)}8\in(0,1],\qquad p_m(z)=m^9p(z/m),\qquad b=m\rho.
$$

The roots of $p_m$ remain in the unit disk, and its critical points
are $mH,mL_1,mL_2$. If $U_*,V_*,W_*$ are the original reciprocals,
the scaled reciprocals are $U=U_*/m,V=V_*/m,W=W_*/m$. Thus

$$
 |U|=r,\quad |V|=|W|=s,\quad 6r+2s=8.
$$

Gauss--Lucas gives the floors in (2).
The global strict bound in graph7152 gives

$$
 m>\frac{46643}{50000},\qquad
 b=m\rho>\frac{46643}{50000}\frac{43750}{46643}=\frac78.
$$

When $b<1$, the full arbitrary-phase complex $6+1+1$ polar
necessary-mean lemma, graph8148, gives the actual $\mu>b$.
Its weak consequence (3) suffices. This premise was independently
confirmed in graph8184; the improved reviewer constant is unused.

For completeness, at $b=1$ use the marked-root logarithmic derivative
directly. If $z_j$ are the other eight roots, then

$$
 \sum_{\rm critical}\frac1{1-\zeta_j}
       =2\sum_{j=1}^8\frac1{1-z_j},\qquad
 \operatorname{Re}\frac1{1-z_j}\ge\frac12.
$$

Thus again $\mu\ge1=b$. This is a classical boundary identity, not
an assumption that the interior polar lemma applies at its endpoint.

Finally integrate $p_m'$ from its marked root to zero. Its monic
factorization gives

$$
 p_m(0)=-b\left(\prod_{\rm critical}(b-\zeta_j^{(m)})\right) I.
$$

Taking squared moduli yields the exact communication identity

$$
 \frac{|I|^2}{R}=\frac{|p_m(0)|^2}{b^2}
    =m^{16}\frac{|p(0)|^2}{\rho^2}
    =m^{16}\prod_{j=1}^8|z_j|^2\le1.
 \tag{17}
$$

The exponent is **16**, not18. The source independently constructs a
monic polynomial by integrating its eight critical factors, fixes its
marked root and tests this scale exactly at two nonunit scales.

For $b<1$, strict (5) contradicts (17). At $b=1$, necessarily
$m=\rho=1$, and equality in (5) forces every scaled reciprocal to
be1, so every critical point is zero. Therefore $p(z)=z^9-a^9$ up
to its original nonzero scalar. Conversely that boundary binomial
attains eight. This proves (1), including strictness and equality.

## 8. Reproducibility and remaining trust boundary

[verify.py](verify.py) regenerates all eighteen tensors from the
integral formulas using only this directory and CPython's standard
library. It requires [expected.json](expected.json), rejects missing
or changed full fixtures, and uses explicit failures retained under
optimized Python. It also checks 324 direct Gaussian integral points
with both signs (648 norms), their Gram products, 42 integer-versus-
Fraction evaluation controls, all sixteen cube vertices and two
interior points for every case, and the full E1-nearer reference
comparison: 14956 monomials and 28120 tensor entries. Altering a
positive entry in that comparison is rejected by the inverse identity.
These controls test implementation bridges; they are not sampled
proofs of a universal sign inequality.

The large universal evidence is the complete eighteen-case sign cover
with full inverse identities. The largest case is not separately
compared entry by entry to a second large rational implementation;
its complete inverse and definition controls are checked instead.
Generic arithmetic lineage is credited; this regeneration is author
validation, not independent peer review.

The stability extension adds73 complete one-variable signs, a whole
power identity, rational constant gates and72 direct unequal-light
integral controls. Both final G6 checks audit every positive u-index
through70 needed for its quadratic margin. Selected arithmetic on
fixture metadata alone does not supply those full tensor checks.

Classical complex analysis, the three imported campaign lemmas,
cube coverage, Bernstein basis soundness, strict support interpretation
and actual-polynomial reduction remain ordinary mathematical proof
outside a formal kernel. No external solver, floating-point tolerance,
unverified imported tensor, private corpus or exploratory random search
is a premise. Source publication does not itself supply a reviewer
verdict. Commands, finite case partition and resource bounds are in
[README.md](README.md).
