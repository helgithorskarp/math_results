# Universal ancestry certificate for odd-cycle stacking

For every integer `k >= 3`, label `C_(2k+1)` cyclically and put

```text
M_k = 5*2^(k-1) - 6,
c_k = M_k e_0 + e_k + e_(k+2).
```

The certificate proved here shows that `c_k` is not stackable for **every**
`k >= 3`.  Consequently

```text
stack(C_(2k+1)) >= 5*2^(k-1) - 3       for every k >= 3.
```

This removes the finite `k <= 1000` restriction from the preceding
residue-compressed computation.  It is a lower bound, not the conjectured
matching upper bound.

## Ancestry-tree criterion

Label the initial pebbles and trace a final pebble backwards.  One pebbling
move combines two pebbles at a vertex `u` into a pebble at a neighbor of `u`.
Thus each final pebble has a full binary ancestry tree.  Its leaves are
initial pebbles, its root is the final location, and both children of every
internal node lie at the same neighboring vertex.  The final pebbles partition
all initial labels into a forest with a common root location.  Conversely,
postorder traversal executes every such forest.  This is an equivalence.

Let `x` and `y` denote the two singleton leaves.  For one ancestry tree define

```text
D(v,S,r),       S subset of {x,y},  r in Z/3Z,
```

to be the displayed lower bound on the number of leaves drawn from the pile
at `0`.  A table is a valid certificate if it has the three one-leaf bases and
if, for every edge `uv`, disjoint `A,B`, and residues `a,b`,

```text
D(v,A union B,a+b) <= D(u,A,a) + D(u,B,b).             (1)
```

Induction on tree size then proves that `D` is a lower bound for every legal
ancestry tree.  All residues below are modulo three.

## Closed-form table

Put `P=2^k`.  Use two coordinates for the cycle:

```text
L_d = d                 (0 <= d <= k),
R_d = 2k+1-d            (1 <= d <= k).
```

The main pile is at `L_0`, singleton `x` is at `L_k`, singleton `y` is at
`R_(k-1)`, and `R_k` is the vertex between the singletons.  At a generic
vertex put `Z=2^d` and `h=k-d`.

If three displayed integers have distinct residues, write
`<a,b,c>_r` for the unique one congruent to `r`.  The symbolic checker verifies
the distinct-residue assertion in every parity class.  The four rows in each
table are indexed by `S=empty,x,y,xy`.

For `L_d` with `h >= 1`, set

```text
D(empty,r) = < Z, 4P-2Z, 5P-2Z >_r
D(x,r)     = < 2P-2Z, 3P-2Z, 4P-2Z >_r
D(y,r)     = < P+Z-3, 7P/2-2Z, 9P/2-2Z >_r
D(xy,r)    = < 5P/2-2Z, 7P/2-2Z, 3P-2Z-3 >_r.
```

For `R_d` with `h >= 2`, set

```text
D(empty,r) = < Z, 4P-2Z, 5P-2Z >_r
D(x,r)     = < 2P+Z-3, 3P-2Z, 4P-2Z >_r
D(y,r)     = < P-2Z, 7P/2-2Z, 9P/2-2Z >_r
D(xy,r)    = < 5P/2-2Z, 7P/2-2Z, 3P-2Z-3 >_r.
```

The three remaining vertices use the following unordered residue triples:

| vertex, row | three candidate values |
|---|---|
| `L_k, empty` | `P, 2P, 3P` |
| `L_k, x` | `0, 2P, 5P/2` |
| `L_k, y` | `3P/2, 2P-3, 5P/2` |
| `L_k, xy` | `3P/2, 2P, 5P/2-3` |
| `R_k, empty` | `P, 2P, 3P` |
| `R_k, x` | `P, 2P, 3P-3` |
| `R_k, y` | `P/2, 5P/2, 3P-3` |
| `R_k, xy` | `3P/2, 2P-3, 5P/2-3` |
| `R_(k-1), empty` | `P/2, 3P, 4P` |
| `R_(k-1), x` | `2P, 5P/2-3, 3P` |
| `R_(k-1), y` | `0, 5P/2, 7P/2` |
| `R_(k-1), xy` | `3P/2, 5P/2, 11P/4-3` |

Each table row is again assigned by residue.  All fractions are integers for
`k >= 3`.

The bases are immediate: `D(L_0,empty,1)=1`, `D(L_k,x,0)=0`, and
`D(R_(k-1),y,0)=0`.

## Why the symbolic check covers infinitely many cycles

There are two infinite edge families and five boundary edge types:

```text
L_d--L_(d+1),             h >= 2,
R_d--R_(d+1),             h >= 3,
L_0--R_1,
L_(k-1)--L_k,
L_k--R_k,
R_k--R_(k-1),
R_(k-1)--R_(k-2).
```

For each direction, the checker expands every instance of (1).  After fixing
the parities of `d` and `h`, every generic-arm difference is exactly

```text
A*2^(d+h) + B*2^d + C = 2^d (A*2^h+B) + C.
```

The checker proves `A >= 0`, proves `A*2^h+B >= 0` at the least admissible
`h` of that parity, and then proves the full expression nonnegative at the
least admissible `d`.  Both monotonicity steps are exact and cover the whole
infinite parity-restricted domain.  At the boundary, every difference has
the form `A*2^k+C`; the same least-`k` argument applies.  No finite cutoff or
extrapolation occurs.

## Forest bound

In a common-root ancestry forest the special leaves are either together in
one `xy` tree or separated into an `x` tree and a `y` tree.  Every remaining
tree has row `empty`.  Among any three or more empty-tree residues, two prefix
sums in `Z/3Z` agree; deleting the intervening residue-zero block preserves
the total residue and cannot increase the lower-bound cost.  It is therefore
enough to check zero, one, or two empty trees.

The checker expands every such decomposition at every table type.  For pile
residue `M_k mod 3`, it proves the lower bound

```text
5P/2 - 3   at L_(k-2), L_(k-1), L_k, R_k, R_(k-1), R_(k-2),
5P/2       at every other root.
```

Both exceed `M_k=5P/2-6`.  Hence no common-root ancestry forest exists and
`c_k` is non-stackable.

## Reproduction

Only CPython's standard library is needed; all arithmetic uses exact integers
and `fractions.Fraction`.

```bash
python3 universal_verify.py
python3 finite_regression.py --max-k 250
python3 ../odd_cycle_stacking_ancestry_certificates/independent_check.py --max-k 9
```

Expected compact output:

```text
UNIVERSAL ODD-CYCLE CERTIFICATE VERIFIED FOR EVERY k >= 3
residue_rows=56
arm_inequalities=1232
fixed_k_inequalities=1596
proof_obligation_sha256=f5ee96681ce4113b11edaf6e8ad7fffcc1f5d47434c05d698e69b22541eaffaa
EXACT TABLE MATCH k=3..250 entries=755904
INDEPENDENTLY VERIFIED k=3..9 targets=91 representation=bounded_cost_bitsets
```

As a fresh regression check, numerical instantiations of the displayed table
agree entry-for-entry with the earlier tree-grammar relaxation for every
`3 <= k <= 250` (755,904 table entries).  The preceding contribution's
relaxation separately verified its root profile through `k=1000`, and its
independent bounded-cost bitset implementation verifies nonstackability
through `k=9`.  Those finite checks support the translation into closed form;
the universal conclusion itself comes from the symbolic inequalities above.

## Scope and sources

The primary source reports
`stack(C_3),...,stack(C_11)=4,8,17,37,77` and does not state an odd-cycle
formula:

- Tamás Csernák and Lajos Soukup, *Stacking and clearing in graph pebbling*,
  arXiv:2604.22341v1, <https://arxiv.org/abs/2604.22341>.

The preceding finite certificate and its independent checker are in
[`odd_cycle_stacking_ancestry_certificates`](../odd_cycle_stacking_ancestry_certificates/).
The present result proves a universal lower bound only.  It does not prove the
conjectured equality, the asserted exact value for `C_13`, or an upper bound.

The trust boundary is the ancestry-forest equivalence, the residue reduction,
the displayed table, the exact symbolic checker, CPython, and the execution
host.  There is no randomization, floating-point decision, SAT/SMT solver, or
external generated input.  Apparent novelty is limited to the searched
primary source and committed Discovery Net graph; no priority claim is made.
