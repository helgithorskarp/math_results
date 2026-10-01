# First power for reflected light points and a complex center tube

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.
This complete ordinary author argument uses fresh exact rational
coefficient evidence. It is unformalized; independent review is pending.
The one imported campaign premise and the classical methods are credited
in [LITERATURE.md](LITERATURE.md). Unrestricted degree-nine first power
and unrestricted complex critical6+1+1 remain open here.

## 1. Polynomial statements

Let p have degree nine, with all zeros in the closed unit disk and
critical multiset \(\{H^6,L_1,L_2\}\), allowing coincidence. Let a be
a marked zero and write \(\rho=|a|\). Each critical point is counted
with its displayed multiplicity; a collision contributes infinity.

**Reflected-light theorem.** If a is nonzero, rotate the coordinates
so that a is positive real. Suppose the two light points are mutual
conjugates, \(L_2=\overline{L_1}\). Then

\[
 S_1(a)=6|a-H|^{-1}+|a-L_1|^{-1}+|a-L_2|^{-1}\ge8.       \tag{1}
\]

The heavy point may have any complex direction and either distance
order relative to the lights. The inequality is strict for \(\rho<1\).
Equality in this sector is precisely
\(p(z)=C(z^9-a^9)\), \(C\ne0\), \(|a|=1\).

**Complex center-tube theorem.** Instead suppose the light distances
are equal. In the same rotated coordinates, put

\[
 v=\frac{|a-L_1|}{a-L_1},\quad
 w=\frac{|a-L_2|}{a-L_2},\quad
 q=\frac{v+w}{|v+w|}.
\]

If \(v+w\ne0\) and

\[
 \boxed{|q-1|\le\frac{1-\rho}{80000}},                    \tag{2}
\]

then (1), its interior strictness and its binomial equality statement
hold. There is no heavy-direction or distance-order restriction.
The constant is sufficient, not asserted sharp. The reflected theorem
also covers reflected pairs with zero or negative real reciprocal sum,
which need not meet this center definition.

At a=0, the classical strict inequality holds without either sector
assumption. The center tube shrinks at the unit boundary; the prior
constant-width cone sector remains complementary there.

## 2. A reflected origin inequality with a quantitative surplus

Take \(0\le b\le1\) and positive r,s with

\[
 3r+s=4,\qquad r,s\ge(1+b)^{-1}.
\]

Let \(U=x+iY\), \(|U|=r\), and let \(-1\le c\le1\) satisfy
\(\mu=(3x+sc)/4\ge b\). Define

\[
 I=9\int_0^1(1-b\tau U)^6
                 (1-2bsc\tau+b^2s^2\tau^2)\,d\tau,
 \qquad R=r^{12}s^4>0.
\]

The new analytic lemma is

\[
 \boxed{|I|^2\ge R+(1-b)},\qquad
 \frac{|I|^2}{R}\ge2-b.                                  \tag{3}
\]

Equality in \(|I|^2/R\ge1\) occurs exactly at
\(b=r=s=x=c=1\). No individual critical disk or heavy phase cone is
assumed in (3). The second inequality uses weighted AM--GM:
\(r^6s^2\le[(6r+2s)/8]^8=1\), hence R<=1.

Here is a complete parameterization sufficient for (3). Put
\(\varepsilon=1-b\). The radius floors give

\[
 \frac1{1+b}\le r\le1+\frac{b}{3(1+b)}.
\]

Use the two closed charts, \(0\le y\le1\),

\[
 r_+(b,y)=1+\frac{by}{3(1+b)},\qquad
 r_-(b,y)=1-\frac{by}{1+b}.                              \tag{4}
\]

For b<1, the mean condition is exactly the loss budget

\[
 3(r-x)+s(1-c)\le4\varepsilon.
\]

Both terms are nonnegative. Thus for some v,w in [0,1],

\[
 x=r-\tfrac43\varepsilon v,\qquad
 sc=s-4\varepsilon(1-v)w.                               \tag{5}
\]

If v=1 the remaining budget forces c=1, and any w is usable.
Conversely, (5) has mean
\(1-\varepsilon[v+(1-v)w]\ge b\). At b=1, saturation forces
x=r,c=1 and either chart represents every radius; (5) has those same
values regardless of v,w. This handles all degenerate faces.

The whole larger cube in (4)--(5) retains a real Y because
\(r-x\le4\varepsilon/3\le2r\), using
\(r\ge(1+b)^{-1}\) and \(4(1-b^2)/3\le2\). Some cube values
of c are below minus one. The next polynomial certificate covers
them too; the interpretation as two unit light phases is used only
at actual \(-1\le c\le1\). No invalid phase is used to exclude a
physical point.

## 3. The complete rational coefficient certificate

Write t=sc and \(Y^2=r^2-x^2\). Over Q[b,r,x,t], let

\[
 A=9\int_0^1(1-b\tau U)^6d\tau,\quad
 B=9b\int_0^1\tau(1-b\tau U)^6d\tau,\quad
 C_0=9b^2\int_0^1\tau^2(1-b\tau U)^6d\tau.
\]

Then \(I=A-2tB+s^2C_0\). [kernel.py](kernel.py) constructs
each moment as a real plus iY times a rational polynomial. Binomial
integration agrees coefficient by coefficient with the independent
endpoint sums, for h=1-bU:

\[
 A=\tfrac97\sum_{j=0}^6h^j,\quad
 B=\tfrac{9b}{56}\sum_{j=0}^6(j+1)h^j,\quad
 C_0=\tfrac{b^2}{56}\sum_{j=0}^6(j+1)(j+2)h^j.
\]

The full eight-factor integration also agrees. The squared norm is
checked by a separate Chebyshev recurrence
\(\Re U^{j+1}=2x\Re U^j-r^2\Re U^{j-1}\) applied to every
coefficient cross-product. This gives the same complete 292-term
polynomial \(P=|I|^2-R\) as the real/imaginary squared norm.

Substitute (5), then each (4), with D=1+b. Exact denominator
clearing gives the polynomials

\[
 Q_\pm(b,y,v,w)=D^{16}\{P(r_\pm,x,t)-(1-b)\}.             \tag{6}
\]

The intermediate phase and loss polynomials have 929 and 1453 terms;
each mapped P has 4570. Homogeneous substitution and Horner clearing
agree coefficient by coefficient, and the clearing exponent is 16.
Each complete tensor degree in (b,y,v,w) is **(32,16,8,2)**.

[verify.py](verify.py) regenerates all **15147 coefficients per chart**,
**30294 total**. Every coefficient is nonnegative. Each tensor has
**15093 positive entries**, with exact minimum positive coefficient
**79**, and exactly these **54** zero indices:

\[
 \{(32,j,k,\ell):j\in\{0,1\},\ 0\le k\le8,\ 0\le\ell\le2\}.
\]

Both full tensors are inverted exactly to (6). Bernstein basis
functions are nonnegative and sum to one, so these finite signs prove
(3) on the entire two-chart domain, with all closed faces retained.
The coefficient hashes, complete zero-support hashes and polynomial
hashes are in [expected.json](expected.json); no bulky tensor corpus
is needed.

For b<1, (3) gives strict norm greater than R directly. At b=1,
if y>0, an active y-index16 coefficient is positive for every v,w,
since all zero indices have y-index0 or1. Thus Q is positive. If y=0,
r=s=x=c=1, and direct integration gives I=1. This proves the entire
stated equality set, without sampling its candidates.

## 4. A uniform perturbation of the light center

Retain the radius and real-mean hypotheses, now take two unit phases
with sum 2cq, product q^2, \(0\le c\le1\), \(|q|=1\), and
actual mean \((3x+sc\Re q)/4\ge b\). Assume the one heavy disk
\(|b-1/U|\le1\). The integral is

\[
 I(q,c)=A-2scqB+s^2q^2C_0.
\]

Reflection increases the real mean because c>=0 and Re(q)<=1.
Consequently (3) applies to I(1,c). Put h=|q-1| and
\(M=(7/6)^6\). The heavy disk implies
\(|1-bU|\le r\), and convexity along the segment gives
\(|1-b\tau U|\le\max(1,r)\le7/6\). Hence

\[
 |A|\le9M,\quad |B|\le\tfrac92bM,\quad |C_0|\le3b^2M.
\]

The radius floor also gives s<=5/2. Since |q^2-1|<=2h,

\[
 |I(1,c)|\le\tfrac{201}4M,\qquad
 |I(q,c)-I(1,c)|\le60Mh.
\]

Therefore

\[
 |I(q,c)|^2\ge |I(1,c)|^2-6030M^2h,
 \qquad6030(7/6)^{12}<40000.
\]

If \(h\le(1-b)/80000\), we obtain the rigorous surplus

\[
 \boxed{|I(q,c)|^2\ge R+\tfrac12(1-b)}.                   \tag{7}
\]

The rational constant comparison and exact shifted-center controls
are checked separately. Neither this bound nor (3) asserts that
opening or rotating lights is monotone at every admissible point.

## 5. Passage to actual disk-root polynomials

Rotate a to real a>0 and make p monic. If a is a multiple root, the
critical collision is immediate. Otherwise suppose S1(a)<=8. Put

\[
 U_*=(a-H)^{-1},\quad V_*=(a-L_1)^{-1},\quad
 W_*=(a-L_2)^{-1},\quad m=S_1(a)/8\in(0,1].
\]

Use the actual scaled polynomial \(p_m(z)=m^9p(z/m)\), with marked
zero b=ma and reciprocals U=U_*/m, V=V_*/m, W=W_*/m.
Its roots remain in the unit disk. Equal light distances give
\(|V|=|W|=s\), \(|U|=r\), and 6r+2s=8. Gauss--Lucas gives
the radius floors and all critical disks of Sections2 and4.

For 0<b<1, the **one imported campaign premise** is the full complex
critical6+1+1 polar lemma8148, specifically its implication (3)--(4)
in the [credited proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_radial_sixfold_critical_first_power/PROOF.md).
It applies to the actual p_m, with arbitrary heavy and light phases.
Classical polar communication has modulus at least one, so this lemma
forces the actual mean

\[
 \mu=(6\Re U+\Re V+\Re W)/8>b.                           \tag{8}
\]

Only the weak consequence mu>=b is needed here. Its independent
audit8184 confirms that precise premise; that verdict does not audit
the new coefficient certificate or theorem.

For b=1, m=a=1. Write \(p(z)=(z-1)q_0(z)\) and let z_j be the
other eight roots. The classical marked-root derivative identity gives

\[
 \sum_{p'(\zeta)=0}\frac1{1-\zeta}
 =\frac{p''(1)}{p'(1)}
 =2\sum_{j=1}^8\frac1{1-z_j}.
\]

Each real part on the right sum is at least1/2 for a disk root.
Thus mu>=1=b. Collisions were already separated. No interior polar
formula is divided by 1-b at this endpoint.

If the lights reflect, V and W are conjugate. Put c=Re(V)/s in
[-1,1]. Their product s^2 and sum2sc make the origin integral exactly
I in Section2, even when c is nonpositive. Apply (3).

For the center tube, scaling preserves both unit phases and q. The
unit-circle pair identity gives V+W=2scq, VW=s^2q^2, with
\(c=|v+w|/2\in(0,1]\). The assumed chord obeys
\(|q-1|\le(1-a)/80000\le(1-b)/80000\); use (7).

Finally, integrate the actual p_m' from b to zero. For either integral,

\[
 I=-\frac{p_m(0)}b U^6VW,\qquad
 \frac{|I|^2}{r^{12}s^4}
 =m^{16}\frac{|p(0)|^2}{a^2}
 =m^{16}\prod_{j=1}^8|z_j|^2\le1.                       \tag{9}
\]

If a<1, b<1, so (3) or (7) contradicts (9). At a=1, m<1 would
give the same contradiction. With m=b=1, the reflected equality
classification forces r=s=1,U=1,c=1. The tube has q=1 at this
endpoint, so it has the same classification. All eight critical points
are zero. Integrating p'=9z^8 with p(1)=0 gives z^9-1. Undo rotation
and the leading scalar to obtain the stated binomial equality family.
It indeed attains S1=8.

At a=0, if there is no critical collision, write p(z)=zq_0(z).
Then \(|p'(0)|=\prod|z_j|\le1\) and
\(|p'(0)|=9\prod|\zeta_j|\). Thus AM--GM gives
\(S_1(0)\ge8\,9^{1/8}>8\). This is the classical endpoint.

## 6. Examples beyond the preceding heavy cone

Set a=1/2, H=a+i/100, L1=a-(3-4i)/250, L2=a-(3+4i)/250 and define the monic
polynomial by p(a)=0 and p'=9(z-H)^6(z-L1)(z-L2). The heavy unit
reciprocal is i, whose real part0 fails the preceding cone's required
11/20. These light points reflect and the heavy distance is smaller.

In centered coordinates z=a+w, write P(w)=p(a+w). On |w|=1/4,
the sum of the lower coefficient bounds is exactly

\[
 \sum_{j<9}(|\Re P_j|+|\Im P_j|)(1/4)^j
 =\frac{1856581828293}{1120000000000000000}
 <(1/4)^9=1/262144.
\]

Rouche puts all nine roots in |z-a|<1/4, hence strictly in the unit
disk. The marked root is simple, the derivative has exactly the stated
critical multiset and the monic polynomial is nonreal.

For a nonreflected example, rotate both light reciprocals by
\(\alpha=(1-k^2+2ik)/(1+k^2)\), k=1/1000000, keeping the heavy
point and a fixed. Thus
\(v=\alpha(3+4i)/5\), \(w=\alpha(3-4i)/5\), and
\(L_1=a-\overline v/50\), \(L_2=a-\overline w/50\).
The equal light distances persist. Their actual unit reciprocal sum
is \((6/5)\alpha\ne0\), so their short center is alpha and
\(|\alpha-1|^2=4/1000000000001\le(1/160000)^2\).
The two lights are not mutual conjugates. The regenerated exact
centered coefficient bound still lies below1/262144, so all roots
remain in the disk. This example also fails the preceding heavy cone.
The compact fixture records both polynomial hashes and exact bounds.
These examples illustrate the enlarged hypotheses; no optimized
first-power excess is claimed for them.

**Illustrative correction, 2026-10-01.** The original Section6 rotated
an antipodal light pair and called alpha its short center. That pair's
unit reciprocal sum was zero; its nonreflected example did not meet
the short-center hypothesis. The preceding reflected-origin lemma,
sign tensors and sector theorems were unaffected. The examples and
their full compact records above now use the non-antipodal pair and
verify the center from the original critical points. An explicit
antipodal invalid-center control is checked. The larger square-root
tube and this correction are documented in the
[subsequent proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_square_root_center_first_power/PROOF.md).

## 7. Evidence and remaining frontier

The standalone checker proves the complete coefficient identities and
30294 signs, including the entire zero supports and both inverse basis
transforms. It also checks270 direct quadratic-field cube controls,
including nonphysical enlarged faces;532 original Gaussian controls,
including nonreal, opened and negative-heavy-real cases; the center
Lipschitz constants and shifted-center controls; two actual nonreal
polynomials with exact Rouche bounds; six full scaling/origin/polar
communication identities; and the marked derivative identity.
Thirteen altered compact proof fixtures reject through explicit
exceptions, including with Python optimization enabled.

The ordinary analytic reductions, classical complex analysis and the
credited polar lemma remain outside a formal proof kernel. This proof
does not rely on the previously unreviewed full6+2 origin lemma or on
positive opening derivatives. The new real-mean loss map supplies the
origin surplus directly. General equal-radius centers at large angle,
unequal light radii and unrestricted degree-nine first power remain
unresolved. The exact two-phase Schur reconstruction is exploratory
context only and is not an input to this certificate.
