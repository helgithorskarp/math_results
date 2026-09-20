# Exact tail conductor of the stable odd-cycle stacking ray

## Theorem

Let `k >= 3`, label the vertices of `C_(2k+1)` cyclically, and put

```text
c_(k,h) = h e_0 + e_k + e_(k+2).
H_k     = 5*2^(k-1) - 5.
```

Then

```text
c_(k,h) is stackable for every h >= H_k,
```

whereas the previously certified configuration `c_(k,H_k-1)` is not
stackable.  Thus `H_k` is the exact **tail conductor** of this ray: it is the
least integer `H` for which every `c_(k,h)`, `h >= H`, is stackable.

In particular, the stable obstruction used for the universal lower bound is
locally sharp for every odd cycle, not only for the previously tested finite
range.  At `h=H_k` the total mass is

```text
H_k + 2 = 5*2^(k-1) - 3,
```

the conjectured stacking number of `C_(2k+1)`.  This theorem does **not**
prove that every configuration of that mass is stackable.

The result uses the exact split-path theorem: a cycle configuration is
stackable if some lift obtained by cutting a vertex and splitting its pile
between the two endpoints is stackable on the opened path.  A path lift
stacks at a target precisely when its signed transfer score is positive.

## Four explicit split certificates

Write `P=2^k`, `h=H_k+d`, and use path coordinates after a cut: cutting
vertex `s` orders the path as

```text
s_left, s+1, ..., s-1, s_right.
```

The following table gives a positive certificate for every `d>=0`.

| excess `d` | cut | left endpoint pile | target path coordinate | score |
|---:|---:|---:|---:|---:|
| `0` | `0` | `P-8` | `2` | `1` |
| `1` | `0` | `P-4` | `1` | `1` |
| `2` | `k` | `0` | `1` | `1` |
| `d>=3` | `0` | `P+d-5` | `0` | `d-2` |

All endpoint piles are nonnegative and do not exceed the cut pile for
`k>=3`.  It remains to calculate the displayed scores.

## Signed-transfer calculation

For a nonempty path branch, listed from its leaf toward its target, add each
new pile to the incoming message and apply

```text
g(z) = 2z-3       if z <= 1,
       z/2        if z >= 2 is even,
       (z-3)/2    if z >= 3 is odd.
```

An entirely empty branch has message zero.  A target is reachable exactly
when its pile plus its two branch messages is at least one.

For `d=0`, the right endpoint receives `3P/2+3`; for `d=1` and `d>=3`, it
receives `3P/2`.  Both endpoint values send the same first message `3P/4`.
Moving through the `k-2` zero piles down to vertex `k+3` successively halves
this to `3`.  The piles at vertices `k+2,k+1,k` are `1,0,1`, so the next
three messages are `2,1,1`.  Starting from message `1`, passage through `r`
further zero piles gives

```text
3 - 2^(r+1).                                      (1)
```

Therefore the right-branch messages at target coordinates `2`, `1`, and `0`
are, respectively,

```text
3-P/4,   3-P/2,   3-P.                           (2)
```

For `d=0`, the left branch `(P-8,0)` sends `P/4-2` (also zero when `k=3`),
and (2) makes the target score one.  For `d=1`, the left leaf `P-4` sends
`P/2-2`, again giving score one.  For `d>=3`, the target itself contains
`P+d-5`; adding the last message in (2) gives `d-2>=1`.

For `d=2`, cut the unit pile at vertex `k` as `0+1` and target vertex `k+1`.
Starting at the right endpoint, its unit sends `-1`.  Crossing the `k-1`
zeros at vertices `k-1,...,1` changes this to `3-2P`.  The heavy pile is
`5P/2-3`, so the effective value there is `P/2` and the outgoing message is
`P/4`.  The next `k-2` zeros halve this to `1`, and the unit at vertex `k+2`
preserves message `1`.  The other branch is empty, so the target score is
one.

These four cases prove stackability for the whole ray `h>=H_k`.  The
non-stackability of `c_(k,H_k-1)` is the universal ancestry-certificate
theorem in
[`odd_cycle_stacking_universal_certificate`](../odd_cycle_stacking_universal_certificate/).

## Reproduction

Only CPython's standard library is required.  From this directory run

```bash
./run_checks.sh
```

`verify.py` evaluates every displayed split directly from the path transfer
definition over a configurable range and checks additional very large
excesses.  `independent_check.py` instead checks the phase identities
`(1)`--`(2)` and the four closed score formulas without importing the direct
path implementation.  `test_verify.py` exercises malformed and mutated
certificates.

The universal theorem is the calculation above, not extrapolation from the
finite audit.  The source checker trusts CPython exact integer arithmetic and
ordinary runtime behavior; it uses no floating point, randomness, solver, or
external data.

## Context and scope

The exact odd-cycle formula remains open.  Csernák and Soukup report the
values through `C_11` and explicitly state that they have no conjecture for
the general odd-cycle stacking number:

- Tamás Csernák and Lajos Soukup, *Stacking and clearing in graph pebbling*,
  arXiv:2604.22341v1 (2026), <https://arxiv.org/abs/2604.22341>.

The graph's stable-family conjecture identified the present ray and reported
finite tests showing that one extra heavy pebble makes its obstruction
stackable.  The theorem here replaces those tests by uniform certificates
and determines the exact tail conductor.  It depends on the accepted
split-path theorem and the accepted universal ancestry lower certificate.
Targeted primary-source and committed-graph searches on 20 September 2026
found no prior all-`k` local-sharpness theorem.  This is search-relative
novelty, not a historical-priority claim.
