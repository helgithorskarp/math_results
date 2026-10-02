# Positive near-middle support without centering

Author **six-downset-2**, role **researcher**, 2026-10-02. This is an
ordinary exact author proof, unformalized and independently unreviewed.
The written counting, PSD/kernel, moment, induction and Chernoff arguments
supply unbounded coverage. Finite exact computations validate identities
and conventions; they do not replace those arguments.

## Quantified statement

For integer n>=6 put

\[
 D_n=\{A\subseteq[n]:|A|\le n-2\},\quad
 F=D_n\setminus\{\varnothing\},\quad T=2^{n-1},
\]
\[
 N=2T-n-1,\quad s=T-n,\quad h=T-1=N-s,\quad q=\binom n2.
\]

An H matrix here is real symmetric on **every actual member of D_n**,
including its empty vertex and permitted loop, and satisfies

\[
 M\mathbf1=\mathbf1,\quad M_{AB}=0\quad(A\cap B\ne\varnothing),
 \quad L=hM+sI\succeq0.                                    \tag{1}
\]

The additional cap is M<=I in Loewner order, equivalently L<=NI.
It is an extra hypothesis; it is not spectral inertia Conjecture I.
No centering, invariance, rationality, entry sign, rank, strict gap or
bound on the actual empty-row defect is assumed.

For integer

\[
 2\le k\le\lfloor(n-2)/2\rfloor                             \tag{2}
\]

let P_(n,k) be the **unordered original pairs** of disjoint nonempty
sets with both sizes>k and A union B a proper subset of[n]. Their sizes
automatically lie in the bulk k+1,...,n-k-1. For bulk a define

\[
 v_a=\max\left(0,\frac54-\frac{(2a-n)^2}{4n}\right),\quad
 \mu=\frac{(2n-5)^2}{16},\quad f_a=a-v_a,\quad
 \rho_{ab}=1-\frac{f_af_b}{\mu}\quad(a+b<n).                \tag{3}
\]

Set

\[
 B_{n,k}=\sum_{a=3}^k a^2\binom na,\quad
 A_{n,k}=4q+B_{n,k}=\sum_{a=2}^k a^2\binom na,
\]
\[
 S_{n,k}=\sum_{a=k+1}^{n-k-1}\binom na v_a^2,\quad
 R_n=s-12n^2,
\]
\[
 C_{n,k}=nh-2qs+(h-s^2/h)A_{n,k}+(n-1)S_{n,k},\quad
 \eta_{n,k}=C_{n,k}+\mu(4s-4),\quad
 \delta_{n,k}=-\eta_{n,k}/(2h\mu).                          \tag{4}
\]

**General certificate.** All weights in(3) satisfy 0<rho_ab<1.
At any n,k in(2) for which eta_(n,k)<0, every real capped H satisfies

\[
 \boxed{\sum_{\{A,B\}\in P_{n,k}}\rho_{|A|,|B|}M_{AB}
                 \ge\delta_{n,k}>0.}                     \tag{5}
\]

Its **positive original entry mass** on P_(n,k) is strictly greater
than delta_(n,k); some original entry there is positive.

**Unbounded sufficient criterion.** For every integer n>=12 and k in(2),

\[
 \boxed{6B_{n,k}\le R_n}                                   \tag{6}
\]

implies eta_(n,k)<-R_n/3<0 and delta_(n,k)>R_n/(6h mu).
When n>=16 this also gives positive original mass>1/(2n^2).

**Near-middle consequence.** For every integer n>=24, every real capped H
has a positive original entry on a proper disjoint pair with

\[
 \boxed{\min(|A|,|B|)>
        n/2-\sqrt{(n/2)\log(4n^2)}.}                       \tag{7}
\]

The logarithm is natural. With k the floor of the right side, total
positive original mass on P_(n,k) is **greater than1/(2n^2)**.
These are necessary conditions if a capped H exists, not constructions.
They exclude the support face permitting only complements and proper
nonempty pairs touching a size at most k, even with all those low-touching
couplings arbitrary and with an unrestricted actual empty row.

Exact weighted sums in(6) give additional finite consequences:

| n | Largest k certified by(6) | Forced integer minimum size of both sets |
| --- | --- | --- |
| 24 | 5 | 6 |
| 32 | 7 | 8 |
| 64 | 17 | 18 |
| 128 | 41 | 42 |
| 256 | 93 | 94 |
| 512 | 203 | 204 |

The next integer fails **this sufficient scalar criterion** in each row.
No optimal cutoff, best mass, sharp starting order, matching positive
construction, exhaustive classification or general H/I resolution is
asserted. General H on this near-cube family was already known.

## Prior literature and precise increment

The primary problem remains
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [version record](https://arxiv.org/abs/2609.28404), checked live
2026-10-02, still lists v1, 2026-09-23. It proves the classical Chvatal
conclusion and states separate open spectral H/I conjectures.

Nonempty-core and actual-empty conventions are credited to
[the structural certificates](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
and the forced-star kernel to
[the six-element proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
Their necessary implications are rederived below. The
[ordinary near-cube theorem](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md)
and the [n10 noncentered S2 cap](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_multiple_pair_caps/PROOF.md)
retain distinct scopes.

The [centered active-layer theorem9201](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_active_layer_growth/PROOF.md)
already established a near-half growth scale. Its independent
[review9245 by six-reviewer-3](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/active-support-audit/REVIEW.md)
proved the **same log(4n^2) threshold** as(7), at n>=64, under centering,
and a signed original-coordinate functional bound. The growth scale,
logarithm constant and use of original-coordinate functionals are prior
art. That audit explicitly left removal of centering open.

[Result9365](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_pair_separation/PROOF.md)
removed centering for the fixed n16 S2 separation. Its
[star-only affine completion](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_pair_separation/affine.py)
is copied here with credit solely for validation.
[Result9424](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_uniform/PROOF.md)
proved positive original middle support without centering at every
n>=11, but only for the fixed low cutoff k=2. Its clipped profile, two-test
method, k2 scalar and original-coordinate signs are the basis of this proof.
The new increment is the **general-k cancellation and exact constant**,
the weighted sufficient criterion, and **positive original near-middle
support and mass without centering**, uniformly from n24.
The fresh independent [review9450](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/near-cube-cap-audit/REVIEW.md)
and [review9455](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/uniform-support-audit/REVIEW.md)
now confirm9424. They additionally prove an ordinary S2 spectral-gap
bound and a changed-profile n11 mass improvement, respectively. Those
distinct k2 refinements provide baseline provenance, not premises for
the new general-k cancellation or growth bridge here.
Neither the review of9201 nor any prior review is a verdict on this new
proof. No historical priority claim is made.

## Necessary core, cardinality kernel and complement deficits

Every point star has s members. Put C=L_(F,F)-J. Because L1=N1 and L is
real symmetric PSD, L-J is PSD: it vanishes on1 and equals L on1-perp.
The two necessary nonempty forms are therefore

\[
 C\succeq0,\qquad U=NI_F-J_F-C\succeq0.                    \tag{8}
\]

The second is a principal restriction of the assumed cap NI-L.
Regularity fixes the actual empty entries as

\[
 L_{\varnothing,A}=1-(C\mathbf1)_A,\quad
 L_{\varnothing,\varnothing}=1+\mathbf1^TC\mathbf1.         \tag{9}
\]

There is no C1=0 premise. The empty loop must not be deleted.

For the full indicator y_i of a point star, support and diagonal give
y_i^T L y_i=s^2. Thus y_i-(s/N)1 has zero L energy. A zero-energy vector
of a real PSD matrix is a kernel vector, hence Ly_i=s1. Restricting to F,
C annihilates the actual star indicator x_i. It therefore annihilates
the cardinality vector a_A=|A|=sum_i(x_i)_A:

\[
 Ca=0.                                                     \tag{10}
\]

For disjoint nonempty distinct vertices write beta_AB=hM_AB. As a literal
matrix on F,

\[
 C=sI-J+\mathcal B,\quad
 \mathcal B_{AB}=\beta_{AB}\text{ on disjoint distinct pairs, zero otherwise}.
                                                               \tag{11}
\]

For each bulk vertex its complement is also an actual bulk vertex.
Define z_A=s-beta_(A,A^c). The C energy of e_A-e_(A^c) is2z_A, so

\[
 z_A\ge0,\qquad z_A=z_{A^c}.                                \tag{12}
\]

These are individual original entries; no averaging or orbit sign is used.

## General-k tests and complete original identity

Low sizes are1,...,k; bulk sizes are k+1,...,n-k-1; high sizes are
n-k,...,n-2. Set K=sum_(a=2)^k binom(n,a), and
G=sum_bulk binom(n,a)=2s-2-2K. On original F take

\[
 \ell_A=\begin{cases}0&|A|\le k,\\1&A\text{ bulk},\\2&A\text{ high},\end{cases}
 \quad
 u_A=\begin{cases}|A|&|A|\le k,\\v_{|A|}&A\text{ bulk},\\
                 s(n-|A|)/h&A\text{ high}.\end{cases}      \tag{13}
\]

A high vertex has no disjoint bulk or high partner. Its complement touches
low, where ell is zero. Bulk complements contribute sG-sum_bulk z_A to
the lower test. The remaining nonzero disjoint products of ell are exactly
the proper pairs in P_(n,k), all with product1. Hence

\[
 \ell^TC\ell=4s-4-\sum_{A\,\mathrm{bulk}}z_A
                 +2\sum_{\{A,B\}\in P_{n,k}}\beta_{AB}.     \tag{14}
\]

Its constant is s(G+4K)+sG-(G+2K)^2=4s-4, since G+2K=2s-2.

Use(10) in the upper test:

\[
 u^TUu=u^T(NI-J)u-(u-a)^TC(u-a).                           \tag{15}
\]

The shifted vector vanishes at **every low original vertex**. At bulk
size a it equals -f_a. A high vertex has no disjoint nonzero shifted
partner. Thus all disjoint original entries touching low cancel, whatever
their signs, sizes, centering defects or permutation dependence.
Write w_a=f_af_(n-a)=v_a^2-nv_a+a(n-a). Expanding(15) gives

\[
 u^TUu=C_{n,k}+\sum_{A\,\mathrm{bulk}}w_{|A|}z_A
     -2\sum_{\{A,B\}\in P_{n,k}}f_{|A|}f_{|B|}\beta_{AB}.    \tag{16}
\]

Here is a direct check of the general constant, retaining the missing
n-1 layer. Put V=sum_bulk binom(n,a)v_a and
J=sum_(a=2)^k a binom(n,a). Then

\[
 U_0=\sum_F u_A=n+(1+s/h)J+V,\qquad
 \sum_F(u_A-|A|)=U_0-ns,
\]
\[
 \sum_F u_A^2=n+(1+s^2/h^2)A_{n,k}+S_{n,k}.
\]

Bulk complement symmetry gives sum_bulk a binom(n,a)=nG/2 and
sum_bulk a v_a binom(n,a)=nV/2. The sum of the bulk shifted norm and its
ordered complement product is n^2G/2-2nV+2S_(n,k).
The remaining high shifted norm is

\[
 H_2=\sum_{a=2}^k\binom na\{sa/h-(n-a)\}^2
     =(1+s/h)^2A_{n,k}-2n(1+s/h)J+n^2K.
\]

The constant in(15), setting bulk complement weights to s and bulk
proper weights to zero only to evaluate the constant term, is

\[
 N\{n+(1+s^2/h^2)A_{n,k}+S_{n,k}\}-U_0^2
 -s\{n^2G/2-2nV+2S_{n,k}+H_2\}+(U_0-ns)^2.               \tag{17}
\]

All V and J terms cancel. Substitute G=2s-2-2K and N=s+h=2s+n-1;
the A coefficient is h-s^2/h, the S coefficient is n-1, and the remaining
term is nh-n(n-1)s=nh-2qs. This proves(4).
The substitution is a constant-term evaluation, not a feasible-matrix
assertion. The z and proper-pair coefficients in(16) follow directly
from the original expansion(11).

Replacing each high root sa/h by an arbitrary r_a in(17) changes its
constant by exactly h sum_(a=2)^k binom(n,a)(r_a-sa/h)^2.
Thus the rational roots in(13) minimize this scalar within the fixed
test profile; no global certificate optimality is claimed.

The actual quadratic sum Phi=u^TUu+mu ell^TC ell is nonnegative.
Combining(14),(16) gives the complete original identity, valid before
any support restriction:

\[
 \boxed{\Phi=\eta_{n,k}
 -\sum_{A\,\mathrm{bulk}}(\mu-w_{|A|})z_A
 +2h\mu\sum_{\{A,B\}\in P_{n,k}}\rho_{|A|,|B|}M_{AB}.}      \tag{18}
\]

## Signs and positive mass

Put d=a-n/2. If v_a>0, v_a=5/4-d^2/n and
w_a=n^2/4-5n/4+v_a^2<=mu. If v_a=0, d^2>=5n/4 and
w_a=a(n-a)<=n^2/4-5n/4<mu. Thus mu-w_a>=0 on every bulk layer.

For a>=3, f_a>=a-5/4>0, and

\[
 f_a=\min\left(a,\frac{a^2}{n}+\frac n4-\frac54\right).
\]

Both functions inside the minimum are strictly increasing for a>0,
so their minimum is strictly increasing. For every proper bulk pair
b<n-a, giving 0<f_af_b<f_af_(n-a)=w_a<=mu.
This proves every strict weight sign in(3), including clipped and central
layers. With(12),(18) it proves(5) whenever eta<0.
The signed weighted sum is at most its weighted positive part, strictly
smaller than the unweighted positive original mass because every rho<1
and the positive weighted lower bound guarantees a positive entry.
This proves the strict mass conclusion.

## Weighted sufficient criterion at all n>=12

The k2 constant is exactly the credited9424 scalar, since A_(n,2)=4q.
Completing its rational root square gives

\[
 \eta_{n,2}=nh+q(8h-10s)+(n-1)S_{n,2}+\mu(4s-4)
                         -4q(n-1)^2/h.                    \tag{19}
\]

The full binomial centered moments, proved by expanding the sum of n
independent uniform signs and counting surviving even-index products, are

\[
 \sum_{a=0}^n\binom na(a-n/2)^2=2^n n/4,\quad
 \sum_{a=0}^n\binom na(a-n/2)^4=2^n(3n^2-2n)/16.
\]

Clipping negative values to zero and discarding layers reduces a sum of
squares. Therefore

\[
 S_{n,2}\le\sum_{a=0}^n\binom na\{5/4-(a-n/2)^2/n\}^2
                       =(s+n)(9/4-1/(4n)).
\]

Substitute this bound in(19), discarding the last nonpositive term:

\[
 \eta_{n,2}\le F_n=-s\frac{3n-15-1/n}{4}
       +4n^3-\frac{23n^2}{4}+\frac{11n}{2}-6.              \tag{20}
\]

For all integer n>=12, R_n>0. The base is s_12-12*12^2=308>0.
Since s_(n+1)=2s_n+n-1, the induction difference is
12n^2-23n-13=12t^2+265t+1439>0 for n=12+t, t>=0.
Moreover (3n-15-1/n)/4>n/3 because
5n^2-45n-3=5t^2+75t+177>0, and the cubic remainder in(20) is
less than4n^3 because 23n^2-22n+24=23t^2+530t+3072>0.
Hence

\[
 F_n<-(n/3)R_n\quad(n\ge12).                               \tag{21}
\]

The exact general-k difference is

\[
 \eta_{n,k}-\eta_{n,2}
  =(h-s^2/h)B_{n,k}+(n-1)(S_{n,k}-S_{n,2}).               \tag{22}
\]

Here S_(n,k)<=S_(n,2), and
0<h-s^2/h=(n-1)(h+s)/h<2(n-1).
Equations(20)-(22) therefore give

\[
 \eta_{n,k}<-(n/3)R_n+2(n-1)B_{n,k}.
\]

Under(6) the last expression is at most -R_n/3<0, proving the criterion
and its explicit delta margin. This covers every asserted n,k;
no finite profile fit or truncated search supplies the unbounded bridge.

For every integer n>=16, a stronger induction gives

\[
 R_n>3T/4.                                                 \tag{23}
\]

Indeed a_n=T/4-n-12n^2=2^(n-3)-n-12n^2 has base a_16=5104>0,
and a_(n+1)-2a_n=12n^2-23n-13=12t^2+361t+2691>0 for n=16+t.
Since h<T and 0<mu<n^2/4, the delta margin now implies

\[
 \delta_{n,k}>R_n/(6h\mu)>1/(2n^2)                         \tag{24}
\]

whenever(6) holds and n>=16.

## Chernoff consequence and exact endpoint domain

For X~Bin(n,1/2), its centered exponential moment is
E exp(-lambda(X-n/2))=cosh(lambda/2)^n.
For every real z, cosh z<=exp(z^2/2): compare the nonnegative power-series
coefficients using (2j)!>=2^j j!, whose factors prove it for every j.
Markov and lambda=4d/n consequently give

\[
 \Pr(X\le n/2-d)\le\exp(-2d^2/n)\qquad(d\ge0).              \tag{25}
\]

Put theta=n/2-sqrt((n/2)log(4n^2)) and k=floor(theta).
We check all needed integer endpoints. For real x>=24 define

\[
 H(x)=x/2-4+8/x-\log(4x^2).
\]

Since e>sum_(j=0)^3 1/j!=8/3 and (8/3)^8>2304, log(4*24^2)<8.
Thus H(24)>1/3. Also H'(x)=1/2-2/x-8/x^2>=29/72>0 for x>=24.
This proves (n/2-2)^2>(n/2)log(4n^2), hence theta>2 for all n>=24.
The square root exceeds1: e<3 by its series, so log(4n^2)>1.
Thus theta<n/2-1, and the integer k lies in precisely domain(2).
These endpoint arguments use exact rational inequalities; floating
logarithms and square roots are not proof inputs.

For a<=k<n/2, a^2<=n^2/4. Since n/2-k is at least the deviation in
theta, (25) gives

\[
 B_{n,k}\le\frac{n^2}{4}\sum_{a=0}^k\binom na
       \le\frac{n^2}{4}\frac{2^n}{4n^2}=T/8.
\]

Consequently 6B_(n,k)<=3T/4<R_n by(23). Apply(5),(24).
An integer minimum size>k is at least k+1, strictly greater than theta,
including when theta is integral. This proves(7) and its mass assertion
for **every** n>=24.

## Reproduction and trust boundary

[certificate.py](certificate.py) regenerates profiles, exact constants,
weights, conditional floors and the greatest cutoff certified by(6).
[verify.py](verify.py) checks the whole full-star affine identity on606
independent free directions at19(n,k) pairs, using direct singleton
completion and independent exact RREF in [affine.py](affine.py),
byte-copied with credit from9365. Every original class coefficient is
checked, including cancellations of low-touching proper pairs and
complements. Necessary physical layer forms in [model.py](model.py)
are copied from9424; no harmonic completeness is used.

The constant is independently computed from literal layer norms,
without feeding the closed formula into that calculation.
Varying high roots checks the exact squared excess.
At n6 and n8, all64,258 actual original entries are checked, including
the empty loop, regularity, original support, each point star and both
scalar pairings; n8 uses both k2 and k3.
These are affine controls, not PSD examples.

A noninvariant signed mixed-cardinality trade at(n,k)=(16,3) changes32
ordered original positions. On each of two disjoint eight-point blocks,
use the signed indicator vector +{four points}+{other four points}
-{first three points}-{remaining five points}. Each vector has zero sum
and annihilates every individual point star. Their symmetric cross-product
preserves stars, rows, diagonals and allowed support.
Its two-test scalar change and weighted omitted-pair change both equal
**9063/128**, with the size-three terms cancelling. No original matrix
of order65,519 is materialized and no PSD/cap feasibility is asserted.

All unordered proper-pair counts are also checked against an independent
ternary-assignment inclusion-exclusion count. Full exact binomial moment
sums validate the counted moments at the recorded orders.
The checker records positive induction coefficients and rational logarithm
endpoint witnesses. The written proofs above, rather than those finite
controls, supply the analytic and completeness bridges.
The exact tail table checks every next failing integer solely for(6).

The complete compact record [expected.json](expected.json) must agree in
normal and optimized Python modes. The checker uses explicit conditions,
not assert statements. No solver, numerical spectrum, floating proposal,
large private corpus, incomplete enumeration, timeout, memory kill,
external data or transferred review verdict is a mathematical premise.
The trust boundary is inspected stdlib Fraction/integer arithmetic plus
ordinary real PSD/kernel, counting, moment, induction, calculus and
Chernoff arguments. No proof assistant or independent review of this
new theorem is claimed.
