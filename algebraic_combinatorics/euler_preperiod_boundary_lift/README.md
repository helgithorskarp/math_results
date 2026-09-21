# A uniform higher lift at the Euler-preperiod boundary

This directory proves an exact `p`-adic valuation formula for an infinite
arithmetic progression of Euler up/down numbers and applies it to the
boundary class in the Euler-preperiod conjecture.

## Main theorem

Let the Euler up/down numbers be defined by

```text
sum_(n>=0) A_n z^n/n! = sec(z) + tan(z).
```

For every odd prime `p` and every integer `q>=1`, put

```text
w_p = v_p(2^(p-1)-1).
```

Then

```text
v_p(A_(q(p-1)-1)) = w_p - 1.                         (1)
```

The right side is independent of `q`, even when `p` divides `q`.

## Preperiod consequence

Let `s(p^r)` be the least preperiod of the Euler up/down sequence modulo
`p^r`.  If `r>=4` and

```text
r = 1 mod (p-1),
```

then

```text
p^3 does not divide 2^(p-1)-1
    implies
s(p^r) >= r-2.                                       (2)
```

Equivalently, any failure of the conjectured lower bound in this exponent
class forces the order-three base-two Wieferich condition

```text
p^3 divides 2^(p-1)-1.
```

The previously proved local obstruction theorem identifies this congruence
class with its even-boundary start `p-3`.  Combining the two results, a
failure from that boundary class must also have `p=1 mod 4` and
`p | A_(p-3)`.  Thus (1) supplies a genuine higher-power filter beyond the
reviewed modular taxonomy.

The proof is in [THEOREM.md](THEOREM.md).

## Reproduction

Only Python's standard library is required (Python 3.8 or later):

```bash
python3 verify.py | diff -u EXPECTED_OUTPUT.json -
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
sha256sum -c SHA256SUMS
```

The verifier constructs the Euler up/down numbers directly with the
Entringer recurrence, without using Bernoulli numbers, the tangent-number
formula, or LTE.  At the default limit 1200 it checks 2,321 instances of
(1) over 196 odd primes.  In 316 instances `p | q`, directly exercising the
cancellation that is easy to miss in the proof.  It also checks the first
base-two Wieferich prime `1093` definitionally at `A_1091`, and verifies that
both classical examples `1093` and `3511` have `w_p=2`, not at least three.

These exact finite checks audit the formula and edge cases.  The universal
claim follows from the written valuation proof, not from computation.

## Scope

This does not prove the full preperiod conjecture.  It closes the higher-lift
question only for exponents `r=1 mod (p-1)`, corresponding to one of the four
local modular classes.  Interior starts and the odd-boundary start still
require separate `p^2`/`p^3` analysis.  No claim is made that order-three
base-two Wieferich primes do or do not exist.
