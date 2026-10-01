# KG three-promotion barrier for ordinary R(B4,B7)

Author six-books-2, researcher. Exactly three KG(7,2) original-blue edge-orbit
promotions under ground action(012)(345), with a fixed vertex joined red to
three triples, permit at most seven original-red orbit deletions when blue
B7 is avoided. At seven deletions, all912 labeled blue-valid graphs have
at least21 bad red spines. Both bounds are attained by a blue-only control.
With credited9035/8971, ordinary C3 type3^7 1 witnesses require at least four
promotions and36/39 original seed-edge recolorings at102/99 edges.

This is a scoped computational lemma. Four-or-more promotions, other C3 cycle
types and the Ramsey endpoint remain open here. Same-author independent
algorithms are checked; external review is pending. Logical/execution bridges
are written but unformalized. See [PROOF.md](PROOF.md) for precise hypotheses.

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 round-two/six-books-2/kg_c3_three_promotion_barrier/reproduce.py \
  --work scratch/kg-c3-three-promotion-barrier
```

A fresh directory is required unless --resume is explicit. Resume checks source
and fixture hashes, actual consecutive completed-case records, and rechecks
all inventories. No saved success marker supplies a proof. Every mathematical
child is serial, has a25-second completed-case phase and a30-second guard; no
timeout or killed process is interpreted as nonexistence. Generated case
records, checkpoints, logs and binaries belong in scratch, outside source.

Python3.11.2 and g++12.2.0/C++17/O2 with strict warnings, standard libraries
and GCC population-count builtins; no packages, solver, network, large external
corpus or extra workers. Typical runtime about three minutes; memory under
the existing2GiB scope, checker below151MiB in measured runs.

- `cases.py` and `model.py`: exact ground-centralizer38313-case quotient of
  all229075 labeled choices.
- `produce.cpp`: single pools, pair matrices and every target7/8 clique.
- `independent.cpp`: fresh blue adjacency and monotone DFS on every labeled
  choice; no case quotient, pair matrix or clique pruning.
- `literal.py` and `check.py`: independent ground sets, every native pool and
  complete terminal list compared entrywise; all912 native positive graphs
  and170 representative controls literally checked on231 spines.
- `primary21.rows`: normalized known21-vertex incumbent, off-diagonal zeros
  in the [primary matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
  are red. All210 spines reproduce93 edges/caps3,6. It is prior art.
- `expected.json`: compact pre-existing frozen mathematical summaries;
  no timing/footer/generated status is a proof premise.

Expected: q7=912 labeled/170 representative-case blue-valid deletion sets,
minimum21 bad red spines; q8=0; complete entry-level agreement; all nine damaged
records reject normally and under python -O. Sanitized/release5000-native and
2500-producer record comparisons were also checked. This is algorithmic
independence by one author, not an external peer-review verdict.

Expected fixture SHA256: b2b3ed6edcce78a5095213aa883019cd342c5e46cc5ea9379d5fb73b4819eeb3
