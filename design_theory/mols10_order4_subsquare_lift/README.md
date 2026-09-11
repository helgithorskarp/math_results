# Exact named-coordinate lift for the Myrvold `(U,U)` branch

## Scope

This package gives an exact SAT lift and complete symmetry-safe branch
framework for the open question whether a `3-MOLS(10)` can contain a Latin
subsquare of order four.  It specializes first to Myrvold type `(U,U)` but
the distinguished-square and `Sigma`-support machinery applies to all eight
surviving type pairs.

It does **not** claim an existence or nonexistence decision.  The mathematical
advance is an exact named-coordinate formulation of the distinguished square,
forced dark- and white-intersection theorems for `(U,U)`, and proved exhaustive
finite decompositions that support certified follow-up searches.

The starting pair encoder is from Bright--Keita--Stevens,
[*Myrvold's Results on Orthogonal Triples of 10 x 10 Latin Squares: A SAT
Investigation*](https://doi.org/10.37236/13960), with source archived at
[Zenodo](https://doi.org/10.5281/zenodo.18130631).  See `NOTICE.md` for
attribution and the derivative-code license.

## Exact distinguished-square lift

The published encoder searches for a coloured mutual-transversal-
representation pair `(P,Q)`.  Its colours are necessary shadows of a possible
distinguished square but do not name that square.  The added flags

```text
-triple -direct-extension -distinguished-subsquare
```

introduce the actual distinguished Latin square `L` and agreement tensors

```text
Z[q,j,p]  <=> Q[q,j] = P[p,j],
PE[p,l,j] <=> P[p,j] = L[l,j],
QE[q,l,j] <=> Q[q,j] = L[l,j].
```

Each tensor is Latin, and the three are coupled by the exact coordinate
identity

```text
PE[p,l,j] <=> exists q: QE[q,l,j] and Z[q,j,p].
```

The lower-right block `L[6:10,6:10]` is fixed to the selected representative
`Omega_1` (the cyclic square) or `Omega_2` (the Klein square).  Every dark,
white, and light status in `P,Q` is tied back to the named source row and
symbol in `L`.  Thus this mode represents the target itself, rather than the
larger generic-extension problem used to reject the individual pair samples
in Section 4.6 of the paper.

Completeness follows from Theorem 4.1 of Bright--Keita--Stevens: every target
triple has a representative with `(P,Q)` in their normal form and the
distinguished subsquare equal to `Omega_1` or `Omega_2`.  Conversely, a model
contains the three mutual TRPs `(L,P,Q)`.  Their Theorem 3.1(b) constructs the
three MOLS

```text
L, P^{-1}L, Q^{-1}L.
```

`verify_triple_model.py` reconstructs these arrays and checks all Latin, TRP,
colour, subsquare, normalization, and pairwise-orthogonality conditions from
a SAT model without consulting the CNF clauses.

The optional `-pairwise-onehot` mode replaces a general totalizer when the
cardinality is exactly one.  For the unbranched exact `(U,U)` instance this
reduces the representation from 49,690 variables and roughly 414,000 clauses
to 8,890 variables and roughly 230,000 clauses.

## Forced dark-intersection theorem

**Lemma.** In every distinguished-square realization of type `(U,U)`, the
twelve dark cells induce the following unique simple bipartite graph between
the four dark-bearing rows of `P` and `Q`:

```text
{(p,q): 6 <= p,q < 10 and (p >= 8 or q >= 8)}.
```

Indeed, row-pair uniqueness follows from the TRP property.  The nonzero dark
degrees on both sides are `(2,2,4,4)`.  Each degree-four vertex must meet all
four opposite vertices.  Each degree-two vertex can then meet only the two
opposite degree-four vertices, proving the assertion.

The encoder feeds all twelve forced intersections and all forbidden ones back
into the named `Z` coordinates.  `audit_uu_dark_structure.py` independently
enumerates every simple labelled 4-by-4 bipartite graph with these degrees and
finds exactly the displayed graph.

## Forced white-intersection theorem

**Theorem.** In every distinguished-square realization of type `(U,U)`, join
a row of `P` to a row of `Q` when their unique intersection is one of the
sixteen white cells in the last four columns.  The resulting simple bipartite
graph has exactly the following form:

- rows 6 and 7 on the two sides induce `K_2,2`;
- rows 8 and 9 of `P` partition rows 0 through 5 of `Q` into two triples;
- rows 8 and 9 of `Q` partition rows 0 through 5 of `P` into two triples;
- there are no other white edges.

The white degrees on both sides are `(1,1,1,1,1,1,2,2,3,3)`.  This graph is
edge-disjoint from the forced dark graph because a pair of TRP rows intersects
in exactly one column.  The two degree-three `P` rows cannot meet any of the
last four `Q` rows in a white edge, since every such pair is already a dark
edge.  Their six white edges therefore use all six degree-one `Q` rows.
The symmetric argument uses all six degree-one `P` rows.  Only the four
low--low pairs remain for the two degree-two rows, forcing `K_2,2`.

There are exactly `binom(6,3)^2=400` labelled graphs of this form.  Normalize
the first triple using the six top-row permutations of `Q`.  Since row 0 of
`P` is distinguished by the published first-row form, the second partition
has two cases according as row 0 meets row 8 or row 9 of `Q`; the other five
top rows normalize each case.  Quotient the pair consisting of this bit and
the column-0 dark matching by the four low/high row swaps.  The resulting
action on `38*2=76` states has exactly nine orbits, of sizes

```text
4,16,16,8,8,4,8,8,4.
```

The flags `-whitegraph-0` through `-whitegraph-8` impose representatives and
retain the lexicographic symmetries inside each fixed three-row part.  With
the three first-row forms and two subsquare classes they give an exact family
of `2*3*9=54` CNFs.  This supersedes the coarser 36-CNF dark-only family as
the preferred global `(U,U)` decomposition.

There is also a complete named-coordinate refinement.  The white graph has
five components: four 3-edge stars and one 4-cycle.  Its edges biject with the
sixteen cells of the fixed order-four subsquare; incident edges must have
different column, source-row, and symbol coordinates.  The unique white edge
of `P` row 0 anchors one cell.  The other two edges of its star have exactly
six possible unordered coordinate pairs for either subsquare class and any
of the three first-row forms.  Flags `-fixedstar-0` through `-fixedstar-5`
therefore refine the exact cover to 324 CNFs.  Direct enumeration finds
373,248 anchored coordinate embeddings for the cyclic square and 2,985,984
for the Klein square.  These are skeleton counts, not MOLS completions.

`audit_uu_white_structure.py` independently enumerates the 400 graphs, the
nine joint orbits, the six anchored-star cases, and the coordinate-embedding
counts from their definitions.

## Two exhaustive decompositions

First, sort the six rows of `L` outside the subsquare by their first-column
symbols.  Latinness forces those entries to be

```text
0,1,2,3,a,b,  with 4 <= a < b <= 9.
```

The fifteen `-lfirstpair-ab` flags therefore form a complete split for either
subsquare class and any fixed published `P` first-row normal form.

A smaller `(U,U)` split uses the forced graph.  The two dark cells in column
zero form a size-two matching in its twelve edges.  There are 38 labelled
matchings.  The four unused swaps within the two `p_2` and two `p_3` rows of
`P` and `Q` produce exactly six orbits, of sizes

```text
2,16,8,2,8,2.
```

The flags `-darkcol0-0` through `-darkcol0-5` choose orbit representatives
and omit precisely the four row-order inequalities consumed by those swaps.
Together with `-p0a`, `-p0b`, `-p0c` and the two subsquare classes, these are
`2*3*6=36` exhaustive instances.  `generate_darkcol0_family.py` generates
the family and a hash manifest.

Finally, the large-symbol support in the top-left 6-by-6 block `Sigma` has
all row and column sums two.  It is a 2-regular bipartite graph and hence has
one of exactly four cycle patterns:

```text
12, 8+4, 6+6, 4+4+4.
```

The `-sigma-*` flags fix canonical representatives.  In this alternative
normalization the published `P` first-row form is correctly omitted because
the first-six-column action has instead been spent on `Sigma`.  Exhaustive
enumeration finds 67,950 labelled supports, split as 43,200, 16,200, 7,200,
and 1,350 across the four patterns.  This decomposition transfers unchanged
to the other Myrvold type pairs.

## Reproduction

Only Python 3 standard-library code is required to run the audits and produce
CNF.  To reproduce the finite structural counts:

```sh
python3 audit_trp_encodings.py
python3 audit_uu_dark_structure.py
python3 audit_uu_white_structure.py
```

Expected output is in `EXPECTED_OUTPUT.txt`.  To build the complete 36-CNF
family:

```sh
python3 generate_darkcol0_family.py \
  --encoder encode.py \
  --out build/cnf \
  --manifest build/manifest.json
```

To build the stronger 54-CNF white-graph family, or its 324-CNF anchored-star
refinement, run

```sh
python3 generate_whitegraph_family.py \
  --encoder encode.py --out build/whitegraph \
  --manifest build/whitegraph-manifest.json
python3 generate_whitegraph_family.py --fixed-star \
  --encoder encode.py --out build/fixedstar \
  --manifest build/fixedstar-manifest.json
```

A single exact instance, for example, is generated with

```sh
python3 encode.py UU -triple -direct-extension \
  -distinguished-subsquare -pairwise-onehot -z4 \
  -p0a -whitegraph-0 -fixedstar-0 > UU-z4-p0a-whitegraph-0-fixedstar-0.cnf
```

Kissat 4.0.4 or CaDiCaL 1.9.5 can read the result.  A SAT solver output can be
checked with

```sh
python3 verify_triple_model.py --type UU --omega z4 \
  --encoding direct --distinguished-subsquare MODEL
```

The first exploration tested unbranched exact cases for both subsquare
classes, all four canonical `Sigma` supports for `Omega_1`, eight of the
fifteen `(p0a,a,b)` branches for `Omega_1`, and bounded representatives of the
dark-, white-, and fixed-star decompositions.  All bounded runs ended
`UNKNOWN`; none is treated as evidence for nonexistence.  The next certified
search should use the 54-instance white-graph family or its exact 324-instance
fixed-star refinement.
