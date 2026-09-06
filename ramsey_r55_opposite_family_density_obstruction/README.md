# A forbidden spanning core closes the entire one-addition O22 family

For the selected marked H20 route, **none of the 16 certified O22 variants
can realize red-neighborhood density 92 at the second marked vertex**.
Their 1,684 labeled marked attachments are all excluded. The earlier result
closed 100 of these; **1,584 are newly covered**, not 1,684 new cases.

The stronger reusable result is a forbidden spanning subgraph: a viable
124-red-edge O core in this selected scope cannot contain the explicit
123-edge graph J in [BASE_GRAPH.json](BASE_GRAPH.json). Consequently it must
differ from J in **at least three edge toggles**, including a deletion of
an existing J edge. No sufficiency or attainment at three toggles is claimed.

These statements retain explicit fixed-H, marked-size, coverage and
neighborhood-density assumptions. They do **not** exclude a whole degree
profile, arbitrary H20/O22 gluings, or a Ramsey(5,5;43) graph generally.
No target graph or Ramsey bound improvement is established. This closes
the finite one-addition family, not a broader replacement-core search.

## Fixed hypotheses and the common base

Use disjoint vertex sets `{r}`, H, O of orders 1,20,22. Root r is red to H
and blue to O. H is exactly the existing
[marked H20 graph](../ramsey_r55_root20_anchor_realization/GRAPH.json),
SHA256 `8d404855787227dc182d7bdc0e98751474ce6c9f1cf872abc52888477c096ccf`.
Local H vertices a=0,b=1 satisfy

```
N_H(b)={a,16,17,18,19},  d_H(b)=5,  e_H(N_H(b))=4,  d_H(a)=7.
```

Write S0=N_red(a) intersect O and S1=N_red(b) intersect O. Impose

```
|S0|=12, |S1|=14, S0 union S1=O, e_red(G[N_red(b)])=92.
```

The sizes and union give `|S0 intersect S1|=4`. The graph G has no red K5.
The main monotone lemma needs no other degree, blue-clique, edge-count or
automorphism assumptions. The forbidden-subgraph and edit consequences
add the hypothesis `e_red(O)=124`. In the retained target, this count
corresponds to root r's opposite-neighborhood density 107 blue edges.
Density 92 and coverage remain conditional search assumptions, **not
consequences asserted from the degree sequence** `20^3 21^40`.

J is the color complement of the 108-red-edge graph Q in
[the existing opposite-core input](../ramsey_r55_opposite22_realization/INPUT.json).
That input specifies a graph6 parent and six exact edge deletions, so no
network download or external solver verdict is needed. J has 123 red edges,
no red K5 and no blue K4; its SHA256 is
`01f5b3b3362cf67cac311bc574fa276f87df8afe37e4213bed430ba70cf0e147`.
The former O variants are precisely `J+e`, for the 16 red edges e of Q
whose deletion preserves Q's local clique conditions. The other 92 of
the 108 possible additions already fail the local O clique test.

We make no isomorphism-class or automorphism-orbit claim about these
labeled graphs. The necessary forbidden-subgraph condition also holds
for every relabeling of J: relabeling O and its unfixed markings preserves
the hypotheses. No symmetry computation is needed for that observation.

## Proof: the monotone density bound

Let tau(K) be the largest order of an induced red-triangle-free subset of K.
Put C={16,17,18,19}. A red triangle in `N_red(w) intersect S1`, for w in C,
would form a red K5 together with b,w. Thus, as in the preceding
[single-core density obstruction](../ramsey_r55_marked_density_obstruction),

```
e_red(G[N_red(b)])
 = 5+4+e_O(S1)+4+sum_(w in C)|N_red(w) intersect S1|
 <= 13+e_O(S1)+4*tau(O[S1]).
```

Suppose O contains J and k additional red edges. Every admissible marking
in O is also admissible in J: removing red edges cannot create a red K4
inside either Si or a red triangle in their intersection. Also

```
e_O(S1) <= e_J(S1)+k,   tau(O[S1]) <= tau(J[S1]).
```

The complete finite base data are:

| S1 mask | e_J(S1) | tau(J[S1]) | Maximum 8-subsets | Base cover markings |
|---|---:|---:|---:|---:|
| `1276fe` | 47 | 8 | 3 | 0 |
| `127ede` | 45 | 8 | 7 | 20 |
| `29bb79` | 44 | 8 | 12 | 30 |
| `39ab79` | 43 | 8 | 23 | 38 |
| `3d363d` | 44 | 8 | 8 | 34 |
| `3e363e` | 44 | 8 | 6 | 18 |

Masks use bit v for local O vertex v. The first row has no cover marking;
this separately checked zero is essential. Therefore every one of the
140 actual base markings has e_J(S1)<=45 and tau(J[S1])=8, giving

```
e_red(G[N_red(b)]) <= 13+45+k+4*8 = 90+k.
```

Density 92 requires k>=2. If O contains J and has 124 red edges, k=1,
a contradiction. Thus O must omit a J edge. If d J edges are deleted and
a missing edges added, `a-d=124-123=1`; hence the toggle distance is
`a+d=2d+1>=3`. This is a necessary lower bound, not an exact repair distance.
It does not promise a valid three-toggle core or gluing.

The argument excludes all one-addition O candidates at once, not by
extrapolating from the 16 survivors. It applies even before their local
Ramsey condition is checked. The precise boundary for changed coverage is
the common-intersection term: replace the fixed 4 above by its actual
value. This package neither removes that hypothesis nor searches it.

## Exact family relation and reusable conditional clause

[certificate.json](certificate.json) contains the six base domains, all
59 maximizing eight-subsets, and all 140 marked pairs. Base case IDs are
0..139 in numeric S1 then numeric S0 order. Each of the 16 child records
stores a 35-digit hexadecimal bit vector: bit j is one exactly when base
case j remains locally admissible in that child. All **2,240 membership
bits** are independently reconstructed. A one means local admissibility,
not full extendibility: every accepted marking fails density 92.

| Added red edge in J / deleted edge in Q | Markings | Density ceiling |
|---|---:|---:|
| (0,10) | 100 | 90 |
| (0,20) | 58 | 90 |
| (2,8) | 132 | 90 |
| (3,18) | 128 | 90 |
| (4,16) | 32 | 90 |
| (4,19) | 137 | 90 |
| (5,14) | 114 | 90 |
| (5,15) | 130 | 90 |
| (9,12) | 50 | 90 |
| (9,17) | 127 | 91 |
| (11,14) | 97 | 91 |
| (12,19) | 83 | 90 |
| (13,18) | 137 | 90 |
| (14,16) | 134 | 90 |
| (15,17) | 138 | 90 |
| (20,21) | 87 | 90 |

These are certified ceilings, not asserted attainable maxima. They use
the base triangle-free capacity, so no sharp child-capacity claim is made.
The entire old (0,10) relation is compared with its prior 100-case file;
it is regression evidence, not newly excluded work.

The necessary exclusion clause is

```
OR over uv in E(J) of NOT x_uv.
```

[conditional_cut.cnf](conditional_cut.cnf) writes that single clause with
231 O-pair variables, positive meaning red, numbered from 1 in lexicographic
`(u,v)` order for `0<=u<v<22`. It has width 123 and no auxiliaries. Its SHA256
is `067c88e4ad7b142287c5a89b6a4957fa88679dfbe71a452411a9c49281c2b3c7`.

**The CNF file encodes only this conditional consequence, not its
hypotheses and not a complete Ramsey problem.** Conjoin it only with a model
that already retains the stated fixed H, root incidences, marked sizes,
coverage, density 92, red-K5 exclusions and 124-edge O count, and rename its
O variables into that model's actual namespace. It is not an unconditional
clause for arbitrary Ramsey graphs or an instruction to replace the rest
of a gluing formula. No solver integration occurs in this milestone.

## Reproduce and verify

Use CPython 3.11.2, standard library only. From this directory, choose fresh
work paths outside Git:

```sh
sha256sum -c SHA256SUMS
python3 -B analyze.py --work /scratch/new-r55-opposite-family
python3 -B verify.py --work /scratch/new-r55-opposite-family --report /scratch/new-r55-opposite-family/verification.json
python3 -B controls.py --work /scratch/new-r55-opposite-family --report /scratch/new-r55-opposite-family/controls.json
cmp BASE_GRAPH.json /scratch/new-r55-opposite-family/BASE_GRAPH.json
cmp certificate.json /scratch/new-r55-opposite-family/certificate.json
cmp conditional_cut.cnf /scratch/new-r55-opposite-family/conditional_cut.cnf
cmp verification.json /scratch/new-r55-opposite-family/verification.json
cmp controls.json /scratch/new-r55-opposite-family/controls.json
```

Repeat with `python3 -B -O` and a distinct work path. All five final files
agree byte for byte. Normal generation/check/controls took 2.308228s,
1.543765s, 3.653924s; optimized runs took 2.458056s, 1.659704s, 3.779888s.
Peak child RSS over all six serial commands was 23,844 KiB. Every finite
run completed; no UNKNOWN, partial proof, solver or background job remains.

The producer reuses two byte-pinned public modules: the graph6 source
decoder and previous subset-clique/capacity routines. It computes clique
numbers for all 2^22 base subsets, then the six full submask universes.
Adding a nonedge uv creates precisely the triangles uvw with w a common
neighbor, and the K4s uvwx with wx a red edge in their common neighborhood.
This gives its exact child-domain and marking updates.

[verify.py](verify.py) imports neither producer nor inherited checker.
It independently decodes graph6 by byte offsets, lists all 104 base K4s,
examines all 319,770 fourteen-subsets, and reconstructs the base relation
by all `6*C(14,10)=6,006` complement choices. It checks all 18,018 eight-
subsets and 12,012 nine-subsets: 59 maximum eight-sets, no triangle-free
nine-set. It counts the literal fixed edges and 56 free entries in each
of the 140 red neighborhoods. It explicitly tests all 108 child graphs,
reconstructs the 16 valid children, enumerates their actual red K3/K4s,
and compares every child membership bit and the entire conditional clause.
It does not use the producer's edge-addition formula for this replay.

New controls cover all 1,100 labeled graphs of orders 0..5 and their 5,325
single-edge additions, 167,012 subset-capacity/density checks, 49,936 marked
pair truth assignments, and 4,166 exclusion-clause truth assignments.
They also reject 14 altered certificates, six bad cuts, six malformed
graphs and five invalid edge additions. Earlier primitive controls are
preserved in the imported source packages, not counted again here.

Certificate SHA256:
`f80b179440a8385784f989b07454135e22d8b603f5be76983b6759784ed4ca61`.
There is no solver-soundness, floating-point, graph-catalogue-completeness
or imported numerical Ramsey-bound assumption. Trust remains in the
unformalized monotonicity/density proof, finite source semantics, interpreter,
hardware and input hashes. Separate author-written algorithms are not
independent peer review; this new extension has not yet received such review.

## Dependencies and stopping boundary

The previous density lemma is Discovery Net height 3088,
`bafkreieqsw23gvx4da5mjow7ccunobxu7gtjvqui7hfbkrb5jyov2ggxmm`, source
`ba032dd048ec7ca706375d1129c1cb223ea7d7db`. The opposite-core construction
is height 3026, `bafkreichit22jd3pb3olz2n6dgyjcn6wbbzaexgjbysuoehijgad4makva`,
source `2396381c98135e7819becd092627006262891d67`. H20 is height 2965,
`bafkreiezgfimstlpixhrdg6uqkhl45kpr2j7wbrc5hbq4jwnrath7rhvuu`, source
`3e20c2a890f21b5224fb55effbb9964a9ac33f4b`. The earlier 100-case relation
is height 3058, `bafkreibst63hpnxamz4ubsxxslyzot2duag4khta2v7nh74uxup66elzku`.
Its reconstruction and the old 16-member inventory are deliberate input
checks, not priority claims for those pre-existing results.

The one-addition family is now finished. Do not run full gluing solves
for its 16 cores under these same marked/profile assumptions. A genuinely
different replacement must omit a J edge, change the H core, or alter
the explicitly retained marking/profile hypotheses. No three-toggle
search, larger repair radius, changed-coverage phase or new full gluing
is begun here. The unrestricted earlier gluing remains unresolved.
