# Derived G24 capacity certificate

Actual author six-tammes-2, researcher. The exact thirteen-label motif
consists of original G20 plus5-12,2-x,9-x,10-x. On the entire closed
cosine band[14/25,593/1000] it admits at most ONE arbitrary additional
unit code point, so it cannot occur in a fifteen-point code. Applying
the motif derivation in9922 eliminates the5-12/degree10=5 branch.
The other G20 branches and global optimality remain open.

Read [PROOF.md](PROOF.md) for the ordinary normalization, convexity and
cap arguments. The certificate covers all364 active-plane triples
and the complete closed interval, including the critical strip.
Independent mathematical review/formalization are pending.

Python3.11+ and its standard library suffice. Set all native threads to1.
From this directory:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 generate.py --output /tmp/derived-g24-certificate.json
cmp CERTIFICATE.json /tmp/derived-g24-certificate.json
python3 check.py --output /tmp/derived-g24-check.json
cmp EXPECTED.json /tmp/derived-g24-check.json
python3 audit.py --output /tmp/derived-g24-audit.json
cmp AUDIT_EXPECTED.json /tmp/derived-g24-audit.json
python3 controls.py > /tmp/derived-g24-controls.json
cmp CONTROLS.json /tmp/derived-g24-controls.json
```

Repeat each Python command with`python3 -O` for the optimized controls.
These are serial commands; run one mathematical child at a time.
Every program has a50-second internal guard; the recorded subprocess
guard is55seconds. An incomplete run supplies no exclusion.
The generator uses integer Bernstein signs, the checker uses rational
Horner/Bernstein signs, and the audit uses rational Taylor enclosures.
They share the displayed coordinate/Cramer reduction and polynomial
kernel; this corroboration is not independent peer review.

[SYSTEM.json](SYSTEM.json) fixes the literal graph, interval and arbitrary
addition quantifier. [CERTIFICATE.json](CERTIFICATE.json) is a compact
parameter cover, not a search log or raw expanded polynomial corpus.
[RUNTIME_PINS.json](RUNTIME_PINS.json), [VALIDATION.json](VALIDATION.json),
[DEPENDENCIES.json](DEPENDENCIES.json) and [LITERATURE.md](LITERATURE.md)
record reproducibility, credit and scope. No floating-point pilot is a
proof input. Label13 here means fresh x, with a different mask from the
older fixed-incumbent G24.
