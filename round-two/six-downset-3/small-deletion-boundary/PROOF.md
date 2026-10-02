# The exact three-deletion boundary of the affine triangle-majority repair

Author: **six-downset-3**, role **researcher**, 2026-10-02.
Status: author-checked computer-assisted lemma with ordinary, unformalized
lifting, convexity, energy and tail arguments. Independent review is pending.

## Statement and scope

Let q>=4 be an integer. On core points a,b,c and q outside points W,
take the empty set, all singletons and pairs, and every triple containing
at least two core points. Delete precisely bcx for x in Z, |Z|=k.
Write this downset D(q,Z), and set

```
N0=(q²+13q+16)/2,     N=N0-k,      s=3q+4,
h=1/(3q+5),          alpha=q(q+1)/2+3(q+1)h.
```

The affine table Q_kappa is exactly the credited table in
[weights.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/two-deletion-kappa/weights.py).
Its expanded constant and derivative coefficients are given in
[literal.py](literal.py). Define, on surviving **nonempty** members,

```
C_kappa[A,B] = s-1                   if A=B,
               -1                   if A intersects B and A!=B,
               Q_kappa[typeA,typeB]-1 otherwise,
typeA=(|A intersect {a,b,c}|, |A intersect W|).
R[a,b]=R[a,c]=+1, R[b,ac]=R[c,ab]=-1, symmetrically,
all other R entries zero.
C_kappa,t=C_kappa+tR,
E=[-1'; I_(N-1)],
L=J_N+E C_kappa,t E',    M=(L-sI_N)/(N-s).
```

**The sharp ansatz theorem:** for k=3, some real kappa,t make M a
**capped H certificate** if and only if q>=8. The infeasibility direction
covers **every real kappa and every real t**, without symmetry or sign
restrictions on these two parameters beyond the specified construction.
It excludes this exact affine-table/scalar-four-edge family only.

For q=8 the entire real rectangle

```
0<kappa<=1/4096,    3/8<=t<=1/2
```

works. For q=9,10,11 explicit positive parameters and every real
0<t<=tau work by finite cap continuity. For q>=12 the already published
adaptive parameters and interval of LEMMA9195 work.

**Two-deletion continuation:** for k=2, capped certificates in this same
ansatz exist for every integer q>=4. The new finite cases q=4,5,6 join
the unchanged kappa=1/8 construction and full real interval of LEMMA9145
at every q>=7.

All these positive certificates satisfy

```
M=M', M1=1, M[A,B]=0 when A intersects B,
L>=0, NI-L>=beta(I-J/N), beta>0,
rank L=rank(NI-L)=N-1,
ker L=span(S_a-(s/N)1).
```

The unit eigenvalue of M is simple; its gap is at least beta/(N-s).
Both ranks are greatest among the eligible H matrices on these domains.
All entries are rational at rational choices of the parameters.
The empty vertex and its actual permitted loop are included throughout.

For each q,k all choices of Z are equivalent under permutations of W.
The certificate is transported by the corresponding coordinate
permutation, so the finite exceptional census covers every Z. This is
a classification of four exceptional canonical **ansatz** classes and
a construction on two specified infinite cohorts, not an enumeration
of all downsets of any ground-set size.

The target is Conjecture H of
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4).
The [version record](https://arxiv.org/abs/2609.28404) was checked live on
2026-10-02: the September23 v1 leaves H and I open. The extra upper cap
M<=I is a strengthening used here, rather than an identification with I.
Neither the sharp ansatz obstruction nor a numerical search is a
counterexample to general H. No historical priority claim is made.

## Credited inputs and the actual increment

[LEMMA8757](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-majority/PROOF.md)
supplies the original complete harmonic framework. Its source commit is
99d63aa2f085127a670ae375b19a68b89e184074 and graph reference
`bafkreibofxgvkr2ds56flf6irwpvjl2uci5kuziwkfb6o4jziz3qfjx2dy`.

[LEMMA9145](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/two-deletion-kappa/PROOF.md)
supplies the affine table, the positive spectral endpoint and the entire
k2,q>=7 tail. Its source commit is
21bd374fef20b19b8a07f12e0bfc0e43d4f2d3e7 and graph reference
`bafkreiglo6fkpq3sc5ljzc6n2dw6asyygmle4cf56wqlnmyilxcrwuw5ia`.

[LEMMA9195](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/adaptive-deletions/PROOF.md)
supplies the zero endpoint, full positive interpolation, the
deleted-coordinate energy identity and the k3,q>=12 tail. Its source
commit is 6df5f969a5140ec9a7b70973a34cf10257ec5f74 and graph reference
`bafkreihheqg5ispobqtthf6b4kucvyrgcllkg7lxxfuveveio7l26m3evm`.
The generic four-edge/deletion mechanism originally credits
[LEMMA8826](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-deletions/PROOF.md),
source778a2e4e3c3f38eefd232be2d10985168619eb42,
`bafkreiadzt4tymbaupbksv26ffppn2c6qzhoncjy434do7aufw5mttnqvu`.

The increment is the compact real-parameter dual obstruction for
k3,q4..7, the positive q8 rectangle, and the six exceptional
cap-continuity cases. The unbounded tails and their parameter formulas
are retained and credited, not rediscovered by sampling. The previous
B0>0 scalar sufficient condition has k3 cutoff12 and k2 cutoff7; it
was never an actual ansatz necessity condition. Here the positive
cases outside that bound and the separate ansatz necessity are proved.
No contradiction, correction or retraction of those inputs is asserted.
Previously published different certificates on isolated domains are
prior art, not new H existence merely because this ansatz is unified.

The arithmetic helpers and table producer are SHA-pinned by
[bootstrap.py](bootstrap.py). Their exact public historical versions
are required inputs. Independent checking within this source is by
one author and does not transfer an external-review verdict to the
new result or to its intervening dependencies.

## Reduction to the two original core inequalities

The table is affine over the reals: C_kappa=C_0+kappa Delta, with Delta
exactly the derivative table of literal.py. All displayed matrices are
indexed by actual original sets. The nonempty diagonal and intersecting
entries give L[A,A]=s and L[A,B]=0 for distinct intersecting members.
R uses only disjoint edges, has zero diagonal, R S_a=0 and total sum0.
Since E'1=0, L1=N1 and M1=1. Every family here has star sizes

```
a: s,   b,c: s-k,   x in Z: q+5,   x outside Z: q+6,
```

so s is the unique greatest star size and 0<s<N.

E has full column rank and column space 1-perp. For every y in R^(N-1),
v=E(E'E)^(-1)y is in 1-perp and E'v=y. Therefore

```
L>=0 iff C_kappa,t>=0.
```

One direction follows from L=J+E C E'; the other evaluates L on v.
Moreover the direct identity

```
NI_N-J_N = E (NI_(N-1)-J_(N-1)) E'
```

gives NI-L=E U_kappa,t E', where

```
U_kappa,t = NI_(N-1)-J_(N-1)-C_kappa-tR
          = U_0-kappa Delta-tR.
```

Full column rank makes its PSD condition equivalent to NI-L>=0.
Thus capped H feasibility in the specified ansatz is **exactly**
C_kappa,t>=0 and U_kappa,t>=0. This equivalence, including the whole
empty row and loop, is the bridge used by the dual certificates.

The closed empty formulas are also explicit. If rho(A) is the row sum
of C_kappa,t, then

```
rho(A)=kappa r(A)-sum_(x in Z) C_kappa[A,bcx]+t row_R(A),
r(A)=1 if typeA has zero core points,
     h if it has one or two core points,
     -3(q+1)h if it has three,
row_R(a)=2, row_R(ab)=row_R(ac)=-1, others0,
T=sum rho=kappa(alpha-2kh)+k(s-k),
L[empty,empty]=1+T, L[empty,A]=1-rho(A).
```

These are the credited full constant-action identities minus the
deleted columns. If A meets b or c their sum is -k. Otherwise, with
u=|A intersect Z|, the sum is -u+(k-u)(Q_kappa[typeA,(2,1)]-1).
The evaluator [entries.py](entries.py) uses these formulas without
allocating the domain. It checks membership and the stated parameter
regions; it accepts rational inputs while the theorem covers the real
intervals and rectangle. Matrices may have negative entries and are
generally uncentered; no probability-kernel or centered requirement
is imposed.

## Exact exclusions at q=4,5,6,7 for k=3

Let F indicate all admitted triples and the three core pairs on the
nonempty domain. Put z=1-S_b-S_c+F. The deleted triples have z=0.
For each of the four original finite domains the literal checker
verifies

```
C_0 z=0, Rz=0, z'Delta z=alpha>0.
```

The alpha values at q4..7 are185/17,159/10,504/23,376/13.
Consequently z'C_kappa,t z=kappa alpha<0 whenever kappa<0,
for every real t. This excludes all negative kappa by the lower PSD
condition and supplies the necessary parameter-domain bridge for the
upper duals below.

For q=4, N=39,s=16. The original nonempty constant vector gives

```
1'U_0 1=-1, 1'Delta 1=179/17>0, 1'R1=0.
1'U_kappa,t 1=-1-(179/17)kappa<0 for every kappa>=0.
```

Equivalently the actual whole empty diagonal of NI-L is negative.
This rank-one PSD dual excludes the remaining real parameters at q4.

For q=5,6,7, [DUALS.json](DUALS.json) supplies two small integer vectors
u,v indexed by ascending surviving nonempty bitmasks, and a positive
rational lambda. The bit convention is a=1,b=2,c=4 and outside points
8,16,...; the first three outside points form canonical Z. There are
respectively49,61,74 coordinates. Define the PSD dual

```
Q=u u'+lambda v v'.
A=trace(Q U_0), D=trace(Q Delta), H=trace(Q R).
```

All pairings are recomputed from the literal original entries by
[duals.py](duals.py), using only Python's standard library and
literal.py, rather than the imported table producer, a sector decoder,
matrix elimination, a solver, or the discovery search. The exact
combined values are

| q | N | lambda | A | D | H |
|---:|---:|---:|---:|---:|---:|
|5|50|3|-14944/5|1157793/100|0|
|6|62|16/21|-6736/105|3922568/2415|0|
|7|75|2/3|-66508/105|49758757/1365|0|

For every kappa>=0 and every real t,

```
trace(Q U_kappa,t)=A-kappa D-tH=A-kappa D<0.
```

The trace pairing of two PSD matrices cannot be negative, since it
equals ||U^(1/2) Q^(1/2)||_F². Thus the upper condition is impossible.
Together with the lower z test, this excludes **all real** kappa,t.
There is no incomplete-search, timeout or floating-point inference.
Discovery cuts are not premises of the proof; only the compact
literal witnesses and their exact signs are published.

## Positive q8: four corners give a real rectangle

For q=8,k=3,N=89 we check the repaired matrices directly, without
assuming a zero seed cap or a t<=kappa/24 energy bound. The four corners are

```
kappa in {0,1/4096}, t in {3/8,1/2}, eta8=2^-20.
```

Exact fraction-free congruences in [finite.py](finite.py) establish:

| kappa | t | rank C_kappa,t | rank(U_kappa,t-eta8 I) |
|---:|---:|---:|---:|
|0|3/8|86|88|
|0|1/2|86|88|
|1/4096|3/8|87|88|
|1/4096|1/2|87|88|

All eight forms are PSD. At kappa=0 the lower kernel is
span(S_a,z); at kappa=1/4096 it is span(S_a), since the star action is
zero and the rank is87 in dimension88. The second direction at the
zero corners is checked literally, and is independent of S_a (outside
singletons have z=1 and S_a=0).

C_kappa,t and U_kappa,t are affine in the pair (kappa,t). Every point
of the closed rectangle [0,1/4096] x [3/8,1/2] is a convex combination
of its four corners. Thus C>=0 and U>=eta8 I throughout. Whenever
kappa>0, the total weight of positive-kappa corners is positive and
their kernels are span(S_a). For PSD forms the kernel of a convex
combination is the intersection of the kernels with positive weights.
It follows that the lower kernel is exactly span(S_a). This proves
the entire positive-kappa real rectangle including both t endpoints.
It does not assert the interval0<t<=1/2 at q8.

## Six finite cap-continuity bridges

Take the six pairs (q,k)=(4,2),(5,2),(6,2),(9,3),(10,3),(11,3).
Literal exact congruences establish

```
U_0>=eta I, eta=1/4096.
```

They also compute the symmetric absolute derivative row norm
d=max_i sum_j |Delta_ij|. Since Delta is symmetric, ||Delta||_2<=d.
The exact d values and positive rational choices are

| q | k | N | d | kappa=eta/(2d) | tau=kappa/24 |
|---:|---:|---:|---:|---:|---:|
|4|2|40|22/17|17/180224|17/4325376|
|5|2|51|59/50|25/241664|25/5799936|
|6|2|63|129/115|115/1056768|115/25362432|
|9|3|104|2825/2688|21/180800|7/1446400|
|10|3|120|937/900|225/1918976|75/15351808|
|11|3|137|19447/18810|9405/79654912|3135/637239296|

All kappa<=1/8. Consequently

```
U_kappa=U_0-kappa Delta >= (eta-kappa d)I >= gamma I,
gamma=eta/2=1/8192.
```

The lower repair uses the credited **full-domain** interpolation and
deleted-coordinate energy identity of9195; it does not assume that
restriction preserves its spectral floor. For every q>=4 and
0<kappa<=1/8 the full, undeleted seed satisfies

```
C_full,kappa >= (kappa/2)P,
ker C_full,kappa=span(S_a,S_b,S_c,F),
```

with P its range projection. These intermediate facts do not require
B0>0. Upon deleting bcx, the restricted seed C' has kernel
span(S_a,v_b=S_b-F,v_c=S_c-F): zero extension imposes one equation
on the full kernel, since each removed coordinate has family values
(0,1,1,1). Put

```
ell_b=e_b-e_a+e_ac, ell_c=e_c-e_a+e_ab,
K_b=e_b+e_a-e_ac,   K_c=e_c+e_a-e_ab,
L0=[ell_b,ell_c], K0=[K_b,K_c].
R=(K0K0'-L0L0')/2.
```

The negative columns kill the restricted kernel; K0' kills S_a and
has the matrix2I on (v_b,v_c). To justify the energy bound, extend
ell by zero on the removed coordinates and subtract the vector
which is1/k at every deleted coordinate. Call the two columns Y.
They kill the full kernel and

```
Y'Y=[[3+1/k,1+1/k],[1+1/k,3+1/k]]<=6I.
```

Each solution w=C_full,kappa^+ y is invariant under permutations of Z,
so all deleted coordinates have one value z0. Subtracting z0 F gives
a solution with zero removed coordinates and unchanged inner-product
energy; restricting it solves C' w_R=ell. Bilinearly this proves

```
L0'(C')^+L0=Y'C_full,kappa^+Y <= (12/kappa)I,
L0L0'<=(12/kappa)C'.
```

For every real0<t<=tau=min(kappa/24,gamma/4),

```
C'+tR >= (1-6t/kappa)C'+(t/2)K0K0'
       >= (3/4)C'+(t/2)K0K0' >=0,
ker(C'+tR)=span(S_a),
U_kappa-tR >= (gamma-2t)I >= (gamma/2)I,
```

because ||R||<=2. For the six values above kappa/24 is indeed the
smaller interval bound. This proves the whole real interval, not just
the rational endpoints tested in the whole matrices.

## Unbounded tails and whole greatest rank

For k=2,q>=7 use exactly the kappa=1/8,chi,gamma,tau formulas and proof
of9145. For k=3,q>=12 use exactly the adaptive formulas and proof
of9195; its B0 polynomial has first positive q12 for k3. The scalar
factory [boundary_parameters.py](boundary_parameters.py) imports the
SHA-pinned tail selector of9195 and the credited selector of9145.
No finite sample is used to infer these unbounded assertions.

On all positive cases the repaired core has kernel span(S_a) and
U_kappa,t>=beta I with beta=2^-20 on the q8 rectangle,
beta=1/16384 on the six continuation intervals, and beta=gamma/2 on
the credited tails. For any v perpendicular to1,

```
||E'v||²=||v||²+N v_empty²>=||v||².
```

Therefore NI-L>=beta(I-J/N), with kernel exactly span(1) and rankN-1.
Since J and ECE' are PSD and orthogonal on their ranges, the lower
kernel consists of v with 1'v=0 and E'v in span(S_a). This is precisely
span(S_a-(s/N)1), hence rankL=N-1.

For any H matrix on this downset, the support gives S_a'L S_a=s² and
row sums give L1=N1. Thus (S_a-(s/N)1)'L(S_a-(s/N)1)=0. PSD forces
this nonzero vector into the lower kernel, so rankL<=N-1 universally.
For the cap, (NI-L)1=0 always gives rank(NI-L)<=N-1. Our ranks attain
both bounds. Dividing the projected cap by N-s gives the stated
normalized unit-eigenvalue gap. These are ordinary lifting and rank
deductions, not additional finite-search claims.

## Exact replay and trust boundary

[verify.py](verify.py) runs serial processes with fixed60s per task and
all numerical-library thread counts1. [EXPECTED.json](EXPECTED.json)
contains the complete regenerated record, including matrix/domain
hashes, scalars and ranks. Every require is a runtime exception,
retained under python -O. No solver or floating-point spectral step
is used. Timing measurements have no mathematical role.

The finite certificate consists of six shifted zero-cap forms, eight
q8 corner forms, and fourteen whole forms (lower and projected cap on
each of seven positive domains): **28 exact PSD congruences** in total.
Every zero-cap and shifted-cap form is positive definite. Domain
enumeration by combinations is compared with a full bitmask membership
scan; all stars, downward closure, support, rows, restricted kernels,
zero endpoint extra direction and actual empty entries are checked.
There are60,076 distinct ordered whole entries across the seven
matrices, each compared with the separate closed evaluator. The
largest whole dimension is137. Only the canonical original domains
for this family are enumerated.

The exact checker clears a positive common denominator, verifies
symmetry and performs fraction-free Schur elimination. A negative
pivot rejects PSD; a zero pivot requires its remaining row to vanish;
a positive pivot removes one rank and updates the symmetric Schur
complement by exact integer division. The positive rescalings preserve
congruence. Induction proves that acceptance is equivalent to PSD,
and counts the rank, including singular endpoints. This is a
reproducible finite proof computation, not a hash standing in for
mathematics. No bulky inverse or elimination transcript is imported.

The dual replay is separate literal quadratic arithmetic with all
vectors and positive weights public. [controls.py](controls.py)
rejects26 meaningful corruptions: missing classes/corners, vector
dimensions, a changed b coefficient, PSD-weight signs, repair
cancellation, derivative and upper-pairing signs, singular/negative
Schur behavior, exactness, actual empty entries, row-preserving
intersecting support damage, domain order, deleted/unadmitted members,
unproved parameter regions, wrong derivative norms, and helper pins.
The finite producer and literal replay are different same-author
algorithms, not independent peer review.

The normal and optimized complete mathematical records agree; detailed
compact validation and expected hashes are in [RESULTS.json](RESULTS.json).
The unbounded interpolation, energy, real convexity/interval, tail and
whole-matrix reductions remain ordinary unformalized proof inputs.
The earlier costly symbolic inverse expansion was unnecessary for
these finite original-domain proofs and is not resumed. Timeouts or
incomplete experiments are not used as infeasibility evidence.
