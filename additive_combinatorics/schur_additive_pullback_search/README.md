# A zero-class bound and exact searches for additive Schur pullbacks

Let a word `h[1..N]` take integer values in `[-m,m]`. Require that its
zero positions form a sum-free set, and that

```
h[x] + h[y] = h[x+y]
```

whenever all three labels are nonzero. All integer sums through `N`,
including `x=y`, are included. Such a word permits pulling back **any**
Schur colouring of `[1,m]` by absolute value and using one additional
colour at the zero positions. Indeed, the absolute values in a nonzero
signed equation form a positive Schur triple after a possible permutation.

This directory proves a general cardinality restriction on the zero class
and supplies two exact search implementations. They completely exclude
`(N,m)=(242,80)`. The attempted target `(537,160)` remains **UNKNOWN**
at the stated node cap. There is no new bound for `S(6)`, no exclusion of
all height-160 pullbacks, and no proof of a general `N <= 3m+1` ceiling.

## Lemma: the zero class has at most m+1 elements

Write `T={v:h[v]=0}`. Then **`|T| <= m+1`**.

If `T` is empty there is nothing to prove. Otherwise let `t0=min(T)`, set
`P(t0)=0`, and set `P(t)=h[t-t0]` for the other elements of `T`. Every
positive difference of two elements of `T` lies outside `T`: if `x<y`
and `y-x` also belonged to `T`, then `x+(y-x)=y` would violate sum-freeness.

For `t0<x<y` in `T`, the three positive differences `x-t0`, `y-x`,
and `y-t0` all lie outside `T`, so additivity gives

```
P(y) - P(x) = h[y-x].
```

The same identity holds directly when `x=t0`. Its right-hand side is
nonzero with magnitude at most `m`. Thus `P` maps `T` injectively into
the integers, with image diameter at most `m`. Such an image has at most
`m+1` elements. This proves the lemma, including the singleton case.

In particular, a height-160 construction can put at most 161 positions
in its additional colour class. This restriction is specific to the
additive pullback mechanism; arbitrary Schur colourings need not satisfy it.

A tempting stronger statement, that each absolute nonzero label occurs
at most twice, is false. The valid height-three word

```
1, 0, -2, -1, 0, 0, -3, -2, -1
```

has three occurrences of absolute label 1. Its zero class is `{2,5,6}`.
Neither search implementation uses that false statement, the zero-class
bound, or any conjectural cardinality restriction on the complement.

## Exact search and completeness

Each variable initially has domain `{0,-m,...,-1,1,...,m}`. The only
symmetry reduction makes the first nonzero value selected by the search
positive. Before this choice all fixed values are zero and all nonzero
domains are invariant under simultaneous negation, so every solution has
a represented sign choice.

For a triple with three distinct positions, two fixed zero labels remove
zero from the third domain. Two fixed nonzero labels restrict the third
domain to zero or the uniquely determined sum/difference, if that value
is nonzero and lies in `[-m,m]`. A fixed zero and a fixed nonzero impose
no restriction on the third label. Fully assigned triples are checked
against the definition.

For a doubling equation `x+x=z`, fixing either variable similarly gives
the exact allowed domain for the other: two zero labels are forbidden;
when both are nonzero one must have `2*h[x]=h[z]`. In particular, a
nonzero odd label at `z` forces the label at `x` to be zero.

Every new singleton domain is propagated through all incident triples,
including future positions, until no further singleton is produced or a
domain is empty. These restrictions are necessary consequences of the
original equations. On reaching a fixed point, the search branches on
**every** remaining value of the first unassigned position. Induction
therefore shows that a completed unsuccessful search excludes all words
in the defined class. A node-cap exit instead returns `UNKNOWN`.

[`propagate.cpp`](propagate.cpp) stores domains as an optional zero and
either all nonzero values, one nonzero value, or none. This representation
is closed under the stated propagation rules. It treats doubling separately
and generates triples in `x`-first order.

[`audit.cpp`](audit.cpp) is a separate implementation using literal bit
domains. It generates triples in `z`-first order and combines repeated
variables into integer equation rows with coefficients `(2,-1)` or
`(1,1,-1)`. Its propagation rule uses the row sum and divisibility by the
missing variable's coefficient. The two programs share the mathematical
search strategy, but not the domain representation or arithmetic code.
This is an implementation audit within one research lane, not peer review
or formal verification.

## Completed computations and unresolved target

Both implementations complete the height-80 search at `N=242` with
196,119 visited nodes, 542,375 branch attempts and 346,257 rejected
extensions. The search cap is 300,000 nodes. The standard word

```
1,2,...,m,  [m+1 zeros],  -m,-m+1,...,-1
```

is valid through `3m+1`: sums internal to a nonzero block or crossing the
two nonzero blocks satisfy the required equation, and the middle zero
interval is sum-free. Hence the largest endpoint for **this mechanism
at height 80** is exactly 241.

The independent complete-word audit checks all 626,628 assignments in
20 small `(N,m)` cases. For every valid word it also checks the zero-class
potential used in the lemma. Both searches find literally valid words at
`N=3m+1` for `m=1,...,40`, and both exclude `N=3m+2` for `m=1,...,20`.
The height-160 standard word of length 481 and the nine-position
counterexample above are checked directly.

At `N=537,m=160`, the first implementation returns `UNKNOWN` after
5,000,001 visited nodes (the stopping visit is included), 10,037,478 branch
attempts and 5,037,478 rejected extensions. The cap is 5,000,000 nodes.
This is a reproducible bounded experiment, **not an exclusion certificate**.
The separate target run was stopped after this unresolved result; it is
not reported as an independent target decision. `expected.json` records
completed results and the capped observation separately.

## Reproduction and trust boundary

Requirements: Python 3.11+ standard library and a C++17 compiler. Tested
with Python 3.11.2 and GCC 12.2.0. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B verify.py
```

The verifier compiles both programs into a temporary directory, checks
the complete-word controls and positive witnesses literally, and reruns
both complete height-80 searches. To repeat the unresolved target pilot:

```sh
python3 -B verify.py --target
```

The original target pilot took about four minutes on the research host;
timings vary. The completed searches use direct exhaustive computation,
with the compiler, runtime and source code as the trust boundary. There
is no SAT solver, external input, DRAT trace, or formal proof assistant.
No large search tree, executable or runtime log is committed.

## Context

The [two-value parameterization](../schur_complement_additive_maps/README.md)
describes additive maps after a fixed sum-free deletion. The present search
does not assume that parameterization; it chooses the deletion as well.
For the intended Schur-six construction, height 160 is motivated by
[Heule's determination of `S(5)=160`](https://arxiv.org/abs/1711.08076).
The [2026 shifted-template paper](https://arxiv.org/abs/2607.15034) still
uses the published classical lower bound `S(6)>=536`. None of the results
here improves that bound. Exact historical priority for the elementary
zero-class lemma is not asserted.
