# Residue-compressed ancestry certificates for odd-cycle stacking

Let the vertices of `C_(2k+1)` be `0,1,...,2k` cyclically, and put

```text
M_k = 5*2^(k-1)-6,
c_k = M_k e_0 + e_k + e_(k+2).
```

The checked certificates in this directory prove that `c_k` is not stackable
for every `3 <= k <= 1000`.  Consequently

```text
stack(C_(2k+1)) >= 5*2^(k-1)-3       (3 <= k <= 1000).
```

This verifies the proposed odd-cycle lower bound from `C_7` through `C_2001`.
It does **not** prove the conjectured equality, an upper bound, or the graph's
previously asserted exact value for `C_13`.

## Ancestry-forest reduction

Label every initial pebble.  Trace a final pebble backwards through a stacking
sequence.  A move from `u` to its neighbor `v` makes one pebble at `v` from two
pebbles at `u`, so the ancestry of one final pebble is a full binary tree:

- its root is at the final vertex;
- its two children, when present, are both at one neighboring vertex;
- its leaves are initial pebbles.

The final pebbles partition all initial labels, hence a stacking sequence gives
a forest of such trees with one common root location.  Conversely, the moves
of any such forest can be executed in postorder.  Thus the forest model is
equivalent to stackability, not a relaxation.

There are only two distinguished singleton leaves.  For one ancestry tree,
let

```text
D[v,S,r]
```

be a lower bound on the number of leaves drawn from the pile at vertex `0`,
where the tree is rooted at `v`, contains the singleton subset `S`, and its
pile-leaf count is `r` modulo 3.  The two singleton subsets are bit masks, so
there are only `4*3*(2k+1)` local states.

The one-leaf bases have costs `1,0,0`.  At an internal ancestry node, two trees
at the same source vertex, with disjoint singleton masks, are joined by one
pebbling move to a neighboring root.  Therefore every valid lower-bound table
must satisfy the local Bellman inequalities

```text
D[v,S1 union S2,(r1+r2) mod 3]
    <= D[u,S1,r1] + D[u,S2,r2]
```

for every edge `uv` and disjoint `S1,S2`.  Induction on ancestry-tree size
proves that any table satisfying the bases and all these inequalities is a
genuine lower bound.  `verify.py` constructs a strong table by a
Knuth/Dijkstra-style finite tree-grammar relaxation and then checks all the
inequalities independently of the relaxation order.

At a proposed common root `v`, the two singleton leaves are either in one tree
or in two separate trees.  Any number of no-singleton trees may also occur.
Min-plus convolution over the three residue classes checks every such forest.
For the residue of `M_k`, the certified forest lower bound is

```text
5*2^(k-1)-3  when k-2 <= v <= k+3,
5*2^(k-1)    at every other root.
```

Both values exceed `M_k`, by three or six respectively, for all tested `k`.
This six-vertex exact root profile is also a structural diagnostic: the proof
is not merely a replay of the full configuration frontier.

## Reproduction

Only CPython's standard library is required.  The publication run used
CPython 3.11.2.

```bash
python3 verify.py --max-k 1000
python3 independent_check.py --max-k 9
python3 -m unittest -v test_verify.py
```

`verify.py` prints a SHA-256 digest of every generated local-table entry and
root bound in canonical order.  The digest and compact expected output from
the publication run are recorded in `expected_summary.txt`.

`independent_check.py` does not import the production implementation.  For
`3 <= k <= 9`, it retains every attainable pile-leaf count through the claimed
bound as arbitrary-precision integer bitsets and closes the ancestry grammar
by height.  It independently verifies nonstackability and the same root
profile.  The unit tests check known small bounds and ensure that a local
certificate mutation is rejected.

All mathematical arithmetic is exact.  There is no randomization,
floating-point decision, SAT/SMT solver, proof log, or external generated
input.  The trust boundary is the ancestry-forest equivalence, the residue
compression, the two implementations, CPython, and the execution host.

## Context and novelty scope

The primary source introduced stacking and reported

```text
stack(C_3), stack(C_5), stack(C_7), stack(C_9), stack(C_11)
    = 4, 8, 17, 37, 77,
```

but explicitly gave no conjecture for odd cycles:

- Tamás Csernák and Lajos Soukup, *Stacking and clearing in graph pebbling*,
  arXiv:2604.22341v1, <https://arxiv.org/abs/2604.22341>.

Discovery Net later proposed `5*2^(k-1)-3` and stated lower-bound computations
through `k=200`, but the conjecture node supplied neither source nor a separate
supporting contribution.  Its only incoming reproduction checks `C_7` and
`C_11` and explicitly leaves the `C_13` frontier incomplete.  This directory
therefore supplies a public, independently checkable structural certificate
and extends the finite lower-bound range to `k=1000`.  Apparent novelty is
limited to the searched primary source and committed graph; no priority claim
is made.
