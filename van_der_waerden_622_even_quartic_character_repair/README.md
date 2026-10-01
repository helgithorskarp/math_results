Author: **six-vdw-1**, role **researcher**. Exact computer-assisted lemma for
symmetric two colors/seven terms W(2,7).

Over the field F311, consider every quartic

    P(x) = alpha*((x-v)^4 + A*(x-v)^2 + B),  alpha != 0.

Take its quadratic-character bit at every nonroot, with arbitrary independent
bits at its roots, and lift by

    c(t+1) = (t mod2) XOR phi(t mod311).

Every such period-622 seed has **20 root-free monochromatic seven-term integer
APs in [1,2171] with pairwise disjoint field supports**. Root recoloring cannot
suffice. An AP-free repair in this same template must change at least **20
nonroot field bits**, hence at least **220 binary coordinates in [1,3704]**.
An unrestricted word must change at least20 nonroot coordinates; the220
consequence requires the template. No AP-free3704 witness or new W bound is
provided. The lemma covers quartics that become even after translation, not
all quartics, and makes no optimality or distinct-orbit claim.

From the repository root, Python3.11+ and standard library only:

```bash
python3 van_der_waerden_622_even_quartic_character_repair/reproduce.py \
  --output-dir /tmp/vdw622-even-quartic
```

This regenerates all625 sufficient cases in313 serial bounded children,
checks the133,443-byte certificate SHA256, independently verifies all12,500
APs/87,500 actual term colors in normal and optimized Python, rejects18
mathematical corruptions in each mode, and audits the complete96,721(A,B)
normalization parameter pairs. Each child has the unchanged30-second guard,
one thread, and at most200,000 declared arithmetic/truth/choice cases.
Generated chunks and logs stay outside the repository. No private corpus is
an input. Explicit `--resume` reuses only completed identical-source jobs;
failed or interrupted jobs require attention rather than silent retries.

Expected final status:
`EVEN_QUARTIC_CHARACTER_REPAIR_SOURCE_ONLY_REPRODUCTION_PASSED`.
For a quick independent check of the supplied compact certificate, run:

```bash
python3 van_der_waerden_622_even_quartic_character_repair/check_packings.py \
  --certificate van_der_waerden_622_even_quartic_character_repair/packings.json \
  --output /tmp/vdw622-even-quartic-check.json
```

The proposer uses square enumeration and greedy field-disjoint packing.
The checker imports no proposer, evaluates actual integer positions by Horner's
rule and Euler's criterion, and retains every substantive check under `-O`.
This is independent implementation by the same researcher, without external
review or formalization. See [PROOF.md](PROOF.md), [expected.json](expected.json),
[VALIDATION.md](VALIDATION.md), [check_packings.py](check_packings.py),
[audit_reduction.py](audit_reduction.py), and [packings.json](packings.json).

The earlier [degree-at-most-three character lemma](../van_der_waerden_622_degree3_character_repair)
supplies method context; its numerical certificates are not premises here.
The field-affine transport and basic character normalization are familiar
arguments. The new scoped result is the complete625-case root-free packing
bound for this specified quartic family, new to the inspected sources rather
than an exhaustive historical-priority claim.
