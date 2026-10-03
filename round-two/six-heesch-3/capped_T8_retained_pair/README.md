six-heesch-3, researcher. An author-checked two-copy obstruction for the literal left-capped T8 under arbitrary Euclidean motions.

The pair T and T+(-20,-4), with physical coordinates(x,sqrt(3)y)/4, cannot have(0,0) inside any further packing union retaining the pair. In the displayed public h8l six-corona layout this rules out a seventh retaining that layout. Other sixth arrangements and the shape's global Heesch upper remain unresolved. The [proof](PROOF.md) explains the complete50-supplier enumeration and exact strict overlap points.

From the repository root, using CPython3.12.14 (standard library only):

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 round-two/six-heesch-3/capped_T8_retained_pair/check.py --input round-two/six-heesch-3/capped_T8_retained_pair/certificate.json --out /tmp/capped-pair-reading.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 round-two/six-heesch-3/capped_T8_retained_pair/controls.py --out /tmp/capped-pair-controls.json
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 round-two/six-heesch-3/capped_T8_retained_pair/generate.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 round-two/six-heesch-3/capped_T8_retained_pair/application.py
```

Run serially. For an optimized replay put `-O` after `python3` and choose new output filenames; the readers refuse overwrites. All eight source checks exited0 under unchanged1CPU/2GiB and native1 limits. The four entire mathematical result pairs agreed after removing only elapsed time and reported peak RSS. Point checking took about0.03seconds. The application uses the sibling `external_six_corona_replay` directory, already published and credited; it does not rerun the positive whole-corona proof.

Expected certificate SHA256: `a5a1490e65c699d3aee061ff8577712e54c9068abdedc6dc7248bf6e6dbce2d4`. Standalone reading SHA256: `76badc353be021873ebc19ad9a2d38793f8ea1befa42ca00c8e251ffe73f9396`. Controls SHA256: `d09067fe19c2a7b7a8e10c22694e149ca53ab2550bcba4232d238387e0c91916`. The reader reconstructs complete suppliers and checks positive support inequalities at every rational witness; producer flags and clipping are not proof premises.

`expected.json` records the whole result seals. `manifest.json` binds compact source files. No solver, foreign executable, key, ledger, exploratory corpus or large proof dump is included. No independent review, formalization, finite-seven result or global Heesch upper is claimed. Prior construction credit and dependencies are in the proof and application.
