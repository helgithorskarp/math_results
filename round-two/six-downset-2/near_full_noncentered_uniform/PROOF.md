# Positive middle support in every capped near cube from eleven points

Author **six-downset-2**, role **researcher**, 2026-10-02. This is an
ordinary exact author proof, unformalized and independently unreviewed.
The portable arithmetic checks validate its identities and endpoint;
the written induction supplies its unbounded coverage.

## Statement

For an integer n>=11 put

\[
 D_n=\{A\subseteq[n]:|A|\le n-2\},\quad F=D_n\setminus\{\varnothing\},
 \quad N=2^n-n-1,\quad s=2^{n-1}-n,\quad h=N-s=2^{n-1}-1,
 \quad q=\binom n2.
\]

An H matrix here is a real symmetric matrix on **every actual member of D**,
including the empty vertex and its permitted loop, satisfying

\[
 M\mathbf1=\mathbf1,\quad M_{AB}=0\ (A\cap B\ne\varnothing),
 \quad L=hM+sI\succeq0.
\]

The additional cap is M<=I in Loewner order, equivalently L<=NI.
It is an extra hypothesis; it is not inertia Conjecture I.
Let P be the unordered disjoint original pairs with both sizes>=3 and
A union B a proper subset of[n]. For 3<=a<=n-3 define

\[
 v_a=\max\left(0,\frac54-\frac{(2a-n)^2}{4n}\right),\quad
 \mu=\frac{(2n-5)^2}{16},\quad f_a=a-v_a,\quad
 \rho_{ab}=1-\frac{f_af_b}{\mu}\quad(a,b\ge3,\ a+b<n).
                                                        \tag{1}
\]

Write

\[
 S_n=\sum_{a=3}^{n-3}\binom na v_a^2,\quad r=2s/h,
\]
\[
 \eta_n=nh+q\{h(4+r^2)-s(2+4r)\}+(n-1)S_n
                      +\mu(4s-4),\qquad
 \delta_n=-\frac{\eta_n}{2h\mu}.                         \tag{2}
\]

**Theorem.** For every integer n>=11, eta_n<0, all the weights in(1)
satisfy 0<rho_ab<1, and every real capped H matrix on D_n satisfies

\[
 \boxed{\ \sum_{\{A,B\}\in P}\rho_{|A|,|B|}M_{AB}
                  \ge\delta_n>0.\ }                      \tag{3}
\]

Consequently the positive original entry mass on P is **strictly greater
than delta_n**, and some original entry on P is positive. In particular
there is no capped H supported, among nonempty pairs, only on complements
and proper-union pairs touching a singleton or a two-set, called S2 here.
No invariance, centering, rationality, individual entry sign, rank,
strict spectral gap or bound on the empty-row defect is assumed.

At n=11, S_11=4533/2 and eta_11=-1535/93. At n=16 the new mass floor
is larger than1/64; these are explicit bounds, with no optimality assertion.
The older noncentered n10 S2 cap is compatible with this result. In combination
with that credited existence result, **10 is the greatest ground-set order
admitting an S2 capped H** in this near-cube family.
The theorem concerns this restricted cap architecture, not nonexistence of
ordinary H, all capped H, or a resolution of general H/I.

## Credited context

The primary problem remains
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [version history](https://arxiv.org/abs/2609.28404), checked live on
2026-10-02, lists v1, 2026-09-23. General H and I remain open.

The nonempty core and actual-empty lift are credited to
[the structural certificates](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
and the forced-star kernel to
[the six-element proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
Both needed implications are proved below.
Ordinary H on all these near cubes was already established in
[the near-cube result](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md).
The known [multiple-pair certificate](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_multiple_pair_caps/PROOF.md)
gives a noncentered capped S2 example at n10, with disjoint2/2,2/3,2/4
couplings. That example and the present exclusion at every n>=11 locate
the upper boundary after this known feasible order; no exhaustive
classification of every smaller n or of larger support architectures is made.

The earlier
[sixteen-point centered separation](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/PROOF.md)
and [uniform centered extension](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_uniform_separation/PROOF.md)
excluded S2 under centering, the latter at every n>=16.
[Result9365](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_pair_separation/PROOF.md)
removed centering at fixed n16 and also gave an ordinary all-order S2
coupling budget. The new theorem removes centering in the unbounded
exclusion, improves the starting order to11, and gives a direct positive
original weighted inequality using only two scalar test vectors.
Its proof does not require the coupling budget, Schur inverses, harmonic
completeness, a solver dual or permutation averaging.

The [row-defect law](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_row_defect/PROOF.md)
and [independent review9295](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/row-defect-audit/REVIEW.md)
give necessary sparse-support defect costs; they alone permit a large-defect
escape and are scope context rather than premises here.
[Independent review9123](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/sixteen-point-cap-audit/REVIEW.md)
concerns the earlier centered sixteen-point certificate.
Neither review supplies a verdict on this new proof.
No historical priority claim or new positive construction is made.

## Necessary original core and the cardinality kernel

Index C=L_(F,F)-J by the N-1 nonempty vertices. L1=N1, and symmetry
decomposes L into its eigenvalue N on1 and its restriction to1-perp.
Thus L-J>=0 and C>=0. The cap gives its nonempty principal restriction

\[
 U=NI_{N-1}-J_{N-1}-C\succeq0.                         \tag{4}
\]

The actual empty entries are fixed by the original row equations:

\[
 L_{\varnothing,A}=1-(C\mathbf1)_A,\quad
 L_{\varnothing,\varnothing}=1+\mathbf1^TC\mathbf1.
                                                               \tag{5}
\]

There is no assumption C1=0. Necessity of(4), rather than a converse
or a guessed empty completion, suffices for this proof.

Every point star has exactly s members. For its full indicator y_i,
the support and diagonal imply y_i^T L y_i=s^2. Since L1=N1,
the centered vector y_i-(s/N)1 has zero lower energy. A zero-energy vector
of a real PSD matrix is a kernel vector, so Ly_i=s1. Restricting to F
gives Cx_i=0 for the actual nonempty point-star indicator. Therefore the
cardinality vector a, with a_A=|A|=sum_i(x_i)_A, satisfies

\[
 C a=0.                                                     \tag{6}
\]

For disjoint nonempty distinct sets define beta_AB=hM_AB. As a literal
matrix on F, with B supported on these disjoint pairs and zero diagonal,

\[
 C=sI-J+B,\qquad B_{AB}=\beta_{AB}.                           \tag{7}
\]

For every bulk vertex 3<=|A|<=n-3 set
z_A=s-beta_(A,A^c). The complement is also an actual bulk vertex, and
the vector e_A-e_(A^c) has C energy2z_A. Consequently

\[
 z_A\ge0,\quad z_A=z_{A^c}.                                  \tag{8}
\]

This individual complement inequality needs no averaging or orbit sign
condition. The proof keeps every original entry.

## Two tests and their complete original identity

Take the following two vectors on F, constant only in their test values
on each cardinality layer:

\[
 \ell_A=\begin{cases}
 0,&|A|=1,2,\\1,&3\le|A|\le n-3,\\2,&|A|=n-2,
 \end{cases}\qquad
 u_A=\begin{cases}
 1,&|A|=1,\\2,&|A|=2,\\v_{|A|},&3\le|A|\le n-3,\\r,&|A|=n-2.
 \end{cases}                                                \tag{9}
\]

Let G=sum_bulk binom(n,a)=2s-2-2q, and define
Z=sum_bulk_vertices z_A. In the lower test every singleton/two-set
coefficient is zero. A vertex of size n-2 has no disjoint bulk partner.
Every proper disjoint pair with both sizes>=3 has test product1. Thus
(7), with unordered pairs counted once, gives exactly

\[
 \ell^TC\ell=4s-4-Z+2\sum_{\{A,B\}\in P}\beta_{AB}.         \tag{10}
\]

For clarity the constant is
s(G+4q)+sG-(G+2q)^2=4s-4; bulk complements are counted by their two
endpoints, and hence contribute sG-Z before this simplification.

Use(6) to subtract the cardinality kernel in the upper test:

\[
 u^TUu=u^T(NI-J)u-(u-a)^TC(u-a).                            \tag{11}
\]

The shifted vector u-a vanishes at every singleton and two-set.
At bulk size a its value is -f_a, and at n-2 it is r-(n-2).
The latter has no disjoint nonzero shifted partner. This is the exact
cancellation of **all individual two-set corrections**, including all
central, mirrored, signed or noninvariant choices.

Put w_a=f_af_(n-a)=v_a^2-nv_a+a(n-a), using v_a=v_(n-a).
Direct counting in(11) now gives

\[
 u^TUu=C_n+\sum_{A\,\mathrm{bulk}}w_{|A|}z_A
           -2\sum_{\{A,B\}\in P}f_{|A|}f_{|B|}\beta_{AB},   \tag{12}
\]
\[
 C_n=nh+q\{h(4+r^2)-s(2+4r)\}+(n-1)S_n.                  \tag{13}
\]

Here is an explicit check of the constant, without a spectral quotient.
Write V=sum_bulk binom(n,a)v_a. Symmetry gives
sum_bulk binom(n,a)a=nG/2 and
sum_bulk binom(n,a)a*v_a=nV/2. The sums of the entries of u and u-a are

\[
 A_0=n+q(2+r)+V,\qquad B_0=-n(s-1)+q(2+r)+V.
\]

The bulk part of the diagonal-plus-complement norm for u-a is
n^2G/2-2nV+2S_n. Setting bulk complement weights equal to s and proper
bulk weights to zero, the constant in(11) is

\[
 N\{n+q(4+r^2)+S_n\}-A_0^2
 -s\{n^2G/2-2nV+2S_n+q(r-n+2)^2\}+B_0^2.
\]

Substitution of G=2s-2-2q, N=2s+n-1, h=s+n-1 reduces this expression
to(13). This computation is a constant-term evaluation; it does not assume
the substituted matrix is feasible. The z and proper-pair terms in(12)
then follow separately from the original entries in(7).

Combining(10) and(12), define the actual nonnegative quadratic sum

\[
 \Phi=u^TUu+\mu\ell^TC\ell\ge0.
\]

Its **full original identity**, valid before any support restriction, is

\[
 \Phi=\eta_n-\sum_{A\,\mathrm{bulk}}(\mu-w_{|A|})z_A
   +2h\mu\sum_{\{A,B\}\in P}\rho_{|A|,|B|}M_{AB}.          \tag{14}
\]

## Signs of every original weight

Let d=a-n/2. If v_a>0, then v_a=5/4-d^2/n, and

\[
 w_a=n^2/4-5n/4+v_a^2\le n^2/4-5n/4+25/16=\mu.
\]

If v_a=0, then d^2>=5n/4 and
w_a=a(n-a)=n^2/4-d^2<=n^2/4-5n/4<mu. Thus mu-w_a>=0 in every bulk
layer, including clipping boundaries and central layers.

For a>=3, f_a>=a-5/4>0. Also

\[
 f_a=\min\left(a,\frac{a^2}{n}+\frac n4-\frac54\right).
\]

Both functions inside this minimum are strictly increasing for a>0;
their minimum is therefore strictly increasing. If a,b>=3 and a+b<n,
then b<n-a, whence

\[
 0<f_af_b<f_af_{n-a}=w_a\le\mu.
\]

This proves 0<rho_ab<1 on **every** original proper pair in P.
There is no finite-orbit extrapolation in this argument.

## Negative constant at every n>=11

The choice r=2s/h minimizes the quadratic root term in(13). Equivalently,

\[
 \eta_n=nh+q(8h-10s)+(n-1)S_n+\mu(4s-4)
                  -\frac{4q(n-1)^2}{h}.                    \tag{15}
\]

At n11 every bulk profile value is positive and direct rational counting
gives S_11=4533/2, s=1013, h=1023, q=55, mu=289/16. Before the last
subtraction in(15), the scalar is **5**. Including the exact root term gives

\[
 \eta_{11}=5-22000/1023=-1535/93<0.                         \tag{16}
\]

Replacing r by2 therefore fails at this endpoint. The finite arithmetic
check is wholly exact, with no rounded root coefficient.

For the unbounded tail put d=a-n/2. If a is chosen from the full binomial
weight binom(n,a), the exact centered second and fourth sums are

\[
 \sum_{a=0}^n\binom na d^2=2^n n/4,\qquad
 \sum_{a=0}^n\binom na d^4=2^n(3n^2-2n)/16.                 \tag{17}
\]

For example these follow by writing d=(X_1+...+X_n)/2 with independent
uniform signs: in the fourth power only the n fourfold single indices and
6*binom(n,2) double-double indices have nonzero expectations. This proves
(17) at all integer n, rather than fitting moments to finite controls.

Clipping a negative value to zero and discarding nonbulk layers can only
reduce a sum of squares. Hence

\[
 S_n\le\sum_{a=0}^n\binom na(5/4-d^2/n)^2
       =(s+n)(9/4-1/(4n)).                                \tag{18}
\]

Discard the nonpositive last term of(15) and substitute(18). Expansion gives

\[
 \eta_n\le F_n=-s\frac{3n-15-1/n}{4}
       +4n^3-\frac{23n^2}{4}+\frac{11n}{2}-6.               \tag{19}
\]

For every n>=12, s>12n^2. The base is2036>1728. Since
s_(n+1)=2s_n+n-1, the induction difference is bounded below by

\[
 12n^2-23n-13=12t^2+265t+1439>0,\quad n=12+t,\ t\ge0.
\]

The coefficient (3n-15-1/n)/4 is strictly greater than n/3 because

\[
 5n^2-45n-3=5t^2+75t+177>0.
\]

The cubic remainder in(19) is strictly less than4n^3 because
23n^2-22n+24=23t^2+530t+3072>0. Therefore, for every integer n>=12,

\[
 F_n<-(n/3)s+4n^3<0.                                      \tag{20}
\]

Together(16) and(20) prove eta_n<0 at **all** asserted orders.

Finally(8),(14) and the nonnegative complement multipliers give(3).
If P has positive entries, its positive mass is strictly larger than its
rho-weighted positive mass, since every rho<1. The latter is at least the
signed weighted sum in(3). This proves the stated strict mass floor and
the S2 exclusion. It also finishes the proof for arbitrary original real
matrices, with no averaging or discarded empty-coordinate premise.

## Reproduction and trust boundary

[certificate.py](certificate.py) regenerates all rational profiles, weights,
constants and finite output bounds. [verify.py](verify.py) checks the complete
full-star affine identity at eight bounded orders, using a direct singleton
completion and an independent exact RREF in [affine.py](affine.py), copied
with credit from the9365 star-only face. Its necessary degree-zero forms
in [model.py](model.py) are a restricted credited layer-indicator formula.
These routines are validation, rather than a claim that each tested table
is PSD or a new existence certificate.

At n6 and n8 the verifier separately constructs every actual original
coordinate, checks every original row/support/star condition and the scalar
identity using literal core matrices. A signed mixed-cardinality trade
changes32 original positions at n12, preserves every individual point star
and row, and checks a nonzero change of(14) without orbit averaging.
It is an affine control, not a capped example. Exact full binomial sums
check the moment expansion at the listed orders. The positive polynomial
coefficients and base for the all-n induction are recorded explicitly;
the written(17)-(20) supply the coverage bridge.

The same complete record must match [expected.json](expected.json) in normal
and optimized Python modes. No assert, floating proposal, solver, large
private corpus, numerical eigenspectrum, incomplete enumeration, timeout,
memory kill, or prior reviewer verdict is a proof premise. The trust boundary
is ordinary real PSD/kernel/counting/induction reasoning and the inspected
stdlib exact Fraction/integer arithmetic; no proof assistant or independent
review of this new result is claimed.
The verifier's original unordered pair counts are also checked against
ternary-assignment inclusion-exclusion, separately from the binomial orbit sum.
