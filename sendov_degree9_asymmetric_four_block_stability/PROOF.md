# The full asymmetric 3+3+1+1 angular class

Actual author **six-sendov-2**, role **researcher**, 2026-09-30.
Complete ordinary author proof with an exact rational sign certificate.
Independent review of this extension is pending. Spectral continuity
and the all-disk local expansion are explicitly credited premises.

## 1. Claim and its boundary

For a nonzero balanced real eight-vector \(\theta\), set
\[
\mu_m=\sum_j\theta_j^m,\quad e=\mathbf1/\sqrt8,\quad
P=I-ee^*,\quad A=P\operatorname{diag}(\theta)P|_{e^\perp},
\quad w=\operatorname{diag}(\theta)e,
\]
\[
\Psi(\theta)=\sum_{\lambda\in\operatorname{spec}(A)}
                 \|\Pi_\lambda w\|^4,\quad
p_8=\frac{10985}{33554432},\quad
K(\theta)=p_8\left[122+\frac{224\mu_4-5760\Psi}{\mu_2^2}\right].
                                                               \tag{1}
\]
The sum is over distinct eigenvalues and uses their full spectral
projections. The [angular theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and [independent angular audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/REVIEW.md)
supply continuity through all collisions, scale invariance of \(K\),
and its relevance to the reciprocal critical-distance sum.

Let \(\mathcal C_{3311}\) be the balanced vectors whose entries can be
partitioned into two constant triples and two singleton entries.
The four values may coincide. Normalize \(\max|\theta_j|=1\), and put
\(J=\mu_2K/p_8\). Recall the credited scalar curve
\[
j(u)=\frac{2058+21912u-15876u^2+19224u^3+3402u^4}
                 {(3+u)(1+3u)^2},\qquad J_*=j(u_*),             \tag{2}
\]
where \(u_*\in(2/25,9/100)\) is the unique maximizing root of
\[
26634-231084u-907290u^2+376920u^3
                +971190u^4+224532u^5+30618u^6=0.              \tag{3}
\]
The [earlier four-block proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_block_basin/PROOF.md)
and [saturated symmetric face](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_symmetric_displacement_face/PROOF.md)
establish its value, uniqueness, and
\[
J_*>j(1/9)=5472/7>780,\qquad
J_*-j(u)\ge450(u-u_*)^2\quad(0\le u\le1/4).                  \tag{4}
\]
These scalar facts and the basin value below are credited.

**Theorem 1.** Throughout \(\mathcal C_{3311}\),
\[
J\le J_*,                                                   \tag{5}
\]
with equality precisely at permutations of
\((1,1,1,-1,-1,-1,\sqrt{u_*},-\sqrt{u_*})\).
If a triple attains the maximum absolute slope, reflect to make it
\(-1\). Write the other triple as \(x\), and order the singletons as
\(b\ge c=3-3x-b\). Then
\[
\frac13\le x\le1,\quad \frac32(1-x)\le b\le1,\quad
k=\frac{4(1-x)}{1+x},\quad v=\frac{2b-3+3x}{1+x},\quad r=v^2,
\]
\[
0\le k\le2,\qquad 0\le v\le1-k/2.                           \tag{6}
\]
On the competitive cap \(k\le1/16,\ r\le1/4\),
\[
j(r)-J\ge12k,\qquad J_*-J\ge12k+450(r-u_*)^2.                \tag{7}
\]
Every other profile in the class has \(J\le780\).
In particular a singleton-saturated profile cannot maximize.
For the orbit \(\mathcal O_*\) of the unit-normalized equality vector,
\[
\operatorname{dist}(\theta/\|\theta\|,\mathcal O_*)^2
                        \le\frac76(J_*-J).                  \tag{8}
\]
The exact outward derivative is
\[
\left.\partial_kJ(k,r)\right|_{k=0}=-j(r)/2.                 \tag{9}
\]

**Theorem 2 (complex polynomial phase class).** Let
\(p(z)=c(z-a)\prod_{j=1}^8(z-z_j)\), \(c\ne0\), \(0<a<1\),
have all roots in the closed unit disk and simple marked root \(a\).
Set
\[
G=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}-\frac{16}{1+a},\quad
\rho=\max_j|z_j+1|,\quad \kappa=(1+a)(a-5/8).                 \tag{10}
\]
Critical points have their algebraic multiplicities. Other roots may
repeat. When \(\rho\le1/2\), write uniquely
\(z_j=-(1-\tau_j)e^{i\phi_j}\), \(\tau_j\ge0\),
\(-\pi/2<\phi_j<\pi/2\). Restrict to polynomials whose eight phases
can be partitioned into two constant triples and two singleton entries.
This imposes neither real coefficients nor equal inward depths within
the triples.

Let \(R_{3311}(a)\) be the supremum of \(0\le r\le1/2\) such that
every polynomial in this phase class with \(\rho\le r\) has \(G\ge0\).
The admissible radii form an initial interval; its endpoint need not
be admissible. Then
\[
\lim_{a\downarrow5/8}\frac{R_{3311}(a)^2}{\kappa}
 =B_*=\frac{106496}{5J_*},\qquad
                      27.106707<B_*<27.106708.               \tag{11}
\]
Every squared radius \((B_*-\varepsilon)\kappa\), \(0<\varepsilon<B_*\),
is uniformly sufficient for sufficiently small positive \(a-5/8\).
The known symmetric boundary family gives matching negative gaps at
\(\rho^2=\lambda B_*\kappa+O(\kappa^2)\), for every \(\lambda>1\).
No numerical neighborhood or sign at the exact crossing is asserted.

For negative-gap sequences in this class with
\(\rho^2/\kappa\to B_*\), total inward depth and squared total phase
are \(o(E^2)\), the centered unit phase direction approaches
\(\mathcal O_*\), and \(G/E^2\to0\), where
\(E=\sum_j|(a-z_j)^{-1}-(1+a)^{-1}|^2\).

## 2. Complete coverage of the multiplicity class

Permutations, overall sign and positive scaling preserve (1) and its
grouped multiplicities. Suppose a triple is saturated. Reflect to give
it value \(-1\); balance gives \(b+c=3(1-x)\). Bounds on the two
singletons force \(x\ge1/3\). Ordering them gives exactly (6).
In units of half the separation of the triple values, the vector is
\[
\vartheta(k,v)=
(1-k/4)^3,\ (-1-k/4)^3,\ 3k/4+v,\ 3k/4-v,                 \tag{12}
\]
where an exponent here denotes repeated entries, not powers.
Its maximum absolute entry is \(1+k/4\); dividing by that number
gives the original max-normalized vector.

If a singleton is saturated, reflect and order so that it equals \(1\)
and the triple values satisfy \(x\ge y\). Set
\(t=-(x+y)/2,\ d=(x-y)/2\). Balance gives the other singleton
\(6t-1\). Its bound forces \(0\le t\le1/3\), and the triple bounds
give \(0\le d\le1-t\). Thus this chart is exactly
\[
\vartheta_s(t,d)=(d-t)^3,\ (-d-t)^3,\ 1,\ 6t-1,
\qquad 0\le t\le1/3,\quad0\le d\le1-t.                    \tag{13}
\]
Every such vector is balanced and max-normalized. The two charts
cover the whole class, including overlapping saturation and coinciding
values.

## 3. Derivation of the exact cubic trace

For (12), shift the spectral variable by \(k/4\), and put
\[
H(\ell)=(\ell^2-1)^3[(\ell-k)^2-r],\quad
Q(\ell)=4\ell^3-7k\ell^2+(3k^2-3r-1)\ell+k.
\]
Direct differentiation gives
\[
H'=2(\ell^2-1)^2Q.                                         \tag{14}
\]
The four compression eigenvalues from the repeated triples have zero
\(w\)-weight. At a generic active root \(\lambda\) of \(Q\), the
classical secular norm identity is
\[
s_\lambda=\|\Pi_\lambda w\|^2
 =-8H(\lambda)/H''(\lambda)=-4F(\lambda)/Q'(\lambda),\quad
F(\ell)=(\ell^2-1)[(\ell-k)^2-r].                           \tag{15}
\]
To verify it, the compression eigenvector is proportional to
\(((\theta_j-\lambda)^{-1})_j\). Orthogonality to \(e\) gives
\(\sum(\theta_j-\lambda)^{-1}=0\), hence
\(\sum\theta_j/(\theta_j-\lambda)=8\). Its squared \(w\)-inner
product is \(8/\sum(\theta_j-\lambda)^{-2}=-8H/H''\).
The spectral shift changes none of this. This secular mechanism is
classical.

In \(\mathbb Q(k,r)[\ell]/(Q)\), coefficient division gives
\[
16F\equiv f=-A_0\ell^2+B_0\ell+C_0,\quad
A_0=3k^2+4r+12,\quad B_0=3k(k^2-r+9),\quad C_0=16r-15k^2.
                                                               \tag{16}
\]
Multiplication by \(\ell\) in the basis \(1,\ell,\ell^2\) is
\[
M=\begin{pmatrix}
0&0&-k/4\\1&0&-(3k^2-3r-1)/4\\0&1&7k/4
\end{pmatrix},\quad
Y=Q'(M)=12M^2-14kM+(3k^2-3r-1)I.
\]
The discriminant is
\[
\Delta=16+144r+432r^2+432r^3-23k^2+942k^2r
                -855k^2r^2-2k^4+414k^4r+9k^6.              \tag{17}
\]
The standalone checker proves the coefficient identities
\[
\det Y=-\Delta/4,\quad
\operatorname{tr}(f(M)^2\operatorname{adj}(Y)^2)=\Delta V,     \tag{18}
\]
with \(V\in\mathbb Q[k,r]\) having 21 terms, recorded in full in
expected.json. Exact division includes multiply-back reconstruction;
there is no interpolation or modular guessing. At distinct active roots,
\[
\Psi=\operatorname{tr}(f(M)^2Y^{-2})/16=V/\Delta.             \tag{19}
\]
Every matrix product, adjugate identity, quotient reduction and
coefficient of (18) is regenerated from exact rational arithmetic.
Definition-level commutant controls supplement this universal algebra.

For (12) the moments are
\[
\alpha=6+\tfrac32k^2+2r,\quad
\beta=6+\tfrac94k^2+\tfrac{21}{32}k^4+\tfrac{27}{4}k^2r+2r^2.
\]
Define
\[
N=(122\alpha^2+224\beta)\Delta-5760V,\quad
D=\alpha\Delta(1+k/4)^2.
\]
Then \(J=N/D\) generically. At \(k=0\), coefficient comparison recovers
the entire credited curve \(j(r)\). The canonical functional
\(N/(\alpha\Delta)\) is even in \(k\); differentiating
\((1+k/4)^{-2}\) gives (9), also checked as a coefficient identity.

On \(0\le r\le1\),
\[
\Delta=(k^2-1)^2(9k^2+16)+144r+
 r[87k^2+414k^4+432r+432r^2+855k^2(1-r)].                  \tag{20}
\]
It is positive except at \(k=1,r=0\). No zero denominator is divided.
Continuity of (1) extends inequalities from the dense generic set;
the five/three collision there has \(J=8096/25\).

For (13), let \(v_s=1-3t\) and homogenize:
\[
\Delta_s=d^6\Delta(4t/d,v_s^2/d^2),\quad
V_s=d^{10}V(4t/d,v_s^2/d^2).                                \tag{21}
\]
The weighted monomial degrees are at most 6 and 10, so these are
polynomials even at \(d=0\). Put
\[
\alpha_s=6d^2+24t^2+2v_s^2,\quad
\beta_s=6d^4+36d^2t^2+168t^4+108t^2v_s^2+2v_s^4,
\]
\[
N_s=(122\alpha_s^2+224\beta_s)\Delta_s-5760V_s,\quad
D_s=\alpha_s\Delta_s.
\]
At generic points \(d>0\), real-root interlacing gives
\(\Delta_s>0\), and \(J=N_s/D_s\). Generic points are dense in the
closed singleton triangle. Credited continuity handles all its edges
and collisions, including \(d=0\).

## 4. Complete finite sign proof

The tensor Bernstein basis on a rational rectangle is nonnegative and
sums to one. Nonnegative coefficients prove positivity throughout the
rectangle; their minimum bounds the polynomial below. The checker
regenerates all forward coefficients and inverts the basis back to the
power polynomial. It checks rectangle coverage on every open cell cut
out by their boundaries, and by exact area.
CERTIFICATE.md lists all boxes and minima; expected.json supplies
coefficient hashes. There is no imported coefficient corpus.

**Majority cap.** The polynomial \(j_ND-j_DN\) is divisible by \(k\).
Its quotient \(C\) has all 90 Bernstein coefficients positive on
\([0,1/4]^2\), with \(C\ge98784\). On this rectangle,
\[
\Delta<102,\quad\alpha<7,\quad(1+k/4)^2<8/7,\quad j_D<10,
\]
so \(D<816\) and \(j_DD<8160\). Thus
\[
j(r)-J=kC/(j_DD)\ge12k
\]
for \(k>0\), since \(98784>12\cdot8160\); continuity includes \(k=0\).
Using (4) proves (7) on the smaller competitive cap.

**Majority exterior.** The substitution \(k=2h,\ r=(1-h)^2z\),
\(h,z\in[0,1]\), covers (6). Seven rectangles cover
\([1/32,1]\times[0,1]\); every Bernstein coefficient of
\((780D-N)(2h,(1-h)^2z)\) is nonnegative. This proves \(J\le780\)
when \(k\ge1/16\). One positive rectangle in the original coordinates,
\([0,1/16]\times[1/4,1]\), proves it when \(k\le1/16,r\ge1/4\).
This enclosing rectangle contains the relevant domain subset.
Continuity includes the zero-discriminant point.

**Singleton saturation.** Substitute \(d=(1-t)z\). Two rectangles
\([0,1/7]\times[0,1]\) and \([1/7,1/3]\times[0,1]\) cover (13).
All 242 Bernstein coefficients of the substituted \(780D_s-N_s\)
are nonnegative. Positive generic denominators give \(J\le780\),
and continuity closes all edges and collisions.

These are **860 new coefficients on eleven boxes**. The charts cover
Section 2; outside the cap (4) gives \(J_*-J>12/7\), while (7)
vanishes only at \(k=0,r=u_*\). This proves (5) and equality.
The credited scalar loss is also reproduced with six coefficients:
for \(T=j_N'j_D-j_Nj_D'\), \(T'\le-90000\) on \([0,1/4]\),
and \(j_D<10\). Since \(T(u_*)=0\), integration of
\(|j'(r)|\ge900|r-u_*|\) gives 450. The original global scalar
optimizer classification remains credited.

## 5. Quantitative distance

In the cap the \(k\) and \(v\) difference vectors in (12) are orthogonal:
\[
\|\vartheta(k,v)-\vartheta(0,\sqrt{u_*})\|^2
                      =\tfrac32k^2+2(v-\sqrt{u_*})^2.
\]
Since \(\|\vartheta\|^2\ge6\), the normalization and reverse triangle
inequalities give squared unit-vector distance at most
\[
k^2+\tfrac43(v-\sqrt{u_*})^2
                    \le k^2+\tfrac{50}{3}(r-u_*)^2.
\]
Here \(u_*>2/25\) and \(v\ge0\) bound the square-root denominator.
With \(k\le1/16\), (7) therefore gives the stronger cap bound
\(\operatorname{dist}(\widehat\theta,\mathcal O_*)^2\le(J_*-J)/27\).
Outside, the orbit contains both signs, so squared distance to it is
at most two. The deficit exceeds \(12/7\), proving (8).

## 6. Complex phase-class basin

Use the [full displacement variational reduction](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_displacement_variational_basin/PROOF.md),
including its original-root metric conversion. Its all-disk joint
premise is the [sharp energy basin proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sharp_energy_basin/PROOF.md),
checked in the [independent energy audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_energy_basin_review3/REVIEW.md).
These analytic inputs cover arbitrary complex disk roots, independent
inward depths and every angular collision type.

On a negative-gap sequence converging to collapse, put
\[
T=\sum\tau_j,\quad M_\phi=\sum\phi_j,\quad L=\sum\phi_j^2,\quad
s=\|\phi-(M_\phi/8)\mathbf1\|,\quad
\widehat\theta=(\phi-(M_\phi/8)\mathbf1)/s.
\]
The cited bootstrap gives \(L>0\),
\(T=O(L^2),M_\phi^2=O(L^2),\kappa=O(L)\), hence \(s>0\).
Centering preserves the constant triples. Uniformly along these
sequences, with \(d_0=13/8\),
\[
G=\kappa E+\frac{128}{169}T+\frac{40}{2197}M_\phi^2
                    -K(\widehat\theta)E^2+o(E^2),            \tag{22}
\]
\[
\rho^2=s^2q+O(s^3),\quad E=d_0^{-4}s^2+O(s^4),\quad
q=\max|\widehat\theta_j|^2\ge1/8.                            \tag{23}
\]
Theorem 1 after max normalization gives \(K/q\le p_8J_*\).
Negativity, the nonnegative inward/mean terms, and (23) yield
\(\kappa d_0^4/\rho^2\le p_8J_*+o(1)\).
A sequence of failures with \(\rho^2\le(B_*-\varepsilon)\kappa\)
would contradict it. This proves uniform sufficiency and the lower
limit in (11).

For the upper limit use the credited actual family
\[
p_{a,t}(z)=(z-a)(z^2+2\cos t\,z+1)^3
                    (z^2+2\cos(\sqrt{u_*}t)\,z+1).            \tag{24}
\]
It lies in the new phase class. With \(t^2=\lambda B_*\kappa\),
\(\lambda>1\), the known angular/joint expansion gives \(G<0\)
of order \(\kappa^2\), and
\(\rho^2=\lambda B_*\kappa+O(\kappa^2)\).
These radii are below \(1/2\) for small \(\kappa\), so the local
cutoff does not affect the limit. This proves positivity, finiteness
and the matching upper limit. The scale is \(d_0^4/p_8=106496/5\).

At the sharp scale, dividing (22) by \(E^2\) and using (23) gives
\[
\frac G{E^2}
 =q\left[p_8J_*-\frac{K(\widehat\theta)}q\right]
   +\frac{128}{169}\frac T{E^2}
   +\frac{40}{2197}\frac{M_\phi^2}{E^2}+o(1).
\]
All displayed terms are nonnegative and must vanish because \(G<0\).
Equation (8) gives angular convergence and substitution gives
\(G/E^2\to0\). No remainder rate is claimed.

## 7. A failed shortcut and the remaining frontier

The global inequality \(J(k,r)\le j(r)\) is false. At
\(k=1/4,v=2/3,r=4/9\), the actual max-normalized vector is
\[
(15/17,15/17,15/17,-1,-1,-1,41/51,-23/51).
\]
Its four values are distinct, it is balanced and lies in (6), but
\[
J=\frac{7903208317384992}{14021061354337},\quad
j(r)=\frac{848970}{1519},\quad
J-j(r)=\frac{101512976116319958}{21297992197237903}>0.
\]
The checker verifies both values and the compression definition.
This refutes a fixed-\(r\) symmetry-restoration shortcut, and supplies
no polynomial counterexample.

The unrestricted balanced angular maximum remains unidentified.
This proof closes one entire multiplicity class but gives no structural
reduction of arbitrary eight-vectors to it. Other multiplicities,
more distinct entries, general complex higher-order corrections,
effective neighborhoods and the global first-power endpoint remain open
here. At \(a=5/8\), \(16/(1+a)=128/13>8\), so negative local gaps
are not first-power violations. LITERATURE.md compares primary equality
results and complementary campaign inputs.
