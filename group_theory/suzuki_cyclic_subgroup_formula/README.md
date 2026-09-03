# Cyclic subgroups of Suzuki groups and the solvability threshold

## Result

For a finite group `G`, write `cyc(G)` for its number of cyclic subgroups,
including the trivial subgroup, and write `omega(n)` for the number of
distinct prime divisors of `n`.

Let

```text
q = 2^e,  e >= 3 odd,  r = sqrt(2q),  S = Sz(q),
t_plus = q+r+1,  t_minus = q-r+1,
```

and let `tau(n)` be the number of positive divisors of `n`.

**Exact formula.** The simple Suzuki group `S` has

```text
cyc(S) = 1
  + (q^2+1)(q-1)(q+2)/2
  + q^2(q^2+1)(tau(q-1)-1)/2
  + q^2(q-1)t_minus(tau(t_plus)-1)/4
  + q^2(q-1)t_plus(tau(t_minus)-1)/4.              (1)
```

**Almost-simple threshold theorem.** If

```text
S <= G <= Aut(S),
```

then

```text
cyc(G) >= 2^(omega(|G|)+2),
```

and the inequality is strict. Thus the cyclic-subgroup solvability
conjecture of Das, Dey, and Sharma holds for every almost-simple group with
Suzuki socle.

The proofs are structural and computation-free. The companion Python
program audits the exact arithmetic and all intermediate almost-simple
indices over a configurable finite range.

## Suzuki partition and the exact formula

The standard Suzuki subgroup partition gives:

- `q^2+1` Sylow 2-subgroups `Q`, each of order `q^2` and exponent 4;
- cyclic maximal tori `A_0`, `A_plus`, and `A_minus` of respective orders
  `q-1`, `t_plus`, and `t_minus`;
- trivial intersection between distinct partition members; and
- normalizers of orders `2(q-1)`, `4t_plus`, and `4t_minus` for the three
  torus types.

Since

```text
|S| = q^2(q-1)(q^2+1)
    = q^2(q-1)t_plus t_minus,
```

the numbers of conjugates of the three tori are

```text
n_0     = q^2(q^2+1)/2,
n_plus  = q^2(q-1)t_minus/4,
n_minus = q^2(q-1)t_plus/4.                         (2)
```

Each cyclic torus of order `a` has `tau(a)-1` nontrivial cyclic subgroups.
The partition makes all of these subgroups distinct between different
conjugates and different torus types.

Each `Q` contains `q-1` involutions and `q^2-q` elements of order 4. It
therefore contains

```text
(q-1) + (q^2-q)/2
```

nontrivial cyclic subgroups. Distinct Sylow 2-subgroups in the partition
intersect trivially. Adding the identity subgroup and substituting (2)
gives (1).

## The `q^4` torus identity

Taking just each full torus once in (2) gives exactly

```text
n_0 + n_plus + n_minus
  = q^2(q^2+1)/2 + q^2(q-1)(t_plus+t_minus)/4
  = q^2(q^2+1)/2 + q^2(q^2-1)/2
  = q^4.                                             (3)
```

Consequently every overgroup `G` of `S` satisfies

```text
cyc(G) >= cyc(S) >= q^4+1.                           (4)
```

## Comparison with the conjectured threshold

The outer automorphism group of `S` is cyclic of order `e`. Hence, for an
almost-simple group `G` with socle `S`,

```text
d = [G:S] divides e.
```

Put

```text
M = (q-1)(q^2+1),  s = omega(M),  u = omega(e).
```

The odd primes dividing `M` are at least 3, so

```text
2^s <= 3^s <= rad(M) <= M.
```

Also `2^u <= rad(e) <= e`. Therefore

```text
2^(omega(|G|)+2) <= 8 * 2^s * 2^u <= 8eM.           (5)
```

For odd `e >= 7`, one has `q=2^e >= 8e`: it holds at `e=7`, and increasing
`e` by two multiplies the left side by 4 while multiplying `e` by less than
4. Since `M<q^3`, equations (4)--(5) give

```text
q^4 >= 8e q^3 > 8eM >= 2^(omega(|G|)+2).
```

The two remaining exponents are immediate and retain a very large strict
margin:

```text
e=3: M=5*7*13 and d|3, so omega(|G|)<=5 and 2^(omega(|G|)+2)<=128<8^4+1.
e=5: M=5^2*31*41 and d|5, so omega(|G|)=4 and 2^(omega(|G|)+2)=64<32^4+1.
```

This proves the almost-simple threshold theorem.

## Literature scope

Downs and Jones record the Suzuki order, Sylow-2 structure, odd maximal
cyclic subgroups, torus normalizers, disjointness, and the full automorphism
group used above. Alavi, Daneshkhah, and Mosaed give the same partition and
element-order counts in a form that independently cross-checks formula (1).
Das and Sharma use a divisor-count lower bound to show only `cyc(Sz(2^p))>32`
in a restricted minimal-simple argument. The source conjecture, general
cyclic-subgroup-count literature, and targeted title/abstract/formula searches
revealed no exact formula (1), `q^4` identity (3), or parameter-dependent
threshold theorem for Suzuki groups. This is an apparent-novelty statement
relative to the searched sources, not a historical-priority claim.

## Reproduction

Requirements: CPython 3.11 or later; no third-party packages.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_arithmetic.py --max-exponent 19
```

Expected output:

```text
e q exact_cyc torus_lower_bound max_almost_simple_threshold
3 8 6372 4097 128
5 32 1914128 1048577 64
7 128 521257024 268435457 256
9 512 240585146624 68719476737 1024
11 2048 53055596790784 17592186044417 512
13 8192 11259273845673984 4503599627370497 512
15 32768 8074971586622406656 1152921504606846977 4096
17 131072 737870888822519169024 295147905179352825857 512
19 524288 226895023741459302187008 75557863725914323419137 512
checked_exponents=9
VERIFIED
```

The program factors exact integers by trial division, checks the partition's
element total, derives the cyclic-subgroup count independently from the four
partition types, verifies the `q^4` identity, and checks every possible index
`d|e` in the displayed range. It is an audit, not a dependency of the
universal proof.

## References

- M. Downs and G. A. Jones, *Enumerating Regular Objects associated with
  Suzuki Groups*, arXiv:1309.5215 (2013):
  https://arxiv.org/abs/1309.5215
- S. H. Alavi, A. Daneshkhah, and H. P. Mosaed, *Finite groups of the same
  type as Suzuki groups*, arXiv:1606.00041 (2016):
  https://arxiv.org/abs/1606.00041
- A. Das, H. K. Dey, and K. Sharma, *Group Structure via Subgroup Counts*,
  Conjecture 5.5, arXiv:2604.08040 (2026):
  https://arxiv.org/abs/2604.08040
- A. Das and K. Sharma, *Solvability of Groups via Cyclic Subgroup Count*,
  arXiv:2604.23664 (2026):
  https://arxiv.org/abs/2604.23664

## Trust boundary

The theorem trusts the standard Suzuki subgroup partition and automorphism
theorem recorded in the cited primary sources, plus orbit-stabilizer and
elementary integer inequalities. It uses no solver, exhaustive group
enumeration, floating point, randomized search, or generated certificate.
The audit additionally trusts CPython exact integer operations and its short
trial-division factorization routine.
