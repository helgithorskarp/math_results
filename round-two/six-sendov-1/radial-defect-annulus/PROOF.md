# A radial Newton defect and an explicit joint-channel first-power annulus

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.
Complete ordinary author proof, conditional on the explicitly cited mean-tube
lemma in its small-spread branch. Compact exact certificate; unformalized;
independent review of this contribution pending.

## 1. Statements

For eight complex numbers define
\[
 O_a(q)=9\int_0^1\prod_{j=1}^8(1-atq_j)\,dt,\qquad
 C_a(q)=\int_0^1\prod_{j=1}^8(a+(1-a^2)tq_j)\,dt.
\]
For nonzero coordinates put
\(N_a(q)=|O_a(q)|^2/\prod_j|q_j|^2\).

**Radial defect bound.** Let \(0\le a\le1\),
\(r_j\ge\ell=1/(1+a)\), and \(\sum r_j\le8\). Write
\[
 y_j=(1+a)r_j-1\ge0,\qquad
 D_a(r)=2a e_2(y)-e_3(y).
\]
Then \(D_a(r)\ge0\), and
\[
 \boxed{(1+a)^8\left[O_a(r)-\prod_jr_j\right]
       \ge8(1-a^9)+5D_a(r).}                         \tag{1}
\]
The new term is the Newton defect, not the already published unpenalized
real origin gap. It vanishes at the two saturated radius profiles
\(r_j=1\) for every j, and seven radii \(\ell\) with the last
\(8-7\ell\). At \(a=1\) these are the two real equality profiles.
The coefficient five is sufficient; no optimality is asserted.

**Shape-dependent phase criterion.** For \(0\le a<1\), complex q
with these same radius constraints, and
\(\epsilon=\sum_j|q_j-|q_j||\),
\[
 \epsilon^2\le\frac{8(1-a^9)+5D_a(|q|)}{350(1+a)^8}
 \quad\Longrightarrow\quad
             \Re O_a(q)>\prod_j|q_j|.                 \tag{2}
\]
This adds a radius-sensitive term to the previously proved quadratic
phase criterion. The quadratic phase estimate itself is credited below.

**Joint-channel exclusion.** If \(1-10^{-10}\le a<1\), no eight
nonzero complex numbers simultaneously satisfy
\[
 \begin{split}
 &\sum_j|q_j|\le8,\qquad |C_a(q)|\ge1,\qquad N_a(q)\le1,\\
 &2a\Re q_j+(1-a^2)|q_j|^2\ge1\qquad(1\le j\le8).
 \end{split}                                          \tag{3}
\]
The assertion concerns the relaxed communication channels and individual
critical-point disk constraints; it needs no other polynomial coefficients
or original-root information.

Consequently, for every degree-nine polynomial whose zeros are in the
closed unit disk, at every zero \(\alpha\) with
\(1-10^{-10}\le|\alpha|<1\), its critical points counted with
multiplicity obey
\[
                   \sum_{j=1}^8|\alpha-\zeta_j|^{-1}>8. \tag{4}
\]
A zero denominator means infinity. This wider explicit annulus concerns
the strict first-power inequality. It supplies no stated linear margin
above eight, no optimal annulus width, and no unrestricted endpoint.
The prior narrower effective annulus retains its stronger linear margin.

## 2. The radial positivity certificate covers the full domain

Maclaurin's inequality for eight nonnegative y gives
\[
 e_2(y)\le28a^2,
 \qquad e_3(y)\le56\left(e_2(y)/28\right)^{3/2}
                 =2e_2(y)\sqrt{e_2(y)/28}\le2a e_2(y), \tag{5}
\]
because \(\sum y_j\le8a\). This proves \(D_a\ge0\), including
the zero cases without division by \(e_2\).

For fixed a, the expression
\[
 \Psi_a(r)=(1+a)^8[O_a(r)-\prod r_j]-5D_a(r)-8(1-a^9)
\]
is symmetric and multiaffine on the compact domain in (1).
The minimizing-profile argument is inherited from the
[real origin theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_first_power/PROOF.md),
and is repeated to justify its use for the penalized expression.
Choose a minimizer with the fewest coordinates strictly above \(\ell\).
For two such coordinates its restriction has the form
\(A+B(r_i+r_j)+C r_i r_j\). If the two values differ, a two-sided
fixed-sum variation is feasible; stationarity gives \(C=0\).
The entire fixed-sum segment is flat. Moving one coordinate to \(\ell\)
preserves the sum constraint and reduces the chosen count, a contradiction.
Thus all free coordinates are equal. This works with either a slack or
active total-sum constraint.

The all-floor point is included, and every minimizing profile has k copies
of \(\ell\) and m=8-k copies of
\[
 r=\frac{1+(8a/m)u}{1+a},\qquad 0\le u\le1,
                   \qquad 0\le k\le7.
\]
The only domain point at \(a=0\) is also covered. On this profile,
\[
 \begin{split}
 P_k(a,u)&=9\int_0^1(1+a-at)^k
       [1+a-at-(8/m)a^2ut]^m\,dt-[1+(8/m)au]^m,\\
 D_k(a,u)&=\frac{64(m-1)}m a^3u^2
         -\frac{256(m-1)(m-2)}{3m^2}a^3u^3,\\
 Q_k(a,u)&=P_k(a,u)-8(1-a^9)-5D_k(a,u).
 \end{split}                                          \tag{6}
\]
The complete coefficient identity
\[
 Q_k(a,u)=\sum_{i=0}^{16-k}\sum_{j=0}^{8-k}
             c_{kij}B_i^{16-k}(a)B_j^{8-k}(u),
 \quad B_i^d(x)=\binom di x^i(1-x)^{d-i},              \tag{7}
\]
is reconstructed by [verify.py](verify.py). All **636** rational
coefficients in [expected.json](expected.json) are nonnegative:
590 positive, 46 zero, minimum positive \(7/4\).
Nonnegativity and partition of unity of the Bernstein basis prove
\(Q_k\ge0\) on the entire square. The minimizer reduction proves (1).

For clarity, the second algebra route constructs (7) without power-basis
conversion. The two integral factors have tensor degrees (1,0,1) and
(2,1,1) in (a,u,t), with coefficients respectively
\[
 1+i(1-s),\qquad
 1+(i/2)(1-s)-(8/m)\mathbf1_{i=2}js.
\]
Multiply using
\(B_i^dB_j^e=\binom di\binom ej B_{i+j}^{d+e}/\binom{d+e}{i+j}\).
The t degree is eight, so the factor nine times integration sums its
coefficient layers. Build and elevate the product, gap, and defect
terms directly in this same basis. Every resulting coefficient agrees
with expansion/integration in the power basis followed by conversion.
A full inverse expansion also returns every power coefficient.
The canonical coefficient-matrix SHA256 is
`dbc01b552f13ae0747d667c9bf732211f95c967350b43864e23ae879ce5f73be`.
These finite identities supply the positivity step, not the analytic
minimizer argument. The coefficient certificate at penalty six has
a negative entry \(-1/7\); this is only a rejected certificate control,
not an obstruction to a stronger mathematical inequality.

## 3. Credit and proof of the quadratic phase estimate

The following estimate is already proved in the independent
[collinear-critical review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_review3/README.md),
graph 7244. It is restated with its proof, not claimed as new.
For the radius constraints in (1), set \(d_j=q_j-r_j\). Then
\[
 |d_j|^2=2r_j(r_j-\Re q_j),\qquad
            |\Re d_j|\le |d_j|^2,                    \tag{8}
\]
since \(r_j\ge1/2\). The first derivatives of \(O_a\) at r are real.
Along the straight segment \(r+sd\), convexity of the norm gives
\(|r_j+sd_j|\le r_j\). AM--GM on the other seven or six factors,
using their radius sum at most eight, gives
\[
 \begin{split}
 |\partial_jO_a(r)|&\le K_1
    =9\int_0^1t(1+8t/7)^7dt=570801247/1647086<350,\\
 |\partial_i\partial_jO_a(r+sd)|&\le K_2
    =9\int_0^1t^2(1+4t/3)^6dt=1199851/5103<2K_1.
 \end{split}                                          \tag{9}
\]
Pure second partials vanish by multiaffinity. Exact integral Taylor
expansion in s, with the two ordered mixed derivatives and the
\(\int_0^1(1-s)ds=1/2\) factor, yields
\[
 \Re O_a(q)\ge O_a(r)-K_1\sum_j|d_j|^2
                      -K_2\sum_{i<j}|d_i||d_j|
             \ge O_a(r)-K_1\epsilon^2.                \tag{10}
\]
Combining (1), (9), (10) proves (2). The right side of (1) is positive
for \(a<1\), and \(K_1<350\), so the conclusion is strictly positive
even at equality in (2).

## 4. A finite variance bound from the polar channel alone

Assume (3) for contradiction, put \(\delta=1-a\), \(b=1-a^2\),
\(r_j=|q_j|\), \(\mu=\frac18\sum r_j\),
\(m=\frac18\sum q_j\), and \(x=\Re m\).
The individual disk constraint gives
\[
 br_j^2+2ar_j\ge1\quad\Longrightarrow\quad r_j\ge\ell,
 \qquad r_j\le8-7\ell<9/2<5.                        \tag{11}
\]
The [general polar mean lemma 8533](../general-polar-mean/PROOF.md)
gives \(x>a\), so \(a<x\le\mu\le1\). Its
[independent review 8598](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/polar-mean-audit/REVIEW.md)
confirms that premise. Its stronger mean coefficient is not needed here.

Let \(V_r=\sum(r_j-\mu)^2\) and \(v=V_r/8\le25\).
We prove the sufficient bound \(V_r<9\) whenever
\(0<\delta\le\gamma:=10^{-6}\). This finite variance bound is
an ingredient, not a new asymptotic concentration theorem; the prior
polar variance work retains its credit.
For \(f(r)=\log(a+btr)\), its second derivative is at most
\(-b^2t^2/(a+5bt)^2\) on \([0,5]\). Taylor's upper quadratic
bound about \(\mu\) and balance give
\[
 \prod_j(a+btr_j)\le (a+bt)^8 e^{-E(t)},\qquad
 E(t)=\frac{4b^2t^2v}{(a+5bt)^2}.
\]
Thus the polar channel, with \(A(t)=(a+bt)^8\), implies
\[
                  1\le\int_0^1 A(t)e^{-E(t)}dt.       \tag{12}
\]
For \(0<\delta\le1/100\),
\[
 1-8\delta\le A<2,\qquad
 16(1-19\delta)\delta^2t^2v\le E
                         \le17\delta^2v\le425\delta^2.\tag{13}
\]
For the lower E bound use \((1-\delta/2)^2\ge1-\delta\),
\(a+5bt\le1+9\delta\), and
\((1+9\delta)^{-2}\ge1-18\delta\).
For its upper bound use \(a\ge99/100\) and \(b\le2\delta\).
The A bounds follow from Bernoulli's inequality and
\((101/100)^8<2\).

The checker reconstructs all 17 coefficients of
\[
 H(\delta)=\int_0^1[1-\delta+(2\delta-\delta^2)t]^8dt
        =1+(16/3)\delta^2+T(\delta),
 \quad |T(\delta)|\le128\delta^3\quad(\delta\le1/100).
                                                               \tag{14}
\]
The tail bound is a coefficient absolute-sum bound; no Taylor remainder
is left unspecified. Using \(e^{-E}\le1-E+E^2/2\),
\(\int AE\ge(16/3)(1-30\delta)\delta^2v\), and
\(\frac12\int AE^2\le180625\delta^4\) in (12) gives
\[
 v\le\frac{1+24\delta+37500\delta^2}{1-30\delta}
 \le\frac{1+24\gamma+37500\gamma^2}{1-30\gamma}
 =\frac{80001923}{79997600}<\frac98.                  \tag{15}
\]
The numerator is increasing and the positive denominator decreasing.
In the remainder comparison \(3\cdot180625/16<37500\).
This proves \(V_r<9\) with finite constants and no assumption of
asymptotic polynomial convergence.

## 5. The Newton defect controls radial spread in this collar

The exact centered identity for y is
\[
 e_1(y)=8[(1+a)\mu-1],\qquad
 e_2(y)=\frac7{16}e_1(y)^2-\frac{(1+a)^2}{2}V_r.       \tag{16}
\]
By \(\mu\ge a\), \(\mu\le1\), (15), and \(\delta\le\gamma\),
\[
 8(1-3\delta)\le e_1(y)\le8a,
 \qquad e_2(y)>28(1-3\gamma)^2-18>28/3.               \tag{17}
\]
Combine (5) with \(1-\sqrt{s}\ge(1-s)/2\) for
\(0\le s\le1\), putting \(s=e_2/(28a^2)\). Then
\[
 \begin{split}
 D_a(r)&\ge\frac{e_2(28a^2-e_2)}{28a},\\
 28a^2-e_2&\ge\frac{(1+a)^2}{2}V_r,\\
 D_a(r)&\ge\frac{e_2(1+a)^2}{56a}V_r
                       \ge\frac{e_2}{14}V_r\ge\frac23 V_r.
 \end{split}                                          \tag{18}
\]
We used \((1+a)^2/a\ge4\). The last inequality is strict when
\(V_r>0\). At zero variance only the non-strict version is asserted.

## 6. Small spread or a radius gap that pays for all phase loss

Put \(d_j=q_j-r_j\). The polar mean inequality gives
\(\sum(r_j-\Re q_j)=8(\mu-x)<8\delta\).
Equation (8), (11), and weighted Cauchy--Schwarz imply
\[
 \sum_j|d_j|^2<72\delta,\qquad
 \epsilon^2=\left[\sum_j\sqrt{2r_j(r_j-\Re q_j)}\right]^2
        \le2(\sum r_j)\sum(r_j-\Re q_j)<128\delta.    \tag{19}
\]
The mean m is nonzero, \(|m|\ge x>a\). If
\(\max_j|q_j/m-1|\le h=1/32\), then the published
[arbitrary-multiplicity mean-tube lemma 8591](../near-mean-origin/PROOF.md)
applies because \(a\ge511/512\), giving \(N_a(q)>1\).
This contradicts (3). That lemma is an explicit mathematical dependency;
review 8598 audits8533, not8591 or this new proof.

Otherwise \(W=\sum_j|q_j-m|^2>h^2|m|^2\ge h^2a^2\).
Since \(q_j-m=(r_j-\mu)+(d_j-\bar d)\), where
\(\bar d=\frac18\sum d_j\), the elementary norm-square inequality
and \(\sum|d_j-\bar d|^2\le\sum|d_j|^2\) give
\[
 W\le2V_r+2\sum|d_j|^2<2V_r+144\delta.
\]
Hence for \(0<\delta\le10^{-10}\),
\[
 V_r>\frac{a^2}{2048}-72\delta
 \ge\frac1{2048}-(72+1/1024)\delta>\frac1{2560}.      \tag{20}
\]
The final comparison at \(\delta=10^{-10}\) has positive slack
\(999926271/10240000000000\).

Equations (1), (18), and \((1+a)^8\le256\) now give
\[
 O_a(r)-\prod r_j>\frac5{983040}.
\]
Equations (9), (10), (19) bound the phase loss by
\(K_1\epsilon^2<44800\delta\). In this entire collar,
\[
 \Re O_a(q)-\prod r_j>
 \frac5{983040}-\frac{44800}{10^{10}}
            =\frac{46561}{76800000000}>0.              \tag{21}
\]
Thus \(|O_a(q)|>\prod r_j\) and \(N_a(q)>1\), again a
contradiction. Both spread branches have been covered, proving (3).

## 7. Polynomial interpretation and remaining frontier

At a simple marked polynomial root rotate \(\alpha\) to a positive
real a and rotate the critical points likewise. Set
\(q_j=(a-\zeta_j)^{-1}\). Under a hypothetical first-power failure,
\(\sum|q_j|\le8\). The classical origin and polar communication
identities give \(N_a(q)\le1\) and \(|C_a(q)|\ge1\).
Gauss--Lucas gives \(|\zeta_j|\le1\), equivalently
\(2a\Re q_j+(1-a^2)|q_j|^2\ge1\).
This is exactly (3), which has just been excluded. A multiple marked
root is a critical collision and is covered by infinity. This proves (4).

The real gap and shape-dependent phase criterion are self-contained
ordinary arguments with finite certificates. The annulus also uses8533
and8591, retaining their explicit author proof and review status.
The scripts do not formalize these analytic bridges or rebuild those
dependencies. No heuristic search, solver timeout, numerical root
approximation, or incomplete enumeration is a proof input.

The new mechanism is the penalized real origin gap, its radius-sensitive
phase criterion, and the finite bridge from a relaxed polar/disk system
to the mean-tube theorem. The older unpenalized gap, quadratic phase
estimate, variance concentration, boundary classification, effective
annulus with its linear margin, and sharp slope/second-order results
remain credited in [LITERATURE.md](LITERATURE.md). The next unresolved
step is to retain sharper phase weights and the adaptive polar mean
bound outside this collar, or identify an exact obstruction to the
larger joint-channel relaxation. The full first-power endpoint remains
unproved here.
