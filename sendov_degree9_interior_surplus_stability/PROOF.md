# Interior first-power surplus stability around two boundary families

Author **six-sendov-2**, role **researcher**, 2026-09-30. All roots and
critical points are counted with multiplicity. This is an ordinary written
proof over the complex numbers. Exact checks establish finite identities
and constants; formalization and historical priority are not asserted.

## Statement and scope

Let a degree-nine polynomial have all roots in the closed unit disk and a
marked root \(a\). Put
\[
 F(a)=\sum_{j=1}^8|a-\zeta_j|^{-1},\qquad
 \eta=1-|a|,\qquad \sigma\ge0,\qquad h=\eta+\sigma.
\]
Assume
\[
 F(a)\le8+\sigma,\qquad 0<h\le10^{-13}.                 \tag{1}
\]
The sum is finite. No interior lower bound \(F(a)\ge8\) is assumed. Define
\[
 x_j=|a-\zeta_j|^{-1}-\tfrac12\ge0,\qquad L=e_2(x).
\]
Exactly one of two algebraic branches applies.

**Regular branch, \(L\ge1\).** A bijective labeling of the original roots,
anchored at \(z_0=a\), satisfies
\[
 \max_{0\le k\le8}|z_k-ae^{2\pi ik/9}|\le400000h,\qquad
 Q:=\sum_j|\zeta_j|^2\le1600000000h.                    \tag{2}
\]
More precisely, the same matching has error at most
\[
 81\eta+300D_a+2\cdot10^{24}h^{5/2},\qquad
 D_a:=\sum_{k=1}^8\frac{1-|z_k|^2}{|a-z_k|^2}
       \le1016\eta+\sigma.                             \tag{3}
\]
**Collapsed branch, \(L<1\).** The other eight roots and a bijective
labeling of the critical points satisfy
\[
 \max_{k\ge1}|z_k+a|\le15000\sqrt h,\qquad
 \max\{\max_{j\le7}|\zeta_j+a|,\ |\zeta_8-7a/9|\}
       \le1000\sqrt h.                                 \tag{4}
\]
This branch also necessarily satisfies
\[
 \boxed{\ \sigma\ge(4-22000000h)\eta.\ }                \tag{5}
\]
The leading coefficient \(4\) is sharp through interior examples as
\(h\to0\). If \(\eta>0\) and \(\sigma\le3\eta\), only the regular branch
can occur. In particular,
\[
 0<\eta\le\frac1{4\cdot10^{13}},\quad F(a)\le8+3\eta
 \ \Longrightarrow\
 Q\le6400000000\eta,\quad
 \max_k|z_k-ae^{2\pi ik/9}|\le1600000\eta.               \tag{6}
\]
At \(h=0\), the zero-error alternatives are scalar multiples of
\(z^9-a^9\) and \((z-a)(z+a)^8\). This boundary classification is known
and is not claimed anew. The uniform regular root exponent \(1\) and
collapsed exponent \(1/2\) cannot be increased: the boundary subcase
contains the sharp families in the preceding
[two-family boundary proof](../sendov_degree9_two_family_boundary_stability/PROOF.md).
The constants and radius are conservative.

The new scope permits an independent upper surplus at an interior root
and gives the sharp leading collapsed obstruction (5). The previous
effective annulus assumed \(\sigma=\eta/20\) and excluded collapse by a
polar variance estimate. Here both branches are retained, and disk
containment alone supplies (5). The unrestricted first-power Tang--Zhang
endpoint is not established.

Rotate and divide by the leading coefficient to make the polynomial monic
and \(a=|a|=1-\eta\ge99/100\). Write
\[
 p(z)=(z-a)\prod_{k=1}^8(z-z_k),\qquad
 p'(z)=9\prod_{j=1}^8(z-\zeta_j),\qquad
 u_k=(a-z_k)^{-1},\quad q_j=(a-\zeta_j)^{-1},\quad r_j=|q_j|.
\]
Finiteness makes the marked root simple and all reciprocals well defined.
Rotation preserves the energies and restores the complex targets at the
end.

## 1. Bounded coordinates and signed defects

Differentiating \(p(a+w)=p'(a)w\prod_k(1+wu_k)\) gives
\[
 e_k(q)=(k+1)e_k(u),\qquad 0\le k\le8.                 \tag{7}
\]
In particular \(\sum q=2\sum u\). Put \(\mu=F(a)/8>0\).
Triangle inequality and Maclaurin give
\(|e_k(u)|\le\binom8k\mu^k/(k+1)\). A root of the monic reciprocal-root
polynomial with modulus at least \(7\mu\) would give, by its equation,
\[
 1\le\sum_{k=1}^8\frac{\binom8k}{(k+1)7^k}
       =\frac{41980912}{51883209}<1.
\]
Thus \(|u_k|<7\mu<8\). Gauss--Lucas and disk containment give
\[
 |u_k|\ge\frac1{1+a}\ge\tfrac12,\qquad
 \tfrac12\le r_j\le F(a)-\frac7{1+a}\le\tfrac92+\sigma<5. \tag{8}
\]

Set \(b=1-a^2\), \(\alpha_k=\Re u_k-1/2\), and \(A=\sum\alpha_k\).
For \(z_k=a-1/u_k\), its disk constraint is exactly
\[
 b|u_k|^2+2a\Re u_k-1\ge0.                             \tag{9}
\]
Since \(b\le2\eta\), \(|u_k|<8\), and \(a\ge99/100\),
\(\alpha_k\ge(\eta-b|u_k|^2)/(2a)\ge-65\eta\).
These defects can be negative. The sum identity gives \(A\le\sigma/2\).
Their negative parts sum to at most \(520\eta\), so
\[
 A\ge-520\eta,\qquad
 \sum|\alpha_k|\le1040\eta+\sigma/2\le1040h,\qquad
 \Re\sum q_j\ge8-1040\eta.                             \tag{10}
\]
For \(d_j=r_j-\Re q_j\ge0\),
\[
 \sum d_j\le1040\eta+\sigma\le1100h,\qquad
 8-1040\eta\le F(a)\le8+\sigma.                        \tag{11}
\]
Projection to \(U_k=1/2+i\Im u_k\) costs \(|\alpha_k|\). For a positive
defect it reduces modulus; otherwise its cost is at most \(65\eta\).
Thus \(|U_k|<8+65\eta<9\). The boundary-only assertion
\(|U_k|\le|u_k|\) is not used for negative defects.

## 2. Approximate Newton saturation without a variance-gap premise

Telescoping the elementary products using radius \(9\) gives
\[
 |e_2(u)-e_2(U)|\le7\cdot9\cdot1040h=65520h,\qquad
 |e_3(u)-e_3(U)|\le21\cdot9^2\cdot1040h=1769040h.
\]
For arbitrary eight real imaginary coordinates,
\(\Re e_3(U)=3\Re e_2(U)-14\). By (7),
\[
 |\Re e_3(q)-4\Re e_2(q)+56|
 \le4(1769040+3\cdot65520)h=7862400h\le8316000h.        \tag{12}
\]
On any \(k\)-element subset, triangle inequality and Cauchy--Schwarz give
\(1-\cos(\sum\theta_j)\le k\sum(1-\cos\theta_j)\).
Multiply by moduli, use \(r_j<5\), and sum subsets to obtain
\[
 0\le e_k(r)-\Re e_k(q)
 \le k\binom7{k-1}5^{k-1}\sum d_j.
\]
For \(k=2,3\), the errors are at most \(77000h,1732500h\).
Put \(e=e_1(x)=F(a)-4\), \(L=e_2(x)\), \(M=e_3(x)\).
Then \(4-1040\eta\le e\le4+\sigma\), and exact shifting gives
\[
 M-L=e_3(r)-4e_2(r)+56+\frac{35}{4}(F(a)-8).
\]
Since \(|F(a)-8|\le1040h\), (11)--(12) imply
\[
 |M-L|\le(8316000+1732500+308000+9100)h
          =10365600h<11000000h.                        \tag{13}
\]
Cauchy--Schwarz gives \(0\le L\le7e^2/16<8\). The exact Newton identity
for eight nonnegative numbers is
\[
 12L^2-21eM=
 \sum_{i<j}(x_i-x_j)^2
 \left(\sum_{k\notin\{i,j\}}x_k^2+
 \sum_{\substack{k<\ell\\k,\ell\notin\{i,j\}}}x_kx_\ell\right)\ge0. \tag{14}
\]
Thus \(L^2\ge(7/4)eM\). As \(e>0\), apply (13) and split the positive
and negative terms before bounding \(e\):
\[
 \begin{aligned}
 L(7-L)&\le\tfrac74(4-e)L+\tfrac74e\,11000000h\\
 &\le\tfrac74\,1040\cdot8h+8\cdot11000000h<90000000h.     \tag{15}
 \end{aligned}
\]
This does not multiply a possibly negative \(L-11000000h\) by an
incorrect lower bound for \(e\). The branches \(L\ge1\) and \(L<1\) are
exhaustive and neither is discarded.

## 3. Regular energy at an interior marked root

If \(L\ge1\), (15) gives \(7-L\le90000000h\). Divide by \(L\ge1\) when
\(L\le7\); when \(L>7\) the conclusion is immediate. The exact variance is
\[
 v=\frac18\sum(r_j-\mu)^2=\frac{7e^2-16L}{64}.
\]
Using \(e\le4+h\) gives
\[
 v\le\frac{90000000}{4}h+\frac7{64}(8h+h^2)<23000000h.
\]
Directly at the interior root,
\[
 \begin{aligned}
 \sum|q_j-1|^2
 &=8v+8\mu^2-2\Re\sum q_j+8\\
 &\le184000000h+2\sigma+\sigma^2/8+2080\eta<190000000h.  \tag{16}
 \end{aligned}
\]
Here \(\mu\le1+\sigma/8\) and (10) were used. Since
\(\zeta_j=-\eta+(q_j-1)/q_j\) and \(|q_j|\ge1/2\),
\[
 Q\le16\eta^2+8\sum|q_j-1|^2\le1600000000h.             \tag{17}
\]
Consequently \(T=\max|\zeta_j|\le40000\sqrt h\le1/75<1/32\), since
\(\sqrt h\le1/3000000\). No boundary-root stability theorem is applied
at an interior root.

## 4. Projecting all nine roots and anchoring the matching

Summing (9) gives the exact nonnegative radial defect
\[
 D_a=b\sum|u_k|^2+a\Re\sum q_j-8
 \le1024\eta+a(8+\sigma)-8\le1016\eta+\sigma\le1016h.     \tag{18}
\]
Radially project all nine roots to the unit circle, including \(a\) to
\(1\); a zero root can be projected to any unit argument. Let the resulting
monic polynomial be \(\widetilde p\). In coefficient norm
\(\|g\|_1=\sum|g_k|\), telescoping the nine factors gives
\[
 \begin{aligned}
 \|p-\widetilde p\|_1
 &\le2^8\left(\eta+\sum_{k=1}^8(1-|z_k|)\right)\\
 &\le256\eta+256\sum(1-|z_k|^2)\le256\eta+1024D_a.       \tag{19}
 \end{aligned}
\]
The last step uses \(|a-z_k|\le2\). The marked-root term \(256\eta\)
is necessary: leaving \(a\) inside the disk would spoil exact unit-circle
coefficient pairing.

Write \(p=z^9+\sum_{k=0}^8c_kz^k\) and
\(\widetilde p=z^9+\sum b_kz^k\). Then \(|b_0|=1\) and
\(b_k=b_0\overline{b_{9-k}}\), so for \(1\le k\le4\),
\[
 |c_{9-k}|\le|c_k|+|c_k-b_k|+|c_{9-k}-b_{9-k}|.
\]
Differentiation gives \(c_k=(9/k)(-1)^{9-k}e_{9-k}(\zeta)\).
For \(m\ge2\), averaging the pairs in each monomial gives
\[
 |e_m(\zeta)|\le\binom8m(Q/8)T^{m-2}.
\]
Indeed each pair occurs in \(\binom6{m-2}\) monomials; divide by
\(\binom m2\) and use
\(\sum_{i<j}|\zeta_i\zeta_j|\le7Q/2\). This proves the displayed
coefficient by the elementary binomial identity, including \(T=0\).
Summing the four pairs and using (19),
\[
 \begin{aligned}
 C:=\sum_{k=1}^8|c_k|
 &\le256\eta+1024D_a+\frac Q4(126T^3+84T^4+36T^5+9T^6)\\
 &\le256\eta+1024D_a+\frac{129}{4}Q^{5/2}\\
 &\le256\eta+1024D_a+4\cdot10^{24}h^{5/2}.              \tag{20}
 \end{aligned}
\]
Here \(126+84/32+36/32^2+9/32^3<129\), and
\((129/4)(1600000000)^{5/2}=3302400000000000000000000<4\cdot10^{24}\).
The coefficient mechanism follows the preceding boundary proof and
independent unit-circle refinement, now with the interior error (19).

From \(p(a)=0\) and \(p'=9\prod(z-\zeta_j)\), integration along \([a,1]\)
gives \(|p(1)|\le9\eta(1+T)^8\le18\eta\). Therefore
\[
 p(z)-(z^9-1)=p(1)+\sum_{k=1}^8c_k(z^k-1).
\]
Set
\[
 \rho=80\eta+300D_a+2\cdot10^{24}h^{5/2}>0.
\]
Since \(h^{3/2}\le10^{-13}/3000000\),
\[
 \rho+\eta\le[81+300\cdot1016+200000/3]h<400000h<1/100.
\]
On a circle of radius \(\rho\) about a ninth root \(\omega\), writing
\(z=\omega(1+w)\) gives
\[
 |z^9-1|\ge9\rho-\sum_{k=2}^9\binom9k\rho^k\ge8\rho.
\]
The tail divided by \(\rho\) is increasing and is less than one at \(1/100\).
Also \((101/100)^8+1<21/10\), so on that circle
\[
 |p(z)-(z^9-1)|\le18\eta+(21/10)C<8\rho.               \tag{21}
\]
The strict comparisons hold term by term:
\(18+(21/10)256<8\cdot80\), \((21/10)1024<8\cdot300\), and
\((21/10)4\cdot10^{24}<8\cdot2\cdot10^{24}\).
The high-index term is positive as \(h>0\).
The nine disks are disjoint: adjacent ninth roots have separation at least
\(4/9\), and their diameters are less than \(1/50\). Rouche gives exactly
one root per disk, counted with multiplicity. The disk about \(1\) contains
\(a\) because \(\rho>\eta\) if \(\eta>0\), or \(a=1\) otherwise.
Moving the targets from \(\omega\) to \(a\omega\) costs at most \(\eta\).
This proves (2)--(3) with the marked root anchored exactly.

## 5. Collapsed original-root energy with signed terms retained

If \(L<1\), then \(7-L>6\), so (15) gives
\[
 L\le15000000h.                                       \tag{22}
\]
Write \(u_k=1/2+\alpha_k+it_k\), \(B=\sum t_k\), and
\(E=\sum|u_k-1/2|^2\). Expansion using \(e_2(u)=e_2(q)/3\) gives
\[
 E=2\sum\alpha_k^2+B^2-14-7A-A^2+\frac23\Re e_2(q).    \tag{23}
\]
The signed term \(-7A\) cannot be discarded; (10) gives
\(-7A\le3640\eta\). Also \(\sum\alpha_k^2\le(1040h)^2\), and
\[
 B^2=\tfrac14(\sum\Im q_j)^2
 \le2\sum(\Im q_j)^2\le4\cdot5\sum d_j\le22000h.
\]
Here \((\Im q_j)^2=(r_j-\Re q_j)(r_j+\Re q_j)\le10d_j\).
Exact shifting gives \(e_2(r)=L+(7/2)e+7\le L+21+(7/2)\sigma\), and
\(\Re e_2(q)\le e_2(r)\). Dropping only the nonpositive term \(-A^2\)
from (23), then using (22), yields
\[
 E\le2(1040h)^2+22000h+3640\eta+\frac23L+\frac73\sigma
       \le11000000h.                                  \tag{24}
\]
Since \(|u_k|\ge1/2\), inversion gives
\[
 |z_k+a|\le4|u_k-1/2|+2\eta\le4\sqrt E+2\eta
          \le15000\sqrt h.                             \tag{25}
\]
For instance \(\sqrt{11000000}<3317\) and \(2\sqrt h<1\) suffice.
This avoids a generic multiple-root coefficient perturbation estimate.

## 6. Collapsed critical matching and sharp radial obstruction

Choose a largest \(x_j\), labeled \(x_8\). Because \(e\ge4-1040h\),
\(x_8\ge e/8>1/3\). Its pair products belong to \(L\), so
\[
 s:=\sum_{j=1}^7x_j\le3L\le45000000h,\qquad
 |x_8-4|\le|e-4|+s\le45001040h.
\]
For targets \(q_j^0=1/2\) for \(j\le7\) and \(q_8^0=9/2\),
\[
 \sum|r_j-q_j^0|^2\le(45000000^2+45001040^2)h^2\le410h.
\]
Also \(\sum|q_j-r_j|^2=2\sum r_jd_j\le11000h\), whence
\(\sum|q_j-q_j^0|^2\le22820h\). Inversion costs at most \(4\) per
distance, as both reciprocals have modulus at least \(1/2\).
Its targets \(a-2,a-2/9\) differ from \(-a,7a/9\) by at most \(2\eta\).
Thus the maximal critical error is at most
\(4\sqrt{22820h}+2\eta<1000\sqrt h\), proving (4).

A direct radial identity supplies the additional obstruction. Since
\(\sum|u_k|^2=2+A+E\), equation (18) becomes
\[
 0\le D_a=-4\eta-2\eta^2+(2-\eta^2)A+bE.               \tag{26}
\]
Using \(A\le\sigma/2\), \(b\le2\eta\), and (24),
\[
 (1-\eta^2/2)\sigma\ge4\eta+2\eta^2-2\eta E
                    \ge(4-22000000h)\eta+2\eta^2.
\]
The right side is nonnegative and its linear coefficient exceeds \(3\).
Since \(0<1-\eta^2/2\le1\), this proves (5), including \(\eta=0\).
For positive \(\eta\), it excludes \(\sigma\le3\eta\).
To obtain (6), choose the permissible upper parameter \(\sigma=3\eta\),
so \(h=4\eta\), and use (2).

The leading coefficient \(4\) is sharp. For interior \(a=1-\eta\), take
\[
 p_\eta(z)=(z-a)(z+1)^8.
\]
All roots are in the disk, and exactly
\(p'_\eta=(z+1)^7(9z+1-8a)\). Hence the criticals are \(-1\) seven
times and \((8a-1)/9\) once, and
\[
 F(a)=\frac{16}{1+a}=8+\frac{8\eta}{2-\eta},\qquad
 \sigma=\frac{8\eta}{2-\eta},\qquad \sigma/\eta\longrightarrow4.
\]
Here \(h\to0\) and \(L\to0\), so the examples eventually lie in the
collapsed branch. No leading coefficient above \(4\) can hold in a
necessary estimate \(\sigma\ge(C-o(1))\eta\) for this branch.
This is a branch-specific statement, not a globally optimal boundary
first-power margin.

## 7. Zero parameter, dependencies and trust boundary

For \(h=0\), \(a=1,\sigma=0\). Equations (9)--(11) give
\(\alpha_k=d_j=0,F=8\), hence \(e=4,M=L\).
Newton gives \(L(7-L)\le0\), and Maclaurin gives \(0\le L\le7\).
If \(L=7\), variance zero gives \(q_j=1\), hence all criticals are zero;
integration with \(p(1)=0\) gives \(p=z^9-1\).
If \(L=0\), (23) gives \(E=0\), all other roots are \(-1\), and
\(p=(z-1)(z+1)^8\). Undoing rotation and scaling proves the zero case.

The sharpness of the root powers comes from the published boundary
families \(P_u,H_v\): their root displacements are comparable respectively
to \(\tau,\sqrt\tau\), with \(F(1)=8+8\tau\).
Taking \(\sigma=8\tau\) makes \(h=8\tau\). These are cited inputs, not new
sharpness constructions in this contribution.

All finite algebra needed for the interior statement is rederived here.
Methods build on the previous effective-annulus projection/Newton proof,
the two-family boundary proof and independent unit-circle refinement.
Neither a polar variance exclusion nor the full quadratic Tang--Zhang
theorem is needed as a premise. The known equality classification is
context, and is recovered directly at zero parameter.

The standard-library checker verifies Newton, signed reciprocal energy,
vertical projection, shifted symmetric and variance identities, radial
feasibility, paired coefficients, every finite constant comparison, and
the sharp-slope family's factorization. It rejects altered Newton,
signed-energy and marked-root projection certificates. The universal
argument remains written mathematics: complex factorization, Gauss--Lucas,
Maclaurin, disk containment, phase estimates, coefficient norms, integration
and Rouche. No solver, floating roots, incomplete enumeration, external
corpus or private data is evidence. Independent review of this new theorem
is pending.
