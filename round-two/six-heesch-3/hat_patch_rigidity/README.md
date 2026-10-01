# Local rigidity of a 25-hat contact network

Researcher: **six-heesch-3**. This compact exact certificate restricts a
proposed route to finite Heesch number seven. Retaining this particular
25-copy network of complete boundary-port contacts permits locally only
similarities and the published hat edge-length parameter. Every normal
boundary profile is forced flat. The resulting polygons tile the plane.

The `544 x 100` integer endpoint Jacobian has exact rank 95, certified by
a minor nonzero modulo 1009 and five exact independent kernel vectors.
The four function-valued contact components each have a checked odd walk.
See [the proof and scope](proof.md). No finite-seven construction, arbitrary
patch exclusion, or quantitative neighbourhood is claimed.

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B round-two/six-heesch-3/hat_patch_rigidity/check.py --expected
```

CPython 3.11.2; standard library only. The reader reconstructs all contacts
from 25 exact integer poses and checks disjoint interiors, the two
determinant certificates, and eight malformed controls. Runtime is below
one second on one CPU. The optional `--make-certificate` reselects the small
minors; ordinary verification uses only the published certificate.

The hat construction and continuum are prior art from
[Smith, Myers, Kaplan and Goodman-Strauss](https://arxiv.org/html/2303.10798v3).
The fixture was extracted from Kaplan's [hatviz](https://github.com/isohedral/hatviz),
commit `4bb9d01999e4e84accc2a78d0fa279ef20b47263`; the source license is retained.
