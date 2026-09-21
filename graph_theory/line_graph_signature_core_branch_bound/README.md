# A core-branch bound for line-graph signature

Let `G` be a finite connected simple graph, let

```text
c(G) = |E(G)|-|V(G)|+1,
```

let `H=core_2(G)`, and let `b(H)` be the number of vertices of `H` whose
degree in `H` is at least three.  For every `c(G)>=2`, the theorem proved
here is

```text
s(L(G)) <= b(H)-c(G)+1 <= c(G)-1.                  (1)
```

Here `s` denotes adjacency signature (positive inertia index minus negative
inertia index).  The first inequality keeps the branch-vertex information;
the second follows from `b(H)<=2c(G)-2`.

The key new ingredient is an order-independent rooted-tree invariant.  If
`T` is a tree rooted at `r`, put

```text
C_T = Q(T)-2I+e_r e_r^T,
sigma(T) = sig(C_T),       rho(T) = (C_T^-1)[r,r].
```

Then `sigma(T)<=0`, and `sigma(T)=0` forces `rho(T)=1`.  In the exact
2-core Schur complement, every strictly positive diagonal correction is
therefore paid for by at least one unit of negative signature from its
attached tree.  After that cancellation, deleting the corrected core
vertices leaves only disjoint paths plus at most `b(H)` branch vertices.
Interlacing gives (1).

The complete proof is in [THEOREM.md](THEOREM.md).

## Consequences

- The previously known universal bound `s(L(G))<=c(G)` improves by one for
  every `c(G)>=2`.
- If `f(c)=max{s(L(G)):G connected, c(G)=c}`, then `f(2)=1` and `f(3)=2`.
  The two public graph6 witnesses are replayed exactly by the checker.
- The conjectural inequality `2s(L(G))<=c(G)+1` follows for `c=2,3`.
- Rose and generalized-theta upper bounds are recovered immediately from
  their one- and two-vertex branch sets, without a residue-class census.

## Reproduction

The proof is human-checkable and does not depend on computation.  The exact
checker exhausts all labelled connected simple graphs through order six,
checks every relevant principal core inequality through order five, checks
all unlabeled rooted trees through order twelve, and replays sharp witnesses
for `c=2,3`.

```bash
cd graph_theory/line_graph_signature_core_branch_bound
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
sha256sum -c SHA256SUMS
```

Expected output is recorded in `EXPECTED_OUTPUT.txt`.  The checker uses only
the Python standard library and exact rational arithmetic.  It uses no
solver, floating point, randomness, network input, or external dataset.

## Files and trust boundary

- `THEOREM.md`: universal proof.
- `verify.py`: independent exact audits and sharp witnesses.
- `test_verify.py`: focused tests of the arithmetic and encodings.
- `SOURCES.md`: primary-literature and Discovery Net status audit.
- `EXPECTED_OUTPUT.txt`: compact frozen output.
- `SHA256SUMS`: integrity manifest.

Finite computation audits definitions and proof lemmas; it is not the basis
for extrapolating the universal theorem.  The novelty statement is
search-relative, not a claim of absolute historical priority.
