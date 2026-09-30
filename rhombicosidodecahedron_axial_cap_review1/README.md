# RID axial classification and all-source cap: independent review

**six-reviewer-1, independent mathematical reviewer**, 2026-09-30.

This compact audit confirms the exact 436-region axial classification and
the original all-source receiver cap theorem at graph 7256, by
six-rupert-3. It reconstructs the geometry in exact `Q(sqrt(5))` arithmetic,
using nearest points of signed vertex hulls. The four original contact pairs
are reused with credit and validated against all 60 independently generated
vertices. It also proves a `1/25` winning-component normal bound, improving
the `1/24` bound used in graph 7498. It does not settle global RID Rupertness.

- [REVIEW.md](REVIEW.md): scoped verdict, evidence, literature and opportunities.
- [PROOF.md](PROOF.md): complete finite reduction and continuum cap bridge.
- [check.py](check.py): field kernel, proper group and anchored simplex census.
- [cap_checks.py](cap_checks.py): shadow rolls, weak supports, torque facets and exact margins.
- [reproduce.py](reproduce.py): full reconstruction and optional summary comparison.
- [expected.json](expected.json): compact deterministic results.
- [source_manifest.json](source_manifest.json): pinned target provenance and inspected file hashes.

From the repository root, Python 3.11 or later, standard library only:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B rhombicosidodecahedron_axial_cap_review1/reproduce.py --self-test
```

The deterministic expected output SHA-256 is
`1878d73ffd4b7ef0587cdff9eaf7bb0ea8afbf9be66dcb66d030cf416a0a3b22`.
The regenerated full optimizer-record digest is
`4379fb6314158e318402352f572ab08528cad39da604429f54086b9bb3d7bc54`.
The full record list is not a proof input and is not published. An optional
`--records PATH` writes it to a private scratch path; it is unnecessary for
reproduction. Timing and peak RSS are printed separately to stderr.

The checker includes three deliberately corrupted-input controls. Rejecting
an unsupported larger cap means its quantitative proof guards fail; this
does not demonstrate a passage or refute a larger exclusion theorem.

Trust boundaries: coordinate model, exact rational/quadratic kernel, Python,
finite cover arguments and the ordinary analytic proof. No proof assistant,
floating-point geometry, external solver or researcher Python module is used.
Expected output is read only after all finite geometry has been regenerated.
The inspected target commit is
`9e9374854d153addb1d7697d05fd4b5d0180849f`; this review's publication commit
is recorded separately in its graph contribution.
