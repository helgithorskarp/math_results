# Exact cycle stackability by one split-path boundary

## Result

Let `c` be a nonnegative integer configuration on the undirected cycle
`C_n`, `n >= 3`.  Choose a vertex `s`, replace it by two leaves `s^-` and
`s^+`, and thereby open the cycle into the path

```text
s^- , s+1 , s+2 , ... , s-1 , s^+ .
```

For `0 <= a <= c(s)`, let `c[s,a]` put `a` pebbles at `s^-`, put
`c(s)-a` pebbles at `s^+`, and leave all other piles unchanged.

**Split-path theorem.**  The configuration `c` is stackable on `C_n` if and
only if `c[s,a]` is stackable on the opened path for at least one pair
`(s,a)`.

Together with the exact signed transfer theorem for trees, this gives a
direct boundary-signature test for cycle stackability.  It replaces the
move-DAG reachability census by at most

```text
sum_s (c(s)+1) = |c| + n
```

linear-time path tests.  Thus a configuration of mass `M` is decided in
`O(n(M+n))` integer operations by the simple implementation here.  A positive
certificate consists only of a cut vertex, an endpoint split, a path target,
and its positive root score.  The theorem also makes failure of all split
tests an exact negative answer.

This is a structural reduction, not the still-open matching upper bound for
the conjectured odd-cycle formula.  In particular, proving

```text
stack(C_(2k+1)) <= 5*2^(k-1)-3
```

is now equivalent to proving that every configuration of that mass admits a
positive split-path signature.

## Transfer score on the opened path

For a nonempty oriented path branch, define

```text
g(t) = 2t-3                         if t <= 1,
       t/2                          if t >= 2 is even,
       (t-3)/2                      if t >= 3 is odd.
```

An empty branch has message zero.  Messages are propagated from each end of
the path.  The root score at a possible target is its initial pile plus the
two incoming messages.  The exact tree transfer theorem says that the lifted
configuration stacks at that target exactly when this score is at least one.
The file `cycle_split_transfer.py` implements these two sweeps and the split
search using arbitrary-precision Python integers.

## Empty-leaf lemma

The induction below needs one consequence of the transfer theorem.

**Lemma.**  Let `x` be a leaf of a tree `T`, and suppose `d(x)=0`.  If `d` is
stackable on `T`, then its restriction is stackable on `T-x`.

If a successful target is not `x`, the empty branch `x -> y` has message zero,
so the same root score is positive after deleting `x`.  If the successful
target is `x`, let `y` be its neighbor.  The positive score at `x` is the
message `g(q)` of the whole nonempty `y`-side, where `q` is the root score at
`y` after deleting `x`.  Since `g(q) >= 1` implies `q >= 1`, the restriction
stacks at `y`.  This proves the lemma.

## Proof of the split-path theorem

If a lifted configuration stacks on its path, identify the two path endpoints
back to `s`.  Every path move becomes a legal cycle move, and a path stack
maps to a cycle stack.  This proves one direction.

For the converse, induct on the length of a fixed cycle stacking sequence.
The zero-move case is already stacked and has an immediate split lift.  Let
the first move be `u -> v`, and write `c' = c-2e_u+e_v` for its child.  By
induction, some split lift of `c'`, with cut vertex `s`, is stackable.

There are three cases.

1. If `s` is neither `u` nor `v`, the edge `uv` occurs unchanged inside the
   opened path.  Replace one pebble at `v` by two at `u`; the first path move
   recovers the stackable lift of `c'`.
2. If `s=u`, the edge `uv` is incident with one copy of `u`.  Add the two
   restored pebbles to that endpoint and again perform the first move.
3. Suppose `s=v`, and let `v*` be the endpoint adjacent to `u`.  If the chosen
   split puts a pebble at `v*`, remove one there, restore two at `u`, and make
   the first move.  The only delicate case is that `v*` is empty.  Delete this
   empty leaf.  By the lemma, the restriction of `c'` stacks on the spanning
   path `C_n-uv`, whose endpoint is `u`.  Move the cut from `v` to `u`: put all
   of `c'(u)` on the endpoint belonging to that spanning path and zero on the
   new endpoint adjacent to `v`.  This is still a stackable lift of `c'`.
   For `c`, instead put two pebbles on the latter endpoint and replace
   `c'(v)` by `c'(v)-1`.  The move from that endpoint to `v` recovers the
   stackable lift.

In every case a stackable split lift of the parent `c` exists, completing the
induction.

## Why splitting is genuinely stronger than deleting an edge

An ordinary spanning-path shortcut fails even at known exact thresholds.
For example, every spanning path is non-stackable for

```text
C5: (0,1,1,0,6),
C7: (0,0,1,1,0,0,15).
```

Both cycle configurations are stackable.  Splitting the heavy last vertex
repairs them: the deterministic implementation finds splits `2+4` for the
first example and `4+11` for the second.  Thus the endpoint allocation, not
merely a choice of deleted edge, is the essential boundary state.

## Reproduction

The verifier uses only the Python standard library:

```bash
python3 verify_split_transfer.py --check-expected
```

It compares the split-message decision entry by entry with an independent
recursive oracle that follows every legal cycle move.  The exhaustive domain
is every positive-mass configuration through `(order,mass)` equal to

```text
(3,8), (4,10), (5,12), (6,12), (7,17).
```

It also compares every target score on paths of orders 1 through 7 and masses
0 through 10 with a direct move-DAG oracle, checks 16,000 deterministic
reverse-move instances on cycle orders 8 through 15, checks the two
strict-gain examples above, replays exact certificates, and rejects malformed
certificates.  The raw oracles do not use signed messages, cuts, or the theorem
under test.  Finite checks corroborate the universal proof; they are not its
basis.

A fresh run checked 372,017 cycle configurations and 31,823 path
configurations (204,204 target decisions) in 20.9 seconds of wall time.  Its
canonical entry-level digest was

```text
4114c5278bb5f8791703bf44a846274f0c86e8c19f5d0c4e94780a6356cbc259
```

Tested interpreter: CPython 3.11.2.  Exact expected output is stored in
`EXPECTED.json`; source hashes are in `SHA256SUMS`.

## Context and scope

The stacking parameter and pebbling convention are due to Tamás Csernák and
Lajos Soukup, *Stacking and clearing in graph pebbling*, arXiv:2604.22341v1:
<https://arxiv.org/abs/2604.22341>.  That paper reports the values through
`C_11` and states no formula for odd-cycle stacking.  The split reduction uses
the independently reviewed exact tree transfer theorem published at
<https://github.com/helgithorskarp/math_results/tree/main/tree_stacking_transfer_theorem>.

Targeted searches of the current arXiv record and exact split/cycle phrasing
on 20 September 2026 found no prior statement of this reduction.  The novelty
claim is limited to the inspected primary sources and Discovery Net; it is not
a global priority claim.  This result does not prove the conjectured odd-cycle
stacking number, nor does it make the pseudo-polynomial scan polynomial in the
binary encoding of the piles.
