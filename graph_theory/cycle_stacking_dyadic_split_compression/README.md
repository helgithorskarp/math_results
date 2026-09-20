# Dyadic compression of the exact cycle split search

## Result

The split-path theorem reduces stackability of a nonnegative integer
configuration `c` on the undirected cycle `C_n` to the following finite
search.  Cut one vertex `s` into the endpoints of a path, write its pile as

```text
c(s) = x + (c(s)-x),
```

and test every target of that path by the exact signed-transfer rule.  The
literal search in the preceding implementation tests `c(s)+1` allocations at
cut `s`, so its running time is pseudo-polynomial in a binary-encoded pile.

This directory proves that the allocation scan can be compressed to a number
of tests depending only on `n`.

**Dyadic split-compression theorem.**  Fix a cut pile of size `C` and a target
in the opened path.  Let `p` and `q` be the distances from the two split
endpoints to the target, so `p+q=n`.  Put

```text
U_0 = 0,
U_d = 2^(d+1)-2              (d >= 1),
P   = 2^max(p,q).
```

It is enough to test:

1. every `x` for which `x < U_p` or `C-x < U_q`; and
2. one extremal representative of every residue class modulo `P` in the
   central interval `U_p <= x <= C-U_q`.

The number of tested allocations for this cut-target pair is at most

```text
U_p + U_q + 2^max(p,q) <= 3*2^n-2,
```

independently of `C` and of the total mass.  Searching all cuts and targets
therefore decides cycle stackability using fewer than
`3*n*(n+1)*2^n` target tests, or `O(n^3 2^n)` signed-transfer operations with
the direct implementation.  Integer bit complexity is polynomial in the bit
length of the piles for fixed `n`.

Thus the exact cycle test is fixed-parameter tractable in the cycle order and
is no longer pseudo-polynomial in the mass.  A positive certificate remains
the same four integers `(cut, split, target, root_score)`.  A negative answer
is exact by this theorem together with the split-path theorem.

## Signed transfer and the dyadic law

For a nonempty path branch, its outgoing signed message is obtained by adding
the incoming message to the next pile and applying

```text
g(z) = 2z-3                         if z <= 1,
       z/2                          if z >= 2 is even,
       (z-3)/2                      if z >= 3 is odd.
```

An entirely empty branch has message zero.  If `F_d(x)` is the message of a
fixed branch of depth `d` whose leaf pile is the variable `x`, then

```text
F_d(x+2^d) = F_d(x)+1               for every x >= U_d.       (1)
```

Here all other branch piles are arbitrary fixed nonnegative integers.

To prove (1), first note that

```text
g(z+2r) = g(z)+r                    (z >= 2, r >= 0).          (2)
```

Also `U_1=2`, and `U_d=2U_(d-1)+2`.  For every integer `z >= 2A+2`, the two
positive-parity cases in the definition of `g` give `g(z) >= A`.  Therefore,
starting with `x >= U_d`, every effective value along the branch is at least
two, even if all fixed piles are zero.  The increment `2^d` is successively
halved by (2), becoming `2^(d-1),...,1`; this proves (1).  For depth zero use
`F_0(x)=x`, which obeys the analogous shift law with period one.

## Proof of the compression theorem

For the fixed cut and target, orient both branches from their split endpoint
toward the target.  There are fixed branch-message functions `F_p` and `G_q`
such that the target score is

```text
S(x) = b + F_p(x) + G_q(C-x),                              (3)
```

where `b` is the unchanged target pile.  At an endpoint target, its allocated
pile is represented by the depth-zero function, so (3) still applies.

Every allocation outside the central interval is explicitly retained.  In
the central interval both (1) laws apply.  If `x` and `x+P` lie there, repeated
use of (1) gives

```text
S(x+P)-S(x) = P/2^p - P/2^q.                              (4)
```

This difference is constant.  Consequently, within each residue class
modulo `P`, the scores form an arithmetic progression.  Its maximum is at the
last representative if the right side of (4) is positive, and at the first
representative if it is negative; if it is zero, either representative works.
Keeping that single extremal allocation preserves the global maximum of
`S(x)`.  The two fringes contain at most `U_p+U_q` allocations and the central
set contains at most `P` representatives, proving both completeness and the
count.

For an endpoint target, the displayed estimate is exactly `3*2^n-2`.  If both
depths are positive, their maximum is at most `n-1`, and the estimate is at
most `5*2^(n-1)-4 < 3*2^n-2`.  This proves the uniform bound.  Combining the
targetwise result with the exact split-path characterization proves the
algorithmic corollary.

## Reproduction

The implementation and verifier use only Python's standard library:

```bash
python3 verify_dyadic_compression.py --check-expected
```

The verifier checks the branch shift law 6,000 times through depth 12, compares
the compressed and literal target maxima in 6,400 deterministic cases, and
compares complete compressed and literal cycle decisions on 9,802
configurations through orders 3--7.  It also exercises 1,500 cases with
100-digit cut piles and checks malformed inputs.  The exhaustive decision
digest and exact counts are recorded in `EXPECTED.json`.  These checks audit
the implementation; the universal theorem follows from (1)--(4), not from a
finite cutoff.

## Context and limitations

The stacking parameter and pebbling convention are due to Tamás Csernák and
Lajos Soukup, *Stacking and clearing in graph pebbling*, arXiv:2604.22341v1:
<https://arxiv.org/abs/2604.22341>.  The exact split-path characterization and
its proof are published in
[`cycle_stacking_split_transfer`](../cycle_stacking_split_transfer/).  The
tree signed-transfer theorem used there is published in
[`tree_stacking_transfer_theorem`](../../tree_stacking_transfer_theorem/).

The primary paper still reports no formula for odd-cycle stacking.  This
compression does not prove the conjectured odd-cycle upper bound; it removes
the dependence on the numerical mass from exact split testing and isolates
the dyadic boundary signature that a future extremal argument must control.
Targeted searches of the current arXiv record, Discovery Net, and exact
split/dyadic phrasing on 20 September 2026 found no prior statement of this
compression.  Apparent novelty is limited to those sources; no global
priority claim is made.
