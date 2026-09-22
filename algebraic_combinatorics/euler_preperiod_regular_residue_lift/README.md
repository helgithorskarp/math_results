# Regular-residue lifts for Euler up/down numbers

Let `A_n` be the Euler up/down numbers,

```text
sec(z)+tan(z) = sum_(n>=0) A_n z^n/n!.
```

This directory proves an exact higher-`p` lift theorem for every interior
Bernoulli-regular tangent residue.  If `p` is an odd prime,

```text
2 <= j <= p-3,  j even,  p does not divide numerator(B_j),
m >= 2,          m = j (mod p-1),
```

then

```text
v_p(A_(m-1)) = v_p(2^m-1).
```

Writing `d=ord_p(2)` and `w_p=v_p(2^(p-1)-1)`, this is the explicit
dichotomy

```text
v_p(A_(m-1)) = 0                 if d does not divide j,
v_p(A_(m-1)) = w_p + v_p(m)      if d divides j.
```

The proof is a three-line structural combination of Kummer's congruence,
the tangent--Bernoulli identity, and LTE.  Those ingredients are classical;
the mathematical increment here is their uniform use as the missing
higher-lift invariant for the order-only classes in the Euler-preperiod
problem.  No historical priority is claimed for the standalone valuation
identity.

The preperiod application is conditional only on the exact criterion in
Guelec's current paper.  In an even-interior modular obstruction whose middle
tangent zero is order-only, a failure of `s(p^r)>=r-2` forces

```text
w_p + v_p(r-1) >= 2.
```

In an odd-interior obstruction whose first tangent zero is order-only, it
forces

```text
w_p + v_p(r-2) >= 3.
```

For an ordinary non-Wieferich prime these become `r=1 (mod p)` and
`r=2 (mod p^2)`, respectively.  This is a uniform congruence sieve, not a
prime or offset census and not a proof of the full preperiod conjecture.

## Reproduce

CPython 3.11 or later is sufficient; there are no third-party dependencies.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.json -
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
sha256sum -c SHA256SUMS
```

The verifier derives Euler numbers independently from the Entringer triangle
modulo prime powers.  It checks 2,957 theorem instances, including ordinary
and base-two-Wieferich lifts, an instance with `p^2 | m`, and a deliberately
excluded Bernoulli-irregular boundary.  The finite audit checks conventions
and sharp hypotheses; the universal quantifiers rest on
[THEOREM.md](THEOREM.md).

## Files and trust boundary

- `THEOREM.md`: statement, proof, preperiod consequences, and limitations.
- `SOURCES.md`: literature and graph-context audit.
- `verify.py`: exact standard-library audit.
- `test_verify.py`: boundary and mutation tests.
- `EXPECTED_OUTPUT.json`: frozen compact audit output.
- `SHA256SUMS`: hashes of the substantive files.

The theorem is an unformalized human proof.  The audit trusts CPython integer
arithmetic, the displayed Entringer recurrence, and ordinary hardware.  It
uses no solver, floating point, randomness, external dataset, or hidden
certificate.
