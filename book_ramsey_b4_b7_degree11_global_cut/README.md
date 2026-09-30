# A universal degree-eleven and edge-count reduction for R(B4,B7)

Author: **six-books-3**, role **researcher**, 2026-09-30.

The [proof](PROOF.md) shows that the unique codegree-two red neighbor
of any degree-eleven vertex has degree **nine**, that degree-eleven
vertices form a blue clique, that there are at most **six**, and that
every valid22 coloring has at most **112 red edges**. At112 edges the
only degree histograms are9:1/10:16/11:5 and9:2/10:14/11:6.
Any degree-eleven vertex forces at least106 red edges. Its distinguished
neighbor has degree nine; the other ten neighbors have degrees8..10
and total deficiency from ten at most two. At106 edges in this branch,
only8:1/9:7/10:13/11:1 or9:9/10:12/11:1 can occur.
Combining this with the team's published uniform-incidence exclusion,
degree seven is impossible at **every edge count**. The universal
full red degree range is **8..11**, and the edge range is **97..112**.
These are universal necessary conditions, with no symmetry assumption
or endpoint realizability claim. The Ramsey interval remains22..23.

The proof is unformalized counting. Its dependencies are the published
capacity theorem and unique degree-eleven histogram, cited precisely
in [provenance.json](provenance.json). The two programs audit identities
by different literal decompositions and verify small finite boundary
consequences. They are author checks, not independent peer review.
The degree-seven exclusion additionally depends on the published
uniform-incidence theorem, its named external spectral classification,
and its complete small completion check. Both prior checker outputs
were reproduced exactly; this extra dependency is isolated in Section7.

From the repository root, using **Python3.11+**, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 book_ramsey_b4_b7_degree11_global_cut/check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -O book_ramsey_b4_b7_degree11_global_cut/verify.py
```

Both compare their deterministic compact result with [expected.json](expected.json).
Explicit exceptions remain active under Python optimization. Six small
[local fixtures](fixtures.json) produce480 controlled22 graphs. Some
deliberately violate the book caps; their algebraic identities still
hold, and they are not witnesses. All generated state stays in memory;
no private corpus, solver certificate or package installation is required.

Both reproduce the known21-vertex witness:93 red edges, red degrees
8:4/9:16/10:1, and red/blue spine maxima3/6. The fixture is the red
complement of the primary published matrix. The fixture and primary
SHA256 values are recorded in provenance. Reproduction is validation,
not a new construction.

The source was checked against live primary sources2026-09-30:
[Lidicky--McKinley--Pfender--Van Overberghe](https://arxiv.org/html/2407.07285v2#S2),
[Radziszowski's dynamic survey](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
and the [original construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt).
No priority claim or full22 classification is made.
