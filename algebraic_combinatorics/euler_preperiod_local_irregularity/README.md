# Local irregularity obstruction for Euler preperiod drops

Let `A_n` be the Euler up/down numbers,

```text
sum_(n>=0) A_n z^n/n! = sec(z)+tan(z),
```

and let `s(p^r)` be their least preperiod modulo the odd prime power
`p^r`.  Güleç proved the exact criterion

```text
s(p^r) <= r-k  iff  p^j divides A_(r-j) for 1 <= j <= k.
```

Consequently, a failure of the conjectured lower bound
`s(p^r) >= r-2` forces three consecutive Euler up/down numbers to vanish
modulo `p`.  The theorem in [THEOREM.md](THEOREM.md) classifies exactly where
such a modular triple can occur.

## Result

For `p >= 5`, put

```text
E_p = {even j: 2 <= j <= p-3 and p | A_j},
B_p = {even j: 2 <= j <= p-3 and p | numerator(B_j)},
O_p = {even j: 2 <= j <= p-3 and ord_p(2) | j},
T_p = B_p union O_p.
```

Reduce a positive index to `{1,...,p-1}` modulo `p-1`.  The cyclic starting
residues `u` for which

```text
A_u = A_(u+1) = A_(u+2) = 0 mod p
```

are exactly the following four disjoint classes:

1. `u` even, `2 <= u <= p-5`, with
   `u,u+2 in E_p` and `u+2 in T_p`;
2. `u=p-3`, with `p=1 mod 4`, `p-3 in E_p`, and `p` a base-two
   Wieferich prime;
3. `u` odd, `3 <= u <= p-6`, writing `j=u+1`, with
   `j in E_p intersect T_p` and `j+2 in T_p`;
4. `u=p-4`, with `p-3 in E_p intersect B_p` and `p` base-two
   Wieferich.

All other residues, including `1,p-2,p-1`, are impossible.  There is no
triple for `p=3`.

Thus Güleç's lower bound holds for every power of any prime for which these
four local patterns are absent.  This sharpens the earlier global
E-regular/B-regular sieve: the relevant Euler and Bernoulli irregular indices
must be adjacent and aligned with the order of `2`.

The strengthening is strict already at `p=67`.  Exact recurrences give

```text
E_67={26},  B_67={58},  ord_67(2)=66,
```

and `67` is not base-two Wieferich.  Hence `67` is both Euler-irregular and
Bernoulli-irregular, but none of the local patterns occurs.  The theorem
therefore proves `s(67^r) >= r-2` for every `r>=2`, a case not covered at even
exponents by either global regularity hypothesis alone.

## Reproduction

Python 3.11 or later and only the standard library are required.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The verifier uses the differential recurrence for `sec+tan`, an independent
Entringer-triangle implementation at selected primes, and the defining
Bernoulli recurrence.  It checks every odd prime through `1200`, including
the tangent-number and boundary identities and the classification residue by
residue.  This finite audit corroborates the displayed all-prime proof; it is
not extrapolated into that proof.

## Scope and trust boundary

The theorem is a necessary modular obstruction, not a proof of the full
preperiod conjecture: a prime with a listed modular triple still has to meet
the stronger `p^3,p^2,p` divisibilities in Güleç's criterion.  The theorem
does not classify those higher lifts.

The universal argument imports Güleç's shift congruence and preperiod
criterion, the classical tangent-number formula, and von Staudt--Clausen.
The audit trusts CPython arbitrary-precision integer arithmetic, source
inspection, and SHA-256.  It uses no floating point, randomization, solver,
external data, or generated certificate.

Literature and status details are in [SOURCES.md](SOURCES.md).  Novelty is
search-relative; no historical-priority claim is made.
