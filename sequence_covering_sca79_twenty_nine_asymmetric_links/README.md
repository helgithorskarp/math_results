# At least twenty-nine named-asymmetric pair links in `SCA(5040;7,9)`

## Result

Let `D` be the directed graph on the nine symbols of a hypothetical
`SCA(5040;7,9)`, with an arc `w -> x` when the ordered-pair link `P_wx` is
not invariant under relabelling its other seven coordinates.

**Theorem.**  The graph `D` has at least twenty-nine arcs.

The preceding
[`twenty-eight-link theorem`](../sequence_covering_sca79_twenty_eight_asymmetric_links/README.md)
leaves three coefficient-row branches at exact 28.  This result eliminates
all three:

1. two nonconstant rows are impossible by directed-degree parity;
2. one nonconstant row is eliminated by a complete global point-link lift;
3. in the all-constant branch, the named same-type pair-link certificate
   forces a regular type-B vertex to have at least four outgoing arcs although
   its outdegree is three.

This is an unrestricted global bound.  The computation deliberately relaxes
support realizability, so its infeasibility cannot discard a genuine array.
No automorphism restriction, solver verdict, floating point, or external
catalogue is used.

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
row consumes at least two.  If `K` rows are nonconstant and
`|E(D)|=9+s`, then

```text
2s >= 12K+2(9-K).                                             (3)
```

At 28 arcs, `s=19`, so (3) gives `K<=2`.

## The two-nonconstant branch: parity

If `K=2`, equality holds in (3).  Both nonconstant rows have degrees `(7,7)`.
Every one of the seven constant rows has minimum combined excess two.  The
complete minimum options are

```text
(out_excess,in_excess)=(0,2) or (2,0);                        (4)
```

there is no `(1,1)` option.

The total outgoing excess is 19.  The two nonconstant rows contribute 12,
so the seven constant rows would have to contribute 7.  Equation (4) makes
their contribution even, a contradiction.

## The one-nonconstant branch

Let `h` be the unique nonconstant row, with degrees

```text
(outdegree(h),indegree(h))=(7+alpha,7+beta),
alpha,beta in {0,1}.                                          (5)
```

For a constant peripheral row, put

```text
F_r(a,c)=G_r+(-1)^(r+1)(r*c-a).                               (6)
```

If its asymmetric outdegree is `k`, the named immediate-successor equations
give the necessary divisibilities

```text
(8-r) divides F_r(a,c),  r=k+1,...,6.                         (7)
```

Incoming degree applies (7) after reversal,

```text
(a,c) -> (-(8c-a),-c).                                        (8)
```

There are exactly 249 nonnegative constant profiles.  Record each peripheral
degree/profile option as

```text
(out_excess,in_excess,a,c,b).
```

The eight peripheral rows have exactly

```text
10-alpha-beta                                                 (9)
```

extra combined degree units above their minimum, with separate outgoing and
incoming excess totals `13-alpha` and `13-beta`.  The exact enumeration uses
unordered multisets of eight options.  This is complete because every later
constraint depends only on the multiset of peripheral `(a,c)` values.

The global balances determine the central point link:

```text
sum_z c_z=0,       c_hz=c_z,
a_h=-sum_z a_z,    b_h=-a_h.                                 (10)
```

The exact stage counts are

| `(alpha,beta)` | multiplicity | degree/profile | column-balanced | position-feasible | point-feasible |
| --- | ---: | ---: | ---: | ---: | ---: |
| `(0,0)` | 1 | 24,380,366 | 1,218,982 | 369,484 | **0** |
| `(0,1)` or `(1,0)` | 2 | 7,673,973 | 420,290 | 125,045 | **0** |
| `(1,1)` | 1 | 2,388,261 | 149,267 | 43,785 | **0** |
| **total** |  | **42,116,573** | **2,208,829** | **663,359** | **0** |

Reversing every permutation exchanges `(alpha,beta)=(0,1)` and `(1,0)`.
On local options it sends

```text
(o,i,a,c,b) -> (i,o,-b,-c,-a),                               (11)
```

a bijection checked directly by the verifier.  This explains the middle-row
multiplicity two without a duplicate enumeration.

The 663,359 position-feasible multisets induce only 1,078 distinct central
signatures.  Even the best signature has minimum named point-cell value
`-3`.  Hence the one-nonconstant branch is impossible.

## The all-constant branch

If all rows are constant, (2) forces every row constant `c` to be zero.
Every row then has minimum asymmetric indegree and outdegree at least three.
Since each degree sum is 28, there is a unique vertex `O` of outdegree four
and a unique vertex `I` of indegree four; all other directed degrees are
three.

Exact application of (7)--(8) at degrees at most four leaves the following
point-row parameters:

| `a` | minimum outdegree | minimum indegree |
| ---: | ---: | ---: |
| `-8` | 3 | 3 |
| `-2` | 4 | 4 |
| `4` | 3 | 3 |
| `10` | 4 | 4 |

If the exceptional vertex had parameter `-2`, the remaining eight rows would
have parameters `-8` and `4`, and their total together with `-2` would be
`30-12n`, never zero for integral `n`.  Parameter `10` similarly gives
`42-12n`, again never zero.  Therefore every row has one of the two types

```text
A=(-8,0,8),       B=(4,0,-4),                                (12)
```

and (2) forces exactly three A rows and six B rows.

## A regular B source has too many forced arcs

The previous theorem supplies an exact named pair-link certificate with this
consequence:

> If the source has outdegree three, the target has indegree three, both have
> type B, and `P_wx` is coordinate-symmetric, then a nonnegative combination
> of eight pair-link cells equals `-1`, a contradiction.

For completeness, with `z_a=p_(a,0,7-a)`, five-coordinate marginals `M_ijk`,
and target boundary `T_3`, that certificate is

```text
 M_023+4M_122+9M_203-8M_212+12M_302
 -2T_3-9z_2-28z_3-33z_4-12z_5

 = p_025+p_043+10p_133+4p_142+4p_214+2p_223
   +26p_313+16p_412
 = -1.                                                        (13)
```

Choose a B vertex `w` distinct from `O`; at least five choices exist.  It has
outdegree three.  Among the other five B vertices, at most one is `I`, so at
least four are targets of indegree three.  By (13), all of those at least four
ordered links must be asymmetric.  This forces `outdegree(w)>=4`, a
contradiction.  Thus the all-constant branch is impossible.

The three cases exhaust (3), proving the theorem.

## Reproduction and trust boundary

From this directory, run

```sh
python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
sha256sum -c SHA256SUMS
```

The checker uses Python 3.11 standard-library exact integers only.  It
rebuilds the 249 constant profiles and all local options, verifies reversal
closure, enumerates every one-row multiset, evaluates all 256 cells of every
distinct central signature, checks the two-row parity obstruction, classifies
the all-constant low-degree profiles, and expands (13) entry by entry on the
36 ordered compositions.

The direct four-case baseline took 486 seconds.  The publication checker
memoizes central signatures and uses the proved reversal bijection to avoid
duplicating the mixed case; this changes only execution, not the mathematical
state space.  There is no parallelism, randomness, floating point, solver,
external input, or bulky generated certificate.
