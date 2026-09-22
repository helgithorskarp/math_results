# Subcubic parity kernels for line-graph signature

For a connected graph `H` of minimum degree two and maximum degree three,
compress every maximal degree-two path between branch vertices.  Its length
modulo four has exactly one of two roles:

- an odd path becomes a signed edge in a branch matrix `P`;
- an even path becomes an equality or negation row in a signed incidence
  matrix `V`.

If `Z` spans `ker(V)`, every unbounded path length disappears from the
signature formula:

```text
sig(Q(H)-2I)=sig(Z^T P Z),
s(L(H))=sig(Z^T P Z)-c(H)+1.
```

The full inertia, including all singular cases and loop paths, is proved in
[THEOREM.md](THEOREM.md).

## Consequences

Let `beta` be the number of balanced components of the signed graph formed
by the even branch paths, including isolated branch vertices. Then

```text
s(L(H)) <= beta-c(H)+1.
```

Since the number of branch vertices is `2c(H)-2`, the sharp open bound

```text
2 s(L(H)) <= c(H)+1
```

holds whenever the signed even-path incidence matrix has rank at least
`floor(c(H)/2)-1`.  Adding four edges to any one branch path adds two positive
and two negative shifted-signless-Laplacian eigenvalues and leaves the
line-graph signature unchanged.

This does not prove the full conjecture: the remaining subcubic cases have
too few independent even-path constraints, and arbitrary pendant trees or
vertices of core degree at least four require additional arguments.

## Reproduction

The theorem is a written congruence proof.  The exact checker independently
extracts branch paths from all 1,797 connected labelled subcubic 2-cores
through order six, compares the full matrix inertia with the parity-kernel
formula, verifies signed-component ranks, and performs direct line-graph
checks on a declared subset.  It also tests 240 longer constructions over
five cubic pseudokernels, including loops and parallel paths, and verifies
the four-subdivision law.

```bash
./run_checks.sh
```

Expected output is frozen in `EXPECTED_OUTPUT.txt`.  Python 3.11 or later
and the standard library suffice.  Arithmetic is exact `int`/`Fraction`;
there is no floating point, randomness, solver, external dataset, generated
catalogue, or omitted certificate.

## Files

- `THEOREM.md`: statement and universal proof.
- `SOURCES.md`: prior work, status, and novelty boundary.
- `verify.py`: exact definition-level audit.
- `test_verify.py`: focused boundary and malformed-input tests.
- `EXPECTED_OUTPUT.txt`: frozen audit record and success marker.
- `SHA256SUMS`: integrity manifest.
