# Independent repair-face audit

Reviewer: **six-reviewer-5**, independent mathematical reviewer.
Target: LEMMA10119/index0. Exact scope, conditional verdict, ordinary
proof, mathematical trust boundaries and proved improvements are in
[REVIEW.md](REVIEW.md).

Use CPython3.12 and install the exact generation dependencies from
[requirements.txt](requirements.txt) in your own environment. Then run:

```bash
python3 -B validate.py
```

The validation creates fresh ignored `work/normal` and `work/optimized`
directories from source alone. An existing directory is rejected to avoid
silently reusing a mathematical stream; choose a new copy of the packet
for another cold run. The optional `--campaign-state PATH` checks external
pause barriers and supplies no mathematical inputs. No network, solver,
private ledger or producer certificate is used by the mathematics.

Expected:42 positive and12 intended-rejection children, all21 entire
normal/optimized/private records agree, native threads1, one serial child,
fixed45-second child guard. Large regenerated polynomial/coefficient
records remain ignored and unpublished. An incomplete run supplies no
verdict. [VALIDATION.json](VALIDATION.json) records the actual completed
run; [PRIMARY.json](PRIMARY.json) seals the earlier independent source
and records before adapting them to this standalone packet.

The mathematical engine uses SymPy exact rational fields and polynomial
gcd/division for generation. Separate stdlib checks invert every shifted
coefficient certificate, bind full original-member controls, and check
Pell Horner remainders by expanded monic division. All ordinary reduction,
representation, rank and root arguments remain unformalized, with precisely
credited spectral/separation/recovery/tail inputs. This is not a completely
CAS-free or formal proof. The written target proof was exposed, NOT BLIND;
the target's new native programs/certificates/results were not inspected.
