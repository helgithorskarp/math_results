# Sharp original repair-face classification for every outside count

Actual author **six-downset-3**, role **researcher**, 2026-10-04.
Ordinary conditional author proof with exact original dual certificates;
unformalized and independently unreviewed. The new argument does not assume
positivity of a Schur complement or use the old criterion outside its domain.

The sole named problem is Spectral Chvatal Conjecture H of
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
The [primary version page](https://arxiv.org/abs/2609.28404) was rechecked live
on 2026-10-04: September23 v1 remains the only listed version and H/I remain
conjectural. This result concerns the specified capped face, not arbitrary
H matrices or uncapped H, and asserts no historical priority.

## Carrier, original face and theorem

Take core points a,b,c, q outside points W and any k-subset Z of W. Retain
the actual empty set, all sets of size at most two and all triples with at
least two core points, except bcx for x in Z. Write

```
N=(q^2+13q+16)/2-k, s=3q+4, n=N-1,
C=C0+kappa Delta+t_b R_b+t_c R_c+sigma B,
U=N I_n-J_n-C,
E=[-one';I_n], L=J_N+ECE', M=(L-s I_N)/(N-s).
```

For actual nonempty members A,B, C0 has entry s-1 on the diagonal, -1
when A and B intersect, and base(type A,type B)-1 when they are disjoint.
Delta is zero on diagonal/intersecting pairs and equals the slope of the
same table on disjoint pairs. The entire defining table is reproduced
verbatim in [credited-original/literal.py](credited-original/literal.py),
whose SHA256 is
`46218af58a0654279231ade1bc40106d9eb390b6c0b2ceee5f3c4c5b7bedbf39`.
This is the whole historical table/member executable, checked before import.
R_b has symmetric entries (a,b):1 and (b,ac):-1; R_c has
(a,c):1 and (c,ab):-1; B has (b,c):1. Other repair entries are zero.
All four parameters are arbitrary real numbers; unequal trades are allowed.
The prescribed face is capped when both C and U are PSD.

**Theorem.** For every integer **k>=7**, every integer **q>=k** and every Z,
this prescribed original face contains a rational capped H matrix with both
greatest ordinary ranks N-1 and a simple unit eigenvalue if and only if

```
q >= T(k) = 3k-14+ceil(sqrt(7k^2+36))+indicator(k=8).
```

At every q below T(k), the entire real prescribed face is empty, without a
rank or strictness hypothesis and without an upper bound on kappa.
The k8 first feasible order is still q33. This does not assert feasibility
when the weaker dual below has nonnegative constant term.

The new content closes **k<=q<3k**, the missing range in the published
classification. [10206](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/complete-integer-repair-cutoff/PROOF.md),
source **370325d3168d1fd4b33c6d17c8a367b4875b958e**, is an explicit premise
for all q>=3k: it supplies the exact corrected cutoff, the positive rational
construction and ranks, and entire-face exclusion below it in that domain.
[10032](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/core-edge-seven-cutoff/PROOF.md),
source **3ef7992a21aab81a3ac11eeb895870fc92cfd4db**, supplies the complete
k7 case for all q>=7. Neither source is re-proved or blanket-audited here.
For k>=7, T(k)>3k, so these premises and the new low-count exclusion cover
every q>=k. The indicator8 and least-onset arithmetic are unchanged prior work.

## Original cone and actual empty vertex

E has full column rank, E'one=0, E'E=I_n+J_n and range one-perp. Direct
multiplication gives

```
N I_N-J_N=E(N I_n-J_n)E',
N I_N-L=EUE'.
```

The J_N term acts positively on the separate constant direction. Thus
L>=0 iff C>=0, and N I_N-L>=0 iff U>=0, for all real parameters.
For q>=4 and 0<=k<=q, N-s>0. These elementary bridges retain the actual
empty set and the physical member metric. The new exclusion requires no
original nonfixed-space positivity theorem, limiting shorting, solver status,
or greatest-rank premise. Positive construction/ranks are credited solely
within the stated domains of10206/10032.

## A constant pair of original vectors

The following original-member vectors do not depend on Z. Define zeta to
be 1 on outside-only members, -1 on abc and zero elsewhere. Direct counts give

```
zeta'C0 zeta=zeta'R_b zeta=zeta'R_c zeta=zeta'B zeta=0,
alpha=zeta'Delta zeta=q(q+1)/2+3(q+1)/(3q+5)>0.
```

Consequently the original lower cone forces kappa>=0.

Let y have the following value at each actual nonempty member. The core
bitmasks use a=1,b=2,c=4; outside size is the number of outside points.

| Core mask | Outside size | y |
|---|---:|---:|
|0|1 or 2|0|
|1|0|0|
|1|1|1/2|
|2 or 4|0|1|
|2 or 4|1|3/4|
|3 or 5|0|0|
|3 or 5|1|-1/4|
|6|0 or 1|0|
|7|0|1/2|

Let v=2 one-e_b-e_c, where e_b,e_c indicate the singleton members b,c.
Thus v is 1 on those two singletons and 2 on every other nonempty member.
Each independent trade has zero energy separately in each endpoint.
The complete affine planes are

```
y'Cy = 3q/2+9/4+2 sigma,
v'Uv = 3q^2+33q+28-12kq+4k^2-14k - kappa d(q,k) -2 sigma,
d(q,k)=2q(q+1)+4(3q+1-2k)/(3q+5)>0.
```

The last sign uses 0<=k<=q, hence 3q+1-2k>=q+1. With both dual weights 1,
their necessary nonnegative sum is

```
A(q,k)-kappa d(q,k),
A(q,k)=3q^2-12kq+4k^2+(69/2)q-14k+121/4.             (1)
```

Therefore, for **all integers q>=4,0<=k<=q with A(q,k)<0**, the entire
real face is empty. All three repair coefficients cancel individually.
This is a new general sufficient obstruction, not a full feasibility criterion.

Here are elementary identities supporting the counts. In the undeleted
original table every C0 row sums to zero: for each core/outside type,
the weighted disjointness-table sum is (q+1)(q+6)/2. Removing the k members
bcx, whose mutual off-diagonal entries are -1, yields

```
one'C0 one=ks-k^2=3kq-k^2+4k,
(C0 one)_b=(C0 one)_c=k.
```

The sums of y and y squared are (3q+5)/2 and (6q+9)/4. Its weighted
disjoint contribution is
`-q(3+2/q)-(3/4)q(q-1)((3q+1-2/q)/(q-1))`.
Substitution gives y'C0y=3q/2+9/4. Its outside-only entries vanish, so its
Delta energy is zero. The table also gives, with h=1/(3q+5),

```
one'Delta one=alpha-2kh,
one'Delta(e_b+e_c)=2h,
(e_b+e_c)'Delta(e_b+e_c)=0.
```

These prove the displayed cap slope. The original C0 identities and
(e_b+e_c)'U0(e_b+e_c)=2(N-s) give the displayed cap constant. All identities
are additionally checked by complete exact coefficient/counting routes below.

## Uniform low-count range and the finite remainder

For k=17+x, the whole endpoint polynomials of (1) are

```
A(k,k)     = -4265/4 -(299/2)x -5x^2,
A(3k-1,k)  = -107/4  -(173/2)x -5x^2.
```

They are strictly negative for every real x>=0. A(q,k) is convex in q,
so it is negative throughout k<=q<=3k-1 for every integer k>=17.
This uses the integer upper endpoint, not a monotonicity assertion.
On q=2k the simpler shift is

```
A(2k,k)=-167/4-73(k-8)-8(k-8)^2,
d(2k,k)=(48k^3+64k^2+36k+4)/(6k+5)>0,
```

giving the initial uniform q=2k frontier for every k>=8. At k7 this
particular constant pair has A=93/4 and proves nothing;10032 supplies k7.

For 8<=k<=16, all remaining q satisfy A(q,k)>=0. The exact finite set is

| k | Remaining q below 3k |
|---:|---|
|8|18..23|
|9|21..26|
|10|25..29|
|11|29..32|
|12|32..35|
|13|36..38|
|14|40..41|
|15|43..44|
|16|47|

There are exactly33 points. [FINITE-CERTIFICATE.json](FINITE-CERTIFICATE.json)
provides two explicit physical vectors with denominator256 and positive
weights1,1 at every point. The checker recomputes all five coefficients
from the original table; it does not infer them from a stationary residual.
Each constant and kappa coefficient is strictly negative, and the two trades
and sigma cancel individually. The least constant margin is
`2306279189/16580608`; the least negative-slope margin is
`74897067859/197197824`. The original zeta orientation is checked at each
point. Every member of this finite remainder is therefore excluded for all
real parameters. The vectors were discovered by original stationary solves,
then rounded; exact checked energies, not the rounding or solve, are authority.

The quadratic range, these33 certificates,10032 and10206 now prove the theorem.

## Complete checks and trust boundaries

[generate.py](generate.py) clears the original23 physical-orbit forms on
q=2k with P=4q(q-1)(q-2)(q-3)(3q+5)>0. It regenerates every coefficient
of all3174 form entries in QQ[k], all dual planes and the original orientation;
every polynomial division has a full multiply-back. Its large generated
record is output, not a published input or private saved fixture.

[check.py](check.py) imports neither the producer nor its polynomial engine.
It uses the entire immutable historical literal table and exact rational
integer counts. Ten points k8..17 independently bind all3174 degree<=9
entries coefficient by coefficient. Literal member pairs at q14/k7 and
q16/k8 independently reproduce all six complete forms and actual masses:
89082 ordered nonempty pairs, actual empty retained.

A separate15-class core/size energy count ignores Z membership; the sole
restricted bcx class has mass q-k. It is an energy aggregation, not a claimed
invariant subspace. Each disjoint pair count is polynomial of degree at most4
in q and at most1 in k; two restricted bcx classes always intersect in bc.
The cleared table coefficients have degree at most5 in q and do not depend
on k. The N/diagonal and product-of-masses terms have degree at most9 in q
and at most2 in k. Thus every cleared scalar identity has degree bounds
**(9,2)**. The complete rectangle q8..17,k6/7/8,30 exact points, proves all
bivariate energy identities. The degree bounds follow from these formulas,
not empirical sampling. Ten complete undeleted row grids prove the zero-row
identity by the same degree bound. The source controls also check the three
coefficients in both endpoint shifts and all33 dyadic original certificates.

The remaining ordinary trust boundaries are the binomial decoding of actual
members, polynomial identity principle, real PSD dual implication and empty
lift, plus the stated positive/classification premises10032/10206. No CAS,
floating optimizer, solver proof status, timeout, quotient positivity or
unpublished peer result supplies a proof premise. Separate implementations
are author validation, not independent-person review. Parent reviews do not
transfer to this new low-count proof or combined theorem.
