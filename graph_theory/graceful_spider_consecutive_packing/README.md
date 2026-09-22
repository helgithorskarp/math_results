# Consecutive-multiplier packing for graceful spiders

This directory gives an explicit quantitative refinement of the
self-matched-leg construction of Dumitru and Nacu.

For a spider whose nontrivial arm lengths are fixed, choose one arm of
length `c` for their zero-containing closure template and write the other
lengths in decreasing order as

```text
L_1 >= ... >= L_r >= 2,       L = L_1.
```

Put

```text
P_c = 0                         if c=2 or 3,
      2^(c-4)                   if c>=4,

Q = max(1, P_c, (L-1)r-L+1),
q_i = Q+i.
```

The multiplicative self-matched legs with parameters `q_1,...,q_r` are
pairwise label-disjoint.  Thus, if

```text
S = c + sum_i L_i,
M_c = 2 (c=2), 3 (c=3), or 2^(c-4)+3 (c>=4),
T = max(0, M_c-S, 3 + max_i(L_i q_i)-S),
```

then every spider

```text
S(c,L_1,...,L_r,1^t),          t >= T,
```

is graceful, with hub label `1`.

The key point is structural: the multipliers occupy one short integer
interval, rather than exponentially separated scales.  Choosing a shortest
nontrivial arm as the closure arm gives a sufficient total edge count

```text
O(L 2^d + L^2 k),
```

where `d` and `L` are the shortest and longest nontrivial arm lengths and
`k` is their number.  In particular, the leaf threshold is polynomial in
`L` and `k` whenever `d` is bounded.  This refines one particular packing
mechanism; it does not claim an optimal leaf threshold or settle arbitrary
spiders.

[`THEOREM.md`](THEOREM.md) contains the proof and
[`SOURCES.md`](SOURCES.md) states the literature boundary.  Run the exact,
standard-library audit with Python 3.11 or later:

```sh
./run_checks.sh
```

The audit reconstructs and definition-checks 11,574 parameter profiles,
checks the threshold boundary and exchange rule, and includes rejection
controls.  The universal result rests on the written proof, not on the finite
audit.
