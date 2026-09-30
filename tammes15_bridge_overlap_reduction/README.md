# Tammes-15 bridge reduction with shared original vertices

Author: **six-tammes-2**, role: **researcher**, 2026-09-30.
Status: author-audited exact computer-assisted reduction with a written
proof; unformalized and independent mathematical review pending.

A strict improvement on the known fifteen-point incumbent cannot contain
a prescribed contact-triangulated octagon A and pentagon B whose two ears
are outside A and each contact two A vertices, **unless B's anchor triangle
is a prescribed triangle of A**. The remaining three B vertices may be
shared with A. Both patches must still be internally injective.

This replaces full vertex disjointness in the earlier bridge exclusions
by the absence of a shared prescribed triangle. It does not prove global
motif occurrence or improve a numerical Tammes bound. Six continuous
placements remain when the triangle is shared: ten actual points, exactly
seventeen contacts, and four triangulated-decagon contact types. Their
fifteen-point extensions remain unresolved.

Read [PROOF.md](PROOF.md) for the full hypotheses, proof and dependencies.
The old thirteen-point extension certificates and exceptional saturation
theorem are used as published mathematical dependencies; this checker
checks the weakened overlap criterion, rather than replaying those
extension polytopes.

From the repository root, with Python 3.11 or later:

```sh
python3 -B tammes15_bridge_overlap_reduction/check.py
python3 -B tammes15_bridge_overlap_reduction/check.py --selftest
python3 -B -O tammes15_bridge_overlap_reduction/check.py --selftest
cd tammes15_bridge_overlap_reduction
sha256sum -c SHA256SUMS
```

The three checker commands give identical [EXPECTED.json](EXPECTED.json).
The checker regenerates all 355 old-neighbor cases, proves the entire
branch partition, derives all overlap coordinates, and certifies that
both exceptional degree-fifteen frames have no coincident positions.
No solver verdict, floating-point coordinate table or network is used.

The optional separate arithmetic audit uses pinned SymPy 1.14.0:

```sh
python3 -m venv tammes15_bridge_overlap_reduction/.venv
tammes15_bridge_overlap_reduction/.venv/bin/pip install -r tammes15_bridge_overlap_reduction/requirements.txt
tammes15_bridge_overlap_reduction/.venv/bin/python -B tammes15_bridge_overlap_reduction/audit_sympy.py
```

Its six placement rows and exceptional noncoincidence summary agree
exactly with the checker. It separately derives rational coordinates,
residuals, root counts and algebraic signs. It shares the finite graph
catalog, pure graph canonicalization and certificate seeds; this is not
an independent enumeration or independent mathematical review.

Use one thread for each command; run commands sequentially. The compact
[certificate.json](certificate.json) contains root brackets, case/root
assignments, collision witnesses and alias pairs, with no saved coordinate
corpus. Each sign is exact; an unresolved sign raises an error. The
selftest rejects eight false certificate cases and checks arithmetic,
Sturm endpoints and multiple roots. Validation remains active under `-O`.
