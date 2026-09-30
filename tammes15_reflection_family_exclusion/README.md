# A finite reflection-gluing family excluded from better Tammes-15 packings

Author: **six-tammes-2**, role: **researcher**. Date: 2026-09-30.

The [proof](PROOF.md) excludes a family of thirteen-vertex, twenty-four-edge
contact motifs from any fifteen-point packing whose minimum geodesic
separation is strictly better than the incumbent. The family consists of a
triangulated octagon and a triangulated pentagon, with their two pentagon
ears attached by four contacts to pairs with existing common octagon
neighbors. There are 355 degree-compatible cases across eight octagon
patch types. This broadens the cyclic incumbent core's packing exclusion.

Seven identically zero residuals are treated explicitly. Of the remaining
cases, exact root and orientation checks leave six thirteen-point packings
below the incumbent cosine. Exact polytope certificates prove that each
admits at most one additional separated point. These are useful local
exclusions; arbitrary contact graphs remain outside this family and global
Tammes-15 bounds and optimality remain unresolved.

Run with **Python >=3.11**, standard library only:

```sh
python3 -B tammes15_reflection_family_exclusion/check.py
python3 -B -O tammes15_reflection_family_exclusion/check.py
python3 -B tammes15_reflection_family_exclusion/check.py --selftest
```

The normal output matches [EXPECTED.json](EXPECTED.json). Failures remain
active under optimization. The checker compares all 132 octagon
triangulations with an independent enumeration of the 15,504 five-diagonal
subsets, derives every gluing residual, uses exact Sturm counts, constructs
both orientations, and exhaustively enumerates the extension polytopes.
It needs no coordinates, network access, optional generator, scratch data,
solver, floating-point tolerance, or large proof corpus.

The optional generator requires **SymPy 1.14.0** and independently derives
all residuals in its rational-function field before factorization and root
isolation. It reads no certificate:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B tammes15_reflection_family_exclusion/generate_certificate.py \
  | cmp - tammes15_reflection_family_exclusion/certificate.json
```

The six short extension seeds in the generator choose origin tetrahedra
and cap normals; their validity is proved by the checker. The certificate
contains only root brackets, case assignments, packing witnesses and these
seeds. The written reduction, exact custom arithmetic and ordinary Python
execution are the trust boundary. This is an author-audited computational
lemma, unformalized and awaiting independent mathematical review.

Arithmetic helpers reuse the author's preceding exact contact-core work,
but this directory is self-contained. The incumbent and its quintic are
prior results. The [cyclic core](../tammes15_contact_pattern_obstruction/CYCLIC_CORE.md),
the [asymmetric core](../tammes15_contact_pattern_obstruction/CONTACT_CORE.md),
its [independent review](../tammes15_contact_core_review1/README.md), and the
[complementary geometric lane](../tammes15_eight_quad_reduction/ONE_FIVE.md)
provide context; the last two are not proof premises for this new family.
Primary references and the precise scope appear in the proof.
