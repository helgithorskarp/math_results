# A sharp RSK-shape locality obstruction for Dahlberg's `1432/2134` pair

## Result

For a permutation `w`, write `Des(w)` for its descent set and `sh(w)` for
the common RSK shape when `w` is an involution.  Let

```text
C = I_5(1432),       E = I_5(2134).
```

Both sets have 21 elements.  A bijection `F:C -> E` is called
*descent-complementing* when

```text
Des(F(w)) = {1,2,3,4} \ Des(w).
```

It is *shape-local at w* when `sh(F(w)) = sh(w)'`, where the prime denotes
conjugation of partitions.

**Theorem.** Every descent-complementing bijection `F:C -> E` fails to be
shape-local on at least three elements.  This is sharp: there is such a
bijection with exactly three failures.  Order five is minimal; RSK tableau
transposition itself gives a descent-complementing, shape-local bijection for
all orders at most four.

Thus the order-five failure of plain tableau transposition is not repairable
by permuting tableaux only within conjugate RSK-shape fibers.  Any proof of
the conjectured descent-set symmetry by an RSK-based map must transfer objects
between shapes.

## Proof

For a descent set `D` and partition `lambda` of 5, put

```text
a(D,lambda) = #{w in C : Des(w)=D, sh(w)=lambda},
b(D,lambda) = #{v in E : Des(v)=[4]\D, sh(v)=lambda'}.
```

Only the following cells have unequal multiplicities:

| `lambda` | `D` | `a` | `b` |
|---|---:|---:|---:|
| `(2,1,1,1)` | `{1,3,4}` | 1 | 0 |
| `(2,2,1)` | `{1,3,4}` | 0 | 1 |
| `(2,2,1)` | `{2,3}` | 1 | 0 |
| `(3,1,1)` | `{2,3}` | 0 | 1 |
| `(2,2,1)` | `{2,4}` | 1 | 0 |
| `(3,1,1)` | `{2,4}` | 0 | 1 |

Within a cell `(D,lambda)`, at most `min(a,b)` source objects can be sent to
the required complementary-descent, conjugate-shape target cell.  Summing
this bound over all cells shows that at most 18 of the 21 objects can be
shape-local.  Hence at least three cross-shape moves are necessary.

For sharpness, transpose the RSK tableau except for these three inputs:

```text
52431 -> 34125
45312 -> 52341
35142 -> 42315.
```

Plain tableau transposition sends them respectively to `13245`, `21354`, and
`21435`; these are precisely the three outputs outside `E`.  The three stated
replacements are precisely the missing elements of `E`, have the required
complementary descent sets, and are cross-shape.  All other 18 tableau
transposes already lie in `E` and are shape-local.  This proves sharpness.

At orders below five, exhaustive definition-level inspection (or direct
inspection, since a forbidden length-four pattern first appears at order
four) confirms that tableau transposition maps `I_n(1432)` onto
`I_n(2134)`.  The checker verifies this and all claims above.

## Reproduction

Tested with CPython 3.11.2 on Debian 12.  There are no third-party
dependencies, random choices, floating-point operations, or external inputs.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 dahlberg_shape_locality_obstruction/verify.py
```

The final lines are

```text
n=5: |C|=|E|=21, maximum shape-local matches=18, forced cross-shape moves=3
verified sharp three-replacement repair and minimal order-five obstruction
```

The checker enumerates all permutations through `S_5`, tests involution and
pattern avoidance from their definitions, implements forward and inverse RSK,
tests RSK round trips on every permutation in `S_5`, and checks the lower-bound
table and explicit repaired bijection entry by entry.

## Scope and literature

This is a negative structural milestone, not a proof of Dahlberg's full
conjecture.  It strengthens the previously recorded pointwise failure of RSK
transposition at order five by ruling out *every* descent-complementing repair
that remains inside conjugate shape fibers.

The underlying major-index symmetry was conjectured by Samantha Dahlberg,
*Permutation Statistics and Pattern Avoidance in Involutions*, Section 6,
Conjecture 6.13, <https://arxiv.org/abs/1709.08252>.  Standard RSK facts used
here are that an involution corresponds to one standard Young tableau,
tableau transposition conjugates its shape, and transposition complements its
descent set.  The literature search performed for this note found work on
Grassmannian pattern avoidance and refined involution Wilf-equivalence, but no
published statement of this joint descent-set/RSK-shape obstruction.  This is
a search-relative statement, not a priority claim.
