# Total colouring from a matching in the complement

This directory proves a uniform total-colouring theorem and applies it to
the canonical thick-spider frontier in split graphs.

Let `G` be a simple graph of even order `2r>=6`.  If the complement of `G`
has a perfect matching, then

```text
chi''(G) <= 2r-1.
```

If additionally `Delta(G)=2r-2`, this is sharp and `G` is Type 1:

```text
chi''(G) = Delta(G)+1 = 2r-1.
```

The proof constructs a one-factorization of `K_(2r)` with a rainbow perfect
matching.  Delete that matching, restrict the edge colouring to `G`, and
give each endpoint the colour formerly carried by its deleted matching
edge.

For the thick spider `S_r`, whose clique is `x_0,...,x_(r-1)`, whose stable
set is `y_0,...,y_(r-1)`, and where `x_i y_j` is an edge exactly when
`i!=j`, the exact consequence is

```text
chi''(S_r)=2r-1  for every r>=2.
```

For `r>=3` these graphs lie in the stretch-index-three split-graph frontier
left open by the current general classification work.

See [`THEOREM.md`](THEOREM.md) for the proof and [`SOURCES.md`](SOURCES.md)
for the literature boundary.  Reproduce the exact audit with Python 3.11 or
later and no third-party packages:

```sh
./run_checks.sh
```

The code checks the explicit construction through `r=100`, directly checks
the resulting total colouring of thick spiders through `r=100`, and checks
all `2^12=4096` spanning subgraphs of the six-vertex base graph.  These are
definition-level audits; the universal theorem rests on the written proof.
