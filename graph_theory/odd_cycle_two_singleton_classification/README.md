# Critical two-singleton classification on odd cycles

## Theorem

Let `k >= 3`, label `C_(2k+1)` cyclically by `0,1,...,2k`, and set

```text
M_k = 5*2^(k-1) - 6.
```

For distinct `a,b` with `0<a<b<=2k`, consider the almost-stacked
configuration

```text
c_(a,b) = M_k e_0 + e_a + e_b.
```

Then `c_(a,b)` is nonstackable exactly when

```text
{a,b} = {k,k+2}  or  {a,b} = {k-1,k+1}.             (1)
```

The two pairs in (1) are reflections of one another.  Thus, up to the
dihedral symmetry fixing the heavy vertex, the previously certified stable
obstruction is the **unique** nonstackable configuration in this entire
two-singleton slice.  Every configuration in the slice has total mass

```text
M_k+2 = 5*2^(k-1)-4,
```

one below the proposed odd-cycle stacking number.

This is a finite-support classification for every `k`, not a bounded
catalogue.  It does not classify almost-stacked configurations with three or
more singleton piles and does not prove the conjectured stacking number.

## Signed-transfer setup

The exact split-path theorem says that a cycle configuration stacks if some
lift obtained by splitting one vertex into the two endpoints of an opened
path stacks.  For a nonempty path branch, its message is propagated by

```text
g(z) = 2z-3          if z <= 1,
       z/2           if z >= 2 is even,
       (z-3)/2       if z >= 3 is odd.
```

A target is reachable exactly when its pile plus its incoming branch
messages is at least one.  We use this criterion to give a witness for every
pair outside (1).

Put `P=2^k`.  A single unit at distance `d` along an otherwise empty branch
sends

```text
3-2^(d+1).                                             (2)
```

If two units lie on the same branch, at distances `a<b` from the target,
their combined message is

```text
3 - 2^a(2^(b-a+1)-1).                                 (3)
```

Both identities follow immediately by iterating `g(z)=2z-3` while the
effective value is at most one.

## All but five pairs stack at the heavy vertex

First suppose the two units lie on the same side of `0`, and reflect if
needed so that `1<=a<b<=k`.  Cut the first zero after vertex `b` and target
the heavy vertex.  By (3), its score is

```text
M_k + 3 - 2^a(2^(b-a+1)-1).
```

The subtracted term is `2^(b+1)-2^a <= 2P-2`.  Hence the score is at least
`P/2-1`, which is positive for `k>=3`.

It remains to put the units on opposite sides of `0`.  Write their distances
from `0` as `x,y`, with `1<=x,y<=k`, and cut a zero between them.  Equations
(2) give the heavy target the score

```text
M_k + (3-2^(x+1)) + (3-2^(y+1))
    = 5P/2 - 2^(x+1) - 2^(y+1).                       (4)
```

If neither distance is `k`, (4) is at least `P/2`.  If one distance is `k`,
then (4) is positive unless the other distance is one of `k-2,k-1,k`.
Consequently the only pairs not settled at the heavy target are

```text
(k-2,k+1), (k-1,k+1), (k,k+1), (k,k+2), (k,k+3).     (5)
```

## The three recoverable central pairs

For each of the other three pairs in (5), cut the heavy vertex `0`, use path
coordinate `k-1` as the target, and split as follows:

| singleton pair | left endpoint pile | target score |
|---|---:|---:|
| `(k-2,k+1)` | `3P/4` | `1` |
| `(k,k+1)` | `0` | `1` |
| `(k,k+3)` | `0` | `1` |

Here are uniform calculations of those scores.  For `(k,k+1)`, starting at
the right heavy endpoint and passing through the intervening zeros applies
`g` exactly `k` times and sends message one; each of the two consecutive
units preserves message one because `g(2)=1`.

For `(k,k+3)`, the heavy branch reaches message seven just before the farther
unit: for the relevant range,

```text
g^t(M_k) = 5*2^(k-1-t)-3.
```

The farther unit changes `7` into `g(8)=4`, two zeros change `4` to `2` to
`1`, and the nearer unit again preserves `1`.

For `(k-2,k+1)`, the left endpoint `3P/4` sends message `3` to the nearer
unit, which changes it to `g(4)=2`.  The right endpoint contains
`7P/4-6`; it sends message `1` to the other unit, then that unit preserves
`1`, and the final zero changes it to `g(1)=-1`.  The target score is
therefore `2+(-1)=1`.

The two unrecovered pairs in (5) are precisely (1).  The universal ancestry
certificate in
[`odd_cycle_stacking_universal_certificate`](../odd_cycle_stacking_universal_certificate/)
proves nonstackability for `{k,k+2}` for every `k>=3`; reflection gives
`{k-1,k+1}`.  This completes the classification.

## Reproduction

Only CPython's standard library is needed.  Run

```bash
./run_checks.sh
```

`verify.py` evaluates the stated split witness directly for every singleton
pair through `k=64`.  `independent_check.py` separately checks the closed
branch formulas, the five-pair exception partition, and all three central
score-one witnesses through `k=128` without importing the implementation.
The unit tests exercise boundary and mutation cases.  The run also executes
the existing all-`k` symbolic ancestry verifier on which the negative half of
the classification depends.  Finite checks audit the implementation; the
proof above is uniform in `k`.

The trust boundary is the accepted split-path theorem, the accepted universal
ancestry certificate, the displayed transfer calculations, CPython exact
integer arithmetic, and ordinary runtime behavior.  There is no randomization,
floating point, solver, or external generated input.

## Context and scope

Csernák and Soukup introduced stacking and the Almost Stacked Hypothesis and
reported odd-cycle stacking values only through `C_11`; their current paper
does not state the formula considered here:

- Tamás Csernák and Lajos Soukup, *Stacking and clearing in graph pebbling*,
  arXiv:2604.22341v1 (2026), <https://arxiv.org/abs/2604.22341>.

The result supplies a structural uniqueness statement inside a natural
almost-stacked slice.  It does not establish ASH, reduce arbitrary
configurations to this slice, or prove an odd-cycle upper bound.  Targeted
searches of the primary source and the committed Discovery Net graph on
20 September 2026 found no prior statement of this classification.  This is
search-relative novelty, not a historical-priority claim.
