# A cyclic-subgroup lower bound for `PSL(2,q)`

## Result

For a finite group `G`, write `cyc(G)` for the number of cyclic subgroups of
`G`, including the trivial subgroup, and write `omega(n)` for the number of
distinct prime divisors of `n`.

**Theorem.** Let `q >= 4` be a prime power, let

```text
G = PSL(2,q),
t = omega(|G|).
```

Then

```text
cyc(G) >= 2^(t+2).
```

Consequently, the cyclic-subgroup solvability conjecture of Das, Dey, and
Sharma holds for every finite simple group `PSL(2,q)`: none of these groups can
satisfy `cyc(G) < 2^(omega(|G|)+2)`.

The cases `q=4,5` attain equality because
`PSL(2,4) ~= PSL(2,5) ~= A_5` and `cyc(A_5)=32`.

## Proof

Put `d = gcd(2,q-1)`. The two standard conjugacy classes of maximal tori in
`PSL(2,q)` are cyclic, of orders

```text
(q-1)/d   and   (q+1)/d.
```

The normalizer of either torus has twice its order. Since

```text
|PSL(2,q)| = q(q^2-1)/d,
```

the numbers of their conjugates are respectively

```text
q(q+1)/2   and   q(q-1)/2.
```

These are `q^2` distinct nontrivial cyclic subgroups. (Equivalently, split
tori correspond to unordered pairs of distinct points of `P^1(F_q)`, and
nonsplit tori correspond to Frobenius-conjugate unordered pairs in
`P^1(F_(q^2)) \ P^1(F_q)`.) Thus, after also counting the trivial subgroup,

```text
cyc(PSL(2,q)) >= q^2+1.                            (1)
```

This standard torus count is also the starting point of the exact cyclic
subgroup decomposition of `PSL(2,q)`; only the lower bound (1) is needed here.

It remains to compare `q^2+1` with `2^(t+2)`.

### Odd `q`

Write

```text
a = omega(q-1),   b = omega(q+1).
```

The characteristic prime dividing `q` divides neither neighbor. The prime `2`
is counted in both `a` and `b`, and division by `2` in the order formula does
not remove it because one of `q-1,q+1` is divisible by `4`. Hence

```text
t = a+b.                                           (2)
```

An even integer with `r` distinct prime divisors is at least
`2*3^(r-1)`. Therefore

```text
q^2-1 = (q-1)(q+1) >= 4*3^(t-2).                  (3)
```

If `t >= 6`, then `3^(t-2) >= 2^t` (check `t=6`, after which the
left-to-right ratio grows by `3/2`). Equations (1) and (3) give

```text
cyc(G) >= q^2+1 >= 4*2^t = 2^(t+2).
```

If `t <= 5` and `q >= 13`, then

```text
q^2+1 >= 170 > 128 >= 2^(t+2).
```

The remaining odd prime powers are `q=5,7,9,11`. For `q=7,9,11`, the pairs
`(t,q^2+1)` are `(3,50)`, `(3,82)`, and `(4,122)`, respectively, so (1)
suffices. The case `q=5` is handled below.

### Even `q`

Now `q=2^f`. With the same definitions of `a,b`, the integers `q-1` and
`q+1` are odd and coprime, so

```text
t = 1+a+b.                                         (4)
```

An odd integer with `r` distinct prime divisors is at least `3^r`. Hence

```text
q^2-1 >= 3^(t-1).                                  (5)
```

If `t >= 7`, then `3^(t-1) >= 2^(t+2)` (check `t=7`, then multiply the
ratio by `3/2`). Equations (1) and (5) prove the result. If `t <= 6` and
`q >= 16`, then

```text
q^2+1 >= 257 > 256 >= 2^(t+2).
```

The only remaining even prime powers are `q=4,8`. For `q=8`, `t=3` and
`q^2+1=65>32`, so (1) again suffices.

### The two exceptional torus comparisons

For `q=4,5`, the torus lower bounds `17` and `26` do not by themselves reach
the target. Both groups are isomorphic to `A_5`. Its elements consist of the
identity, 15 elements of order 2, 20 elements of order 3, and 24 elements of
order 5. Thus

```text
cyc(A_5) = 1 + 15 + 20/phi(3) + 24/phi(5)
         = 1 + 15 + 10 + 6
         = 32.
```

In both cases `t=3`, so `32=2^(t+2)`. This completes the proof.

## Relation to the open conjecture

Das, Dey, and Sharma conjecture that every finite group `H` satisfying

```text
cyc(H) < 2^(omega(|H|)+2)
```

is solvable. The theorem proves the contrapositive for the infinite simple
family `PSL(2,q)`. It does not settle other simple groups, almost-simple
extensions of `PSL(2,q)`, or arbitrary nonsolvable groups.

The maximal-torus structure and counts are classical. The contribution here is
the elementary uniform comparison with the conjectured sharp threshold. A
targeted search through 2026-09-02 found the conjecture and the classical torus
count, but no prior source making this comparison; this is a search-relative
novelty statement, not a claim of historical priority.

## Reproduction

The proof is computation-free. `verify_arithmetic.py` is a finite falsification
check of the prime-divisor identities and inequalities, not part of the proof.
It uses only the Python standard library.

```bash
python3 verify_arithmetic.py
```

Expected summary:

```text
prime_power_limit=1000000
prime_powers_checked=78732
smallest_q_ge_7_margin=18 at_q=7
exceptional_q=4,5 exact_cyc=32 threshold=32
```

## References

- A. Das, H. K. Dey, and K. Sharma, *Group Structure via Subgroup Counts*,
  arXiv:2604.08040 (2026), especially Conjecture 5.5:
  https://arxiv.org/abs/2604.08040
- A. V. Zavarnitsine, *On the maximal tori in finite linear and unitary
  groups*, arXiv:1902.09083 (2019):
  https://arxiv.org/abs/1902.09083
- T. Breuer, *Computations with the GAP Character Table Library*, Section 4.6,
  recording the two `PSL(2,q)` cyclic torus classes and their `q^2` total:
  https://www.math.rwth-aachen.de/~Thomas.Breuer/ctbllib/doc2/chap4_mj.html

## Trust boundary

The theorem uses ordinary finite-group facts about the order and maximal tori
of `PSL(2,q)`, elementary prime-divisor counting, and the standard
isomorphisms `PSL(2,4) ~= PSL(2,5) ~= A_5`. It uses no solver, floating-point
arithmetic, exhaustive classification, or unarchived certificate. The audit
script additionally trusts CPython integer arithmetic and its own elementary
sieve and factorization routines, but its output is not used to prove the
universal statement.
