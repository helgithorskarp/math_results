# A seven-weight centered template is impossible at even pair degree

Author: **six-downset-2**, role **researcher**, 2026-09-30.
Status: ordinary analytic proof; small exact affine checks corroborate its
equations. No historical priority or independent review is asserted.

Let U be **any simple 2-(9,3,m) design**, with m in {2,4,6}, and let D contain
empty, all nine singletons, all 36 pairs, and the triples of U. Its parameters
are N=46+12m and s=9+4m. This statement does not require an STS decomposition.

There is **no H matrix** whose bound matrix Q=(N-s)M+sI has empty column
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
This is an obstruction to a precise centered template. The
[four-system theorem](FOUR_STS9_PROOF.md) proves capped H on its stated
decomposable cohort using finer entries. The obstruction does not refute H,
and imposes no constraint on certificates outside the displayed template.

## Proof by forced equations and a negative principal quadratic form

If Q is an H bound matrix, then Q1=N1 and Q is PSD. For each star indicator
x_i of size s, put z_i=x_i-(s/N)1. Support gives x_i^TQx_i=s^2 and hence
z_i^TQz_i=0. PSD implies Qz_i=0, so **Qx_i=s1**.

Fix a triple A in U. For i outside A let f(A,i) count its three pairs P
for which P union {i} is in U. Its values over the six outside points sum
to 3(m-1): each pair of A has m completions and precisely one inside A.
Their average is (m-1)/2, which is not an integer for even m. Consequently
f(A,i) takes at least two different values.

Each point is in 4m triples. Inclusion-exclusion gives m+f(A,i) triples
containing i and disjoint from A. The triple row of Qx_i=s1 therefore gives

```
h_1+5h_2+(m+f(A,i))t=s.
```

Variation forces t=0. The triple row of Q1=N1 then gives
1+s+6h_1+15h_2=N. Solving these two equations yields

```
h_2=(18+16m)/15,        h_1=(9-4m)/3.
```

Next fix a pair A and i outside it. Put e=1 when A union {i} is a block
and e=0 otherwise. Exactly m of its seven outside points have e=1, so both
values occur because 0<m<7. The pair row of Qx_i=s1 gives

```
b+6c+2mh_2+e(h_2-u)=s.
```

Thus u=h_2 and b+6c+2mh_2=s. There are 7 disjoint singletons, 21 disjoint
pairs and 5m disjoint triples in a pair row, giving
1+s+7b+21c+4mh_2=N. Therefore

```
c=(81+24m-32m^2)/63,    b=(45-24m+32m^2)/35.
```

Finally the singleton row {j} of Qx_i=s1 for i distinct from j gives
a+7b-mh_2+3mh_1=s. Substitution forces

```
a=m(3-4m)/3.
```

The singleton principal block is (s-a)I_9+aJ_9. Its constant eigenvalue is

```
s+8a=9+12m-(32/3)m^2,
```

equal to -29/3, -341/3, -303 at m=2,4,6. These are negative. Equivalently
the all-ones singleton vector has quadratic form 9(s+8a)<0, contradicting
PSD. This proves the theorem. Upper caps and rationality were not used.

The seven forced weights actually satisfy all the row and star equations.
For the remaining singleton total-row equation, substitution gives
1+s+8a+28b-4mh_2+8mh_1=N; the empty equations are automatic.
The failure is positivity. The theorem explains why simply extending the
single-STS incidence formula with one constant weight for all disjoint
triples cannot produce centered H at these even pair degrees. It does not
exclude noncentered matrices, orbit-dependent weights, or other templates.

## Exact corroboration and proof boundary

[verify_template_obstruction.py](verify_template_obstruction.py) builds
three concrete designs: the first retained two-STS(9) union, the first new
four-STS(9) union, and all triples outside the affine STS(9). It independently
counts pair degrees, constructs the actual seven-variable row/star system
from sets, and solves it by rational Gaussian elimination. Each has unique
weights equal to the displayed expressions. It checks all H equations
apart from PSD, then verifies the explicit negative singleton quadratic form.
The last example has pair degree six; its STS decomposability is unnecessary
for this obstruction. Two encoding controls detect a changed row entry and
a malformed triple set.

From the repository root, CPython 3.11.2 and standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 spectral_downsets_steiner_triples/verify_template_obstruction.py --check
```

[template_obstruction_expected.json](template_obstruction_expected.json)
is compact exact output. These finite examples validate the equations and
encoding. Universal coverage over every simple design in the theorem is
the preceding analytic counting argument, not an inference from three tests.
The general H equality-to-kernel principle is already in
[MAXRANK_PROOF.md](MAXRANK_PROOF.md), credited there to six-downset-3.
The source target remains [Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4),
checked 2026-09-30; H and I remain conjectures.
