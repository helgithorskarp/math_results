# Every 72-point candidate has a frame of nine-point planes

Complete author proof with exact finite certificates; independent review
pending. All sets are subsets of the affine space `F_5^3`. A set is
**line-free** if it contains no entire five-point affine line. Let `a_m`
be the number of affine planes meeting the set in exactly `m` points.

## 1. Global result

**Theorem.** Every line-free 72-point set satisfies

```text
3 a_8 + a_9 >= 11.                                      (1)
```

Combining this with the prior certified theorem `a_8<=1` gives

```text
a_9 >= 8;
a_8=0 implies a_9>=11;
a_8+a_9>=9.                                             (2)
```

Four of the nine-point planes have normal directions forming a projective
frame: every three of their normals are linearly independent. In particular,
every candidate has an affine image whose three coordinate parallel classes
all have the ordered profile

```text
B=(9,15,16,16,16),                                     (3)
```

and which has another nine-point plane `a x+b y+c z=d` with `abc!=0`.
At least five nine-point planes occur outside the three coordinate classes.

Thus **BBB alone, with the additional frame and count constraints, is an
exhaustive global normal form** for the 72-point problem. This does not
exclude a set that also admits an ABB description, and it does not prove
`a_8=0`. The normal forms overlap. The exact value remains between 70 and 72;
neither 72 nor 71 is excluded by this theorem.

## 2. Incidence data and hypotheses

We reuse the complete planar spectra and the incidence system of the
[global low-plane reduction](../low_planes72/README.md). Here are the
mathematical definitions, so the new certificate has an explicit meaning.

A line-free affine plane has at most 16 points. Every section of a 72-set
therefore has at least `72-4*16=8` points. If an affine line has `k` selected
points, its six containing planes satisfy

```text
sum_(H containing the line) |S intersect H| = 72+5k.      (4)
```

Consequently a plane of size at most 11 cannot contain four selected
collinear points: (4) would give `92<=11+5*16=91`.

For each allowed planar spectrum

```text
s=(m,n_0,n_1,n_2,n_3,n_4),
```

let `X_s` count planes of that spectrum; `n_k` counts their `k`-point lines.
The cited enumeration supplies all 70 spectra for sections of sizes 8--16,
with the additional three-points-per-line restriction at sizes 8--11.
Its labelled multiplicities are enumeration controls, not coefficients.

Let `P_p` count parallel classes with sorted size tuple `p`. There are 18
possible five-tuples in `[8,16]` summing to 72. Let `Y_(k,t)` count affine
lines with `k` selected points and sorted six-plane pencil tuple `t`.
There are 375 possible pairs: `0<=k<=4`, the entries of `t` are between
`max(8,5k-8)` and 16, and their sum is `72+5k`. The lower entry bound is
obtained by bounding the other five planes in (4) by 16.

Every actual candidate gives a nonnegative integral vector `u=(X,P,Y)`.
Write `#_m(p)` for the multiplicity of `m` in a tuple. Its 61 equations are

```text
sum_s X_s = 155;
sum_s m(s) X_s = 2232;
sum_s binom(m(s),2) X_s = 15336;
sum_p P_p = 31;

sum_(s:m(s)=m) X_s = sum_p #_m(p) P_p              (8<=m<=16);

sum_(s:m(s)=m) n_k(s) X_s
    = sum_t #_m(t) Y_(k,t)                 (0<=k<=4, 8<=m<=16);

sum_(k,t) Y_(k,t) = 775;
sum_(k,t) k Y_(k,t) = 2232;
sum_(k,t) binom(k,2) Y_(k,t) = 2556.                    (5)
```

There are 155 affine planes, 31 parallel classes, and 775 affine lines.
Each point lies on 31 planes and 31 lines; each pair lies on six planes
and one line. The middle equations count line-plane flags of each type.
These observations prove (5). No sufficiency or geometric realizability
of an arbitrary solution of (5) is asserted.

## 3. Exact weighted certificate

Write (5) as `Mu=b`, with 463 columns. Let `q` have coefficient three on
the `X_s` columns with `m=8`, coefficient one on those with `m=9`, and
zero elsewhere. Thus `q^T u=3a_8+a_9`.

The new [certificate](certificate.json) contains the integer denominator
`D=1000000` and 61 integer multipliers `z`, in the displayed row order.
The [checker](verify.py) reconstructs the matrix and verifies, using only
integers, each of the 463 inequalities and the right-hand side:

```text
M^T z <= D q;
b^T z = 10082223.                                      (6)
```

Since `u>=0`, multiply (6) by `u` and use `Mu=b` to obtain

```text
3a_8+a_9 >= 10082223/1000000 = 10.082223 > 10.
```

The left side is an integer, proving (1). This is a finite certificate
of a linear counting inequality, with no optimization verdict as a premise.
Exploratory HiGHS optimization supplied a real dual vector. Its entries
were rounded to this denominator, then the three count-row multipliers
were decreased enough to make every column inequality exact. The public
replay neither runs nor requires that optimizer.

The prior [two-eight-plane exclusion](../two_eight_planes72/THEOREM.md)
proves `a_8<=1` for all 72-point candidates. This separate computer-assisted
dependency is essential to (2) and the frame conclusion. Substituting
`a_8=0` or `1` into (1) gives (2).

## 4. Eight normals force a projective frame

Two nine-point planes cannot be parallel: their two sections together
with the other three parallel sections contain at most `18+3*16=66`
points. Thus the at least eight nine-point planes in (2) have distinct
normal directions in `PG(2,5)`.

We use the following elementary fact.

**Frame lemma.** A subset of `PG(2,5)` with no four points, every three
noncollinear, has at most seven points.

If the subset is collinear, it has at most six points. Otherwise take a
noncollinear triangle `A,B,C`. Any other point must lie on one of its three
sides, since a point off all three sides forms a frame with the triangle.
If there are further points, rename the triangle so one such point `P`
lies on `AB`. A point `Q` on `AC` other than its endpoints would form the
frame `B,C,P,Q`; a point on `BC` would form `A,C,P,Q`. Consequently every
point belongs to the six-point line `AB` or is `C`. The bound is seven.

Apply the lemma to the at least eight normals. It gives the four claimed
nine-point planes. This argument does not require the prior exclusion of
five collinear low-plane normals.

## 5. The complete coordinate normalization

Choose three planes from the frame. Write them as `n_i dot x=b_i`,
`i=1,2,3`. Their normals are independent. A nine-point plane has parallel
companions of total size 63, each at most 16. These four companions
therefore have sizes `15,16,16,16`. Let the unique fifteen-point companion
be `n_i dot x=c_i`, where `c_i!=b_i`.

Use the invertible affine coordinates

```text
y_i = (n_i dot x-b_i)/(c_i-b_i) in F_5.                (7)
```

Each selected nine-plane has coordinate zero and its fifteen-point
companion has coordinate one. This gives precisely (3); no arbitrary
permutation of the five field elements is used.

Write the fourth normal as `n_4=lambda_1 n_1+lambda_2 n_2+lambda_3 n_3`.
Every `lambda_i` is nonzero, because every three frame normals are
independent. Substitution of (7) makes its normal coefficients
`lambda_i(c_i-b_i)`, all nonzero. Hence the fourth plane belongs to the
80-plane family

```text
x + b y + c z = d,     b,c in F_5^*, d in F_5.          (8)
```

Each of the three coordinate classes contains just one nine-plane. At
least five of the eight occur outside those classes. The fourth plane
in (8) is one of them.

For a complete decision formulation it is therefore sufficient to impose:

* 72 selected points and no selected full affine line;
* the upper bound 16 on every plane;
* profile B on each coordinate axis;
* at least five additional nine-point planes outside the coordinate classes;
* at least one nine-point plane in (8).

Every actual candidate has an affine image satisfying these conditions.
Conversely any assignment satisfying them is itself a 72-point line-free
set. This is a single exhaustive case; generating or solving its formula
is left to the team's certificate route. No UNSAT claim is made here.

## 6. Evidence and boundary of the result

The replay re-enumerates all `2^25` planar subsets with the cited ordinary
C++ program, checks the new certificate with integer arithmetic, rebuilds
the affine incidences, audits the frame argument on all projective
triangles, and checks affine normalizations and the prior 70-point witness.
Normal and optimized Python runs give identical outputs. The certificate
and replay are author evidence, not independent peer review.

The written reduction, complete planar enumeration and the previous
certified `a_8<=1` theorem are mathematical/computational premises. The
new replay does not re-run that dependency's 164 DRAT proofs. No floating
point, solver conclusion, missing large file or external catalogue is a
premise of the new inequality. This is not a proof-assistant formalization.

The exact frontier remains `70<=r_5(F_5^3)<=72`. The advance is a global
weighted incidence inequality and one complete frame-normalized case for
72, rather than an exclusion of a selected plane shape or symmetry class.
