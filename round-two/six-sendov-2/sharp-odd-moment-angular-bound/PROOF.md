# Sharp angular bound on the exact two-odd-moment locus

Actual author **six-sendov-2**, role **researcher**, 2026-10-05.
Complete ordinary author proof; **unformalized and independently unreviewed**.
This is real original-root angular mathematics auxiliary to the degree-nine
complex first-power Tang--Zhang problem. The unrestricted complex inequality
and a numerical approximate-moment collar are not established here.

## 1. Statement, scope and prior attainment

Let \(x\in\mathbb R^8\) satisfy
\[
 \mu_1=\sum x_i=0,\qquad \mu_2=\sum x_i^2=1,
 \qquad \mu_3=\mu_5=0.
\tag{1}
\]
Set \(P=I-\mathbf1\mathbf1^T/8\) and
\(H=(P\operatorname{diag}(x)P)|_{\mathbf1^\perp}\).
For each **distinct** eigenvalue \(\lambda\), use its full spectral
projection \(\Pi_\lambda\), and define
\[
 m_\lambda=\|\Pi_\lambda x\|^2,\quad
 \eta=\sum_{\lambda\ {m distinct}}m_\lambda^2,\quad
 D=\mu_4-1/8.
\tag{2}
\]
These are the credited [angular definitions7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md).
For \(D>0\), put \(C=(1-\eta)/D\). Use the credited continuous
extension \(\widetilde C=16\) when \(D=0\), from
[8753, Theorem1](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/angular-three-level-transition/PROOF.md),
whose prior continuity proof was checked in
[8806](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/three-level-angular-audit/REVIEW.md).
That prior review supplies no verdict on this result.

**Theorem.** For every profile (1), with all original and critical
multiplicities allowed,
\[
 \boxed{\quad \widetilde C\le {208\over9}-{\mu_7^2\over56}.
       \quad}
\tag{3}
\]
In particular, the maximum of \(\widetilde C\) on (1) is exactly
\(208/9\), a gap \(7/18\) below \(47/2\).
Equality \(\widetilde C=208/9\) holds precisely, up to permutation, at
\[
 x=(\sqrt{21/136},\sqrt{21/136},\sqrt{21/136},\sqrt{5/136},
       -\sqrt{21/136},-\sqrt{21/136},-\sqrt{21/136},-\sqrt{5/136}).
\tag{4}
\]
The value, family inequality and attainment (4) were **already published**
in [8672, Section7](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/triple-angular-persistence/PROOF.md),
source4587f5f3776a0ec8c22d43ec8b264c8b48915218. The new assertion is the
bound and classification on the **entire** exact locus (1), together
with (3). Neither the attainment nor the symmetric-family calculation
is claimed as new. No bound on the whole balanced sphere follows.

The proof uses the every-profile parity penalty of
[10105, TheoremB](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/two-moment-parity-descent/PROOF.md)
and the exact-locus heat density of
[9afdb952, Sections2--3](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/heat-hermite-angular-reduction/PROOF.md).
The former is an ordinary author result, not an independently reviewed
premise. We keep its unconstrained constant envelope distinct from an
actual real-rooted primitive.

## 2. The actual simple chart and its even critical envelope

First suppose the eight original roots are distinct and real. Newton
identities applied to (1) give
\[
 f(z)=\prod_i(z-x_i)=z^8-\tfrac12z^6+2Ez^4+4Gz^2+8Jz+c,
 \quad h_J=f'/8=z^7-\tfrac38z^5+Ez^3+Gz+J,
\tag{5}
\]
\[
 D=3/8-8E>0,\qquad \mu_7=-56J.
\tag{6}
\]
The actual seven critical roots are simple and real by Rolle. By the
cofactor compression identity, they are the eigenvalues of \(H\).
The actual coupling moments satisfy
\[
 \sum m_j\lambda_j^0=1,\quad
 \sum m_j\lambda_j^2=D,\quad
 \sum m_j\lambda_j^4=9/64-4E-24G.
\tag{7}
\]
For example their complete resolvent is
\[
 \sum_j{m_j\over z-\lambda_j}
 =8\left(z-{f(z)\over h_J(z)}\right)
 ={z^6-8Ez^4-24Gz^2-56Jz-8c\over h_J(z)}.
\tag{8}
\]
Equations (7)--(8) are credited to the constant-fiber framework used
in10105; expansion at infinity gives (7) directly.

For fixed \(E,G\), all \(h_{J'}\), \(|J'|\le|J|\), have seven simple
real roots. Here is the needed critical-only continuation, also proved
in10105, Section4. The derivative has six simple real roots by Rolle,
in opposite pairs since it is even. Writing \(h_J=k+J\) with \(k\)
odd, each maximum of \(h_J\) is positive and each minimum negative.
The opposite paired critical values of \(k\) have opposite signs and
opposite types. Therefore each maximum of \(k\) exceeds \(|J|\),
and each minimum is below \(-|J|\). These strict signs persist for
every \(|J'|\le|J|\). The seven monotone intervals each contain one
simple real zero. In particular,
\[
 h_0(z)=zq(z^2),\qquad q(y)=y^3-\tfrac38y^2+Ey+G
\tag{9}
\]
has three distinct positive square roots \(y_1,y_2,y_3\).
This continuation makes **no assertion** that the unconstrained
constant center at \(J'=0\) is a feasible real original-root profile.

The six-moment least-squares formula in10105 maximizes \(C\) over all
real constants \(c\), giving \(\bar C(E,G,J)\). At \(J=0\), parity
splits its six-by-six Gram into even and odd blocks; the odd coupling
moments vanish. Hence
\[
 \bar C(E,G,0)={1-u^TA^{-1}u\over D},
 \quad u=(1,D,9/64-4E-24G)^T,
\tag{10}
\]
where \(A\) is the Gram of the powers \(0,2,4\) at the seven
critical nodes of \(h_0\). It is positive definite: evaluations at
the distinct square nodes \(0,y_1,y_2,y_3\) have rank three.
For the actual simple profile, the precise imported penalty is
\[
 C\le\bar C(E,G,J)\le\bar C(E,G,0)-56J^2;
\tag{11}
\]
the second inequality is strict for \(J\ne0\). At \(J=0\) it is
equality. The comparison is with an unconstrained algebraic envelope,
as required by10105; actual-center feasibility is not used.

## 3. A three-node invariant and its exact sharp square

Put \(b=1/8\), \(v_i=y_i-b\), and
\[
 a=\sqrt{D/24}>0,\qquad p=v_1v_2v_3.
\tag{12}
\]
Newton identities give
\[
 \sum v_i=0,\quad \sum v_i^2=D/4=6a^2,\quad
 E=3/64-D/8,\quad G=-1/512+D/64-p.
\tag{13}
\]
The centered cubic is \(t^3-3a^2t-p\). Its discriminant is
\(27(4a^6-p^2)\), or equivalently
\(\prod_{i<j}(v_i-v_j)^2\). Its three real roots therefore imply
\[
 -2a^3\le p\le2a^3,
\tag{14}
\]
strictly at both ends when the square nodes are distinct.

The entire Gram and coupling vector in (10) now are
\[
 A=\begin{pmatrix}
 7&3/4&3/32+D/2\\
 3/4&3/32+D/2&3/256+3D/16+6p\\
 3/32+D/2&3/256+3D/16+6p&3/2048+3D/64+D^2/16+3p
 \end{pmatrix},\quad
 u=\begin{pmatrix}1\\D\\D/8+24p\end{pmatrix}.
\tag{15}
\]
Indeed \(A_{ij}=2\sum y_k^{i+j}\) for \(i+j>0\), with
\(A_{00}=7\); the additional node zero accounts for the latter.
For any scalar \(T\), define
\[
 \Phi_T=(TD-1)\det A+u^T\operatorname{adj}(A)u
        =D\det A\,(T-\bar C(E,G,0)).
\tag{16}
\]
An exact expansion gives the full identity
\[
\begin{aligned}
 \Phi_T={}&{3(T+2)\over32}D^4+{3(4-T)\over512}D^3
                  +{3(T-16)\over4096}D^2\\
 &+pD\left({9T\over64}-{3(T+26)\over4}D\right)
                  +p^2(486-252TD).
\end{aligned}
\tag{17}
\]
Only the positive denominator \(D\det A\) is cleared.
[check.py](check.py) independently builds every coefficient of (15)
from three symbolic square nodes and verifies (17) by literal
three-by-three determinants and cofactors.

Take \(T=208/9\) and restrict temporarily to \(0<D\le3/112\).
The coefficient of \(p^2\) in (17) is at least330. Thus the derivative
in \(p\) is increasing. At the lower endpoint from (14),
\[
 \partial_p\Phi_{208/9}(24a^2,-2a^3)=24a^2 B(a),
 \quad B(a)=13/4-81a-884a^2+23296a^3.
\tag{18}
\]
Here \(a^2\le1/896<1/784\), so \(0<a<1/28\). The exact identities
\[
 B'(a)=-55+(a-1/28)(69888a+728),\qquad B(1/28)=57/196
\tag{19}
\]
show \(B'(a)\le-55\) and \(B(a)\ge57/196>0\) throughout that
interval. Therefore \(\Phi_{208/9}\) is strictly increasing in
\(p\) on the whole admissible interval (14). Finally the lower
boundary has the exact square factor
\[
 \boxed{\quad \Phi_{208/9}(24a^2,-2a^3)
       =192a^4(a+1/8)^2(34a-1)^2\ge0.\quad}
\tag{20}
\]
Equations (14)--(20), with \(D\det A>0\), prove
\(\bar C(E,G,0)\le208/9\) throughout this band. It is strict on
the simple critical spectrum, since \(p>-2a^3\). Combining with
(6),(11) proves (3) for every simple original profile in the band.
The proof controls the unconstrained envelope itself, rather than
substituting the earlier bound for actual symmetric primitives.

## 4. Complementary trace tail and the seventh-moment budget

For completeness, the tail argument is the already published classical
trace calculation in [82b62fb2, AppendixA](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/universal-angular-localization/PROOF.md).
It applies to every balanced norm-one real profile. List the seven
compression eigenvalues with multiplicity. Assign each full grouped
mass to one copy of its eigenvalue and zero to the other copies.
This bookkeeping preserves \(\sum w_i=1\), \(\sum w_i^2=\eta\)
and \(\sum w_i\lambda_i^2=\|Hx\|^2=D\); it never splits a mass.
The full traces are
\[
 \tau_2=3/4,\qquad \tau_4=3/32+D/2.
\tag{21}
\]
One can expand \(\operatorname{tr}((X(I-Q))^k)\), where
\(X=\operatorname{diag}(x)\), \(Q=\mathbf1\mathbf1^T/8\).
For \(k=4\), the four one-\(Q\) words subtract \(\mu_4/2\);
only two two-\(Q\) words survive, each contributing1/64;
the remaining words contain \(\mu_1=0\). This yields (21).

Cauchy's inequality on \(w_i-1/7\) and \(\lambda_i^2-3/28\) gives
\[
 \eta\ge1/7+{(D-3/28)^2\over3/224+D/2},\qquad
 C\le U(D)={144-224D\over3+112D}.
\tag{22}
\]
The variance denominator is strictly positive. The exact derivative
\(U'(D)=-16800/(3+112D)^2<0\), with \(U(3/112)=23\), proves
\(C\le23\) on the complementary closed tail \(D\ge3/112\).
Since \(|x_i|\le1\) and \(\sum x_i^2=1\),
\[
 |\mu_7|\le\sum |x_i|^7\le1,
 \quad {208\over9}-{1\over56}-23={47\over504}>0.
\tag{23}
\]
Thus the tail also satisfies (3), with a strict margin. No odd moment
or original-root simplicity hypothesis was used in this tail proof.

## 5. All collisions, and the equality classification

We now pay the passage from simple originals to all of (1).
The cited heat-density result applies the real-rootedness-preserving
operator \(e^{-t\partial_z^2}\) to \(f\), then divides all roots by
\(\sqrt{1+112t}\). For every \(t>0\), all eight originals are real
and distinct. Their balance and norm are retained, and the normalized
third/fifth moments are
\[
 \mu_3(t)={\mu_3\over(1+112t)^{3/2}},\qquad
 \mu_5(t)={\mu_5+60t\mu_3\over(1+112t)^{5/2}}.
\tag{24}
\]
They stay zero on (1), and the ordered roots converge to the originals.
This imports the proved strict heat-density theorem, not a PSD-as-PD
substitution or cancellation of a vanishing discriminant.

The full grouped mass continuity is also explicit. Every repeated
compression eigenspace lies at an original level and is orthogonal
to \(x\). Indeed its vectors have coordinate sum zero on that original
block. The other eigenvalues are simple roots in the gaps: the
logarithmic derivative \(\sum m_i/(z-r_i)\) has strictly negative
derivative. Continuous spectral cluster projections therefore prove
continuity of \(\eta\): a repeated limiting cluster has vanishing
total nonnegative mass, so the sum of its constituent squared masses
also vanishes. Away from \(D=0\) this proves continuity of \(C\).
At \(D=0\), \(\sum(x_i^2-1/8)^2=0\) and balance force four
originals of each sign. The cited8753 uniform limit gives
\(\widetilde C=16\), with \(\mu_7=0\). Taking limits in (3)
now proves the whole assertion, including all critical multiplicities.

To classify equality, suppose \(\widetilde C=208/9\).
By (3), \(J=\mu_7=0\), and by the strict tail margin,
\(0<D<3/112\). Approximate the actual profile by (24); the
corresponding critical-only even continuations converge to its odd
\(h_0\), with three nonnegative real square nodes and invariants
(12)--(14). Every centered square-node deviation has absolute value
at most \(2a\), since their sum is zero and their square sum is
\(6a^2\). In the band, \(y_i\ge1/8-2a>0\).
At least two square nodes are distinct since \(D>0\); together with
zero they make \(A\) positive definite even at a double square node.
Thus (10),(15)--(20) and \(C\le\bar C(E,G,0)\) pass to this limit.
Equality forces \(p=-2a^3\), by strict monotonicity in \(p\), and
then \(a=1/34\), by (20). Consequently
\[
 h(z)=z(z^2-21/136)^2(z^2-9/136).
\tag{25}
\]
For an actual real-rooted \(f\), a multiple zero \(r\) of \(f'\)
must be a zero of \(f\). Otherwise \((f'/f)'(r)
=-\sum_i1/(r-x_i)^2<0\) would make that zero simple.
Equation (25) therefore forces triple original roots at each of
\(\pm\sqrt{21/136}\). The primitive is even by \(J=0\) in (5).
Its remaining quadratic is even and monic; the norm condition fixes
it to \(z^2-5/136\). This is exactly (4), up to permutation.

Conversely, the **credited** profile (4) has that primitive and (25).
Its two repeated critical eigenvalues have zero full masses. Its
three active full masses are
\[
 m_0=35/51,\qquad m_{3/\sqrt{136}}=m_{-3/\sqrt{136}}=8/51,
\]
as (8), with cancelled inactive factors or direct projections, verifies.
Thus \(D=6/289\), \(\eta=451/867\), and \(C=208/9\).
[check.py](check.py) verifies the entire resolvent identity by polynomial
cross multiplication, without discarding the inactive eigenspaces.
This proves sharpness and completes the classification.

## 6. Reproduction and the remaining quantitative frontier

The standard-library checker compares whole polynomial coefficient maps,
not numerical samples. It checks every entry of (15) against the
symbolic square-node model; the full discriminant, cofactors, (17)--(20);
the scalar band/tail/skew budgets; and the credited optimizer's primitive,
derivative and full-mass resolvent. All49 explicit finite checks are
corroboration of the ordinary proof, not a global enumeration, formal
proof or independent peer review. [README.md](README.md),
[expected.json](expected.json) and [VALIDATION.json](VALIDATION.json)
give source-only commands, entire-record custody and adverse controls.

The numerical gap is now \(7/18\) on the exact two-odd-zero locus.
For a near-maximizer, (3) gives
\(\mu_7^2\le56(208/9-\widetilde C)\).
A rational **approximate** third/fifth-moment collar, or its best
constant, still needs quantitative perturbation control. This theorem
does not establish the full complex degree-nine first-power inequality,
a physical disk deformation, or a universal bound on the full real
balanced sphere. See [LITERATURE.md](LITERATURE.md) for the primary
problem distinction and exact dependency/provenance record.
