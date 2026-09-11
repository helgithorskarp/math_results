# At least thirty named-asymmetric pair links in `SCA(5040;7,9)`

## Result

Let `D` be the directed graph on the nine symbols of a hypothetical
`SCA(5040;7,9)`, with an arc `w -> x` when the ordered-pair link `P_wx` is
not invariant under relabelling its other seven coordinates.

**Theorem.**  The graph `D` has at least thirty arcs.

The preceding
[`twenty-nine-link theorem`](../sequence_covering_sca79_twenty_nine_asymmetric_links/README.md)
leaves three coefficient-row branches at exact 29.  All three are now
eliminated:

1. a new aligned-cell identity reduces the branch with two nonconstant rows
   to 306 exact aggregate profiles, every one with a negative point cell;
2. a coefficient-signature dynamic program leaves only six possibilities
   with one nonconstant row, and a named-coordinate multiplicity argument
   eliminates all six at once; and
3. the all-constant branch has four global point profiles, all contradicted
   by a complete `A/B` family of regular-endpoint pair-link certificates.

This is an unrestricted global bound.  The finite searches use relaxations
of support realizability, so their infeasibility cannot discard a genuine
array.  No automorphism restriction, solver verdict, floating point, or
external catalogue is used.

## Degree budget

Every point link has exact integral coordinates

```text
F_w(S) = G_|S| + (-1)^(|S|+1)
                   (sum_(x in S)c_wx-a_w),                    (1)

G = (560,70,20,10,8,10,20,70,560),
b_w = sum_(x!=w)c_wx-a_w,
```

and the nine rows obey

```text
sum_w a_w=0,
sum_(w!=x)c_wx=0 for every column x.                           (2)
```

A nonconstant coefficient row has asymmetric indegree and outdegree at least
seven, consuming at least twelve combined degree-excess units.  A constant
row consumes at least two.  If `K` rows are nonconstant and `|E(D)|=9+s`,
then

```text
2s >= 12K+2(9-K).                                             (3)
```

At 29 arcs, `s=20`, so (3) gives `K<=2`.

## Two nonconstant rows: an aligned-cell obstruction

Write the two nonconstant rows as `h_1,h_2`.  Their degrees are

```text
(7+alpha_i,7+beta_i),
A=alpha_1+alpha_2, B=beta_1+beta_2.                            (4)
```

The seven other rows are constant, with profiles `(a_z,c_z)`.  Their total
extra combined degree above the constant-row minimum is `2-A-B`; their
outgoing and incoming excess totals are respectively `8-A` and `8-B`.
Exact enumeration of the local divisibility options gives:

| `(A,B)` | local option multisets | distinct `(a_z,c_z)` multisets |
| --- | ---: | ---: |
| `(0,0)` | 538 | 226 |
| `(0,1)` | 62 | 20 |
| `(0,2)` | 20 | 20 |
| `(1,0)` | 62 | 20 |
| `(1,1)` | 0 | 0 |
| `(2,0)` | 20 | 20 |
| **total** | **702** | **306** |

Here is the global obstruction that makes this small enumeration decisive.
Put

```text
C=sum_z c_z,       A_0=sum_z a_z.                             (5)
```

The column balances (2) force both cross-coefficients to be `-C` and, for
each peripheral coordinate `z`,

```text
c_(h_1,z)+c_(h_2,z)=c_z-C.                                   (6)
```

The first balance in (2) gives `a_(h_1)+a_(h_2)=-A_0`.  Align the two cross
coordinates and the seven common peripheral coordinates, and define

```text
D=(-2C,c_1-C,...,c_7-C).                                     (7)
```

For every subset `S` of these eight aligned coordinates, the sum of the two
corresponding central point cells must be

```text
H(S)=2G_|S|+(-1)^(|S|+1)(sum_(i in S)D_i+A_0) >= 0.           (8)
```

The checker evaluates all 256 values in (8) for all 306 aggregate profiles.
Every profile has a negative value: their minima range from `-60` to `-1`.
Thus `K=2` is impossible.  Notice that (8) does not attempt to split the
aggregate data between `h_1` and `h_2`; it is a necessary consequence of the
global balances and therefore eliminates every such split simultaneously.

## One nonconstant row: six signatures and one common obstruction

Let `h` be the unique nonconstant row and write

```text
(outdegree(h),indegree(h))=(7+alpha,7+beta),
alpha,beta in {0,1}.                                         (9)
```

For a constant peripheral row put

```text
F_r(a,c)=G_r+(-1)^(r+1)(r*c-a).                              (10)
```

If its asymmetric outdegree is `d`, the named immediate-successor equations
give the necessary divisibilities

```text
(8-r) divides F_r(a,c),  r=d+1,...,6.                        (11)
```

Incoming degree applies (11) after reversal,

```text
(a,c) -> (a-8c,-c).                                          (12)
```

There are exactly 249 nonnegative constant profiles, and their constants
range from `-10` through `10`.  If the sorted peripheral constants are
`c_1<=...<=c_8`, (2) determines the central coefficient multiset to be that
same tuple and forces its sum to zero.  All 256 central point cells are
nonnegative exactly when

```text
L(c) <= a_h <= U(c),                                         (13)

L(c)=max_(r even)(sum of largest r entries-G_r),
U(c)=min_(r odd) (sum of smallest r entries+G_r).
```

Excluding the all-zero tuple, (13) leaves 1,254 coefficient tuples and 4,566
integer pairs `(a_h,c)`.  For each pair the checker runs a dynamic program on

```text
(sum of peripheral a, sum of minimum outdegrees,
                         sum of minimum indegrees).           (14)
```

It matches the central balance and the relaxed peripheral degree budgets
`22-alpha` and `22-beta`.  Only six signatures survive:

| `a_h` | central coefficient multiset | feasible `(alpha,beta)` |
| ---: | --- | --- |
| 0 | `(-5,-3,0,0,0,0,3,5)` | `(0,0)` |
| 4 | `(-6,0,0,0,0,0,0,6)` | `(0,0)` |
| 4 | `(-6,0,0,0,0,0,3,3)` | `(0,0),(1,0)` |
| 4 | `(-3,-3,0,0,0,0,0,6)` | `(0,0),(0,1)` |
| 4 | `(-3,-3,0,0,0,0,3,3)` | `(0,0),(0,1),(1,0)` |
| 4 | `(-3,0,0,0,0,0,0,3)` | `(0,0)` |

This relaxed list is enough.  If `alpha=0`, exactly one outgoing link from
`h` is coordinate-symmetric.  Symmetry of `P_hx` forces the other seven
coefficients in row `h` to be equal.  Thus some coefficient must have
multiplicity at least seven.  The identical argument for an incoming
symmetric link applies when `beta=0`.

Every tuple in the table has maximum multiplicity at most six.  It therefore
requires `(alpha,beta)=(1,1)`, but that pair occurs in none of the relaxed
survivor sets.  Hence `K=1` is impossible.

## All constant rows: four profiles and all endpoint types

If all rows are constant, (2) forces every row constant to be zero.  Every
row has minimum asymmetric indegree and outdegree at least three, so the
total 29 permits only two excess units in each direction and no degree above
five.  Applying (11)--(12) leaves

| `a` | minimum outdegree | minimum indegree |
| ---: | ---: | ---: |
| -8 | 3 | 3 |
| -6 | 5 | 5 |
| -4 | 5 | 5 |
| -2 | 4 | 4 |
| 0 | 5 | 5 |
| 2 | 5 | 5 |
| 4 | 3 | 3 |
| 6 | 5 | 5 |
| 8 | 5 | 5 |
| 10 | 4 | 4 |

The balance `sum a=0` and the two-unit budget leave exactly four multisets.
Writing

```text
A=(-8,0,8),  B=(4,0,-4),  X=(-2,0,2),  Y=(10,0,-10),          (15)
```

they are

```text
A^4 B^3 Y^2,     A^3 B^4 X Y,
A^3 B^6,         A^2 B^5 X^2.                               (16)
```

The remaining ingredient covers every ordered combination of regular
endpoint types.  If the source has outdegree three, the target has indegree
three, both have type `A` or `B`, and `P_wx` were coordinate-symmetric, an
exact nonnegative-cell certificate would have a negative right side.

For clarity, put `z_a=p_(a,0,7-a)`.  For `i+j+k=5`, let

```text
M_ijk = p_(i+2,j,k)+p_(i,j+2,k)+p_(i,j,k+2)
       +2p_(i+1,j+1,k)+2p_(i+1,j,k+1)+2p_(i,j+1,k+1)
       = i!j!k!.                                              (17)
```

The same-type `AA` and `BB` certificates were established in the
[`twenty-eight-link result`](../sequence_covering_sca79_twenty_eight_asymmetric_links/README.md).
Their right sides are respectively `-2` and `-1`, and the present checker
reconstructs both from scratch.

For the missing `AB` direction, the forced adjacent-endpoint values are

```text
(z_0,...,z_7)=(66,12,2,3,0,6,6,78).                         (18)
```

With source and target boundaries

```text
S_4=sum_(j=0)^3 binom(3,j)p_(4,j,3-j)=F_A(4)=0,
T_4=sum_(i=0)^4 binom(4,i)p_(i,4-i,3)=F_B(5)=6,              (19)
```

the exact identity is

```text
-3M_104+6M_113-8M_122+4M_131
-9M_203+12M_212-2M_221-10M_302
+3S_4+2T_4+3z_1+15z_2+31z_3+24z_4+10z_5

= 2p_043+p_124+2p_133+4p_151+21p_223+6p_241
  +2p_322+p_412+7p_421+3p_430
= -1.                                                         (20)
```

The middle expression is nonnegative, a contradiction.  Reversing every
permutation preserves types `A,B` and turns `AB` into `BA`, so this also
covers the fourth ordered endpoint type.

In each profile in (16) containing `X` or `Y`, the two special vertices
consume the entire degree budget.  The seven `A/B` vertices therefore all
have degrees `(3,3)`, and any one of them has forced arcs to the other six.
In the all-`A/B` profile, at least seven vertices have outdegree three and at
least seven have indegree three.  Choose a degree-three source: at least six
of the other eight vertices are degree-three targets, again forcing at least
six outgoing arcs.  Both conclusions contradict outdegree three.  Hence
`K=0` is impossible, completing the proof.

## Reproduction and trust boundary

From this directory, run

```sh
python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
sha256sum -c SHA256SUMS
```

The checker uses Python 3.11 standard-library exact integers only.  It
rebuilds all 249 constant profiles and the local divisibility options,
exhausts the 306 two-row aggregate profiles and all their aligned cells,
enumerates the complete one-row coefficient/signature relaxation, verifies
the six multiplicity obstructions, classifies all four constant-row global
profiles, and expands the `AA`, `BB`, and `AB` certificates entry by entry as
vectors on the 36 ordered compositions.  Runtime is about ten seconds and
memory use is modest.  There is no random choice, floating point, solver, or
external input.
