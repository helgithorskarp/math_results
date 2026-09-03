# A 23-vertex branched-broom counterexample to symmetric double-broom extremality

## Result

For a finite tree `T`, let `N(T)` be the number of non-stackable pebbling
configurations of maximum possible mass `stack(T)-1`.  The committed
sibling-leaf classification gives

```text
N(T) = sum over maximizing leaf-parents p of
       binom(X_p + d_p - 1, d_p - 1),
```

where `d_p` is the number of graph leaves adjacent to `p` and

```text
X_p = sum over nonleaf vertices u of deg_T(u) * 2^dist_C(p,u).
```

Here `C` is the nonleaf core of `T`.

Define `R(d,e,t)` as follows.  Start with a path

```text
p = v_0 - v_1 - ... - v_t = q,
```

attach `d` leaves directly to `p`, and attach `e` pairwise disjoint two-edge
arms `q-a_i-b_i` to `q`.  Thus every `b_i` is a graph leaf and every `a_i`
has degree two.  The order is

```text
|V(R(d,e,t))| = d + 2e + t + 1.
```

For

```text
T = R(8,4,6),
```

the tree has 23 vertices.  The eight leaves at `p` are its unique maximizing
sibling class, with

```text
X_p = 1477.
```

Consequently

```text
N(T) = binom(1484,7)
     = 3,100,645,395,776,119,256.
```

Every symmetric double broom on 23 vertices has parameters
`B(a,a,22-2a)` for `1 <= a <= 10`.  Their largest critical multiplicity is
attained at `B(6,6,10)` and equals

```text
2 * binom(9224,5)
= 1,111,665,975,462,168,688.
```

Therefore `R(8,4,6)` has more maximum-mass non-stackable configurations than
every symmetric double broom of the same order.  This refutes the committed
symmetric-double-broom extremal conjecture.  It occurs at the first order
after the independently reviewed global census through order 22.

## Proof of the two potentials

The nonleaf degrees of `R(d,e,t)` are

- `d+1` at `p`;
- `2` at each `v_j`, `1 <= j < t`;
- `e+1` at `q`; and
- `2` at each `a_i`.

Evaluating the distance potential at `p` gives

```text
X_p
 = d+1 + sum_(j=1)^(t-1) 2*2^j + (e+1)2^t + e*2*2^(t+1)
 = d-3 + (5e+3)2^t.
```

At any one of the arm endpoints `a_i`, the same calculation gives

```text
X_a
 = (d+1)2^(t+1)
   + sum_(j=1)^(t-1) 2*2^(t-j+1)
   + 2(e+1) + 2 + 8(e-1)
 = (d+3)2^(t+1) + 10e - 12.
```

For `(d,e,t)=(8,4,6)`, these are

```text
X_p = 8-3 + 23*64 = 1477,
X_a = 11*128 + 40-12 = 1436.
```

The graph leaves are precisely the eight leaves adjacent to `p` and the four
vertices `b_i`, whose parents have potential `X_a`.  Since `1477 > 1436`,
only `p` belongs to the maximizing-parent set, and the sibling-leaf formula
gives `N(T)=binom(1477+8-1,8-1)=binom(1484,7)`.

For a symmetric double broom `B(a,a,l)`, the same established formula is

```text
N(B(a,a,l)) = 2 * binom(2^l(a+3)+2a-4, a-1).
```

Substitution for the ten possible 23-vertex parameter pairs is an exact
finite comparison.  The full table is emitted by both checkers.

## Reproduction

Requires CPython 3.11 or later and only the standard library.

```bash
python3 verify_formula.py
python3 verify_direct.py
```

`verify_formula.py` checks the displayed algebraic formulas and all ten
symmetric-double-broom values.  `verify_direct.py` does not use those
potential formulas: it builds the trees as adjacency lists, finds leaves and
nonleaves, obtains every distance by breadth-first search, and applies the
sibling-leaf count formula to the reconstructed potentials.

Both programs end with

```text
status=VERIFIED
```

and report candidate value
`3100645395776119256`, best symmetric value `1111665975462168688`, and
difference `1988979420313950568`.

A fresh CPython 3.11.2 run gave these SHA-256 values:

```text
500278a1d414a93d6d44c587ecfcdac2900db3cd55717ae16c1ee1ab4fdcdafc  verify_formula.py
3aef2f717c8a8c286ffbfd446268c20ac5b6e36a78754c03eed62e6b75f85fad  verify_direct.py
04f61de213aed5f94e7fc51aad32264eec8f86123de341f7b7c1e2efba9285b9  verify_formula.py output
d5dd818dcad413654f41d8706a13acf284f68ffc0582fad28c434d31d5e41bf5  verify_direct.py output
```

## Scope and trust boundary

The potential identities and exact comparison are ordinary integer proofs.
The scripts are corroborating definition-level checks, not the logical basis
for the theorem.  They use arbitrary-precision Python integers and make no
network calls.  No solver, floating point, random sampling, external data,
or exhaustive enumeration of all 23-vertex trees is used.

The count formula is imported from the committed and independently reviewed
sibling-leaf classification.  This artifact does not re-prove the underlying
tree-stacking transfer theorem, and it does not claim that `R(8,4,6)` is the
global maximizer among all 23-vertex trees.  It proves only the decisive
counterexample: no symmetric double broom is a maximizer at order 23.

The original stacking parameter and tree formula problem are due to Tamás
Csernák and Lajos Soukup, *Stacking and clearing in graph pebbling*,
arXiv:2604.22341 (2026): <https://arxiv.org/abs/2604.22341>.  Their paper and
public computation repository introduce the stacking problem but do not
study multiplicities of maximum-mass obstructions.  Targeted searches found
no earlier occurrence of this multiplicity counterexample.  This is only a
search-relative novelty statement, not a priority claim.
