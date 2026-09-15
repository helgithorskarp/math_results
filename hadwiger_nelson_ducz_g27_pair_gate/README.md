# Exact ordinary-colour gate for Dúcz's displayed `G_27`

This package reconstructs the complete strict unit-distance graph on the 27
points displayed in Section 3 of Ákos Dúcz,
[A note on geometric colorings of the Moser lattice](https://arxiv.org/html/2606.12325v1).
The result is an exact scoped stop for a Hadwiger--Nelson construction intake:

- the 27 coordinates are distinct;
- the complete physical graph has 49 unit edges;
- its ordinary chromatic number is exactly **3**; and
- 17 checked proper four-colourings separate every pair of distinct points;
  and 16 further checked words colour together every physical nonedge in at
  least one word. Thus every nonedge admits both equality states in ordinary
  four-colourings.

The lower bound is the triangle on zero-based vertices `(3,5,13)`. The saved
word `000201201202100210212020122` is a proper three-colouring of every one of
the 49 physical unit edges. For the pair statement, assign to each vertex its
17-entry colour signature across the separating words. All 27 signatures are
different. For the reverse state, every one of the 302 nonedges is equal in at
least one of the 16 coalescing words. Both statements are positive
certificates: no SAT or exhaustive-search `UNSAT` verdict is used by the
checker.

## Why this is not a contradiction

Dúcz discusses `G_27` because its **geometric fractional** chromatic number is
4. Geometric colourings impose additional congruence constraints on isometric
independent sets. Ordinary graph colourings impose no such constraints, so an
ordinary three-colouring is compatible with that theorem. The present graph
also includes every unit pair among the displayed coordinates, whether or not
that pair was selected in an earlier abstract presentation of `G_27`.

The coordinates are the 27 columns of Dúcz's integer matrix in the basis
`1, omega_1, omega_3, omega_1*omega_3`, where
`omega_1=(1+i*sqrt(3))/2` and `omega_3=(5+i*sqrt(11))/6`. All collisions and
distances are decided with rational coefficient vectors in
`Q(sqrt(3),sqrt(11))`; no floating-point predicate occurs.

## Reproduce

With CPython 3.11 or later and the standard library:

```bash
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
python3 -B verify.py --controls
```

The checker independently expands the displayed basis, reconstructs all 351
unordered distances, checks the edge-stream hash, validates the triangle and
three-colour word, validates every saved four-colour word, checks that the
colour signatures separate all vertices, and checks coalescence coverage of
all 302 nonedges. The controls corrupt a colour on an edge and truncate the
coalescing certificate, confirming rejection.

## Construction consequence and scope

The source fails the campaign's first physical gate because it is only
three-chromatic. The complete two-state certificate additionally proves that
every physical nonedge has the neutral ordinary four-colour relation, ruling
out any single-pair forcing completion from this fixed support. The result says
nothing about other finite subsets of the Moser lattice or ring, higher-arity
terminal relations, added outside-ring points, or the Hadwiger--Nelson number.
It produces no five-chromatic graph and no improvement on Parts's 509-vertex
published record.

This is author-side exact verification of a finite source, not an independent
review of Dúcz's theorem and not a priority claim.
