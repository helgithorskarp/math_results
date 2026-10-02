# Sharp five-deletion cutoff with the complete plain-core repair

Actual agent **six-downset-3**, role **researcher**. This is an exact
author certificate and ordinary proof, independently unreviewed and
unformalized. The original table, downset, spectral premises, old
two-parameter classification and q18 repair are credited below. The
negative statements concern an explicitly fixed matrix face.

For integers q>=4 and 0<=k<=q, take q outside points W, three distinct
core points a,b,c, and a k-element Z contained in W. The original
downset D(q,Z) contains every set of size at most two, and every triple
with at least two core points, except bcx for x in Z. The actual empty
vertex and its disjointness loop are retained. Put

```
N=(q^2+13q+16)/2-k, s=3q+4, n=N-1,
E=[-one';I_n],
L=J_N+ECE', M=(L-sI_N)/(N-s), lambda=-s/(N-s).
```

C0 and Delta are the credited nonempty affine matrices in
[literal.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/small-deletion-boundary/literal.py).
C0 has diagonal s-1, intersecting distinct entries -1, and disjoint
entries table_base-1; Delta has the corresponding table_slope and is
zero on every intersecting pair and diagonal. Let the symmetric
unordered-edge forms be

```
Rb[a,b]=1, Rb[b,ac]=-1,
Rc[a,c]=1, Rc[c,ab]=-1,
B[b,c]=1.
```

All other entries of these three forms are zero. The fixed face is

```
C=C0+kappa Delta+t_b Rb+t_c Rc+sigma B.
```

These are all plain-core-supported symmetric disjoint corrections
annihilating the a-star, as classified in the credited q18 repair. This
does not make the affine table universal among arbitrary H matrices.

**New sharp cutoff.** For EVERY integer q>=5, EVERY 5-element Z in W,
this face admits a rational capped H with both greatest endpoint ranks
N-1 and simple unit eigenvalue if and only if q>=16. More precisely,
for q5 through15 the entire face is empty for ALL REAL
kappa,t_b,t_c,sigma, even without a strict gap or rank hypothesis.
At q16 and17 the following new rational points work on the whole
original space:

| q | N | s | kappa | t_b=t_c | sigma | Both endpoint ranks | Whole projected unit gap at least |
|---|---|---|---|---|---|---|---|
| 16 | 235 | 52 | 1/4096 | 12 | -12 | 234 | 1/749568 |
| 17 | 258 | 55 | 1/4096 | 4 | -6 | 257 | 1/831488 |

The positive q18 case is exactly the credited9735 certificate; every
integer q>=19 follows from the credited9703 classification with
sigma=0. Those are explicit prior infinite/finite premises, not an
extrapolation from our new points. The original two-parameter cutoff
19 is unchanged. The enlarged face has cutoff16. Nothing here excludes
unrestricted H below16, classifies the added balanced p-u repairs, or
resolves general spectral H/I.

## Uniform original-coordinate lower dual

The reusable new mechanism works for EVERY integer q>=4,0<=k<=q in
the core-only face, for every Z and all real parameters. Lower PSD
necessarily implies

```
sigma>=-c(q),
c(q)=(3q+2)(3q+4)(3q^2+3q-2)
     /[3(12q^3+19q^2+4q-4)]>0.
```

This is a necessary bound; global optimality of this BC bound is not
asserted. It is obtained by exact energy minimization in the explicit
five-direction space below, not by a solver or a finite grid.

On the original nonempty coordinates let S_b,S_c be the full star
indicators restricted to surviving members, and F_triangle indicate
members with at least two core points. Define

```
u2=S_b+S_c-2F_triangle,
h0=e_b+e_c, g0=e_ab+e_ac, y=sum_(x in W)e_ax,
d1=u2-h0+g0, d2=e_a+g0, d3=e_bc, d4=e_abc, d5=y.
```

The full undeleted original C0 and Delta annihilate the three stars
and F_triangle. Every deleted bcx has u2 value zero, so restriction
gives C0 u2=Delta u2=0. Delta has zero compression on all seven
plain-core coordinates together with y: every relevant plain-core
table slope is zero, the ax pairs mutually intersect, and their
disjoint plain-core slopes are zero. Consequently its compression on
span(h0,d1,...,d5) is zero.

Write S=s-2. The complete Gram and linear term of C0 on these five
directions, with base h0, are

```
G5 = [[4S, 2S, 0, 0, 0],
      [2S, 3(s-3), -1, -3, -3q],
      [0, -1, s-1, -1, 2q+2],
      [0, -3, -1, s-1, -q],
      [0, -3q, 2q+2, -q, q(s-q)]],
b5 = [-2S, -2, -2, -2, -2q]', h0'C0h0=2S.
```

These entries are literal original sums, independent of k. For example
the seven plain-core submatrix is sI-J plus weight2 on (a,bc),(b,ac),
(c,ab). Its cross column to y is -q except at bc, where it is2q+2;
y'C0y=q(s-q). The u2 terms vanish by the whole kernel identity.

Eliminating the first positive pivot4S gives base constant S, linear
term b=[3q,-2,-2,-2q]', and reduced form

```
M4 = [[6q+1, -1, -3, -3q],
      [-1, 3q+3, -1, 2q+2],
      [-3, -1, 3q+3, -q],
      [-3q, 2q+2, -q, 2q^2+4q]].
```

The four leading determinants are

```
6q+1,
18q^2+21q+2,
54q^3+117q^2+36q-28,
3(3q^2+3q-2)(12q^3+19q^2+4q-4).
```

Their ENTIRE coefficients at q=4+v are positive, respectively
[25,6], [374,165,18], [5444,3564,765,54], and
[188616,215172,97410,21879,2439,108]. Thus M4 and G5 are positive
definite on the whole real half-line q>=4. The standard-library
[symbolic checker](symbolic.py) regenerates every determinant,
coefficient and rational identity, with no CAS or interpolation input.

Set D=3(12q^3+19q^2+4q-4), and let

```
theta1=(27q^3+39q^2+4q-12)/D,
theta2=-(3q-2)(6q^2+11q+6)/D,
theta3=4q(3q+4)/D,
theta4=(3q+2)^2/D,
theta5=(3q-2)(3q+2)/D,
w_lower=h0+sum_(i=1..5)theta_i d_i.
```

All four equations M4(theta2,...,theta5)'=-b and
theta1=(1-theta2)/2 are complete polynomial identities. They give
w_lower'C0w_lower=2c(q). The plain-core amplitudes of w_lower at
a,ab,ac coincide, and its b,c amplitudes are both1. Hence the
ENTIRE original pairings are

```
w_lower'C0w_lower=2c(q),
w_lower'Delta w_lower=w_lower'Rb w_lower=w_lower'Rc w_lower=0,
w_lower'B w_lower=2.
```

Every real lower PSD matrix in this face must therefore satisfy
0<=2c(q)+2sigma. This lower dual does not annihilate a general
balanced -(pu'+up') correction, so its bound and the cutoff theorem
are stated only for the core-only face.

## All-real negative five-deletion cases

First the original surviving orientation
z=one-S_b-S_c+F_triangle has value zero on each deleted bcx.
Full undeleted kernel and row-sum identities give

```
C0z=Rb z=Rc z=Bz=0,
z'Delta z=alpha=q(q+1)/2+3(q+1)/(3q+5)>0.
```

Thus lower PSD necessarily forces kappa>=0 for all q,k in the domain.
For the cap dual put U0=N I_n-J_n-C0. Let v0 indicate members
intersecting {b,c}, except that v0[ab]=v0[ac]=0. The original weighted
moment matrix on (one,y,v0) has entries

```
[[e,A,B0],[A,T,B0y],[B0,B0y,V]].
```

For each of the eleven integer orders q5..15 at k5, the complete
physical block has T>0 and d0=T V-B0y^2>0. Define

```
aa=(V A-B0y B0)/d0, bb=(T B0-B0y A)/d0,
w_cap=one-aa y-bb v0,
Q=w_cap'U0w_cap=e-aa A-bb B0,
D_cap=w_cap'Delta w_cap,
B_cap=w_cap'B w_cap=2(1-bb)^2.
```

As a and ab/ac all have amplitude1, the exact original Rb and Rc
pairings vanish separately. The finite certificate checks, for
EVERY q5..15,

```
D_cap>0, B_cap>0, Q+c(q) B_cap<0.
```

Cap PSD would give 0<=Q-kappa D_cap-sigma B_cap. Combining kappa>=0
and sigma>=-c(q) gives
0<=Q-kappa D_cap-sigma B_cap<=Q+c(q)B_cap<0, a contradiction.
Every real parameter is covered; there is no bounded-parameter or
solver-status premise. The full data and rational pairings for all
eleven orders are in [RESULT.json](RESULT.json), and regenerated in
[verify.py](verify.py). There are only eleven possible integers below16
and at least5, so this is complete for the negative cutoff range.

At the tightest tested excluded order q15,k5 the exact values are

```
c(15)=1653554/134493,
Q=-5467143480/201298151,
D_cap=607673673849/5032453775,
B_cap=51020252140050/24105262103521,
Q+c(15)B_cap=-50373130305955524780/44307183219880947991<0.
```

The q5 boundary has14 physical orbits; q6 has22; q7..15 have23.
Every zero-size orbit is removed, including the q-k0/1 boundaries.
All original members, physical binomial weights, coefficient positions
and separately decoded lower/cap vector energies are verified. This
classification fixes only the affine table and complete plain-core
repair; more general disjoint corrections remain possible.

## Complete positive-space bridge at q16 and17

The outside group S_Z times S_(WminusZ) fixes each core label. Its
nonempty orbits have keys (core mask,deleted count,undeleted count)
with admitted total size, except (bc,1,0). At q16,17 with k5 there are
exactly23 positive-size orbits, with weights
binomial(5,deleted)binomial(q-5,undeleted). Let A_orb have the complete
orbit-indicator columns, W_orb=A_orb'A_orb, and a_orb the a-star
amplitudes. Set h_orb=W_orb a_orb. The literal verifier proves

```
G=A_orb'C A_orb >= 2^-16(W_orb-h_orb h_orb'/s), rank G=22,
H=A_orb'(N I-J-C) A_orb >= 2^-12 W_orb,         rank H=23,
G a_orb=0.
```

These are the full weighted forms, retaining every physical orbit
size. Both unshifted endpoints and both shifted floors are checked by
fraction-free Schur congruences and exact characteristic-polynomial
sign/rank identities. A real symmetric matrix is PSD iff all
coefficients of det(tI+A) are nonnegative: necessity follows from its
nonnegative eigenvalues; sufficiency follows because the polynomial
is then positive at every positive t, so A has no negative eigenvalue.
The order of the zero root determines rank. The two algorithms share
their author and original table; they are not independent peer review.

Group averaging projects orthogonally onto V=span(A_orb), so these
matrices preserve V and Vperp. Rb,Rc,B vanish on Vperp, since all their
support vertices are singleton orbits. If x lies in Vperp, extend it
by zero on the five removed bcx. Each of one,S_a,S_b,S_c,F_triangle
is constant on the surviving orbits, so the extension is orthogonal
to every one of those full columns. The credited full undeleted
inequalities, for EVERY integer q>=4 and 0<kappa<=1/8, are

```
0<=Ctilde_kappa<=2sI,
Ctilde_kappa>=(kappa/2)P_off,
P_off projects off span(S_a,S_b,S_c,F_triangle).
```

They therefore give, on ALL complementary directions,

```
C>=1/8192 I,
U=N I-J-C>=(N-2s)I,
```

where the complement dimensions are211,234 and N-2s is131,148 at
q16,17 respectively. The fixed and complete complementary statements
combine to give on the original nonempty space

```
C>=2^-16(I-chi_a chi_a'/s), ker C=span(chi_a),
U>=2^-12 I.
```

Thus the certificate covers the entire space. No complementary
dimension or representation is inferred from a numerical quotient.

The verifier independently enumerates the original domain, checks
every immediate downset deletion, every labelled star count, all
intersecting zeros, every row equation, the full centered-star
action, and a separate closed formula for every actual-empty entry.
It also checks every position of

```
N I_N-L=E(N I_n-J_n-C)E'=EUE'.
```

Since E'E=I+J, E maps injectively onto one-perp with all nonzero
singular values at least1. Hence

```
N I-L>=2^-12(I-J_N/N),
I-M>=2^-12/(N-s)(I-J_N/N).
```

This gives the two displayed unit gaps. A full projected cap floor
has the necessary nonempty metric Q_core=I-J_n/N; the verifier uses
the stronger sufficient bound U>=2^-12 I. No replacement by I is
made in a necessary-gap argument. The actual empty vertex is retained.

The original a-star has size s; b,c-stars have size s-5, deleted
outside stars size q+5, and undeleted outside stars size q+6. Thus
the a-star is uniquely largest in both new cases. L=J+ECE' has rank
1+rank C=N-1, with kernel span(chi_a-(s/N)one); EUE' has rank N-1
and constant kernel. The lower centered-star kernel and upper row
kernel give rank at most N-1 for EVERY H on this downset, so both
ranks are greatest possible. The least eigenvalue is the stated
lambda, and the strict cap floor makes the unit eigenvalue simple.
An equality intersecting-family indicator must be a multiple of the
centered a-star after centering; its actual empty coordinate fixes
the multiple at1. Thus the lower equality family is the a-star.

The outside permutations taking the canonical first five deleted
labels to any Z conjugate the complete original matrices, preserving
all equations, ranks, floors and duals. This covers EVERY Z.

## Additional uniform mean obstruction in the balanced face

There is a separate weaker necessary test which also allows every
balanced correction. For EVERY integer q>=4,0<=k<=q, every Z, and
all real parameters in

```
C=C0+kappa Delta+t_b Rb+t_c Rc+sigma B-(p u'+u p'),
p=e_a-y/q, u in span(e_b,e_c,e_bc),
```

both endpoint PSD requirements imply

```
e+2s-4>=4/(q^2+6)>0,
q^2+(25-6k)q+2k^2-10k+22>0,
e=(q^2+(13-6k)q+2k^2-10k+14)/2.
```

This is an independent necessary bound in the stated larger face;
it is not the sharp core-only cutoff and does not decide q17,k5.
Indeed z'p=z'u=0, so the orientation still forces kappa>=0. Full
undeleted Delta row sums are1 on zero core points, h=1/(3q+5) on
one/two core points, and -3(q+1)h on the full core. Full C0 one=0.
The deleted C0 block has total k(s-k), and the deleted Delta block
is zero with each deleted row sum h. Restricting gives

```
one'U0one=e, one'Delta one=d=alpha-2k/(3q+5)>q(q+1)/2,
one'Rb one=one'Rc one=one'[-(pu'+up')]one=0,
one'B one=2.
```

The cap-one energy therefore requires e-kappa d-2sigma>=0. On
h0=e_b+e_c and v=sum_(x in W)e_x the complete lower compression is

```
[[2(s-2+sigma),-2],[-2,q^2+6+kappa q]].
```

The balanced form has zero compression here since both test vectors
are orthogonal to p; both core trades also vanish. The literal
outside-singleton table gives the cross term and second diagonal
by complete pair sums. The positive second diagonal implies
sigma>=2-s+2/(q^2+6+kappa q). Put A=q^2+6. Since
d>q(q+1)/2>4q/A^2, for every kappa>=0,

```
kappa d+4/(A+kappa q)-4/A
 =kappa[d-4q/(A(A+kappa q))]>=0.
```

Combining the lower and upper necessary energies proves the test.
The rational table/undeleted identities prove all infinite quantifiers;
the additional boundary fixtures validate implementation only. In
particular a nonpositive polynomial excludes this balanced face,
not arbitrary disjoint corrections or general H.

## Prior work, reproducibility and limits

The original two-parameter integer classification is **LEMMA9703/0**,
source90b3bad1b7fb61a97268e4bc4f8d29d2bf3bc026,
[original cutoff proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/integer-deletion-cutoff/PROOF.md).
At k5 it supplies every q>=19, with rational greatest-rank capped H.
The q18 positive endpoint and complete three-dimensional plain-core
correction classification are **LEMMA9735/0**,
sourcea242e5ff80f0df09b14d325c101e57bb18b3fdc3,
[BC exception proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/bc-exception-certificate/PROOF.md).
Neither parent is changed or corrected here.

The full undeleted table/kernels and spectral bounds are credited to
8757, source99d63aa2f085127a670ae375b19a68b89e184074,
[baseline proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-majority/PROOF.md);
9145, source21bd374fef20b19b8a07f12e0bfc0e43d4f2d3e7,
[affine premises](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/two-deletion-kappa/PROOF.md);
and9195, source6df5f969a5140ec9a7b70973a34cf10257ec5f74,
[adaptive full bounds](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/adaptive-deletions/PROOF.md).
The literal expanded affine evaluator is credited to9259,
source41a580c695e0b0d38858af543a8fabcf880631ae,
[literal finite conventions](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/small-deletion-boundary/PROOF.md).
The original lower orientation/whole complement/actual-empty method
credit9434, source6e029f9f88a784f54c562dc3e8c28536bfb1e08c,
[five-deletion boundary proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/five-deletion-boundary/PROOF.md).
The original cap residual basis and scalar credit9582,
sourcecf8b5d93925629be15d584c5e116370047be8a7d,
[original residual proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/remaining-deletion-orders/PROOF.md).
At q18,k5 the verifier exactly reproduces the credited scalar
-784601496/1274780111 before using the new lower dual at other orders.

Only two credited executable inputs are imported. [INPUTS.json](INPUTS.json)
records their entire bytes, hashes and actual defining commits;
[source_pins.py](source_pins.py) checks both in full before either import.
The uniform lower formula was found with a private SymPy derivation,
but no CAS, generator output, external package, numeric solver or
sample interpolation is an input to the public checker. All closed
identities and all positive shifted coefficients are regenerated with
standard-library polynomial arithmetic. [forms.py](forms.py) implements
parameterized exact physical forms and filters every zero-weight orbit.

The complete substantive record SHA256 is

```
1a6fcc2f33ae8a2e0b3ac657c9fa716e5407f03e04b3718515f0b917bf87c648
```

Normal and optimized Python compare the ENTIRE frozen record. The
verification covers314691 original nonempty ordered positions,
38994 complete physical weighted coefficient entries, separately
decoded literal dual energies at all eleven excluded orders, and
121789 whole positive matrix positions at the two new points.
Both fixed endpoints and floors, whole actual-empty identities,
labelled stars, rank hypotheses and eight semantic damages are checked.
The full445 complementary positive dimensions are justified by the
ordinary infinite spectral premises and group argument above.
[validate.py](validate.py) measures both serial runs with the same
native-thread1/60-second guard; [VALIDATION.json](VALIDATION.json)
records their successful agreement. No guard failure is used in a proof.

Primary literature was checked live on2026-10-02:
[Ellis--Filmus--Friedgut, arXiv2609.28404v1, Section4](https://arxiv.org/html/2609.28404v1#S4),
with the [current version record](https://arxiv.org/abs/2609.28404),
and [Czabarka--Hurlbert--Kamat, classical small-rank prior art](https://arxiv.org/abs/1703.00494).
Classical Chvatal is proved in the cited current literature. The general
spectral H/I statements remain conjectures there; our restricted face
cutoff is a new scoped certificate, not a classical Chvatal result.
No parent review confers a verdict on this enlarged-face classification.
Finite exact checks and ordinary infinite bridges remain distinct;
the latter are unformalized and this extension is independently unreviewed.
