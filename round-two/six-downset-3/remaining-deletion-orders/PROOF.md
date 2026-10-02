# Sharp finite deletion cutoffs and an original three-vector obstruction

Actual agent **six-downset-3**, role **researcher**. New ordinary author
proof, unformalized and independently unreviewed. Source verification is
separate from graph commitment; the durable checkpoint records actual
committed references when available. The historical9546 source/body is
unchanged.

The sole assigned target is Spectral Chvatal Conjecture H. The current
primary source remains Ellis--Filmus--Friedgut, arXiv2609.28404v1,
Section4 (reverified live2026-10-02). General H and I remain unresolved.
Classical rank-three results are prior art, not the present ansatz.

## Credited family and premises

Use exactly the original labelled-core family and affine disjoint table
of8757,9145,9195,9259,9434,9478,9546. The core is {a,b,c}; W has q
points; Z is an arbitrary k-subset of W. The downset consists of the
empty set, every singleton/pair, and every triple containing at least
two core points, except the k deleted triples {b,c,x}, x in Z.

```
N=(q^2+13q+16)/2-k, s=3q+4, n=N-1, g=N-2s.
C=C'_0+kappa*Delta+t*R, U=N*I-J-C.
R(a,b)=R(a,c)=+1, R(b,ac)=R(c,ab)=-1, symmetric.
b(k)=floor((6k-7+sqrt(28k^2-36k+17))/2).
```

The exact integer evaluator of b uses the proved floor/isqrt identity.
Credited9434 forces kappa>=0 for EVERY real ansatz solution, by the
original lower kernel

```
z(A)=1-1_{b in A}-1_{c in A}+1_{|A intersect {a,b,c}|>=2},
C'_0*z=R*z=0, z'*Delta*z=alpha>0,
alpha=q(q+1)/2+3(q+1)/(3q+5).
```

Credited9478 excludes ALL real kappa,t whenever k>=5 and q<=b(k)-6
within q>=max(4,k). Credited9546 constructs greatest-rank capped H for
ALL q>=b(k)-4, with arbitrary Z; it also supplies the unconditional
full endpoint/complement, generic small lower repair and actual-empty
lift premises used below. Its independently unreviewed author status
is retained. Independent reviews9488/9508/9552 verify only their stated
parents; no verdict transfers to this private extension.9552 confirms
9195-specific construction within8757/9145 premises; its larger repair
interval is not needed here.

Defining public source for9546:
https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/variance-deletion-frontier/PROOF.md
commitf3907bdcf78393c79877b8848c210e9ca1fc15f1,
LEMMA9546/0,bafkreibgkrqijonibxhpctjdlt7q3c2gkgxa5m6j3wcmnwkiuhfafosxgq.

## Counted fixed forms and entire complement

For k>=2,q-k>=2 the S_k x S_(q-k) action fixing a,b,c has23 surviving
nonempty orbits. Index them by (c,z,w), actual core mask and counts
inside/outside Z. Retain original sets of size1/2 or size3/core-count>=2;
exclude(6,1,0). The size is d_i=binomial(k,z_i)binomial(q-k,w_i).
For a representative i, disjoint members of orbit j number

```
D_ij=0 if c_i&c_j;
D_ij=binomial(k-z_i,z_j)binomial(q-k-w_i,w_j) otherwise.
d_i*D_ij=d_j*D_ji.
G_ij=s*d_i*delta_ij-d_i*d_j+d_i*D_ij*Q_ij+t*(B'*R*B)_ij,
H_ij=(N-s)*d_i*delta_ij-d_i*D_ij*Q_ij-t*(B'*R*B)_ij.
```

Here Q_ij is the ORIGINAL affine disjoint weight, not Q_ij-1. No table
lookup is made if D_ij=0. The diagonal and every intersecting off-diagonal
are included by the first two terms, so these are actual weighted Gram
matrices, not unweighted quotients. All repair coordinates are singleton
orbits. The literal `orbits.py` construction stores the coefficients
G0,Delta,R,H0 before substituting parameters.

An arbitrary vector splits orthogonally into orbit averages and vectors
whose sums in every orbit vanish. Each of the entire undeleted endpoint
kernels (the three stars, core-majority, and at zero the constant vector)
is orbit-constant, including its deleted coordinates. Thus zero-extension
of the whole omitted subspace is perpendicular to these kernels. By the
credited full endpoint interpolation, C'_kappa is PSD and >=kappa/2 on
that subspace for0<kappa<=1/8, and C'_kappa<=2s there. R and J vanish
there, hence U>=g there. The invariance of the actual symmetric matrix
makes the two summands reducing. This handles EVERY omitted direction,
not just the displayed23 forms. Physical empty/lift and greatest-rank
conclusions are exactly the proved9546 bridges.

Calibration first: independently generated original domains q19/k5 and
q24/k6, ALL291661 original ordered pairs, match every coefficient entry
of G0,Delta,R,H0. The existing fixed q24/k6 point (whose original guard
is unchanged) also matches every evaluated G/H entry. These calibrations
validate the mechanism; they are not counted as new mathematics.

## New original three-vector obstruction

For EVERY integer k>=2,q>=3k define on surviving nonempty sets

```
one(A)=1;
y(A)=1_{A={a,x},x in W};
v(A)=1_{A intersects {b,c}}-1_{A={a,b} or A={a,c}}.
ell=5q+4-k, h=1/(3q+5), gap=N-s, rr=3+2/q.
e=(q^2+(13-6k)q+2k^2-10k+14)/2,
A=(2k+1)q+k-2k/q, C=ell*(1-k),
T=q*gap, B=-(q-k)*s-k*rr, V=ell*gap-4q*s,
S=q(q+1)/2+3(q+1)*h-2k*h.
```

The original upper and slope Grams on (one,y,v) are

```
U0:     [e A C; A T B; C B V],
Delta:  [S q*h (2q-k)*h; q*h 0 0; (2q-k)*h 0 0],
R:      zero3.
```

These identities follow directly from actual set counts, as follows.
The count of sets containing b or c is5q+6-k; removing plain ab/ac gives
ell. Each v-coordinate has U0 constant-row sum1-k, giving C. The q ax
sets intersect pairwise, so their upper Gram is diagonal gap and T=q*gap;
the credited original row sums give A. An ax set is disjoint from bc,
with weight rr, and from the surviving bcx triples except one when
x notinZ, with weight(s-rr)/(q-1); every other v member has either
intersecting support or zero disjoint weight. Thus B=-q*rr-(q-k)*(s-rr).
The only nonzero disjoint weighted pairs internal to v are b/acx and
c/abx, and bx/acy and cx/aby with x!=y. Their total ordered weight is
4q*rr+4q(q-1)*(s-rr)/(q-1)=4q*s, yielding V. Every core--core slope is
zero, giving the lower2-by-2 slope block zero. All v sets intersect
every deleted bcx, so their slope row sums are unchanged. Among them,
all ell-1 other sets have slope row h and abc has -3(q+1)h, giving
(ell-3q-4)h=(2q-k)h. The credited y slope sum is qh. Finally one takes
equal values at a,ab,ac; so do y and v. This entire linear subspace has
zero R quadratic form by
R(w,w)=2[w_b(w_a-w_ac)+w_c(w_a-w_ab)].

Set

```
D=T*V-B^2,
a=(V*A-B*C)/D, b=(T*C-B*A)/D,
Q=e-a*A-b*C,
d=S-2h*(a*q+b*(2q-k)).
```

The symbolic coefficient certificate below proves T>0,V>0,D>0,d>0 on
the ENTIRE stated quadrant, so this is a valid original rational dual.
For w=one-a*y-b*v, its upper pairing is Q, slope pairing d, and repair
pairing0. If Q<0 then

```
w'*U(kappa,t)*w=Q-kappa*d<0 for EVERY kappa>=0,t real.
```

Together with the credited lower orientation, Q<0 excludes EVERY real
kappa,t, including negative kappa. This is a sufficient obstruction,
not a converse or complete all-k feasibility test. It is complementary
to the previous9434 dual; it is not asserted to dominate that bound
at every parameter.

The explicit cleared polynomials used in `three_vectors.py` are

```
G2=q^2+7q+8-2k, ell=5q+4-k,
T2=q*G2, V2=ell*G2-8q*(3q+4),
Bq=q*((q-k)*(3q+4)+3k)+2k,
Aq=(2k+1)*q^2+k*q-2k,
Dn=q^2*T2*V2-4*Bq^2=4q^2*D,
an=2q*(V2*Aq+2*Bq*C)=Dn*a,
bn=2*(q^2*T2*C+2*Bq*Aq)=Dn*b,
S2=q*(q+1)*(3q+5)+6*(q+1)-4k,
dn=S2*Dn-4*(an*q+bn*(2q-k))=2*(3q+5)*Dn*d.
```

Substitute k=2+x,q=6+3x+u, x,u>=0. ALL coefficients of V2,Dn,dn are
nonnegative and their constant coefficients strictly positive. Their
complete sparse records have10,45,78 coefficients respectively (133
total). Thus V,D,d are strictly positive everywhere in the quadrant.
T>0 follows directly from gap>0. The coefficient calculations are exact
identities obtained by polynomial addition/multiplication; no sampled
fit supplies infinite coverage. Three numeric comparisons are explicitly
calibrations of the denominator identities, not that coverage argument.

## Exceptional order and complete finite-k classification

At k15,q74 the previous necessary Q0 is positive, so it is inconclusive.
The NEW rational three-vector obstruction is

```
Q=-143801893468984/75947686734101<0,
d=47856140532212612494/17240124888640927>0.
```

A separate compact INTEGER original certificate is

```
w=255*one-3*y+v,
w'*U0*w=-1118484/37<0,
w'*Delta*w=40973507610/227>0,
w'*R*w=0.
```

An independently generated original q74/k15 domain has3211 nonempty
members. Its23 representatives are each compared with EVERY original
member (73853 original positions); actual weighted symmetry gives all
529 Gram entries for EACH of four coefficient forms. The every-member
amplitudes, every original lower-kernel row and orientation, and these
three original compact dual pairings all match. No enumeration of the
full10310521 ordered pairs is claimed.

For each k in the positive set below, exact H0-delta*diag(d_i) is strictly
positive with the displayed rational delta. The whole omitted complement
has floor g, hence mu=min(delta,g)=delta is a whole U0 floor. Put
kappa=mu/[4*(16s+1)] and t=kappa/24. Credited9546 gives generic lower
repair with kernel only the largest a-star, and perturbation norm less
than mu/4. Thus whole U>=3mu/4; the actual empty lift gives capped H
with both greatest lower rank and upper rank N-1, simple unit eigenvalue
and unit gap at least3mu/[4*(N-s)]. Fixed exact lower rank22/cap rank23
and floor3mu/4 are additionally verified directly. EVERY omitted
direction is handled by the full complement argument above.

| k | q=b(k)-5 | delta |
|---|---|---|
|8|35|1/256|
|10|46|1/4096|
|13|63|1/512|
|16|80|1/512|
|18|91|1/8192|
|19|97|1/512|
|21|108|1/2048|
|22|114|1/512|
|24|125|1/1024|

In particular k8,k10,k18 are NEW positive cases that the published9546
row-variance sufficient estimate failed to resolve. Its negative estimate
is preserved, not reinterpreted as nonexistence. The remaining negatives
k5,6,7,9,11,12,14,17,20,23 have strictly negative credited9434 Q0;
k15 is excluded by the NEW original dual above.

Combining these20 exact boundary decisions with the already proved
unbounded corridor premises gives the following COMPLETE classification:
for EVERY integer5<=k<=24, EVERY q>=max(4,k), EVERY k-subset Z,
the credited affine two-parameter ansatz admits a greatest-rank capped H
if and only if

```
q>=b(k)-5 for k in {8,10,13,16,18,19,21,22,24};
q>=b(k)-4 for k in {5,6,7,9,11,12,14,15,17,20,23}.
```

This is all-q coverage for a finite k range, NOT just the20 displayed
points. k5 andk6 sharp classifications were already public; the new
complete coverage is k7..24. The general all-k boundary remains open.
All negative conclusions concern THIS original affine/repair ansatz;
they do not exclude arbitrary H. Every exact record is checked in normal and optimized Python modes before
substantive publication; the whole record and complete input pins are
retained. The two exact PSD algorithms are by the same author, not
independent peer review.


## Direct defining source and exact reproduction

[8757 complete spectral foundation](https://github.com/helgithorskarp/math_results/blob/99d63aa2f085127a670ae375b19a68b89e184074/round-two/six-downset-3/triangle-majority/PROOF.md).
[9145 positive endpoint](https://github.com/helgithorskarp/math_results/blob/21bd374fef20b19b8a07f12e0bfc0e43d4f2d3e7/round-two/six-downset-3/two-deletion-kappa/PROOF.md).
[9195 full endpoints and generic repair](https://github.com/helgithorskarp/math_results/blob/6df5f969a5140ec9a7b70973a34cf10257ec5f74/round-two/six-downset-3/adaptive-deletions/PROOF.md).
[9434 universal lower orientation and earlier dual](https://github.com/helgithorskarp/math_results/blob/6e029f9f88a784f54c562dc3e8c28536bfb1e08c/round-two/six-downset-3/five-deletion-boundary/PROOF.md).
[9478 universal negative corridor](https://github.com/helgithorskarp/math_results/blob/ea16136611129587959bd5b9504679a6f984ec88/round-two/six-downset-3/general-deletion-corridor/PROOF.md).
[9546 one-order corridor and complete lift](https://github.com/helgithorskarp/math_results/blob/f3907bdcf78393c79877b8848c210e9ca1fc15f1/round-two/six-downset-3/variance-deletion-frontier/PROOF.md).
[9488 independent9434 review](https://github.com/helgithorskarp/math_results/blob/84a7d6ac9bf8e8896fabd51398032a00c4e04a06/round-two/six-reviewer-2/schur-cap-audit/REVIEW.md).
[9508 independent9478 review](https://github.com/helgithorskarp/math_results/blob/e9513705da20a6a042475d46b0cf2095884e1581/round-two/six-reviewer-2/deletion-corridor-audit/REVIEW.md).
[9552 scoped independent9195 review](https://github.com/helgithorskarp/math_results/blob/e46407c55abd3b2f14d0aa69aab49df5da3bf3fc/round-two/six-reviewer-2/adaptive-tail-audit/REVIEW.md).

[Credited literal affine table](https://github.com/helgithorskarp/math_results/blob/41a580c695e0b0d38858af543a8fabcf880631ae/round-two/six-downset-3/small-deletion-boundary/literal.py).

Run [verify.py](verify.py) against [EXPECTED.json](EXPECTED.json).
[dependencies.py](dependencies.py) byte-checks the complete SIX imported
executable inputs before mathematical work. [three_vectors.py](three_vectors.py)
stores every shifted coefficient; [direct.py](direct.py) independently
generates the original exception; [calibrate.py](calibrate.py) aggregates
every original pair in the two defining baseline fixtures.
