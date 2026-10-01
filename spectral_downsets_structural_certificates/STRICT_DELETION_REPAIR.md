# Strict inherited pair-deletion caps admit maximal-rank repairs

Author: **six-downset-1**, role **researcher**, 2026-10-01.
Status: complete ordinary author-checked proof with exact rational
validation; unformalized and not independently reviewed. No historical
priority is asserted. General Spectral Chvatal H/I remain unresolved.

The increment is a uniform rank perturbation, a complete deleted-graph
kernel classification, and one proper recoloring per bipartite component.
Ordinary rank-two H, the inherited cap test, star/triangle classification,
empty lift, strict convex kernel repair and tensor identities are credited.
This proves more than the original matching candidate. Failure of the
inherited test is not mathematical nonexistence.

## 1. Exact hypotheses and theorem

Let n>=4, V={0,...,n-1}, and let T be an arbitrary simple graph of deleted
pairs on V. Assume at least one vertex is incident to no edge of T.
Let r be the number of untouched vertices, and put

```
ell=binom(n,2), k=|T|, N0=1+n+ell, N=N0-k, s=n,
D={empty} union all singletons union all pairs outside T,
kappa=n(n-1)/(n-2), delta=N-kappa.
```

Exactly the r untouched stars have size n. Since k<=binom(n-1,2), N>=2n
and delta>0. Define the k by k rational Gram matrix

```
G[e,e]=n-1;
G[e,f]=-1 if distinct deleted pairs e,f meet;
G[e,f]=2/(n-2) if e,f are disjoint.
f=1_k^T G(delta I_k+G)^(-1)1_k.                  (1)
```

For k=0 set f=0. The inverse is well-defined because G>=0 and delta>0.
The theorem's hypothesis is **f<1**. The prior inherited-matrix cap test
is f<=1; it is not an all-matrix feasibility criterion.

**Theorem.** There is an explicit rational symmetric matrix M on D with
M1=1, M[A,B]=0 when A intersects B, and

```
-n/(N-n) I <= M <= I,
rank L=N-r, L=(N-n)M+nI,
rank(I-M)=N-1.                                  (2)
```

The lower rank is maximal among **all real H matrices**, even without the
extra cap. The lower endpoint has multiplicity r and the top endpoint is
simple. Exactly the r untouched stars are maximum intersecting families.
Signed entries are permitted; no full sign classification is asserted.
No symmetry hypothesis on T is imposed.

Every matching with 0<=2k<n and every partial star with 0<=k<=n-2 passes
the strict hypothesis at n>=4. In particular k=0 gives capped maximal-rank
matrices on every uniform rank-two downset at n>=4. These infinite
corollaries are proved in Section 6, separately from finite computation.

Also f<1 implies N>2n. For a finite nonempty product of theorem factors
on disjoint supports, put p=max_j n_j/N_j, N_P=product_j N_j, and
d=sum_(j:n_j/N_j=p)r_j. The tensor has unrestricted maximal lower rank
N_P-d, simple top endpoint and exactly d maximum coordinate stars.
A positive integer a-th power has lower rank N^a-ar. Section 7 proves
these statements. No claim is made for f>=1, n=3, or deletions touching
every coordinate. Excluded cases can have other capped matrices.

## 2. Credited baseline and a strict rational buffer

The uniform C0 from [PROOF.md, Section 9](PROOF.md), graph7578, has diagonal
n-1, distinct intersecting entries -1, singleton/singleton entries -1,
and all other disjoint entries 2/(n-2). It satisfies

```
C0>=0, C0*1=0, C0^2=kappa C0, rank C0=ell-1.
```

Its Gram vectors form a centered tight frame on the range. Let W contain
the deleted vectors, t0=W1_k, so W^T W=G. The retained empty lift's frame
operator is F0=kappa I-WW^T+t0*t0^T, by
[DELETIONS.md, Sections 2–3](DELETIONS.md), graph7584. No new inherited
H-existence or cap-test assertion is made here.

Put A=delta I+WW^T, nu=delta(1-f), mu=nu/N. The identity
AW=W(delta I+G) gives t0^T A^(-1)t0=f. Cauchy–Schwarz in the A inner
product yields t0*t0^T<=f A. Consequently

```
N I-F0=A-t0*t0^T >= (1-f)A >= nu I.              (3)
```

G commutes with delta I+G, so f>=0; the hypothesis gives 0<mu<1.
The lifted Gram Q0 kills the full constant vector and has F0's nonzero
spectrum. Therefore N I_N-J_N-Q0>=nu(I_N-J_N/N).
Take the principal block on the retained m=N-1 nonempty indices.
I_m-J_m/N has least eigenvalue 1/N. Thus the retained core C0' has

```
N I_m-J_m-C0' >= mu I_m.                         (4)
```

The principal-buffer mechanism also occurs in the matching corner of
[FOUR_CENTER_BIPARTITE.md, Section 5](FOUR_CENTER_BIPARTITE.md), graph8150.
That corner is credited context, not a premise about arbitrary T.
Gram square roots explain spectra only; the constructor uses rational
arithmetic and (1).

## 3. A complete uniform perturbation

On all n+ell nonempty singleton/pair indices define C(t) with diagonal
n-1, intersecting entries -1, and disjoint weights for sizes11,12,22

```
b=-1+(n-2)(n-3)t,
p=2/(n-2)-(n-3)t,
z=2/(n-2)+t.                                   (5)
```

The star row equations are b-1+(n-2)p=0 and p-2+(n-3)z=0; rows in the
star have n-1 plus n-1 entries -1. Hence every full star is killed,
and C(0)=C0. Centering is not required for t>0.

Let B be point/pair incidence. Counting gives BB^T=(n-2)I+J, so B has
row rank n. The entire nonempty space splits orthogonally into the two
level constants, singleton standard plus its pair incidence image, and
pair incidence kernel. Their dimensions are 2, 2(n-1), ell-n.

For x perpendicular to 1_n, directions (x,0),(0,B^T x) have squared norms
||x||^2,(n-2)||x||^2. Their Gram, divided by ||x||^2, is
a[[1,-1],[-1,1]], where a=n-(n-2)(n-3)t. The cross image counts
-(1+p)(n-2)=-a. Pair line-graph adjacency acts by n-4 on the incidence
image; its pair Gram entry is a. Thus the active standard eigenvalue is
kappa-(n-1)(n-3)t, with multiplicity n-1.

On level constants, with norms n,ell, the Gram is
A0[[1,-1/2],[-1/2,1/4]], A0=n(n-1)(n-2)(n-3)t.
The killed direction (1,2) is the sum of stars. The active eigenvalue is
gamma*t, gamma=(n-2)(n-3)(2n-1)/2. The entries follow by counting n-1
intersecting pairs at a singleton and 2(n-2) at a pair. On ker B,
line-graph adjacency acts by -2; C(t) acts by n+1+z=kappa+t.

Thus the complete nonzero spectrum is

| Mode | Eigenvalue | Multiplicity |
|---|---|---:|
| Pair incidence kernel | kappa+t | ell-n |
| Active standard | kappa-(n-1)(n-3)t | n-1 |
| Active constant | gamma*t | 1 |

For every real 0<t<n/[(n-2)(n-3)], C(t)>=0 has rank ell and exactly the
n independent stars in its kernel. This makes the missing constant mode
positive; a small norm bound alone would not settle the singular rank.

All these subspaces and eigenvectors are independent of t.
E0=(C(t)-C0)/t has eigenvalues 1,-(n-1)(n-3),gamma on the active modes
and zero on the stars. For n>=4 gamma>=1 and gamma>(n-1)(n-3):
2[gamma-(n-1)(n-3)]=(n-3)(2n^2-7n+4)>0, whose last factor at n=4+U
has coefficients 8,9,2. Hence ||E0||=gamma.

Choose **t=mu/(2gamma)**. It lies in the positivity interval because
mu<1<n(2n-1). Principal compression cannot increase operator norm.
For the retained Ct', (4) now gives

```
Ct'>=0, N I_m-J_m-Ct' >= (mu/2)I_m.             (6)
```

The symbolic checker clears every row-count, Gram, trace, scalar and
margin identity independently over rational polynomials. The incidence
completeness and norm argument above is the all-order ordinary bridge.

## 4. Deleted-graph kernels and detecting partitions

For a PSD matrix, y is in a principal block's kernel iff its extension
by zero is in the full kernel: its full quadratic form is zero, hence
the PSD matrix annihilates it. A full star combination has value h_i+h_j
on deleted pair ij. The retained kernel is therefore identified with

```
h_i+h_j=0 for every ij in T.                    (7)
```

An isolated vertex gives one free coefficient. On each connected
nonisolated component, propagating signs gives one coefficient if it
is bipartite, while an odd cycle forces zero. Let b_T count nonisolated
bipartite components. The entire retained kernel has dimension r+b_T,
with basis the untouched stars and
X_C=sum_(i in C)sigma_i S_i', signs +1/-1 on the two parts of C.
Singleton coordinates prove independence. Rank Ct'=m-r-b_T.

Start from the full proper n-color partition: singleton i has color 2i
mod n, pair ij has color i+j mod n. Every full star has every color once.
Delete T's pairs. For each nonisolated bipartite component C choose its
least vertex a and least neighbor b, with sigma_a=1. Make one separate
partition by recoloring **only singleton a**, from 2a to a+b mod n.
The new color is absent among retained incident pairs: its unique old
incident pair ab was deleted. It differs from 2a since a!=b modulo n.
The partition is proper; untouched stars still have all colors once.

Let H_C be its one-hot incidence and P_C=H_C(nI_n-J_n)H_C^T.
This PSD matrix has diagonal n-1, intersecting entries -1, and kills
untouched stars. For any solution h of (7), its signed retained-star
vector X(h) has color count (sum_i h_i)1_n before recoloring: deletion
of ij subtracts (h_i+h_j)e_(i+j)=0. After recoloring,

```
H_C^T X(h)=(sum_i h_i)1_n+h_a(e_(a+b)-e_(2a)),
X(h)^T P_C X(h)=2n h_a^2.                      (8)
```

Thus P_C has quotient 2n on its own signed component vector and zero on
the others. This works even for unequal bipartition sizes; nI-J kills
the constant color count. For b_T>0 average these b_T matrices to get P.
Its extra-kernel quotient is **(2n/b_T)I_(b_T)**, positive definite. Hence
ker Ct' intersect ker P is exactly the untouched-star span.
One explicit partition per bipartite component suffices; no coloring
enumeration is a premise.

## 5. Quantitative convex repair and empty lift

If a proper partition's color-class sizes are n_c, then

```
N I_m-J_m-P_C=N I_m-n H_C H_C^T >= -beta_C I_m,
beta_C=max(0,n*max_c n_c-N).
```

For b_T>0 set beta=max_C beta_C, epsilon=mu/[2(mu+2beta)] and
Cbar=(1-epsilon)Ct'+epsilon P. Since 0<epsilon<=1/2<1, the kernel is
the PSD kernel intersection: sum the two nonnegative quadratic forms.
Thus Cbar has exactly the r untouched-star kernels and rank m-r.
Moreover

```
N I_m-J_m-Cbar >= [(1-epsilon)mu/2-epsilon beta]I
                  = (mu/4)I.                  (9)
```

For b_T=0 use Cbar=Ct', already of rank m-r with buffer mu/2.
All prescribed diagonal/intersecting entries are retained. The generic
convex kernel mechanism is credited to [CLIQUE_CENTERS.md](CLIQUE_CENTERS.md),
graph7733; the component-detecting partitions are the new ingredient.

Use the credited empty lift E=[-1_m^T;I_m]:

```
Q=E Cbar E^T, L=Q+J_N,
M=(L-nI_N)/(N-n).                              (10)
```

No centered-core hypothesis is needed. Q>=0, Q1=0, rank Q=m-r because E
has full column rank. J adds the independent constant direction, giving
rank L=N-r. The prescribed nonempty entries give H support and diagonal;
the empty loop is legal and M1=1. The identity

```
(N-n)(I-M)=N I_N-J_N-Q
         =E(N I_m-J_m-Cbar)E^T
```

and the strict core buffer prove the cap with upper rank N-1 and simple
top endpoint. Formula (1) and (10) give a rational constructor.

## 6. Infinite corollaries and density

At k=0, f=0 and
N0-kappa=[n(n-1)(n-2)-4]/[2(n-2)]>0.

For a matching, 1<=k and 2k<n, the credited top is
q=kappa+(k-1)[n-1+2(k-1)/(n-2)]. Its gap h(k)=N-q is
n(n+3)/2-kappa-nk-2(k-1)^2/(n-2), decreasing for real k>=1.
Since k<=(n-1)/2,

```
N-q >= (n^2-9)/[2(n-2)] >0 for n>=4.
```

For a partial star, 1<=k<=n-2, the credited top is
q=kappa+(k-1)(n-k). Completing the square gives

```
N-q=[k-(n+2)/2]^2+n^2(n-4)/[4(n-2)]>0.
```

At n=4 the allowed k=1,2 leave a positive square; at n>=5 the second
term is positive. For either regular deletion, f=kg/(delta+g),
q=kappa+(k-1)g; these strict gaps imply f<1. This proves the all-order
matching/partial-star corollaries, including odd orders.

N=2n would force k=binom(n-1,2); the untouched vertex then implies T
is the complete graph on all other vertices. Its regular deleted
line graph has g=2/(n-2) and q=kappa+(k-1)g=2n=N. Thus delta=(k-1)g
and f=kg/(delta+g)=1, contradicting strictness. Therefore N>2n and
rho=n/(N-n)<1. This boundary is not a capped-H obstruction: the prior
equitable-partition construction supplies capped matrices for these
retained star downsets, whose family size is N=2s.

## 7. Unrestricted rank, equality and products

For any real H slack L on D and intersecting indicator 1_I of size q,

```
(1_I-(q/N)1)^T L(1_I-(q/N)1)=q(n-q).
```

Support and L1=N1 prove this identity. At q=n, each maximum centered
star is in the PSD kernel. The r centered stars are independent by
empty and untouched-singleton evaluations. Thus every real H slack
has rank at most N-r. Our construction attains it and its kernel is
exactly their span.

The same identity proves q<=n. An equality indicator has form
1_I=(n/N)(1-sum_i a_i)1+sum_i a_i S_i.
Its empty entry gives sum_i a_i=1, and untouched-singleton entries
make each a_i zero or one. Exactly one equals one, hence I is one
untouched star. The classical star/triangle classification is credited.

Tensor support, symmetry and row sums follow from the credited product
identity. Each factor has spectrum in [-rho_j,1], rho_j<1, simple top
space and lower multiplicity r_j. The least product eigenvalue is
-max_j rho_j. It occurs from exactly one greatest-density factor at
its lower endpoint and all others at one. An additional magnitude <1
reduces it strictly; three or more negative factors do so as well.
Thus lower multiplicity is d=sum eligible r_j, and rank is N_P-d.
Centered eligible coordinate stars force that rank upper bound for
every real H matrix on the product. Empty and global singleton entries
prove independence and force every equality family to be exactly one
eligible coordinate star. These are ordinary arguments, separate from
finite tensor checks.

## 8. Exact reproduction and trust boundary

The constructor is [strict_deletion_repair.py](strict_deletion_repair.py);
rational identities are in [strict_deletion_identities.py](strict_deletion_identities.py);
the literal checker is [verify_strict_deletion_repair.py](verify_strict_deletion_repair.py).
The compact record is [strict_deletion_repair_expected.json](strict_deletion_repair_expected.json).
Run from repository root, CPython 3.11+ standard library, tested 3.11.2:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B spectral_downsets_structural_certificates/verify_strict_deletion_repair.py --check
```

All checks also run under python3 -B -O; no proof obligation uses assert.
The checker reproduces the prior 74-case labelled inherited-deletion
baseline at n=3,4,5, including independent entry formulas, exact cap tests
and top eigenpairs. Only n>=4 strict cases enter the new construction.
All deletion masks fixing an untouched last vertex at n=4,5 are enumerated
and classified as strict, boundary or inherited-uncapped. Every strict
case has full row/support/PSD/rank/buffer checks and a complete literal
maximum-family census. Excluded cases carry no nonexistence conclusion.

Additional full matrices cover every allowed matching and partial-star
size at n=4..8, plus irregular bipartite, odd-cycle and mixed-component
graphs. Five complete uniform image/spanning bases verify all directions
and the perturbation norm. The retained principal kernel, deleted-incidence
rank, all component quotients, proper colorings and untouched-star colors
are checked. The full entries are reconstructed with the closed lift
formula independently of the lift routine; the orbit-weight helper is
shared with the constructor. Full PSD/rank checks and the symbolic
count identities supply separate validation. Two full tensors check tied and distinct
greatest fractions; their equality classification uses the written proof,
not a tensor census.

Nineteen rational identities are independently cleared without parameter
interpolation. Five shifted sign records contain nineteen positive
coefficients. Malformed inputs, excluded strict-domain cases, invalid PSD
forms and the unperturbed extra-kernel control remain active under -O.
Complete expected-result equality checks every deterministic output field.
No omitted corpus, solver, floating spectrum, unfinished enumeration or
resource-limit outcome is a premise. The ordinary frame, completeness,
principal-kernel, component propagation, strict mixture, lift and equality
bridges are unformalized; finite checks do not replace them.
Completed normal and optimized outputs match the expected record exactly.
The normal run took 35.30 seconds at 23,004 KiB peak child RSS; the
optimized expected-output check took 31.98 seconds at 24,908 KiB,
with one mathematical process and numeric threads one.

Production dependencies: graph7578 (lift, uniform projection and tensor),
graph7584 (inherited cap test and regular top), graph7733 (generic partition
kernel repair). Graph8150 is matching-corner predecessor context.
The all-rank ordinary uniform coupling graph8064 and its independent
review8104 overlap at rank two: their matrices fail the extra cap.
This rank-two theorem does not generalize their wider-rank assertions,
and their reviews do not independently review the present proof.
There is also a precise small-order overlap: at n=4, the uniform rank-two
downset is the near-cube downset of rank n-2. The recent
[weighted complement-only classification](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md),
graph8154, already supplies capped maximal-rank matrices there. In its
notation our invariant point has every z_P=2-t. No new four-point
existence assertion is made. The generic strict-deletion repair and
all-order matching/partial-star formulas are the current increment.

The live [Ellis–Filmus–Friedgut Section 4](https://arxiv.org/html/2609.28404v1#S4)
and [arXiv record](https://arxiv.org/abs/2609.28404), checked 2026-10-01,
still list v1 dated 2026-09-23 and H/I as conjectures. Ordinary rank-two
H is known from constructive Vizing, credited to Misra–Gries 1992 in
[PROOF.md](PROOF.md). The cap/rank repair is the scoped increment.
Bounded primary/graph/source checks are not a historical-priority proof.
