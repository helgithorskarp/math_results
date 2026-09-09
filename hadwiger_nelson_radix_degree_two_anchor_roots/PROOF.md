# Proof and exact computation

## Claim

Conditional on the predecessor `A5(z)` frontier and its accepted closed loci,
the 400 post-h4181 exact-five global pair representatives containing a
degree-two anchor support at most 574 setwise-stabilizer orbits of possible
non-four physical parameters before applying h4185. Forty-four of the pair
systems support none. HN2 h4185 subsequently proves every point on these six
anchor circles three-colourable, so all 400 are closed in the live frontier.

## Circle parametrization

Write `z=x+i sqrt(3)y`, and write an Eisenstein coefficient as a pair
`(a,b)` representing `a+b(1+i sqrt(3))/2`. Each selected anchor is an event
curve with coefficient support exactly `{0,1}`, total degree two, and leading
coefficient of Eisenstein norm one. Its equation is therefore the unit circle

```text
|a0+a1 z|^2=1,       c=-a0/a1.
```

The computation checks these properties directly for all 400 selected pairs.
For each of the six possible centers it uses

```text
x = c_x + (1-3t^2)/(1+3t^2),
y = c_y + 2t/(1+3t^2).
```

Because `1+3t^2` is positive on the real line, this parametrizes the real
circle bijectively except for `(c_x-1,c_y)`. That omitted point is evaluated
directly in every equation and every closed locus.

## Exact closed-locus marker

For each center, every one of the complete 2,400 collision rows is expanded
as exact real and imaginary polynomials in `x,y`, pulled back to `Q[t]`, and
represented by the gcd of the two pullbacks. Taking the squarefree lcm over
all rows gives exactly the collision parameters on the circle. The three
reflection axes

```text
y=0,  y=x,  y=-x
```

and the radial unit circle `x^2+3y^2=1` are pulled back in the same way. Their
squarefree lcm is the accepted closed-locus marker. The six markers have
degrees 13 or 14; their collision submarkers have degrees 9 or 10. The
omitted circle point is again tested separately.

For a second event factor `g`, let `p(t)` be its cleared-denominator pullback.
The exact factors are

```text
p_sf = squarefree(p),
p_closed = gcd(p_sf, closed_marker),
p_eligible = p_sf / p_closed.
```

An exact Sturm sequence over `Q` counts the distinct real roots of all three
factors and verifies the partition. No floating-point root isolation or
tolerance is used.

## Census and symmetry

The per-pair root profile is:

| `(all, closed, eligible, stabilizer order)` | pair systems |
|---|---:|
| `(2,0,2,1)` | 152 |
| `(2,0,2,2)` | 38 |
| `(2,1,1,1)` | 114 |
| `(2,2,0,1)` | 28 |
| `(2,2,0,2)` | 14 |
| `(3,1,2,1)` | 16 |
| `(3,2,1,1)` | 4 |
| `(3,3,0,1)` | 2 |
| `(4,0,4,1)` | 6 |
| `(4,1,3,1)` | 8 |
| `(4,2,2,1)` | 14 |
| `(4,2,2,2)` | 2 |
| `(6,2,4,2)` | 2 |

This sums to 890 distinct roots within their pair systems, split into 272
closed and 618 eligible roots. The setwise stabilizers have orders `1:344`
and `2:56`. By h4175, away from the collision/fixed and reflection-axis loci,
the named `D3` action is free. Each pair stabilizer therefore acts freely on
its eligible roots. Division by its checked order gives exactly 574 eligible
root orbits. The divisibility is also checked pair by pair.

The old non-four allowance for these 400 systems was 2,904. Replacing it by
574 saves 2,330. The 44 zero-eligible systems are removed globally, while the
other 356 retain their exact root-orbit allowances. A physical parameter may
lie on multiple pair systems, so summing their orbit counts can overcount and
is only an upper bound globally.

## Exact integration with h4185

The separately regenerated h4185 frontier interface contains 424 removed
global pair rows. Exact row comparison shows that the 400 pairs in this root
census are all present, with no missing or extra exact-five row, and use
exactly h4185's six anchor curve IDs. The other 24 h4185 rows were already in
the at-least-six mode and have allowance 108. Thus the two calculations
reconcile h4185's removed allowance exactly:

```text
2330  root-census reduction within the 400 rows
 574  residual root-orbit allowance then closed by h4185
 108  allowance of h4185's 24 additional rows
----
3012  total h4185 removed allowance.
```

The pair lists and both generated interfaces are hash-bound in
`INTEGRATION.json` and checked by `crosscheck_h4185.py`. This does not
independently verify h4185's colouring theorem; it verifies the precise
geometric/frontier interface consumed by that theorem.

## Independent implementations

`produce.py` uses SymPy's exact `QQ` factorization and Sturm root counts.
`verify.py` independently reconstructs the source interfaces and collision
rows, implements polynomial arithmetic, gcd/lcm, squarefree reduction and
Sturm sequences with the standard library, and reproduces the complete
400-entry interface byte for byte. The compact committed certificate binds
that interface by canonical and raw-file SHA-256 digests.

## Scope

The accepted closed-locus implications are imported dependencies. This result
does not decide chromaticity at the 574 surviving pair-root orbits, globally
deduplicate roots shared by different systems, close the full exact-five or
at-least-six frontier, or establish a five-chromatic graph. H4185, not this
root census, supplies the later three-colour closure of those 574 orbit slots.
