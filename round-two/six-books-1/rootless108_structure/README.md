# Ordinary reductions for rootless 108-edge Book graphs

Actual author **six-books-1**, role **researcher**, 2026-10-01.

[PROOF.md](PROOF.md) proves two scoped ordinary theorems. At108 red edges
and maximum degree10, absence of a full-degree root forces three/four
low points. Any red K4 saturates a complete type signature with an exact
root count; in the rootless case it is the four degree-nine clique and
its six pair-type points induce a graph of maximum degree2 with no triangle.
Separately, a cubic neighborhood at a degree-ten root with at most one
neighbor of degree9 and all others10 is Petersen. The cubic hypothesis
remains explicit.

No108-edge nonexistence or Ramsey endpoint is established. The rootless
sector remains open; a bounded solver probe returned UNKNOWN. The new
proofs are ordinary unformalized mathematics with author exact validation,
not independent peer review. The historical minimum-degree catalogue is
not a premise. The8012 maximum-degree theorem is needed only for applying
the first theorem to arbitrary valid108-edge Book graphs.

From the repository root, run sequentially:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 -B round-two/six-books-1/rootless108_structure/check.py
python3 -B -O round-two/six-books-1/rootless108_structure/verify.py
```

Python3.11 standard library only. `check.py --write` regenerates the small
[expected record](expected.json). The separate checker imports no producer.
No solver, downloaded input, private corpus or external graph catalogue
is required. Source makes every finite control scope explicit.

Expected:35 signed clique degree controls/2520 literal cross identities;
20 pair-triangle cases;1858 labelled maximum-degree-two graphs,1708 triangle-free;
54 residual degree2^4,3^2 graphs, zero girth-five; primary21 valid with93
red edges/pages3,6; six damaged records rejected. Completed runs0.416/0.265s,
under19MiB each. These checks validate the ordinary arguments; counts alone
are not a host classification or mathematical nonexistence certificate.
