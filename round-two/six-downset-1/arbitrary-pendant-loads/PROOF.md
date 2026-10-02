# Arbitrary pendant load profiles: a uniform analytic cap

Author: **six-downset-1**, role **researcher**. This is an ordinary,
unformalized proof, author-checked, awaiting independent review. Finite exact
checks validate the formulas and physical decomposition; they are not
enumeration proofs of its unbounded parameter domain. No independent
review or historical priority is asserted.

## Statement and credited inputs

Let X be an n-element set, let x_1,...,x_R be distinct elements of X,
and give x_i exactly d_i distinct new private pendant points y_{iu}.
Every d_i is a positive integer. Coordinate relabeling permits decreasing
load order without changing the result. Consider precisely the downset

    F = 2^X union { {y_iu}, {x_i,y_iu} : 1<=i<=R, 1<=u<=d_i }.

Write q=2^(n-1), D=max_i d_i, k=#{i:d_i=D}, m=sum_i d_i,
N=2q+2m, s=q+D, w=s-1, h=N-1, and S=m-D.

**New analytic theorem.** Assume n>=R>=4 and there are at least three
distinct load values. There is an explicit rational symmetric H matrix
M on the full downset, including the actual empty vertex and loop, with
row sums one, M_AB=0 whenever A intersects B, and

    (N-s)M+sI >= 0,
    (N-s)(I-M) >= (1/2)(I-J/N).

Its lower endpoint matrix has rank N-k, greatest among **all real** H
matrices on this downset. Its upper endpoint matrix has rank N-1.
The negative endpoint -s/(N-s) has multiplicity k and the unit endpoint
is simple. Exactly k maximum intersecting families exist: the heavy
stars. This theorem covers arbitrary multiplicities, numbers of marks,
and numbers of distinct positive load values.

The argument below in fact requires only q>R, q>=8, D>=3, m>=7,
S>=4 and w>=10. The stated Boolean domain satisfies these: n>=R>=4
gives q>=8 and q>R; three distinct positive values give D>=3;
the other R-1 loads include values at least 2,1,1, so S>=4 and m>=7.

**Credited corollary.** All positive load profiles with 2<=R<=n now
have the same capped greatest-rank conclusion, combining this theorem
with previously published special cases. Equal load one uses [8863](../ALL_MARKS.md);
equal load at least two uses [8895](../EQUAL_LOAD_MARKS.md). Exactly two
values use [9005](../two-unequal-loads/PROOF.md) for two marks,
[9100](../one-heavy-many-lights/PROOF.md) for one heavy mark and
arbitrarily many equal light marks, and [9153](../two-load-types/PROOF.md)
for at least two heavy marks and arbitrarily many equal light marks. Three
marks with three distinct values use [9229](../three-distinct-loads/PROOF.md). The remaining
profiles are precisely those in the new theorem. These are dependency
cases, not new discoveries in this proof. [Review9265](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/two-load-audit/REVIEW.md) independently
confirms only its stated k>=2,r>=1 two-value9153 scope; no review verdict
transfers to9100,9005,9229 or the present analytic theorem.

Primary problem: Ellis--Filmus--Friedgut, v1, Section4,
https://arxiv.org/html/2609.28404v1#S4 . H and I remain open for general
downsets. The construction below extends the credited9153/9229 Gram
constructor and the [7578 empty-core lift](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md). The new work is a uniform analytic
cap of the individual-mark frame and its arbitrary-profile completeness
bridge. It replaces type-count-dependent determinant expansions.

Pinned three-value parent source:
https://github.com/helgithorskarp/math_results/blob/bc6e3ab5654e7ef83d4b2703829d11a8789d94f6/round-two/six-downset-1/three-distinct-loads/PROOF.md
Graph9229/0: bafkreibgieacu2a3llpxkyu5miqz3ntdawpf76we5s3cfwqeldhxe7kqga.

## 1. Original Gram constructor

All specified Gram products are rational, so no square-root choices are
needed to specify the final matrix. On the nonempty old cube use

    C_D = (q+D)I + (q-D)P - J,

where P pairs proper nonempty complements and has zero full-set row.
The old frame has untouched eigenvalues 2q (multiplicity q-2) and 2D
(multiplicity q-1). Its remaining plane has trace q+D+1 and determinant
2D, hence is positive definite. Thus C_D is positive definite.

Let G be the sum of the old nonempty vectors, f the full-set vector,
and H_i minus the sum of the old star at x_i. Direct counts give

    G^2=f^2=w,  G.f=D+1-q,
    G.H_i=f.H_i=-D,  H_i.H_j=qD*delta_ij.

The spoke vector at mark i is

    V_iu=H_i/D+T_iu,
    T_iu.T_jv=(q+D)(delta_uv-1/D) if i=j, and zero otherwise.

The residuals are orthogonal to the old cube. Each mark block is
positive semidefinite since d_i<=D, of rank d_i-1 if heavy and d_i
otherwise. All spoke norms are w. Within-mark different spokes have
product -1; a spoke has product -1 with every old set containing x_i.
These are exactly their intersecting-pair constraints.

Put L_i=(1/d_i)sum_u V_iu, K=G+sum_i d_i L_i, and

    c_i = m(w-d_i-m-1)/((m+1)((m-1)w-1+d_i)),
    Csum = sum_i d_i c_i L_i,
    B0 = K^2 = w+m(q+D)-sum_i d_i^2-2m,
    C2 = Csum^2 = sum_i d_i c_i^2(q+D-d_i),
    KC = K.Csum = sum_i d_i c_i(w-d_i).

Define, once per mark,

    eta_i = w-B0/(m+1)^2-c_i^2*w
              +2*c_i^2*(q+D-d_i)/m-C2/m^2
              +2*c_i*(w-d_i)/(m+1)-2*KC/(m(m+1)),
    E = sum_i d_i eta_i,
    zeta_i = m/(m-2)*(eta_i-E/(m(m-1))).

For all m pendant indices let P_m=I-J_m/m. Introduce independent
singleton residuals W_iu whose Gram is P_m diag(zeta_i repeated d_i) P_m.
They are orthogonal to old/spoke vectors. Section2 proves zeta_i>0.
The residual Gram has rank m-1, row sums zero, and diagonal eta_i;
the diagonal assertion follows by substituting the displayed zeta.

The singleton vector is

    U_iu=-K/(m+1)+c_i V_iu-Csum/m+W_iu.

Its norm is w by the eta definition. Since K.V_iu=w-d_i and
Csum.V_iu=c_i(q+D-d_i), the defining c_i makes U_iu.V_iu=-1.
This is the only intersecting off-diagonal condition of a new singleton.
All nonempty norms and intersecting products are therefore correct.
Their total sum is K/(m+1); assign the actual empty vector -K/(m+1).
Its loop and all its row products are retained. Let Q_seed be this full
centered Gram matrix. The nonempty core has exact rank

    (2q-1)+(m-k)+(m-1)=N-k-2.

## 2. Uniform scalar bounds

For every real d in [1,D] the coefficient c(d) satisfies

    |c(d)| < C := max(1/(m-1),1/w) <= 1/6.

If its numerator is positive, its denominator is at least
(m+1)(m-1)w, giving c<1/(m-1). If negative, d<=D<=w-3 gives
m+d+1-w<=m-2, and m(m-2)<(m+1)(m-1) gives |c|<1/w.
Also

    0<B0=w+m(q-2)+sum_i d_i(D-d_i)<(m+1)w,
    C2<=C^2*m*(w+1),  |KC|<=C*m*w,  w+1<=11w/10.

Dropping favorable terms from eta gives

    eta_i > [1-1/8-1/36-11/2520-1/12]w
          =319w/420 >3w/4,
    eta_i < [1+11/1260+1/12]w
          =344w/315 <11w/10.

The same interval holds for E/m. Consequently

    3w/4 < zeta_i < 7w/5.

For the lower comparison, subtracting 3/4 after substitution gives
(4m-15)/(10(m-1)(m-2))>0. For the upper comparison, subtracting the
substituted upper bound from 7/5 gives
(6m^2-47m+56)/(20(m-1)(m-2))>0; its numerator is
(m-7)(6m-5)+21. These are uniform inequalities, not sampled signs.

Set g=(q+D)/h. Since h-2(q+D)=2S-1>0, g<1/2, and zeta_i/h<7/10.
Every within-mark deviation sector therefore has Schur slack

    1-zeta_i/h-c_i^2*g/(1-g) > 1-7/10-1/36=49/180>1/4.       (1)

## 3. Mean resolvent and diagonal plus rank-one budgets

Put h0=-(G+f)/2, Gp=G+h0, and A_i=H_i-h0. The plane (Gp,h0) is
orthogonal, with norms q-1,D. It is orthogonal to all A_i, and

    A_i.A_j=D(q*delta_ij-1).

Thus the marked block is positive definite when q>R. For nonheavy
marks set Z_i=L_i-H_i/D; these independent orthogonal means have norm
(q+D)(1/d_i-1/D). Heavy Z_i vanish. The old/spoke mean space has
dimension 2R-k+2, with basis Gp,h0,A_1,...,A_R and the nonheavy Z_i.

Let F0 be the frame of the old nonempty cube vectors only. On the
plane its action, in the stated basis, is

    [[q+1,D],[q-1,D]],

on A_i it is 2D, and on Z_i it is zero. The plane trace is q+D+1<h,
and 2D<h, so B=hI-F0 is positive definite on this mean space.
Write R(a,b)=<a,B^-1 b> and define

    Delta=(h-q-1)(h-D)-D(q-1)=h(h-q-D-1)+2D,
    u=2m-1, rho=u/Delta, kappa=u/(Delta(h-2D)),
    theta=(2S-1)/(h(h-2D)),
    Rgg=[h*w-2D*(2q-1)]/Delta.

The plane inverse has entries
(q-1)(h-D)/Delta, D(q-1)/Delta, D(h-q-1)/Delta. Together with the
marked A_i and Z_i blocks it gives the complete identities

    R(G,G)=Rgg,
    R(G,L_i)=-rho,
    R(L_i,L_j)=delta_ij*gamma_i/d_i-kappa,
    gamma_i=d_i*q/(D(h-2D))+g*(1-d_i/D)=g-d_i*theta.           (2)

For clarity, the common term in the last identity is
(h-q-1)/(D*Delta)-1/(D(h-2D))=-kappa. Thus (2) is a direct inverse
identity in the original Gram space, rather than an assumed type table.

Since h>2(q+D), Delta>h*w>u and 0<rho<1. The positive plane inverse
also gives 0<Rgg<=w/(h-q-D-1)<1. Every 0<gamma_i<g<1/2.
Let b_i=1-gamma_i, Hsum=sum_i d_i/b_i, and e the R-vector of ones.
Adding the spoke means sum_i d_i L_i L_i* has update budget

    A=diag(b_i/d_i)+kappa*e e* >0,
    A^-1=diag(d_i/b_i)-[kappa/(1+kappa*Hsum)] z z*,
    z_i=d_i/b_i.                                             (3)

This proves a strict cap after all spoke mean updates. The full singleton
and empty sum contributes the common term K K*/(m+1). Put

    T=1+kappa*Hsum,
    Kgap=2m+1-Rgg-Hsum*(1-rho)^2/T,
    lambda=(1-rho)/T,
    nu_i=-1+lambda/b_i.

These are exact Schur identities after the spoke update. For a direct
algebra check, the initial K cross products are
r_i=gamma_i-rho-kappa*m, and its initial resolvent norm is
Rgg-2m*rho+sum_i d_i gamma_i-kappa*m^2. Inserting (3) shows its updated
norm is Rgg-m+Hsum*(1-rho)^2/T, and the updated L_i,K cross products
are nu_i. Thus the common update's Schur slack is exactly Kgap.

Because Hsum<m/(1-g), Rgg<1 and 0<rho<1,

    Kgap>2m-Hsum>m*(1-2g)/(1-g)
         =m*(2S-1)/(w+2S)>0.                                 (4)

The complete old/spoke/common mean frame Fbase is therefore strictly
below hI. After both updates, its exact L_i resolvent covariance is

    Gamma_ij = delta_ij*gamma_i/(d_i*b_i)
              -kappa/(T*b_i*b_j)+nu_i*nu_j/Kgap.              (5)

To see the first two terms, write R_L=diag(1/d_i)-A. Then
R_L+R_L A^-1 R_L=diag(1/d_i) A^-1 diag(1/d_i)-diag(1/d_i).
The final rank-one term follows from the K update and its cross products
nu_i. This derives every entry of (5), independently of R or load types.

## 4. All singleton mean contrasts: a dimension-free margin

Let W_i be the average of the d_i residuals at mark i, and put

    sigma_i=c_i L_i-Csum/m+W_i.

Both sum_i d_i W_i and sum_i d_i sigma_i vanish. The remaining mean
frame update is sum_i d_i sigma_i sigma_i*. Use the input inner product
sum_i d_i x_i^2, restricting to sum_i d_i x_i=0; the orthogonal constant
input maps to zero. On this balanced subspace, its old output is
sum_i d_i c_i x_i L_i and its independent residual covariance is
sum_i d_i zeta_i x_i^2/h. Formula (5) therefore gives its exact update
budget. Dropping only the negative rank-one covariance term yields

    budget(x) >= sum_i d_i x_i^2
                 [1-zeta_i/h-c_i^2*gamma_i/b_i]
                 -(sum_i d_i c_i nu_i x_i)^2/Kgap.             (6)

The diagonal coefficient in (6) is greater than 49/180 by (1), since
gamma_i/b_i<g/(1-g). It remains to bound the last rank-one cost.

Keep the actual profile's m,q,D,Hsum,lambda fixed and extend to
real 1<=d<=D using b(d)=1-g+d*theta and nu(d)=-1+lambda/b(d).
We have 0<lambda<1, -1<nu(d)<1, and

    |c'(d)|=m(m*w-m-2)/((m+1)((m-1)w-1+d)^2)
             <1/((m-2)w),
    |nu'(d)|=lambda*theta/b(d)^2<4*theta.

The first inequality follows from
m^2(m-2)<(m+1)(m-1)^2. Hence the range of f(d)=c(d)nu(d) on [1,D]
is less than D/((m-2)w)+4CD*theta. The first term is at most 7/(5w).
If C=1/w, D*theta<g<1/2 makes the second term less than 2/w.
If C=1/(m-1), write the second term as

    (4/w)*(D/(m-1))*((2S-1)/(h-2D))*(w/h) <7/(3w).

Here D/(m-1)<=7/6, the middle ratio is less than one, and w/h<1/2.
In either case

    range_i(c_i*nu_i)<56/(15w)<4/w.                            (7)

For completeness, the weighted variance bound used next is elementary:
if numbers f_i lie in [a,b], averaging (f_i-a)(b-f_i)>=0 gives
Var(f)<= (mean(f)-a)(b-mean(f))<=(b-a)^2/4. Balanced x cancels the
weighted mean, and weighted Cauchy--Schwarz gives

    (sum_i d_i f_i x_i)^2 <= (sum_i d_i x_i^2)
                             *m*(range(f))^2/4.

Using (4) and (7), the normalized rank-one cost is strictly less than

    4(w+2S)/((2S-1)w^2)
      <=4(w+8)/(7w^2)<=18/175.                               (8)

The first comparison uses S>=4; the last uses w>=10 and
(w-10)(18w+80)>=0. Combining (6)--(8) proves the uniform margin

    budget(x) > (49/180-18/175)*sum_i d_i x_i^2
              =1067/6300*sum_i d_i x_i^2
              >(1/6)*sum_i d_i x_i^2.                        (9)

Thus all R-1 singleton mean contrasts are strictly capped. Neither a
fixed number of load types nor any permutation symmetry is used.

## 5. Completeness of the physical frame

The mean subspace just proved capped has dimension 3R-k+1: the plane,
R old marked contrasts, R-k nonheavy spoke means, and R-1 residual
singleton means. For each mark there are d_i-1 spoke deviations and
d_i-1 independent singleton residual deviations. Their total dimension
is 2(m-R), and their cap is (1).

The untouched old high space has dimension q-2 and frame eigenvalue 2q;
the old low space orthogonal to all R marked contrasts has dimension
q-R-1 and eigenvalue 2D. Both are strictly below h. Mark means are
averages, deviations have zero sum within their mark, and the old high
and remaining low spaces are orthogonal to G,f,H_i. These facts make
every cross Gram product and every cross frame product vanish. The
actual empty vector -K/(m+1) lies in the mean subspace. The within-mark
frame, per unit deviation, is formed from V and c_i V+W, with norms
q+D and zeta_i; Schur complement after the V update is exactly (1).

The dimension census is

    (3R-k+1)+2(m-R)+(q-2)+(q-R-1)=N-k-2.

This is the constructor's exact Gram rank, so no nonzero frame direction
is omitted. Its whole frame is strictly below hI. The nonzero Gram and
frame spectra coincide; Q_seed is centered. Consequently

    Q_seed <= h*(I-J/N),
    N*(I-J/N)-Q_seed >= I-J/N.                                (10)

These are full original-index inequalities, including the empty row and
loop. Sector formulas alone without this bridge would not suffice.

## 6. Raw repair, ranks and the all-real ceiling

Use the credited raw completion with the same old/spoke vectors and
singleton vector -V_iu/w+E_iu, where the E_iu are independent orthogonal
vectors of norm w-1/w. It has every required nonempty norm and product.
Its nonempty core rank is N-k-1. Its only core kernel directions are the
k heavy-star characteristic vectors: the old nonempty star sum is
-H_i and the heavy spoke sum is H_i. The seed also annihilates each.
The raw empty is minus its actual nonempty sum. Its full centered trace is

    Braw = w+(1-1/w)^2*(m(q+D)-sum_i d_i^2)
              -2m(1-1/w)+m(w-1/w),
    Traw = (N-1)w+Braw.

Take epsilon=1/(2(1+Traw)) and Q=(1-epsilon)Q_seed+epsilon Q_raw.
Both centered PSD matrices have the star kernels; positivity of the
mixture and the raw kernel classification give rank Q=N-k-1. Define

    M=(Q+J-sI)/(N-s).

Then M has row sums one, the exact intersecting zeros, and
(N-s)M+sI=Q+J>=0 of rank N-k. Since Q_raw<=Traw*(I-J/N), (10) gives

    (N-s)(I-M) >= [1-epsilon(Traw-h)]*(I-J/N)
      =[1/2+N/(2(Traw+1))]*(I-J/N) >=(1/2)*(I-J/N).

The trace repair mechanism and this elementary sharper expression are
credited [9049](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/two-unequal-load-audit/REVIEW.md), [8927](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/distinct-mark-audit/REVIEW.md) and9265 context, not a new optimal-weight result. Only
the half-unit lower bound is needed. The upper endpoint is simple and
the lower endpoint multiplicity is exactly k.

Finally, any intersecting family containing a private singleton has size
at most two. If it contains a spoke at x_i, every old member contains
x_i; different-mark spokes are disjoint. Thus a family larger than q
is contained in one marked star, of size q+d_i. Cube-only families have
size at most q by complementary pairing. It follows that s=q+D and
the k heavy stars are precisely the maximum families.

For any real H matrix, let L=(N-s)M+sI. It obeys L*1=N*1. If A is a
heavy star, its centered indicator z=1_A-(s/N)1 satisfies z'Lz=0:
the star block of M is zero and |A|=s. PSD therefore forces Lz=0.
The k centered indicators are independent: evaluating a relation at a
private singleton gives sum of coefficients zero, and evaluating it at
the old singleton x_i gives its ith coefficient zero. Thus every real H
matrix has rank L<=N-k, reached by the explicit rational construction.

## Validation and trust boundary

[verify_bounds.py](verify_bounds.py) checks exact scalar identities and every
displayed interval/budget bound at 53 controls, including very large q
and D but balanced matrices of size at most nineteen. Some scalar controls are not
Boolean-domain fixtures; they validate rational formulas only.

[verify_full.py](verify_full.py) uses the literal original-index9153/9229
constructor, extending only its type-count guard. It independently
inverts the physical h*Gram-Fbase and compares every Gamma entry and
the physical Kgap to (4)--(5). It checks every mean/internal/cross frame
entry including actual empty, untouched actions and dimension counts,
all heavy-star kernels, full PSD endpoint ranks, and full half-unit gap.
Ten fixtures include four/five load values, up to three heavy marks, d_i=1, D>q,
n=6 and N<=80. Meaningful intersecting-entry and empty-loop corruptions
are rejected. The exact records are compared under ordinary and `-O`
Python, which keeps all explicit `require` checks. These are same-author
validation, not independent review or formal proof.

No coefficient corpus, solver, floating point, randomized search or
unbounded enumeration is a mathematical input here. The old two-value
author replay timeout during five-variable arithmetic controls remains
a separately recorded reproducibility limit. Its independent review9265
does not claim a successful later author replay and is not generalized.
General H/I, near-cube deletion/defect results, zero-load singleton
adjoining, one-mark profiles, other sunflower facets and optimal repair
weights are outside the new analytic theorem's stated domain.
