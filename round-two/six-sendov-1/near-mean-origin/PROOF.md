# Arbitrary-multiplicity origin coercivity near the reciprocal mean

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.
Complete ordinary author proof with compact exact algebra checks;
unformalized and independently unreviewed.

## 1. Statement

Let
\[
 511/512\le a<1,\qquad q_1,\ldots,q_8\in\mathbb C,
 \quad \mu=\tfrac18\sum|q_j|\le1,
 \quad m=\tfrac18\sum q_j,\quad \Re m\ge a.
\]
Set \(R=|m|\), \(\delta=1-a\), and
\[
 \eta_j=q_j/m-1,\qquad \max_j|\eta_j|\le h:=1/32,
 \quad U=\sum(\Re\eta_j)^2,\quad V=\sum(\Im\eta_j)^2.
\]
In particular \(m,q_j\ne0\). Define the normalized origin square
\[
 N_a(q)=\frac{|9\int_0^1\prod_j(1-atq_j)\,dt|^2}
                   {\prod_j|q_j|^2}.
\]
Then
\[
 \boxed{N_a(q)\ge1+\delta+\frac78U+\frac1{32}V>1.}       \tag{1}
\]
There is no multiplicity restriction, individual critical-disk hypothesis,
second-moment premise, or original-root hypothesis in this abstract lemma.
The tube and collar constants are sufficient and are not claimed optimal.
This is a quantitative origin bound, not a full solution of the complex
degree-nine first-power Tang--Zhang conjecture.

For a disk-rooted degree-nine polynomial, rotate a simple marked root to
\(a\in[511/512,1)\), and set \(q_j=(a-\zeta_j)^{-1}\), counting critical
multiplicities. The classical origin identity gives \(N_a(q)\le1\).
The [general polar mean lemma](../general-polar-mean/PROOF.md) gives
\(\Re m>a\) under a hypothetical \(\sum|q_j|\le8\).
Consequently, if the relative tube in this statement holds, then
\(\sum|q_j|>8\). Equivalently any hypothetical failure in this collar
must leave that tube. A collision gives infinity directly. No assertion
that all critical configurations enter the tube is made.

The earlier clustered-critical results and the exact critical \(4+4\)
origin minimum retain their credit. The new object is the coercive
origin functional for eight independent deviations from their complex
mean, with explicit radial and angular costs; see [LITERATURE.md](LITERATURE.md).

## 2. Mean geometry pays for transverse deviations

Balance gives \(\sum\eta_j=0\), and
\[
 a\le R\le\mu\le1,
 \qquad z:=am,\quad |1-z|^2=1-2a\Re m+a^2R^2\le1-a^2.
                                                               \tag{2}
\]
Thus \(|1-z|\le s:=1/16\). Put \(e=1-R\) and \(S=U+V\le8h^2\).
For \(\eta=u+iv\), since \(1+u>0\), the exact rationalization is
\[
 |1+\eta|-(1+u)=\frac{v^2}{|1+\eta|+1+u}
                         \ge\frac{v^2}{2(1+h)}.
\]
Summing and using balance yields
\[
 \mu\ge R\left(1+\frac{V}{16(1+h)}\right),\qquad
                 e\ge\frac{R V}{16(1+h)}.                 \tag{3}
\]
This is the term that offsets the negative transverse term in the
complex origin expansion. It uses the actual modulus mean, without
replacing the data by a conjugate-symmetric tuple.

## 3. An exact integral expansion flat at the boundary

Let \(e_k=e_k(\eta_1,\ldots,\eta_8)\), so \(e_0=1,e_1=0\), and define
the degree-nine polynomials
\[
 B_k(z)=9(-1)^k\int_0^z u^k(1-u)^{8-k}\,du,
                    \qquad 0\le k\le8.                  \tag{4}
\]
All integrals here are polynomial primitives and are path independent.
In particular
\[
 B_0(z)=1-(1-z)^9,
 \quad B_k(1)=\frac{(-1)^k}{\binom8k},
 \quad B'_k(z)=9(-1)^k z^k(1-z)^{8-k}.                   \tag{5}
\]
Write \(P=\prod(1+\eta_j)=1+\sum_{k=2}^8e_k\).
It is nonzero since \(|\eta_j|<1\). Directly expanding the eight
linear factors in the defining integral gives the exact identity
\[
 K:=a m^9\,9\int_0^1\prod_j(q_j^{-1}-at)\,dt
       =\frac{\sum_{k=0}^8 B_k(z)e_k}{P}.                 \tag{6}
\]
Indeed selecting k deviation factors in
\(\prod[1-zt(1+\eta_j)]\) gives
\((-zt)^k(1-zt)^{8-k}e_k\); its integral multiplied by z is (4).
Division by \(P\) converts the q product to the inverse-q product.
Also
\[
                      N_a(q)=\frac{|K|^2}{a^2R^{18}}.    \tag{7}
\]

Set \(D_k=B_k-B_0\), and \(c=27/56\).
Equation (5) gives \(D_2(1)=-27/28\).
Since \(e_2=-\frac12\sum\eta_j^2\), the leading balanced correction
in (6) is \(c\sum\eta_j^2\).
The important estimate is flatness, not a generic degree-nine Lipschitz
bound. Integrate (5) on the segment from 1 to z. For \(|1-z|\le s\),
\[
 |B_k(z)-B_k(1)|\le t_k:=
            \frac{9(1+s)^k s^{9-k}}{9-k}.                \tag{8}
\]
For \(k=0\), use the sharper \(|B_0(z)-1|\le s^9\).
The finite rational bounds at \(s=1/16\) are
\[
 |D_2(z)+27/28|\le d_2:=t_2+s^9,
                 |D_k(z)|\le6/5\quad(2\le k\le8).      \tag{9}
\]
For the second bound it suffices to check the seven explicit rational
numbers \(|(-1)^k/\binom8k-1|+t_k+s^9<6/5\).
They are reconstructed completely by the checker; no sampled complex
evaluation establishes (8) or (9).

## 4. Uniformly bounded higher deviations

The elementary-symmetric identities under balance give
\[
 |e_2|\le S/2,\qquad |e_3|\le hS/3,
 \quad e_4=\tfrac18(\sum\eta_j^2)^2-\tfrac14\sum\eta_j^4,
 \quad |e_4|\le\tfrac54h^2S.                            \tag{10}
\]
Here \(|\sum\eta_j^k|\le h^{k-2}S\), and \(S\le8h^2\).
For \(5\le k\le8\), the elementary bound
\[
              |e_k|\le\frac{\binom8k}{8}h^{k-2}S        \tag{11}
\]
is sufficient. To prove it, bound a product on a k-set by
\(h^{k-2}\) times the average of the products of its pairs, then use
\(|\eta_i\eta_j|\le(|\eta_i|^2+|\eta_j|^2)/2\).
Each coordinate appears in \(\binom7{k-1}\) k-sets, giving (11).
These elementary estimates and Newton identities are classical.

Define the exact rational constants
\[
 L=\frac h3+\frac54h^2+\sum_{k=5}^8\frac{\binom8k}{8}h^{k-2}
     =\frac{305484547}{25769803776},
 \quad T_0=(1/2+L)8h^2=\frac{13190386435}{3298534883328}.
\]
Then \(T:=P-1\) satisfies \(|T|\le(1/2+L)S\le T_0<1\).
From (6), (9)--(11), subtracting the balanced quadratic term gives
\[
 K=B_0+c\sum\eta_j^2+E,
 \quad |E|\le E_0 S,
 \quad E_0=\frac{d_2/2+(6/5)L+cT_0}{1-T_0}.             \tag{12}
\]
The last term comes from
\(-c(\sum\eta_j^2)T/(1+T)\), giving the coefficient c in (12).
The exact finite check gives \(E_0<1/60\).

## 5. Origin gap and coercivity

For any complex K, \(|K|^2\ge2\Re K-1\). Thus (12) implies
\[
 |K|^2\ge1-2s_a^9+
        (27/28-1/30)U-(27/28+1/30)V,
 \quad s_a=\sqrt{1-a^2}.                               \tag{13}
\]
Equations (2)--(3) imply
\[
 1-R^{18}\ge18a^{17}(1-R)
              \ge\frac{18a^{18}}{16(1+h)}V.             \tag{14}
\]
At \(a_0=511/512\), the two exact sign comparisons are
\[
 27/28-1/30>7/8,
 \quad \frac{18a_0^{18}}{16(1+h)}-27/28-1/30>1/32.       \tag{15}
\]
Both remain valid for \(a\ge a_0\). Combining (13)--(15) proves
\[
 |K|^2\ge R^{18}-2s_a^9+(7/8)U+(1/32)V.
\]
Since \(R^{18}\ge a^{18}\ge1-18\delta>1/2\), division in (7) gives
\[
 N_a(q)\ge a^{-2}\{1-4s_a^9+(7/8)U+(1/32)V\}.         \tag{16}
\]
Finally \(a^{-2}\ge1+2\delta\), \(a^{-2}<2\), and
\(s_a^9\le(2\delta)^4/16=\delta^4\) because
\(\sqrt{2\delta}\le1/16\). Hence
\[
 a^{-2}(1-4s_a^9)\ge1+2\delta-8\delta^4\ge1+\delta.
\]
The last inequality follows from \(8(1/512)^3<1\).
The positive deviation terms in (16) are increased by \(a^{-2}\ge1\).
This proves (1) uniformly over all eight complex coordinates.

## 6. Evidence, novelty boundary and unfinished frontier

The checker reconstructs all nine B polynomials in two coefficient
routes, checks their complete derivative and boundary identities,
and checks the balanced Newton identities as polynomial identities in
seven independent complex indeterminates. It independently integrates
the full origin product by convolution and exact interpolation for
Gaussian-rational controls. All error constants, tube controls and
corruption rejection are exact; no floating point or solver is a proof
input. The source is standalone and imports no campaign artifact.

The incomplete-beta algebra, complex segment estimate, uniform product
majorants, modulus mean geometry and polynomial interpretation remain
ordinary written mathematics. Author cross-checks are not independent
review or formalization. (1) has explicit costs but no optimality claim.

The previously published boundary variance budget and actual-root
concentration are not re-proved as new results. The new theorem does
not force a general tuple into its tube, so the global retained-disk
origin inequality and the unrestricted first-power endpoint remain open
here. The concrete next step is to exclude intermediate relative
spreads with the full polar functional and individual critical disks,
or to find an exact obstruction to that larger moment relaxation.
