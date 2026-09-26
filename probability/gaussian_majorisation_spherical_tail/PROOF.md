# A spherical tail test and a ball-hull reformulation

Author proof, 26 September 2026. Independent review pending.
The bounded-input Gaussian majorisation conjecture in dimension three is
**not resolved** here. No violating configuration, new all-threshold class,
or new Kneser--Poulsen inequality is asserted.

The result gives an explicit counterexample-transfer test at very low
thresholds. Unlike a finite moment test, its sign is a spherical integral
of a log moment-generating function. For finite configurations, requiring
that sign for every weight vector is exactly an arbitrary-radius ball-hull
mean-width comparison. Neither direction of this last equivalence assumes
the missing geometric inequality.

## 1. Definitions and the explicit transfer theorem

Let sigma be normalized area measure on S^2. For a probability measure nu
supported in B(0,L), define

\[
 S_\nu(\lambda)=\int_{S^2}\log\left(\int e^{\lambda\theta\cdot x}
                  \,d\nu(x)\right)\,d\sigma(\theta),\qquad\lambda>0.
 \tag{1}
\]

For a probability density f let H_f(a)=integral (f-a)_+ dx. Thus f is
majorised by g precisely when H_f(a)<=H_g(a) for every positive a.
Write gamma_s for the Gaussian density with covariance s I_3 and
C_s=(2 pi s)^(-3/2).

**Theorem A.** Let nu and omega be any two probability measures supported
in B(0,L); they need not be related by a contraction. Fix lambda>0 and set

\[
 A=\lambda L,\quad K(A)=4A^2+3A+3,\quad
 a_s=C_s e^{-\lambda^2s/2},\quad f_s=\nu*\gamma_s,
 \quad g_s=\omega*\gamma_s.
\]

If lambda^2 s>=max{1,4A}, then

\[
 \left|\frac{H_{g_s}(a_s)-H_{f_s}(a_s)}
                   {4\pi\lambda s^2 a_s}
       -\big(S_\nu(\lambda)-S_\omega(\lambda)\big)\right|
 \le \frac{2K(A)}{\lambda^2s}.
 \tag{2}
\]

Consequently, if omega=T_#nu for a contraction and

\[
 S_\nu(\lambda)-S_\omega(\lambda)\le-\eta<0,
 \tag{3}
\]

then the desired Gaussian majorisation fails for **every** s satisfying

\[
 \lambda^2s\ge\max\{1,4A\},\qquad
 \lambda^2s>2K(A)/\eta,
 \tag{4}
\]

at the explicitly specified threshold a_s. Thus the full conjecture
requires S_nu(lambda)>=S_(T_#nu)(lambda) for every lambda>0.
An affirmative result for (1) alone would not establish full majorisation.

Both S and H are invariant under translation of their measures/densities.
For S, translation adds lambda theta dot b inside the outer integral, whose
average is zero. The two measures may therefore be centered separately
before choosing a common L. Their pair-distance contraction property is
also invariant under separate translations.

## 2. A uniform single-density estimate

We prove a stronger estimate for each density separately and then subtract.
Put R=lambda sqrt(s), epsilon=1/sqrt(s)=lambda/R, C=(2 pi)^(-3/2),
a=C exp(-R^2/2), and let

\[
 F(x)=\mathbb E\gamma_1(x-\epsilon X),\quad X\sim\nu,
 \qquad b(\theta)=\log\mathbb E e^{\lambda\theta\cdot X}.
\]

Under R^2>=max{1,4A}, we claim

\[
 \left|\frac{1-H_F(a)}{4\pi aR}
              -\left(\frac{R^2}{3}+1+S_\nu(\lambda)\right)\right|
       \le \frac{K(A)}{R^2}.
 \tag{5}
\]

All estimates below are uniform over theta and over the probability law
with the stated support bound. In particular, no minimum atom weight,
positive covariance eigenvalue, smooth input density, or finite support
assumption is used.

### 2.1 The level boundary is one radial graph

The translated centers have norm at most c=A/R. Gaussian comparison with
distances r+c and r-c shows

\[
 F(r\theta)\ge C e^{-(r+c)^2/2}\quad(r\ge0),\qquad
 F(r\theta)\le C e^{-(r-c)^2/2}\quad(r\ge c).
 \tag{6}
\]

Every point with r<R-c is above level a. For r>c,

\[
 \partial_r\log F(r\theta)=-r+
 \epsilon\frac{\mathbb E[(\theta\cdot X)
 e^{\epsilon r\theta\cdot X-\epsilon^2|X|^2/2}]}
 {\mathbb E e^{\epsilon r\theta\cdot X-\epsilon^2|X|^2/2}}
 \le-r+c<0.
 \tag{7}
\]

Since c<=R/4, each ray has a unique level boundary r=r(theta) in
[R-c,R+c]. The superlevel set consists of the interval from zero to this
boundary on every ray. Set u=R(r-R), so |u|<=A and r>=3R/4.

For

\[
 \ell(t,\theta)=\log\mathbb E
       e^{\lambda(t/R)\theta\cdot X-\lambda^2|X|^2/(2R^2)},
\]

the boundary equation and an elementary logarithmic comparison give

\[
 u+\frac{u^2}{2R^2}=\ell(r,\theta),\qquad
 |\ell(r,\theta)-b(\theta)|
 \le\frac{A|u|+A^2/2}{R^2}.
\]

Here we use that if two exponents differ pointwise by at most d, the
logarithms of their exponential integrals differ by at most d. It follows
that

\[
 |u-b(\theta)|\le\frac{2A^2}{R^2}.
 \tag{8}
\]

The volume contribution on the ray therefore satisfies

\[
 \left|\frac{r^3}{3}-\frac{R^3}{3}-Rb(\theta)\right|
 \le\frac{3A^2}{R}+\frac{A^3}{3R^3}
 \le\frac{4A^2}{R}.
 \tag{9}
\]

The last step uses A/R^2<=1/4. These inequalities also cover A=0.

### 2.2 The outside mass has a universal leading term

Let Q(theta)=integral_r^infinity F(t theta)t^2 dt. At the boundary F(r theta)=a.
Changing variable v=(t^2-r^2)/2 gives

\[
 \frac{Q(\theta)}a
 =r\int_0^\infty e^{-v}\sqrt{1+2v/r^2}\,J(v)\,dv,
\]

where t=sqrt(r^2+2v) and

\[
 J(v)=\frac{\mathbb E e^{\epsilon t\theta\cdot X-\epsilon^2|X|^2/2}}
 {\mathbb E e^{\epsilon r\theta\cdot X-\epsilon^2|X|^2/2}}.
\]

Because t-r<=v/r,

\[
 e^{-qv}\le J(v)\le e^{qv},\qquad
 q=\frac A{Rr}\le\frac13.
\]

Using 1<=sqrt(1+2v/r^2)<=1+v/r^2, and integrating the two elementary
exponentials, we obtain

\[
 \frac1{1+q}\le\frac{Q(\theta)}{ar}
 \le\frac1{1-q}+\frac1{r^2(1-q)^2}.
\]

In particular

\[
 \left|\frac{Q(\theta)}a-r\right|
 \le\frac{3A}{2R}+\frac9{4r}
 \le\frac{3A/2+3}{R},
\]

and hence

\[
 \left|\frac{Q(\theta)}a-R\right|
 \le\frac{5A/2+3}{R}.
 \tag{10}
\]

### 2.3 Reassemble the hinge defect and rescale

Probability normalization gives the exact identity

\[
 1-H_F(a)=a\,|\{F>a\}|+\int_{\{F\le a\}}F.
 \tag{11}
\]

Insert (9) and (10), integrate over S^2 with area measure 4 pi sigma,
and divide by 4 pi a R. This proves (5), since
4A^2+(5/2)A+3<=K(A).

For the original density f_s, F(z)=s^(3/2) f_s(sqrt(s) z), so
H_F(a)=H_(f_s)(a/s^(3/2)). Here a/s^(3/2)=a_s and
aR=lambda s^2 a_s. Subtract (5) for nu and omega, reversing the defects
as H_g-H_f=(1-H_f)-(1-H_g), to obtain (2). This also verifies its sign
and its normalization. Conditions (3)--(4) then imply strict negativity.

## 3. Exact equivalence with arbitrary-radius ball hulls

This part holds in every finite dimension. We state it in dimension three
to match the research problem. Fix labelled configurations x_1,...,x_N and
y_1,...,y_N. For c in R^N write

\[
 W_x(c)=\int_{S^2}\max_i(\theta\cdot x_i+c_i)\,d\sigma(\theta).
 \tag{12}
\]

**Theorem B.** The following conditions are equivalent for this fixed pair:

1. For every positive probability vector p and every lambda>0,
   S_(sum p_i delta_x_i)(lambda)>=S_(sum p_i delta_y_i)(lambda).
2. W_x(c)>=W_y(c) for every c in R^N.
3. For every vector of nonnegative radii r_i, the mean width of
   conv(union_i B(x_i,r_i)) is at least that of conv(union_i B(y_i,r_i)).

No contraction assumption is needed for the equivalence. For a contraction
pair these are necessary conditions for Gaussian majorisation at all weights
and variances, by Theorem A. We do not prove them for arbitrary contractions.

**Proof that 1 implies 2.** Given c and t>0, choose
p_i(t)=exp(t c_i)/sum_j exp(t c_j), and use lambda=t. For each theta,

\[
 \max_i(\theta\cdot x_i+c_i)
 \le t^{-1}\log\sum_i e^{t(\theta\cdot x_i+c_i)}
 \le\max_i(\theta\cdot x_i+c_i)+\frac{\log N}{t}.
 \tag{13}
\]

The common normalizing log sum_j exp(t c_j) cancels in the comparison.
Integrate and let t tend to infinity. The convergence is uniform in theta.

**Proof that 2 implies 1.** Let G_1,...,G_N be independent standard Gumbel
variables, with CDF exp(-exp(-z)), and let kappa=E G_1. The elementary CDF
calculation

\[
 \Pr\{\max_i(v_i+G_i)\le z\}
 =\exp\left(-e^{-z}\sum_i e^{v_i}\right)
\]

shows

\[
 \mathbb E\max_i(v_i+G_i)=\log\sum_i e^{v_i}+\kappa.
 \tag{14}
\]

Apply condition 2 to the random offsets c_i=(log p_i+G_i)/lambda, and
multiply by lambda. Integrating also in G and using (14) proves condition 1;
the common kappa cancels. Fubini is justified by bounded center coordinates
and the finite first absolute moments of the finite collection of Gumbels.

**Equivalence with 3.** Adding a common constant C to all c_i adds C to
both W values. We can therefore make every c_i nonnegative. The support
function of conv(union_i B(x_i,c_i)) is max_i(theta dot x_i+c_i).
Mean width is twice the normalized spherical average of that function.
This proves equivalence with condition 3, including zero radii by continuity.

### 3.1 An explicit geometric counterexample transfer

Suppose a contraction pair were found with
W_x(c)-W_y(c)<=-eta<0. Choose t>2 log(N)/eta and
p_i=exp(t c_i)/sum_j exp(t c_j). The two errors in (13) are each in
[0,log(N)/t], so their difference has absolute value at most log(N)/t.
Consequently

\[
 S_{\sum p_i\delta_{x_i}}(t)-S_{\sum p_i\delta_{y_i}}(t)
 \le -t\eta+\log N<-t\eta/2.
 \tag{15}
\]

Theorem A now supplies a Gaussian hinge counterexample at every variance
s satisfying (4), with lambda=t and its eta replaced by t eta/2. This is
a rigorous conditional conversion. **No c,x,y satisfying its negative
hypothesis is supplied or claimed in this work.**

## 4. What this does and does not settle

The known mean-width theorem for finite point sets is the equal-offset
case of (12). It does not supply every offset required in Theorem B.
Csikos--Horvath prove the corresponding convex-hull-of-disks perimeter
comparison in dimension two. That is useful prior context, not a theorem
in dimension three; see [SOURCES.md](SOURCES.md).

The theorem isolates the regime of fixed lambda>0, s tending to infinity,
and thresholds a_s=C_s exp(-lambda^2 s/2). Positive S gap controls that
particular regime for sufficiently large s, but not all thresholds, and
not regimes where lambda varies with s. Zero S gap requires finer terms.
No converse from Theorem B to all Gaussian hinge comparisons is asserted.

This is distinct from the team's small-perturbing-mass analysis, in which
the law varies as (1-e)delta_0+e nu at fixed variance. Here the law and its
weights are fixed while variance increases. It is also distinct from
finite-degree high-variance comparisons: even the new degree-unrestricted
sparse-polynomial theorem leaves arbitrary hinges and larger Hankel
matrices unproved. A counterexample produced by (3) would automatically
escape every energy class that has already been proved safe.

The covariance-free rigidity theorem supplies closeness and entropy
information but no signed inequality (1). We do not infer that sign from
rigidity, entropy comparison, a Gaussian average of (1), or positivity at
individual points along a lifted contraction.

At the final team refresh, full comparison was established for the balanced
twelve-ray class by relabelling, and for sufficiently small perturbing mass
at each fixed variance under nested-hull and strict-radius hypotheses.
The former includes the unanchored symmetric cuboctahedral law; the latter
includes dominant-origin anchored flaps of depths up to two. These covered
cases and the exact distinction between the two tail regimes are recorded
in [SOURCES.md](SOURCES.md). Neither result is needed in the proof above.

The accompanying audit checks formulas and normalizations on a solvable
two-point law. Its quadrature is explicitly floating point and does not
establish any universal claim or certify a conjecture counterexample.
The written estimates and elementary Gumbel identity carry the proofs.
