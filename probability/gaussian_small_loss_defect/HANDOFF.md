# Uniform loss and threshold handoff for R2/R8

The previous fixed-window theorem is now independently accepted at graph
6432. This continuation is a new author proof, pending independent review.
Its [proof](PROOF.md) and [exact schedule](certificate.py) give a signed
moving window plus a whole-curve error, with no atom-count dependence.

At a fixed variance s, put

~~~
Sigma_X=Cov(X)/s, d=2(tr Cov(X)-tr Cov(Y))/s.
~~~

For a contracting pair law satisfying centered source radius<=sqrt(s)/2
and Sigma_X>=2^-15 I, request a relative defect accuracy of 2^-b, b>=0.
The exact consumer is

~~~
from certificate import relative_schedule
schedule = relative_schedule(b)
~~~

It returns m=max(4,ceil(sqrt(3(b+20)))) and N=44m+208. The sufficient
guard d<=2^-N gives

~~~
H(u)>=0 on [exp(-m^2/2),infinity),
Def<=2^-b d.
~~~

The program represents log thresholds and binary exponents exactly; it
does not construct a denominator of size 2^N merely to produce a schedule.
Even a request with b=10^200 uses only compressed integer operations.
That does not make the subsequent geometric input or hinge computations
comparably inexpensive.

## One guard for an entire parameter family

If the radius, covariance and contraction hypotheses hold throughout a
parameter cell, and an exact argument gives d<=D<=2^-N throughout it,
the same m works on the whole cell. The error is pointwise 2^-b d and
uniformly at most 2^-b D. Checking the center or a sample grid is not
sufficient. No common cubature rule over the parameter cell is assumed.

A concrete nested rational family is the previously credited R6 template:
v_i=(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1), source sites
a_i=v_i/80, b_i=-v_i/4, and target sites
(1-tau)a_i, (1-tau)29v_i/120. Give core sites weights
p_i>=(1-alpha)/8, sum p_i=1-alpha, and outer sites arbitrary nonnegative
weights summing to alpha. For independent parameters

~~~
0<=tau,alpha<=2^-(N+2),
~~~

the accepted previous proof gives radius<1/2, covariance>=I/25600 and
d<=tau/400+2alpha<2^-N. Thus this entire rational parameter polytope,
including all its unbalanced priors, receives the new moving sign and
whole-curve defect bound. At tau=0,alpha>0 the old quartic condition still
fails since Q/d>=59/1800. The geometry and these elementary guards are
prior results, not a newly discovered map class. The new information is
the moving endpoint and arbitrarily prescribed relative defect.

## Common finite-source interface

Only marginal means and second moments enter the guard. Degree-two
paired cubature preserves them using at most 19 original pairs. At
higher degree the existing budget 2 binom(2q+3,3)-1 is unchanged.
No extra mixed feature is needed. The theorem applies directly to the
original law; guard preservation does not assert equality of its hinge
with the cubature hinge.

The general function annular_schedule(R,kappa,m) gives an exact cutoff
for exp(-m^2/2)<=u<=exp(-S0^2/2), S0=max(5R,3R+1).
Its label ANNULAR_WINDOW_ONLY is deliberate: a separate fixed-window
cutoff must also hold to infer a global upper window outside the worked
normalization. Section 6 of the proof provides that cutoff explicitly.

R2's new covariance-collapse guard is complementary: it signs the fixed
middle interval when either marginal variance in a direction is at most
2^-86 d^2. It does not supply a fixed positive covariance floor for
this flat-defect theorem. No unproved joint-boundary cover is inferred.

## Remaining sign obligation

For a fixed nonzero input loss, increasing b eventually fails the loss
guard. One cannot pass to b=infinity with the same input and conclude
Def=0. The possible adverse region remains below the moving endpoint.
The all-radius estimate makes its defect smaller than every power of d
at fixed radius and covariance floor; it is still an error estimate.

This result supplies a quantitative small-loss error budget to exact
hinge or moment machinery. It does not certify the positive-loss
complement, ordinary rational rounding, covariance-collapse uniformity,
unrestricted majorisation, or a new Kneser--Poulsen consequence.
