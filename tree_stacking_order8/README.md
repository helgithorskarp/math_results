# Exact tree-stacking census at order eight

## Result

For every tree $T$ on eight vertices,

$$
\operatorname{stack}(T)=\operatorname{estim}(T),
$$

where, following Csernák and Soukup,

$$
\operatorname{estim}(T)=
\max_{r\in V(T)}\left(
1+\operatorname{leaf}(r)+
\sum_{\substack{v=r\text{ or }\deg_T(v)>1}}
\deg_T(v)2^{d_T(r,v)}
\right).
$$

Thus their tree-stacking conjecture holds for all trees on at most eight
vertices. Their primary paper reports the exhaustive result only through seven
vertices. This is a finite computer-assisted finding, not a proof of their
conjecture for arbitrary trees.

In the order produced by NetworkX 3.5's `nonisomorphic_trees(8)`, the 23 exact
stacking numbers are

```text
255, 160, 83, 144, 85, 77, 136, 97, 89, 104, 81, 58,
52, 54, 31, 48, 61, 50, 33, 57, 46, 35, 22.
```

## Exact recurrence

Let $N_m(T)$ be the set of non-stackable configurations of total size $m$.
Every pebbling move lowers total size by one. A non-stacked configuration
$d$ of size $m>1$ is in $N_m(T)$ exactly when every legal one-move child of
$d$ is in $N_{m-1}(T)$. If $d$ has a legal child, it is a parent of an element
of $N_{m-1}(T)$; if it has no child, it is a binary configuration and is added
explicitly. These observations give a complete recurrence with no heuristic
step.

`enumerate_tree8_stacking.cpp` implements this recurrence and stores one
canonical representative per automorphism orbit. Automorphisms preserve both
moves and stackability, so this quotient is lossless. For each tree the program
computes the automorphism group by testing all $8!$ permutations, reconstructs
the estimate independently from graph distances and degrees, and asserts that
the first empty frontier above weight eight occurs at the recorded estimate.

The largest frontier in the census belongs to the path: 212,846 non-stackable
orbits at weight 46. The largest non-path frontier has 169,577 orbits. The
complete fresh run had 1,882 output lines and SHA-256
`badf8114972d310f68da3c77760d4aa5413d3ec381232dac69a9eb2f7ae1d48b`.
The log belongs under `/scratch` and is intentionally not committed.

## Independent checks

`check_tree8_results.py` uses NetworkX 3.5 independently to:

- regenerate all 23 nonisomorphic order-eight trees;
- match the catalog bijectively up to graph isomorphism;
- recompute every estimate and automorphism-group order;
- parse all 23 result records from the C++ run; and
- optionally verify selected critical configurations by direct memoized
  forward reachability, without reading the C++ frontier tables.

Direct forward checks covered catalog IDs 2, 14, 18, and 22. ID 2 alone
visited 207,054 canonical descendants; the three more symmetric controls
visited 5,359 descendants in total. All four critical configurations were
independently non-stackable. The complete upper bounds still rely on the C++
frontier recurrence.

## Reproduction

The reported run used GCC 12.2.0, Python 3.11.2, and NetworkX 3.5.

```bash
g++ -std=c++20 -O3 -DNDEBUG -march=native \
  -Wall -Wextra -Wpedantic \
  enumerate_tree8_stacking.cpp \
  -o /scratch/enumerate_tree8_stacking

/scratch/enumerate_tree8_stacking tree8_catalog.tsv \
  > /scratch/tree8-stacking-full.log

python3 -m venv /scratch/tree8-check-venv
/scratch/tree8-check-venv/bin/pip install -r requirements.txt

/scratch/tree8-check-venv/bin/python check_tree8_results.py \
  tree8_catalog.tsv /scratch/tree8-stacking-full.log \
  --witness-tree 2 --witness-tree 14 \
  --witness-tree 18 --witness-tree 22

sha256sum /scratch/tree8-stacking-full.log
```

Individual catalog IDs can be rerun by passing the ID as the second argument
to the C++ program.

## Trust boundary and novelty

The result depends on the parent/child recurrence, correct automorphism
canonicalization, the 23-tree catalog, the implementations, and the named
compiler/runtime. All configuration arithmetic is integral. No randomized
search, SAT solver, proof log, floating-point decision, or unverified external
certificate enters the equality claims; wall-clock timings are the only
floating-point outputs.

The primary paper and its companion repository were searched through
2026-08-31. They report equality for the 24 trees of orders two through seven,
but not for order eight. No later source extending their finite tree census was
located. The order-eight extension is therefore apparently new to the searched
sources, not a claim of literature priority.

Primary source:

- T. Csernák and L. Soukup, *Stacking and clearing in graph pebbling*,
  arXiv:2604.22341v1 (2026), <https://arxiv.org/abs/2604.22341>.
- Authors' computational repository, inspected at commit
  `701cdd93dd19869a9b90947edd6361efd81cfc1f`,
  <https://github.com/lajossoukup/pebbling>.
