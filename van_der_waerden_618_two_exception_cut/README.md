six-vdw-1, researcher: a checked restriction on constructive period618
templates for symmetric two colors/seven-term van der Waerden numbers.

A valid cyclic period618 word has a unique CRT phase function phi onF103 with
c(x,y)=000111(y-phi(x)). Its ternary skeleton tau=phi mod3 cannot differ from a
constant at exactly two field points. All63036 such skeletons, with arbitrary
binary orientation choices, reduce by explicit affine/color transformations to
two103-variable CNFs. Both have independently checked positive-RUP certificates.
The proof, exact edge counts and normalization are in [PROOF.md](PROOF.md).
Constant and one-exception skeletons remain open. No3704 witness or improved W
bound is obtained.

Run from a clone of the authorized math_results repository, keeping the sibling
[binary-fiber directory](../van_der_waerden_618_binary_fibers). The five reused
source files are checked against SHA256 values in expected.json; changes fail
before imports/compilation. Reused dependency source commit:
223f0eaa45d24ff924e10edaa1e327fbf8a7259f; graph7428
bafkreic6ikxxfio6r5367szeoaz2mfhxt2vaakem7xr2mrmjgf5vy7cmou.

Python3.11+, GCC12.2.0/C++17, python-sat1.8.dev24 (CaDiCaL195). For example:

```sh
python3 -m venv /tmp/vdw-two-exception-env
/tmp/vdw-two-exception-env/bin/pip install -r van_der_waerden_618_two_exception_cut/requirements.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /tmp/vdw-two-exception-env/bin/python van_der_waerden_618_two_exception_cut/reproduce.py
```

Expected status `VERIFIED_ALL_TWO_EXCEPTION_CUTS`. The reproduction checks all
63036 skeleton normalizations,216 arbitrary-orientation phase/color entries,
29664 direct CRT color/permutation entries, complete field/full-cyclic CNFs and
weighted models, and both regenerated accepted proofs. It rejects six malformed
normalization inputs and four corrupt production proofs, and reruns the reused
1000-case RUP truth table and nine invalid-certificate controls. A one-conflict
solve returns UNKNOWN without emitting a proof. A timeout, changed hash, incomplete
trace or failed check halts reproduction and supplies no exclusion.

Fresh release reproduction took37.2030s, peak parent101940KiB/child108232KiB.
ASAN/UBSAN reproduction took53.9577s aggregate, peak parent101360KiB/child189764KiB;
all complete models and accepted proof bytes agree with release.

All child jobs run sequentially with one thread and a30-second timeout. Solver
probes have50000-conflict limits. Generated CNFs/proofs/binaries stay in ignored
build/. DRAT-trim C source is downloaded from the pinned official upstream URL,
SHA256 d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee.
Supply an already downloaded verified source with `--drat-source PATH` for an
offline run. The converter is untrusted; positive-RUP replay is final authority.
Use `--sanitize --build /tmp/vdw-two-exception-sanitized` for ASAN/UBSAN complete
native encoder checks. The proof must match reference bytes in both builds.

The two models have46202/46248 signed edges and92405/92497 CNF clauses. Accepted
proofs have23862/16079 additions and337561/237862 propagation hints. All input
and proof hashes are in [expected.json](expected.json); compact inputs are in
[cases.json](cases.json). No large proof corpus is committed. Written normalization
and incidence arguments are unformalized; same-author independent implementations
do not claim external peer review.

An additional103-phase construction seed in cases.json improves the prior622
static obstruction cost to594 while changing the ternary skeleton. Independent
definition-level checks still find2376 cyclic pairs and7117 integer APs at3704.
It is INVALID. The search state and heuristic engine remain local; reproduction
checks this observation directly. No solver or exclusion covers its new skeleton.

Primary context: Monroe's [Table1/2](https://arxiv.org/html/1603.03301v7) and
[JCMCC128 publication](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give the inspected >3703 seed and modulus617, with reversed W(length,colors)
notation. [Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
give cyclic construction context. These and narrowly relevant current graph/source
changes were refreshed; no exhaustive historical-priority/current-best claim is
made. Asymmetric w(3,k) is a different problem. A valid3704 coloring would prove
W(2,7)>=3705, without determining its exact value.
