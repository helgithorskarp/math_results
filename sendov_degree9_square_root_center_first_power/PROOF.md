# A square-root complex-center tube for degree-nine first power

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.
Complete ordinary analytic author proof; independent review is pending.
Attributions, source provenance and the earlier illustrative error are
in [LITERATURE.md](LITERATURE.md). The arithmetic checker supplies exact
identities and controls, not a formal proof of the analytic bridges.

## 1. Polynomial statement

Let p be a degree-nine polynomial whose zeros lie in the closed unit
disk, with critical multiset {H^6,L1,L2}, allowing coincidence. Mark
a zero a, put rho=|a|, and count every algebraic multiplicity. A zero
reciprocal denominator contributes infinity. When a is nonzero,
rotate the coordinates so that a=rho is real positive. Assume
|a-L1|=|a-L2|, and define

\[
 v=\frac{|a-L_1|}{a-L_1},\qquad
 w=\frac{|a-L_2|}{a-L_2},\qquad v+w\ne0,
 \qquad q=\frac{v+w}{|v+w|}.
\]

If

\[
 \boxed{|q-1|^2\le\frac{1-\rho}{40000^2}},                 \tag{1}
\]

then

\[
 S_1(a)=6|a-H|^{-1}+|a-L_1|^{-1}+|a-L_2|^{-1}\ge8.
\]

The inequality is strict for rho<1. Equality is exactly
p(z)=C(z^9-a^9), C nonzero and |a|=1. No assumption is made on the
heavy direction or the distance order. At a=0 the classical strict
endpoint holds without this sector assumption. The constants are
sufficient and are not asserted sharp. Large centers, unequal light
radii and unrestricted degree-nine first power remain outside this
result.

For 0<=epsilon<=1, epsilon/80000<=sqrt(epsilon)/40000. Thus (1)
contains the preceding linear tube. The earlier constant-width tube
under a heavy cone remains complementary; it is not wholly contained
in (1). The separate full reflected theorem remains a credited result,
including reflected antipodal or negative-sum pairs for which this
short-center condition is unavailable.

## 2. Normalized analytic hypotheses and imported origin surplus

Take 0<=b<=1, positive r,s with

\[
 3r+s=4,\quad r,s\ge(1+b)^{-1},\quad U=x+iY,\ |U|=r,
 \quad |b-1/U|\le1.
\]

Let c in [0,1], and let q=z+iW be a unit complex number with z>=0.
Assume the actual mean

\[
 (3x+scz)/4\ge b.                                      \tag{2}
\]

Write epsilon=1-b and h=|q-1|. In this section z denotes Re(q),
not the polynomial variable. Set

\[
 M=7/6,\quad
 A=9\int_0^1(1-b\tau U)^6\,d\tau,\quad
 B=9b\int_0^1\tau(1-b\tau U)^6\,d\tau,\quad
 C_0=9b^2\int_0^1\tau^2(1-b\tau U)^6\,d\tau,
\]
\[
 I(q,c)=A-2scqB+s^2q^2C_0,\quad I_0=I(1,c),\quad R=r^{12}s^4.
\]

The credited reflected-origin lemma (graph8291, Sections2--3) gives

\[
 |I_0|^2\ge R+\epsilon.                                \tag{3}
\]

Indeed reflection increases the real mean because c>=0 and z<=1,
so its hypotheses hold. That lemma permits every heavy direction
and both radial orders. Its equality statement at b=1 is precisely
b=r=s=x=c=1. The present proof imports (3) and its equality statement;
it does not rederive the old complete sign tensor.

The radius floors imply r<=7/6 and s<=5/2. The individual heavy disk
gives |1-bU|<=r. By convexity, for 0<=tau<=1 and also after replacing
Y by any number between zero and Y,

\[
 |1-b\tau U|\le M.                                    \tag{4}
\]

The reflected mean budget is

\[
 3(r-x)+s(1-c)\le4\epsilon.
\]

Both summands are nonnegative. Consequently

\[
 Y^2=(r-x)(r+x)\le2r(r-x)\le\frac{28}{9}\epsilon
 <4\epsilon\quad(\epsilon>0),                         \tag{5}
\]

and |Y|<=2sqrt(epsilon) also at epsilon=0. Keeping this factor is
the gain over a direct norm-Lipschitz argument.

## 3. Antisymmetric moment-product estimates

Put f_tau=1-b tau U. For any complex Z, telescoping the difference
Z^6-conj(Z)^6 proves |Im(Z^6)|<=6|Im Z||Z|^5. Thus (4) yields

\[
 |\Im(f_\tau^6\overline{f_\sigma^6})|
 \le6b|Y||\tau-\sigma|M^{10}.                          \tag{6}
\]

For M_l=9b^l integral tau^l f_tau^6, antisymmetrizing in tau and
sigma gives

\[
 \Im(M_l\overline{M_m})=
 \frac{81b^{l+m}}2\int_{[0,1]^2}
 (\tau^l\sigma^m-\tau^m\sigma^l)
 \Im(f_\tau^6\overline{f_\sigma^6})\,d\tau\,d\sigma.
\]

The three required nonnegative weight integrals are

\[
 \int(\tau-\sigma)^2=1/6,\qquad
 \int(\tau-\sigma)^2(\tau+\sigma)=1/6,\qquad
 \int\tau\sigma(\tau-\sigma)^2=1/36.
\]

For (l,m)=(0,1),(0,2),(1,2), respectively, (6) therefore gives

\[
 |\Im(A\overline B)|\le\frac{81}{2}b^2|Y|M^{10},\quad
 |\Im(A\overline{C_0})|\le\frac{81}{2}b^3|Y|M^{10},\quad
 |\Im(B\overline{C_0})|\le\frac{27}{4}b^4|Y|M^{10}.       \tag{7}
\]

These are uniform analytic bounds, including Y=0. No sign of a
moment's imaginary part is assumed. The checker integrates the full
weight polynomials exactly and checks the full telescoping identity.

## 4. Exact phase decomposition and norm loss

Since h^2=2(1-z), write Delta=I(q,c)-I0 exactly as

\[
 \Delta=E_0+iWD_0,\quad
 E_0=h^2[scB-s^2(1+z)C_0],\quad
 D_0=-2scB+2s^2zC_0.                                  \tag{8}
\]

Here E0 is a complex moment combination, not an error remainder.
Elementary multiplication gives the complete skew identity

\[
 \Im(I_0\overline{D_0})=
 -2sc\Im(A\overline B)+2s^2z\Im(A\overline{C_0})
 +2s^3c(1-2z)\Im(B\overline{C_0}).                    \tag{9}
\]

Because 0<=z,c,b<=1, s<=5/2, and |1-2z|<=1, (7) implies

\[
 |\Im(I_0\overline{D_0})|
 \le(81s+81s^2+\tfrac{27}{2}s^3)|Y|M^{10}
 \le\frac{14715}{16}|Y|M^{10}.                        \tag{10}
\]

Also |A|<=9M^6, |B|<=(9/2)bM^6 and |C0|<=3b^2M^6, so

\[
 |I_0|\le\frac{201}{4}M^6,\qquad
 |E_0|\le\frac{195}{4}M^6h^2.                         \tag{11}
\]

Use |W|<=h, (5), and discard the nonnegative |Delta|^2 in the
exact norm expansion. Equations(8)--(11) yield

\[
 |I(q,c)|^2\ge|I_0|^2
 -\frac{14715}{4}M^{10}\sqrt\epsilon\,h
 -\frac{39195}{8}M^{12}h^2.
\]

The exact rational comparisons are

\[
 \frac{14715}{4}(7/6)^{10}
 =\frac{153949010705}{8957952}<18000,
\quad
 \frac{39195}{8}(7/6)^{12}
 =\frac{60278805760355}{1934917632}<32000.
\]

Together with (3) this proves the reusable perturbation inequality

\[
 \boxed{|I(q,c)|^2\ge R+\epsilon
          -18000\sqrt\epsilon\,h-32000h^2}.             \tag{12}
\]

If h^2<=epsilon/40000^2, the norm loss is at most

\[
 (18000/40000+32000/40000^2)\epsilon
 =\frac{22501}{50000}\epsilon<\epsilon/2.
\]

Hence

\[
 \boxed{|I(q,c)|^2\ge R+\epsilon/2}.                   \tag{13}
\]

The same proof handles epsilon=0 directly: h=0 and (3) applies.
Weighted AM--GM gives R<=1, so the normalized norm is at least
1+epsilon/(2R)>=1+epsilon/2.

## 5. Passage to an actual polynomial and endpoints

Suppose a=rho>0 is not a critical collision and S1<=8. Put m=S1/8,
0<m<=1, and scale the actual polynomial by p_m(z)=m^9 p(z/m).
Its zeros and critical points are still in the unit disk. Write
b=m rho, and let its reciprocals from b be U six times, sv and sw.
Then |U|=r, 3r+s=4, and Gauss--Lucas gives r,s>=1/(1+b) and
the heavy disk used in(4). The unit phases and short center do not
change under the positive scaling. With c=|v+w|/2 in (0,1],
the unit-light sum and product are v+w=2cq and vw=q^2. Thus the
origin integral of this actual scaled polynomial is I(q,c).

For 0<b<1, the full arbitrary-phase complex6+1+1 polar necessary-mean
lemma (graph8148, equations3--4 and Section5), independently confirmed
in8184, gives the actual mean (2), in fact strictly. This is the only
extra campaign premise in the actual-polynomial passage. No radial
heavy theorem or 6+2 origin theorem is used. Since b<=rho, (1) implies
h^2<=(1-b)/40000^2, and it implies Re(q)>0. Thus (13) applies.

The exact classical origin communication identity is

\[
 \frac{|I|^2}{r^{12}s^4}
 =m^{16}\frac{|p(0)|^2}{\rho^2}
 =m^{16}\prod_{j=1}^8|z_j|^2\le1,
\]

where z_j are the eight original unmarked roots of monic p. This
contradicts (13) when b<1. In particular S1>8 at every rho<1 in
the stated sector. Notice that the scaling exponent is 16.

If b=1, then m=rho=1 and q=1. At the marked simple boundary root,
p''(1)/p'(1)=2 sum_j (1-z_j)^(-1) has real part at least 8,
since Re(1-z_j)^(-1)>=1/2 for each unmarked disk root. This supplies
(2) at the endpoint. The imported equality statement in(3), together
with the origin norm upper bound, forces r=s=x=c=1, so all critical
points vanish. Integration and p(1)=0 give the binomial equality.

At a=0, the marked derivative product gives
9 product_j |zeta_j|=product_j |z_j|<=1. AM--GM on the eight
inverse critical distances yields S1(0)>=8*9^(1/8)>8 unless a
critical collision already makes the sum infinite. This classical
endpoint needs no sector assumption.

## 6. Actual enlargement example and correction of an older example

Let a=1/2, H=a+i/100, k=1/160000,
alpha=(1-k^2+2ik)/(1+k^2), and set

\[
 v=\alpha(3+4i)/5,\quad w=\alpha(3-4i)/5,
 \quad L_1=a-\overline v/50,\quad L_2=a-\overline w/50.
\]

Define the monic polynomial by p(a)=0 and
p'=9(z-H)^6(z-L1)(z-L2). Its unit light reciprocals are exactly
v,w, their sum is (6/5)alpha, and their short center is alpha.
In particular the center is actually defined. The light points are
not mutually conjugate. The heavy unit reciprocal is i, so it
fails the preceding heavy cone's 11/20 floor. Further,

\[
 |\alpha-1|^2=\frac4{25600000001},\quad
 \frac1{160000^2}<|\alpha-1|^2<\frac1{3200000000}.
\]

The left bound excludes the preceding linear center tube at a=1/2;
the right is exactly the new squared width in(1). The checker builds
the entire polynomial, marked derivative and both unit reciprocals.
On |z-a|=1/4 it bounds every lower coefficient by the exact positive
coefficient majorant obtained from six critical offsets of magnitude
1/100 and two of magnitude1/50. Its integrated lower tail is strictly
less than(1/4)^9. Rouche therefore puts all nine roots in |z-a|<1/4,
strictly inside the unit disk. No numerical root approximation enters.

The earlier source f93b9864c4519deb005dffa2e6a4c40982af1b20, graph8291,
Section6, instead rotated an antipodal light pair and erroneously
called alpha its short center. Its unit sum was zero, so that
nonreflected example did not satisfy that theorem's center hypothesis.
The reflected-origin lemma, sign certificate and polynomial sector
theorems were unaffected. The older source now uses the non-antipodal
pair above with k=0 and k=1/1000000, verifies its actual nonzero center
from the original critical points, and regenerates the compact example
records. The corrected k=1/1000000 example does belong to the older
linear tube. This is an explicit correction of an illustration, not
a claim that its old antipodal pair ever had a short center.

## 7. Evidence and scope

The standalone exact checker verifies all coefficients of(8)--(9),
the sixth-power telescoping identity, the three antisymmetric weight
integrals and all rational comparisons. Gaussian controls check the
moment product bounds and squared tube surplus at exact parameter
points. The actual example includes full polynomial/derivative
construction and rigorous Rouche bounds, and invalid zero-sum or wrong
center controls reject. Every compact expected record is rebuilt in
normal and optimized modes. None of these finite controls substitutes
for the written universal analytic argument.

The credited reflected-origin lemma remains independently unreviewed
at this publication; its complete pinned author replay and source
continuity are recorded separately. The credited polar premise has
independent confirmation8184. This new analytic argument is itself
unformalized and independently unreviewed. No unrestricted first-power
solution, optimized constant or historical priority is asserted.
