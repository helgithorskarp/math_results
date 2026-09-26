# A cubic algorithm for stacking on a cycle

## Theorem

Let `c=(c_0,...,c_(n-1))` be a configuration of nonnegative integers on the
undirected cycle `C_n`, `n>=3`. A pebbling move removes two pebbles from a
vertex and places one on a neighbor. A configuration is stackable if it can
reach a configuration of support size one; the zero configuration is not
stackable.

Stackability can be decided in **O(n^3) exact integer operations**, independently
of the numerical sizes of the piles. The integers used have O(n+L) bits, where
`L=max(1,max_i bit_length(c_i))`. The algorithm uses O(n^2) integer storage and
returns a four-integer split-path witness in the positive case.

More precisely, it computes the maximum signed root score over all allocations
at each of the `n(n+1)` cut/target pairs. This is a maximum over split paths;
we make no assertion about maximum attainable final mass on the cycle, or
stacking at a prescribed original cycle vertex.

The theorem is conditional only on two established graph lemmas stated below:
the exact tree-transfer criterion and the exact cycle split-path criterion.
The new proof gives the residue decomposition, linear profile bound,
constant-candidate optimization, and cubic assembly. Those two imported lemmas
have separate proofs and independently accepted graph reviews.

## 1. Imported criteria and endpoint convention

For a nonempty tree branch with effective root pile `z`, its maximal signed
transfer to its parent is

```
g(z) = 2z-3                if z<=1,
       z/2                if z>=2 is even,
       (z-3)/2            if z>=3 is odd.
```

An entirely empty branch instead has transfer zero. On a path, propagate these
messages from both ends. The target root score is its own pile plus the two
incoming messages. A configuration stacks at that path target exactly when
this score is at least one.

For a cycle vertex `s` of pile `C`, replace `s` by the two endpoints of the
path

```
s_left, s+1, ..., s-1, s_right,
```

with all indices interpreted modulo `n`. Put `x` at the left endpoint and
`C-x` at the right. The cycle configuration is stackable exactly when some
`0<=x<=C`, some cut `s`, and some target position `p` in `{0,...,n}` give a
positive path root score.

For each cut we evaluate `x=0` and `x=C` directly, with the empty-branch rule.
Every remaining allocation satisfies `1<=x<=C-1`; both variable endpoints
are occupied, so every branch starting there remains a nonempty branch even
when an effective signed message is zero or negative. This distinction is
necessary: substituting zero into the occupied formula would give `g(0)=-3`
where an entirely empty branch has transfer zero.

References for these criteria:

- [Tree-transfer theorem](../../tree_stacking_transfer_theorem/README.md).
- [Cycle split-path theorem](../cycle_stacking_split_transfer/README.md).
- [Independent split-path review](../cycle_stacking_split_transfer_review1/REVIEW.md).

## 2. Fixing a residue makes transfer monotone

Suppose a branch message is `3q+rho`, where `rho` belongs to `{0,1,2}`, and
we add a fixed nonnegative pile `c`. Write

```
rho+c = 3h+sigma,     0<=sigma<=2,     w=q+h.
```

The effective pile is `3w+sigma`. Its outgoing residue is
`rho'=(-sigma) mod 3`, independent of `q`. Its outgoing quotient is

```
q' = 2w+ell_sigma                    if w<=K_sigma,
     floor((w+eta_sigma)/2)          otherwise,
```

where

| sigma | rho' | K_sigma | ell_sigma | eta_sigma |
|---|---:|---:|---:|---:|
| 0 | 0 | 0 | -1 | 0 |
| 1 | 2 | 0 | -1 | -1 |
| 2 | 1 | -1 | 0 | 0 |

These identities follow by substituting `3w+sigma` into `g`. For the upper
branch, one can equivalently take the largest integer of the required residue
not exceeding `(3w+sigma)/2`.

Each quotient map is nondecreasing on the integers. This holds within both
branches; at their junctions the consecutive values are respectively
`-1,0`, `-1,0`, and `-2,0`. Consequently a branch whose initial pile is
`x=3t+r` has a quotient that is nondecreasing in `t` at every depth. Its
residue at each depth depends only on `r` and the fixed piles.

The unconditioned map `g` itself is not monotone: `g(2)=1>g(3)=0`.
The residue restriction is essential.

## 3. At most d+1 branch pieces

Fix the source residue `r` and an integer interval `lo<=t<=hi` on which
`3t+r` is positive. At depth zero the quotient is `q(t)=t`. We represent
its successive values on integer intervals by

```
q(t) = a floor((t+b)/P) + D,                        (1)
```

where `a` and `P` are positive powers of two and `b,D` are arbitrary integers.
The initial representation has `a=P=1` and `b=D=0`.

For one step with constants `h,sigma` from Section 2, the lower branch is
chosen exactly when `q(t)+h<=K_sigma`. On a piece (1), this is equivalent to

```
t <= P (floor((K_sigma-h-D)/a)+1) - b - 1.          (2)
```

Thus the interval can be split by an explicit integer boundary, with no scan
and no binary search.

The lower update preserves (1), with

```
a' = 2a,    P'=P,    b'=b,    D'=2(D+h)+ell_sigma.
```

For the upper update there are two cases. If `a>=2`, then

```
a'=a/2,    P'=P,    b'=b,    D'=floor((D+h+eta_sigma)/2).
```

If `a=1`, the nested-floor identity gives

```
a'=1,    P'=2P,    b'=b+P(D+h+eta_sigma),    D'=0.
```

The identity used here is valid for all integers, including negative offsets:

```
floor((floor((t+b)/P)+K)/2) = floor((t+b+PK)/(2P)).
```

It remains to bound the number of pieces. The quotient before each step is
globally nondecreasing, by Section 2. Hence the set where
`q(t)+h<=K_sigma` is an initial interval of the entire domain, not a separate
arbitrary set in each old piece. A step adds at most one breakpoint to the
old partition. Induction therefore gives **at most d+1 pieces at depth d**.
This argument also proves the ordered, gap-free partition invariant used by
the implementation. Existing adjacent pieces need not be merged.

Building all profiles at depths `0,...,n` costs O(n^2) integer operations
and storage, since the update of a depth-d profile processes at most d+1
pieces.

## 4. Four candidates for two opposing dyadic floors

Consider on an integer interval `[l,u]` the function

```
H(t) = a floor((t+b)/P) + d floor((T-t+e)/Q) + K,   (3)
```

where `a,d` are positive and `P,Q` are powers of two. Its maximum is attained
among at most four points:

- the two interval endpoints;
- if `P<=Q`, the first and last points of `[l,u]` congruent to `T+e` modulo Q;
- if `P>Q`, the first and last points congruent to `-b` modulo P.

An absent congruence class contributes no points, and coincident candidates
are counted once.

For `P<=Q`, partition the integers into bands on which the second floor is
constant. Within a band the first term is nondecreasing, so its rightmost
point maximizes (3). The complete-band right endpoints are exactly
`t congruent T+e modulo Q`. At successive such endpoints, (3) changes by
the constant `aQ/P-d`, because `P` divides `Q`. Thus their first or last
representative is optimal, and the right endpoint of the whole interval
handles its final truncated band. The included left endpoint is harmless.

For `P>Q`, use bands on which the first floor is constant. The other term is
nonincreasing, so take band left endpoints, congruent to `-b` modulo P.
Successive values differ by the constant `a-dP/Q`. The first/last
representatives and the interval endpoints again suffice.

This proves the optimization exactly even when the interval, coefficients,
or offsets have arbitrarily large magnitude. It does not inspect all
residues modulo a dyadic period.

## 5. Assemble all cut-target maxima

Fix a cut of mass C, and a residue `r` for the left endpoint. Write

```
x=3t+r,       C-r=3T+s,       C-x=3(T-t)+s.
```

Restrict to the exact interior domain

```
max(0,ceil((1-r)/3)) <= t <= floor((C-1-r)/3).       (4)
```

Skip it if empty. Build clockwise profiles from residue r on (4), and
counterclockwise profiles from residue s on the reflected domain in `T-t`.
The first addition on either branch is zero, representing its variable leaf;
subsequent additions are the fixed interior piles.

For a target at path position p, use the clockwise profile of depth p and
the counterclockwise profile of depth `n-p`. There are at most `p+1` and
`n-p+1` pieces, respectively. Reflect the second interval partition and
merge the two ordered partitions. Their common refinement has at most
`n+1` intervals and is obtained in linear time.

On each common interval, the target root score is a fixed constant plus
three times an expression (3). Its maximum therefore requires at most four
candidate evaluations. At an endpoint target use the depth-zero identity
profile, and do not add a separate target pile. At an interior target add
its unchanged pile. This proves the computed maximum is exact at every
cut-target pair.

There are three source residues, n cuts, and n+1 targets. Reusing all depth
profiles for a given cut and residue gives the claimed cubic cost. Explicit
bounds on stored/processed data over the entire run are

```
profile pieces over all depths:   <= 3n(n+1)(n+2),
common-refinement intervals:      <= 3n(n+1)^2,
interior candidate evaluations:   <= 12n(n+1)^2,
endpoint root-score evaluations:  <= 2n(n+1).
```

The two directional profile tables and the result table each require O(n^2)
storage. The largest powers `a,P` used in a depth-n profile are at most
`2^n`. Offsets are obtained by at most n additions, doublings, halvings and
multiplications by these powers. For example their magnitudes are bounded
by `O(n^2 (max_i c_i+1) 4^n)`, which suffices for O(n+L) bits. Interval
boundaries and candidate evaluations obey the same type of bound. All
operations are therefore polynomial in the binary input length as well.

Finally take the largest of the exact maxima. It is positive precisely when
the imported split-path criterion holds. A positive allocation, cut, target
and score give the promised witness. No positive witness exists in the
zero-configuration case, where the endpoint scores are zero.

## Scope

This is an exact per-configuration decision theorem for every cycle length,
including even cycles and zero piles. It replaces the previous
O(n^3 2^n) transfer-operation bound from dyadic split compression by a cubic
bound. It does not determine the universal threshold `stack(C_n)`, establish
the Almost Stacked Hypothesis, or prove the conjecture
`stack(C_(2k+1))=5*2^(k-1)-3`.
