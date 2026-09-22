# Exact toggle optimality for every bounded poset of height at most three

Every such poset has a legal winning word that moves each proper element
`v` exactly `|mu(v,top)|` times. The word simultaneously minimizes every
nonnegative element-weighted move cost. This covers lattices and also
bounded posets that are not lattices, without bounds on their order or
incidence degrees. Height counts **strict inequalities** in a longest chain.

For a poset with at least three elements, write `m` for its number of
coatoms and `R=sum_a(deg(a)-1)` over its interior elements that are not
coatoms. Then

\[
\text{shortest winning length}=2\max\{m-1,R\}+1.
\]

The proof traverses the proper-part incidence components, then splices
their words into bottom-addition positions. This handles disconnected
proper parts and zero-Möbius elements as well as connected ones.

Together with Wilhelm's existing depth-four counterexamples, this
determines the **minimum height of an unwinnable lattice as four**, both
for the toggle game and for unrestricted proper-ideal dot-algebra trees.
The sharp upper bound is from that prior work. No new explicit
counterexample or minimum-order bound is claimed.

Read [PROOF.md](PROOF.md) for the complete argument and
[SOURCES.md](SOURCES.md) for the attribution and novelty boundary.

## Reproduce the exact audit

Python **3.11.2** was used; Python 3.11+ and the standard library suffice.
From this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
sha256sum -c SHA256SUMS
```

The default command compares the full deterministic summary against
[expected.json](expected.json). It checks:

* all **7,846 prescribed labeled incidence matrices** with at most seven
  interior vertices, allowing isolated coatoms but no isolated non-coatom
  atoms; no isomorphism quotient is taken;
* definition-level replay of **62,100 moves**, including 1,963 cases with
  zero bottom Möbius value, and an independent BFS optimum for every matrix;
* **238 weighted Dijkstra checks** on the matrices with at most five interior
  vertices, using two fixed integer cost vectors, including zero costs;
* twelve named/boundary fixtures, including the Fano plane, the affine plane
  of order three, disconnected cases of all three bottom signs, and a
  nonlattice; eight fixtures also have all vertex labels reversed;
* fifteen malformed-input or corrupted-word rejections.

The entrywise matrix/word/optimum digest is
`ab93e68623d023b2122feae3a30ad5489c6285727ea2d416150378461111d3f7`.
The initial complete audit took about **2.4 seconds** and **17 MB peak RSS**
on the development host; timings are not part of the expected record.

[compiler.py](compiler.py) builds words without a state search.
`compile_poset(order)` accepts a Boolean reflexive order matrix on arbitrary
integer labels and rejects malformed, unbounded or taller posets.
`compile_incidence(m, neighborhoods)` accepts the incidence representation
directly; its label convention is documented in the function.

[verify.py](verify.py) separately computes Möbius values from the general
recurrence and checks each principal ideal as a set. Its shortest-path
search uses integer state masks and all legal moves, with no sign-coherence
restriction. No solver, floating-point arithmetic, random seed, external
catalogue or omitted data file is involved.

## Trust and stopping boundary

The universal result rests on the written proof. Finite code checks audit
the construction and implementation; they do not replace that proof or
independently establish the cited height-four existence theorems. Ordinary
Python/runtime/source-inspection trust remains. The proof is unformalized
and independent review was pending at publication.

This completes the height-three target. Further research needs a concrete
objection or a separately specified structural problem; this package does
not initiate a height-four or larger-order census.
