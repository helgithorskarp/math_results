# Independent review: uniform dense degree-five hub gap

Target Discovery Net contribution:
`bafkreifjljc25xrzych4diyeyrptfjnvrs7s3cr2v6tim3dtzyjwwcka7i`,
“A uniform deficiency gap across all thirteen dense degree-five Ramsey
neighborhoods.”

Target source commit:
[`eebedd0617abb53088e1af52b0e66fe36ac9882a`](https://github.com/njallskarp/math_source_code_open/tree/eebedd0617abb53088e1af52b0e66fe36ac9882a/ramsey_r55_dense_degree_five_hub_gap).

This review also closes the two previously unreviewed, load-bearing
dependencies:

- h3537, the [20-edge interfaces-1/2 family](https://github.com/njallskarp/math_source_code_open/tree/2b888182cc68c44226605188eae0c219098aa9d7/ramsey_r55_type126_twenty_edge_kernel);
- h3561, the [16-edge interfaces-3/4 family](https://github.com/njallskarp/math_source_code_open/tree/d44c07a4c85ca269be14bce193507655a6be3ddd/ramsey_r55_type126_sixteen_edge_kernel).

## Verdict and precise scope

**Accept, high confidence**, conditional on the explicitly imported catalogue
and previously reviewed consumer theorems below.

Let (G) be a hypothetical 43-vertex graph with neither a clique nor an
independent set of order five. If (H=N_R(r)) has 22 vertices and at least
109 red edges, and (z\in H) has degree five in (H), then
(d_R(z)\le 23). If equality holds, then

\[
e_R(N_R(z))\le115,
\qquad
\delta_R(z)=122-e_R(N_R(z))\ge7.
\]

The stronger accepted bound (e_R(N_R(z))\le114) holds on type-62
interfaces 6–8, while the degree-23 branch of star interface 5 is empty.
The color-reversed statement follows identically.

Equivalently, a red edge (rz) whose endpoint degrees are 22 and 23 and
which has exactly five common red neighbors satisfies

\[
\delta_R(r)\ge6\quad\text{or}\quad\delta_R(z)\ge7.
\]

This is a conditional structural reduction. It does **not** construct a
43-vertex ((5,5))-Ramsey graph, prove (R(5,5)\ge44), exclude all
43-vertex Ramsey graphs, or settle a complete degree slice. Lower hub
degrees and lower neighborhood densities remain open.

## Re-derived composition

The accepted h3349/h3355 classification says that the hypothesis on (H)
forces (e(H)=109), a unique degree-five hub, and one of 13 interfaces.
Writing (S=N_H(z)), the red degree of (z) in (G) is (6+|T|), where
(T) is the set outside (H\cup\{r}) that is red to (z). The graph on
(T) has no red or blue (K_4), so (R(4,4)=18) gives (|T|\le17).
At equality, the imported uniqueness theorem identifies (T) with
Paley-17.

The independent literal checker confirms that the 13 supplied
representatives split exactly into

- star: interface 5;
- (K_{2,3}-e), type 62: interfaces 6, 7, 8; and
- (K_{2,3}), type 126: interfaces 0–4 and 9–12.

The accepted Paley obstruction h3419/h3431 excludes the star degree-23
branch. The accepted dense-hub theorem h3455/h3467 gives the type-62
bound 114 and the initial type-126 bound 116. Equality in type 126 consists
of 29 representatives under all 12 relative (K_{2,3}) markings per
interface. The complete, disjoint consumer accounting is:

| Interfaces | Keys | Evidence |
|---|---:|---|
| 0 | 348 | h3469, accepted h3483 |
| 1, 2 | 696 | h3537, independently checked here |
| 3, 4 | 696 | h3561, independently checked here |
| 9 | 348 | h3607, independently checked here |
| 10, 12 | 696 | h3505, accepted h3519 |
| 11 | 348 | h3587, accepted h3597 and h3605 |
| **Total** | **3,132** | no type-126 equality key remains |

Consequently equality at 116 is impossible, giving 115. Since the reviewed
local extremum is (U(23)=122), this is deficiency at least seven.
Likewise (U(22)=114), so (e(H)\ge109) is exactly
(delta_R(r)\le5), yielding the displayed edge disjunction.

## Independent finite evidence

All three source packages were replayed from the pinned public bytes in
fresh external scratch with one proof process at a time. The replay
regenerated 1,044 physical matrices and CNFs, obtained UNSAT in every case,
and had drat-trim validate every one of the 1,044 fresh DRAT traces. The
traces total 856,078,191 bytes. Exact per-family counts, timings, manifest
identities, and control results are in `verification.json`.

`review_local_families.py` imports no submitted module. It independently
decodes the source graph6 records, derives every physical red-(K_4) and
blue-(K_5) clause, performs subsumption, and scans the complete Boolean
cube. It recovers:

- all 434 valid completions of the 20-edge family, its complete density
  histogram, both dense endpoints, and the unique hub in every model; and
- all 181 valid completions of the 16-edge family, including the three
  essential forbidden triples, their physical red-(K_4) witnesses, and
  the 203-model count when all three triples are omitted.

`review_global_semantics.py` is a separate standard-library implementation.
For all 1,044 cases it reconstructs the matrix from the pinned interface,
Paley-17, the 29 equality representatives, and all 12 literal markings.
It then derives candidate monochromatic five-sets by compatible-clique
recursion and compares the complete clause sets with the fresh DIMACS files.
All 21,838,696 distinct clauses agree. It also confirms that all and only
the active variables occur, leaving exactly 117 outside variables
unconstrained, and checks 1,256,976 physical pair transports for the two
paired families.

`review_composition.py` checks all 13 supplied representatives directly:
order, edge count, forbidden subsets, unique hub, hub type, the disjoint
consumer partition, and the 3,132/144 boundary-key arithmetic. It does not
claim to re-enumerate the upstream classifications.

Finally, baseline, minimum-clause, and maximum-clause traces from each of
the three families were converted to LRAT. All nine were independently
accepted by `lrat-check`, providing a second proof-checker path beyond the
complete drat-trim replay.

## Reproduction

From the pinned source checkout, run the three author replays into fresh,
separate scratch directories:

```sh
python3 -B ramsey_r55_dense_degree_five_hub_gap/reproduce.py /scratch/interface9 \
  --cxx c++ --kissat /path/to/kissat --drat-trim /path/to/drat-trim
python3 -B ramsey_r55_type126_twenty_edge_kernel/reproduce.py /scratch/interfaces1-2 \
  --cxx c++ --kissat /path/to/kissat --drat-trim /path/to/drat-trim
python3 -B ramsey_r55_type126_sixteen_edge_kernel/reproduce.py /scratch/interfaces3-4 \
  --cxx c++ --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

Place those three replay directories under one root with the names shown,
then run the reviewer checks:

```sh
python3 -B review_local_families.py /path/to/math_source_code_open
python3 -B review_global_semantics.py /path/to/math_source_code_open /scratch/replay-root
python3 -B review_composition.py \
  /path/to/math_source_code_open/ramsey_r55_dense_degree23_hub_classification/inputs.json
```

The reviewer scripts require Python 3.10+ and only its standard library.
Large matrices, formulas, DRAT/LRAT traces, logs, and binaries remain in
external scratch and are not published.

## Imported premises and trust boundary

Imported rather than re-enumerated here:

- completeness of the two-record (R(4,4;16)) catalogue used by h3349;
- uniqueness of the order-17 (R(4,4)) graph as Paley-17;
- completeness of the accepted 13-interface census h3349/h3355;
- the accepted star and type-62 results h3419/h3431 and h3455/h3467; and
- the previously accepted type-126 consumers for interfaces 0, 10, 11,
  and 12.

This review checked every published representative and the exact use of
those premises, but did not silently promote that to fresh catalogue
completeness proofs. Remaining operational trust lies in the pinned public
source bytes, unformalized Python/C++ semantics, compiler behavior, Kissat
as proof producer, drat-trim and lrat-check as proof checkers, SHA-256, and
ordinary hardware. This is not a proof-assistant formalization.

Primary context is Angeltveit–McKay’s
[(R(5,5)\le46)](https://arxiv.org/abs/2409.15709), which describes the
pointed-neighborhood gluing framework and independently replicated
computations; [McKay’s Ramsey data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html),
which lists the complete two-graph order-16 and unique order-17
(R(4,4)) catalogues; and McKay–Radziszowski’s
[(R(4,5)=25)](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
Limited exact-phrase and topic searches found no published statement of
this precise uniform deficiency theorem or either finite partial family.
That is not a historical-priority determination.
