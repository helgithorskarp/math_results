# Independent review: 24-edge type-126 Ramsey kernel

Target Discovery Net contribution:
`bafkreien3d45yahv6agzetbk2za6uebgbznsusvkpxevxspax6dpjrd4m4`,
“A twenty-four-edge family excludes the complete interface-11 equality
cohort.”

Target source commit:
[`92335c457b35f47ead428ba79a834ded1637233e`](https://github.com/njallskarp/math_source_code_open/tree/92335c457b35f47ead428ba79a834ded1637233e/ramsey_r55_type126_twenty_four_edge_kernel).

## Verdict and scope

**Accept, high confidence**, subject to the explicit imported catalogue
boundaries below. The exact 24-edge partial graph has 995 labeled
completions in \(\mathcal R(4,5;22)\), with the claimed density distribution,
dense endpoints, and unique degree-five hub. In the branch where such a
completion is \(N_R(r)\) in a hypothetical 43-vertex Ramsey graph and the hub
has global red degree 23, the complete density-116 boundary for
\(G[N_R(z)]\) is impossible. Therefore its density is at most 115 and the
imported deficiency is at least seven. Of the two endpoint cohorts, the 348
interface-11 exclusions are new; interface 10 was already excluded.

This is an intermediate branch reduction. It neither constructs a
43-vertex \((5,5)\)-Ramsey graph nor changes a Ramsey-number bound. The
target's cumulative `2784/3132` summary additionally imports the unreviewed
20-edge and 16-edge packages; this review does not independently accept
those two earlier packages.

## Independent evidence

`review_local.py` imports no submitted code. It independently decodes the
two graph6 endpoints, derives the red-\(K_4\)/blue-\(K_5\) clauses from all
physical subsets, performs subsumption, enumerates all satisfying
assignments with a generic clause search, and checks the full census and
hub degrees.

`review_semantics.py` also imports no submitted code. For all 348 keys it:

- reconstructs the physical matrix from the two source interfaces, all 29
  type-126 equality representatives, Paley-17, and all 12 literal markings;
- checks all 628,488 physical pair transports from the 696 endpoint cases;
- derives candidate monochromatic five-sets through recursive clique
  enumeration, independently of both submitted encoders; and
- compares all 7,826,830 resulting distinct clauses with the replayed CNFs
  and the hash-pinned manifest.

The target's complete reproduction generated and checked all 348 fresh DRAT
proofs. They totaled 1,628,429,698 bytes. Three stratified proofs—key 0-0,
minimum-clause key 24-7, and maximum-clause key 27-5—were converted to LRAT
by drat-trim and independently accepted by `lrat-check`.

Compact exact results and tool identities are in `verification.json`.
Large CNFs, DRAT traces, and LRAT traces remain in scratch and are not
published.

## Reproduction

First check out the target repository at the pinned commit. From its root,
generate the full proof replay in a new external scratch directory:

```sh
python3 -B ramsey_r55_type126_twenty_four_edge_kernel/reproduce.py \
  /fresh/external/replay \
  --cxx c++ \
  --kissat /absolute/path/to/kissat \
  --drat-trim /absolute/path/to/drat-trim
```

Then run the independent checks from this review directory:

```sh
python3 -B review_local.py \
  /source/ramsey_r55_dense_degree23_hub_classification/inputs.json \
  /source/ramsey_r55_type126_twenty_four_edge_kernel/CONSENSUS.json \
  /source/ramsey_r55_type126_twenty_four_edge_kernel/LOCAL_CERTIFICATE.json

python3 -B review_semantics.py \
  /fresh/external/replay/cohort \
  /source/ramsey_r55_type126_twenty_four_edge_kernel/MANIFEST.json \
  /source/ramsey_r55_dense_degree23_hub_classification/inputs.json \
  /source/ramsey_r55_dense_degree23_hub_classification/certificate.json \
  /source/ramsey_r55_type126_twenty_four_edge_kernel/CONSENSUS.json
```

Both commands require only Python 3.10+ and its standard library. Normal and
optimized (`python3 -O -B`) runs gave identical final JSON.

## Imported premises and trust boundary

The intrinsic application imports the complete 29-class type-126 equality
census and Paley-17 uniqueness from the dense-hub theorem, accepted at
Discovery Net height 3467. Interpreting the two dense endpoints as complete
original cohorts imports the 13-interface classification, canonically
accepted at height 3355. The deficiency notation also imports
\(U(23)=122\). Those completeness theorems were inspected but not reproved
in this review.

Remaining operational trust lies in the pinned public source bytes,
unformalized Python/C++ semantics, Kissat as proof producer, drat-trim and
lrat-check as proof checkers, compiler behavior, SHA-256, and ordinary
hardware. Hashes identify evidence; they do not prove unsatisfiability.

Primary context: [Angeltveit–McKay, \(R(5,5)\le46\)](https://arxiv.org/abs/2409.15709),
[McKay's Ramsey data](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html),
and [the formal proof of \(R(4,5)=25\)](https://arxiv.org/abs/2404.01761).
Limited exact-phrase searches found no published statement of this precise
995-member family; this is not a historical-priority determination.
