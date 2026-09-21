# Exact stable transitivity of locally transitive tournaments

Every locally transitive tournament `T` has

```text
m(T) = 0 if T is transitive, and m(T) = 1 otherwise.
```

This is an order-uniform theorem with an explicit degree-one witness.  Fix
any vertex `v`, let `L={v} union N+(v)` and `H=N-(v)`, and reverse the cut
`(L,H)`.  Local transitivity forces the resulting tournament `P` to be a
total order.  If `P_L,P_H` are its two restrictions, then

```text
T + P = (P_L P_H) + (P_H P_L).
```

The full proof, including the switching lemma, a closed witness for every
odd carousel tournament, and a substitution-closure consequence, is in
[THEOREM.md](THEOREM.md).

## Reproduction

The proof does not depend on computation.  A compact exact audit checks all
labelled tournaments through order six and every possible root of the
construction, then checks independent cut-switch and carousel families:

```bash
cd graph_theory/stable_transitivity_local_orders
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
sha256sum -c SHA256SUMS
```

Expected output is recorded in `EXPECTED_OUTPUT.txt`.  The recorded run uses
CPython 3.11.2 and only the Python standard library.

## Files and trust boundary

- `THEOREM.md`: universal proof and exact formulas.
- `verify.py`: exhaustive and parametric exact checks.
- `test_verify.py`: focused boundary tests.
- `SOURCES.md`: primary-literature and Discovery Net status audit.
- `EXPECTED_OUTPUT.txt`: compact expected output.
- `SHA256SUMS`: integrity manifest.

The checker uses integer tournament profiles, with no solver, randomness,
floating point, network input, or external dataset.  Its finite checks are
an audit of the construction, not evidence from which the theorem is
extrapolated.

## Scope and novelty status

Davis and Schroeder introduced stable transitivity in 2026.  Local-order
tournaments and their switching characterization are classical.  Targeted
primary-source and Discovery Net searches through 2026-09-21 found no prior
statement of the exact stable-transitivity formula above.  The novelty claim
is therefore deliberately search-relative, not a historical-priority claim.
