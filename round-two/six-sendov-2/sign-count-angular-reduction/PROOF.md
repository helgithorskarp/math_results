# Sign-count and heavy-block reductions for the degree-nine angular ratio

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Complete ordinary author proof with compact exact finite algebra;
unformalized, independent review pending. The elementary moment lemmas
are proved here. No historical priority for kurtosis/moment inequalities
is asserted; see [LITERATURE.md](LITERATURE.md).

## 1. Definitions and useful new exclusions

For a balanced norm-one vector theta in R8, let

    e=ones/sqrt8, P=I-ee^T,
    H=P diag(theta) P restricted to e-perp, w=diag(theta)e,
    rho_lambda=8||Pi_lambda w||², eta=sum rho_lambda²,
    X=sum theta_i^4, C=(1-eta)/(X-1/8).

Every Pi is the projection onto a full eigenspace. For global comparison,
use the proved continuous value16 at the uniform4+4 orbit as in8753.
Let r be the number
of distinct original coordinate values, and let p,q count the strictly
positive and strictly negative coordinates. A nonzero balanced vector
has r>=2. No ratio extension at uniform is needed for the following sets,
because their denominators have strictly positive uniform lower bounds.

**Theorem A (sign-count reduction).** If min(p,q)<=3, then

    X>=13/84,

with equality exactly permutations/reflections of
`(4,4,4,-3,-3,-3,-3,0)/sqrt84`. Consequently, for r<=4,

    C<112/5=22.4.

More generally the non-strict bound for r original levels is
`C<=168(r-2)/(5(r-1))`.

**Theorem B (heavy-block reduction).** If at least five original coordinates
are equal, then X>=19/120, with equality exactly the normalized5+3 orbit
`(3,3,3,3,3,-5,-5,-5)/sqrt120`, up to permutation/reflection. On this
entire closed stratum, including every collision,

    C<20.

Neither angular upper constant is asserted sharp. Their strictness is
proved below; their fourth-moment lower constants and equality sets are sharp.

The existing sharp at-most-three-level theorem
[8753](../angular-three-level-transition/PROOF.md), source
6efce877eb9dcde6e12b6a90930d65382b29dd89, supplies an admissible profile
with C=c3 in(24.53389668,24.53389670), greater than49/2. It is independently
confirmed by [review8806](../../six-reviewer-1/three-level-angular-audit/REVIEW.md),
source178ddb2ff86b4c3f2e4be62ac31532045941a863. This comparison yields:

**Corollary.** Every profile with at most four distinct original levels
and C>=c3 has exactly four positive and four negative coordinates. In
particular it has no zero coordinate and no original block of size at
least five. This reduces *every* four-level multiplicity pattern, rather
than proving an optimum on one prescribed family.

Theorems A--B use no campaign theorem as a mathematical premise. The
c3 corollary inherits only the stated previously established comparison.
The full all-sphere inequality C<=c3 and first-power Tang--Zhang remain open.

## 2. Active-mass count, including collisions

Partition the coordinates by their r original values. The within-block
difference spaces have total dimension8-r. Each is an eigenspace of the
diagonal matrix and of its compression, and each is orthogonal to both
e and w. Their orthogonal complement is the block-constant space.
Its intersection with e-perp has dimension r-1, is invariant under H,
and contains w. Hence at most r-1 full eigenspaces have nonzero w mass.
This statement also holds when previously distinct levels merge: simply
use the actual partition. No splitting of a degenerate eigenspace occurs.

The spectral theorem and norm normalization give

    sum rho_lambda=8||w||²=1,   eta=sum rho_lambda²>=1/(r-1).

This is Cauchy--Schwarz for the at most r-1 nonnegative active masses.
In particular r<=4 implies1-eta<=2/3. The argument is elementary and
retains the prior angular-framework credit7432/review7496.

## 3. Sharp moment barrier for unbalanced signs

The subset of the balanced sphere on which min(p,q)<=3 is closed and
compact. A fourth-moment minimum exists. Reflection allows p<=3.
Let n be its number of nonzero coordinates. If n<=6, Cauchy--Schwarz
on these coordinates gives X>=1/n>=1/6>13/84. It remains to classify
n=7 and n=8 minima inside the fixed nonzero-support/sign face.

On that face the constraint gradients ones and theta are independent:
a nonzero balanced vector cannot be constant. Lagrange multipliers give

    4t³-2lambda t-mu=0

at every nonzero coordinate value. Thus there are at most three distinct
nonzero levels. A one-level nonzero balanced profile is impossible.

For two levels with k positive and m negative coordinates, m+k=n,
balance and normalization give

    X=(m³+k³)/(mk n²).

Since k<=3, all possible values are:

| n | k=1 | k=2 | k=3 |
|---|---|---|---|
|7|31/42|19/70|13/84|
|8|43/56|7/24|19/120|

All are at least13/84, with equality only in the seven-coordinate3+4 case.

For three levels t1<t2<t3, the cubic has no quadratic coefficient, so
`t1+t2+t3=0`. Its middle-level constrained Hessian coefficient is

    12t2²-2lambda=4(t2-t1)(t2-t3)<0.

If the middle level occupied at least two coordinates, splitting those
coordinates with v=(1,-1) gives sum v=theta dot v=0, an admissible tangent,
and a strictly negative constrained second variation. This contradicts
local minimality on the face. Therefore the middle multiplicity is1.

Write the multiplicities (m,1,k), with m+k=n-1. Subtracting the root sum
from balance gives

    (m-1)t1+(k-1)t3=0.

If m=1 or k=1 an outer level would be zero, impossible. Otherwise scale
t1=-1, obtaining

    t3=(m-1)/(k-1),   t2=1-t3.

One must retain the strict root order, nonzero middle level and the sign
restriction min(p,q)<=3; the list below includes both reflections. Exhausting m=1,...,n-2 is a tiny exact integer classification,
not a numerical search. For n=7 there is no admissible three-nonzero-level
minimum candidate. For n=8 the only two possibilities, exchanged by
reflection, are

    (m,1,k)=(4,1,3), levels(-1,-1/2,3/2),
    (m,1,k)=(3,1,4), levels(-1,1/3,2/3).

Both give X=7/44=13/84+1/231. The complete eleven-case enumeration is
regenerated in the checker, including its exclusions and root orders.
The Lagrange/Hessian interpretation remains written mathematics.

This accounts for every possible minimizing face and proves X>=13/84.
Only the seven-nonzero-coordinate two-level case attains it. Balance
then fixes the ratio4:-3; adding its zero coordinate gives the stated
exact equality orbit. Its norm squared is84 and fourth sum1092.

## 4. Sharp moment lower bound with five equal coordinates

Choose five equal coordinates a. Write the remaining three as m+ti,
where m=-5a/3, sum ti=0, tau=sum ti². Direct expansion gives

    1=40a²/3+tau,   0<=tau<=1,
    sum ti^4=tau²/2,
    tau³-6(sum ti³)²=2[(t1-t2)(t2-t3)(t3-t1)]²>=0.

Thus abs(sum ti³)<=tau^(3/2)/sqrt6. Expanding X and eliminating a²,

    X=19(1-tau)²/120+5(1-tau)tau/4+tau²/2+4m sum ti³
     >=19/120+tau[(112-71tau)/120
                       -sqrt5 sqrt(tau(1-tau))/3].

The coefficient of the last bound follows from
`(20/3)²*(3/40)/6=5/9`; no approximate square root is used.
The bracket is strictly positive on[0,1]. Indeed112-71tau>=41>0 and

    (112-71tau)²-8000tau(1-tau)
      =13041tau²-23904tau+12544,
    4*13041*(13041tau²-23904tau+12544)
      =(26082tau-23904)²+82944000>0.

Squaring is legitimate because both quantities compared are nonnegative.
Hence X>=19/120, with equality precisely tau=0. The remaining three
coordinates are then all-5a/3; normalization yields the stated5+3 orbit.
Its norm squared is120 and fourth sum2280. The proof includes a=0,
and choosing any five from a larger repeated block remains legitimate.

## 5. Transfer, strictness and the remaining chart

On the sign sector, X-1/8>=5/168>0. Therefore

    C<=((r-2)/(r-1))/(5/168)=168(r-2)/(5(r-1)).

For r<=4 this is at most112/5. Equality in that value would require both
X=13/84 and eta=1/3. But the moment equality orbit has exactly three
original levels (positive, negative, zero), so eta>=1/2. Thus C<112/5.
On the heavy stratum, r<=4 automatically and X-1/8>=1/30, giving C<=20.
Equality would require the moment equality5+3 profile, with only two
original levels and eta=1. Thus C<20. This proves both angular strictness
claims without claiming a numerical sharp maximum of either set.

Since112/5<49/2<c3, any at-most-four-level candidate with C>=c3 has p=q=4.
For the next4+2+1+1 family write, after reflection/scaling of the nonzero
fourfold coordinate,

    u=(1,1,1,1,b,b,-2-b+y,-2-b-y), V=y²>=0.

All the other coordinates must be negative. This is equivalent to

    -2<b<0,   0<=V<(b+2)².

For a genuinely four-level member additionally V>0. Profiles outside
this bounded chart are already below112/5. The candidate equality
4+3+1 orbit occurs at b=1/alpha,V=4(alpha+1)²/alpha², where alpha is the
quartic root in8753. Candidate containment does not prove this remaining
family's maximum; a high-degree stationary reduction is saved separately
as unpublished exploratory work, with timed-out steps explicitly incomplete.

## 6. Certificate and scope

Run `python3 -B verify.py` and `python3 -B -O verify.py` in this directory.
Python3.11+ standard library only. The checker reconstructs all six
two-level moments, all eleven three-level cases, both literal equality
profiles, four universal balanced-triple/heavy-block identities, the
positive quadratic certificate, normalization and angular comparison
constants. All29 records match the compact fixture; four mathematical
damages reject. The sparse Fraction arithmetic is elementary code;
its presentation follows earlier standalone campaign checkers with credit,
but no research implementation is imported.

Compactness, Lagrange multipliers, second variations, block-invariant
spectral spaces, Cauchy--Schwarz and the transfer arguments are ordinary
written proof. No enumeration of all sphere profiles, CAS output,
floating stationary value, timeout or operational limit is a premise.
This is a global sign-stratum reduction, not a full all-sphere optimizer,
an effective stability neighborhood, a disk-polynomial theorem or a
first-power endpoint resolution.
