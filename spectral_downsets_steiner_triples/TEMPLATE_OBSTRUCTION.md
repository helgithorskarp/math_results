# An all-orders obstruction to the seven-weight centered template

Author: **six-downset-2**, role **researcher**, 2026-09-30.
Status: ordinary analytic proof; small exact affine checks corroborate its
equations. No historical priority or independent review is asserted.

Let U be a **simple 2-(v,3,m) design**, v>=9 and 2<=m<=v-3, and let D contain
empty, all points, all pairs, and the triples of U. Its parameters are
N=1+v+v(v-1)/2+mv(v-1)/6 and s=v+m(v-1)/2. For a block A and point i outside
A, let f(A,i) count pairs P in A for which P union {i} is a block.
Suppose some block A has nonconstant f(A,i) over its outside points.
This is guaranteed if **v-3 does not divide 3(m-1)**.

**Theorem:** There is **no H matrix** whose bound matrix Q=(N-s)M+sI has empty column
identically one and the following seven shared weights on disjoint distinct
nonempty pairs:

| Sizes | Q entry |
|---|---:|
| 1,1 | a |
| 1,2, with union outside U | b |
| 1,2, with union in U | b-u |
| 2,2 | c |
| 1,3 | h_1 |
| 2,3 | h_2 |
| 3,3 | t |

Nonempty diagonals must be s and intersecting off-diagonals zero. All seven
parameters may be arbitrary real numbers, without sign restrictions.
In particular this excludes the template for **every simple 2-(v,3,2)
design with v>=9**, including the union of any two block-disjoint STS(v).
It also excludes every simple 2-(9,3,m) design with m=2,4,6. No decomposition
into STSs is required for the general result. This is an obstruction to a precise centered template. The
[four-system theorem](FOUR_STS9_PROOF.md) proves capped H on its stated
decomposable cohort using finer entries. The obstruction does not refute H,
and imposes no constraint on certificates outside the displayed template.

## General proof by forced equations and a negative quadratic form

If Q is an H bound matrix, then Q1=N1 and Q is PSD. For each star indicator
x_i of size s, put z_i=x_i-(s/N)1. Support gives x_i^TQx_i=s^2 and hence
z_i^TQz_i=0. PSD implies Qz_i=0, so **Qx_i=s1**.

Each point lies in r=m(v-1)/2 triples, and U has mv(v-1)/6 blocks. The
sum of f(A,i) over the v-3 outside points is 3(m-1): each pair of A has
m completions and precisely one inside A. If v-3 does not divide 3(m-1),
the average is not an integer and hence the values vary. For m=2 and v>=9
the average is strictly between zero and one. For v=9 and m=2,4,6 it is
(m-1)/2, a half-integer. This proves the stated sufficient conditions.

Inclusion-exclusion gives m(v-7)/2+f(A,i) triples
containing i and disjoint from A. The triple row of Qx_i=s1 therefore gives

```
h_1+(v-4)h_2+[m(v-7)/2+f(A,i)]t=s.
```

Variation forces t=0. The triple row of Q1=N1 then gives
1+s+(v-3)h_1+[(v-3)(v-4)/2]h_2=N. Solving yields

```
h_2=[v(v-5)+(2/3)m(v-1)(v-3)]/[(v-3)(v-4)],
h_1=2v/(v-3)-m(v-1)/6.
```

Next fix a pair A and i outside it. Put e=1 when A union {i} is a block
and e=0 otherwise. Exactly m of its v-2 outside points have e=1, so both
values occur because 0<m<v-2. The pair row of Qx_i=s1 gives

```
b+(v-3)c+[m(v-5)/2]h_2+e(h_2-u)=s.
```

Thus u=h_2. A pair row has v-2 disjoint singletons, binom(v-2,2) disjoint
pairs, and m(v-3)(v-4)/6 disjoint triples. Its total row equation is
1+s+(v-2)b+[(v-2)(v-3)/2]c+[m(v-1)(v-6)/6]h_2=N. Together these force

```
c=2[(v-1)s+1-N-(m(v-3)(v-4)/3)h_2]/[(v-2)(v-3)],
b=s-(v-3)c-[m(v-5)/2]h_2.
```

Finally the singleton row {j} of Qx_i=s1 for i distinct from j gives
a+(v-2)b-mh_2+[m(v-3)/2]h_1=s. Substitution forces

```
a=m(v-3)[6-m(v-1)]/36.
```

The singleton principal block is (s-a)I_v+aJ_v. Its constant eigenvalue is

```
lambda(m)=s+(v-1)a
         =v+mv(v-1)/6-m^2(v-1)^2(v-3)/36.
```

For m=2 this is -[v^2(v-8)+v-3]/9<0. For m>=2,

```
lambda(m)-lambda(2)
 =(m-2)(v-1)[6v-(m+2)(v-1)(v-3)]/36 <=0.
```

The bracket is negative: v-3>=6 and m+2>=4 give
(m+2)(v-1)(v-3)>=24(v-1)>6v. Thus lambda(m)<0. Equivalently the
all-ones singleton vector has quadratic form v*lambda(m)<0, contradicting
PSD. This proves the all-orders theorem. Upper caps and rationality were
not used, and no existence of a design outside the input hypothesis is presumed.

The seven forced weights actually satisfy all the row and star equations.
For the remaining singleton total-row equation, substitution gives
1+s+(v-1)a+binom(v-1,2)b-[m(v-1)/2]h_2
  +[m(v-1)(v-3)/6]h_1=N; the empty equations are automatic.
The failure is positivity. The theorem explains why simply extending the
single-STS incidence formula with one constant weight for all disjoint
triples cannot produce centered H under the stated variation hypothesis. It does not
exclude noncentered matrices, orbit-dependent weights, or other templates.

## Nine-point specialization and exact corroboration

At v=9 and m=2,4,6, the variation condition is automatic. The formulas reduce to
h_2=(18+16m)/15, h_1=(9-4m)/3, c=(81+24m-32m^2)/63,
b=(45-24m+32m^2)/35, a=m(3-4m)/3. The singleton constant eigenvalues are
-29/3, -341/3 and -303, with explicit quadratic forms -87, -1023, -2727.

[verify_template_obstruction.py](verify_template_obstruction.py) builds
four concrete designs: the first retained two-STS(9) union, the first new
four-STS(9) union, all triples outside the affine STS(9), and a specified
two-STS(13) union. The last consists of the cyclic system and its image under
the literal checked permutation in the source. It independently
counts pair degrees, constructs the actual seven-variable row/star system
from sets, and solves it by rational Gaussian elimination. Each has unique
weights equal to the displayed expressions. It checks all H equations
apart from PSD, then verifies the explicit negative singleton quadratic form.
The third example has pair degree six; its STS decomposability is unnecessary
for this obstruction. The fourth has N=144,s=25 and singleton quadratic
form -1235. Two encoding controls detect a changed row entry and
a malformed triple set.

From the repository root, CPython 3.11.2 and standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/verify_template_obstruction.py --check
```

[template_obstruction_expected.json](template_obstruction_expected.json)
is compact exact output. These finite examples validate the equations and
encoding. Universal coverage over every simple design in the theorem is
the preceding analytic counting argument, not an inference from four tests.
The general H equality-to-kernel principle is already in
[MAXRANK_PROOF.md](MAXRANK_PROOF.md), credited there to six-downset-3.
The source target remains [Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4),
checked 2026-09-30; H and I remain conjectures.
