# Gal's conjecture through six excess vertices, in every dimension

**Complete proof attempt; independent review pending.** Every finite flag
generalized homology `(d-1)`-sphere over a field with `n <= 2d+6` vertices
has an entrywise nonnegative gamma-vector.

[PROOF.md](PROOF.md) transfers the accepted seventeen- and eighteen-vertex
five-sphere results to **all dimensions**. The new work is a structural
reduction, not a further fixed-order enumeration:

- A parameterized complement identity proves `gamma_2 >= 0` for excess
  `ell=n-2d <= 6` without either computational seed.
- At excess six and `d>=8`, every sphere has a vertex with at most two
  nonneighbors. The last obstruction would have a link with `gamma_2<=3`,
  while a near-maximal-dimension lemma forces `gamma_2=5`.
- Suspension and two-antipode recurrences then propagate the small-dimensional
  inequalities to every dimension.

The full all-face-links homology condition is essential. This is not the
unrestricted Gal conjecture, a sphere classification, or the stronger claim
that gamma is the face vector of a flag complex.

## Reproduction

No packages, compiler, solver, network access, or external data are required
for the **new exact audit**. From this directory, with Python 3.11 or later:

```sh
python3 verify.py
sha256sum -c SHA256SUMS
```

Expected: `status: PASS`, 135,619 parameterized graph identity instances,
11 explicit sphere fixtures, and canonical-output SHA-256
`b30063d70d13873b42862c9f2dc1973a212352a157874e4eb26eb6245b59bc30`.
The output is [EXPECTED.json](EXPECTED.json). To regenerate a separate copy:

```sh
python3 verify.py --write /tmp/excess-six-audit.json
```

The audit derives gamma coefficients from direct face counts, checks 811,139
individual link identities, all 35,425 relevant integer degree profiles,
and exact polynomial recurrences. Exhaustive small-graph checks include
non-spheres and even negative formal excess; these test polynomial identities,
not the hypotheses or enumeration completeness of a sphere classification.
Fixture spherehood follows from joins and edge subdivisions of cycles or a
cross-polytope boundary. Their full face and gamma polynomials are checked.

The written proof, not the finite audit range, supplies the universal
induction and structural statements. Running this audit does not replay the
inherited eighteen-vertex UNSAT certificates; use the
[base package](../charney_davis_18_vertex_certificate/README.md) for that.

## Provenance and trust

[SOURCES.md](SOURCES.md) identifies published topology inputs, both graph
theorems, their independent reviews, and the literature overlap. In
particular, the recent small-pseudomanifold classification already discusses
`gamma_2 >= 0` at excess at most five; no novelty is claimed for that subrange.

The new argument is human mathematics, not proof-assistant formalized. The
computer-assisted base retains its topology-to-CNF and certificate-checking
boundary. Acceptance of that base does not constitute review of this transfer.
No new large certificate is needed or distributed.
