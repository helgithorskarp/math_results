# The marked H20/O22 density-92 branch is empty

For the specific H20 and O22 below, every rooted gluing with no red K5,
marked outside degrees 12 and 14, and the stated coverage condition has
**at most 90 red edges in the red neighborhood of the second marked vertex**.
The retained target requires 92. Thus **all 100 marked cases are excluded**
under that density condition, without a gluing solver or further degree
assumptions on the other vertices.

This is a complete closure of one selected fixed-core, marked-coverage-and-
density branch. It is **not** a whole degree-profile exclusion, a general
incompatibility of H20 with O22, or an improvement of the Ramsey bound.
In particular, neither coverage nor density 92 is asserted for every
Ramsey(5,5;43) graph. No 43-vertex target has been constructed. The earlier
unrestricted 440-edge gluing timeout remains UNKNOWN.

## Exact hypotheses and labels

Take a graph G on disjoint parts `{r}`, H, O of orders 1,20,22. Red denotes
edges and blue their complement. Root r is red to every H vertex and blue
to every O vertex. The induced graphs are the byte-pinned edge lists

- [H20](../ramsey_r55_root20_anchor_realization/GRAPH.json), SHA256
  `8d404855787227dc182d7bdc0e98751474ce6c9f1cf872abc52888477c096ccf`;
- [O22](../ramsey_r55_opposite22_realization/GRAPH.json), SHA256
  `e7f6086e6f99edcf47f5f931106bdfc294703e9a74aa8eb1caad60978917f355`.

Let a,b be local H vertices 0,1. Inside H,

```
N_H(b) = {a,16,17,18,19},
d_H(b) = 5,  e_H(N_H(b)) = 4,  d_H(a) = 7.
```

Write C={16,17,18,19}, S0=N_red(a) intersect O and S1=N_red(b) intersect O.
The selected assumptions are

```
|S0|=12, |S1|=14, S0 union S1=O.
```

They imply `|S0 intersect S1|=4` and red degrees 20 at a,b. The complete
43-vertex labels, when needed, are `r=0,H=1..20,O=21..42`; masks always
use local O labels, with bit v indicating vertex v. No automorphism or
row-order normalization is imposed.

The [earlier decomposition](../ramsey_r55_marked_pair_decomposition)
lists all 100 admissible markings in [cases.json](../ramsey_r55_marked_pair_decomposition/cases.json),
SHA256 `c5dfb2f121e8b85fb4078f622257d4a6d924a3f81e055ded9f214d5ed9c89ef9`.
Both new programs reconstruct that relation entry by entry. It is not
assumed complete solely because its hash matches.

The density assumption needed for exclusion is explicitly

```
e_red(G[N_red(b)]) = 92.
```

This was one of the conditional `(92,107)` exceptional neighborhood profiles
in the [H20 handoff](../ramsey_r55_root20_anchor_realization/README.md).
The new upper bound also excludes any required density at least 91.
It does not derive a density from a degree sequence.

## A general local inequality

For a graph J write tau(J) for the largest order of an induced red-triangle-
free subset. If G has no red K5, then for every w in C,

```
|N_red(w) intersect S1| <= tau(O[S1]).
```

Indeed, a red triangle in that intersection, together with the red edge
bw, would form a red K5. This argument does not require a prescribed degree
at w, a full vertex-attachment domain, or any blue-clique constraint.

Now partition the edges of the actual red neighborhood
`N_red(b)={r} union N_H(b) union S1`. There are five red edges from r to
N_H(b), four within N_H(b), e_O(S1) within S1, four from a to S1 by
coverage, and the four C-to-S1 rows. Root r is blue to S1. Hence

```
e_red(G[N_red(b)])
  = 5 + 4 + e_O(S1) + 4 + sum_(w in C) |N_red(w) intersect S1|
 <= 13 + e_O(S1) + 4 tau(O[S1]).
```

More generally, before imposing coverage, replace the second 4 in the
first line by `|S0 intersect S1|`. Keeping that term is essential. This
package does not enumerate changed-coverage markings.

## Complete finite data and closure

Absence of a red K5 requires each O[Si] to be red-K4-free and their common
red neighborhood to be triangle-free. The five possible red-K4-free
14-sets and their exact triangle-free capacities are:

| S1 mask | e_O(S1) | tau | Number of maximizing 8-sets | Valid cover markings | Density ceiling |
|---|---:|---:|---:|---:|---:|
| `1276fe` | 47 | 8 | 3 | 0 | 92, but no marking |
| `127ede` | 45 | 8 | 7 | 20 | 90 |
| `29bb79` | 44 | 8 | 12 | 30 | 89 |
| `39ab79` | 43 | 8 | 23 | 35 | 88 |
| `3e363e` | 44 | 8 | 6 | 15 | 89 |

The first row cannot be discarded by the density inequality alone. Its
zero marking count is separately and exhaustively checked. Across the
100 actual markings the uniform ceiling is therefore 90. We do not claim
that this upper bound is attainable by a full 43-vertex gluing.

At the desired density 92, the four C-to-S1 rows would have to contain
34, 35 or 36 red edges; their combined capacity is at most 32. Case deficits
are exactly 2 (20 cases), 3 (45 cases), or 4 (35 cases).
[certificate.json](certificate.json) contains all five capacity records,
all 51 maximizing eight-subsets, and the separate fixed-edge equation and
strict deficit for every one of the 100 cases. Its SHA256 is
`1451cd470e041a5b3de0874184315265836303880be6387c5b44e35f5c828612`.

This saves all 100 proposed density-92 extension solves. It supplies a
graph-realization obstruction rather than another count-only relaxation.
The longer exploratory local-26-domain scan is not a proof input: the
published argument uses only the elementary common-neighborhood inequality
and the smaller complete finite certificate.

## Independent algorithms, controls, and reproduction

CPython **3.11.2**, standard library only. There is no solver, floating-point,
catalogue-completeness, imported Ramsey-number, or proof-trace dependency.

[analyze.py](analyze.py) computes red clique numbers for all `2^22` O subsets
by least-vertex deletion/intersection. It recovers the size12/14 attachment
domains and exact cover relation. For each of the five size14 domains it
checks all its subsets, finding every triangle-free maximizer.

[verify.py](verify.py) imports neither the producer nor an inherited checker.
It lists the 111 red K4s of O and examines all **319,770** fourteen-subsets.
For each survivor it enumerates all ten-subsets that could be the complement
of S0, checks the local clique conditions, and matches all 100 markings.
It independently enumerates all **15,015** eight-subsets and **10,010**
nine-subsets of the five fourteen-sets: exactly 51 eight-sets are triangle-
free, every nine-set contains a literal red triangle. Heredity rules out
every larger triangle-free set. The complete lists of maximizing masks,
not just their totals, are matched. For each marking the checker builds
the vertex set of N_red(b), inspects every pair, and reconstructs the
known red edges and the **56** remaining C-to-S1 variables.

[controls.py](controls.py) checks:

- all 1,100 labeled graphs of orders 0..5: 33,867 exact subset clique numbers
  and 1,100 complete triangle-free maximizer lists;
- all 16,384 graphs in a specified seven-vertex rooted interface: the exact
  density identity on every graph, and the bound on all 16,243 red-K5-free
  graphs; 16 counterexamples when red-K5-freeness is dropped confirm that
  this hypothesis is essential to the general inequality;
- 18 corrupt certificates and 8 malformed graphs rejected, the latter by
  both input readers. Corruptions include false scope expansion and a
  Boolean/integer alias, not only numerical changes.

From this directory, choose fresh output paths outside Git:

```sh
sha256sum -c SHA256SUMS
python3 -B analyze.py --output /scratch/new-r55-marked-density.json
python3 -B verify.py --certificate /scratch/new-r55-marked-density.json --report /scratch/new-r55-marked-density-check.json
python3 -B controls.py --certificate /scratch/new-r55-marked-density.json --report /scratch/new-r55-marked-density-controls.json
cmp certificate.json /scratch/new-r55-marked-density.json
cmp verification.json /scratch/new-r55-marked-density-check.json
cmp controls.json /scratch/new-r55-marked-density-controls.json
```

Repeat with `python3 -B -O` and distinct paths. All three final files match
byte for byte between normal and optimized Python. Normal generation,
verification and controls took 1.741374s, 1.249092s, 2.299508s; optimized runs
took 1.903526s, 1.376248s, 2.456707s. Peak child RSS over the six serial commands
was 23,156KiB. These are measured costs, not proof premises. All commands
and finite universes terminate without any timeout or UNKNOWN result.

The unformalized local-to-global inequality, enumeration completeness,
source semantics, CPython/hardware and SHA256 input identity remain the
trust base. Different author-written algorithms are **not independent peer
review**. This new exclusion has not yet received such a review.

## Dependencies and stopping boundary

The substantive new step is the triangle-free capacity bound combined with
the exact marked density equation. The five attachment domains and 100-case
relation are inherited from Discovery Net height 3058,
`bafkreibst63hpnxamz4ubsxxslyzot2duag4khta2v7nh74uxup66elzku`, source
`c281801fd5341821de0f72ab9a83442573a277b9`, and deliberately reconstructed
here for validation, not recounted as a new decomposition.

H20 is from height 2965,
`bafkreiezgfimstlpixhrdg6uqkhl45kpr2j7wbrc5hbq4jwnrath7rhvuu`, source
`3e20c2a890f21b5224fb55effbb9964a9ac33f4b`; its earlier direct graph/handoff
check has an accepted independent review. O22 is from height 3026,
`bafkreichit22jd3pb3olz2n6dgyjcn6wbbzaexgjbysuoehijgad4makva`, source
`2396381c98135e7819becd092627006262891d67`. Only this selected O is covered;
the other 15 successful deletions in its construction are not analyzed here.

The pass ends with this checkable whole-branch exclusion. No new gluing
timeout, changed-coverage search, or additional core search is started.
The best next bounded use is to screen alternative certified local O cores
with the same inequality before attempting any new full gluing. Alternatively,
changed coverage requires keeping the common-intersection term and admitting
empty/full signature issues omitted from the earlier proper-signature kernel.
Neither avenue is decided by the present certificate.
