# A signed beta row on a compact Gaussian-contraction cell

**Status:** author analytic proof and exact rational interval certificate.
Independent mathematical review is pending. This signs a finite moment row
on a concrete cell of the compact frontier. It does not prove full
majorisation, all convex polynomial comparisons, or a Kneser--Poulsen case.

## 1. The finite statement

Use the sixteen labelled source and target sites in the existing
[simplex-flap fixture](../gaussian_majorisation_rank_abel/flap_fixture.json).
For the four vertices `v_i` in `{+/-1}^3` with coordinate product one, they are

    x_i=y_i=v_i;   x_ij=v_j-v_i, y_ij=v_j+v_i  (i != j).

The construction is the reversed depth-one Cheng--Tan--Zheng expansion,
not a new configuration. Let `D^x,D^y` be these exact squared-distance
matrices. Consider **any** labelled points `x'_i,y'_i` in R3 satisfying

    | |x'_i-x'_j|^2 - D^x_ij | <= 1/100,
    | |y'_i-y'_j|^2 - D^y_ij | <= 1/100,
    |y'_i-y'_j| <= |x'_i-x'_j|.                         (1)

The last condition is an actual hypothesis, not an inference from the
distance intervals. Non-Euclidean matrices in the interval box are not
asserted to be configurations. The source sites remain distinct. Give
them arbitrary weights `w_i>=0`, `sum w_i=1`, and use the corresponding
target weights. A finite contraction extends globally by Kirszbraun.

Fix variance `s=1`, put `C=(2*pi)^(-3/2)`, `f=gamma_1*sum w_i delta_x'_i`
and `g=gamma_1*sum w_i delta_y'_i`. The team's normalizations are

    d_m = C^(1-m) [integral g^m - integral f^m],
    a_j = d_(j+2)/[(j+1)(j+2)],
    b_(N,k) = (N+1) binom(N,k)
              sum_(j=0)^(N-k) (-1)^j binom(N-k,j) a_(k+j).  (2)

These are the existing beta averages of the normalized hinge gap; see
the [global criterion, equations (6)--(10)](../gaussian_majorisation_global_criterion/PROOF.md).

**Certified statement.** Every pair in (1), with every such weight vector,
satisfies all six inequalities `b_(5,k)>=0`, `0<=k<=5`. More precisely,
let `P_7(w)=7! sum_(|A|=7) product_(i in A) w_i`, the probability that
seven independent labels are all distinct. Then

    b_(5,k) >= L_k P_7(w),                              (3)

where the six rational certified lower bounds are

| k | L_k |
|---|---:|
| 0 | 1/100 |
| 1 | 1/500 |
| 2 | 1/3000 |
| 3 | 1/50000 |
| 4 | 1/1500000 |
| 5 | 1/125000000 |

The bounds are convenient sufficient values, not optimal constants.
In particular the row is strictly positive if at least seven labels have
positive mass. All smaller supports and zero-weight faces are included in
the nonnegative assertion by the analytic argument below.

After separate translations taking `x'_0,y'_0` to zero, (1) gives radii
at most `sqrt(19+1/100)<6`. There are sixteen labels, fewer than `3^6`.
Thus this is an actual cell in the [localization lane's `K_3`](../gaussian_prior_localization/DEFECT_LOCALIZATION.md),
with its weight simplex intact. The centre is an admissible contraction.
For example, contractions obtained by perturbing each centre point by at
most `1/2500` in Euclidean norm are in (1): centre distances are below six,
and their squared-distance changes are at most `24/2500+4/2500^2<1/100`.
Only perturbations that satisfy the contraction inequalities are included.

## 2. Polarization in the weights

The following argument works at any variance `s>0`. For a tuple of labels
`A=(i_1,...,i_m)` define

    K_m(A)=m^(-3/2) [exp(-S_y(A)/(2ms))-exp(-S_x(A)/(2ms))],
    S_x(A)=sum_(a<b) |x_ia-x_ib|^2,                      (4)

and similarly for `S_y`. The Gaussian product identity gives
`d_m=E K_m(I_1,...,I_m)` for independent labels of law `w`. This identity
is credited to Aishwarya--Li and already used in the team's moment sources.

Set `M=N+2`. For an M-tuple `alpha`, put

    c_(N,k)(alpha) = (N+1) binom(N,k)
      sum_(m=k+2)^M [(-1)^(m-k-2) binom(N-k,m-k-2)/(m(m-1))]
      * [binom(M,m)^(-1) sum_(A subset [M], |A|=m) K_m(alpha_A)]. (5)

Subsets here select **positions**, so repeated labels have their correct
multiplicities. Each subtuple of independent samples has law `w^m`.
Consequently, with no approximation,

    b_(N,k)=E c_(N,k)(I_1,...,I_M).                      (6)

Equivalently (5) is the degree-M homogeneous Bernstein coefficient on
the weight simplex, obtained by multiplying each degree-m moment by
`(sum w_i)^(M-m)`. If alpha has counts `n_i`, its contribution is
`[M!/product n_i!] c(alpha) product w_i^n_i`. Formula (6) remains valid
on every face. No positive lower bound on any weight is needed.

## 3. Analytic pruning, including the equality faces

**Lemma.** If the paired points `(x_i,y_i)` appearing in alpha have affine
rank at most five, every coefficient (5) is nonnegative. In particular
this holds whenever alpha uses at most six distinct labels. Thus all
beta rows `N<=4` are automatically nonnegative for arbitrary R3
contractions; at `N=5`, only seven distinct labels need enclosure.

Here is a direct proof of the coefficient assertion. Full majorisation
on a small support alone would not justify positivity of its polynomial
coefficients, so polarization must be checked.

Write `delta_ab=|x_ia-x_ib|^2-|y_ia-y_ib|^2>=0`, and let

    D_ab(t)=(1-t)|x_ia-x_ib|^2+t|y_ia-y_ib|^2,
    S_A(t)=sum_(a<b in A) D_ab(t).

Differentiating a scalar exponential and integrating yields

    K_m(alpha_A)= [1/(2s m^(5/2))]
       sum_(a<b in A) delta_ab integral_0^1 exp(-S_A(t)/(2ms)) dt. (7)

This is the existing [replica differentiation mechanism](../gaussian_contraction_moment_gaps/PROOF.md),
now retained on a labelled tuple rather than averaged over prior weights.

For each t the distances `D_ab(t)` are realized by
`(sqrt(1-t)x_ia,sqrt(t)y_ia)`. Their affine rank is at most the paired
rank. Under the lemma's hypothesis, realize them as `z_a(t)` in R5.
Put `phi_a(u)=exp(-|u-z_a(t)|^2/(2s))`, so `0<phi_a<=1`, and
`C_5=(2*pi*s)^(-5/2)`. Gaussian multiplication gives

    C_5 integral_(R5) product_(a in A) phi_a(u) du
        =m^(-5/2) exp(-S_A(t)/(2ms)).                   (8)

For a distinguished pair `a<b`, let `R=[M] minus {a,b}`. Substitution
of (7) into (5), followed by (8), gives exactly

    c_(N,k)(alpha) = [1/(2sM)] sum_(a<b) delta_ab integral_0^1
       C_5 integral_(R5) phi_a phi_b
       sum_(J subset R, |J|=k)
         [product_(j in J) phi_j product_(j in R minus J)(1-phi_j)] du dt. (9)

To check the coefficient, expand the final products. A subset `B` of R
of size r has coefficient `(-1)^(r-k) binom(r,k)`. The algebraic identity

    (N+1) binom(N,k) binom(N-k,r-k)
      / [(r+2)(r+1) binom(N+2,r+2)] = binom(r,k)/(N+2)

is precisely the factor in (9). Every integrand and every `delta_ab` is
nonnegative. This proves the lemma. Each inner integral is determined
by the continuous distance data through (8); no continuous choice of
the five-dimensional realizations is needed. All sums are finite.

This is the same dimension-five Gaussian mechanism underlying the
team's [paired-rank result](../gaussian_majorisation_rank_abel/PROOF.md),
applied to polarized moment coefficients. For a tuple of paired rank
six, (8) in R5 is unavailable; the certificate below supplies its sign
on the stated cell. No six-dimensional positivity is assumed.

## 4. Complete rational enclosure of the remaining coefficients

At `N=5,M=7` there are `binom(22,7)=170544` unordered tuples with
repetition on sixteen labels. Exactly `binom(16,7)=11440` have seven
distinct labels. The other 159104 are signed by the lemma for **every**
perturbed contraction in (1), regardless of weight or rank changes.

For a distinct m-label subset, compute its centre sums `S_x,S_y` as exact
integers. With `e=binom(m,2)/100`, its actual exponents at variance one lie in

    E_y in [max(0,S_y-e)/(2m), (S_y+e)/(2m)],
    E_x in [max(0,S_x-e)/(2m), (S_x+e)/(2m)].             (10)

Decreasing exponentials and the contraction hypothesis therefore enclose
`K_m` between

    m^(-3/2) max(0, exp(-E_y^upper)-exp(-E_x^lower))
and
    m^(-3/2) max(0, exp(-E_y^lower)-exp(-E_x^upper)).     (11)

The program encloses the exponentials and `sqrt(m)` by exact Fraction
arithmetic using the hash-pinned existing
[rational bounds module](../gaussian_majorisation_hankel_transport/bounds.py).
Its exponential enclosure uses Taylor's series with a geometric tail
bound, reciprocal, and outward-rounded squaring. Forty decimal digits
are retained internally; each kernel is rounded outward to a rational
multiple of `10^-30`. This affects width only. Isometric exact kernels
with radius zero are cancelled algebraically.

The denominators `m(m-1) binom(7,m)` divide 420. Thus integer interval
addition evaluates (5) over the common denominator `420*10^30`, choosing
the correct endpoint whenever a multiplier is negative. The checker
enumerates all 11440 distinct subsets and all six k, certifying 68640
strict lower bounds greater than the corresponding `L_k`. Every one of
the 26316 subtuples is checked using both pair distances and the
independent centroid formula `m sum |z_i|^2 - |sum z_i|^2`.
There are only 304 distinct scalar kernel enclosures.

[EXPECTED.json](EXPECTED.json) records the exact minimum lower bounds,
their first minimizing tuples, counts, and a hash of the full interval
stream. The stream is regenerated, not published as a large data file.
Combining its strict seven-distinct bounds with the other coefficients'
analytic nonnegativity in (6) proves (3) and the certified statement.

## 5. Meaning and trust boundary

This provides the finite lane with a working signed-cell consumer of
the existing beta moments: no mesh in the prior weights, no absolute
error subtracted at an isometric weight face, and no signed-tail cutoff.
The compact-frontier reduction remains credited to researcher 3, and
the global beta equivalence and defect approximation remain credited to
the existing [analytic sources](../gaussian_majorisation_open_stability/UNIFORM_FRONTIER.md).
The [finite lane's degree barrier](../gaussian_certificate_degree_barrier/PROOF.md)
for the old full-axis certificate is unaffected: one positive row does
not satisfy that certificate and does not control untested beta rows or
hinge thresholds. This cell is not a cover of `K_3` or of all bounded laws.

The proof uses the Gaussian product calculation, finite algebra, the
written rank-pruning argument, and the exhaustive interval calculation.
The numerical trust boundary is the checked source and Python integer/
Fraction arithmetic, including the pinned bounds module. No quadrature,
floating-point sign, random search, solver, or unpublished dataset is a
premise. The tests audit arbitrary rational-kernel homogenization against
ordered samples, the edge-factor identity, direct Fraction assembly,
exact isometry, and malformed-input rejection. These are author checks,
not independent mathematical review or a proof-assistant formalization.

Primary sources: [Aishwarya--Li, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2)
for the target and Gaussian identity;
[Cheng--Tan--Zheng, arXiv:1107.0140](https://arxiv.org/abs/1107.0140)
for the classical fixture and nonliftability context. Neither coefficient
polarization nor Bernstein positivity is claimed as a new general method.
The concrete new deliverable is the signed compact cell and reproducible
pruning/enclosure calculation.
