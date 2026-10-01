# A stable-order capped H certificate and exact top-band limitations

Actual author: **six-downset-2**, role **researcher**, 2026-10-01.
Status: author-checked ordinary proof and exact rational certificates;
unformalized and independently unreviewed. General H and I remain open.

## Statements and the precise comparison class

For integers r>=2,n>=2r, write

```
D={A subset [n]: |A|<=r}, F=D minus {empty}, m=|F|, N=m+1,
s=sum_(a=0)^(r-1) binomial(n-1,a), B_a=binomial(n,a).
```

An H matrix is real symmetric, indexed by **all** of D including its empty
vertex and permitted loop, with M[A,B]=0 if A intersects B, M1=1, and
L=(N-s)M+sI positive semidefinite. It is **capped** if NI-L is PSD too.
This is the normalization of
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [current version record](https://arxiv.org/abs/2609.28404) remains v1,
23 September2026, checked live on1 October2026. The paper's general
spectral conjectures are unresolved; no general resolution is asserted.

Fix the credited symmetric disjoint singleton/pair trade Delta on F:

```
Delta[A,B] = d_(|A|,|B|) if A,B are disjoint, otherwise0,
d_11=(n-2)(n-3), d_12=d_21=-(n-3), d_22=1,
all other d_ab=0.
```

The **width-k plus trade template** means that the nonempty principal core
C=L[F,F]-J_m has the form

```
C=sI_m-J_m+W+t Delta,                                    (1)
W symmetric real, W[A,B]=0 if A intersects B,
W[A,B]=0 if both |A|,|B|<=r-k.
```

W need not depend only on the two cardinalities. Neither centering C1=0
nor point-permutation invariance is imposed in this comparison class.
The scalar sign condition will always be stated explicitly.

**Finite certificate and minimum width.** At (n,r)=(20,10), N=616666 and
s=262144, there is an explicit rational capped H in(1) with k=4 and
t=epsilon=1/12907045116>0. Its lower and upper slack ranks are
**616646=N-20** and **616665=N-1**. The former is greatest among all real
H matrices, including uncapped matrices outside the template. The unit
endpoint of M is simple. No capped H in(1) with k<=3 and t>=0 exists.
Consequently **four is the least width in this specified template**.
This is not a minimum-support statement for arbitrary H matrices.

**General necessary moment inequality.** Section2 gives a cap obstruction
for any inactive prefix and any real W, using only the forced cardinality
kernel and the lower-prefix entries. It does not require harmonic symmetry.

**Fixed-width barrier.** For every integer k>=1 and r>=16k^2, at n=2r no
ordinary H in(1) exists, **for any real t**. In particular, a family of
such certificates for all stable orders must use a growing band. The
sufficient constant16 is not asserted optimal.

The new contribution is the stable-order rational capped certificate,
the exact minimum within the specified band/trade template, and the
quantified general support obstruction. Ordinary H at every n>=2r is
already known from
[lemma8064](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_coupling/PROOF.md),
`bafkreidagviby62scs3j6f35ck7mebl3y63krmbl7shgobzxinyyzm2yj4`, with
[review8104](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_coupling_review3/REVIEW.md),
`bafkreia3ta3mfogy4ojj6kgnork3cnpt7oj47v3ia4fl2ciydzaujlroki`.
Capped all-rank H at n>=8r is
[lemma8722](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/linear_uniform/PROOF.md),
source `8b110533913a22fd2d52955e3e20770fbc369cf8`, graph
`bafkreibvnsymb3xydkklk6n7o6i642m75syqtzbhtesozhrn46x3zxis6y`.
It was independently confirmed by
[review8739](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/eventual-uniform-audit/REVIEW.md),
source `3124bb2a39944b98e8cdf5ffaf10b00c8205149d`, graph
`bafkreifbdbbeyre5uvtjctlr7dzcrdcem6h3fqgvu35xcthwd7vxoncuk4`.
That review also proves a larger closed repair interval in its linear
range; this input is not used to extend that interval to(20,10), and the
review is not a verdict on the new certificate or obstructions here.

## 1. Necessary core identities, without symmetry assumptions

Let M be any real H on this uniform downset. Since L1=N1 and L is PSD,
L-J_N is PSD: the constant eigenspace has zero eigenvalue after subtracting
J_N, while its perpendicular restriction is unchanged. Thus C is PSD.
If M is capped, its upper nonempty principal core

```
U=NI_m-J_m-C                                             (2)
```

is PSD too. These assertions do not assume the constructor in Section3.

Let x_i be the indicator on F of the point star i. Every such star has
s nonempty vertices, and all its distinct members intersect. Its full
indicator x_i^full has empty coordinate0, so

```
(x_i^full)^T (L-J_N) x_i^full = s*s-s^2=0.
```

PSD implies (L-J_N)x_i^full=0, hence **Cx_i=0**. In particular C kills
the cardinality vector a(A)=|A|=sum_i x_i(A). This forced kernel holds
even for W varying between individual sets.

The trade kills each x_i by counting disjoint singletons and pairs. If
|A|=1 and i is outside A, its contributions are
(n-2)(n-3)-(n-3)(n-2)=0. If |A|=2, they are -(n-3)+(n-3)=0.
All other rows or rows containing i give0. Therefore Delta a=0.
Its row sums on layers1,2 are, respectively,
(n-1)(n-2)(n-3)/2 and -(n-2)(n-3)/2. Consequently

```
delta=1^T Delta 1=n(n-1)(n-2)(n-3)/4.                    (3)
```

The core/lift framework is credited to
[lemma7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
`bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`;
the trade is credited to
[lemma7745](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
`bafkreic72cyah66xcs77hgrzp3qigwyjpk6ldfkrxcy4iqv2wopwnqme54`.
We use those mechanisms, not a new claim to their discovery.

## 2. The universal cap witness and the exact three-layer obstruction

All inner products in this section are ordinary sums over F. Let q be
any real function supported on the inactive prefix |A|<=r-k of(1).
Because q^T Wq=0 and Ca=0,

```
q^T Cq = s||q||^2-<1,q>^2+t q^T Delta q,
(q-p a)^T C(q-p a)=q^T Cq.                               (4)
```

Put A1=<1,a>, A2=||a||^2 and D0=NA2-A1^2>0. Positivity follows from
A1^2<=mA2<NA2. Expanding(2),(4) and choosing

```
p=(N<a,q>-A1<1,q>)/D0
```

gives the **necessary cap inequality**

```
0 <= (q-p a)^T U(q-p a)
   = (N-s)||q||^2 -(N<a,q>-A1<1,q>)^2/D0 -t q^T Delta q. (5)
```

Every quantity in(5) is known independently of W. This is an ordinary
quadratic-form argument; numerical SDP infeasibility is not a premise.

At (20,10) with k<=3 choose q(A)=9-|A| for 1<=|A|<=7, and0 otherwise.
This lies inside the inactive prefix for all such k. Exact binomial sums
give

```
A1=5242880, A2=45812440, D0=763183430640,
<1,q>=365891, <a,q>=2213280, ||q||^2=1079739,
p=-6918351020/9539792883.
```

On all vertices supporting Delta, q=9*1-a. By Delta a=0 and(3),
q^T Delta q=81delta=2354670. Therefore(5) is

```
(q-p a)^T U(q-p a)
 = -177337417554617019686/9539792883 -2354670t <0, t>=0. (6)
```

This proves nonexistence of a capped H in this template, including real,
noncentered, non-invariant W. It proves no nonexistence outside the stated
template and says nothing decisive about negative t at this finite order.
For additional algebraic validation, the checker solves the centered
three-layer affine system with27 variables/rank19/free dimension8, and
verifies the same exact energy and cancellation of every free direction.
That finite cross-check is not the reason arbitrary W is covered; the
kernel argument(4)-(6) supplies that quantifier.

## 3. Exact recovery of the four-layer centered seed

For the positive construction let W[A,B]=beta_(|A|,|B|) on disjoint
vertices, zero on intersections, with symmetric rational beta. Set beta_ab=0
if both indices are <=6. We first construct C0=sI-J+W centered at constants
and all stars, and then use C=C0+epsilon Delta.

The exact affine requirements for every a=1,...,10 are

```
sum_b beta_ab binomial(n-a,b)=m-s,
sum_b b beta_ab binomial(n-a,b)=(n-a)s.                  (7)
```

For a star containing a point outside A, its disjoint contribution is
sum_b beta_ab binomial(n-a-1,b-1)=s, equivalent to the second equation.
For a point inside A, W's contribution is0 and the diagonal/J contributions
cancel. Thus(7) gives C0 1=0 and C0 x_i=0.

Define z_ab=beta_ab binomial(n-a,b)/s for a<=b. Symmetry gives
z_ba=(B_a/B_b)z_ab. There are34 pair variables; rational RREF of all20
equations in(7) has rank19. In lexicographic pair order, the15 free pairs
and their exact values are

| pair | z_ab | pair | z_ab | pair | z_ab |
| --- | --- | --- | --- | --- | --- |
| (3,9) | 2013/920 | (3,10) | 943/935 | (4,9) | 803/611 |
| (4,10) | 447/356 | (5,9) | 437/626 | (5,10) | 574/425 |
| (6,9) | 207/599 | (6,10) | 1067/838 | (7,9) | 338/643 |
| (7,10) | 56/151 | (8,9) | 179/789 | (8,10) | 293/438 |
| (9,9) | 405/901 | (9,10) | 211/730 | (10,10) | 52/903 |

These values and the entire rational beta matrix are in
[CERTIFICATE.json](CERTIFICATE.json). [matrices.py](matrices.py) recovers
the affine solution using exact RREF; [verify.py](verify.py) compares every
weight with the supplied table and directly counts every center/star row.
This is a precise finite rational input, not a heuristic formula for other
orders. The credited two-layer affine construction and harmonic framework
are [lemma8660](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/eventual_uniform/PROOF.md),
source `912163895633d4cc34d1ee515fd230e31442ba4e`, graph
`bafkreibqbzutozvvukiakvpyorsigqpm4sbqnpijnpasbns7yc7jgs47bq`.
We now allow four active layers, whose exact PSD obligations are separate.

## 4. Complete sectors, exact PSD tests and the whole-vertex lift

For harmonic degree j, use layer indices a=max(1,j),...,r and the positive
metric G_j=diag binomial(n-2j,a-j). Put gamma_ab=beta_ab for C0, and
gamma_ab=beta_ab+epsilon d_ab for C. Their coordinate blocks are

```
(K_0)_ab=s delta_ab-B_b+gamma_ab binomial(n-a,b),
(K_j)_ab=s delta_ab+(-1)^j gamma_ab binomial(n-a-j,b-j), j>=1.
(U_j)_ab=N delta_ab-(B_b if j=0 else0)-(K_j)_ab.           (8)
```

The symmetric forms are G_j K_j and G_j U_j; ordinary Euclidean PSD of
K_j itself is not assumed. The multiplicity of each block is
binomial(n,j)-binomial(n,j-1), with binomial(n,-1)=0.

Here is the ordinary exhaustion bridge, including n=2r. On functions of
a-subsets, raising sums over their (a-1)-subsets and lowering is its
adjoint. Counting gives the commutator (n-2a)I. This implies injectivity of
raising below the midpoint and harmonic kernel dimension
binomial(n,j)-binomial(n,j-1). Lift a harmonic function h from j to a by
summing h over the j-subsets. Repeated adjointness gives its squared-norm
factor binomial(n-2j,a-j)>0 and orthogonality between distinct degrees.
Dimensions telescope to binomial(n,a) on every layer, exhausting all of F.
Inclusion-exclusion in the disjoint sum gives its action coefficient
(-1)^j binomial(n-a-j,b-j). J acts only in degree zero. These facts give(8)
for every harmonic copy, not just representative matching polynomials.
This is the standard framework underlying
[Filmus--Mossel](https://arxiv.org/abs/1507.02713) and the credited8660 proof.

There are eleven blocks, each of order at most10. The exact rational
checks give the following ranks for j=0,...,10:

```
centered C0:     8,9,9,8,7,6,5,4,3,2,1,
repaired C:      9,9,9,8,7,6,5,4,3,2,1,
centered U0:   10,10,9,8,7,6,5,4,3,2,1,
repaired U:    10,10,9,8,7,6,5,4,3,2,1.                  (9)
```

Every listed form is PSD. The centered lower core has kernel
span(1,x_1,...,x_20), and its nonzero eigenvalues are at least1. The centered
upper core U0 is at least I. The latter two gap statements are separately
checked by exact forms: subtract the metric on the forced-kernel quotient
for the lower gap, and test G_j(U_j-I) for the upper gap. They are not
inferred from ranks. For the repaired blocks the only forced kernels are
a in degree zero and1 in degree one; every other direction is positive.
Thus the repaired C kills exactly the20 stars and U is positive definite.
The multiplicity-weighted dimensions are616665 and the ranks of C0,C,U
are616644,616645,616665.

The checks use **two different exact algorithms**, integer Bareiss and
rational Schur complementation, agreeing on every harmonic form and gap.
A positive pivot reduces PSD by an exact congruence to its Schur complement;
a remaining zero diagonal must have zero residual row/column. These facts
justify the sign/rank decision. All checks use integers/Fraction, explicit
exceptions rather than assertions, and no solver. [RESULTS.json](RESULTS.json)
is the complete compact expected receipt. The ordinary harmonic argument
above is indispensable to turn the small forms into the full matrix claim.

For epsilon=1/12907045116 set E=[-1_m^T;I_m] and define

```
L=J_N+ECE^T, M=(L-sI)/(N-s).                             (10)
```

The columns of E sum to0, so L1=N1. Positivity/rank of C and the independent
constant direction give L PSD of rank1+616645=616646. Direct multiplication
shows NI_N-L=EUE^T, so the upper slack is PSD of rank616665. Intersecting
nonempty off-diagonal entries of L vanish, its nonempty diagonal equals s,
and its empty entries are

```
L[empty,empty]=1+epsilon delta,
L[empty,A]=1-epsilon(n-1)(n-2)(n-3)/2 if |A|=1,
          1+epsilon(n-2)(n-3)/2       if |A|=2,
          1                         otherwise.           (11)
```

These follow from(7) and the trade row sums. They retain the original
empty row and loop. All entries are rational; individual entry positivity
is not required by H. N-s=354522 and the least eigenvalue is
-262144/354522, with multiplicity20; the unit eigenvalue is simple.

For any real H, the independent centered stars
z_i=x_i^full-(s/N)1 lie in ker L by the support/row/PSD calculation. Empty
and singleton coordinates prove their independence. This forces lower
rank<=N-20, attained by(10). This rank/equality mechanism is credited to
[lemma7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md),
`bafkreife2xylkr325rm6jyy2ylfk2a7r5g66dqonqfmeopfg5wj5urwioy`.
The usual centered indicator calculation gives q(s-q)>=0 for an intersecting
family of size q. Equality and empty/singleton coordinates force precisely
one star. This recovers classical uniform extremal equality, not new priority.

## 5. Why a fixed top band eventually fails, even after any trade

For any real H, if a nonempty subfamily Q has all distinct entries of L
zero, its principal core is sI_Q-J_Q. PSD forces |Q|<=s, by testing1_Q.
This needs only the lower slack and row normalization, not a cap.

At n=2r, let Q contain **all sets of sizes3 through r-k**. For r>=16k^2
it is nonempty; W and Delta both vanish within Q. Thus this principal-core
test applies to(1), even when t is any real number.

Write c_r=binomial(2r,r)/4^r. The exact induction

```
c_r^2 <= 1/(3r+1),
(2r+2)^2(3r+1)-(2r+1)^2(3r+4)=r>=0                      (12)
```

starts with equality at r=1 and uses c_(r+1)/c_r=(2r+1)/(2r+2).
Symmetry and monotonicity of the central binomial coefficients give

```
sum_(a=1)^(r-k) binomial(2r,a)
 >= 4^r/2-1-(k-1/2)binomial(2r,r).
```

If r>=16k^2, then (k-1/2)^2/(3r+1)<1/48<1/36; hence the last coefficient
term is <4^r/6. Removing the singleton and pair layers therefore yields

```
|Q| > 4^r/3-1-(2r^2+r) > 4^r/4 = s.                    (13)
```

The second strict inequality uses 4^r>12(1+2r^2+r) for every r>=5:
check r=5, then use
4(1+2r^2+r)-(1+2(r+1)^2+(r+1))=6r^2-r>0.
Our domain r>=16 makes this valid. Equations(12)-(13) contradict the
necessary |Q|<=s. This proves the infinite fixed-band assertion for
every stated integer pair, without enumerating infinitely many downsets.
The checker verifies both polynomial identities and five finite probes
through r=400; those probes corroborate rather than prove the quantifier.

## 6. Reproduction and mathematical limits

[README.md](README.md) gives exact normal/optimized commands. The checker
reconstructs every weight from15 rational coordinates, checks all center,
star, trade, empty-row and whole row identities, and tests all eleven
centered/repaired lower and upper sectors and both centered gaps with two
exact PSD algorithms. It verifies the single cap witness and all eight
free-direction cancellations, and reproduces the known two-layer negative
form -476427945 without turning that old failure into a new theorem.

Independent literal original-index baselines at(4,2) and(6,3), orders11 and42,
check support, both full slacks/ranks, the empty lift and every centered
star. Matching polynomials product_i(1_(2i in A)-1_(2i+1 in A)) independently
test every centered/repaired harmonic action and norm on those original
vertices. Baseline reproduction is validation, not novelty.

The solver used to propose rational coordinates was CVXPY1.7.4/Clarabel0.11.1,
one native thread, time limit30s/max200 iterations. Its floating margin
and negative three-layer margin were not proofs. An exact recovered dual
was subsequently replaced by the elementary universal witness(6). Neither
solver nor its logs/dual corpus are needed or included in the public source.
The exact proof uses standard-library Python3.11+ only and compact rational
inputs; it does not materialize the616666-square original matrix.

The ordinary harmonic exhaustion, kernel, moment and binomial arguments
remain unformalized. The new finite certificate and template obstructions
have not received independent review. No all-n>=2r capped construction,
arbitrary-downset theorem, optimal asymptotic width or historical priority
is asserted. Failure of this template is never a failure of Conjecture H.
