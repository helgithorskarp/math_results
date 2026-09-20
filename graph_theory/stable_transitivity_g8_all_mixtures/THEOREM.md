# Proof of the complete `G8` mixture theorem

## 1. Definitions

An order predicts the arc `u->v` when `u` occurs before `v`.  A transitive
tournament decomposition (TTD) is a multiset of orders whose arc counts equal
the entries of the directed multigraph being decomposed.

Let `W` be a `k`-tournament.  Its stable-transitivity number `m(W)` is the
least `a` for which some `a`-tournament `A` has a TTD and `W+A` also has a
TTD.  Equivalently, there are orders `X_1,...,X_a` and
`Y_1,...,Y_(k+a)` satisfying

```text
W + X_1 + ... + X_a = Y_1 + ... + Y_(k+a)          (1)
```

coordinatewise on directed arcs.

Let `F` be the following 20 fixed arcs:

```text
01 02 03 40 60 70 13 14 51 16 71 23 24 52 62 27 35 36 37 45.
```

The eight remaining pairs, written in increasing orientation, are

```text
E = (05,12,34,46,47,56,57,67).
```

For `d=(d_1,...,d_8)` in `{0,...,k}^8`, write `W_k(d)` for the unique
`k`-tournament having multiplicity `k` on every arc in `F`, multiplicity
`d_i` on the displayed orientation of `E_i`, and multiplicity `k-d_i` on its
reverse.  These are precisely the degree-`k` extensions of `G8`.

## 2. Margin-profile equivalence

**Lemma 1.** For a `k`-tournament `W` and integer `a>=0`, `m(W)<=a` if and
only if there is a multiset `P` of `k+2a` orders such that every directed arc
`e` is predicted exactly `W(e)+a` times by `P`.

**Proof.** Given (1), put the reversals of `X_1,...,X_a` together with all
the `Y` orders.  On any arc `e`, these `k+2a` orders predict it

```text
a - sum_i X_i(e) + sum_j Y_j(e) = W(e)+a
```

times.  Conversely, choose any `a` members `B_1,...,B_a` of `P`, set
`X_i` to the reverse of `B_i`, and use the remaining `k+a` members as the
`Y` orders.  If `B(e)` is the number of selected members predicting `e`, then
the two sides of (1) both have value `W(e)+a-B(e)`.  This proves the
equivalence for an exact size-`a` stabilizer.  Finally, a witness of size
`b<a` can be padded to size `a` by adding the same `a-b` arbitrary orders to
both sides of its decomposition equation, so this is equivalent to
`m(W)<=a`. `square`

## 3. Universal lower bound on the face

**Lemma 2.** Every order predicts at most 13 arcs of `F`.

The verifier enumerates all `8!=40,320` orders directly.  If the defect of an
order is `13` minus its number of predicted `F` arcs, the exact layer sizes
are

```text
defect:  0    1     2      3      4     5    6
count: 832  4192  9344  11584  9344  4192  832.
```

In particular, no order predicts more than 13 fixed arcs.

Now suppose `m(W_k(d))<=a`.  Lemma 1 supplies `k+2a` orders, and each of the
20 fixed arcs must occur `k+a` times.  Counting predictions of fixed arcs in
two ways gives

```text
20(k+a) <= 13(k+2a),
```

so `7k<=6a`.  Therefore

```text
m(W_k(d)) >= ceil(7k/6).                            (2)
```

## 4. Six certified residue boxes

Put `a_r=ceil(7r/6)=r+1` for `r=1,...,6`.  A sharp profile for target
`d in {0,...,r}^8` is a multiset of `r+2a_r` orders satisfying

```text
fixed arc f in F:     count(f)   = r+a_r,
missing pair E_i:     count(E_i) = a_r+d_i.          (3)
```

By Lemma 1, such a profile proves `m(W_r(d))<=a_r`.

For each `r`, `corners_dr.txt` supplies and the verifier checks profiles for
all 256 corner targets `d in {0,r}^8`.  To pass from corners to the whole box,
consider one order in a profile.  If the endpoints of some `E_i` are adjacent
in that order, exchange them.  An adjacent exchange reverses exactly their
mutual pair, so it changes `d_i` by `+1` or `-1` and leaves every other
equation in (3) unchanged.

`verify_boxes.cpp` independently:

1. enumerates and ranks all 40,320 orders;
2. reconstructs their 28-bit prediction masks;
3. checks every corner profile against (3), including its degree, length,
   target, and total `G8` defect;
4. constructs the 80,640 directed adjacent exchanges across the eight
   missing pairs and confirms by mask XOR that every exchange changes exactly
   one pair; and
5. performs breadth-first closure, retaining only the first profile for each
   encoded target in `{0,...,r}^8`.

The resulting exact coverage counts are:

| `r` | `a_r` | profile orders | targets certified |
|---:|---:|---:|---:|
| 1 | 2 | 5 | 256 |
| 2 | 3 | 8 | 6,561 |
| 3 | 4 | 11 | 65,536 |
| 4 | 5 | 14 | 390,625 |
| 5 | 6 | 17 | 1,679,616 |
| 6 | 7 | 20 | 5,764,801 |

Thus every residue box has a sharp profile:

```text
m(W_r(d)) = ceil(7r/6)  for r=1,...,6.              (4)
```

The equality uses the universal lower bound (2).  The computation contains
no heuristic cutoff: for each `r`, its success condition is exactly
`(r+1)^8` reached targets.

## 5. Additive lift to all degrees

**Theorem.** For every `k>=1` and `d in {0,...,k}^8`,

```text
m(W_k(d)) = ceil(7k/6).
```

**Proof.** Write `k=6q+r` with `0<=r<6`.  For each coordinate choose

```text
f_i = max(0,d_i-6q),       e_i=d_i-f_i.
```

Then `0<=f_i<=r` and `0<=e_i<=6q`.  Decompose each `e_i` as a sum of `q`
digits from `{0,...,6}`; this can be done independently in every coordinate,
for example by greedily taking `min(6,remaining)`.  Hence `W_k(d)` is the
sum of `q` degree-six extensions and, when `r>0`, one degree-`r` extension.

Add their profiles from (4).  Profile arc counts add, so Lemma 1 gives

```text
m(W_k(d)) <= 7q + ceil(7r/6) = ceil(7k/6).
```

For `r=0` the residual term is absent.  The reverse inequality is (2), which
proves the formula. `square`

## 6. What is finite and what is structural

The only exhaustive component is the six explicitly bounded boxes in
Section 4.  Lemma 1, the 13-hit double count, and the additive degree lift are
parameter-uniform.  The result therefore does not depend on extrapolating a
numerical pattern or imposing a cutoff on `k`.
