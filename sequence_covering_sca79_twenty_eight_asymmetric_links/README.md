# At least twenty-eight named-asymmetric pair links in `SCA(5040;7,9)`

## Result

Let `D` be the directed graph on the nine symbols of a hypothetical
`SCA(5040;7,9)`, with an arc `w -> x` when the ordered-pair link `P_wx` is
not invariant under relabelling its other seven coordinates.

**Theorem.**  The graph `D` has at least twenty-eight arcs.

The preceding
[`twenty-seven-link theorem`](../sequence_covering_sca79_twenty_seven_asymmetric_links/README.md)
leaves two structurally different possibilities at equality.  This result
eliminates both:

1. an exact enumeration of the global point-flow equations rules out the
   branch with one nonconstant point-link coefficient row; and
2. two explicit nonnegative-cell certificates rule out every symmetric link
   between equal point-row types in the all-constant branch, where the 3+6
   type split would require at least 36 asymmetric links.

Thus this is an unrestricted improvement of the global lower bound, not an
automorphism-restricted calculation.  No solver verdict, floating point, or
external catalogue is used.

## Point-link input and the exact-27 dichotomy

For every symbol `w`, the exact point-link coordinates are

```text
F_w(S) = G_|S| + (-1)^(|S|+1)
                   (sum_(x in S)c_wx-a_w),                    (1)

G = (560,70,20,10,8,10,20,70,560),
b_w = sum_(x!=w)c_wx-a_w.
```

The global path-flow balances are

```text
sum_w a_w=0,
sum_(w!=x)c_wx=0 for every column x.                           (2)
```

The earlier boundary theorem proves that a nonconstant coefficient row has
asymmetric indegree and outdegree at least seven, consuming at least twelve
combined degree-excess units.  A constant row consumes at least two.  If
`K` rows are nonconstant and `|E(D)|=9+s`, then

```text
2s >= 12K+2(9-K).                                             (3)
```

At 27 arcs, (3) gives `K<=1`.  The cases `K=1` and `K=0` are treated
separately below.

## The one-nonconstant branch

Let `h` be the unique nonconstant row.  Its degrees are

```text
(outdegree(h),indegree(h))=(7+alpha,7+beta),
alpha,beta in {0,1}.                                          (4)
```

The other eight rows are constant.  For such a row, write

```text
F_r(a,c)=G_r+(-1)^(r+1)(r*c-a).                               (5)
```

If its asymmetric outdegree is `k`, the named immediate-successor equations
give the necessary divisibilities

```text
(8-r) divides F_r(a,c),  r=k+1,...,6.                         (6)
```

Incoming degree applies (6) after reversal,

```text
(a,c) -> (-(8c-a),-c).                                        (7)
```

There are exactly 249 nonnegative constant profiles.  Record a peripheral
degree/profile option as

```text
(out_excess,in_excess,a,c,b).
```

At 27 arcs the eight peripheral rows have exactly

```text
8-alpha-beta                                                  (8)
```

extra combined degree units above their minimum cost.  The verifier
enumerates every unordered multiset of eight local options with this exact
extra total and with the separate incoming and outgoing totals.  This is a
relaxation of support realizability, hence cannot discard a genuine array.

For peripheral constant values `c_z`, the global balances determine the
entire central point link:

```text
sum_z c_z=0,       c_hz=c_z,
a_h=-sum_z a_z,    b_h=-a_h.                                  (9)
```

The complete exact count is

| stage | surviving unordered multisets |
| --- | ---: |
| degree/profile totals | 3,890,963 |
| column balance | 259,869 |
| central position nonnegativity | 75,293 |
| all 256 central point cells | **0** |

The 75,293 position-feasible cases induce 460 distinct central signatures.
Even the best signature has minimum point-cell value `-3`.  Therefore the
one-nonconstant exact-27 branch is impossible.

## The all-constant branch

If all nine rows are constant, (2) forces every row constant to be zero.
Exact degree 27 and (6)--(7) then force every vertex of `D` to have degrees
`(3,3)`.  The only possible point-row parameters are

```text
type A: (a,c,b)=(-8,0,8),
type B: (a,c,b)=( 4,0,-4).                                    (10)
```

The first balance in (2) forces exactly three type-A rows and six type-B
rows.

For either type parameter `t in {-8,4}`, put

```text
f_t(r)=G_r+(-1)^r*t.                                          (11)
```

This is the common value of the point cell with a named predecessor set of
size `r`.

## Forced adjacent-endpoint values on a symmetric nonarc

Suppose `P_wx` is coordinate-symmetric and both endpoints have type `t`.
Let

```text
p_abc
```

be its common cell value when `a` other symbols precede `w`, `b` lie between
`w,x`, and `c` follow `x`, where `a+b+c=7`.  Write

```text
z_a=p_(a,0,7-a).                                              (12)
```

Vertex `w` has three asymmetric out-neighbours and five symmetric ones.
Choose a predecessor set containing all three asymmetric out-neighbours and
partition its rows by the immediate successor of `w`.  Exchanging named
symmetric successors gives

```text
z_a=f_t(a)/(8-a),  a=4,5,6,
z_7=f_t(7).                                                    (13)
```

Likewise, `x` has three asymmetric in-neighbours.  Choose its predecessor set
inside its five symmetric in-neighbours and partition by the immediate
predecessor of `x`.  Exchanges give

```text
z_0=f_t(1),
z_a=f_t(a+1)/(a+1),  a=1,2,3.                                (14)
```

Consequently the eight values in (12) would have to be

```text
type A: (78,6,6,0,0,6,6,78),
type B: (66,12,2,3,3,2,12,66).                               (15)
```

## Two exact nonnegative-cell certificates

For `i+j+k=5`, the defining five-coordinate marginal equation of a
coordinate-symmetric pair link is

```text
M_ijk := p_(i+2,j,k)+p_(i,j+2,k)+p_(i,j,k+2)
       +2p_(i+1,j+1,k)+2p_(i+1,j,k+1)+2p_(i,j+1,k+1)
       = i!j!k!.                                               (16)
```

The target point boundary at predecessor-union size three is

```text
T_3 := sum_(i=0)^3 binom(3,i)p_(i,3-i,4)=f_t(4).              (17)
```

For type A, the following exact linear combination of (12), (16), and (17)
is

```text
-M_203+M_212+T_3+z_2+z_3+z_4

 = p_034+3p_124+2p_214+p_223+p_232+2p_322+p_412
 = -2.                                                        (18)
```

For type B, an analogous combination is

```text
 M_023+4M_122+9M_203-8M_212+12M_302
 -2T_3-9z_2-28z_3-33z_4-12z_5

 = p_025+p_043+10p_133+4p_142+4p_214+2p_223
   +26p_313+16p_412
 = -1.                                                        (19)
```

Every cell on the middle lines of (18) and (19) is nonnegative.  Their
negative right sides are contradictions.  Hence every ordered pair whose
endpoints have the same type must be an arc of `D`.

There are three A symbols and six B symbols, so the number of forced arcs is

```text
3*2 + 6*5 = 36,                                               (20)
```

contradicting the assumption that `D` has 27 arcs.  This eliminates the
all-constant branch.  Together with the previous section, it proves the
theorem.

## Reproduction and trust boundary

From this directory, run

```sh
python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
sha256sum -c SHA256SUMS
```

The checker uses Python 3.11 standard-library exact integers only.  It
rebuilds all 249 constant profiles and all local degree options, exhausts the
complete one-nonconstant branch, checks every central point cell, derives the
forced sequences (15), and reconstructs both certificate identities entry by
entry as vectors on the 36 ordered compositions.  Runtime is about 70 seconds
on the publication machine and memory use is modest.  There is no random
choice, floating point, solver, external input, or bulky generated
certificate.
