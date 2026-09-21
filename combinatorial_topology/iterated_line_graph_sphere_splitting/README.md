# Sphere splitting under iterated line graphs

For every finite connected simple graph `G` with at least two edges,

\[
\mathrm{Cl}(L^2G)\simeq\mathrm{Cl}(LG)\vee
\bigvee^{\sum_v\binom{\deg_G(v)-1}{3}}S^2.
\]

Here `L` is the line graph and `Cl` is the full clique complex; degrees
at most three contribute zero. The proof uses explicit relative
collapses and nullhomotopic triangle attachments, together with
Adamaszek's known one-step theorem.

As a consequence, every connected graph other than a path, cycle or
claw has an `S^2` homotopy retract in **every clique complex of its
fifth and later line graphs**. Five is sharp: a claw with one subdivided
edge has four contractible positive iterates, followed by an `S^2`.
Exactly paths, cycles and the claw have all nonempty positive iterates
aspherical. The one-edge graph is excluded from the displayed formula
because its second line graph is empty.

- [PROOF.md](PROOF.md): universal splitting, degree argument, sharpness,
  conventions and homotopy trust boundary.
- [SOURCES.md](SOURCES.md): prior one-step and degree-growth results,
  bounded novelty audit, and an inaccessible 1991 full-text limitation.
- [verify.py](verify.py): exact face-poset replay and separate boundary
  matrix checks, using CPython 3.11+ and its standard library only.
- [expected.json](expected.json): compact deterministic evidence.

From the repository root:

```sh
python3 combinatorial_topology/iterated_line_graph_sphere_splitting/verify.py
```

Expected status: `VERIFIED`, matching `expected.json`. Tested with
CPython 3.11.2. From this contribution directory, verify file integrity:

```sh
sha256sum -c SHA256SUMS
```

The checker examines all 772 connected labelled simple graphs on at
most five vertices, including the 770 in the recurrence's domain.
It replays 320 elementary collapse pairs and verifies their 320 cone
disks. Four additional high-degree fixtures exercise longer collapse
sequences. Separate `F_2` boundary-rank calculations include tetrahedra
and confirm the predicted homology changes. The sharpness fixture is
checked through its fifth iterate; malformed inputs and corrupted
collapse certificates are rejected. All checks remain active under
Python's `-O` option.

These finite checks corroborate an ordinary mathematical proof; they
do not prove the universal homotopy claim, and acyclicity is never used
as a substitute for contractibility. There is no solver, floating-point
step, random sampling, external dataset or omitted large certificate.
The equivalences are not asserted canonical or equivariant. Independent
review and formalization are not part of this source. No global
priority claim or resolution of Whitehead's conjecture is made.
