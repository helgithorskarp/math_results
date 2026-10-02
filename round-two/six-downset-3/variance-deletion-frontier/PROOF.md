# Sharp uniform one-order corridor and exact Pell deletion frontiers

Actual author **six-downset-3**, role **researcher**, 2026-10-02.
Status: ordinary author proof with exact scalar/coefficient and original
matrix certificates. The counting, complete-space spectral bounds,
Schur estimates, lower repair, lift and infinite Pell bridges remain
unformalized. Independent review of THIS extension is pending. Reviews
of the explicitly credited parents supply no verdict on the new result.

## Quantified results

Let a,b,c be core points and W a disjoint set of integer size q. Include
the empty set, every singleton and pair, and every triple containing at
least two core points. For an arbitrary Z subset W of size k, delete
bcx for every x in Z. Denote the whole downset by D(q,Z). Throughout the
main theorem, integers satisfy k>=5 and q>=max(4,k). Put

```
N = (q²+13q+16)/2-k,    s = 3q+4,
DB = 28k²-36k+17,
b(k) = floor((6k-7+sqrt(DB))/2)
     = (6k-7+isqrt(DB))//2.
```

In the explicit affine table and four-edge scalar repair defined below:

* EVERY q>=b(k)-4, for EVERY Z, has an explicit rational capped H
  certificate. Its lower and cap ranks are N-1, both greatest, its unit
  eigenvalue is simple, and its unique maximum intersecting family is
  the a-star. The construction supplies a strict projected cap gap.
* The credited9478 obstruction excludes EVERY real parameter pair at
  EVERY admissible q<=b(k)-6. Thus at most the single integer b(k)-5
  remains between these two universal regions. No feasibility
  monotonicity or full classification of that remaining order is assumed.
* For k=6 the exact ansatz cutoff is **q=24**: a capped H exists in this
  ansatz if and only if q>=24.
* Let (p_1,u_1)=(8,3),
  `p_(j+1)=8p_j+21u_j`, `u_(j+1)=3p_j+8u_j`.
  For EVERY j>=2, put k=u_j+1. The exact ansatz cutoff is
  **q=3u_j+p_j-5=b(k)-5**. In particular all SIX old corridor orders
  b(k)-5,...,b(k) have full rational certificates, not merely positive
  necessary tests. The first such cutoff is k49,q266.

The two uniform integer-offset bounds are sharp: q<=b-6 cannot be
replaced by q<=b-5 because of these Pell certificates; q>=b-4 cannot
be replaced by q>=b-5 because k6,q23 is excluded. These are statements
about this specified ansatz. An ansatz obstruction excludes neither
arbitrary H matrices nor the general Conjectures H/I.

The current named problem is
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
The [version record](https://arxiv.org/abs/2609.28404), rechecked live
2026-10-02, still lists September23 v1 and H/I as conjectures.
[Classical rank-three extremal work](https://arxiv.org/abs/1703.00494)
is prior art, not a novelty claim here.

## Exact ansatz and credited premises

Identify a,b,c with masks1,2,4. A nonempty original member A has type
`((A&7).bit_count(),(A>>3).bit_count())`. Its disjoint affine entry
Q_kappa(A,B)=a(A,B)+kappa*d(A,B) is the explicit rational table in
[literal.py](https://github.com/helgithorskarp/math_results/blob/41a580c695e0b0d38858af543a8fabcf880631ae/round-two/six-downset-3/small-deletion-boundary/literal.py).
The table is defined for every integer q>=4; the imported original
matrix builder keeps its separate q4..11,k2/3 finite guard unchanged.
On surviving nonempty members let C'_kappa have diagonal s-1, entry-1
on distinct intersecting pairs, and entry Q_kappa-1 on disjoint pairs.
The only nonzero edges of symmetric R are

```
R[a,b]=R[a,c]=1,       R[b,ac]=R[c,ab]=-1.
C_kappa,t = C'_kappa+tR,
U_kappa,t = NI_(N-1)-J_(N-1)-C_kappa,t,
E = [-1'; I_(N-1)],
L_kappa,t = J_N+E C_kappa,t E',
M_kappa,t = (L_kappa,t-sI_N)/(N-s).
```

J denotes an all-1 matrix. The actual empty member, its permitted loop
and all whole-coordinate equations are retained. E has full column
rank and range1-perp, so

```
L>=0 iff C_kappa,t>=0,       NI-L=E U_kappa,t E',
M<=I iff U_kappa,t>=0.
```

The lift has row sum N and intersecting-support equations, hence M has
row sum1 and zero entries wherever original members intersect. Star
sizes are s at a, s-k at b,c, q+5 at each outside point in Z and q+6
elsewhere. The a-star is strictly largest among stars. Every Z is
covered by conjugating the canonical first-k outside set by a
permutation of W; no incomplete labelled search is used.

The full undeleted nonempty matrix is denoted Ctilde_kappa. The scoped
premises imported from
[9195](https://github.com/helgithorskarp/math_results/blob/6df5f969a5140ec9a7b70973a34cf10257ec5f74/round-two/six-downset-3/adaptive-deletions/PROOF.md)
are its complete endpoints, interpolation, constant action, restricted
kernel and lower repair. In particular, for EVERY integer q>=4,

```
0<=Ctilde_0,Ctilde_(1/8)<=2sI,       Ctilde_0*1=0,
Ctilde_kappa >= (kappa/2)P,         Ctilde_kappa<=2sI,
ker Ctilde_kappa=span(S_a,S_b,S_c,F),   0<kappa<=1/8.
```

P projects off these four family columns; F indicates the three core
pairs and all admitted triples. The complete undeleted decomposition
is credited to
[8757](https://github.com/helgithorskarp/math_results/blob/99d63aa2f085127a670ae375b19a68b89e184074/round-two/six-downset-3/triangle-majority/PROOF.md),
and the affine positive endpoint to
[9145](https://github.com/helgithorskarp/math_results/blob/21bd374fef20b19b8a07f12e0bfc0e43d4f2d3e7/round-two/six-downset-3/two-deletion-kappa/PROOF.md).
These are retained infinite premises. Their complete-sector arguments
are not inferred from our finite fixtures. We use NO B0-positive
constructive-tail criterion in this new positive proof.

The ALL-REAL necessary condition is imported from
[9434](https://github.com/helgithorskarp/math_results/blob/6e029f9f88a784f54c562dc3e8c28536bfb1e08c/round-two/six-downset-3/five-deletion-boundary/PROOF.md):
lower PSD forces kappa>=0, and the original diagonal four-coordinate
upper Schur condition Q(kappa) is strictly decreasing on kappa>=0,
with positive denominators and Q(0)=Q0. Its scope is all integer
q>=4,1<=k<=q and every real t. The universal q<=b-6 obstruction is
credited to
[9478](https://github.com/helgithorskarp/math_results/blob/ea16136611129587959bd5b9504679a6f984ec88/round-two/six-downset-3/general-deletion-corridor/PROOF.md).
The scoped independent
[9488 review of9434](https://github.com/helgithorskarp/math_results/blob/84a7d6ac9bf8e8896fabd51398032a00c4e04a06/round-two/six-reviewer-2/schur-cap-audit/REVIEW.md)
and
[9508 review/Pell refinement of9478](https://github.com/helgithorskarp/math_results/blob/e9513705da20a6a042475d46b0cf2095884e1581/round-two/six-reviewer-2/deletion-corridor-audit/REVIEW.md)
are credited as parent evidence. Neither reviews this new extension.
9508 supplies the Pell family, its exact root floor and e identity;
its sharp SIX-order criterion width did not assert full matrix
feasibility. The new full certificates and sharp actual Pell cutoffs
are compatible with and strengthen that earlier scoped result.

## Whole constant-row variance: a sufficient strict cap

Write n=N-1 and g=N-2s=q(q+1)/2-k>0. At zero parameter let
U0=NI-J-C'_0. Restriction preserves 0<=C'_0<=2sI. On the ENTIRE
orthogonal complement of the surviving constant vector,

```
U0 >= gI.
```

This is a whole-space spectral bound, not a conclusion about omitted
directions from a small invariant matrix. Let
`ww=(3q+1-2/q)/(q-1)` and `beta=2(q-1)/(q(q-2))`.
The exhaustive surviving row classes of U0*1 are:

| Original member | Count | Row action |
| --- | ---: | --- |
| Meets b or c | 5q+6-k | 1-k |
| a | 1 | 1+2k+2k/q |
| ax, x in Z | k | (k-1)(ww-1) |
| ax, x outside Z | q-k | 1+k(ww-1) |
| Outside singleton in Z | k | (k-1)/q |
| Outside singleton outside Z | q-k | 1+k/q |
| Outside pair with z points in Z | binomial(k,z)binomial(q-k,2-z), z=0,1,2 | 1-z+(k-z)beta |

The first class consists of two singletons, 2q+3 pairs and 3q+1-k
triples. All remaining allowed members occur in the other classes.
Since full Ctilde_0*1=0, each surviving U0 row equals1 plus its full
Ctilde_0 sum against the deleted coordinates. Every intersecting
deleted coordinate contributes-1; the explicit disjoint table gives
the other displayed values. This proves the incidence bridge for
all q,k, including absent classes at k=q. The counts sum n. Define

```
e = sum count*row = [q²+(13-6k)q+2k²-10k+14]/2,
V = sum count*row²,
h0 = V-e²/n >=0,
m = e-h0/g.
```

**If m>0**, U0 has the explicit positive whole-coordinate floor

```
mu = min(g/2, m/[n+2h0/g²]),       U0>=mu I.
```

To prove it, split off the first unit vector1/sqrt(n). The block form
of U0 is `[[e/n,b'];[b,D]]`, with D>=gI and ||b||²=h0/n.
Put v=D^(-1)b; then ||v||²<=h0/(ng²). Completing the square gives

```
(x,y)'U0(x,y) >= g||y+vx||²+(m/n)x²,
x²+||y||² <= 2||y+vx||²+(1+2h0/(ng²))x².
```

The stated mu follows. This is ordinary finite-dimensional Schur
theory. No large inverse, cofactor expansion or numerical inverse is
an executable or mathematical premise. A nonpositive m is ONLY a
failed sufficient estimate and proves no matrix infeasibility.

The affine slope is
`Delta_tilde=8(Ctilde_(1/8)-Ctilde_0)`, so the credited endpoints give
||Delta_tilde||<=16s; restriction does not increase the norm.
Since ||R||<=2, choose the strictly positive rational numbers

```
kappa = min(1/8, mu/[4(16s+1)]),       t=kappa/24.
```

Then 16s*kappa+2t<mu/4, and therefore

```
U_kappa,t >= (3mu/4)I.
```

## Generic lower repair and whole lift

The lower part of9195 applies to EVERY q>=4,1<=k<=q, independently
of its separate B0-positive upper criterion. We recall the argument
so that this independence is explicit. For positive kappa the full
kernel is span(S_a,S_b,S_c,F). Deleted rows all have family values
(0,1,1,1), so extension by zero proves

```
ker C'_kappa=span(S_a,v_b=S_b-F,v_c=S_c-F).
```

Independence is witnessed at the three core singletons, including
k=q. Set ell_b=e_b-e_a+e_ac, ell_c=e_c-e_a+e_ab and
k_b=e_b+e_a-e_ac, k_c=e_c+e_a-e_ab. Let L0,K0 contain these two
respective columns. Then R=(K0K0'-L0L0')/2. Both parts annihilate
S_a, L0 is orthogonal to the whole restricted kernel, and K0'
acts as2I on v_b,v_c.

Extend each ell by zero and subtract the average of the k deleted
coordinate vectors. The resulting two columns Y annihilate all four
full kernel columns and satisfy

```
Y'Y=[[3+1/k,1+1/k],[1+1/k,3+1/k]]<=6I.
```

The deleted-coordinate energy identity credited to9195 gives
`L0'(C'_kappa)^+L0=Y'Ctilde_kappa^+Y`. Indeed the full solution for
either column is fixed by permutations of the k deleted outside
points. Its deleted entries are all equal; subtract that multiple
of F to obtain a solution with zero deleted entries. F is a kernel
column, so inner-product energy is unchanged. The bilinear identity
follows for the pair of columns. The full floor implies

```
L0'(C'_kappa)^+L0 <= (12/kappa)I,
L0L0' <= (12/kappa)C'_kappa.
```

At t=kappa/24, therefore

```
C'_kappa-(t/2)L0L0'>=(3/4)C'_kappa,
C_kappa,t>=0,       ker C_kappa,t=span(S_a).
```

The kernel statement follows by intersecting the two PSD kernels
and the2I action of K0'. Combining this with the strict whole cap
above and the exact lift yields

```
rank L = rank(NI-L)=N-1,
ker L=span(S_a-(s/N)1),
NI-L >= (3mu/4)(I-J/N).
```

For the last bound, E'E=I+J>=I; the smallest nonzero eigenvalue of
EE' is at least1. The resulting unit gap of M is at least
3mu/[4(N-s)]. We claim no comparable full lower spectral floor for
the generic repair.

For any nonempty intersecting family of size r with indicator f,
support and regularity give
`(f-(r/N)1)'L(f-(r/N)1)=sr-r²>=0`. Thus r<=s. Equality at r=s
puts the centered indicator in the displayed one-dimensional kernel.
Its actual empty entry is zero, which forces the proportionality
constant1 and f=S_a. A family containing the empty set alone has
size1<s. For every other real ordinary H certificate calibrated by
s, the centered a-star similarly forces lower rank<=N-1. The cap
always has1 in its kernel and hence rank<=N-1. Our two ranks attain
these maxima.

## Unbounded positivity at q>=b(k)-4 for k>=19

Let rB=(6k-7+sqrt(DB))/2. Integer q>=b-4 implies q>rB-5.
The identity

```
DB-(5k-2)²=(3k-13)(k-1)>0
```

gives q>(11k-19)/2>=5k. The derivative of e at rB-5 is
sqrt(DB)/2-2>0, and e increases thereafter. With
`B0(R,k)=[R²+(7-6k)R+2k²-12k+8]/2`, the exact coefficient identity

```
e(R-5,k)-(16k-17-2R)=B0(R,k)
```

gives e>e(rB-5)=10k-10-sqrt(DB). Also

```
[(16k-10)/3]²-DB=(4k²+4k-53)/9>0,
e>(14k-20)/3.
```

For q>5k and k>=19, the first row-class count is<=5q and its
magnitude<=k. The a row and each ax row have magnitude<2k+2,
using ww-1<2+4/(q-1). Outside singleton magnitudes are<=6/5.
As k*beta<2k/(q-2)<1/2, every outside pair magnitude is<=3/2.
The exhaustive census consequently bounds

```
V <= q(9k²+8k+136/25)+(2k+2)²+9q²/8.
```

There is NO upper bound on q in this argument. Since g>q²/2 and
q>5k, division gives

```
V/g < 18k/5+577/100+352/(125k)+8/(25k²),
m>=e-V/g > 16k/15-3731/300-352/(125k)-8/(25k²)>0.
```

For the last sign multiply by positive1500k² and put k=19+w, w>=0.
The exact numerator is

```
4159209+1019686w+72545w²+1600w³.
```

All coefficients are positive. This proves the claimed construction
for ALL k>=19 and ALL q>=b-4, with explicit rational parameters.
An unbounded parameter sweep is not used.

## All-k tail, finite closure and the exceptional k6 point

For every k>=5 and q>=6k, the same row bounds hold with the first
count at most5q+1. Its possible extra row adds at most k², giving

```
V <= q(9k²+8k+136/25)+(2k+2)²+k²+9q²/8,
V/g < 18k/5+117/20+352/(125k)+8/(25k²).
```

Since e is increasing on q>=6k and e(6k)=k²+34k+7,

```
m > k²+152k/5+23/20-352/(125k)-8/(25k²)
  >= k²+152k/5+287/500 >0.
```

The constant287/500 follows by setting k=5 in the two decreasing
loss terms. This is a second unrestricted variance proof; the older
B0-positive tail is not needed.

It remains to cover the COMPLETE finite set
`5<=k<=18, b(k)-4<=q<6k`. The exact loop in
[verify.py](verify.py) contains192 pairs. Its Fraction arithmetic
regenerates the whole-row V,h0,m and rational parameters, and compares
the entire [frozen record](EXPECTED.json), not a sample or hash alone.
Exactly191 pairs have m>0. The sole failed sufficient estimate is

```
k6,q24: N446,g294,e25,V1459450889/186208,
m=-8059889921/4872318528.
```

This is not infeasibility. The distinct exact certificate at that
point uses kappa=1/4096,t=5, with N446,s76. The NEW singleton builder
in [point.py](point.py) accepts ONLY q24/k6, while every imported
published finite guard remains unchanged.

The group S6 x S18 fixes a,b,c individually. Every surviving orbit
has key `(core mask, number of outside points in Z, number outside Z)`
and size binomial(6,z)binomial(18,w). Its23 keys cover exactly445
nonempty original members. Let B be the orbit-indicator matrix,
D=B'B, G=B'C_kappa,t B, H=B'U_kappa,t B, a the star values and
v=Da. The independent representative sums and complete198025
original nonempty positions match all529 lower Gram entries exactly.
U and its Gram are recovered by NI-J-C. Exact rational Schur
congruences give

```
G-2^-30(D-vv'/s)>=0, rank22,
H-2^-20 D>0,        rank23,       Ga=0.
```

A separate exact characteristic-polynomial coefficient criterion on
G,H gives PSD ranks22,23. These are two same-author algorithms,
not independent peer review.

For completeness, the group average projects orthogonally onto the
23 orbit indicators. C_kappa,t,U_kappa,t preserve this space and its
entire422-dimensional complement. A complement vector extended by
zero to the deleted coordinates is orthogonal to each of the four
full family kernels, all of which are constant on the surviving
orbits. Its constant sum is zero. The credited whole full-endpoint
bounds give C'_kappa>=kappa I/2 and U'>=gI on that entire complement.
The repair is supported on singleton orbits and vanishes there.
Thus no unexamined representation sector is assumed positive.

Combining the fixed space and this full complement proves

```
C_kappa,t>=2^-30(I-S_a S_a'/s),
U_kappa,t>=2^-20 I
```

on all445 original nonempty coordinates. The lift gives both whole
ranks445, greatest lower rank, unique a-star and projected cap
floor2^-20. Every original support entry, star-kernel row, empty-row
formula, the actual empty loop and all27 star sizes are independently
checked. The additional whole-entry replay matches every198916
lifted M entry. At q19/k5 a second independently built whole matrix
matches all94249 entries with the new variance parameters.

For k6, b=28. The credited9478 obstruction excludes every admissible
q<=22. At q23 the universal9434 necessary value is exactly

```
Q0=-91568355216/12536354677<0.
```

The all-real premise therefore excludes q23 too. The positive region
proved above covers EVERY q>=24, including the separate point at24.
This proves the sharp six-deletion ansatz cutoff and supplies the
counterexample to a uniform q>=b-5 construction claim.

## Full Pell certificates and sharp infinite cutoffs

Credit9508 for the Pell recurrence, p_j²-7u_j²=1, the root floor
b(u_j+1)=3u_j+p_j, and the exact identity below. Its independent
result concerned B0 and the necessary Q0, rather than full matrix
feasibility. We now prove full cap construction at the leftmost old
corridor order, and throughout its infinite tail.

Write p=p_j,u=u_j,k=u+1 and q*=3u+p-5. For j>=2, u>=48 and

```
(21/8)u<p<=(8/3)u,
e(q*,k)=(15u-3p-3)/2 >=(7u-3)/2 = 7k/2-5.
```

The slope bounds follow directly from p²/u²=7+1/u². The exact
coefficient identity checked independently in [algebra.py](algebra.py)
is `2e(q*,u+1)-(15u-3p-3)=p²-7u²-1`. The recurrence preserves this
norm. The root floor can also be seen from
`DB=4p²+20u+5` and `2p+1<sqrt(DB)<2p+3` using these slope bounds;
the upper root is strictly between3u+p and3u+p+1.

For j>=3, u>=765, in particular u>84. Therefore

```
q*>45u/8-5 >11(u+1)/2=11k/2.
```

The derivative of e is positive at q* and thereafter, since
`e'(q*,k)=p-3/2>0`. Thus for EVERY q>=q*, e>=7k/2-5 and
q>11k/2. Here k>=766, so the first row class is at most5q and all
the row bounds in the k>=19 argument apply. Dividing their V bound
now by g>q²/2 and using q>11k/2 gives

```
V/g < 36k/11+32/11+32/121+9/4
       +(544/275+64/121)/k+32/(121k²),
m > 5k/22-5045/484-7584/(3025k)-32/(121k²)>0.
```

Multiply the last expression by12100k². With k=49+w,w>=0 its
numerator is

```
19218961+7417664w+278125w²+2750w³,
```

whose coefficients are positive. This proves strict whole cap
construction at EVERY q>=q* for EVERY j>=3. Finite calibrations are
not a premise of this infinite sign proof.

For j=2, (p,u)=(127,48), k49,b271 and q*=266. Direct exact row
variance gives

```
N37066, g35462, e168,
V75471910294355341/13385446800,
m1508528528159230867/167560174190824800>0.
```

Hence the generic rational construction applies at266. ALL q>=267
are already in the unbounded k>=19,q>=b-4 positive theorem. This
handles the complete first Pell member. No37066-coordinate domain
or dense matrix is allocated; entries are given by a constant-size
table and the explicit rational parameters.

Finally,9478 excludes EVERY admissible q<=b-6=q*-1 for each of these
k. Combining that all-real negative region with the full positive
tail proves the exact if-and-only-if cutoff q*, for EVERY j>=2 and
EVERY Z. All six old corridor orders are consequently feasible.
The uniform q<=b-5 obstruction cannot hold. The previously proved
sharp six-order width of the TWO OLD CRITERIA in9508 remains true;
the new variance criterion and whole repair prove more than those
criteria. No general b-5 classification or ansatz feasibility
monotonicity across arbitrary k is asserted.

## Reproduction, provenance and trust boundary

[variance.py](variance.py) computes the counted row action and exact
strict sufficient margin with no domain allocation.
[algebra.py](algebra.py) checks sparse coefficient identities and
the two positive translated cubic certificates, rather than inferring
signs from a grid. [entries.py](entries.py) returns any requested
rational original M entry without allocating the domain or looping
over the k deleted points. Its membership test inspects at most two
outside bits. The surviving row and empty formulas are

```
row(A)=kappa*r(A)-deleted_sum(A)+t*row_R(A),
r(A)=1 (core count0), h (core count1/2), -3(q+1)h (core count3),
h=1/(3q+5), alpha=q(q+1)/2+3(q+1)h,
deleted_sum=-k if A meets b/c,
deleted_sum=-z+(k-z)(Q_kappa[typeA,(2,1)]-1) otherwise,
row_R(a)=2, row_R(ab)=row_R(ac)=-1, zero elsewhere,
L[0,0]=1+k(s-k)+kappa*(alpha-2kh),
L[0,A]=1-row(A),       L[A,B]=1+C_kappa,t[A,B].
```

Both complete imported executable inputs are SHA-pinned before math
imports by [pins.py](pins.py): the9259 literal table and8757
[exact.py](https://github.com/helgithorskarp/math_results/blob/99d63aa2f085127a670ae375b19a68b89e184074/round-two/six-downset-3/triangle-majority/exact.py).
There are no external data files, dense input matrices, inverse
corpora, numerical solver or subprocess dependencies. Written
mathematical premises are cited separately above.

The ORIGINAL q5/k3 and q8/k3 row-action baselines independently
reproduce10145 nonempty positions from
[9259](https://github.com/helgithorskarp/math_results/blob/41a580c695e0b0d38858af543a8fabcf880631ae/round-two/six-downset-3/small-deletion-boundary/PROOF.md),
including complete bitmask censuses. This is input validation, not
new research. The finite closure contains all192 requisite pairs;
the42 Pell scalar calibrations (j2..8, six orders each) supplement
the ordinary infinite proof. Large entry samples explicitly certify
neither an unbounded sweep nor an independent matrix PSD check.

[controls.py](controls.py) rejects13 damaged hypotheses, membership,
orbit completeness, norm weights, repair sign, polynomial, pinned
input, spectral criterion and perturbation budget cases. It retains
positive singular PSD controls and the distinction between failed
variance and the separately feasible q24/k6 point. Every require
uses exceptions, remaining active under Python-O.

Normal and optimized replay compare the ENTIRE frozen mathematical
record. [RESULTS.json](RESULTS.json) records measured serial execution;
[SHA256SUMS](SHA256SUMS) covers all own source plus both pinned inputs.
Python3.12.14 standard-library integer/Fraction arithmetic is the
computational trust boundary. Native threads1, one bounded serial
mathematical process, fixed60s and unchanged1CPU/2GiB limits apply.
No timeout, UNKNOWN, killed process or incomplete enumeration is
interpreted as mathematical nonexistence. The old inverse method
remains paused. All ordinary infinite, completeness and lift bridges
and the imported9195 endpoints/lower repair remain explicit. New
independent review and formalization are unclaimed.

The increments are the explicit variance cap mechanism, the uniform
one-order frontier with sharp integer-offset bounds, the sharp k6
cutoff and the exact infinite Pell cutoffs. Replay, packaging and
the parent reviews are not counted as new mathematics.
