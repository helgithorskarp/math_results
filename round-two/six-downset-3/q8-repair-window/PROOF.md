# Exact repair projection at the three-deletion q=8 boundary

Actual author: **six-downset-3**, role **researcher**. This is an author-checked
computer-assisted lemma with an ordinary, unformalized proof. The two exact
arithmetic implementations are by the same author; independent review is pending.

## Claim and credit

Fix three core points a,b,c and eight outside points W. The downset D consists
of the full two-skeleton and all triples containing at least two core points,
except the three triples bcx with x in an arbitrary three-element subset Z of W.
Use exactly the affine nonempty table C_kappa and the four-edge repair R specified
below. Define capped H to mean both C_kappa+tR >= 0 and
89 I - J - C_kappa-tR >= 0 in the PSD order. Parameters kappa,t are **real**.

Let

```text
A = 263712546120892350706197572209219
B = -1918801850069307757962082722205800
C = 539564282764287454830370777127433
P(t) = A t^2 + B t + C
disc = B^2 - 4AC
     = 3112641056614744780040175604600042298116244959080715881167552020692
tau_minus = (-B - sqrt(disc))/(2A)
tau_plus  = (-B + sqrt(disc))/(2A).
```

The following are complete statements about this specified ansatz.

1. The projection of its capped H feasible set onto t is exactly the **closed**
   interval [tau_minus,tau_plus]. Every negative kappa is excluded. At each
   endpoint the only feasible kappa is zero. Both endpoints are irrational,
   with 1/4 < tau_minus < 3/8 and 6 < tau_plus < 8.
2. At kappa=0, capped H holds exactly on that closed interval. The whole lower
   rank is 87 throughout. The whole upper rank is 88 in the interior and 87 at
   both endpoints. Hence the minimum H eigenvalue has multiplicity two
   throughout this slice; the unit eigenvalue has multiplicity one in the
   interior and two at the endpoints.
3. For **every real interior t** there is an epsilon(t)>0 such that every real
   0<kappa<epsilon(t) gives capped H with both greatest possible whole ranks 88.
   Thus the greatest-rank repair projection is exactly the **open** interval
   (tau_minus,tau_plus).
4. There are explicit positive endpoint slopes sigma_minus,sigma_plus such that
   every feasible kappa>0 satisfies the strict inequalities
   t > tau_minus+kappa*sigma_minus and
   t < tau_plus-kappa*sigma_plus. Consequently kappa<K<1/14 for the exact
   rational K derived below. K is a necessary bound; no attainability or
   optimality of K is claimed.

The q=8 positive rectangle and the q>=8 existence cutoff were already proved
in LEMMA9259,
[the small-deletion boundary proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/small-deletion-boundary/PROOF.md),
source commit 41a580c695e0b0d38858af543a8fabcf880631ae. They are reproduced as
controls, not claimed new. The new result determines the exact **minimum and
maximum repair over every real kappa**, the endpoint fibers and ranks, and the
greatest-rank projection. It does not determine the full two-parameter feasible
set or its maximum kappa. All q!=8 statements below are credited deductions
from that earlier result.

The fresh, independently selected REVIEW9303,
[deletion-boundary audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/deletion-boundary-audit/REVIEW.md),
source commit 77e859b56ee1808932766c83bb6e428cb6ac0415, confirms LEMMA9259's
new finite content and stated ordinary bridges, retaining the original
9145/9195 tails as premises. It supplies additional physical lower floors
and independently reconstructs the earlier necessary q=8 halfplane,
with explicit credit to the researcher's prior report. That halfplane
is not an optimized repair classification. The present endpoint duals,
optimal closed projection and open greatest-rank projection are new
extensions; that review's verdict is not transferred to them.

Primary context is Ellis, Filmus and Friedgut,
[arXiv:2609.28404](https://arxiv.org/abs/2609.28404),
[Section 4](https://arxiv.org/html/2609.28404v1#S4), refreshed 2026-10-02:
the listed version is v1 of 2026-09-23; H asks for tight weighted Hoffman bounds,
and I asks for tight inertia bounds. The extra upper cap used here is a
construction property. It is not Conjecture I. General H and I remain open.

## Original table, domain and whole matrix

Canonical bitmasks use a=1,b=2,c=4, Z={8,16,32}; the five remaining outside
bits are 64,128,256,512,1024. All original members are enumerated in increasing
bitmask order, including the actual empty set first. There are N=89 members
and n=88 nonempty members. The a-star has size s=28 and is the unique largest
star: b and c lose three members each, and every outside star has size at most
14. No star, empty loop, or member is deleted from the matrix domain.

The compact literal table is the already published
[literal.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/small-deletion-boundary/literal.py).
Write its disjoint-entry table at q=8 as w_0(type(A),type(B)) plus
kappa*w_1(type(A),type(B)), where type records core and outside cardinality.
The complete nonempty matrix is

```text
C0[A,A]=27; Delta[A,A]=0;
C0[A,B]=-1; Delta[A,B]=0                 if A!=B and A intersects B;
C0[A,B]=w0(type(A),type(B))-1;
Delta[A,B]=w1(type(A),type(B))           if A and B are disjoint;
C_kappa=C0+kappa*Delta.
R[a,b]=R[b,a]=R[a,c]=R[c,a]=1;
R[b,ac]=R[ac,b]=R[c,ab]=R[ab,c]=-1;
every other R entry is zero.
U0=89 I_88-J_88-C0.
```

The affine table was credited to LEMMA9145 through LEMMA9259. Exact generic
whole-matrix arithmetic originated in LEMMA8757 and its
[exact.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-majority/exact.py),
source commit 99d63aa2f085127a670ae375b19a68b89e184074. Both source files are
SHA-pinned by [inputs.py](inputs.py). No earlier matrix producer or solver is
imported.

Put T=C0+kappa*Delta+tR and E=[-1';I_88], an 89 by 88 full-column-rank matrix.
The original whole matrices are

```text
L=J_89+E T E';        M=(L-28 I_89)/61;
89 I_89-L = E (U0-kappa*Delta-tR) E'.
L[empty,empty]=76+(1065/29)*kappa;
M[empty,empty]=(48+(1065/29)*kappa)/61;
L[empty,A]=1-sum_B T[A,B];
L[A,B]=1+T[A,B]       for A,B nonempty.
```

These identities retain all empty rows and loops. E'1=0, so L1=89*1 and M1=1.
Every nonempty intersecting M entry is zero, including its diagonal. R changes
only disjoint entries. The nonempty star vector Sa satisfies T Sa=0 for all
parameters; the whole centered star satisfies L(1_star-(28/89)1)=0.
Since the image of E is exactly 1-perp, the cap and lower conditions are
equivalent to T>=0 and U0-kappa*Delta-tR>=0. Their ranks give
rank(L)=1+rank(T) and rank(89 I-L)=rank(U0-kappa*Delta-tR).
Thus capped feasibility certifies H with lambda_min(M)=-28/61 and M<=I.

The two-skeleton, table and R are invariant under all outside permutations;
permuting the three deleted outside points transports every matrix and
certificate to every Z. [whole.py](whole.py) checks all 56 such domain
transports as well as four original whole matrices. No invariant-subspace
restriction is imposed on candidate vectors or matrices in the proof.

## Complete physical Schur reduction at kappa=0

The repair has rank four. Its kernel consists of physical vectors with
v_b=v_c=0 and v_a=v_ab=v_ac. A basis K for this kernel comprises
e_a+e_ab+e_ac and each original coordinate unit outside {a,b,c,ab,ac}; it has
84 columns. The active complement B0 has columns e_b,e_c,e_ab,e_ac. Together
these form a unimodular basis of the entire original R^88: its inverse takes
the coefficient of the first K column to v_a and the active coefficients to
v_b,v_c,v_ab-v_a,v_ac-v_a, with all other coefficients unchanged.

Let F0 be the indicator of all retained triples and of the three core pairs.
Define z=1-Sb-Sc+F0. Direct original-coordinate equations give

```text
C0 Sa=C0 z=C0(Sb-F0)=C0(Sc-F0)=0;
R Sa=R z=0;        Delta Sa=0;
z' Delta z=1071/29>0.
```

Sa,z belong to ker(R). Their coefficients at the first K column and the
outside singleton 8 are (1,0) and (1,1), respectively. Replacing those two K
columns by Sa,z therefore has determinant one. The remaining 82 K columns,
the four active columns, and Sa,z are a complete basis; the last two have zero
rows and columns for C0+tR. Their independence is explicit, not inferred
from a numerical rank.

[schur.py](schur.py) rebuilds the entire original matrices, checks every
kernel equation and the R action on every K column, and proves that the
84-dimensional upper compression and 82-dimensional lower compression are
positive definite. Positive rational denominators are cleared. Every
fraction-free Bareiss pivot is strictly positive, proving positive leading
principal minors; all four solved right-hand sides are checked again against
the original compressed matrix. This is a finite 84/82 solve, not an
unbounded symbolic inverse or cofactor expansion.

Eliminating each PD compression gives an exact four-coordinate Schur form.
In the complete even/odd active basis
(1,1,0,0),(0,0,1,1),(1,-1,0,0),(0,0,1,-1), all cross blocks vanish. The basis
is invertible; congruence proves PSD and rank without treating it as an
orthonormal spectral basis. The complete lower and upper blocks are

```text
lower-even(t) = [[m,m-2t],[m-2t,m]],
lower-odd(t)  = [[m',-m'+2t],[-m'+2t,m']],
  m  = 13517166019574988998136/1066241189378785104899 > 8,
  m' = 5992/211 > 8.

upper-even(t) = [[a,b+2t],[b+2t,c]],
  a = 298297253937885903403766923833762/A,
  b = B/A,
  c = 10434695645112731990798012688520266/A,
  ac = disc/A^2,
  det(upper-even(t)) = -4 P(t)/A.
upper-odd(t) = [[d,e-2t],[e-2t,d]],
  d = 5902726/49735, e = 265864/49735.
```

These rational blocks are frozen in [CERTIFICATE.json](CERTIFICATE.json),
and all entries are rederived from the complete original solve. Both lower
blocks are PD when 0<t<min(m,m'). The odd upper block is PD for 0<=t<=8:
d>abs(e), d>abs(e-16), and convexity of absolute value bounds every
intermediate off-diagonal. The even upper block, whose diagonal entries
are positive, is PSD precisely when P(t)<=0.

[geometry.py](geometry.py) derives the primitive polynomial from those blocks,
checks its positive nonsquare discriminant, and verifies
P(1/4)>0, P(3/8)<0, P(6)<0, P(8)>0. Its vertex lies strictly between 3/8 and 6,
so these inequalities isolate the two roots and prove the stated ordering.
The entire upper interval lies inside the strict lower and odd-upper
intervals. Complete congruence proves the kappa=0 slice and all its ranks.
This establishes sufficiency for every real t in the closed interval,
including the algebraic endpoints.

## Endpoint PSD duals close the projection over all real kappa

The slice alone does not exclude other kappa. The following original PSD
separators supply that missing bridge. First, for all real t,
z'(C0+kappa*Delta+tR)z=kappa*(1071/29). Hence every feasible kappa is
nonnegative.

Let xi denote either root of P, and let H=K'U0K, G=K'U0B0. The upper H is PD.
In the upper even Schur block the vector (-b-2xi,a) is an exact null vector.
Put y=(-b-2xi,-b-2xi,a,a)' in the four active coordinates and set

```text
w(xi) = A * [ B0 y - K H^{-1} G y ].
```

Here the factor A is only a positive integral scaling. The original
back-substitution, not a numerical eigensolver, gives all 88 coordinates.
[generator.py](generator.py) clears all denominators and verifies that this
scaling is exactly A. The affine integer vector has 17 orbits, indexed by
(a present, b/c count, Z count, W\Z count). The counts are
binom(2,b/c count)*binom(3,Z count)*binom(5,W\Z count), total 88.
The compact integer affine coefficients are in [CERTIFICATE.json](CERTIFICATE.json).
Every original bitmask is covered. For either embedding, the checks give

```text
(U0-xi R)w(xi)=0                          at every original coordinate;
u(xi)=w(xi)' U0 w(xi)=xi*r(xi);
r(xi)=w(xi)' R w(xi)=A^2*4a*(b+2xi);
d(xi)=w(xi)' Delta w(xi)>0.
```

The two R signs are r(tau_minus)<0 and r(tau_plus)>0. Positivity of both
d values is checked exactly, not inferred from a rational approximation.
[field.py](field.py) uses Q[x]/(P) with rational root isolators.
[radical.py](radical.py) independently expands the frozen integer orbit
vector in Q[sqrt(disc)], imports no Schur solve, generator or native field,
checks all original equations at both embeddings, and determines each
nonzero sign by comparing rational squares. Its pairings convert back to
exactly the same native elements. Both implementations use only the
SHA-pinned original table; their agreement is same-author arithmetic
independence, not external mathematical review.

Testing the PSD cap with w(xi) is a rank-one PSD dual. It gives

```text
0 <= w(xi)'(U0-kappa*Delta-tR)w(xi)
   = (xi-t)r(xi)-kappa*d(xi).
sigma_minus=d(tau_minus)/(-r(tau_minus))>0;
sigma_plus =d(tau_plus)/r(tau_plus)>0;
t >= tau_minus+kappa*sigma_minus;
t <= tau_plus-kappa*sigma_plus.
```

Together with kappa>=0, these exclude t outside the closed interval for
**every real kappa**, and force kappa=0 at either endpoint. Combining them
with the kappa=0 construction proves the exact all-kappa projection and
endpoint fibers. These are restrictions on this declared affine-repair
ansatz, not nonexistence of arbitrary H certificates.

The inequalities are strict if kappa>0. Indeed a PSD matrix Q with w'Qw=0
has Qw=0, by diagonalization (or its PSD square root). The actual original
outside singleton 8 has R row zero, whereas

```text
(Delta*w(xi))[8]
  = 1806551262643647298076113174610784
    -492972928211729838123752463204220*xi != 0.
```

Both embeddings of this nonzero rational affine element are nonzero because
P is irreducible. Since (U0-xi R)w=0, the outside coordinate of
(U0-kappa*Delta-tR)w is -kappa*(Delta*w)[8]. It is nonzero for every kappa>0,
regardless of t. Equality in either cap pairing is therefore impossible.

For a compact rational consequence, write d(xi)=d0+d1*xi, and
r(xi)=rho*(b+2xi), with rho=4a*A^2>0. Let
trace_d=2*d0-(B/A)*d1, the positive sum of the two d values. The gap between
the roots is sqrt(ac), so adding the strict slope inequalities gives

```text
kappa < K = rho*ac/trace_d
  = 272224880469885531979073806016882723901628987668138977481035919749350766798778399499256307524743
    /3875443163685812036883283664960749379268150006168643494577602044210906689571988575475589419417991;
1/16 < K < 1/14.
```

The generator and radical checker agree on this rational value and its
enclosure. Neither the two dual bands nor K characterize all feasible
positive kappa.

## Every interior repair has a positive-kappa interval

Fix a real tau_minus<t<tau_plus. The complete preceding lower congruence gives
C0+tR>=0 with kernel exactly span(Sa,z), and the cap U0-tR is PD. Since
Delta Sa=0, remove the forced Sa direction. Set
ztilde=z-((z'Sa)/(Sa'Sa))*Sa. This vector is nonzero and
ztilde'Delta*ztilde=z'Delta*z=1071/29>0.

On Sa-perp, choose an orthonormal basis with first vector ztilde/||ztilde||.
The remaining baseline lower block H_t is PD. In this complete space the
perturbed lower matrix has the ordinary block form

```text
[[kappa*a_t, kappa*b_t'],
 [kappa*b_t, H_t+kappa*D_t]],  a_t>0, H_t>0.
```

Write mu_t=lambda_min(H_t)>0. For sufficiently small positive kappa,
H_t+kappa*D_t >= (mu_t/2)I. Its scalar Schur complement is at least
kappa*a_t-kappa^2*(2||b_t||^2/mu_t), strictly positive for sufficiently small
positive kappa. The PD baseline cap U0-tR also remains PD for sufficiently
small kappa, because its smallest eigenvalue is positive and Delta is a
fixed finite matrix. Taking the minimum of these positive smallness
thresholds supplies epsilon(t)>0. Zero cross terms or derivative norms
simply omit the corresponding restriction. This proof applies to all real
interior t; no compactness of the entire open interval, floating gap, or
computed optimal epsilon is assumed.

It follows that the only lower kernel is Sa and the cap is PD on R^88,
giving whole ranks 88 and 88 for all 0<kappa<epsilon(t). Every such whole
matrix has minimum H eigenvalue -28/61 with multiplicity one and a simple
unit eigenvalue. The endpoint fibers have kappa=0 and lower rank 87, so
they cannot attain these greatest ranks. This proves the exact open
greatest-rank repair projection. It is an ordinary finite-dimensional
perturbation/Schur argument, not a proof-assistant formalization.

## Consequences and exact evidence limits

In particular, t=0 is impossible at q=8 for every real kappa. Combined with
the credited all-real q4..7 obstruction in LEMMA9259 and its unrepaired
positive seeds at q9..11 and q>=12, the unrepaired three-deletion affine
seed has the sharp integer cutoff q>=9 (within q>=4). This is a corollary of
the new q=8 duals plus earlier results; no new tail or q4..7 proof is claimed.

[verify.py](verify.py) runs six serial phases, each with an unchanged 60s
limit and all native threads one. It compares the whole deterministic
mathematical record with [EXPECTED.json](EXPECTED.json). Normal and
optimized Python must give identical records; exceptions, not assert
statements, enforce every check. The compact source requires only Python
3.11+ and two existing SHA-pinned public input files. The 14 damage controls
cover the primitive polynomial, missing/duplicate orbits, original counts,
both affine vector coefficients, a zero dual, changed source, original
empty set/diagonal, row-preserving intersecting support, physical symmetry
and negative pivots, and floating entries.

Four whole rational controls at (kappa,t)=(0,3/8),(0,1/2),(0,6),(1/4096,1/2)
inspect 31,684 original ordered entries, all row/support/star conditions,
and both PSD ranks in the nonempty and whole matrices. The positive-kappa
control reproduces LEMMA9259. The interval and global dual statements are
proved by the complete reductions above, not by sampling these controls.
The rational evaluator does not accept irrational t; the real formula and
both exact field embeddings decode the endpoint matrices in the proof.

Trusted, unformalized bridges are literal finite-domain completeness,
positive-pivot/Schur congruence, basis decoding, real PSD dual interpretation,
the whole empty lift, permutation transport and the positive perturbation
argument. The finite original computations are exact and reproducible.
No solver, search, external data corpus or floating-point premise is used.
Source hashes prove provenance rather than mathematical correctness.
Results are scoped to the declared q=8,k=3 ansatz; no full general H/I
resolution, arbitrary-certificate obstruction, optimal kappa, or transferred
independent verdict is asserted.
