# Proof and exact computation

## Claim

Conditional on the complete h4117 pair quotient, the accepted h4139 and h4167
filters, h4171's five-active pencil classification, and h4175's reflection-axis
closure, the 128,616 pair representatives compatible with exactly five active
curves support at most 3,767,184 `D3` orbits of possible non-four-colourable
parameters, counted conservatively by intersection multiplicity.

## Pairwise bound

Let `q={f,g}` be a retained global pair representative. If the norm curves
have total degrees `2k` and `2l`, their bihomogenizations in

```text
u = x + i sqrt(3)y,  v = x - i sqrt(3)y
```

have bidegrees `(k,k)` and `(l,l)`. The product-surface intersection number is

```text
(k,k) . (l,l) = 2kl.
```

The distinct irreducible curve factors have no common component, so their
common-zero scheme has length at most `2kl`. This is the sharp imported
bidegree bound used in h4175, replacing the older total-degree product `4kl`.

Let `H_q <= D3` be the setwise stabilizer of `q`. It preserves the common-zero
scheme. HN2 h4175 closes all three reflection axes by exact physical
three-colourings; together with h4119's closure of the rotational fixed
parameter `z=0`, it shows that `D3` acts freely on every possible
non-four-colourable parameter.
Consequently `H_q` acts freely on the possible non-four points of the common
zero scheme. Their number of `H_q` orbits is therefore bounded by

```text
floor(2kl / |H_q|).
```

Summing this bound over the global pair representatives may count a parameter
more than once if it lies on several pair systems, so it remains a safe upper
bound rather than an exact root count.

## Five-active projection

h4171 partitions the retained h4167 pair representatives into three
`D3`-invariant modes. Its exact-five mode consists of 128,616 representatives,
and every one has a pair/triple-constraint-avoiding affine-pencil extension.
The present computation reconstructs that mode and its named stabilizers:

| stabilizer order | systems | sum of `2kl` | orbit allowance |
|---:|---:|---:|---:|
| 1 | 126,660 | 3,741,632 | 3,741,632 |
| 2 | 1,956 | 51,104 | 25,552 |
| total | 128,616 | 3,792,736 | 3,767,184 |

There are no order-three stabilizers in the exact-five mode. Thus the
bidegree improvement removes 3,792,736 from the old allowance and the
reflection-free action removes a further 25,552, for a total reduction of
3,818,288.

The two modes requiring at least six active curves contain 2,740 systems and
have allowance 79,520. Adding them gives 3,846,704, exactly reproducing h4175's
independent whole-frontier accounting.

## Computational verification

The producer consumes h4171's constructive interface and h4175's independently
row/polynomial-checked named group. The verifier instead reconstructs h4171
through its independent checker and rebuilds `R` and `C` directly from
Eisenstein row transformations. For every pair it checks canonicality,
orbit-stabilizer, subgroup sizes, bidegrees, the stabilizer mask, and all mode
sums. The independently generated 131,356-row files are byte-identical.

The explicit interface records actions in the order

```text
1, R, R^2, C, RC, R^2C.
```

It must be used globally. Applying an additional fundamental-chamber
restriction to these already quotient representatives would double-count a
symmetry reduction and is invalid.

## Scope

This establishes a certified, mode-specific viability allowance and an exact
stabilizer interface. It does not enumerate common roots, prove that any bound
is attained, delete a whole pair system, close the six-active branch, or
establish a five-chromatic unit-distance graph.
